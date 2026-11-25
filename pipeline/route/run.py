"""python -m pipeline.route.run --ch <id> | --md <путь> …  → out/<ch>/routing.json (нужен layer.json)."""
import argparse
import os
from collections import Counter

from contracts.models import Layer
from pipeline.common import config, domain, io, paths
from pipeline.route.build import route
from pipeline.structure.run import difficulty_types


def run(spec: config.ChapterSpec):
    os.environ["CH"] = spec.id
    layer = io.load(Layer, paths.layer(spec.id))
    r = route(layer, difficulty_types(domain.load(spec.domain)))
    io.save(r, paths.routing(spec.id))
    print(f"[route] {spec.id}: {dict(Counter(x.format for x in r.routes))}; "
          f"крючков {sum(1 for x in r.routes if x.hook_short)}")
    return r


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pipeline.route.run", description="layer.json → routing.json")
    config.add_chapter_args(ap)
    run(config.spec_from_ns(ap.parse_args(argv)))


if __name__ == "__main__":
    main()
