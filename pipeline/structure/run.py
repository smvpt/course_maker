"""python -m pipeline.structure.run --ch <id> | --md <путь> …  → out/<ch>/layer.json + coverage.json

Нужны: out/<ch>/units.json (ingest) и доменный пакет domain/<домен>/ (заблуждения).
"""
import argparse
import json
import os

from contracts.models import ChapterUnits
from pipeline.common import config, domain, io, paths
from pipeline.structure.build import Context, book_meta, build, chapter_title

TYPES_DOC = paths.ORGANIZERS / "06_подача_и_референсы" / "подача_доменов_геологии.md"
VIEWERS = paths.ORGANIZERS / "04_доменные_заготовки" / "портреты_зрителя.md"
EXAMPLE = paths.SCHEMAS / "example_layer.json"


def difficulty_types(pack) -> str:
    """Таблица 8 типов трудности: из доменного пакета (difficulty_types.md), иначе — раздел документа организаторов."""
    if pack.has("difficulty_types.md"):
        return pack.text("difficulty_types.md")
    doc = TYPES_DOC.read_text(encoding="utf-8")
    start = doc.find("## Восемь типов трудности")
    end = doc.find("\n## ", start + 5)
    if start < 0:
        raise ValueError(f"в {TYPES_DOC} нет раздела «Восемь типов трудности»")
    return doc[start:end if end > 0 else None].strip()


def known_terms(spec: config.ChapterSpec) -> str:
    parts = []
    for title, p in (("Карточки-предпосылки", spec.prereq_cards), ("Короткое чтение к главе", spec.prereading)):
        if p:
            parts.append(f"{title}:\n{p.read_text(encoding='utf-8')}")
    return "\n\n".join(parts) or "нет (карточек-предпосылок не выдано)"


def context(spec: config.ChapterSpec) -> Context:
    pack = domain.load(spec.domain)
    example = json.loads(EXAMPLE.read_text(encoding="utf-8"))["nodes"][0]
    return Context(difficulty_types=difficulty_types(pack), viewers=VIEWERS.read_text(encoding="utf-8"),
                   example_node=json.dumps(example, ensure_ascii=False, indent=1),
                   misconceptions=pack.misconceptions, known_terms=known_terms(spec))


def run(spec: config.ChapterSpec):
    os.environ["CH"] = spec.id
    cu = io.load(ChapterUnits, paths.units(spec.id))
    layer, cov = build(cu, spec.md.read_text(encoding="utf-8"), context(spec))
    layer.ext["core"].update({"title": chapter_title(cu.units), **book_meta(spec)})
    io.save(layer, paths.layer(spec.id))
    io.save(cov, paths.coverage(spec.id))
    no_node = sum(1 for r in cov.rows if not r.node_ids)
    claims = sum(len(n.claims) for n in layer.nodes)
    unverified = sum(1 for n in layer.nodes for c in n.claims if not c.ext.get("core", {}).get("quote_verified"))
    print(f"[structure] {spec.id}: {len(layer.nodes)} узлов, {claims} утверждений "
          f"(цитата не подтверждена: {unverified}); единиц {len(cov.rows)}, без узла с причиной: {no_node}")
    return layer, cov


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pipeline.structure.run", description="units.json → layer.json + coverage.json")
    config.add_chapter_args(ap)
    run(config.spec_from_ns(ap.parse_args(argv)))


if __name__ == "__main__":
    main()
