"""T4 «Ствол скважины»: проверка параметров SceneSpec до озвучки и функции сцены из одного состояния.

Описание, допущения, параметры, цвета и ограничения — domain/<домен>/templates/T4.json.
Состояние — глубина кровли газовой пачки; обе скважины, объём газа и график давления считаются
одной моделью WellModel (state, profile).
"""
from __future__ import annotations

import math

import numpy as np

from contracts.models import SceneSpec, Script
from pipeline.video.inputs import VideoInputError
from pipeline.video.t2_template import _exag_txt, _has_number
from pipeline.video.t4_model import G, P_ATM, WellModel

ALLOWED_CLASSES = {"B"}
FROZEN_BEATS = {"prediction", "final"}   # на этих фразах газ не поднимается
PHYSICAL = ("depth_m", "mud_density_kg_m3", "gas_volume_m3", "hole_diameter_m")


def _num(v) -> bool:
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v)


def prepare(spec: SceneSpec, script: Script, cfg: dict) -> dict:
    problems: list[str] = []
    p = dict(spec.params)
    unknown = sorted(set(p) - set(cfg["params"]))
    if unknown:
        problems.append(f"неизвестные параметры T4: {unknown}; допустимы {sorted(cfg['params'])}")
    for key, d in cfg["params"].items():
        if key not in p:
            if d.get("required"):
                problems.append(f"нет обязательного параметра params.{key} ({d['meaning']})")
            else:
                p[key] = d.get("default")
    for key in (*PHYSICAL, "top_stop_m"):
        if key in p and (not _num(p[key]) or p[key] <= 0):
            problems.append(f"params.{key} должно быть числом > 0, получено {p[key]!r}")
    lim, disp = cfg["limits"], cfg["display"]
    for key in ("mud_density_kg_m3", "hole_diameter_m"):
        lo, hi = lim[key]
        if _num(p.get(key)) and not lo <= p[key] <= hi:
            problems.append(f"params.{key} = {p[key]} вне {lo}–{hi} ({cfg['params'][key]['unit']}) — проверьте единицы")
    shoe = p.get("casing_shoe_m")
    if shoe is not None and (not _num(shoe) or shoe <= 0):
        problems.append(f"params.casing_shoe_m — число > 0 или null, получено {shoe!r}")
    k = p.get("horizontal_exaggeration")
    if not _num(k) or k < 1:
        problems.append(f"params.horizontal_exaggeration — число ≥ 1, получено {k!r}")
        k = None

    model = None
    if not problems:
        try:
            model = WellModel(p["depth_m"], p["mud_density_kg_m3"], p["gas_volume_m3"], p["hole_diameter_m"])
        except ValueError as e:
            problems.append(f"модель: {e}")
    if model is not None:
        D, stop = model.depth_m, float(p["top_stop_m"])
        if model.start_length > lim["max_gas_fraction_of_depth"] * D:
            problems.append(f"газовая пачка у забоя {model.start_length:.0f} м — больше {lim['max_gas_fraction_of_depth']} "
                            f"глубины ствола")
        if shoe is not None and shoe > D:
            problems.append(f"башмак колонны {shoe:g} м глубже ствола {D:g} м")
        if stop >= model.start_top:
            problems.append(f"top_stop_m {stop:g} м не выше начального положения кровли пачки ({model.start_top:.0f} м)")
        elif model.start_top - stop < lim["min_rise_fraction"] * D:
            problems.append(f"газ поднимается лишь на {model.start_top - stop:.0f} м — меньше {lim['min_rise_fraction']} "
                            f"глубины; уменьшите top_stop_m")
        else:
            end_open = model.state(stop, closed=False)
            if end_open["bottom"] > D:
                problems.append(f"в открытой скважине пачка к концу ({end_open['length']:.0f} м) не помещается в ствол — "
                                f"выброс раствора не моделируется; увеличьте top_stop_m")
        if k is not None:
            w_px = model.hole_diameter_m * k * disp["nominal_column_height_px"] / D
            if w_px > disp["max_well_fraction_of_column"] * disp["column_width_px"]:
                problems.append(f"ствол при увеличении {k:g} шире {disp['max_well_fraction_of_column']} колонки кадра")

    shots = {s.id: s for s in spec.shots}
    evolve = p.get("evolve_shot_ids")
    if evolve is None:
        evolve = list(shots)
    elif not isinstance(evolve, list) or not evolve or any(e not in shots for e in evolve):
        problems.append(f"params.evolve_shot_ids — непустой список id кадров из {sorted(shots)}, получено {evolve!r}")
        evolve = []
    for s in spec.shots:
        if s.frame_class not in ALLOWED_CLASSES or s.label != "симуляция":
            problems.append(f"кадр {s.id}: T4 рисует расчёт — нужен класс B с меткой «симуляция», "
                            f"а не {s.frame_class}/«{s.label}»")
    ts = spec.true_scale_shot_id
    if ts is not None and ts not in shots:
        problems.append(f"true_scale_shot_id {ts} — нет такого кадра")
    if k is not None:
        kt = _exag_txt(k)
        plaqued = [s.id for s in spec.shots if s.plaque]
        if k == 1 and plaqued:
            problems.append(f"horizontal_exaggeration = 1 (всё в истинном масштабе), а у кадров {plaqued} плашка")
        if k > 1:
            for s in spec.shots:
                if s.plaque and not _has_number(s.plaque, kt):
                    problems.append(f"кадр {s.id}: на плашке нет числа увеличения {kt}")
            if not any(_has_number(e, kt) for e in spec.exaggerations):
                problems.append(f"в exaggerations нет увеличения ширины ствола с числом {kt}")
            if ts is None:
                problems.append("ствол расширен — нужен кадр в истинном масштабе (true_scale_shot_id)")
            elif ts in shots and shots[ts].plaque:
                problems.append(f"кадр истинного масштаба {ts} не может иметь плашку")
            if not plaqued:
                problems.append(f"ствол расширен в {kt} раз, но ни у одного кадра нет плашки")

    if problems:
        err = VideoInputError("параметры T4 некорректны:\n- " + "\n- ".join(problems))
        err.problems = problems
        raise err

    beat = {ph.id: ph.beat for ph in script.phrases}
    phrase_shot = {pid: s.id for s in spec.shots for pid in s.phrase_ids}
    return {"model": model, "top_start": model.start_top, "top_stop": float(p["top_stop_m"]),
            "casing_shoe": float(shoe) if shoe is not None else None, "exaggeration": float(k),
            "exaggerated_shots": {s.id for s in spec.shots if s.plaque}, "true_scale_shot_id": ts,
            "evolve_phrase_ids": {pid for pid, sid in phrase_shot.items()
                                  if sid in evolve and beat.get(pid) not in FROZEN_BEATS},
            "display": disp}


