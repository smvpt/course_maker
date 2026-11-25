"""Паспорт доверия главы: out/<ch>/verify/trust.json (П3 показывает его страницей курса).

Покрытие единиц, доля сверенных цитат и чисел, замечания по уровням, ручные минуты из журнала,
стоимость из out/_metrics/llm_calls.jsonl (пишет pipeline.llm).
"""
import json
from datetime import datetime

from contracts.models import Coverage
from journal.cli import minutes as journal_minutes
from pipeline.verify.numbers import extract_numbers
from pipeline.verify.quotes import check_quote_md
from pipeline.verify.terms import node_texts


def _pct(part, total):
    return round(100.0 * part / total, 1) if total else None


def coverage_stats(path):
    if not path.exists():
        raise FileNotFoundError(f"{path} не найден — паспорт доверия без покрытия не строится")
    cov = Coverage.model_validate_json(path.read_text(encoding="utf-8"))
    n = len(cov.rows)
    in_nodes = sum(1 for r in cov.rows if r.node_ids)
    with_reason = sum(1 for r in cov.rows if not r.node_ids and (r.reason or "").strip())
    return {"units": n, "in_nodes": in_nodes, "with_reason": with_reason,
            "pct_in_nodes": _pct(in_nodes, n), "pct_accounted": _pct(in_nodes + with_reason, n)}


def quote_stats(layer, md):
    st = {"found": 0, "other_page": 0, "not_found": 0}
    for n in layer.nodes:
        for c in n.claims:
            st[check_quote_md(md, c.page_pdf, c.quote).status] += 1
    total = sum(st.values())
    return {"claims": total, **st, "pct": _pct(st["found"], total)}


def number_stats(layer, sources):
    total = found = 0
    for n in layer.nodes:
        src = [v for s in sources[n.id] for v in extract_numbers(s)]
        for v in extract_numbers(" \n".join(node_texts(n))):
            total += 1
            found += any(abs(v - s) <= 1e-6 * max(abs(v), abs(s), 1e-12) for s in src)
    return {"total": total, "found": found, "pct": _pct(found, total)}


def cost_stats(calls_path, ch):
    st = {"llm_calls": 0, "cached": 0, "money_usd": 0.0, "unpriced_calls": 0, "tokens_in": 0, "tokens_out": 0}
    if not calls_path.exists():
        return st
    for line in calls_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("chapter") != ch:
            continue
        st["llm_calls"] += 1
        if row.get("cache_hit"):
            st["cached"] += 1
            continue
        st["tokens_in"] += row.get("tokens_in") or 0
        st["tokens_out"] += row.get("tokens_out") or 0
        if row.get("money_usd") is None:
            st["unpriced_calls"] += 1
        else:
            st["money_usd"] += row["money_usd"]
    st["money_usd"] = round(st["money_usd"], 4)
    return st


def build(ch, out_dir, layer, report, md, sources, journal_root, calls_path):
    sev = {s: sum(r.severity == s for r in report.remarks) for s in ("critical", "significant", "minor")}
    manual = journal_minutes(journal_root).get(ch, {"person_minutes": 0, "mentor_minutes": 0, "edits": 0})
    return {
        "chapter": ch,
        "generated": datetime.now().strftime("%Y-%m-%dT%H:%M"),
        "nodes": len(layer.nodes),
        "coverage": coverage_stats(out_dir / "coverage.json"),
        "quotes": quote_stats(layer, md),
        "numbers": number_stats(layer, sources),
        "remarks": sev,
        "manual": manual,
        "cost": cost_stats(calls_path, ch),
    }
