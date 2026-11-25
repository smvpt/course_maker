"""T3 «Рост тела»: проверка параметров SceneSpec до озвучки и функции сцены из одного состояния.

Описание, параметры, цвета и ограничения — domain/<домен>/templates/T3.json.
Состояние — радиус береговой линии R(t) модели LobeModel; план (plan_field) и разрез (section_profile)
считаются одной функцией LobeModel.surface, поэтому граница тела в обоих видах совпадает.
"""
from __future__ import annotations

import math

import numpy as np

from contracts.models import SceneSpec, Script
from pipeline.video.inputs import VideoInputError
from pipeline.video.t2_template import _exag_txt, _has_number
from pipeline.video.t3_model import LobeModel

ALLOWED_CLASSES = {"B"}
FROZEN_BEATS = {"prediction", "final"}   # на этих фразах время модели стоит


def _num(v) -> bool:
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v)


def prepare(spec: SceneSpec, script: Script, cfg: dict) -> dict:
    problems: list[str] = []
    p = dict(spec.params)
    unknown = sorted(set(p) - set(cfg["params"]))
    if unknown:
        problems.append(f"неизвестные параметры T3: {unknown}; допустимы {sorted(cfg['params'])}")
    for key, d in cfg["params"].items():
        if key not in p:
            if d.get("required"):
                problems.append(f"нет обязательного параметра params.{key} ({d['meaning']})")
            else:
                p[key] = d.get("default")
    positive = ("depth_m", "foreset_angle_deg", "supply_m3_per_yr", "initial_radius_m", "t_end_yr", "r_max_m",
                "lobe_angle_deg")
    for key in positive:
        if key in p and (not _num(p[key]) or p[key] <= 0):
            problems.append(f"params.{key} должно быть числом > 0, получено {p[key]!r}")
    lim, disp = cfg["limits"], cfg["display"]
    if _num(p.get("foreset_angle_deg")) and p["foreset_angle_deg"] > lim["max_foreset_angle_deg"]:
        problems.append(f"params.foreset_angle_deg {p['foreset_angle_deg']} больше {lim['max_foreset_angle_deg']}°")
    if _num(p.get("lobe_angle_deg")) and p["lobe_angle_deg"] > 180:
        problems.append(f"params.lobe_angle_deg {p['lobe_angle_deg']} больше 180°")
    n = p.get("n_layers")
    if isinstance(n, bool) or not isinstance(n, int) or not lim["min_layers"] <= n <= lim["max_layers"]:
        problems.append(f"params.n_layers — целое от {lim['min_layers']} до {lim['max_layers']}, получено {n!r}")
    k = p.get("vertical_exaggeration")
    if not _num(k) or k < 1:
        problems.append(f"params.vertical_exaggeration — число ≥ 1, получено {k!r}")
        k = None

    model = r_end = None
    if not problems:
        try:
            model = LobeModel(p["depth_m"], p["foreset_angle_deg"], p["supply_m3_per_yr"], p["initial_radius_m"],
                              p["lobe_angle_deg"])
        except ValueError as e:
            problems.append(f"модель: {e}")
    if model is not None:
        r_max, t_end = float(p["r_max_m"]), float(p["t_end_yr"])
        r_end = model.radius(t_end)
        toe = r_end + model.foreset_length
        if toe > r_max:
            problems.append(f"подножие склона к концу ({toe:.0f} м) выходит за окно r_max_m {r_max:g} м")
        if r_end - model.r0_m < disp["min_growth_fraction"] * r_max:
            problems.append(f"береговая линия за t_end продвигается лишь на {r_end - model.r0_m:.0f} м — меньше "
                            f"{disp['min_growth_fraction']} окна; увеличьте t_end_yr или уменьшите r_max_m")
        if k is not None:
            h_px = model.depth_m * k * disp["nominal_section_width_px"] / r_max
            if h_px > disp["max_section_height_px"]:
                problems.append(f"высота разреза при увеличении {k:g} — {h_px:.0f} px, больше "
                                f"{disp['max_section_height_px']} px; уменьшите vertical_exaggeration")

    shots = {s.id: s for s in spec.shots}
    evolve = p.get("evolve_shot_ids")
    if evolve is None:
        evolve = list(shots)
    elif not isinstance(evolve, list) or not evolve or any(e not in shots for e in evolve):
        problems.append(f"params.evolve_shot_ids — непустой список id кадров из {sorted(shots)}, получено {evolve!r}")
        evolve = []
    for s in spec.shots:
        if s.frame_class not in ALLOWED_CLASSES or s.label != "симуляция":
            problems.append(f"кадр {s.id}: T3 рисует расчёт — нужен класс B с меткой «симуляция», "
                            f"а не {s.frame_class}/«{s.label}»")
    ts = spec.true_scale_shot_id
    if ts is not None and ts not in shots:
        problems.append(f"true_scale_shot_id {ts} — нет такого кадра")
    if k is not None:
        kt = _exag_txt(k)
        plaqued = [s.id for s in spec.shots if s.plaque]
        if k == 1 and plaqued:
            problems.append(f"vertical_exaggeration = 1 (всё в истинном масштабе), а у кадров {plaqued} плашка")
        if k > 1:
            for s in spec.shots:
                if s.plaque and not _has_number(s.plaque, kt):
                    problems.append(f"кадр {s.id}: на плашке нет числа увеличения {kt}")
            if not any(_has_number(e, kt) for e in spec.exaggerations):
                problems.append(f"в exaggerations нет вертикального увеличения с числом {kt}")
            if ts is None:
                problems.append("вертикаль увеличена — нужен кадр в истинном масштабе (true_scale_shot_id)")
            elif ts in shots and shots[ts].plaque:
                problems.append(f"кадр истинного масштаба {ts} не может иметь плашку")
            if not plaqued:
                problems.append(f"вертикаль увеличена в {kt} раз, но ни у одного кадра нет плашки")

    if problems:
        err = VideoInputError("параметры T3 некорректны:\n- " + "\n- ".join(problems))
        err.problems = problems
        raise err

    phrase_shot = {pid: s.id for s in spec.shots for pid in s.phrase_ids}
    beat = {ph.id: ph.beat for ph in script.phrases}
    return {"model": model, "r_max": float(p["r_max_m"]), "t_end": float(p["t_end_yr"]), "n_layers": n,
            "layer_times": model.layer_times(n, float(p["t_end_yr"])), "r_end": r_end, "exaggeration": float(k),
            "exaggerated_shots": {s.id for s in spec.shots if s.plaque}, "true_scale_shot_id": ts,
            # вопрос-предсказание (и пауза после него) и финал не двигают модель, даже если их кадр в evolve
            "evolve_phrase_ids": {pid for pid, sid in phrase_shot.items()
                                  if sid in evolve and beat.get(pid) not in FROZEN_BEATS},
            "grid": int(disp["plan_grid"]), "display": disp}


