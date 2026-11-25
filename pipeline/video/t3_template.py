"""T3 «Рост тела»: проверка параметров SceneSpec до озвучки и функции сцены из одного состояния.

Два режима (params.mode):
- quantitative (по умолчанию) — расчётная проградация лопасти LobeModel; физические параметры — из узла;
- qualitative — схема с относительной геометрией без чисел для узлов, где чисел для расчёта нет: элементы
  схемы (конус, зоны, депоцентр, стадии лопастей) — только из утверждений узла, с claim_id; допущения
  расчётной проградации не используются.

Описание, параметры, цвета и ограничения — domain/<домен>/templates/T3.json.
Состояние — радиус береговой линии R(t) модели LobeModel; план (plan_field) и разрез (section_profile)
считаются одной функцией LobeModel.surface, поэтому граница тела в обоих видах совпадает.
"""
from __future__ import annotations

import math
import re

import numpy as np

from contracts.models import SceneSpec, Script
from pipeline.video.inputs import VideoInputError
from pipeline.video.t2_template import _exag_txt, _has_number
from pipeline.video.t3_model import LobeModel

ALLOWED_CLASSES = {"B"}
MODES = ("quantitative", "qualitative")
# единицы и величины, которые качественная схема не вводит сама (допустимы, только если есть в утверждениях узла)
UNIT_RE = re.compile(r"\b(метр|километр|сантиметр|миллиметр|кубометр|тонн|лет|год|столети|тысячелети|"
                     r"миллион|градус|процент|м³|км)\w*", re.IGNORECASE)
FROZEN_BEATS = {"prediction", "final"}   # на этих фразах время модели стоит


def _num(v) -> bool:
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v)


def mode_of(spec: SceneSpec) -> str:
    return spec.params.get("mode", "quantitative")


def mode_params(cfg: dict, mode: str) -> dict:
    """Параметры шаблона, допустимые в режиме (у параметра без modes — во всех режимах)."""
    return {k: d for k, d in cfg["params"].items() if mode in d.get("modes", MODES)}


def prepare(spec: SceneSpec, script: Script, cfg: dict) -> dict:
    mode = mode_of(spec)
    if mode == "qualitative":
        return prepare_qualitative(spec, script, cfg)
    if mode != "quantitative":
        raise _error([f"params.mode — одно из {list(MODES)}, получено {mode!r}"])
    problems: list[str] = []
    p = dict(spec.params)
    allowed = mode_params(cfg, "quantitative")
    unknown = sorted(set(p) - set(allowed))
    if unknown:
        problems.append(f"параметры {unknown} не относятся к режиму quantitative; допустимы {sorted(allowed)}")
    for key, d in allowed.items():
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
        raise _error(problems)

    phrase_shot = {pid: s.id for s in spec.shots for pid in s.phrase_ids}
    beat = {ph.id: ph.beat for ph in script.phrases}
    return {"mode": "quantitative", "model": model, "r_max": float(p["r_max_m"]), "t_end": float(p["t_end_yr"]), "n_layers": n,
            "layer_times": model.layer_times(n, float(p["t_end_yr"])), "r_end": r_end, "exaggeration": float(k),
            "exaggerated_shots": {s.id for s in spec.shots if s.plaque}, "true_scale_shot_id": ts,
            # вопрос-предсказание (и пауза после него) и финал не двигают модель, даже если их кадр в evolve
            "evolve_phrase_ids": {pid for pid, sid in phrase_shot.items()
                                  if sid in evolve and beat.get(pid) not in FROZEN_BEATS},
            "grid": int(disp["plan_grid"]), "display": disp}


def _error(problems: list[str]) -> VideoInputError:
    err = VideoInputError("параметры T3 некорректны:\n- " + "\n- ".join(problems))
    err.problems = problems
    return err