def check(spec: SceneSpec, script: Script, cfg: dict) -> list[str]:
    try:
        prepare(spec, script, cfg)
    except VideoInputError as e:
        return [f"T4: {x}" for x in getattr(e, "problems", [str(e)])]
    return []


# ---------------------------------------------------------------- одно состояние → скважины и график

def top_at(prep: dict, progress: float) -> float:
    """Глубина кровли пачки по прогрессу подъёма 0…1."""
    return prep["top_start"] + (prep["top_stop"] - prep["top_start"]) * min(max(progress, 0.0), 1.0)


def states(prep: dict, top: float) -> tuple[dict, dict]:
    m = prep["model"]
    return m.state(top, closed=False), m.state(top, closed=True)


def pressure_curves(prep: dict, top: float, n: int = 400) -> dict:
    """Избыточное давление по глубине (МПа) для открытой, закрытой скважины и до подъёма газа — одна модель."""
    m = prep["model"]
    x = np.linspace(0.0, m.depth_m, n)
    o, c = states(prep, top)
    s0 = m.state(prep["top_start"], closed=True)
    to_mpa = lambda p: (p - P_ATM) / 1e6
    return {"x": x, "open": to_mpa(m.profile(o, x)), "closed": to_mpa(m.profile(c, x)),
            "initial": to_mpa(m.profile(s0, x)), "open_state": o, "closed_state": c}


def auto_checks(prep: dict) -> dict[str, tuple[bool | None, str]]:
    """Проверки по модели для паспорта. Частично проверенный пункт — None (в паспорте «не проверено»)."""
    m = prep["model"]
    x = np.linspace(0.0, m.depth_m, 301)
    heavy = WellModel(m.depth_m, m.mud_density * 1.25, m.gas_volume_m3, m.hole_diameter_m)
    hydro_ok = bool(np.allclose(m.hydrostatic(x) - P_ATM, m.mud_density * G * x)
                    and np.all(np.diff(m.hydrostatic(x)) > 0) and np.all(heavy.hydrostatic(x[1:]) > m.hydrostatic(x[1:])))
    hydro = (None if hydro_ok else False,
             "по модели: избыточное давление столба = ρ·g·x, растёт с глубиной и плотностью (проверено расчётом); "
             "циркуляция в шаблоне не показана — пункт целиком не подтверждён" if hydro_ok
             else "гидростатика модели не прошла расчётную проверку")
    tops = np.linspace(prep["top_start"], prep["top_stop"], 80)
    o = [m.state(t, False) for t in tops]
    c = [m.state(t, True) for t in tops]
    vo = np.array([s["volume"] for s in o])
    dv = np.diff(vo) / -np.diff(tops)
    open_ok = bool(np.all(np.diff(vo) > 0) and np.all(np.diff(dv) > 0))
    closed_ok = bool(all(math.isclose(s["volume"], m.gas_volume_m3) for s in c)
                     and np.all(np.diff([s["p_surface"] for s in c]) > 0) and np.all(np.diff([s["p_bottom"] for s in c]) > 0)
                     and np.all(m.profile(c[-1], x) >= m.profile(c[0], x) - 1e-6))
    gas = (open_ok and closed_ok,
           f"по модели: в открытой газ расширяется {m.gas_volume_m3:g} → {vo[-1]:.3g} м³, прирост на метр подъёма растёт "
           f"к устью; в закрытой объём постоянен, давление на устье {(c[0]['p_surface'] - P_ATM) / 1e6:.3g} → "
           f"{(c[-1]['p_surface'] - P_ATM) / 1e6:.3g} МПа, на забое растёт, по всему стволу не ниже начального")
    pv = np.array([s["p_gas"] * s["volume"] for s in o])
    pit = np.array([s["pit_gain"] for s in o])
    bal_ok = bool(np.allclose(pv, pv[0], rtol=1e-12) and np.allclose(pit, vo - m.gas_volume_m3))
    bal = (bal_ok, "по модели: масса газа постоянна (p·V неизменно по закону Бойля), вытесненный в ёмкость раствор "
                   "равен приросту объёма газа; в закрытой скважине объём не меняется")
    return {"hydrostatic": hydro, "gas_open_closed": gas, "mass_balance": bal}
