"""python -m pipeline.ingest.run --ch <id> | --md <путь> [--pdf …] [--pages a-b] [--errata …] [--no-render] [--no-vision]

→ out/<ch>/units.json (+ out/<ch>/chapter.json, сканы data/pages/<ch>/).
"""
import argparse
import os
import sys
from pathlib import Path

from pipeline.common import config, io, paths
from pipeline.ingest import figures, parse, render


def rel(p: Path) -> str:
    p = Path(p).resolve()
    try:
        return p.relative_to(paths.ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def run(spec: config.ChapterSpec, render_pages: bool = True, vision: bool = True):
    os.environ["CH"] = spec.id
    md = spec.md.read_text(encoding="utf-8")
    errata = parse.load_errata(spec.errata) if spec.errata else None
    cu = parse.build_units(md, chapter=spec.id, source=rel(spec.md), pages=spec.page_set(),
                           start_heading=spec.start_heading, end_heading=spec.end_heading,
                           errata=errata, language=spec.language, domain=spec.domain)
    described = 0
    if spec.pdf and render_pages:
        images = render.render_pages(spec.pdf, cu.pdf_pages, spec.id)
        for u in cu.units:
            if u.kind in ("figure", "table"):
                u.image_path = rel(images[u.page_pdf])
        if vision:
            described = figures.describe_figures(cu, images, dict(parse.split_pages(md)))
    elif not spec.pdf:
        print("[ingest] PDF не задан: сканов нет, рисунки — только по подписям и описаниям из md", file=sys.stderr)
    config.save_spec(spec)
    out = io.save(cu, paths.units(spec.id))
    kinds = {}
    for u in cu.units:
        kinds[u.kind] = kinds.get(u.kind, 0) + 1
    print(f"[ingest] {spec.id}: {len(cu.units)} единиц на {len(cu.pdf_pages)} стр. {kinds}; язык {cu.language}; "
          f"описано vision: {described} → {out}")
    return cu


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pipeline.ingest.run", description="md главы → units.json")
    config.add_chapter_args(ap)
    ap.add_argument("--no-render", action="store_true", help="не рендерить сканы страниц")
    ap.add_argument("--no-vision", action="store_true", help="не описывать рисунки vision-моделью")
    ns = ap.parse_args(argv)
    run(config.spec_from_ns(ns), render_pages=not ns.no_render, vision=not ns.no_vision)


if __name__ == "__main__":
    main()
