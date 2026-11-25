"""pipeline.run: порядок этапов, громкий итог при пропусках, пересборка, smoke без ключа."""
import pytest

from contracts import models as m
from pipeline import run
from pipeline.common import io, paths


@pytest.fixture
def out(tmp_path, monkeypatch):
    monkeypatch.setenv("OUT_DIR", str(tmp_path))
    monkeypatch.setenv("LLM_OFFLINE", "")   # smoke/run пишут в os.environ — monkeypatch вернёт как было
    monkeypatch.setenv("CH", "")
    return tmp_path


def test_smoke_offline_writes_core_outputs(out, monkeypatch):
    calls = []
    monkeypatch.setattr(run, "external", lambda rep, mod, *a: calls.append((mod, *a)) or True)
    assert run.main(["--smoke"]) == 0
    d = out / run.SMOKE_CH
    assert io.load(m.ChapterUnits, d / "units.json").units
    assert io.load(m.Layer, d / "layer.json").nodes
    assert [c[0] for c in calls] == ["pipeline.verify.run", "pipeline.illus.run", "pipeline.course.build"]


def test_missing_module_makes_run_fail_loudly(out):
    rep = run.Report()
    assert run.external(rep, "pipeline.no_such_module", "--ch", "x") is False
    assert rep.done("t") == 1 and "нет модуля" in rep.problems[0]


def test_core_failure_stops_chain(out, monkeypatch):
    from pipeline.common import config
    from pipeline.structure import run as structure
    monkeypatch.setattr(run, "external", lambda *a: pytest.fail("дальше этапов ядра идти нельзя"))

    def boom(spec):
        raise RuntimeError("нет ключа")
    monkeypatch.setattr(structure, "run", boom)
    spec = config.resolve(md=str(run.MINI / "chapter.md"), ch="t1")
    from pipeline.ingest import run as ingest
    monkeypatch.setattr(ingest, "run", lambda spec: None)
    assert run.run_all(spec) == 1


def test_rebuild_finds_chapter_and_video(out, monkeypatch):
    d = out / "chx"
    d.mkdir()
    for name in ("layer.json", "routing.json"):
        (d / name).write_text((run.MINI / name).read_text(encoding="utf-8"), encoding="utf-8")
    node = io.load(m.Layer, d / "layer.json").nodes[0].id
    (d / "videos" / node).mkdir(parents=True)
    calls = []
    monkeypatch.setattr(run, "external", lambda rep, mod, *a: calls.append((mod, *a)) or True)
    assert run.main(["--rebuild", node]) == 0
    assert calls == [("pipeline.course.build", "--ch", "chx", "--node", node),
                     ("pipeline.video.build", "--ch", "chx", "--node", node, "--format", "long")]
    with pytest.raises(ValueError, match="CH="):
        run.find_chapter("no.such.node")
