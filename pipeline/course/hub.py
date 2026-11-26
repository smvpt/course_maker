"""Главная всех курсов: out/index.html (+ out/assets). Сканирует out/*/course/course.json (его пишет pipeline.course.build).

python -m pipeline.course.hub [--out out]

Статичный офлайн-сайт: данные курсов и индекс поиска встроены JSON-ом, без fetch; ссылки относительные (<ch>/course/index.html).
Прогресс и «последний курс» читает JS из localStorage (общий ключ course:last и ключи course:<ch>:…); если localStorage на file://
недоступен — статусы «Не начат», без ошибок.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from markupsafe import Markup

from pipeline.course.build import make_env

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def fixture_chapters() -> set[str]:
    """Id синтетических глав из fixtures/course (мини-глава и т. п.): на главную они не попадают. Настоящие главы, чей выход лежит в
    fixtures/core (живой выход ядра), — не фикстуры."""
    ids = set()
    for f in (ROOT / "fixtures/course").glob("*.json"):
        try:
            ch = json.loads(f.read_text(encoding="utf-8")).get("chapter")
        except (OSError, ValueError):
            continue
        if isinstance(ch, str):
            ids.add(ch)
    return ids


def collect(out_root: Path, include_fixtures: bool = False) -> list[dict]:
    """Данные каждого собранного курса: out/<ch>/course/course.json. Курс без course.json (собран старой версией) — громкое предупреждение.
    Тестовые фикстуры (fixtures/course/*) пропускаются, если не просили include_fixtures."""
    courses = []
    skip = set() if include_fixtures else fixture_chapters()
    for d in sorted(p for p in out_root.iterdir() if p.is_dir()):
        course = d / "course"
        if not (course / "index.html").exists() or d.name in skip:
            continue
        info = course / "course.json"
        if not info.exists():
            print(f"WARNING: {course}: нет course.json (курс собран старой версией), в главную не включён: пересоберите курс", file=sys.stderr)
            continue
        data = json.loads(info.read_text(encoding="utf-8"))
        if data["ch"] != d.name:
            raise ValueError(f"{info}: ch={data['ch']!r}, а папка называется {d.name!r}")
        courses.append(data)
    return courses


def build_hub(out_root: Path, include_fixtures: bool = False) -> Path:
    out_root = Path(out_root)
    courses = collect(out_root, include_fixtures)
    if not courses:
        raise FileNotFoundError(f"в {out_root} нет собранных настоящих курсов (out/<глава>/course/index.html с course.json; тестовые фикстуры "
                                "на главной не показываются): сначала make course CH=<id>")
    assets = out_root / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    first = out_root / courses[0]["ch"] / "course" / "assets"
    shutil.copy2(first / "tokens.css", assets / "tokens.css")                      # цвета и тема — те же, что в курсах
    for f in ("course.css", "hub.css", "hub.js"):
        shutil.copy2(HERE / "assets" / f, assets / f)
    shutil.copytree(HERE / "assets/brand", assets / "brand", dirs_exist_ok=True)
    env = make_env()
    env.used_icons.clear()
    search = [{**e, "c": c["ch"], "ct": c["title"]} for c in courses for e in c["search"]]
    data = [{k: c[k] for k in ("ch", "title", "author", "book", "minutes", "tasks", "steps", "task_ids")} for c in courses]
    html = env.get_template("hub.html.j2").render(
        courses=data, totals={"steps": sum(len(c["steps"]) for c in courses), "tasks": sum(c["tasks"] for c in courses)}, data_json=Markup(json.dumps(data, ensure_ascii=False).replace("</", "<\\/")),
        search_json=Markup(json.dumps(search, ensure_ascii=False).replace("</", "<\\/")))
    home = out_root / "index.html"
    home.write_text(html, encoding="utf-8")
    return home


def main() -> None:
    ap = argparse.ArgumentParser(description="главная всех курсов: out/index.html")
    ap.add_argument("--out", type=Path, default=Path(os.environ.get("OUT_DIR") or ROOT / "out"), help="корень out/")
    ap.add_argument("--with-fixtures", action="store_true", help="показать и тестовые фикстуры (fixtures/course/*)")
    a = ap.parse_args()
    print(f"главная всех курсов: {build_hub(a.out, include_fixtures=a.with_fixtures)}")


if __name__ == "__main__":
    main()
