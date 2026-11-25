"""Термин не используется в узлах раньше узла, где он объяснён (terms_introduced)."""
import re
from typing import NamedTuple

from pipeline.verify.pages import normalize


class TermHit(NamedTuple):
    node_id: str       # где термин встретился раньше времени
    term: str
    defined_in: str    # узел, где он объяснён


def _stem(w):
    if len(w) <= 3:
        return w
    return w[:-1] if len(w) <= 5 else w[:-2]


def term_regex(term):
    """Термин с любыми окончаниями слов (рус./англ.): «проницаемость» ловит «проницаемостью»."""
    words = normalize(term).split()
    if not words:
        raise ValueError(f"пустой термин: {term!r}")
    return re.compile(r"\b" + r"\s+".join(re.escape(_stem(w)) + r"\w{0,4}" for w in words) + r"\b")


def node_texts(node):
    """Тексты узла, написанные для читателя (без дословных цитат автора)."""
    L = node.layers
    t = [node.title, node.title_novice or "", node.why_here.text,
         L.topic.text, L.main.text, L.mechanism.text, L.practice.text, L.nuances.text]
    t += [d.text for d in L.deeper]
    t += [c.text for c in node.claims]
    if node.misconception:
        t.append(node.misconception.text)
    dm = node.data_meaning
    t += [dm.from_chapter.text, dm.breaks.text] + [h.text for h in dm.hypotheses]
    t.append(node.it_analogy.text)
    if node.now_practice:
        t.append(node.now_practice.text)
    for w in node.worked_examples:
        t += [w.condition, *w.steps, w.result]
    return [x for x in t if x]


def check_terms(layer):
    nodes = sorted(layer.nodes, key=lambda n: n.order)
    first_def = {}
    for n in nodes:
        for term in n.terms_introduced:
            first_def.setdefault(term, n)
    hits = []
    for term, dnode in first_def.items():
        rx = term_regex(term)
        for n in nodes:
            if n.order >= dnode.order:
                break
            if any(rx.search(normalize(t)) for t in node_texts(n)):
                hits.append(TermHit(n.id, term, dnode.id))
    return sorted(hits, key=lambda h: [n.id for n in nodes].index(h.node_id))