def _evolve_phrases(spec: SceneSpec, script: Script, evolve, problems: list[str]) -> set[str]:
    shots = {s.id: s for s in spec.shots}
    if evolve is None:
        evolve = list(shots)
    elif not isinstance(evolve, list) or not evolve or any(e not in shots for e in evolve):
        problems.append(f"params.evolve_shot_ids — непустой список id кадров из {sorted(shots)}, получено {evolve!r}")
        evolve = []
    beat = {ph.id: ph.beat for ph in script.phrases}
    return {pid for s in spec.shots if s.id in evolve for pid in s.phrase_ids if beat.get(pid) not in FROZEN_BEATS}


def prepare_qualitative(spec: SceneSpec, script: Script, cfg: dict) -> dict:
    """Качественная схема: без чисел, плашек и масштаба; каждый элемент — с утверждением узла, которое звучит."""
    problems: list[str] = []
    q = cfg["qualitative"]
    p = dict(spec.params)
    allowed = mode_params(cfg, "qualitative")
    foreign = sorted(set(p) - set(allowed))
    if foreign:
        problems.append(f"параметры {foreign} не задаются в режиме qualitative (расчёта нет — числа не выдумываются); "
                        f"допустимы {sorted(allowed)}")
    for key, d in allowed.items():
        if key not in p:
            if d.get("required"):
                problems.append(f"нет обязательного параметра params.{key} ({d['meaning']})")
            else:
                p[key] = d.get("default")
    elements: dict[str, str] = {}
    raw = p.get("elements")
    if raw is not None and (not isinstance(raw, list) or not raw):
        problems.append(f"params.elements — непустой список {{element, claim_id}}, получено {raw!r}")
        raw = []
    for i, e in enumerate(raw or []):
        if not isinstance(e, dict) or not isinstance(e.get("element"), str) or not isinstance(e.get("claim_id"), str):
            problems.append(f"params.elements[{i}] — объект {{element, claim_id}} со строками, получено {e!r}")
            continue
        name, cid = e["element"], e["claim_id"]
        if name not in q["elements"]:
            problems.append(f"params.elements[{i}]: элемент «{name}» неизвестен; допустимы {sorted(q['elements'])}")
        elif name in elements:
            problems.append(f"params.elements: элемент «{name}» указан дважды")
        elif not cid.startswith(f"{spec.node_id}#"):
            problems.append(f"params.elements[{i}]: claim_id {cid} не из узла {spec.node_id}")
        else:
            elements[name] = cid
    if raw:
        for name, d in q["elements"].items():
            if d.get("required") and name not in elements:
                problems.append(f"params.elements: нет обязательного элемента «{name}»")
    first_phrase: dict[str, str] = {}
    for ph in script.phrases:
        first_phrase.setdefault(ph.claim_id, ph.id)
    for name, cid in elements.items():
        if cid not in first_phrase:
            problems.append(f"элемент «{name}»: его утверждение {cid} не звучит ни в одной фразе сценария")
    n = p.get("n_lobes")
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= q["max_lobes"]:
        problems.append(f"params.n_lobes — целое от 1 до {q['max_lobes']}, получено {n!r}")
    elif n > 1 and "lobe_cycles" not in elements:
        problems.append(f"params.n_lobes = {n}: несколько стадий — только с элементом lobe_cycles из узла")
    elif n == 1 and "lobe_cycles" in elements:
        problems.append("элемент lobe_cycles показывает повторение стадий — нужно n_lobes ≥ 2")
    for s in spec.shots:
        if s.frame_class not in ALLOWED_CLASSES or s.label != "схема":
            problems.append(f"кадр {s.id}: качественная схема T3 — нужен класс B с меткой «схема» (расчёта нет), "
                            f"а не {s.frame_class}/«{s.label}»")
        if s.plaque:
            problems.append(f"кадр {s.id}: у схемы без масштаба нет плашки с числом преувеличения — уберите plaque")
    if spec.exaggerations:
        problems.append("exaggerations должен быть пустым: у схемы без масштаба нет чисел преувеличения")
    if spec.true_scale_shot_id is not None:
        problems.append("true_scale_shot_id — null: у схемы без масштаба нет кадра истинного масштаба")
    evolve_ids = _evolve_phrases(spec, script, p.get("evolve_shot_ids"), problems)
    # фазы показа: первая стадия растёт на фразах до первой фразы о стадиях, остальные стадии — после неё
    phases = [(evolve_ids, 1.0)]
    if "lobe_cycles" in elements and "lobe_cycles" in {k for k in elements if elements[k] in first_phrase} \
            and isinstance(n, int) and n > 1:
        order = [ph.id for ph in script.phrases]
        split = order.index(first_phrase[elements["lobe_cycles"]])
        before = {pid for pid in evolve_ids if order.index(pid) < split}
        after = evolve_ids - before
        if not before or not after:
            problems.append("evolve_shot_ids: нужны кадры с ростом и до первой фразы о стадиях лопастей (рост первой "
                            "стадии), и начиная с неё (следующие стадии)")
        phases = [(before, 1.0 / n), (after, 1.0)]
    if problems:
        raise _error(problems)
    return {"mode": "qualitative", "phases": phases, "elements": elements, "appear_at": {k: first_phrase[c] for k, c in elements.items()},
            "n_lobes": n, "t_end": 1.0, "evolve_phrase_ids": evolve_ids, "display": q,
            "true_scale_shot_id": None, "exaggerated_shots": set()}


