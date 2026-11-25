"""Числа в тексте (цифрами и русскими словами) и сверка с исходными единицами узла."""
import math
import re

_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻−", "0123456789--")
_SUPRUN = re.compile(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+")

_NUM = (r"(?<![\w.,])(\d{1,3}(?:[   ]\d{3})+(?![\d,.]?\d)|\d+)(?:[.,](\d+))?"
        r"(?:\s*·\s*10\s*\^\s*(-?\d+)|\s*\^\s*(-?\d+))?")
_NUM_RE = re.compile(_NUM)


def _prep(text):
    t = _SUPRUN.sub(lambda m: "^" + m.group(0).translate(_SUP), text)
    t = t.replace("−", "-")
    t = re.sub(r"\\cdot|\\times|×|∙", "·", t)
    t = re.sub(r"\^\s*\{\s*(-?\d+)\s*\}", r"^\1", t)
    return t.replace("$", " ")


def digit_numbers(text):
    """Числа цифрами: 0,25 · 5–20 · 10⁻² · 5·10^3 · 2 800 · 40 %. Знак не учитывается."""
    out = []
    for m in _NUM_RE.finditer(_prep(text)):
        ip, fp, e10, ep = m.groups()
        v = float(re.sub(r"\s", "", ip) + ("." + fp if fp else ""))
        if e10 is not None:
            v *= 10.0 ** int(e10)
        elif ep is not None:
            v = v ** int(ep)
        out.append(v)
    return out


# --- числа словами (русский: курс и сценарий всегда на русском) ---

def _soft(nom, gen=None):
    """пять → пять, пяти, пятью."""
    g = gen or nom[:-1] + "и"
    return [nom, g, nom + "ю", g[:-1] + "ью"]


_W = {}


def _add(v, forms):
    for f in forms:
        _W[f] = v


_add(0, ["ноль", "нуль", "ноля", "нуля", "нолем", "нулем"])
_add(1, ["один", "одна", "одно", "одного", "одной", "одному", "одним", "одном", "одну", "одною"])
_add(2, ["два", "две", "двух", "двум", "двумя"])
_add(3, ["три", "трех", "трем", "тремя"])
_add(4, ["четыре", "четырех", "четырем", "четырьмя"])
for _v, _n in [(5, "пять"), (6, "шесть"), (7, "семь"), (9, "девять"), (10, "десять"),
               (11, "одиннадцать"), (12, "двенадцать"), (13, "тринадцать"), (14, "четырнадцать"),
               (15, "пятнадцать"), (16, "шестнадцать"), (17, "семнадцать"), (18, "восемнадцать"),
               (19, "девятнадцать"), (20, "двадцать"), (30, "тридцать")]:
    _add(_v, _soft(_n))
_add(8, ["восемь", "восьми", "восемью", "восьмью"])
_add(40, ["сорок", "сорока"])
for _v, _n, _g in [(50, "пятьдесят", "пятидесяти"), (60, "шестьдесят", "шестидесяти"),
                   (70, "семьдесят", "семидесяти"), (80, "восемьдесят", "восьмидесяти")]:
    _add(_v, [_n, _g])
_add(90, ["девяносто", "девяноста"])
_add(100, ["сто", "ста"])
_add(200, ["двести", "двухсот", "двумстам", "двумястами", "двухстах"])
_add(300, ["триста", "трехсот", "тремстам", "тремястами", "трехстах"])
_add(400, ["четыреста", "четырехсот", "четыремстам", "четырьмястами", "четырехстах"])
for _v, _n, _g in [(500, "пятьсот", "пятисот"), (600, "шестьсот", "шестисот"),
                   (700, "семьсот", "семисот"), (800, "восемьсот", "восьмисот"),
                   (900, "девятьсот", "девятисот")]:
    _add(_v, [_n, _g])
_HALF = {"полтора", "полторы", "полутора"}
_INT_MARK = {"целых", "целая", "целой", "целую"}
_MULT = [("миллиард", 1e9), ("миллион", 1e6), ("тысяч", 1e3)]
_DEN = [("тысячн", 1000), ("десят", 10), ("сот", 100)]   # после «целых»
_TOKEN = re.compile(r"[а-яё]+")


def _mult(w):
    if w.startswith("тысячн"):
        return None
    for stem, v in _MULT:
        if w.startswith(stem):
            return v
    return None


def _den(w):
    for stem, v in _DEN:
        if w.startswith(stem) and w not in _W:
            return v
    return None


def words_to_numbers(text):
    """«двадцать пять» → 25, «две тысячи восемьсот» → 2800, «четыре целых одна десятая» → 4.1."""
    out = []
    total = cur = 0.0
    active = False
    int_part = None
    lone_one = False   # «одна из причин» — не число; «один метр» тоже пропускаем

    def flush():
        nonlocal total, cur, active, int_part, lone_one
        if int_part is not None:
            out.append(int_part)       # «целых» без дробной части
        elif active and not lone_one:
            out.append(total + cur)
        total = cur = 0.0
        active = False
        int_part = None
        lone_one = False

    for w in _TOKEN.findall(text.lower().replace("ё", "е")):
        if w in _W:
            lone_one = (not active) and _W[w] == 1
            cur += _W[w]
            active = True
        elif w in _HALF:
            cur += 1.5
            active = True
        elif active and _mult(w):
            total += (cur or 1) * _mult(w)
            cur = 0.0
            lone_one = False
        elif not active and _mult(w) and int_part is None:
            total, active = _mult(w), True
        elif active and w in _INT_MARK:
            int_part = total + cur
            total = cur = 0.0
            active = False
        elif int_part is not None and active and _den(w):
            out.append(int_part + (total + cur) / _den(w))
            total = cur = 0.0
            active = False
            int_part = None
        else:
            flush()
    flush()
    return out


def extract_numbers(text):
    """Все числа текста: сначала цифрами, потом словами."""
    return digit_numbers(text) + words_to_numbers(text)


def _same(a, b):
    return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-12)


def missing_numbers(text, source_texts):
    """Числа из text, которых нет ни в одном из source_texts (исходные единицы узла)."""
    src = [v for s in source_texts for v in extract_numbers(s)]
    missing = []
    for v in extract_numbers(text):
        if not any(_same(v, s) for s in src) and not any(_same(v, m) for m in missing):
            missing.append(v)
    return missing
