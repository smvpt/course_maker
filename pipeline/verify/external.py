"""Внешний пакет организаторов (review_package.schema.json) → замечания (review_output.schema.json).

python -m pipeline.verify.external --pkg <package.json> --out <ответ.json> [--team <имя>] [--workers N]

Глава — chapter_file рядом с пакетом (или путь от корня репозитория). Каждая цель проверяется
LLM-критиком со своим контекстом; страницы и цитаты сверяются с md главы.
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from contracts.models import Remark, ReviewOutput, ReviewPackage
from pipeline.verify.critic import ask, page_context, to_remark
from pipeline.verify.pages import load_pages
from pipeline.verify.quotes import check_quote_md

ROOT = Path(__file__).resolve().parents[2]


def _chapter_md(pkg_path, pkg):
    for base in (pkg_path.parent, ROOT):
        p = base / pkg.chapter_file
        if p.exists():
            return p
    raise FileNotFoundError(f"md главы {pkg.chapter_file} не найден ни рядом с пакетом, ни от корня репозитория")


def _claim_view(c):
    return {"id": c.id, "text": c.text, "kind": c.kind, "page_pdf": c.page_pdf, "quote": c.quote}


def _domain_checklist(domain):
    p = ROOT / "domain" / domain / "physics_checklist.json"
    if not p.exists():
        raise FileNotFoundError(f"нет чек-листа физики {p}")
    return p.read_text(encoding="utf-8")


class _Ctx:
    def __init__(self, pkg_path, pkg, domain):
        self.pkg_dir = pkg_path.parent
        self.md = _chapter_md(pkg_path, pkg)
        self.pages = load_pages(self.md)
        self.items = {i.id: i for i in pkg.items}
        self.claims_by_node = {}
        for i in pkg.items:
            if i.type == "claim":
                self.claims_by_node.setdefault(i.node_id, []).append(i)
        self.scenes = {s.video_id: s.spec for s in pkg.scenes}
        self.frames = pkg.frames
        self.checklist = _domain_checklist(domain)

    def node_claims(self, node_id):
        return self.claims_by_node.get(node_id, [])

    def video_node(self, video_id):
        spec = self.scenes.get(video_id) or {}
        return spec.get("node_id")


def _job(ctx, target):
    """(target, item_type, item_dict, context, related, checklist, image, default_page, allowed_pages)"""
    if target in ctx.items:
        it = ctx.items[target]
        d = it.model_dump(exclude_none=True, exclude={"ext"})
        if it.type == "claim":
            pages = [it.page_pdf - 1, it.page_pdf, it.page_pdf + 1]
            related = json.dumps([_claim_view(c) for c in ctx.node_claims(it.node_id) if c.id != it.id],
                                 ensure_ascii=False, indent=1)
            return it.type, d, page_context(ctx.pages, pages), related, "—", None, it.page_pdf, {it.page_pdf}
        if it.type == "script_line":
            ref = ctx.items.get(it.claim_ref)
            if ref is None or ref.type != "claim":
                raise ValueError(f"{it.id}: claim_ref {it.claim_ref} не найден среди утверждений пакета")
            node = ctx.node_claims(ref.node_id)
            related = json.dumps({"claim_ref": _claim_view(ref),
                                  "other_claims_of_node": [_claim_view(c) for c in node if c.id != ref.id]},
                                 ensure_ascii=False, indent=1)
            pages = {ref.page_pdf - 1, ref.page_pdf, ref.page_pdf + 1}
            return it.type, d, page_context(ctx.pages, pages), related, "—", None, ref.page_pdf, {ref.page_pdf}
        # analogy, scene_fact: опора — утверждения узла (и спецификация сцены)
        node = ctx.node_claims(it.node_id)
        if not node:
            raise ValueError(f"{it.id}: у узла {it.node_id} нет утверждений в пакете — страницу взять неоткуда")
        claim_pages = [c.page_pdf for c in node]
        rel = {"node_claims": [_claim_view(c) for c in node]}
        checklist = "—"
        if it.type == "scene_fact":
            rel["scene_spec"] = ctx.scenes.get(it.video_id)
            checklist = ctx.checklist
        related = json.dumps(rel, ensure_ascii=False, indent=1)
        return (it.type, d, page_context(ctx.pages, claim_pages), related, checklist, None,
                claim_pages[0], set(claim_pages))
    # кадр
    f = next(f for f in ctx.frames if f.id == target)
    node = ctx.node_claims(ctx.video_node(f.video_id))
    if not node:
        raise ValueError(f"{f.id}: у ролика {f.video_id} нет узла с утверждениями в пакете")
    claim_pages = [c.page_pdf for c in node]
    others = [x.model_dump(exclude={"ext"}) for x in ctx.frames if x.video_id == f.video_id]
    related = json.dumps({"node_claims": [_claim_view(c) for c in node], "scene_spec": ctx.scenes.get(f.video_id),
                          "all_frames_of_video": others}, ensure_ascii=False, indent=1)
    image = ctx.pkg_dir / f.file
    if not image.exists():
        raise FileNotFoundError(f"нет файла кадра {image}")
    return ("frame", f.model_dump(exclude={"ext"}), page_context(ctx.pages, claim_pages), related, ctx.checklist,
            image, claim_pages[0], set(claim_pages))


def _quote_remark(ctx, it):
    """Детерминированно: цитата утверждения на своей странице."""
    r = check_quote_md(ctx.md, it.page_pdf, it.quote)
    if r.status == "not_found":
        return Remark(target=it.id, category="other", severity="significant", page_pdf=it.page_pdf, quote=None,
                      problem="цитаты нет в главе", fix="заменить дословной цитатой со страницы утверждения")
    if r.status == "other_page":
        return Remark(target=it.id, category="other", severity="minor", page_pdf=r.page, quote=it.quote,
                      problem=f"цитата стоит на стр. {r.page}, а не на {it.page_pdf}", fix=f"page_pdf: {r.page}")
    return None


def _review_one(ctx, target):
    item_type, item, context, related, checklist, image, default_page, allowed = _job(ctx, target)
    v = ask(item_type, item, context, related, checklist, image)
    remark, status = to_remark(target, item_type, v, ctx.md, default_page, allowed)
    if remark is None and item_type == "claim":
        remark = _quote_remark(ctx, ctx.items[target])
    return remark, status


def review(pkg_path, out_path, team="", workers=4, domain="geology"):
    pkg_path = Path(pkg_path)
    pkg = ReviewPackage.model_validate_json(pkg_path.read_text(encoding="utf-8"))
    ctx = _Ctx(pkg_path, pkg, domain)
    targets = [i.id for i in pkg.items] + [f.id for f in pkg.frames]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(lambda t: _review_one(ctx, t), targets))
    remarks = [r for r, _ in results if r is not None]
    unproven = [t for t, (_, s) in zip(targets, results) if s == "unproven"]
    out = ReviewOutput(package_id=pkg.package_id, team=team, remarks=remarks)
    out.ext["verify"] = {"targets": len(targets), "unproven": unproven}
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Модуль проверки: внешний пакет → замечания")
    ap.add_argument("--pkg", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--team", default="")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--domain", default="geology")
    a = ap.parse_args(argv)
    out = review(a.pkg, a.out, a.team, a.workers, a.domain)
    sev = {s: sum(r.severity == s for r in out.remarks) for s in ("critical", "significant", "minor")}
    print(f"{out.package_id}: {len(out.remarks)} замечаний {sev}, без доказательства отброшено "
          f"{len(out.ext['verify']['unproven'])} → {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