def node_problems(spec: SceneSpec, script: Script, node, cfg: dict) -> list[str]:
    """Проверки качественного режима против узла: элемент называется своим утверждением; в тексте нет единиц
    и величин, которых нет в утверждениях узла."""
    if mode_of(spec) != "qualitative" or "qualitative" not in cfg:
        return []
    q, problems = cfg["qualitative"], []
    claims = {c.id: c for c in node.claims}
    raw = spec.params.get("elements")
    for e in raw if isinstance(raw, list) else []:
        if not isinstance(e, dict) or e.get("element") not in q["elements"] or not isinstance(e.get("claim_id"), str):
            continue                                   # структуру проверяет prepare_qualitative
        c = claims.get(e["claim_id"])
        if c is None:
            problems.append(f"T3: элемент «{e['element']}»: claim_id {e['claim_id']} не из узла {node.id}")
            continue
        text = f"{c.text}\n{c.quote}".casefold()
        for group in q["elements"][e["element"]]["evidence"]:
            if not any(w.casefold() in text for w in group):
                problems.append(f"T3: элемент «{e['element']}»: утверждение {c.id} его не называет "
                                f"(нет ни одного из {group}) — элемента нет в источнике")
    source = "\n".join(f"{c.text}\n{c.quote}" for c in node.claims).casefold()
    for ph in script.phrases:
        for field in ("text", "on_screen"):
            for m in UNIT_RE.finditer(getattr(ph, field) or ""):
                if not re.search(r"(?<!\w)" + re.escape(m.group(1).casefold()), source):  # не «гео-метр-ия»
                    problems.append(f"T3: фраза {ph.id}.{field}: «{m.group(0)}» — такой величины в узле нет, "
                                    f"а качественная схема чисел и единиц не вводит")
    return problems


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


# ---------------------------------------------------------------- качественная схема: одно состояние → два вида

def stages(prep: dict, s: float) -> list[dict]:
    """Стадии к доле показа s ∈ [0, 1]: стадия k растёт на [k/n, (k+1)/n]; growth — доля полной длины конуса
    (первая стадия — от start_growth), active — текущая стадия, остальные отмершие и перекрытые."""
    n, g0 = prep["n_lobes"], prep["display"]["start_growth"]
    s = min(max(float(s), 0.0), 1.0)
    out = []
    for k in range(n):
        a, b = k / n, (k + 1) / n
        if k > 0 and s <= a:
            break
        g = min(max((s - a) / (b - a), 0.0), 1.0)
        out.append({"k": k, "growth": g0 + (1 - g0) * g if k == 0 else g, "active": False, "base": float(k)})
    out[-1]["active"] = True
    return out