def check(spec: SceneSpec, script: Script, cfg: dict) -> list[str]:
    try:
        prepare(spec, script, cfg)
    except VideoInputError as e:
        return [f"T3: {x}" for x in getattr(e, "problems", [str(e)])]
    return []


# ---------------------------------------------------------------- одно состояние → два вида

def plan_field(prep: dict, t: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """План: отметка z на сетке x ∈ [−r_max, r_max], y ∈ [−r_max, 0] (точка питания — (0, 0), лопасть вниз).
    Возвращает (z, xs, ys, inside) — inside: точка в секторе лопасти."""
    m, n = prep["model"], prep["grid"]
    xs = np.linspace(-prep["r_max"], prep["r_max"], n)
    ys = np.linspace(0.0, -prep["r_max"], (n + 1) // 2)
    X, Y = np.meshgrid(xs, ys)
    r = np.hypot(X, Y)
    inside = np.abs(np.degrees(np.arctan2(X, -Y))) <= m.lobe_deg / 2 + 1e-9
    return m.surface(r, t), xs, ys, inside


def section_profile(prep: dict, t: float, n: int = 801) -> tuple[np.ndarray, np.ndarray]:
    """Разрез по оси лопасти (линия А–Б): r ∈ [0, r_max] — та же функция surface, то же время."""
    r = np.linspace(0.0, prep["r_max"], n)
    return r, prep["model"].surface(r, t)


def layer_bands(prep: dict, t: float, n: int = 801) -> list[dict]:
    """Слои разреза к моменту t: слой k — осадок интервала [t_k, t_{k+1}], низ — поверхность в t_k,
    верх — в min(t, t_{k+1}); текущий слой — частичный."""
    r = np.linspace(0.0, prep["r_max"], n)
    tb, m = prep["layer_times"], prep["model"]
    out = []
    for k in range(prep["n_layers"]):
        if t <= tb[k]:
            break
        top_t = min(t, tb[k + 1])
        out.append({"k": k, "r": r, "z_bottom": m.surface(r, tb[k]), "z_top": m.surface(r, top_t),
                    "partial": top_t < tb[k + 1]})
    return out


def shoreline_radii(prep: dict, t: float) -> list[float]:
    """Прошлые береговые линии (границы слоёв, t_k ≤ t) и текущая — для плана; те же радиусы, что в разрезе."""
    m = prep["model"]
    past = [m.radius(float(tk)) for tk in prep["layer_times"] if tk < t]
    return past + [m.radius(t)]


def auto_checks(prep: dict) -> dict[str, tuple[bool, str]]:
    """Проверки по модели для паспорта: порядок слоёв и баланс объёма (численно)."""
    m, r = prep["model"], np.linspace(0.0, prep["r_max"], 4001)
    ts = np.linspace(0.0, prep["t_end"], 61)
    surf = np.array([m.surface(r, t) for t in ts])
    ok_order = bool(np.all(np.diff(surf, axis=0) >= -1e-9))
    phi = math.radians(m.lobe_deg)
    v_num = phi * np.trapezoid((surf[-1] - surf[0]) * r, r)
    v_exp = m.supply_m3_per_yr * prep["t_end"]
    rel = abs(v_num - v_exp) / v_exp
    return {"layers_order": (ok_order, "по модели: поверхность только наращивается во времени (61 момент, 4001 точка) — "
                                       "слои не пересекаются, молодые лежат на старых"),
            "mass_balance": (bool(rel <= 1e-3), f"по модели: объём отложенного за t_end численно {v_num:.4g} м³ против "
                                          f"Q·t = {v_exp:.4g} м³, отн. ошибка {rel:.1e}")}
