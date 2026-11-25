"""Иллюстрации курса, нарисованные кодом (SVG). Генеративных картинок здесь нет: всё, что видно на рисунке, взято из
слоя главы или посчитано кодом. Цвета, метки происхождения и конвенции — только из styleguide.json (доменный пакет).

Генераторы не знают предметной области: схема утверждений, график по формуле главы, график по таблице книги и условная
колонка слоёв. Что именно рисовать, решают поля узла и styleguide, а не код.

Геометрия: viewBox шириной W=400, шрифт 18 единиц. Рисунок масштабируется под ширину страницы: на телефоне 390 px
(контейнер ≈358 px) 18 единиц дают ≥16 px.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from html import escape
from typing import Optional

from contracts.models import Claim, Node

W = 400
FS = 18                 # размер шрифта в единицах viewBox
LH = 25                 # межстрочный интервал
PAD = 16
CHAR = 0.6              # средняя ширина знака в долях кегля (с запасом: лучше перенести строку, чем вылезти за рамку)
FONT = "system-ui, 'Segoe UI', sans-serif"
LAYER_GROUP = "lithology"   # раздел styleguide.json, описывающий слои разреза (формат организаторов)


# ---------------------------------------------------------------- стиль

def _lum(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def _contrast(a: str, b: str) -> float:
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


class Style:
    """Палитра рисунка из styleguide.json. Ничего, кроме этих цветов, на рисунке не используется."""

    def __init__(self, raw: dict):
        for key in ("background", "panel", "text", "muted", "measurement", "uncertainty", "provenance", "curves", LAYER_GROUP):
            if key not in raw:
                raise ValueError(f"в styleguide нет раздела {key!r}")
        self.raw = raw
        self.bg, self.panel, self.text, self.muted = raw["background"], raw["panel"], raw["text"], raw["muted"]
        self.measurement = raw["measurement"]["color"]
        self.uncertainty = raw["uncertainty"]["color"]

    def prov(self, label: str) -> str:
        if label not in self.raw["provenance"]:
            raise ValueError(f"в styleguide нет метки происхождения {label!r}")
        return self.raw["provenance"][label]

    def curve(self, key: Optional[str]) -> Optional[str]:
        return self.raw["curves"][key]["color"] if key in self.raw["curves"] else None

    def layers(self) -> list[tuple[str, str, str]]:
        return [(k, v["ru"], v["color"]) for k, v in self.raw[LAYER_GROUP].items()]

    def on(self, bg: str) -> str:
        """Цвет текста с лучшим контрастом на заданном фоне (из палитры стайлгайда)."""
        return max((self.text, self.bg), key=lambda c: _contrast(c, bg))

    def colors(self) -> set[str]:
        out: set[str] = set()

        def walk(o):
            if isinstance(o, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", o):
                out.add(o.upper())
            elif isinstance(o, dict):
                [walk(v) for v in o.values()]
        walk(self.raw)
        return out


@dataclass
class Figure:
    kind: str                         # chain | curve | crossplot | column
    svg: str
    frame_class: str                  # A | B
    origin: str                       # code_from_data | code_from_model
    label: str                        # реальные данные | симуляция | схема
    caption: str
    alt: str
    source: Optional[str]
    claim_ids: list[str]
    ext: dict = field(default_factory=dict)


# ---------------------------------------------------------------- рисование

def wrap(text: str, max_chars: int, max_lines: Optional[int] = None) -> list[str]:
    lines: list[str] = []
    cur = ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" .,;:") + "…"
    return lines


class Canvas:
    def __init__(self, style: Style, title: str, desc: str):
        self.s, self.title, self.desc = style, title, desc
        self.parts: list[str] = []
        self.y = PAD

    def chars(self, width: float, bold: bool = False) -> int:
        return max(8, int(width / (FS * (CHAR + (0.04 if bold else 0)))))

    def rect(self, x, y, w, h, fill="none", stroke=None, sw=2, rx=10, dash=None, opacity=None) -> None:
        a = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' fill-opacity="{opacity}"'
        self.parts.append(a + "/>")

    def line(self, x1, y1, x2, y2, stroke, sw=2, dash=None, opacity=None) -> None:
        a = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' stroke-opacity="{opacity}"'
        self.parts.append(a + "/>")

    def text(self, x, y, s: str, fill: str, bold=False, anchor="start") -> None:
        weight = ' font-weight="700"' if bold else ""
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{FS}" fill="{fill}" text-anchor="{anchor}"{weight}>{escape(s)}</text>')

    def block(self, x, y, s: str, width: float, fill: str, bold=False, max_lines=None) -> float:
        """Абзац с переносами. y — верх блока. Возвращает y под блоком."""
        for ln in wrap(s, self.chars(width, bold), max_lines):
            self.text(x, y + FS - 4, ln, fill, bold)
            y += LH
        return y

    def arrow_down(self, x, y1, y2, color) -> None:
        self.line(x, y1, x, y2 - 8, color, 3)
        self.parts.append(f'<path d="M{x - 7:.1f},{y2 - 10:.1f} L{x:.1f},{y2:.1f} L{x + 7:.1f},{y2 - 10:.1f}" fill="none" '
                          f'stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')

    def finish(self, label: str) -> str:
        """Метка происхождения на самой картинке — цветом из styleguide.json."""
        bw = len(label) * FS * CHAR + 28
        by = self.y + 8
        color = self.s.prov(label)
        self.rect(W - PAD - bw, by, bw, 32, fill=color, rx=16)
        self.text(W - PAD - bw / 2, by + 22, label, self.s.on(color), bold=True, anchor="middle")
        h = by + 32 + PAD
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h:.0f}" role="img" aria-labelledby="t d" '
                f'font-family="{FONT}"><title id="t">{escape(self.title)}</title><desc id="d">{escape(self.desc)}</desc>'
                f'<rect width="{W}" height="{h:.0f}" rx="12" fill="{self.s.bg}"/>')
        return head + "".join(self.parts) + "</svg>"


def _alt(title: str, pieces: list[str], limit: int = 420) -> str:
    s = f"{title}. " + "; ".join(pieces)
    return s if len(s) <= limit else s[:limit - 1].rsplit(" ", 1)[0] + "…"


# ---------------------------------------------------------------- 1. схема утверждений (класс B)

KIND_RU = {"observation": "Наблюдение", "assumption": "Допущение", "inference": "Вывод"}
KIND_CAP = {"observation": 3, "assumption": 1, "inference": 2}


def chain(node: Node, style: Style, title: str) -> Figure:
    """Утверждения шага по ролям: наблюдение → допущение → вывод. Стрелка только между ролями, а не между утверждениями:
    причинность не выдумываем, показываем, что автор наблюдал и что из этого вывел. Текст карточек — утверждения слоя."""
    groups = [(k, [c for c in node.claims if c.kind == k][:KIND_CAP[k]]) for k in ("observation", "assumption", "inference")]
    groups = [(k, cs) for k, cs in groups if cs]
    cv = Canvas(style, title, "")
    cv.y = PAD
    cv.y = cv.block(PAD, cv.y, title, W - 2 * PAD, style.text, bold=True, max_lines=3) + 8
    used: list[Claim] = []
    prev_bottom: Optional[float] = None
    for k, cs in groups:
        stroke = {"observation": style.measurement, "assumption": style.uncertainty, "inference": style.muted}[k]
        if prev_bottom is not None:
            cv.arrow_down(W / 2, prev_bottom + 2, cv.y + 12, style.muted)
            cv.y += 14
        cv.text(PAD, cv.y + FS, KIND_RU[k], stroke if k != "inference" else style.text, bold=True)
        cv.y += LH + 4
        for c in cs:
            lines = wrap(c.text, cv.chars(W - 2 * PAD - 24), 6)
            h = len(lines) * LH + 20
            cv.rect(PAD, cv.y, W - 2 * PAD, h, fill=style.panel, stroke=stroke, dash="7 5" if k == "assumption" else None)
            for i, ln in enumerate(lines):
                cv.text(PAD + 12, cv.y + 10 + FS + i * LH - 4, ln, style.text)
            cv.y += h + 10
            used.append(c)
        prev_bottom = cv.y - 10
    cv.desc = "; ".join(f"{KIND_RU[c.kind]}: {c.text}" for c in used)
    svg = cv.finish("схема")
    pages = sorted({c.page_pdf for c in used})
    return Figure(
        kind="chain", svg=svg, frame_class="B", origin="code_from_model", label="схема",
        caption="Утверждения шага по ролям: что автор наблюдает, что допускает и что из этого выводит. "
                "Схема построена кодом из утверждений шага.",
        alt=_alt(f"Схема шага «{title}»", [f"{KIND_RU[c.kind].lower()}: {c.text}" for c in used]),
        source="утверждения шага, стр. " + ", ".join(map(str, pages)), claim_ids=[c.id for c in used])


# ---------------------------------------------------------------- 2. график по формуле главы (класс B, «симуляция»)

def nice_ticks(lo: float, hi: float, n: int = 5) -> list[float]:
    span = hi - lo
    if span <= 0:
        return [lo]
    raw = span / (n - 1)
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    t = math.ceil(lo / step - 1e-9) * step
    out = []
    while t <= hi + step * 1e-9:
        out.append(round(t, 10))
        t += step
    return out


def fmt(v: float) -> str:
    if v == int(v) and abs(v) < 1e7:
        return str(int(v))
    s = f"{v:.4g}"
    if "e" in s:
        m, e = s.split("e")
        s = f"{m}·10^{int(e)}"
    return s.replace(".", ",")


def _axis_label(label: str, unit: str, depth: bool) -> str:
    s = f"{label}, {unit}" if unit else label
    return s + (" (глубина растёт вниз)" if depth else "")


def curve(title: str, x_label: str, x_unit: str, y_label: str, y_unit: str, xs: list[float], ys: list[float],
          depth_axis: str, curve_color: Optional[str], note: str, style: Style) -> str:
    """Линия по значениям, посчитанным кодом. Глубина всегда по вертикали и растёт вниз."""
    if depth_axis == "x":
        h, v, h_lab, v_lab, v_depth = ys, xs, _axis_label(y_label, y_unit, False), _axis_label(x_label, x_unit, True), True
    elif depth_axis == "y":
        h, v, h_lab, v_lab, v_depth = xs, ys, _axis_label(x_label, x_unit, False), _axis_label(y_label, y_unit, True), True
    else:
        h, v, h_lab, v_lab, v_depth = xs, ys, _axis_label(x_label, x_unit, False), _axis_label(y_label, y_unit, False), False
    cv = Canvas(style, title, note)
    cv.y = cv.block(PAD, cv.y, title, W - 2 * PAD, style.text, bold=True, max_lines=3) + 6
    cv.y = cv.block(PAD, cv.y, "по вертикали: " + v_lab, W - 2 * PAD, style.muted, max_lines=3) + 6
    pl, pr, pt, ph = 74, W - PAD - 6, cv.y + 4, 230
    pb = pt + ph
    hlo, hhi = min(h), max(h)
    vlo, vhi = min(v), max(v)
    hp = lambda val: pl + (val - hlo) / ((hhi - hlo) or 1) * (pr - pl)
    vp = (lambda val: pt + (val - vlo) / ((vhi - vlo) or 1) * ph) if v_depth else (lambda val: pb - (val - vlo) / ((vhi - vlo) or 1) * ph)
    for t in nice_ticks(hlo, hhi, 4):
        cv.line(hp(t), pt, hp(t), pb, style.muted, 1, opacity=0.35)
        cv.text(hp(t), pb + 24, fmt(t), style.text, anchor="middle")
    for t in nice_ticks(vlo, vhi, 5):
        cv.line(pl, vp(t), pr, vp(t), style.muted, 1, opacity=0.35)
        cv.text(pl - 8, vp(t) + 6, fmt(t), style.text, anchor="end")
    cv.line(pl, pt, pl, pb, style.muted, 2)
    cv.line(pl, pb if not v_depth else pt, pr, pb if not v_depth else pt, style.muted, 2)
    pts = " ".join(f"{hp(a):.1f},{vp(b):.1f}" for a, b in zip(h, v))
    cv.parts.append(f'<polyline points="{pts}" fill="none" stroke="{curve_color or style.measurement}" stroke-width="3.5" '
                    f'stroke-linejoin="round" stroke-linecap="round"/>')
    cv.y = pb + 34
    cv.y = cv.block(PAD, cv.y, "по горизонтали: " + h_lab, W - 2 * PAD, style.muted, max_lines=3)
    return cv.finish("симуляция")


# ---------------------------------------------------------------- 3. график по таблице книги (класс A)

NUM_RE = re.compile(r"[<>≈~]?\s*[-−–]?\d+(?:[.,]\d+)?\s*%?")


def to_float(cell: str) -> Optional[float]:
    cell = cell.strip()
    if not NUM_RE.fullmatch(cell):
        return None
    m = re.search(r"\d+(?:[.,]\d+)?", cell)
    v = float(m.group(0).replace(",", "."))
    return -v if re.search(r"[-−–]\s*\d", cell) else v


def table_numeric(rows: list[list[str]]) -> Optional[tuple[list[str], list[str], list[list[float]]]]:
    """(заголовки числовых столбцов, подписи строк, значения по столбцам) или None, если таблица не числовая."""
    if len(rows) < 4:                       # заголовок + минимум 3 строки
        return None
    head, body = rows[0], rows[1:]
    width = min(len(r) for r in rows)
    cols = []
    for j in range(1, width):
        vals = [to_float(r[j]) for r in body]
        if sum(v is not None for v in vals) >= max(3, math.ceil(0.8 * len(body))):
            cols.append((head[j].strip(), vals))
    if not cols:
        return None
    keep = [i for i in range(len(body)) if all(vals[i] is not None for _, vals in cols)]
    if len(keep) < 3:
        return None
    return ([h for h, _ in cols], [body[i][0].strip() for i in keep], [[vals[i] for i in keep] for _, vals in cols])


def crossplot(claim: Claim, rows: list[list[str]], title: str, style: Style) -> Optional[Figure]:
    parsed = table_numeric(rows)
    if parsed is None:
        return None
    heads, labels, cols = parsed
    cv = Canvas(style, title, "")
    cv.y = cv.block(PAD, cv.y, title, W - 2 * PAD, style.text, bold=True, max_lines=3) + 6
    if len(cols) >= 2:                      # кроссплот двух числовых столбцов
        xs, ys = cols[0], cols[1]
        cv.y = cv.block(PAD, cv.y, "по вертикали: " + heads[1], W - 2 * PAD, style.muted, max_lines=2) + 6
        pl, pr, pt, ph = 74, W - PAD - 6, cv.y + 4, 230
        pb = pt + ph
        xlo, xhi, ylo, yhi = min(xs), max(xs), min(ys), max(ys)
        xlo, xhi = (xlo, xhi) if xhi > xlo else (xlo - 1, xhi + 1)
        ylo, yhi = (ylo, yhi) if yhi > ylo else (ylo - 1, yhi + 1)
        hp = lambda v: pl + 14 + (v - xlo) / (xhi - xlo) * (pr - pl - 28)
        vp = lambda v: pb - 14 - (v - ylo) / (yhi - ylo) * (ph - 28)
        for t in nice_ticks(xlo, xhi, 4):
            if xlo <= t <= xhi:
                cv.line(hp(t), pt, hp(t), pb, style.muted, 1, opacity=0.35)
                cv.text(hp(t), pb + 24, fmt(t), style.text, anchor="middle")
        for t in nice_ticks(ylo, yhi, 5):
            if ylo <= t <= yhi:
                cv.line(pl, vp(t), pr, vp(t), style.muted, 1, opacity=0.35)
                cv.text(pl - 8, vp(t) + 6, fmt(t), style.text, anchor="end")
        cv.line(pl, pt, pl, pb, style.muted, 2)
        cv.line(pl, pb, pr, pb, style.muted, 2)
        for a, b in zip(xs, ys):
            cv.parts.append(f'<circle cx="{hp(a):.1f}" cy="{vp(b):.1f}" r="7" fill="{style.measurement}"/>')
        cv.y = pb + 34
        cv.y = cv.block(PAD, cv.y, "по горизонтали: " + heads[0], W - 2 * PAD, style.muted, max_lines=2)
        shown = [f"{lab}: {fmt(a)} и {fmt(b)}" for lab, a, b in zip(labels, xs, ys)]
    else:                                   # один числовой столбец: полосы по строкам таблицы
        vals = cols[0]
        cv.y = cv.block(PAD, cv.y, heads[0], W - 2 * PAD, style.muted, max_lines=2) + 4
        top = max(vals) or 1
        for lab, val in zip(labels, vals):
            cv.text(PAD, cv.y + FS, lab, style.text)
            cv.y += LH
            bw = max(4.0, val / top * (W - 2 * PAD - 80))
            cv.rect(PAD, cv.y, bw, 18, fill=style.measurement, rx=4)
            cv.text(PAD + bw + 8, cv.y + 15, fmt(val), style.text)
            cv.y += 18 + 12
        shown = [f"{lab}: {fmt(v)}" for lab, v in zip(labels, vals)]
    svg = cv.finish("реальные данные")
    return Figure(
        kind="crossplot", svg=svg, frame_class="A", origin="code_from_data", label="реальные данные",
        caption="График по таблице книги: значения из таблицы нарисованы кодом, без изменений.",
        alt=_alt(f"График по таблице книги «{title}»", shown), source=f"таблица книги, стр. {claim.page_pdf}",
        claim_ids=[claim.id])


# ---------------------------------------------------------------- 4. условная колонка слоёв (класс B)

def mentioned_layers(node: Node, style: Style) -> list[tuple[str, str, str, list[Claim]]]:
    """Слои из styleguide, которые названы в утверждениях шага, в порядке первого упоминания."""
    found = []
    for key, ru, color in style.layers():
        stem = re.sub(r"\s*\(.*\)", "", ru).strip().lower()
        stem = stem[:-2] if len(stem) >= 6 else stem[:-1] if len(stem) == 5 else stem   # отбрасываем окончание, чтобы совпадали падежи
        pos, hits = None, []
        for i, c in enumerate(node.claims):
            m = re.search(r"(?<!\w)" + re.escape(stem), c.text.lower())
            if m:
                hits.append(c)
                pos = (i, m.start()) if pos is None else pos
        if hits:
            found.append((pos, key, ru, color, hits))
    found.sort(key=lambda t: t[0])
    return [(k, ru, col, hits) for _, k, ru, col, hits in found]


def column(node: Node, style: Style, title: str) -> Optional[Figure]:
    layers = mentioned_layers(node, style)
    if len(layers) < 2:
        return None
    cv = Canvas(style, title, "")
    cv.y = cv.block(PAD, cv.y, title, W - 2 * PAD, style.text, bold=True, max_lines=3) + 6
    cv.y = cv.block(PAD, cv.y, "Условная колонка: показаны только породы, которые упоминает шаг.", W - 2 * PAD, style.muted) + 6
    x0, bw, bh = 96, 250, 52
    top = cv.y
    for i, (_, ru, color, _) in enumerate(layers):
        y = top + i * bh
        cv.rect(x0, y, bw, bh, fill=color, rx=0)
        cv.text(x0 + bw / 2, y + bh / 2 + 6, ru, style.on(color), bold=True, anchor="middle")
    bottom = top + len(layers) * bh
    cv.arrow_down(PAD + 28, top, bottom, style.muted)
    cv.text(PAD, bottom + 28, "глубина ↓", style.muted)
    cv.y = bottom + 40
    cv.y = cv.block(PAD, cv.y, "не в масштабе: порядок и толщины слоёв условные", W - 2 * PAD, style.uncertainty, bold=True) + 2
    claims = []
    for _, _, _, hits in layers:
        claims += [c for c in hits if c not in claims]
    names = [ru for _, ru, _, _ in layers]
    svg = cv.finish("схема")
    return Figure(
        kind="column", svg=svg, frame_class="B", origin="code_from_model", label="схема",
        caption="Условная колонка: какие породы упоминает шаг. Цвета по единой легенде курса. "
                "Порядок и толщины слоёв условные, колонка не показывает реальный разрез.",
        alt=_alt(f"Условная колонка слоёв «{title}», не в масштабе", [", ".join(names)]),
        source="утверждения шага, стр. " + ", ".join(map(str, sorted({c.page_pdf for c in claims}))),
        claim_ids=[c.id for c in claims])
