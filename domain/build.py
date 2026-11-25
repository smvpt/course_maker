"""Сборка доменного пакета для нового домена (структура 05_шаблоны/domain_pack_template.md).

python -m domain.build --domain <name> --ch <id главы>           # глава из out/<id>/units.json (после ingest)
python -m domain.build --domain <name> --md <глава.md> [--pages a-b]
                       [--base geology] [--force]

Из главы + базового пакета-образца + LLM: glossary.md, misconceptions.json, physics_checklist.json,
it_bridges.md, pronunciation.md, stress_dictionary.md; styleguide.json — копия базового; errata/ — пустая.
templates/ не создаётся (параметры шаблонов сцен пишет П4). Время сборки — в build_log.json.
"""
import argparse
import json
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field

from pipeline.verify.pages import load_pages, out_root
from pipeline.verify.quotes import md_from_units

DOMAIN_DIR = Path(__file__).resolve().parent


class Term(BaseModel):
    term: str
    en: str
    definition: str
    western: str


class Reading(BaseModel):
    written: str
    spoken: str
    expansion: str


class Stress(BaseModel):
    word: str
    stressed: str


class GlossaryAnswer(BaseModel):
    glossary: list[Term] = Field(min_length=1)
    pronunciation: list[Reading]
    stress: list[Stress]


class Misc(BaseModel):
    id: str = Field(pattern=r"^misc\.[a-z0-9_]+$")
    text: str


class MiscAnswer(BaseModel):
    items: list[Misc] = Field(min_length=1)


class CheckItem(BaseModel):
    id: str = Field(pattern=r"^pc\.[a-z0-9_]+$")
    group: str
    item: str


class ChecklistAnswer(BaseModel):
    items: list[CheckItem] = Field(min_length=1)


class Bridge(BaseModel):
    concept: str
    analogy: str
    breaks_where: str


class BridgesAnswer(BaseModel):
    items: list[Bridge] = Field(min_length=1)


def chapter_text(md, pages=None):
    """Страницы главы с метками <!-- page N -->; pages=None — все страницы файла."""
    all_pages = load_pages(md)
    nums = sorted(all_pages) if pages is None else [p for p in sorted(set(pages)) if p in all_pages]
    if not nums:
        raise ValueError(f"в {md} нет страниц {pages}")
    return "\n".join(f"<!-- page {n} -->\n{all_pages[n].strip()}" for n in nums)


def _unique(items, key):
    ids = [getattr(i, key) for i in items]
    dup = {x for x in ids if ids.count(x) > 1}
    if dup:
        raise ValueError(f"повторяются id: {sorted(dup)}")


def _cell(s):
    return s.replace("|", "\\|").replace("\n", " ").strip()


def _table(header, rows):
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    out += ["| " + " | ".join(_cell(c) for c in r) + " |" for r in rows]
    return "\n".join(out) + "\n"


