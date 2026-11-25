"""units → учебный слой (Layer) и покрытие (Coverage).

Этап A (strong): план узлов по всем единицам → цикл покрытия (дозапрос «куда это или почему нет»).
Этап B (strong, по узлу, параллельно): поля узла из полного текста его единиц → цикл цитат.
Всё, что код поправил или отбросил за моделью, записано в ext["core"] (ничего не теряется молча).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Optional

from contracts.models import (ChapterUnits, Claim, Coverage, CoverageRow, DifficultyPair, Field_, Layer, Link,
                              NeedsScan, Node, Unit)
from pipeline.common import config, paths
from pipeline.ingest.parse import split_pages
from pipeline.llm import complete_json, fallbacks, resolve_model
from pipeline.structure import quotes
from pipeline.verify import pages as verify_pages
from pipeline.verify import quotes as verify_quotes
from rapidfuzz import fuzz
from pipeline.structure.schemas import Assignments, ClaimDraft, NodeDraft, Plan, PlanNode, QuoteFix

BAD_REASONS = {"", "непоказуемо", "неважно", "не важно", "слишком сложно"}
COVERAGE_ROUNDS = 2
PLAN_UNIT_CHARS = 250_000          # больше — в плане текст единиц укорачивается


@dataclass
class Context:
    difficulty_types: str
    viewers: str
    example_node: str
    misconceptions: list[dict]
    known_terms: str


def warn(msg: str) -> None:
    print(f"[structure] {msg}", file=sys.stderr)


def slugify(s: str) -> str:
    """Латиница [a-z0-9_]; пустая строка, если букв нет."""
    if not re.search(r"\w", s or ""):
        return ""
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9_]", "_", config.slug_id(s))).strip("_")


def unit_line(u: Unit, limit: Optional[int] = None) -> str:
    core = u.ext.get("core", {})
    text = u.text
    desc = core.get("figure_description")
    if desc and desc != u.text:
        text += "\n(описание моделью) " + desc
    elif desc:
        text = "(описание моделью) " + text
    if limit and len(text) > limit:
        text = text[:limit] + " …"
    return f"[{u.unit_id} | {u.kind} | стр. {u.page_pdf}] {text}"


def excerpt(text: str, n: int = 12) -> str:
    words = re.sub(r"[#$|\\{}*]|━+|-{3,}", " ", text).split()
    return " ".join(words[:n])


# ---------------------------------------------------------------- этап A

def plan_stage(cu: ChapterUnits, ctx: Context) -> tuple[list[PlanNode], dict[str, str], dict]:
    units = cu.units
    total = sum(len(u.text) for u in units)
    limit = 600 if total > PLAN_UNIT_CHARS else None
    plan = complete_json("core/structure_plan", {
        "chapter": cu.chapter, "language": cu.language, "known_terms": ctx.known_terms,
        "difficulty_types": ctx.difficulty_types,
        "units": "\n\n".join(unit_line(u, limit) for u in units),
    }, schema=Plan, tier="strong")

    order = {u.unit_id: i for i, u in enumerate(units)}
    log = {"dropped_unit_ids": [], "bad_reasons": [], "auto_assigned": [], "empty_nodes": []}

    # slug: латиница, уникальный; карта «как назвала модель» → slug
    alias, seen = {}, set()
    for pn in plan.nodes:
        raw, slug = pn.slug, slugify(pn.slug) or "node"
        base, k = slug, 2
        while slug in seen:
            slug, k = f"{base}_{k}", k + 1
        seen.add(slug)
        alias[raw] = alias[slug] = slug
        pn.slug = slug
    for pn in plan.nodes:
        pn.prerequisites = [alias[p] for p in pn.prerequisites if p in alias and alias[p] != pn.slug]
        bad = [x for x in pn.unit_ids if x not in order]
        log["dropped_unit_ids"] += [{"node": pn.slug, "unit_id": x} for x in bad]
        pn.unit_ids = [x for x in dict.fromkeys(pn.unit_ids) if x in order]

    reasons: dict[str, str] = {}

    def take_reason(uid: str, reason: Optional[str]) -> None:
        r = (reason or "").strip()
        if uid in order and r.lower().strip(".") not in BAD_REASONS:
            reasons[uid] = r
        elif uid in order:
            log["bad_reasons"].append({"unit_id": uid, "reason": r})

    for uc in plan.uncovered:
        take_reason(uc.unit_id, uc.reason)

    by_slug = {pn.slug: pn for pn in plan.nodes}
    for _ in range(COVERAGE_ROUNDS):
        assigned = {x for pn in plan.nodes for x in pn.unit_ids}
        missing = [u for u in units if u.unit_id not in assigned and u.unit_id not in reasons]
        if not missing:
            break
        ans = complete_json("core/structure_missing", {
            "nodes": "\n".join(f"- {pn.slug} — {pn.title}" for pn in plan.nodes),
            "units": "\n\n".join(unit_line(u, 1500) for u in missing),
        }, schema=Assignments, tier="strong")
        for a in ans.items:
            node = alias.get(a.node or "") or alias.get(slugify(a.node or ""))
            if node and a.unit_id in order:
                by_slug[node].unit_ids.append(a.unit_id)
            else:
                take_reason(a.unit_id, a.reason)

    # остаток после дозапросов — к узлу соседней единицы, с пометкой
    assigned_at = {}
    for pn in plan.nodes:
        for x in pn.unit_ids:
            assigned_at.setdefault(x, pn.slug)
    for u in units:
        if u.unit_id in assigned_at or u.unit_id in reasons:
            continue
        i = order[u.unit_id]
        near = sorted(assigned_at, key=lambda x: (abs(order[x] - i), order[x] > i))
        if not near:
            raise ValueError("план не отнёс к узлам ни одной единицы главы")
        slug = assigned_at[near[0]]
        by_slug[slug].unit_ids.append(u.unit_id)
        log["auto_assigned"].append({"unit_id": u.unit_id, "node": slug})
        warn(f"{u.unit_id} модель не распределила за {COVERAGE_ROUNDS} дозапроса — отнесена к узлу {slug} по соседству")

    nodes = []
    for pn in plan.nodes:
        pn.unit_ids = sorted(dict.fromkeys(pn.unit_ids), key=order.get)
        if pn.unit_ids:
            nodes.append(pn)
        else:
            log["empty_nodes"].append(pn.slug)
            warn(f"узел {pn.slug} остался без единиц — пропущен")
    for pn in nodes:
        pn.prerequisites = [p for p in pn.prerequisites if p in {n.slug for n in nodes}]
    return nodes, reasons, log


# ---------------------------------------------------------------- этап B

def _model_fields(obj) -> None:
    """Все текстовые поля с пометкой происхождения пишет модель — ставим by_model честно."""
    if isinstance(obj, Field_):
        obj.by_model = True
    elif hasattr(obj, "by_model"):
        obj.by_model = True
    if hasattr(obj, "__dict__"):
        for v in obj.__dict__.values():
            if isinstance(v, list):
                for x in v:
                    _model_fields(x)
            elif hasattr(v, "__dict__") and not isinstance(v, (str, int, float)):
                _model_fields(v)


def check_claim_quote(near: dict[int, str], near_units: dict[int, str], md_path, quote: str,
                      page: int) -> tuple[Optional[int], str, Optional[str]]:
    """(страница, цитата, как найдена). exact — дословно (правило организаторов); recovered — сверка П2 нашла,
    цитата заменена дословным отрывком md; fuzzy — сверка П2 нашла, дословный отрывок не выделить; None — нет."""
    for pages in (near, near_units):              # сырой md, затем текст единиц (колонтитулы убраны)
        found = quotes.find(pages, quote, page)
        if found is not None:
            return found, quote, "exact"
    r = verify_quotes.check_quote_md(md_path, page, quote)        # интерфейс П2 (pipeline/verify/quotes.py)
    if r.status not in ("found", "other_page"):
        return None, quote, None
    raw = near.get(r.page, "") + "\n" + near.get(r.page + 1, "")
    exact = quotes.recover(raw, quote)
    if (exact and quotes.find(near, exact, r.page) == r.page
            and fuzz.ratio(verify_pages.normalize(exact), verify_pages.normalize(quote)) >= verify_quotes.THRESHOLD):
        return r.page, exact, "recovered"
    return r.page, quote, "fuzzy"


def resolve_claim(c: ClaimDraft, near: dict[int, str], near_units: dict[int, str],
                  md_path) -> tuple[Optional[int], str, Optional[str]]:
    """Цитата утверждения: дословно → сверка П2 (+ дословный отрывок md) → дозапрос quote_fix, если не дословно.
    Дозапрос не дал дословной — остаётся похожая (fuzzy), которую нашла сверка П2."""
    page, quote, match = check_claim_quote(near, near_units, md_path, c.quote, c.page_pdf)
    if match in (None, "fuzzy"):
        fix = complete_json("core/quote_fix", {
            "claim": c.text, "quote": c.quote, "page": c.page_pdf,
            "pages": "\n\n".join(f"<!-- page {p} -->\n{t}" for p, t in near.items()),
        }, schema=QuoteFix, tier="default")
        if fix.found and fix.quote:
            p2, q2, m2 = check_claim_quote(near, near_units, md_path, fix.quote, fix.page_pdf or c.page_pdf)
            if p2 is not None and (page is None or m2 != "fuzzy"):
                return p2, q2, m2
    return page, quote, match


def node_stage(pn: PlanNode, idx: int, nodes: list[PlanNode], units_by_id: dict[str, Unit],
               md_pages: dict[int, str], ctx: Context, chapter: str, md_path=None) -> Node:
    node_id = f"{chapter}.{pn.slug}"
    known = [t for n in nodes[:idx] for t in n.terms_introduced]
    nunits = [units_by_id[x] for x in pn.unit_ids]
    d = complete_json("core/structure_node", {
        "node_id": node_id, "title": pn.title,
        "difficulty": f"{pn.difficulty_primary}" + (f" (второй {pn.difficulty_secondary})" if pn.difficulty_secondary else ""),
        "why_here": pn.why_here,
        "plan": "\n".join(f"{i + 1}. {n.slug} — {n.title}" for i, n in enumerate(nodes)),
        "known_terms": ", ".join(known) + ("; " if known else "") + ctx.known_terms,
        "units": "\n\n".join(unit_line(u) for u in nunits),
        "difficulty_types": ctx.difficulty_types,
        "misconceptions": "\n".join(f"{x['id']} — {x['text']}" for x in ctx.misconceptions),
        "viewers": ctx.viewers, "example_node": ctx.example_node,
    }, schema=NodeDraft, tier="strong")

    dropped = []
    pages = sorted({u.page_pdf for u in nunits} | {p for u in nunits for p in u.ext.get("core", {}).get("pages", [])})
    near = {p: md_pages[p] for p in range(pages[0] - 1, pages[-1] + 2) if p in md_pages}
    near_units = quotes.unit_pages([u for u in units_by_id.values() if pages[0] - 1 <= u.page_pdf <= pages[-1] + 1])

    claims = []
    for c in d.claims:
        page, quote, match = resolve_claim(c, near, near_units, md_path)
        if page is None and len(quote.strip()) < 8:
            dropped.append({"claim": c.text, "why": "цитата не найдена и короче 8 символов"})
            warn(f"{node_id}: утверждение без цитаты отброшено: {c.text[:60]}")
            continue
        cl = Claim(id=f"{node_id}#c{len(claims) + 1}", text=c.text, kind=c.kind,
                   page_pdf=page if page is not None else c.page_pdf, quote=quote, source_kind=c.source_kind,
                   by_model=page is None or c.source_kind == "figure_description_model")
        cl.ext["core"] = {"quote_verified": page is not None, "quote_match": match}
        if match == "recovered":
            cl.ext["core"]["quote_by_model"] = c.quote
        if page is None:
            warn(f"{node_id}: цитата не найдена на стр. {c.page_pdf}: «{quote[:60]}»")
        claims.append(cl)
    if not claims:
        raise ValueError(f"{node_id}: ни одного утверждения с цитатой — узел нельзя собрать")

    slugs = {n.slug: f"{chapter}.{n.slug}" for n in nodes}
    misc_ids = {x["id"] for x in ctx.misconceptions}
    links, seen = [], set()
    for l in [*d.links, *(Link(type="prerequisite", target=p) for p in pn.prerequisites)]:
        t = l.target.strip()
        if l.type in ("prerequisite", "example_of"):
            t = slugs.get(t) or slugs.get(slugify(t)) or (t if t in slugs.values() or t.startswith("prereq.") else None)
        elif l.type == "refutes_misconception":
            t = t if t in misc_ids else None
        elif l.type == "to_data":
            t = t if t.startswith("data.") else None
        if t is None or t == node_id:
            dropped.append({"link": l.model_dump(), "why": "цель не найдена"})
            continue
        if (l.type, t) not in seen:
            seen.add((l.type, t))
            links.append(Link(type=l.type, target=t, note=l.note))

    mis = d.misconception
    if mis and mis.ref and mis.ref not in misc_ids:
        dropped.append({"misconception_ref": mis.ref, "why": "нет в списке заблуждений домена"})
        mis.ref = None

    needs = list(d.needs_scan)
    for u in nunits:
        core = u.ext.get("core", {})
        if u.kind == "figure" and u.figure_ref and ("needs_scan" in core or "figure_description" not in core):
            if not any(n.page == u.page_pdf for n in needs):
                needs.append(NeedsScan(page=u.page_pdf, what=core.get("needs_scan") or f"{u.figure_ref}: нет описания рисунка"))

    for part in (d.layers, d.data_meaning, d.it_analogy, d.now_practice, d.inefficiency_lens, mis):
        if part is not None:
            _model_fields(part)

    node = Node(
        id=node_id, order=idx + 1, title=pn.title, title_novice=pn.title_novice,
        why_here=Field_(text=pn.why_here, by_model=True),
        difficulty=DifficultyPair(primary=pn.difficulty_primary, secondary=pn.difficulty_secondary),
        threshold=pn.threshold, layers=d.layers, claims=claims, links=links, misconception=mis,
        data_meaning=d.data_meaning, it_analogy=d.it_analogy, now_practice=d.now_practice,
        inefficiency_lens=d.inefficiency_lens,
        terms_introduced=list(dict.fromkeys([*pn.terms_introduced, *d.terms_introduced])),
        terms_used=d.terms_used, needs_scan=needs, decision_on_data=d.decision_on_data,
        worked_examples=d.worked_examples, book_tasks=d.book_tasks, pages=pages, unit_ids=pn.unit_ids,
    )
    if dropped:
        node.ext["core"] = {"dropped": dropped}
    return node


# ---------------------------------------------------------------- сборка

def term_order_issues(nodes: list[Node]) -> list[dict]:
    first = {}
    for n in nodes:
        for t in n.terms_introduced:
            first.setdefault(t.lower(), n.order)
    return [{"node": n.id, "term": t, "introduced_in_order": first[t.lower()]}
            for n in nodes for t in n.terms_used if first.get(t.lower(), 0) > n.order]


NUMBER_ONLY_HEADING = re.compile(r"^(глава|часть|раздел|chapter|part|section)\s+[\dIVXLCivxlc]+\.?$", re.I)


def chapter_title(units) -> Optional[str]:
    """Название главы — первый заголовок; «Глава V» без названия склеивается со следующим заголовком."""
    heads = [re.sub(r"^#+\s*", "", u.text).strip() for u in units if u.kind == "heading"]
    heads = [h for h in heads if h]
    if not heads:
        return None
    if NUMBER_ONLY_HEADING.match(heads[0]) and len(heads) > 1:
        return f"{heads[0].rstrip('.')}. {heads[1]}"
    return heads[0]


def book_meta(spec: config.ChapterSpec) -> dict:
    """Автор и книга для шапки курса: из конфига или аргументов, иначе из имени PDF «Автор - Книга[ - год]»."""
    if spec.author or spec.book:
        return {"author": spec.author, "book": spec.book, "meta_source": "config"}
    if spec.pdf:
        parts = [x.strip() for x in spec.pdf.stem.split(" - ")]
        if len(parts) >= 2 and all(parts[:2]):
            return {"author": parts[0], "book": parts[1], "meta_source": "pdf_name"}
    return {"author": None, "book": None, "meta_source": None}


def generated_by() -> str:
    model = resolve_model("strong")[0]
    extra = [m for m in fallbacks("strong") if m != model]
    return (f"конвейер «глава → курс», structure, модель {model}"
            + (f" (запасные при лимитах: {', '.join(extra)}; какая ответила — out/_metrics/llm_calls.jsonl)"
               if extra else ""))


def build(cu: ChapterUnits, md: str, ctx: Context) -> tuple[Layer, Coverage]:
    nodes_plan, reasons, log = plan_stage(cu, ctx)
    units_by_id = {u.unit_id: u for u in cu.units}
    md_pages = dict(split_pages(md))
    workers = int(os.environ.get("LLM_WORKERS", "4"))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        md_path = Path(cu.source) if Path(cu.source).is_absolute() else paths.ROOT / cu.source
        nodes = list(ex.map(lambda a: node_stage(a[1], a[0], nodes_plan, units_by_id, md_pages, ctx, cu.chapter,
                                                 md_path),
                            enumerate(nodes_plan)))

    layer = Layer(chapter=cu.chapter, source=cu.source, pdf_pages=[str(p) for p in cu.pdf_pages],
                  generated_by=generated_by(),
                  nodes=nodes)
    layer.ext["core"] = {"plan": log, "term_order_issues": term_order_issues(nodes)}

    owners: dict[str, list[str]] = {}
    for n in nodes:
        for x in n.unit_ids:
            owners.setdefault(x, []).append(n.id)
    rows = [CoverageRow(unit_id=u.unit_id, kind=u.kind, page_pdf=u.page_pdf, excerpt=excerpt(u.text),
                        node_ids=owners.get(u.unit_id, []),
                        reason=None if u.unit_id in owners else reasons[u.unit_id])
            for u in cu.units]
    return layer, Coverage(chapter=cu.chapter, rows=rows)
