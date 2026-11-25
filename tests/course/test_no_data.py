"""Пустые состояния и «нет данных» (мини-глава без иллюстраций, видео, routing, заданий) и открытие двойным кликом (file://)."""
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path

import pytest

from pipeline.course import hub
from pipeline.course.build import build

ROOT = Path(__file__).resolve().parents[2]


class _Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.text, self.srcs = [], set(), [], []
        self._skip = 0

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip += 1
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("script", "img", "link", "video", "source", "track") and (a.get("src") or a.get("href")):
            self.srcs.append(a.get("src") or a.get("href"))

    def handle_data(self, data):
        if data.strip() and not self._skip:
            self.text.append(data.strip())


def _parse(path: Path) -> _Page:
    p = _Page()
    p.feed(path.read_text(encoding="utf-8"))
    return p


@pytest.fixture(scope="module")
def bare(tmp_path_factory):
    """Мини-глава без иллюстраций, видео, routing и заданий; рядом — hub."""
    out = tmp_path_factory.mktemp("bare") / "out"
    d = out / "mini_test"
    d.mkdir(parents=True)
    shutil.copy2(ROOT / "fixtures/course/mini_layer.json", d / "layer.json")
    (d / "units.json").write_text(json.dumps({"domain": "geology"}), encoding="utf-8")
    course = build("mini_test", out_root=out, pages_dir=out / "pages", hub=True)
    hub.build_hub(out)
    return out, course


def test_no_broken_links_or_anchors_on_any_page(bare):
    out, course = bare
    for page in list(course.glob("*.html")) + [out / "index.html"]:
        parsed = _parse(page)
        for href in parsed.links + parsed.srcs:
            if href.startswith(("#", "mailto:")):
                assert href[1:] == "" or href[1:] in parsed.ids or href == "#", (page.name, href)
                continue
            target, _, frag = href.partition("#")
            path = (page.parent / target).resolve()
            assert path.exists(), (page.name, href)                              # ссылка не ведёт в пустоту
            if frag and path.suffix == ".html":
                assert frag in _parse(path).ids, (page.name, href)               # и якорь есть на целевой странице


def test_no_zero_counts_placeholders_or_empty_frames(bare):
    out, course = bare
    for page in list(course.glob("*.html")) + [out / "index.html"]:
        html = page.read_text(encoding="utf-8")
        body = " ".join(_parse(page).text)
        assert not re.search(r"\b0 (задани|заданий)|0 из 0|\bNone\b|undefined|NaN|\{\{|\}\}", body), (page.name, re.search(r"\b0 (задани|заданий)|0 из 0|\bNone\b|undefined|NaN|\{\{|\}\}", body).group())
        assert not re.search(r'<(ul|ol|dl|section|nav)\b(?![^>]*\bid=")[^>]*>\s*</\1>', html), page.name   # пустых списков и рамок нет (списки с id наполняет JS)
        assert not re.search(r'<(p|h[1-6]|button|a|li)\b[^>]*>\s*</\1>', html.replace("<script", "<x-script")), page.name


def test_pages_without_data_are_not_offered_in_menu_or_tiles(bare):
    out, course = bare
    index = (course / "index.html").read_text(encoding="utf-8")
    menu = re.search(r'<dialog id="menu".*?</dialog>', index, re.S).group(0)
    assert 'href="tasks.html"' not in menu and 'href="progress.html"' not in menu and 'href="mistakes.html"' not in menu      # заданий нет
    assert 'href="cards.html"' in menu and 'href="summary.html"' in menu
    tiles = re.findall(r'<span class="tile-t">([^<]+)</span>', index)
    assert "Все задания" not in tiles and ("Лист опечаток" in tiles) == (course / "errata.html").exists()      # плитка есть, только если есть что показать
    assert 'class="lead">' in index and not re.search(r"\d+ заданий", index.split('class="lead">')[1].split("</p>")[0])
    assert "<video" not in index and "illus" not in index                                             # ни видео, ни иллюстраций


def test_step_pages_without_illustrations_video_and_routing_have_no_empty_blocks(bare):
    out, course = bare
    for page in course.glob("step-*.html"):
        html = page.read_text(encoding="utf-8")
        assert 'id="b-media"' not in html and 'id="b-illus"' not in html and 'id="b-interactive"' not in html or "b-interactive" in html
        for m in re.finditer(r'<section class="tier[^"]*" id="tier-([a-z]+)"(.*?)\n</section>\n(?=<section class="tier|</div><!--/step-body-->)', html, re.S):
            assert m.group(2).count('class="block') >= 1, (page.name, m.group(1))
        assert "Ролик по этому шагу не собран" not in html                                            # нет ролика — нет и блока-пустышки
        assert not re.search(r'<section id="b-[a-z]+" class="block[^"]*"><h3 class="block-h">[^<]*(?:<svg.*?</svg>)?[^<]*</h3>\s*</section>', html, re.S)


# ---------------------------------------------------------------- двойной клик: file://, без сети, ≤ 30 МБ
def test_everything_opens_from_files_without_network_and_fits_the_size_limit(bare):
    out, course = bare
    files = [f for f in out.rglob("*") if f.is_file()]
    for f in files:
        if f.suffix in (".html", ".js", ".css") and "katex" not in f.parts:
            text = f.read_text(encoding="utf-8")
            assert "fetch(" not in text and "XMLHttpRequest" not in text and "navigator.sendBeacon" not in text, f.name
            assert not re.search(r'(?:src|href)="(?:https?:)?//', text), f.name                    # ни одной внешней ссылки (xmlns SVG — не ссылка)
            assert not re.search(r"url\(\s*['\"]?https?:", text), f.name
            assert not re.search(r"@import\s+(?:url\()?['\"]?https?:", text), f.name
    css = (course / "assets/katex/katex.min.css").read_text(encoding="utf-8")
    assert not re.search(r"url\(\s*['\"]?https?:", css)
    assert sum(f.stat().st_size for f in files) <= 30 * 1024 * 1024