def build(domain, dst, md, pages=None, base=DOMAIN_DIR / "geology", force=False):
    from pipeline.llm import complete_json
    dst, base = Path(dst), Path(base)
    if dst.exists() and not force:
        raise FileExistsError(f"{dst} уже есть — пакет не перезаписываю (--force, если это нужно)")
    t0 = time.monotonic()
    started = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    text = chapter_text(md, pages)
    ex = {f: (base / f).read_text(encoding="utf-8") for f in
          ("glossary.md", "misconceptions.json", "physics_checklist.json", "it_bridges.md",
           "pronunciation.md", "stress_dictionary.md")}
    jobs = {
        "glossary": ("verify/domain_glossary", GlossaryAnswer,
                     ex["glossary.md"] + "\n" + ex["pronunciation.md"] + "\n" + ex["stress_dictionary.md"]),
        "misc": ("verify/domain_misconceptions", MiscAnswer, ex["misconceptions.json"]),
        "checklist": ("verify/domain_checklist", ChecklistAnswer, ex["physics_checklist.json"]),
        "bridges": ("verify/domain_it_bridges", BridgesAnswer, ex["it_bridges.md"]),
    }

    def run(job):
        prompt, schema, example = job
        return complete_json(prompt=prompt, schema=schema, tier="strong",
                             vars={"domain": domain, "chapter": text, "example": example})

    with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        res = dict(zip(jobs, pool.map(run, jobs.values())))
    g, misc, pc, br = res["glossary"], res["misc"], res["checklist"], res["bridges"]
    _unique(misc.items, "id")
    _unique(pc.items, "id")

    tmp = dst.with_name(dst.name + ".tmp")
    if tmp.exists():
        shutil.rmtree(tmp)
    (tmp / "errata").mkdir(parents=True)
    (tmp / "errata" / ".gitkeep").write_text("", encoding="utf-8")
    note = f"Собрано domain.build ({started}) по главе {Path(md).name} моделью; проверить у ментора.\n\n"
    (tmp / "glossary.md").write_text(f"# Глоссарий — {domain}\n\n" + note + _table(
        ["Термин", "EN", "Определение", "Западный аналог / обозначение"],
        [(t.term, t.en, t.definition, t.western) for t in g.glossary]), encoding="utf-8")
    (tmp / "pronunciation.md").write_text(f"# Как читать аббревиатуры и обозначения — {domain}\n\n" + note + _table(
        ["Пишется", "Читается", "Расшифровка"], [(r.written, r.spoken, r.expansion) for r in g.pronunciation]),
        encoding="utf-8")
    (tmp / "stress_dictionary.md").write_text(f"# Словарь ударений — {domain}\n\n" + note + _table(
        ["Слово", "С ударением"], [(s.word, s.stressed) for s in g.stress]), encoding="utf-8")
    (tmp / "it_bridges.md").write_text(f"# ИТ-мосты — {domain}\n\n" + note + _table(
        ["Предметная область", "ИТ-аналогия", "Где ломается"],
        [(b.concept, b.analogy, b.breaks_where) for b in br.items]), encoding="utf-8")
    (tmp / "misconceptions.json").write_text(
        json.dumps([m.model_dump() for m in misc.items], ensure_ascii=False, indent=1), encoding="utf-8")
    (tmp / "physics_checklist.json").write_text(
        json.dumps([c.model_dump() for c in pc.items], ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.copy(base / "styleguide.json", tmp / "styleguide.json")
    log = {"domain": domain, "chapter_md": str(md), "pages": pages, "base": base.name, "started": started,
           "seconds": round(time.monotonic() - t0, 1), "llm_calls": len(jobs),
           "counts": {"glossary": len(g.glossary), "pronunciation": len(g.pronunciation), "stress": len(g.stress),
                      "misconceptions": len(misc.items), "physics_checklist": len(pc.items),
                      "it_bridges": len(br.items)},
           "templates": "параметры шаблонов сцен — domain/<домен>/templates/ (П4), отчёт: pipeline.video.coverage"}
    (tmp / "build_log.json").write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    if dst.exists():
        shutil.rmtree(dst)
    tmp.rename(dst)
    return dst


def _pages_arg(s):
    out = []
    for part in s.split(","):
        a, _, b = part.strip().partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Сборка доменного пакета для нового домена")
    ap.add_argument("--domain", required=True)
    ap.add_argument("--ch", help="id главы: md и страницы из out/<ch>/units.json")
    ap.add_argument("--md", help="путь к md главы (вместо --ch)")
    ap.add_argument("--pages", help="страницы PDF: a-b[,c-d]")
    ap.add_argument("--base", default="geology", help="пакет-образец в domain/")
    ap.add_argument("--force", action="store_true", help="перезаписать существующий пакет")
    a = ap.parse_args(argv)
    if a.md:
        md, pages = Path(a.md), _pages_arg(a.pages) if a.pages else None
    elif a.ch:
        units = out_root() / a.ch / "units.json"
        md = md_from_units(units)
        pages = _pages_arg(a.pages) if a.pages else json.loads(units.read_text(encoding="utf-8"))["pdf_pages"]
    else:
        ap.error("нужна глава: --ch <id> или --md <путь>")
    dst = build(a.domain, DOMAIN_DIR / a.domain, md, pages, DOMAIN_DIR / a.base, a.force)
    log = json.loads((dst / "build_log.json").read_text(encoding="utf-8"))
    print(f"пакет {a.domain}: {log['counts']} за {log['seconds']} с → {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
