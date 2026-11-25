"""python -m pipeline.verify.run --ch <id> → out/<id>/verify/report.json (ReviewOutput).

Детерминированные проверки слоя (+ задания курса П3 и сценарии П4, если уже есть):
цитаты на своих страницах, числа из исходных единиц, термины не раньше определения.
Код выхода 1, если есть critical.
"""
import argparse
import sys
from pathlib import Path

from contracts.models import ChapterUnits, Layer, Remark, ReviewOutput, SceneSpec, Script, Tasks
from pipeline.verify.numbers import missing_numbers
from pipeline.verify.pages import load_pages, out_root
from pipeline.verify.quotes import check_quote_md, md_from_units
from pipeline.verify.remarks import SEV_ORDER, one_per_target
from pipeline.verify.scene import check_scene, check_script, load_misconceptions
from pipeline.verify.terms import check_terms, node_texts

ROOT = Path(__file__).resolve().parents[2]


def _fmt(nums):
    return ", ".join(f"{v:g}" for v in nums)


def _load(path, model):
    if not path.exists():
        raise FileNotFoundError(f"{path} не найден")
    return model.model_validate_json(path.read_text(encoding="utf-8"))


def node_sources(node, units_by_id, md_pages):
    """Исходные тексты узла: его единицы главы (или его страницы md) + цитаты утверждений."""
    missing = [u for u in node.unit_ids if u not in units_by_id]
    if missing:
        raise ValueError(f"узел {node.id}: единиц {missing} нет в units.json")
    src = [units_by_id[u] for u in node.unit_ids]
    if not src:
        src = [md_pages[p] for p in node.pages if p in md_pages]
    if not src:
        raise ValueError(f"узел {node.id}: нет ни unit_ids, ни страниц из md — числа сверить не с чем")
    return src + [c.quote for c in node.claims]


def _check_claims(layer, md):
    remarks = []
    for node in layer.nodes:
        for c in node.claims:
            r = check_quote_md(md, c.page_pdf, c.quote)
            if r.status == "not_found":
                remarks.append(Remark(
                    target=c.id, category="other", severity="critical", page_pdf=c.page_pdf, quote=None,
                    problem=f"цитата не найдена в главе (лучшее сходство {r.score:.0f}): «{c.quote[:120]}»",
                    fix=f"заменить цитату дословным фрагментом md со стр. {c.page_pdf} или убрать утверждение"))
            elif r.status == "other_page":
                remarks.append(Remark(
                    target=c.id, category="other", severity="significant", page_pdf=r.page, quote=c.quote,
                    problem=f"цитата стоит на стр. {r.page}, а указана стр. {c.page_pdf}",
                    fix=f"page_pdf: {r.page}"))
    return remarks


def _numbers_remark(target, texts, sources, page, where):
    miss = missing_numbers(" \n".join(texts), sources)
    if not miss:
        return None
    return Remark(target=target, category="other", severity="significant", page_pdf=page, quote=None,
                  problem=f"{where}: чисел {_fmt(miss)} нет в исходных единицах узла",
                  fix="заменить числами из исходных единиц главы или убрать")


def _check_numbers(layer, units_by_id, md_pages):
    remarks = []
    for node in layer.nodes:
        src = node_sources(node, units_by_id, md_pages)
        page = node.pages[0] if node.pages else node.claims[0].page_pdf
        for c in node.claims:
            r = _numbers_remark(c.id, [c.text], src, c.page_pdf, "формулировка утверждения")
            if r:
                remarks.append(r)
        rest = [t for t in node_texts(node) if t not in {c.text for c in node.claims}]
        r = _numbers_remark(node.id, rest, src, page, "текст узла")
        if r:
            remarks.append(r)
    return remarks


def _check_terms(layer):
    pages = {n.id: (n.pages[0] if n.pages else n.claims[0].page_pdf) for n in layer.nodes}
    return [Remark(target=h.node_id, category="other", severity="significant", page_pdf=pages[h.defined_in],
                   quote=None, problem=f"термин «{h.term}» используется раньше узла {h.defined_in}, где он объяснён",
                   fix=f"объяснить «{h.term}» здесь или перенести узел {h.defined_in} раньше")
            for h in check_terms(layer)]


def _check_tasks(tasks, nodes, sources):
    remarks = []
    for t in tasks.tasks:
        if t.step_id not in nodes:
            remarks.append(Remark(target=t.id, category="other", severity="significant", page_pdf=None,
                                  problem=f"шаг {t.step_id} не найден в слое", fix="step_id — id узла слоя"))
            continue
        texts = [t.prompt, t.explanation] + [o.text for o in t.options]
        if isinstance(t.answer, (int, float)):
            texts.append(str(t.answer))
        r = _numbers_remark(t.id, texts, sources[t.step_id], nodes[t.step_id].pages[0] if nodes[t.step_id].pages
                            else None, "задание")
        if r:
            remarks.append(r)
    return remarks


def run(ch, out_dir, team=""):
    out_dir = Path(out_dir)
    layer = _load(out_dir / "layer.json", Layer)
    units = _load(out_dir / "units.json", ChapterUnits)
    md = md_from_units(out_dir / "units.json")
    md_pages = load_pages(md)
    units_by_id = {u.unit_id: u.text for u in units.units}
    nodes = {n.id: n for n in layer.nodes}
    sources = {n.id: node_sources(n, units_by_id, md_pages) for n in layer.nodes}
    claim_ids = {c.id for n in layer.nodes for c in n.claims}

    remarks = _check_claims(layer, md) + _check_numbers(layer, units_by_id, md_pages) + _check_terms(layer)
    stats = {"claims": len(claim_ids), "tasks_checked": False, "scripts_checked": []}

    tasks_path = out_dir / "course" / "tasks.json"
    if tasks_path.exists():
        remarks += _check_tasks(_load(tasks_path, Tasks), nodes, sources)
        stats["tasks_checked"] = True
    for sp in sorted((out_dir / "videos").glob("*/script.json")):
        script = _load(sp, Script)
        if script.node_id not in nodes:
            raise ValueError(f"{sp}: узла {script.node_id} нет в слое")
        spec_path = sp.parent / "scene_spec.json"
        if spec_path.exists():
            remarks += check_scene(_load(spec_path, SceneSpec), script, claim_ids, sources[script.node_id],
                                   units.domain)
        else:
            remarks += check_script(script, claim_ids, sources[script.node_id], load_misconceptions(units.domain))
        stats["scripts_checked"].append(script.video_id)

    report = ReviewOutput(package_id=ch, team=team, remarks=one_per_target(remarks))
    report.ext["verify"] = stats
    vdir = out_dir / "verify"
    vdir.mkdir(parents=True, exist_ok=True)
    (vdir / "report.json").write_text(report.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    code = 1 if any(r.severity == "critical" for r in report.remarks) else 0
    return report, code


def main(argv=None):
    ap = argparse.ArgumentParser(description="Детерминированная проверка главы → out/<ch>/verify/report.json")
    ap.add_argument("--ch", required=True)
    ap.add_argument("--team", default="", help="название команды в отчёте (схема требует строку)")
    a = ap.parse_args(argv)
    report, code = run(a.ch, out_root() / a.ch, a.team)
    counts = {s: sum(r.severity == s for r in report.remarks) for s in SEV_ORDER}
    print(f"verify {a.ch}: {len(report.remarks)} замечаний {counts} → out/{a.ch}/verify/report.json")
    return code


if __name__ == "__main__":
    sys.exit(main())
