"""Чтение LAS по описанию набора данных: глубины, единицы, пропуски, происхождение."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from pipeline.video.inputs import VideoInputError
from pipeline.video.las_data import load_dataset
from pipeline.video.templates import load_template_config

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "fixtures" / "video" / "t2_demo"
CFG = load_template_config(ROOT / "domain" / "geology" / "templates", "T2")
LAS_TEXT = (FIX / "synthetic_well.las").read_text(encoding="ascii")
DESC = json.loads((FIX / "dataset.json").read_text(encoding="utf-8"))


def _make(tmp_path, las_text=LAS_TEXT, fix_hash=True, **desc_changes):
    las = tmp_path / "w.las"
    las.write_bytes(las_text.encode("ascii"))
    d = dict(DESC, las="w.las", **desc_changes)
    if fix_hash:
        d["sha256"] = hashlib.sha256(las.read_bytes()).hexdigest()
    p = tmp_path / "dataset.json"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return p


def test_synthetic_fixture_loads_as_simulation():
    ds = load_dataset(FIX / "dataset.json", CFG)
    assert ds.label == "симуляция" and ds.kind == "synthetic" and not ds.real_verified
    assert ds.well == "SYNTH-1" and ds.depth[0] == 1000 and ds.depth[-1] == 1100
    assert set(ds.curves) == {"GR", "RT", "NPHI"} and ds.units["RT"] == "OHMM"
    assert ds.provenance["file"] == "synthetic_well.las" and ds.provenance["interval_m"] == [1000, 1100]


def test_gaps_stay_gaps_not_zeros():
    ds = load_dataset(FIX / "dataset.json", CFG)
    rt, d = ds.curves["RT"], ds.depth
    gap = (d >= 1024) & (d <= 1026)
    assert np.all(np.isnan(rt[gap])) and gap.sum() == 5
    assert not np.any(rt[~gap] == 0)


@pytest.mark.parametrize("edit,needle", [
    (lambda t: t.replace(" GR  .API ", " GR  .UNKNOWNU "), "GR"),                        # единица не как в описании
    (lambda t: t.replace(" DEPT.M ", " DEPT.KM "), "глубин"),                            # неизвестная единица глубины
    (lambda t: t.replace(" NPHI.V/V    : SYNTHETIC NEUTRON POROSITY\n", "").replace("      NPHI", "")
     .replace(" ~A", "~A"), "NPHI"),
])
def test_bad_las_header(tmp_path, edit, needle):
    text = edit(LAS_TEXT)
    if needle == "NPHI":   # убираем и последний столбец данных
        text = "\n".join(" ".join(l.split()[:3]) if l[:1].isspace() and l.split()[0][0].isdigit() else l
                         for l in text.splitlines()) + "\n"
    with pytest.raises(VideoInputError, match=needle):
        load_dataset(_make(tmp_path, text), CFG)


def test_unit_declared_differently_in_description(tmp_path):
    with pytest.raises(VideoInputError, match="RT"):
        load_dataset(_make(tmp_path, units={**DESC["units"], "RT": "OHM.M"}), CFG)


def test_curve_without_declared_unit_is_not_available(tmp_path):
    ds = load_dataset(_make(tmp_path, units={k: v for k, v in DESC["units"].items() if k != "NPHI"}), CFG)
    assert "NPHI" not in ds.curves                 # единица не подтверждена описанием — кривую не берём


def test_non_monotonic_depth(tmp_path):
    lines = LAS_TEXT.splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith("~A")) + 10
    lines[i], lines[i + 1] = lines[i + 1], lines[i]
    with pytest.raises(VideoInputError, match="глубин"):
        load_dataset(_make(tmp_path, "\n".join(lines) + "\n"), CFG)


def test_hash_mismatch(tmp_path):
    with pytest.raises(VideoInputError, match="sha256"):
        load_dataset(_make(tmp_path, fix_hash=False, sha256="0" * 64), CFG)


def test_well_mismatch(tmp_path):
    with pytest.raises(VideoInputError, match="WELL"):
        load_dataset(_make(tmp_path, well="15/9-F-11"), CFG)


def test_interval_outside_data(tmp_path):
    with pytest.raises(VideoInputError, match="интервал"):
        load_dataset(_make(tmp_path, interval_m=[900, 1100]), CFG)


def test_real_label_needs_confirmed_origin(tmp_path):
    with pytest.raises(VideoInputError, match="license"):
        load_dataset(_make(tmp_path, kind="real", license=None), CFG)
    ds = load_dataset(_make(tmp_path, kind="real", license="условная лицензия для теста"), CFG)
    assert ds.label == "реальные данные" and ds.real_verified
    assert {"source", "file", "well", "interval_m", "units", "sha256"} <= set(ds.provenance)


def test_bad_description(tmp_path):
    p = tmp_path / "dataset.json"
    p.write_text(json.dumps({"kind": "maybe"}), encoding="utf-8")
    with pytest.raises(VideoInputError, match="kind"):
        load_dataset(p, CFG)
    with pytest.raises(VideoInputError, match="не найден"):
        load_dataset(tmp_path / "nope.json", CFG)