def zone_bounds(prep: dict, growth: float) -> list[dict]:
    """Границы зон одной стадии вдоль оси конуса (доли полной длины) — общий источник для плана и разреза."""
    out, x0 = [], 0.0
    for z in prep["display"]["zones"]:
        out.append({"key": z["key"], "from": x0 * growth, "to": z["to"] * growth})
        x0 = z["to"]
    return out


def stage_profile(prep: dict, growth: float, x: np.ndarray) -> np.ndarray:
    """Кровля стадии над её подошвой в долях толщины стадии; top зоны — кровля на её внешнем краю: равнина
    плоская, авандельта — крутой спуск, продельта — пологий клин до 0. Вне конуса — 0."""
    zones = prep["display"]["zones"]
    kx = [0.0] + [z["to"] * growth for z in zones]
    ky = [zones[0]["top"]] + [z["top"] for z in zones]
    x = np.asarray(x, dtype=float)
    if growth <= 0:
        return np.zeros_like(x)
    return np.where(x <= kx[-1], np.interp(x, kx, ky), 0.0)


def qualitative_checks(prep: dict) -> dict[str, tuple[bool, str]]:
    """Проверка схемы для паспорта (по построению, 101 момент × 241 точка): каждая стадия лежит на кровле
    предыдущей (моложе — выше), кровля не ниже подошвы; стадия не уменьшается и не исчезает."""
    ss, x = np.linspace(0.0, 1.0, 101), np.linspace(0.0, 1.0, 241)
    order = True
    for s in ss:
        st = stack_profiles(prep, s, x)
        order &= all(np.all(b["top"] >= b["bottom"] - 1e-12) for b in st)
        order &= all(np.allclose(st[k]["bottom"], st[k - 1]["top"]) for k in range(1, len(st)))
    grow = all(len(stages(prep, s1)) >= len(stages(prep, s0)) and
               all(a["growth"] <= b["growth"] + 1e-12 for a, b in zip(stages(prep, s0), stages(prep, s1)))
               for s0, s1 in zip(ss, ss[1:]))
    return {"stages_order": (bool(order and grow), "по построению схемы (101 момент): каждая стадия лежит на кровле "
                                                   "предыдущей — моложе выше; стадия не уменьшается и не исчезает")}


def depocenter_extent(prep: dict, s: float) -> float:
    """Депоцентр — место, где накопленное тело толще всего: у устья, где перекрываются все стадии; его край —
    конец авандельты самой короткой из показанных стадий (доля полной длины). Одно значение для плана и разреза."""
    zones = prep["display"]["zones"]
    return min(st["growth"] for st in stages(prep, s)) * zones[1]["to"]


def stack_profiles(prep: dict, s: float, x: np.ndarray) -> list[dict]:
    """Разрез: стадия k облекает кровлю стадий ниже — подошва = сумма кровель стадий 0…k−1 (в толщинах стадии),
    кровля = подошва + stage_profile. Возвращает для каждой показанной стадии x, низ, верх и границы зон."""
    out, base = [], np.zeros_like(np.asarray(x, dtype=float))
    for st in stages(prep, s):
        prof = stage_profile(prep, st["growth"], x)
        out.append({**st, "x": x, "bottom": base.copy(), "top": base + prof, "zones": zone_bounds(prep, st["growth"])})
        base = base + prof
    return out


def phase_knots(segments: list[tuple[str, float, float]], phases: list[tuple[set[str], float]]
                ) -> list[tuple[float, float]]:
    """Опорные точки доли показа по фазам: фаза — (фразы, доля к её концу); фазы идут одна за другой во времени."""
    from pipeline.video.timeline import progress_knots
    knots, v0 = [(0.0, 0.0)], 0.0
    for pids, v1 in phases:
        knots += [(t, v0 + v) for t, v in progress_knots(segments, pids, v1 - v0)[1:]]
        v0 = v1
    return knots
