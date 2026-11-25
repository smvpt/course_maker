"""T2 «Каротаж»: проверка параметров SceneSpec до рендера и чистые функции сцены.

Описание и ограничения — domain/<домен>/templates/T2.json; данные — набор (dataset.json + LAS).
Одна переменная — глубина прибора d (м, растёт вниз) — задаёт положение прибора, раскрытие
кривых и колонки решения: всё через depth_frac / revealed / rule_state.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np

from contracts.models import SceneSpec, Script
from pipeline.video.inputs import VideoInputError
from pipeline.video.las_data import Dataset, load_dataset

OPS = {"<": np.less, ">": np.greater, "<=": np.less_equal, ">=": np.greater_equal}
RULE_STATUS = {"из узла": "правило из узла", "условное": "условное правило"}
ROOT = Path(__file__).resolve().parents[2]


def resolve_dataset_path(value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else ROOT / p


def _num(v) -> bool:
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v)


def _exag_txt(k: float) -> str:
    return str(int(k)) if float(k).is_integer() else str(k).replace(".", ",")


def _has_number(text: str, num: str) -> bool:
    return re.search(rf"(?<![\d,.]){re.escape(num)}(?![\d,.])", text) is not None


def prepare(spec: SceneSpec, script: Script, cfg: dict) -> dict:
    problems: list[str] = []
    p = dict(spec.params)
    unknown = sorted(set(p) - set(cfg["params"]))
    if unknown:
        problems.append(f"неизвестные параметры T2: {unknown}; допустимы {sorted(cfg['params'])}")
    for key, d in cfg["params"].items():
        if key not in p:
            if d.get("required"):
                problems.append(f"нет обязательного параметра params.{key} ({d['meaning']})")
            else:
                p[key] = d.get("default")

    ds: Dataset | None = None
    if isinstance(p.get("dataset"), str):
        try:
            ds = load_dataset(resolve_dataset_path(p["dataset"]), cfg)
        except VideoInputError as e:
            problems += [f"набор данных: {x}" for x in getattr(e, "problems", [str(e)])]
    elif "dataset" in p:
        problems.append("params.dataset — путь к описанию набора данных (строка)")

    lim = cfg["limits"]
    curves_in = p.get("curves")
    curves: list[dict] = []
    if not isinstance(curves_in, list) or not 1 <= len(curves_in) <= lim["max_curves"]:
        problems.append(f"params.curves — список из 1–{lim['max_curves']} кривых, получено {curves_in!r}")
        curves_in = []
    for i, c in enumerate(curves_in):
        if not isinstance(c, dict):
            problems.append(f"params.curves[{i}] — объект {{mnemonic, kind, unit, label}}")
            continue
        m, kind, unit, label = (str(c.get(k, "")).strip() for k in ("mnemonic", "kind", "unit", "label"))
        m, unit = m.upper(), unit.upper()
        kcfg = cfg["curve_kinds"].get(kind)
        if kcfg is None:
            problems.append(f"кривая {m}: kind «{kind}» не из {sorted(cfg['curve_kinds'])}")
            continue
        if unit not in kcfg["units"]:
            problems.append(f"кривая {m}: единица «{unit}» недопустима для {kind}; допустимы {kcfg['units']}")
        if not label or len(label) > lim["max_label_chars"]:
            problems.append(f"кривая {m}: label — обозначение до {lim['max_label_chars']} символов")
        if ds is not None:
            if m not in ds.curves:
                problems.append(f"кривой {m} нет в наборе данных (с подтверждённой единицей); есть {sorted(ds.curves)}")
                continue
            if ds.units[m] != unit:
                problems.append(f"кривая {m}: в спецификации единица «{unit}», в LAS «{ds.units[m]}»")
            if ds.curve_types.get(m) == "interpreted":
                problems.append(f"кривая {m} — результат интерпретации, а не измерение: на трек «измерение» "
                                f"ставятся только измеренные кривые")
        curves.append({"mnemonic": m, "kind": kind, "unit": unit, "label": label, "log": kcfg["log"],
                       "unit_display": cfg["unit_display"].get(unit, unit)})
    if len({c["mnemonic"] for c in curves}) != len(curves):
        problems.append("кривые в params.curves повторяются")

    iv = p.get("interval_m")
    top = bottom = None
    if not (isinstance(iv, list) and len(iv) == 2 and all(_num(x) for x in iv) and iv[0] < iv[1]):
        problems.append(f"params.interval_m — [верх, низ] в метрах, верх < низ; получено {iv!r}")
    else:
        top, bottom = float(iv[0]), float(iv[1])
        if bottom - top < lim["min_interval_m"]:
            problems.append(f"интервал короче {lim['min_interval_m']} м")
        if ds is not None and (top < ds.interval[0] or bottom > ds.interval[1]):
            problems.append(f"интервал {iv} выходит за интервал набора данных {list(ds.interval)}")

    if ds is not None and top is not None:
        sel = (ds.depth >= top) & (ds.depth <= bottom)
        for c in curves:
            if c["mnemonic"] in ds.curves:
                v = ds.curves[c["mnemonic"]][sel]
                ok = np.isfinite(v)
                if ok.mean() < lim["min_valid_fraction"]:
                    problems.append(f"кривая {c['mnemonic']}: в интервале {ok.mean():.0%} значений, "
                                    f"нужно не меньше {lim['min_valid_fraction']:.0%}")
                elif c["log"] and np.any(v[ok] <= 0):
                    problems.append(f"кривая {c['mnemonic']}: для логарифмической шкалы нужны значения > 0")
                else:
                    c["range"] = display_range(v, c["log"])

    rule = p.get("rule")
    mnems = {c["mnemonic"] for c in curves}
    if not isinstance(rule, dict):
        problems.append("params.rule — объект {status, conditions, conclusion, caveat}")
        rule = {}
    else:
        if rule.get("status") not in RULE_STATUS:
            problems.append(f"rule.status — «из узла» или «условное», получено {rule.get('status')!r}")
        conds = rule.get("conditions")
        if not isinstance(conds, list) or not conds:
            problems.append("rule.conditions — непустой список {curve, op, value}")
            conds = []
        for c in conds:
            if not isinstance(c, dict) or str(c.get("curve", "")).upper() not in mnems or c.get("op") not in OPS \
                    or not _num(c.get("value")):
                problems.append(f"условие {c!r}: curve — одна из {sorted(mnems)}, op — {sorted(OPS)}, value — число")
        concl = str(rule.get("conclusion") or "").strip()
        if not concl:
            problems.append("rule.conclusion — вывод обязателен")
        bad = [w for w in cfg["forbidden_conclusion_words"] if w in concl.lower()]
        if bad:
            problems.append(f"rule.conclusion «{concl}» утверждает больше, чем даёт правило ({bad}): "
                            f"высокое сопротивление — не доказательство нефти")
        if not str(rule.get("caveat") or "").strip():
            problems.append("rule.caveat — ограничение правила обязательно")

    shots = {s.id: s for s in spec.shots}
    evolve = p.get("evolve_shot_ids")
    if evolve is None:
        evolve = list(shots)
    elif not isinstance(evolve, list) or not evolve or any(e not in shots for e in evolve):
        problems.append(f"params.evolve_shot_ids — непустой список id кадров из {sorted(shots)}, получено {evolve!r}")
        evolve = []

    data_label = ds.label if ds is not None else None
    for s in spec.shots:
        if s.frame_class != "A":
            problems.append(f"кадр {s.id}: T2 показывает данные — класс A, а не {s.frame_class}")
        if data_label and s.label != data_label:
            why = "" if ds.real_verified else " (происхождение набора не подтверждено как реальное)"
            problems.append(f"кадр {s.id}: метка «{s.label}», а данные — «{data_label}»{why}")

    diam = p.get("borehole_diameter_m")
    if ds is not None:
        if ds.borehole_diameter_m is None:
            problems.append("в описании набора данных нет borehole_diameter_m — ствол без размера не рисуем")
        elif not _num(diam) or not math.isclose(float(diam), ds.borehole_diameter_m, rel_tol=1e-6):
            problems.append(f"borehole_diameter_m {diam!r} не совпадает с набором данных ({ds.borehole_diameter_m})")
    k = p.get("borehole_exaggeration")
    if not _num(k) or k < 1:
        problems.append(f"params.borehole_exaggeration — число ≥ 1, получено {k!r}")
        k = None
    disp = cfg["display"]
    if k is not None and _num(diam) and top is not None:
        px_per_m = disp["nominal_panel_height_px"] / (bottom - top)
        width_px = float(diam) * k * px_per_m
        if width_px > lim["max_borehole_fraction_of_panel"] * disp["nominal_borehole_panel_px"]:
            problems.append(f"ствол при увеличении {k} шире {lim['max_borehole_fraction_of_panel']} панели")
    ts = spec.true_scale_shot_id
    if ts is not None and ts not in shots:
        problems.append(f"true_scale_shot_id {ts} — нет такого кадра")
    if k is not None:
        kt = _exag_txt(k)
        plaqued = [s.id for s in spec.shots if s.plaque]
        if k == 1 and plaqued:
            problems.append(f"borehole_exaggeration = 1 (всё в истинном масштабе), а у кадров {plaqued} плашка")
        if k > 1:
            for s in spec.shots:
                if s.plaque and not _has_number(s.plaque, kt):
                    problems.append(f"кадр {s.id}: на плашке нет числа увеличения {kt}")
            if not any(_has_number(e, kt) for e in spec.exaggerations):
                problems.append(f"в exaggerations нет преувеличения ствола с числом {kt}")
            if ts is None:
                problems.append("ствол увеличен — нужен кадр в истинном масштабе (true_scale_shot_id)")
            elif ts in shots and shots[ts].plaque:
                problems.append(f"кадр истинного масштаба {ts} не может иметь плашку")
            if not plaqued:
                problems.append(f"ствол увеличен в {kt} раз, но ни у одного кадра нет плашки")

    if problems:
        err = VideoInputError("параметры T2 некорректны:\n- " + "\n- ".join(problems))
        err.problems = problems
        raise err

    sel = (ds.depth >= top) & (ds.depth <= bottom)
    depth = ds.depth[sel]
    values = {c["mnemonic"]: ds.curves[c["mnemonic"]][sel] for c in curves}
    phrase_shot = {pid: s.id for s in spec.shots for pid in s.phrase_ids}
    conds = [{"curve": str(c["curve"]).upper(), "op": c["op"], "value": float(c["value"])} for c in rule["conditions"]]
    return {
        "dataset": ds, "depth": depth, "values": values, "curves": curves, "top": top, "bottom": bottom,
        "rule": {**rule, "conditions": conds, "status_label": RULE_STATUS[rule["status"]]},
        "rule_state": rule_state(depth, values, conds),
        "borehole_diameter_m": float(diam), "exaggeration": float(k),
        "exaggerated_shots": {s.id for s in spec.shots if s.plaque}, "true_scale_shot_id": ts,
        "evolve_phrase_ids": {pid for pid, sid in phrase_shot.items() if sid in evolve},
    }


def check(spec: SceneSpec, script: Script, cfg: dict) -> list[str]:
    try:
        prepare(spec, script, cfg)
    except VideoInputError as e:
        return [f"T2: {x}" for x in getattr(e, "problems", [str(e)])]
    return []


# ---------------------------------------------------------------- чистые функции сцены

def depth_frac(prep: dict, d: float) -> float:
    """Доля глубины в интервале: 0 — верх, 1 — низ (глубина растёт вниз)."""
    return (d - prep["top"]) / (prep["bottom"] - prep["top"])


def revealed(prep: dict, mnemonic: str, d: float) -> tuple[np.ndarray, np.ndarray]:
    """Отсчёты кривой не глубже d (NaN — пропуск, остаётся пропуском)."""
    m = prep["depth"] <= d + 1e-9
    return prep["depth"][m], prep["values"][mnemonic][m]


def value_at(prep: dict, mnemonic: str, d: float) -> float:
    """Значение на ближайшей к d глубине (NaN, если там пропуск). Без интерполяции через пропуск."""
    i = int(np.argmin(np.abs(prep["depth"] - d)))
    return float(prep["values"][mnemonic][i])


def rule_state(depth: np.ndarray, values: dict, conds: list[dict]) -> np.ndarray:
    """1 — все условия выполнены; 0 — хотя бы одно известное условие не выполнено;
    -1 — нет данных: известные условия выполнены, но какое-то нельзя проверить из-за пропуска."""
    any_false = np.zeros(depth.shape, dtype=bool)
    any_nan = np.zeros(depth.shape, dtype=bool)
    for c in conds:
        v = values[c["curve"]]
        fin = np.isfinite(v)
        with np.errstate(invalid="ignore"):
            ok = OPS[c["op"]](v, c["value"])
        any_nan |= ~fin
        any_false |= fin & ~ok
    return np.where(any_false, 0, np.where(any_nan, -1, 1))


def display_range(values: np.ndarray, log: bool) -> tuple[float, float]:
    """Шкала трека по значениям без пропусков. Постоянная кривая: лог — в 2 раза в обе стороны
    (диапазон всегда > 0), линейная — ±1."""
    v = values[np.isfinite(values)]
    lo, hi = float(np.min(v)), float(np.max(v))
    if hi > lo:
        return lo, hi
    return (lo / 2, hi * 2) if log else (lo - 1, hi + 1)


def decision_rows(depth: np.ndarray, state: np.ndarray, top: float, bottom: float, n_rows: int) -> np.ndarray:
    """Состояние правила для n_rows строк, равномерных по глубине [top, bottom].

    Каждый отсчёт LAS занимает ячейку от середины до предыдущего до середины до следующего
    (первый — от своей глубины, последний — до своей), поэтому неравномерный шаг и пропуски
    ложатся на фактические глубины. Строки вне записи — -2 (нет отсчёта)."""
    centers = top + (np.arange(n_rows) + 0.5) * (bottom - top) / n_rows
    mids = (depth[1:] + depth[:-1]) / 2
    idx = np.searchsorted(mids, centers, side="right")
    rows = state[idx].astype(int)
    rows[(centers < depth[0]) | (centers > depth[-1])] = -2
    return rows


def curve_frac(value: np.ndarray, rng: tuple[float, float], log: bool) -> np.ndarray:
    """Положение значения на треке: 0 — левый край, 1 — правый."""
    lo, hi = rng
    if log:
        return (np.log10(value) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
    return (value - lo) / (hi - lo)
