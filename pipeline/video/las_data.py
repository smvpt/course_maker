"""Набор данных для T2: описание (dataset.json) + LAS через lasio.

Описание набора данных — JSON рядом с LAS или где угодно (путь к LAS — относительно описания):
    kind: "synthetic" | "real"; las; sha256; source; license и attribution (обязательны для real); well;
    uwi (если задан — сверяется с UWI в LAS); interval_m: [верх, низ]; units: {мнемоника: единица как в LAS};
    curve_types: {мнемоника: "measured" | "interpreted"} (обязательно для real);
    диаметр ствола — borehole_diameter_m (+ borehole_diameter_source) ИЛИ borehole_diameter_from_curve
    (мнемоника кавернограммы: медиана на interval_m с переводом единиц длины); note.
Подключить реальный фрагмент (например, Volve) — положить LAS и написать к нему такое описание; код не меняется.

Проверки: хэш файла, скважина, единица и монотонность глубины, единицы кривых по описанию и по
допустимому списку шаблона. Пропуски (NULL) остаются NaN — нулями не заменяются. Кривая, единица
которой не подтверждена описанием, в набор не попадает. Метка «реальные данные» — только для
kind = real при совпавших хэше и скважине, с указанными источником и лицензией.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from pipeline.video.inputs import VideoInputError

REQUIRED = ("kind", "las", "sha256", "source", "well", "interval_m", "units")


@dataclass
class Dataset:
    kind: str
    label: str                     # метка происхождения кадров с этими данными
    real_verified: bool
    well: str
    depth: np.ndarray              # м, строго возрастает
    curves: dict[str, np.ndarray]  # мнемоника → значения (NaN = пропуск)
    units: dict[str, str]          # мнемоника → единица как в LAS (верхний регистр)
    curve_types: dict[str, str]    # мнемоника → measured | interpreted | synthetic
    attribution: str               # как ссылаться на данные (в кадре)
    interval: tuple[float, float]
    borehole_diameter_m: float | None
    provenance: dict = field(default_factory=dict)


def _fail(problems: list[str], where: Path) -> None:
    err = VideoInputError(f"набор данных {where} некорректен:\n- " + "\n- ".join(problems))
    err.problems = problems
    raise err


def load_dataset(desc_path: Path, cfg: dict) -> Dataset:
    desc_path = Path(desc_path)
    if not desc_path.is_file():
        raise VideoInputError(f"описание набора данных не найдено: {desc_path}")
    try:
        d = json.loads(desc_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise VideoInputError(f"описание набора данных {desc_path} — не JSON: {e}") from e
    problems = [f"нет поля {k}" for k in REQUIRED if k not in d]
    if d.get("kind") not in ("synthetic", "real"):
        problems.append(f"kind должен быть synthetic или real, получено {d.get('kind')!r}")
    if problems:
        _fail(problems, desc_path)
    if d["kind"] == "real":
        for key in ("license", "attribution"):
            if not str(d.get(key) or "").strip():
                problems.append(f"для реальных данных нужно поле {key} — без него происхождение не подтверждено")
    if not str(d["source"]).strip():
        problems.append("пустой source")

    las_path = (desc_path.parent / d["las"]).resolve()
    if not las_path.is_file():
        _fail(problems + [f"LAS не найден: {las_path}"], desc_path)
    sha = hashlib.sha256(las_path.read_bytes()).hexdigest()
    if sha != d["sha256"]:
        problems.append(f"sha256 файла {las_path.name} = {sha}, а в описании {d['sha256']} — файл не тот или изменён")

    import lasio
    try:
        las = lasio.read(str(las_path))
    except Exception as e:   # lasio бросает разные исключения на битых файлах
        _fail(problems + [f"lasio не прочитал {las_path.name}: {type(e).__name__}: {e}"], desc_path)
    well = str(las.well["WELL"].value).strip() if "WELL" in las.well else ""
    if well != str(d["well"]).strip():
        problems.append(f"скважина в LAS (WELL) «{well}», а в описании «{d['well']}»")
    uwi = str(las.well["UWI"].value).strip() if "UWI" in las.well else ""
    if d.get("uwi") is not None and uwi != str(d["uwi"]).strip():
        problems.append(f"UWI в LAS «{uwi}», а в описании «{d['uwi']}»")

    declared = {k.upper(): str(v).upper() for k, v in d["units"].items()}
    idx = las.curves[0]
    depth_unit = (idx.unit or "").upper()
    factor = cfg["depth_units"].get(depth_unit)
    if factor is None:
        problems.append(f"неизвестная единица глубины «{idx.unit}» у {idx.mnemonic}; допустимы {sorted(cfg['depth_units'])}")
    if declared.get(idx.mnemonic.upper()) != depth_unit:
        problems.append(f"единица глубины {idx.mnemonic} в LAS «{idx.unit}», в описании «{declared.get(idx.mnemonic.upper())}»")
    depth = np.asarray(las.index, dtype=float) * (factor or 1.0)
    if depth.size < 2 or np.any(~np.isfinite(depth)) or np.any(np.diff(depth) <= 0):
        problems.append("глубина должна строго возрастать без пропусков")

    allowed_units = {u for k in cfg["curve_kinds"].values() for u in k["units"]}
    curves, units = {}, {}
    for c in las.curves[1:]:
        m, u = c.mnemonic.upper(), (c.unit or "").upper()
        if m not in declared:
            continue                                   # единица не подтверждена описанием — не используем
        if declared[m] != u:
            problems.append(f"кривая {m}: единица в LAS «{c.unit}», в описании «{declared[m]}»")
            continue
        if u not in allowed_units:
            problems.append(f"кривая {m}: единица «{c.unit}» не из допустимых для кривых T2 — не угадываем")
            continue
        curves[m], units[m] = np.asarray(c.data, dtype=float), u
    for m in declared:
        if m != idx.mnemonic.upper() and m not in curves and not any(m in p for p in problems):
            problems.append(f"кривой {m} из описания нет в LAS")

    types = {k.upper(): v for k, v in (d.get("curve_types") or {}).items()}
    if d["kind"] == "real":
        for m in declared:
            if m != idx.mnemonic.upper() and types.get(m) not in ("measured", "interpreted"):
                problems.append(f"кривая {m}: для реальных данных укажите curve_types — measured или interpreted")
    curve_types = {m: (types.get(m) if d["kind"] == "real" else "synthetic") for m in curves}

    top, bottom = (float(x) for x in d["interval_m"])
    if not top < bottom:
        problems.append(f"интервал {d['interval_m']}: верх должен быть меньше низа")
    elif depth.size and (top < depth.min() - 1e-9 or bottom > depth.max() + 1e-9):
        problems.append(f"интервал {d['interval_m']} выходит за глубины LAS {depth.min():g}–{depth.max():g} м")
    diam = d.get("borehole_diameter_m")
    diam_source = d.get("borehole_diameter_source")
    from_curve = d.get("borehole_diameter_from_curve")
    if diam is not None and from_curve is not None:
        problems.append("заданы и borehole_diameter_m, и borehole_diameter_from_curve — нужен один источник")
    elif from_curve is not None:
        cm = str(from_curve).upper()
        factor = cfg.get("length_units", {}).get(units.get(cm, ""))
        if cm not in curves:
            problems.append(f"borehole_diameter_from_curve: кривой {cm} нет среди кривых с подтверждённой единицей")
        elif units[cm] not in cfg["curve_kinds"].get("CALIPER", {}).get("units", []):
            problems.append(f"borehole_diameter_from_curve: единица {units[cm]} — не единица кавернограммы")
        elif factor is None:
            problems.append(f"borehole_diameter_from_curve: единица длины {units[cm]} неизвестна — не угадываем")
        elif curve_types.get(cm) == "interpreted":
            problems.append(f"borehole_diameter_from_curve: {cm} — результат интерпретации, нужна измеренная кривая")
        elif top < bottom:
            sel = (depth >= top) & (depth <= bottom)
            v = curves[cm][sel]
            v = v[np.isfinite(v)]
            if v.size == 0:
                problems.append(f"borehole_diameter_from_curve: у {cm} нет значений на интервале")
            else:
                diam = float(np.median(v)) * factor
                diam_source = (f"медиана кривой {cm} на {top:g}–{bottom:g} м: {np.median(v):.4g} {units[cm]} "
                               f"({v.size} отсчётов, от {v.min():.4g} до {v.max():.4g})")
    if diam is not None and (isinstance(diam, bool) or not isinstance(diam, (int, float)) or diam <= 0):
        problems.append(f"borehole_diameter_m должен быть числом > 0, получено {diam!r}")
    if problems:
        _fail(problems, desc_path)

    real = d["kind"] == "real"
    attribution = str(d.get("attribution") or ("данные синтетические, условные" if not real else "")).strip()
    return Dataset(
        kind=d["kind"], label="реальные данные" if real else "симуляция", real_verified=real, well=well,
        depth=depth, curves=curves, units=units, curve_types=curve_types, attribution=attribution,
        interval=(top, bottom),
        borehole_diameter_m=float(diam) if diam is not None else None,
        provenance={"kind": d["kind"], "source": d["source"], "license": d.get("license"),
                    "attribution": attribution, "file": las_path.name, "sha256": sha, "well": well,
                    "uwi": uwi or None, "interval_m": [top, bottom],
                    "units": {idx.mnemonic.upper(): depth_unit, **units}, "curve_types": curve_types,
                    "borehole_diameter_m": float(diam) if diam is not None else None,
                    "borehole_diameter_source": diam_source, "note": d.get("note"),
                    "download": d.get("download"), "description": str(desc_path)})
