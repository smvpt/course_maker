"""T1: проверка параметров SceneSpec до рендера и подготовка данных сцены.

Описание, состав параметров и настройки показа — domain/<домен>/templates/T1.json.
Код не знает ни автора, ни главы: все числа приходят из SceneSpec.params.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np

from contracts.models import SceneSpec, Script
from pipeline.video.inputs import VideoInputError
from pipeline.video.t1_model import PressureModel

ALLOWED_CLASSES = {"A", "B"}


def load_config(templates_dir: Path) -> dict:
    path = Path(templates_dir) / "T1.json"
    if not path.is_file():
        raise VideoInputError(f"нет описания шаблона T1: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def fmt_num(v: float, digits: int = 3) -> str:
    """Число для кадра: значащие цифры, десятичная запятая, без хвостовых нулей."""
    if v == 0:
        return "0"
    s = f"{v:.{digits}g}"
    if "e" in s:
        s = f"{v:.{max(0, digits - 1 - int(math.floor(math.log10(abs(v)))))}f}"
    return s.replace(".", ",")


def nice_ceil(v: float) -> float:
    """Ближайшее сверху «круглое» число 1, 2, 2,5, 5 × 10^n."""
    e = 10 ** math.floor(math.log10(v))
    for m in (1, 2, 2.5, 5, 10):
        if m * e >= v * (1 - 1e-12):
            return m * e
    return 10 * e


def time_unit(t_end_s: float) -> tuple[str, float]:
    if t_end_s < 2 * 3600:
        return "мин", 60.0
    if t_end_s < 3 * 86400:
        return "ч", 3600.0
    return "сут", 86400.0


def field_values(prep: dict, t: float) -> tuple[np.ndarray, np.ndarray]:
    """Карта Δp на сетке плана [-r_max, r_max]²; у скважины (r < r_min) значение берётся при r_min."""
    xs = np.linspace(-prep["r_max"], prep["r_max"], prep["grid"])
    r = np.hypot(xs[None, :], xs[:, None])
    return prep["model"].delta_p(np.maximum(r, prep["r_min"]), t), xs


def profile(prep: dict, t: float, n: int = 240) -> tuple[np.ndarray, np.ndarray]:
    """График Δp(r) на [r_min, r_max] — та же функция, что и у карты."""
    r = np.geomspace(prep["r_min"], prep["r_max"], n)
    return r, prep["model"].delta_p(r, t)


def _number(params: dict, key: str, problems: list[str]) -> float | None:
    v = params.get(key)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0:
        problems.append(f"params.{key} должно быть числом > 0, получено {v!r}")
        return None
    return float(v)


def prepare(spec: SceneSpec, script: Script, cfg: dict) -> dict:
    """Проверяет параметры и связи кадров; возвращает всё, что нужно сцене. Ошибки — списком."""
    problems: list[str] = []
    p = dict(spec.params)
    known = set(cfg["params"])
    unknown = sorted(set(p) - known)
    if unknown:
        problems.append(f"неизвестные параметры T1: {unknown}; допустимы {sorted(known)}")
    for key, d in cfg["params"].items():
        if key not in p:
            if d.get("required"):
                problems.append(f"нет обязательного параметра params.{key} ({d['meaning']}, {d.get('unit', '')})")
            else:
                p[key] = d.get("default")
    vals = {k: _number(p, k, problems) for k, d in cfg["params"].items() if d.get("required") and k in p}
    k = p.get("well_exaggeration")
    if isinstance(k, bool) or not isinstance(k, (int, float)) or not math.isfinite(k) or k < 1:
        problems.append(f"params.well_exaggeration должно быть числом ≥ 1, получено {k!r}")
        k = None

    shots = {s.id: s for s in spec.shots}
    evolve = p.get("evolve_shot_ids")
    if evolve is None:
        evolve = list(shots)
    elif not isinstance(evolve, list) or not evolve or any(e not in shots for e in evolve):
        problems.append(f"params.evolve_shot_ids — непустой список id кадров из {sorted(shots)}, получено {evolve!r}")
        evolve = []

    for s in spec.shots:
        if s.label != "симуляция" or s.frame_class not in ALLOWED_CLASSES:
            problems.append(f"кадр {s.id}: T1 рисует расчёт — нужен класс A или B с меткой «симуляция», "
                            f"а не {s.frame_class}/«{s.label}»")
    ts = spec.true_scale_shot_id
    if ts is not None and ts not in shots:
        problems.append(f"true_scale_shot_id {ts} — нет такого кадра")

    model = None
    lim, disp = cfg["limits"], cfg["display"]
    if None not in vals.values() and len(vals) == sum(1 for d in cfg["params"].values() if d.get("required")):
        kappa, scale = vals["kappa_m2_s"], vals["pressure_scale_mpa"]
        r_w, r_max, t_end, thr = vals["r_well_m"], vals["r_max_m"], vals["t_end_s"], vals["threshold_mpa"]
        model = PressureModel(kappa, scale)
        r_min = r_max * disp["graph_r_min_fraction"]
        if r_w >= r_min:
            problems.append(f"r_well_m {r_w} должен быть меньше {fmt_num(r_min)} м "
                            f"({disp['graph_r_min_fraction']} от r_max_m) — иначе скважина закрывает график")
        x_w = r_w ** 2 / (4 * kappa * t_end)
        if x_w > lim["max_well_argument"]:
            problems.append(f"к концу анимации r_w²/(4κt) = {x_w:.3g} > {lim['max_well_argument']}: "
                            f"приближение линейного источника неприменимо, увеличьте t_end_s или κ")
        try:
            r_end = model.influence_radius(t_end, thr)
        except ValueError as e:
            problems.append(str(e))
            r_end = float("nan")
        if r_end > r_max:
            problems.append(f"условная граница к концу ({fmt_num(r_end)} м) выходит за окно r_max_m {r_max} м")
        elif r_end < lim["min_radius_fraction_at_end"] * r_max:
            problems.append(f"условная граница к концу ({fmt_num(r_end)} м) меньше "
                            f"{lim['min_radius_fraction_at_end']} окна — её не будет видно; уменьшите r_max_m")
        if k is not None and r_w * k > lim["max_marker_fraction"] * r_max:
            problems.append(f"значок скважины при увеличении {k} больше {lim['max_marker_fraction']} окна")

    # плашки ↔ увеличение значка скважины: число на плашке = well_exaggeration
    if k is not None:
        k_txt = str(int(k)) if float(k).is_integer() else fmt_num(k)
        plaqued = [s.id for s in spec.shots if s.plaque]
        if k == 1 and plaqued:
            problems.append(f"well_exaggeration = 1 (всё в истинном масштабе), а у кадров {plaqued} плашка")
        if k > 1:
            for s in spec.shots:
                if s.plaque and not re.search(rf"(?<![\d,.]){re.escape(k_txt)}(?![\d,.])", s.plaque):
                    problems.append(f"кадр {s.id}: на плашке нет числа увеличения {k_txt}")
            if not any(re.search(rf"(?<![\d,.]){re.escape(k_txt)}(?![\d,.])", e) for e in spec.exaggerations):
                problems.append(f"в exaggerations нет преувеличения значка скважины с числом {k_txt}")
            if ts is None:
                problems.append("значок скважины увеличен — нужен кадр в истинном масштабе (true_scale_shot_id)")
            elif ts in shots and shots[ts].plaque:
                problems.append(f"кадр истинного масштаба {ts} не может иметь плашку")
            if not plaqued:
                problems.append(f"значок скважины увеличен в {k_txt} раз, но ни у одного кадра нет плашки")

    if problems:
        err = VideoInputError("параметры T1 некорректны:\n- " + "\n- ".join(problems))
        err.problems = problems
        raise err

    phrase_shot = {pid: s.id for s in spec.shots for pid in s.phrase_ids}
    graph_max = nice_ceil(float(model.delta_p([r_min], t_end)[0]))          # ось графика без обрезки
    color_max = nice_ceil(float(model.delta_p([r_max * disp["color_r_fraction"]], t_end)[0]))  # ближе — насыщение
    return {
        "model": model, "r_well": r_w, "r_max": r_max, "r_min": r_min, "t_end": t_end, "threshold": thr,
        "exaggeration": float(k), "exaggerated_shots": {s.id for s in spec.shots if s.plaque},
        "true_scale_shot_id": ts, "evolve_phrase_ids": {pid for pid, sid in phrase_shot.items() if sid in evolve},
        "color_max": color_max, "graph_max": graph_max, "grid": int(disp["field_grid"]), "field_color_key": disp["field_color"],
        "time_unit": time_unit(t_end), "r_influence_end": r_end, "well_argument_end": x_w,
    }


def check(spec: SceneSpec, script: Script, cfg: dict) -> list[str]:
    """Те же проверки, что перед рендером, — списком (для повторной попытки в video.spec)."""
    try:
        prepare(spec, script, cfg)
    except VideoInputError as e:
        return [f"T1: {p}" for p in getattr(e, "problems", [str(e)])]
    return []
