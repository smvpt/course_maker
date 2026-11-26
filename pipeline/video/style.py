"""Единый дизайн и моушн-стиль серии роликов: общие приёмы для всех шаблонов (T1–T4 и следующих).

Сюжет, объекты и данные задаёт шаблон по учебному узлу и SceneSpec; оформление и движение — только отсюда.

Оформление:
- токены: кегли, отступы, радиусы, толщины контуров, длительности (цвета — только стайлгайд, их передаёт шаблон);
- фактура (texture, grain_overlay): детерминированный крап, без границ слоёв — их рисует шаблон из данных;
- подписи: «таблетка», бирка значения, выноска с линией к точке; стрелка; кольцо внимания; рамка-выделение;
- проверка пересечений подписей (check_no_overlap).

Движение:
- smooth_progress — разгон и торможение хода модели поверх тех же опорных точек времени;
- reveal / show_from — появление с подъёмом и исчезновение; grow_from — рост врезки из точки объекта;
- CameraRig — камера: приближение к области, перелёт между областями, возврат к общему виду; кратность
  приближения считается из геометрии цели; в окнах кадра истинного масштаба камера стоит на общем виде;
- HudLayer — служебный слой (метка происхождения, плашки, подписи фразы, часы, шаги) в экранных координатах:
  при движении камеры он не плывёт и не масштабируется, под ним появляется подложка для читаемости.

Растры, которые сами обновляют pixel_array (поле, полосы, фактура в лупе), — DataImage: прозрачность хранится
отдельно от альфа-маски данных, поэтому порядок обновлений не важен и маска не накапливает искажений.
Всё — функции времени ролика tau (ValueTracker).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Sequence

import numpy as np
from manim import (Circle, Dot, Group, ImageMobject, Line, Polygon, Rectangle, RoundedRectangle, Text, ValueTracker,
                   VGroup, VMobject, always_redraw)
from manim.utils.color import ManimColor

from pipeline.video.layout import FRAME_H, Layout, LayoutError

# ---------------------------------------------------------------- токены
TEXT_PX, CAPTION_PX = 44, 52          # не меньше минимального кегля стайлгайда (проверяет Layout.font_size)
PAD_PX, RADIUS_PX, GAP_PX = 12, 14, 24
STROKE = {"hair": 1.5, "line": 2.0, "bold": 3.0, "accent": 5.0}
FADE_S, RISE_PX = 0.35, 18            # появление: длительность и подъём
PULSE_S = 1.2                         # кольцо внимания: период волны
HIGHLIGHT_S = 1.6                     # рамка-выделение: сколько держится
GROW_S = 0.7                          # рост врезки
TRANS_S = 1.0                         # перелёт камеры
MIN_FOCUS_S = 1.5                     # короче — приближение не делается (не успеть прочитать)
MIN_ZOOM = 1.15                       # слабее — приближение не делается (движение без смысла)
MAX_ZOOM = 2.6                        # предел приближения камеры
SCRIM_OPACITY = 0.88                  # подложка служебного слоя при приближении
SPOT_OPACITY = 0.85                   # приглушение всего, что вне области фокуса
LENS_LINE_OPACITY = 0.55


# ---------------------------------------------------------------- движение и время (чистые функции)

def smoothstep(f: float) -> float:
    f = min(max(f, 0.0), 1.0)
    return f * f * (3 - 2 * f)


def ease_out(f: float) -> float:
    f = min(max(f, 0.0), 1.0)
    return 1 - (1 - f) ** 3


def ease_in_out(f: float) -> float:
    f = min(max(f, 0.0), 1.0)
    return 4 * f ** 3 if f < 0.5 else 1 - (-2 * f + 2) ** 3 / 2


def smooth_progress(raw: float, total: float) -> float:
    """Плавный разгон в начале и торможение в конце хода (0…total); 0 и total сохраняются, ход монотонный."""
    if total <= 0:
        return raw
    return total * smoothstep(raw / total)


def reveal(t: float, a: float, b: float = math.inf, fade: float = FADE_S) -> tuple[float, float]:
    """(непрозрачность, доля подъёма) элемента, видимого на [a, b): проявляется и поднимается, исчезает без сдвига."""
    if t < a or t >= b:
        return 0.0, 1.0
    fin = ease_out((t - a) / fade) if fade > 0 else 1.0
    fout = 1.0 if math.isinf(b) or fade <= 0 else min(1.0, (b - t) / fade)
    return max(0.0, min(fin, fout)), 1.0 - fin


def pulse_state(t: float, t0: float, period: float = PULSE_S, count: int = 2) -> tuple[float, float]:
    """(радиус в долях, непрозрачность) кольца внимания: count расходящихся волн с момента t0."""
    if t < t0 or t >= t0 + period * count:
        return 0.0, 0.0
    f = ((t - t0) % period) / period
    return 0.4 + 0.9 * ease_out(f), 1.0 - f


def highlight_state(t: float, t0: float, hold: float = HIGHLIGHT_S) -> tuple[float, float]:
    """(доля прорисовки контура, непрозрачность) рамки-выделения: прорисовывается, держится, гаснет."""
    if t < t0 or t >= t0 + hold:
        return 0.0, 0.0
    draw = ease_out((t - t0) / 0.45)
    fade = 1.0 - smoothstep((t - (t0 + hold - 0.4)) / 0.4)
    return draw, fade


def grow_state(t: float, t0: float, dur: float = GROW_S) -> float:
    """Масштаб врезки при росте из точки: 0 → 1 с торможением."""
    if t < t0:
        return 0.0
    return ease_out((t - t0) / dur)


def beat_window(segs: Sequence[dict], beats: set[str], after: float = -math.inf) -> tuple[float, float] | None:
    """Окно первой непрерывной серии фраз с битом из beats (не раньше after): от начала первой до конца
    паузы последней. segs — сегменты таймлайна с полем beat."""
    start = end = None
    for s in segs:
        if s.get("beat") in beats and s["start"] >= after:
            if start is None:
                start = s["start"]
            end = s["hold_end"]
        elif start is not None:
            break
    return None if start is None else (start, end)


def shot_window(segs: Sequence[dict], shot_id: str | None) -> tuple[float, float] | None:
    """Окно кадра: от начала первой его фразы до конца паузы последней (None — нет такого кадра)."""
    if shot_id is None:
        return None
    xs = [s for s in segs if s["shot_id"] == shot_id]
    return (xs[0]["start"], xs[-1]["hold_end"]) if xs else None


# ---------------------------------------------------------------- камера: приближение, перелёт, общий вид

Box = tuple[float, float, float, float]       # (x0, x1, y0, y1) в координатах мира


@dataclass
class Focus:
    """Приближение к области box на [a, b): box — кортеж или функция времени ролика (область, которая движется)."""
    a: float
    b: float
    box: Box | Callable[[float], Box]
    name: str = ""
    max_zoom: float = MAX_ZOOM

    def box_at(self, t: float) -> Box:
        return self.box(t) if callable(self.box) else self.box


@dataclass
class CameraRig:
    """Камера как чистая функция времени: общий вид — центр (0, 0), кратность 1; приближение — цель ложится
    в рабочую область кадра area (экранные координаты между служебными полосами). Переход между состояниями —
    за TRANS_S с разгоном и торможением; если следующее приближение начинается вскоре после конца текущего —
    камера перелетает сразу к нему, не возвращаясь к общему виду. В окнах forbidden (кадр истинного масштаба)
    камера обязана стоять на общем виде — иначе ошибка при создании."""
    area: Box
    focuses: list[Focus] = field(default_factory=list)
    forbidden: list[tuple[float, float]] = field(default_factory=list)
    trans: float = TRANS_S

    def __post_init__(self):
        self.focuses = sorted(self.focuses, key=lambda f: f.a)
        for f in self.focuses:
            if not f.b > f.a:
                raise ValueError(f"приближение «{f.name}»: пустое окно [{f.a}, {f.b})")
        for f0, f1 in zip(self.focuses, self.focuses[1:]):
            if f1.a < f0.b:
                raise ValueError(f"приближения «{f0.name}» и «{f1.name}» пересекаются по времени")
        for f in self.focuses:
            for a, b in self.forbidden:
                if f.a < b and f.b + self.trans > a:
                    raise ValueError(f"приближение «{f.name}» задевает кадр истинного масштаба [{a:.2f}, {b:.2f}) — "
                                     f"там камера стоит на общем виде")
        # якоря: (время начала перехода, состояние-цель: индекс приближения или None — общий вид)
        self.anchors: list[tuple[float, int | None]] = [(-math.inf, None)]
        for i, f in enumerate(self.focuses):
            self.anchors.append((f.a, i))
            nxt = self.focuses[i + 1] if i + 1 < len(self.focuses) else None
            if nxt is None or nxt.a - f.b > 1.5 * self.trans:
                self.anchors.append((f.b, None))

    def _target(self, idx: int | None, t: float) -> tuple[float, float, float]:
        if idx is None:
            return 0.0, 0.0, 1.0
        f = self.focuses[idx]
        x0, x1, y0, y1 = f.box_at(t)
        ax0, ax1, ay0, ay1 = self.area
        k = min((ax1 - ax0) / max(x1 - x0, 1e-9), (ay1 - ay0) / max(y1 - y0, 1e-9), f.max_zoom)
        k = max(k, 1.0)
        bx, by = (x0 + x1) / 2, (y0 + y1) / 2
        acx, acy = (ax0 + ax1) / 2, (ay0 + ay1) / 2
        return bx - acx / k, by - acy / k, k                 # экран = (мир − центр) · k

    def state(self, t: float) -> tuple[float, float, float]:
        """(cx, cy, k): центр кадра в мире и кратность приближения в момент t."""
        j = max(i for i, (ta, _) in enumerate(self.anchors) if ta <= t)
        ta, idx = self.anchors[j]
        cur = self._target(idx, t)
        if j == 0 or t - ta >= self.trans:
            return cur
        prev = self._target(self.anchors[j - 1][1], t)
        s = ease_in_out((t - ta) / self.trans)
        lk = math.log(prev[2]) + (math.log(cur[2]) - math.log(prev[2])) * s     # кратность — по логарифму
        k = math.exp(lk)
        # центр так, чтобы точки целей двигались по экрану согласованно с кратностью
        sx0, sy0 = -prev[0] * prev[2], -prev[1] * prev[2]   # сдвиг экрана: экран = мир·k + s
        sx1, sy1 = -cur[0] * cur[2], -cur[1] * cur[2]
        sx, sy = sx0 + (sx1 - sx0) * s, sy0 + (sy1 - sy0) * s
        return -sx / k, -sy / k, k

    def zoom_at(self, t: float) -> float:
        return self.state(t)[2]

    def settled(self, t: float) -> float:
        """Насколько камера «встала» на текущее приближение: 0 в полёте и на общем виде, 1 — на месте."""
        j = max(i for i, (ta, _) in enumerate(self.anchors) if ta <= t)
        ta, idx = self.anchors[j]
        if idx is None:
            return 0.0
        return smoothstep((t - ta - 0.5 * self.trans) / (0.5 * self.trans))

    def active_focus(self, t: float) -> Focus | None:
        """Приближение, к которому камера летит, на котором стоит или от которого возвращается в момент t."""
        j = max(i for i, (ta, _) in enumerate(self.anchors) if ta <= t)
        ta, idx = self.anchors[j]
        if idx is not None:
            return self.focuses[idx]
        if j > 0 and t - ta < self.trans and self.anchors[j - 1][1] is not None:
            return self.focuses[self.anchors[j - 1][1]]
        return None


def plan_camera(area: Box, candidates: Sequence[Focus], forbidden: Sequence[tuple[float, float]],
                trans: float = TRANS_S) -> CameraRig:
    """Камера из кандидатов-приближений по порядку: кандидат, который пересекается с предыдущим или задевает
    кадр истинного масштаба, не берётся (записывается в rig.dropped с причиной)."""
    kept, dropped = [], []
    for f in sorted(candidates, key=lambda f: f.a):
        for a, b in forbidden:                       # укоротить, чтобы возврат закончился до кадра истинного масштаба
            if f.a < a < f.b + trans:
                f = Focus(f.a, a - trans, f.box, f.name, f.max_zoom)
        k_mid = CameraRig(area, [f], [], trans)._target(0, (f.a + f.b) / 2)[2]
        if k_mid < MIN_ZOOM:
            dropped.append((f.name, f"цель уже занимает кадр (×{k_mid:.2f}) — приближение ничего не даёт"))
            continue
        if f.b - f.a < MIN_FOCUS_S:
            dropped.append((f.name, f"после обрезки перед кадром истинного масштаба остаётся {f.b - f.a:.2f} с"))
            continue
        try:
            CameraRig(area, kept + [f], list(forbidden), trans)
            kept.append(f)
        except ValueError as e:
            dropped.append((f.name, str(e)))
    rig = CameraRig(area, kept, list(forbidden), trans)
    rig.dropped = dropped
    return rig


def to_screen(p, state: tuple[float, float, float]) -> np.ndarray:
    cx, cy, k = state
    p = np.asarray(p, dtype=float)
    return np.array([(p[0] - cx) * k, (p[1] - cy) * k, 0.0])


# ---------------------------------------------------------------- фактура

def _rgba(hex_color: str, alpha: int = 255) -> np.ndarray:
    return np.array([*np.round(np.array(ManimColor(hex_color).to_rgb()) * 255), alpha], dtype=np.uint8)


def texture(h: int, w: int, base: str, speck: str, density: float = 0.004, size: int = 2, seed: int = 0,
            mix: float = 0.4, circle: bool = False) -> np.ndarray:
    """RGBA-крап: фон base и детерминированные зёрна speck, смешанные с фоном в доле mix. Без границ слоёв —
    их рисует шаблон из данных, если они есть. circle — прозрачно вне вписанного круга (для врезки)."""
    rng = np.random.default_rng(seed)
    img = np.empty((h, w, 4), dtype=np.uint8)
    img[:] = _rgba(base)
    n = int(h * w * density)
    ys, xs = rng.integers(0, h, n), rng.integers(0, w, n)
    sp = np.round(_rgba(base).astype(float) * (1 - mix) + _rgba(speck).astype(float) * mix).astype(np.uint8)
    for dy in range(size):
        for dx in range(size):
            img[np.clip(ys + dy, 0, h - 1), np.clip(xs + dx, 0, w - 1)] = sp
    if circle:
        img[circle_mask(h, w), 3] = 0
    return img


def grain_overlay(h: int, w: int, speck: str, density: float = 0.003, size: int = 2, seed: int = 0,
                  alpha: int = 70) -> np.ndarray:
    """Прозрачный слой зёрен поверх данных (поле, карта): фактура без изменения цветов данных под ней."""
    rng = np.random.default_rng(seed)
    img = np.zeros((h, w, 4), dtype=np.uint8)
    n = int(h * w * density)
    ys, xs = rng.integers(0, h, n), rng.integers(0, w, n)
    for dy in range(size):
        for dx in range(size):
            img[np.clip(ys + dy, 0, h - 1), np.clip(xs + dx, 0, w - 1)] = _rgba(speck, alpha)
    return img


def circle_mask(h: int, w: int) -> np.ndarray:
    """True — вне вписанного круга."""
    yy, xx = np.mgrid[0:h, 0:w]
    r = min(h, w) / 2
    return (yy - h / 2 + 0.5) ** 2 + (xx - w / 2 + 0.5) ** 2 > r * r


def lens_magnification(lens_radius_px: float, region_radius_m: float, view_m_per_px: float) -> float:
    """Во сколько раз врезка крупнее основного вида: радиус врезки в px против радиуса той же области на виде."""
    return lens_radius_px / (region_radius_m / view_m_per_px)


# ---------------------------------------------------------------- растр данных с отдельной прозрачностью

class DataImage(ImageMobject):
    """Растр, который сам пересчитывает pixel_array (source — массив или функция без аргументов → RGBA uint8).

    Прозрачность появления (set_opacity) хранится отдельно и умножается на альфу данных при каждом пересчёте:
    обновление картинки не возвращает видимость скрытой группе, прозрачные области маски сохраняются,
    многократные обновления не накапливают искажений."""

    def __init__(self, source, **kwargs):
        self._source = source
        base = source() if callable(source) else np.asarray(source)
        self._base = np.array(base, dtype=np.uint8, copy=True)
        self._vis = 1.0
        super().__init__(self._base.copy(), **kwargs)
        if callable(source):
            self.add_updater(lambda m: m.refresh())

    def refresh(self, recompute: bool = True):
        if recompute and callable(self._source):
            self._base = np.asarray(self._source(), dtype=np.uint8)
        arr = self._base.copy()
        arr[..., 3] = np.round(arr[..., 3].astype(float) * self._vis).astype(np.uint8)
        self.pixel_array[:] = arr
        return self

    def set_opacity(self, alpha: float):
        self._vis = float(min(max(alpha, 0.0), 1.0))
        self.refresh(recompute=False)
        return self


def _check_images(mob) -> None:
    """Растр с собственным обновлением внутри появляющейся группы должен быть DataImage (иначе его обновление
    вернёт видимость скрытой группе — ошибка порядка обновлений)."""
    for sm in mob.get_family():
        if isinstance(sm, ImageMobject) and not isinstance(sm, DataImage) and sm.updaters:
            raise TypeError("растр с собственным обновлением в группе с появлением — используйте style.DataImage")


def redraw(func: Callable[[], object]) -> VGroup:
    """Перерисовка без выравнивания точек: каждый кадр дочерние элементы заменяются результатом func().
    В отличие от always_redraw (become), не сопоставляет старую и новую фигуры по числу точек — быстрее и
    устойчиво для полигонов переменной формы (слои, полосы)."""
    g = VGroup()

    def upd(m):
        new = func()
        m.submobjects = list(new.submobjects) if isinstance(new, VGroup) else [new]
    g.add_updater(upd)
    upd(g)
    return g


def set_opacity(mob, op: float) -> None:
    """Непрозрачность любой группы: векторы и растры по отдельности (у Group нет своего set_opacity).
    Внимание: у векторов Manim ставит одну прозрачность и обводке, и заливке — для появления используйте fader."""
    if isinstance(mob, (VMobject, ImageMobject)):
        mob.set_opacity(op)
        return
    for sm in mob.submobjects:
        set_opacity(sm, op)


def fader(mob) -> Callable[[float], None]:
    """Множитель прозрачности для группы с сохранением исходного оформления: у каждого вектора запоминаются
    альфы заливки и обводки (контур без заливки остаётся без заливки), у растров — их собственная прозрачность
    (DataImage) или исходная альфа (ImageMobject). Возвращает apply(op): op ∈ [0, 1] умножает исходные альфы —
    без накопления при многократных вызовах."""
    parts = []
    for sm in mob.get_family():
        if isinstance(sm, ImageMobject):
            parts.append(("img", sm, None, None))
        elif isinstance(sm, VMobject):
            parts.append(("vec", sm, sm.fill_rgbas[:, 3].copy() if len(sm.fill_rgbas) else None,
                          sm.stroke_rgbas[:, 3].copy() if len(sm.stroke_rgbas) else None))

    def apply(op: float) -> None:
        op = float(min(max(op, 0.0), 1.0))
        for kind, sm, fa, sa in parts:
            if kind == "img":
                sm.set_opacity(op)
                continue
            if fa is not None and len(sm.fill_rgbas) == len(fa):
                sm.fill_rgbas[:, 3] = fa * op
            if sa is not None and len(sm.stroke_rgbas) == len(sa):
                sm.stroke_rgbas[:, 3] = sa * op
    return apply


# ---------------------------------------------------------------- проверка пересечений подписей

def bbox(m) -> Box:
    return m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1]


def check_no_overlap(items: Sequence[tuple[str, object]], margin: float = 0.0) -> None:
    """Подписи, шкалы и служебные пометки не пересекаются (по габаритам; margin — зазор в единицах кадра)."""
    boxes = [(n, bbox(m)) for n, m in items if m is not None and len(getattr(m, "points", [])) + len(m.submobjects)]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            (na, a), (nb, b) = boxes[i], boxes[j]
            if a[0] < b[1] + margin and b[0] < a[1] + margin and a[2] < b[3] + margin and b[2] < a[3] + margin:
                raise LayoutError(f"«{na}» пересекается с «{nb}»")


# ---------------------------------------------------------------- служебный слой (экранные координаты)

class HudLayer(Group):
    """Служебный слой поверх мира. Элементы задаются в экранных координатах (общий вид) и при движении камеры
    пересчитываются так, чтобы на экране стоять на месте и сохранять размер. Сначала свои обновления элементов
    (прозрачность, перерисовка), затем привязка к камере. Подъём при появлении — тоже в экранных координатах."""

    def __init__(self, rig_state: Callable[[], tuple[float, float, float]] | None):
        super().__init__()
        self.rig_state = rig_state
        self.items: list[dict] = []

    def register(self, mob, dynamic: bool = False, rise: Callable[[], float] | None = None):
        snap = None if dynamic else [(sm, sm.points.copy()) for sm in mob.get_family() if len(sm.points)]
        self.items.append({"mob": mob, "snap": snap, "rise": rise})
        self.add(mob)
        return mob

    def update(self, dt: float = 0, recursive: bool = True):
        for sm in self.submobjects:
            sm.update(dt, recursive)
        state = self.rig_state() if self.rig_state else (0.0, 0.0, 1.0)
        cx, cy, k = state
        for it in self.items:
            dy = it["rise"]() if it["rise"] else 0.0
            if it["snap"] is None:                               # перерисован заново в экранных координатах
                if (cx, cy, k) != (0.0, 0.0, 1.0) or dy:
                    m = it["mob"]
                    m.shift([0, -dy, 0])
                    m.scale(1 / k, about_point=np.zeros(3)).shift([cx, cy, 0])
                continue
            for sm, pts in it["snap"]:
                p = pts.copy()
                p[:, 1] -= dy
                sm.points = p / k + np.array([cx, cy, 0.0])
        return self


# ---------------------------------------------------------------- набор приёмов, привязанный к сцене

class Kit:
    """Приёмы оформления и движения для одной сцены: шрифт, цвета стайлгайда, компоновка, время ролика tau."""

    def __init__(self, scene, lay: Layout, colors: dict, font: str, tau: ValueTracker):
        self.scene, self.lay, self.c, self.font, self.tau = scene, lay, colors, font, tau
        self.u = lay.units
        self.pad, self.radius, self.gap = self.u(PAD_PX), self.u(RADIUS_PX), self.u(GAP_PX)
        self.rig: CameraRig | None = None
        self.hud_layer = HudLayer(lambda: self.cam_state())
        self._zoom_tag_y = lay.safe_box()[3]

    # -- камера и служебный слой
    def cam_state(self) -> tuple[float, float, float]:
        return self.rig.state(self.tau.get_value()) if self.rig else (0.0, 0.0, 1.0)

    def use_camera(self, rig: CameraRig) -> None:
        """Подключает камеру сцены (MovingCameraScene) к оператору rig. Кадр не меняется, пока rig на общем виде."""
        self.rig = rig
        frame = self.scene.camera.frame
        w0 = frame.width

        def upd(f):
            cx, cy, k = self.cam_state()
            f.set(width=w0 / k)
            f.move_to([cx, cy, 0])
        frame.add_updater(upd)
        self.scene.add(frame)

    def hud(self, mob, dynamic: bool = False, rise: Callable[[], float] | None = None):
        """Добавляет элемент в служебный слой (экранные координаты)."""
        return self.hud_layer.register(mob, dynamic=dynamic, rise=rise)

    def hud_redraw(self, fn: Callable[[], object]):
        """Перерисовываемый служебный элемент (часы, номер шага): fn строит его в экранных координатах."""
        return self.hud(always_redraw(fn), dynamic=True)

    def finish(self, scrim_bands: Sequence[tuple[float, float]] = ()) -> None:
        """Последним в сцене: подложки служебного слоя (полосы по высоте экрана, видимы только при приближении)
        и сам слой — поверх мира."""
        if self.rig is not None:
            left, right = -self.lay.frame_w / 2, self.lay.frame_w / 2
            for y0, y1 in scrim_bands:
                band = Rectangle(width=right - left, height=y1 - y0, stroke_width=0, fill_color=self.c["background"],
                                 fill_opacity=0).move_to([0, (y0 + y1) / 2, 0])

                def upd(m):
                    k = self.cam_state()[2]
                    m.set_fill(opacity=SCRIM_OPACITY * smoothstep((k - 1.0) / 0.15))
                band.add_updater(upd)
                self.hud_layer.items.insert(0, {"mob": band, "snap": [(band, band.points.copy())], "rise": None})
                self.hud_layer.submobjects.insert(0, band)
            spot = always_redraw(self._spotlight)                 # под служебными подписями, над миром
            self.hud_layer.items.insert(0, {"mob": spot, "snap": None, "rise": None})
            self.hud_layer.submobjects.insert(0, spot)
            self.hud_redraw(self._zoom_tag)
        self.scene.add(self.hud_layer)

    def _spotlight(self):
        """Приглушение вне области фокуса (экранные координаты): обрезанные краем кадра подписи уходят в тень,
        внимание — на цели. Сила растёт с кратностью приближения."""
        t = self.tau.get_value()
        f = self.rig.active_focus(t)
        k = self.cam_state()[2]
        op = SPOT_OPACITY * smoothstep((k - 1.0) / 0.3) * self.rig.settled(t)
        if f is None or op <= 0.01:
            return VGroup()
        x0, x1, y0, y1 = f.box_at(t)
        st = self.cam_state()
        a, b = to_screen([x0, y0], st), to_screen([x1, y1], st)
        fl, fr, fb, ft = -self.lay.frame_w / 2, self.lay.frame_w / 2, -FRAME_H / 2, FRAME_H / 2
        sx0, sx1 = max(min(a[0], b[0]), fl), min(max(a[0], b[0]), fr)
        sy0, sy1 = max(min(a[1], b[1]), fb), min(max(a[1], b[1]), ft)
        rects = [(fl, fr, sy1, ft), (fl, fr, fb, sy0), (fl, sx0, sy0, sy1), (sx1, fr, sy0, sy1)]
        g = VGroup()
        for rx0, rx1, ry0, ry1 in rects:
            if rx1 - rx0 > 1e-6 and ry1 - ry0 > 1e-6:
                g.add(Rectangle(width=rx1 - rx0, height=ry1 - ry0, stroke_width=0, fill_color=self.c["background"],
                                fill_opacity=op).move_to([(rx0 + rx1) / 2, (ry0 + ry1) / 2, 0]))
        return g

    def _zoom_tag(self):
        """Кратность текущего приближения — из геометрии камеры (только пока камера приближена)."""
        k = self.cam_state()[2]
        if k < 1.05:
            return VGroup()
        s = f"приближение ×{k:.1f}".replace(".", ",")
        cache = self.__dict__.setdefault("_ztag", {})
        if s not in cache:
            cache[s] = self.pill(self.text(s))
        g = cache[s].copy()
        left, right, bottom, top = self.lay.safe_box()
        return g.move_to([right - g.width / 2, self._zoom_tag_y - g.height / 2, 0])

    def set_zoom_tag_top(self, y: float) -> None:
        self._zoom_tag_y = y

    # -- текст и плашки
    def text(self, s: str, color: str | None = None, px: int = TEXT_PX) -> Text:
        return Text(s, font=self.font, font_size=self.lay.font_size(px), color=color or self.c["text"])

    def pill(self, mob, fill: str | None = None, stroke: str | None | bool = None, opacity: float = 0.95) -> VGroup:
        """«Таблетка» под текстом или группой: скруглённая плашка цвета панели."""
        box = RoundedRectangle(width=mob.width + 2 * self.pad, height=mob.height + 1.4 * self.pad,
                               corner_radius=self.radius, stroke_color=stroke or self.c["muted"],
                               stroke_width=STROKE["line"] if stroke is not False else 0,
                               fill_color=fill or self.c["panel"], fill_opacity=opacity).move_to(mob)
        return VGroup(box, mob)

    def tag(self, s: str, fill: str, text_color: str | None = None) -> VGroup:
        """Цветная бирка (значение, текущее состояние): заливка акцентом, текст цветом фона."""
        t = self.text(s, text_color or self.c["background"])
        box = RoundedRectangle(width=t.width + 1.4 * self.pad, height=t.height + self.pad, corner_radius=self.radius * 0.7,
                               stroke_width=0, fill_color=fill, fill_opacity=1).move_to(t)
        return VGroup(box, t)

    def callout(self, s: str, anchor, box_center, color: str | None = None) -> VGroup:
        """Выноска: таблетка с текстом, линия к точке привязки и точка. Линия — к ближнему краю таблетки."""
        anchor, box_center = np.asarray(anchor, dtype=float), np.asarray(box_center, dtype=float)
        p = self.pill(self.text(s, color)).move_to(box_center)
        box = p[0]
        ex = box.get_left()[0] if anchor[0] < box.get_left()[0] else box.get_right()[0] \
            if anchor[0] > box.get_right()[0] else box_center[0]
        ey = box_center[1] if ex != box_center[0] else (box.get_bottom()[1] if anchor[1] < box_center[1]
                                                         else box.get_top()[1])
        line = Line(anchor, [ex, ey, 0], color=color or self.c["text"], stroke_width=STROKE["line"])
        return VGroup(line, Dot(anchor, radius=self.pad * 0.4, color=color or self.c["text"]), p)

    def follow_callout(self, s: str, anchor_fn: Callable[[], np.ndarray | None], offset, a: float = -math.inf,
                       b: float = math.inf, bounds: Box | None = None):
        """Выноска, которая едет за объектом: таблетка (создаётся один раз) на смещении offset от точки
        anchor_fn(); видна на [a, b) с проявлением; bounds — таблетка не выходит за область (x0, x1, y0, y1).
        anchor_fn может вернуть None — выноски нет (объекта нет на кадре)."""
        pill = self.pill(self.text(s))
        off = np.asarray(offset, dtype=float)

        def draw():
            op = reveal(self.tau.get_value(), a, b)[0]
            p0 = anchor_fn()
            if op <= 0 or p0 is None:
                return VGroup()
            p0 = np.asarray(p0, dtype=float)
            c = p0 + off
            if bounds:
                x0, x1, y0, y1 = bounds
                c[0] = min(max(c[0], x0 + pill.width / 2), x1 - pill.width / 2)
                c[1] = min(max(c[1], y0 + pill.height / 2), y1 - pill.height / 2)
            g = pill.copy().move_to(c)
            box = g[0]
            ex = box.get_left()[0] if p0[0] < box.get_left()[0] else box.get_right()[0]                 if p0[0] > box.get_right()[0] else c[0]
            ey = c[1] if ex != c[0] else (box.get_bottom()[1] if p0[1] < c[1] else box.get_top()[1])
            out = VGroup(Line(p0, [ex, ey, 0], color=self.c["text"], stroke_width=STROKE["line"]),
                         Dot(p0, radius=self.pad * 0.4, color=self.c["text"]), g)
            fader(out)(op)
            return out
        return always_redraw(draw)

    def arrow(self, start, end, color: str | None = None, width: str = "bold") -> VGroup:
        """Стрелка: линия и треугольный наконечник (в единицах кадра, не масштабируется с длиной)."""
        start, end = np.asarray(start, dtype=float), np.asarray(end, dtype=float)
        d = end - start
        n = np.linalg.norm(d[:2])
        col = color or self.c["text"]
        if n < 1e-9:
            return VGroup()
        e = d / n
        nrm = np.array([-e[1], e[0], 0.0])
        tip_l = min(self.u(22), n * 0.6)
        base = end - e * tip_l
        tip = Polygon(end, base + nrm * tip_l * 0.45, base - nrm * tip_l * 0.45, stroke_width=0, fill_color=col,
                      fill_opacity=1)
        return VGroup(Line(start, base, color=col, stroke_width=STROKE[width]), tip)

    # -- время
    def show_from(self, mob, a: float, b: float = math.inf, fade: float = FADE_S, rise: bool = True, hud: bool = False):
        """Появление с a (проявление и подъём на RISE_PX), исчезновение к b. hud — элемент служебного слоя
        (подъём считает слой). Возвращает mob."""
        _check_images(mob)
        rise_u = self.u(RISE_PX) if rise else 0.0
        fade_to = fader(mob)
        if hud:
            def upd_h(m):
                fade_to(reveal(self.tau.get_value(), a, b, fade)[0])
            mob.add_updater(upd_h)
            fade_to(0.0)
            return self.hud(mob, rise=lambda: rise_u * reveal(self.tau.get_value(), a, b, fade)[1])
        state = {"dy": 0.0}

        def upd(m):
            op, r = reveal(self.tau.get_value(), a, b, fade)
            fade_to(op)
            dy = -rise_u * r                                  # смещение — приращением: совместимо с другими сдвигами
            m.shift([0, dy - state["dy"], 0])
            state["dy"] = dy
        mob.add_updater(upd)
        fade_to(0.0)
        return mob

    def grow_from(self, mob, origin, a: float, b: float = math.inf):
        """Рост группы из точки origin (врезка «вырастает» из объекта) и исчезновение к b. Без накопления:
        точки каждый раз строятся от исходных. Растры (DataImage) получают прозрачность отдельно."""
        _check_images(mob)
        origin = np.asarray(origin, dtype=float)
        snap = [(sm, sm.points.copy()) for sm in mob.get_family() if len(sm.points)]
        center = mob.get_center()
        fade_to = fader(mob)

        def upd(m):
            t = self.tau.get_value()
            s = grow_state(t, a) if t < b else 0.0
            op = reveal(t, a, b, FADE_S)[0]
            pivot = origin + (center - origin) * s
            for sm, pts in snap:
                sm.points = pivot + (pts - center) * max(s, 1e-3)
            fade_to(op)
        mob.add_updater(upd)
        fade_to(0.0)
        return mob

    def pulse(self, center_fn: Callable[[], np.ndarray], t0: float, radius: float, color: str | None = None):
        """Кольцо внимания: две расходящиеся волны с момента t0 вокруг точки center_fn()."""
        col = color or self.c["text"]

        def ring():
            k, op = pulse_state(self.tau.get_value(), t0)
            if op <= 0:
                return VMobject()
            return Circle(radius=max(radius * k, 1e-3), color=col, stroke_width=STROKE["bold"],
                          stroke_opacity=op).move_to(center_fn())
        return always_redraw(ring)

    def highlight(self, box_fn: Callable[[], Box], t0: float, color: str | None = None, hold: float = HIGHLIGHT_S):
        """Рамка-выделение: прорисовывается вокруг области, держится и гаснет (кратко, поверх объекта)."""
        col = color or self.c["text"]

        def frame():
            draw, op = highlight_state(self.tau.get_value(), t0, hold)
            if op <= 0:
                return VMobject()
            x0, x1, y0, y1 = box_fn()
            r = RoundedRectangle(width=x1 - x0 + 2 * self.pad, height=y1 - y0 + 2 * self.pad,
                                 corner_radius=self.radius, color=col, stroke_width=STROKE["accent"],
                                 stroke_opacity=op).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
            return r.pointwise_become_partial(r.copy(), 0, max(draw, 1e-3))
        return always_redraw(frame)

    # -- врезка
    def lens(self, center, R: float, content: Group, anchor_fn: Callable[[], np.ndarray], note: str | None,
             backdrop: np.ndarray | None = None, visible: Callable[[], float] | None = None,
             bounds: Box | None = None) -> tuple[Group, VMobject]:
        """Врезка: фон (крап или данные, обрезается по кругу), содержимое шаблона, кольцо и пометка о масштабе
        под кругом (в безопасной зоне); линии-касательные от кольца к точке на основном виде.
        Пометка: для настоящего равномерного приближения — его кратность (lens_magnification), для схемы —
        «схема, размеры условные». Возвращает (врезка, линии) — шаблон добавляет их в нужном порядке слоёв."""
        center = np.asarray(center, dtype=float)
        parts = []
        if backdrop is not None:
            img = backdrop.copy()
            img[circle_mask(*img.shape[:2]), 3] = 0
            bg = DataImage(img)
            bg.stretch_to_fit_width(2 * R).stretch_to_fit_height(2 * R).move_to(center)
            parts.append(bg)
        ring = Circle(radius=R, color=self.c["text"], stroke_width=STROKE["bold"]).move_to(center)
        items = [*parts, content, ring]
        if note:
            label = self.pill(self.text(note, self.c["text"]))
            left, right, _, _ = self.lay.safe_box()
            lo_x, hi_x = (bounds[0], bounds[1]) if bounds else (left, right)
            x = min(max(center[0], lo_x + label.width / 2), hi_x - label.width / 2)   # в безопасной зоне и панели
            label.move_to([x, center[1] - R - self.gap / 3 - label.height / 2, 0])
            items.append(label)
            self.lay.check_inside("пометка врезки", *bbox(label))
        self.lay.check_inside("врезка", *bbox(ring))
        lens = Group(*items)

        def lines():
            vis = visible() if visible else 1.0
            if vis <= 0.01:
                return VGroup()
            a = np.asarray(anchor_fn(), dtype=float)
            d = a - center
            dist = np.linalg.norm(d[:2])
            if dist <= R:
                return VGroup()
            ang = math.atan2(d[1], d[0])
            off = math.acos(min(1.0, R / dist))
            return VGroup(*[Line(center + R * np.array([math.cos(ang + s * off), math.sin(ang + s * off), 0]), a,
                                 color=self.c["text"], stroke_width=STROKE["hair"],
                                 stroke_opacity=LENS_LINE_OPACITY * vis)
                            for s in (-1, 1)])
        return lens, always_redraw(lines)
