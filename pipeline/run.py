"""Сборка главы целиком и пересборка узла (цели make all / rebuild / smoke).

  python -m pipeline.run --ch <id> | --md <путь> [--pdf …] [--pages a-b] [--errata …] [--prereq …] [--domain …] [--video]
  python -m pipeline.run --rebuild <node_id> [--ch <id>]
  python -m pipeline.run --smoke                       (LLM_OFFLINE=1, fixtures/core/mini_chapter, < 3 мин)

Этапы ядра идут в этом процессе, этапы П2–П4 — их точками входа (python -m …) в отдельном процессе.
Нет модуля или этап упал — прогон идёт дальше, где это имеет смысл, а в конце код выхода ≠ 0 и список проблем.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from contracts.models import Layer, Routing
from pipeline.common import config, io, paths

VIDEO_FORMATS = {"шортс": "short", "длинное видео": "long"}
MINI = paths.ROOT / "fixtures" / "core" / "mini_chapter"
SMOKE_CH = "barenblatt_mini"


class Report:
    def __init__(self):
        self.problems: list[str] = []
        self.t0 = time.monotonic()

    def fail(self, msg: str) -> None:
        print(f"[run] ОШИБКА: {msg}", file=sys.stderr)
        self.problems.append(msg)

    def done(self, what: str) -> int:
        dt = time.monotonic() - self.t0
        if self.problems:
            print(f"[run] {what}: НЕ ПОЛНОСТЬЮ за {dt:.0f} с. Проблемы:", file=sys.stderr)
            for p in self.problems:
                print(f"  - {p}", file=sys.stderr)
            return 1
        print(f"[run] {what}: готово за {dt:.0f} с")
        return 0


def has_module(mod: str) -> bool:
    try:
        return importlib.util.find_spec(mod) is not None
    except ModuleNotFoundError:
        return False


def external(rep: Report, mod: str, *args: str) -> bool:
    """Этап другого участника: python -m <mod> <args>. Нет модуля или код ≠ 0 — проблема в отчёте."""
    if not has_module(mod):
        rep.fail(f"нет модуля {mod} — этап пропущен")
        return False
    print(f"[run] → python -m {mod} {' '.join(args)}")
    env = {**os.environ, "PYTHONUTF8": "1"}
    res = subprocess.run([sys.executable, "-m", mod, *args], cwd=paths.ROOT, env=env)
    if res.returncode != 0:
        rep.fail(f"{mod} {' '.join(args)}: код выхода {res.returncode}")
        return False
    return True


def core_stage(rep: Report, name: str, fn, *a, **kw) -> bool:
    print(f"[run] → {name}")
    try:
        fn(*a, **kw)
        return True
    except Exception as e:  # этап ядра упал: дальше по цепочке идти нельзя
        rep.fail(f"{name}: {type(e).__name__}: {e}")
        return False


def downstream(rep: Report, ch: str, video: bool) -> None:
    external(rep, "pipeline.verify.run", "--ch", ch)          # критические ошибки → код ≠ 0, но курс собираем
    external(rep, "pipeline.illus.run", "--ch", ch)
    external(rep, "pipeline.course.build", "--ch", ch)
    if video:
        routing = io.load(Routing, paths.routing(ch))
        for r in routing.routes:
            fmt = VIDEO_FORMATS.get(r.format) or VIDEO_FORMATS.get(r.secondary_format or "")
            if fmt:
                external(rep, "pipeline.video.build", "--ch", ch, "--node", r.node_id, "--format", fmt)


def run_all(spec: config.ChapterSpec, video: bool = False) -> int:
    from pipeline.ingest import run as ingest
    from pipeline.route import run as route
    from pipeline.structure import run as structure

    rep = Report()
    os.environ["CH"] = spec.id
    ok = (core_stage(rep, "ingest", ingest.run, spec)
          and core_stage(rep, "structure", structure.run, spec)
          and core_stage(rep, "route", route.run, spec))
    if ok:
        downstream(rep, spec.id, video)
    return rep.done(f"глава {spec.id}")


def find_chapter(node_id: str) -> str:
    hits = []
    for f in sorted(paths.out_root().glob("*/layer.json")):
        if any(n.id == node_id for n in io.load(Layer, f).nodes):
            hits.append(f.parent.name)
    if len(hits) != 1:
        raise ValueError(f"узел {node_id} найден в главах {hits or 'ни в одной'} — укажи CH=<id главы>")
    return hits[0]


def rebuild(node_id: str, ch: str | None = None) -> int:
    rep = Report()
    ch = ch or find_chapter(node_id)
    os.environ["CH"] = ch
    layer = io.load(Layer, paths.layer(ch))
    if not any(n.id == node_id for n in layer.nodes):
        raise ValueError(f"в {paths.layer(ch)} нет узла {node_id}")
    external(rep, "pipeline.course.build", "--ch", ch, "--node", node_id)
    videos = paths.out_dir(ch) / "videos"
    if videos.exists() and any(d.is_dir() and node_id in d.name for d in videos.iterdir()):
        routing = io.load(Routing, paths.routing(ch))
        r = next((x for x in routing.routes if x.node_id == node_id), None)
        fmt = VIDEO_FORMATS.get(r.format if r else "", "short")
        external(rep, "pipeline.video.build", "--ch", ch, "--node", node_id, "--format", fmt)
    return rep.done(f"пересборка {node_id}")


def smoke() -> int:
    """Без ключа: ingest по mini_chapter; слой, покрытие и маршрутизация — из фикстуры; дальше этапы П2–П4."""
    from pipeline.ingest import run as ingest

    os.environ["LLM_OFFLINE"] = "1"
    rep = Report()
    spec = config.resolve(md=str(MINI / "chapter.md"), ch=SMOKE_CH)
    os.environ["CH"] = spec.id
    if core_stage(rep, "ingest", ingest.run, spec, render_pages=False, vision=False):
        for name in ("layer.json", "coverage.json", "routing.json"):
            shutil.copyfile(MINI / name, paths.out_dir(spec.id) / name)
        print("[run] smoke: layer/coverage/routing — из fixtures/core/mini_chapter (structure и route без ключа не идут)")
        downstream(rep, spec.id, video=False)
    return rep.done("smoke")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pipeline.run", description="глава → курс: весь конвейер")
    config.add_chapter_args(ap)
    ap.add_argument("--video", action="store_true", help="собрать ролики для узлов с видеоформатом")
    ap.add_argument("--rebuild", metavar="NODE_ID", help="пересобрать шаг курса и ролик узла после правки layer.json")
    ap.add_argument("--smoke", action="store_true", help="быстрый прогон без ключа на fixtures/core/mini_chapter")
    ns = ap.parse_args(argv)
    if ns.smoke:
        return smoke()
    if ns.rebuild:
        return rebuild(ns.rebuild, ns.ch)
    return run_all(config.spec_from_ns(ns), video=ns.video)


if __name__ == "__main__":
    sys.exit(main())
