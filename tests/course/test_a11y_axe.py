"""Доступность: axe-core (локальный файл tests/course/vendor/axe.min.js, без CDN) по всем страницам курсов и hub, 390 и 1280, обе темы,
плюс открытые меню и окно книги. serious/critical — ноль. Заодно: ни одной ошибки в консоли браузера. Нет браузера — тест пропускается."""
import json
import shutil
from pathlib import Path

import pytest

playwright_sync = pytest.importorskip("playwright.sync_api")

from pipeline.course import hub
from pipeline.course.build import build

ROOT = Path(__file__).resolve().parents[2]
AXE = Path(__file__).parent / "vendor/axe.min.js"
BB = ROOT / "fixtures/core/live_baraboshkin_par1-2"
PAGES = ("index", "tasks", "progress", "mistakes", "cards", "glossary", "summary", "map", "it")
RUN = """() => axe.run(document, {resultTypes: ['violations']}).then(r => r.violations
  .filter(v => v.impact === 'serious' || v.impact === 'critical')
  .map(v => ({id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target.join(' ') + ' :: ' + n.html.slice(0, 100))})))"""


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("a11y")
    out = tmp / "out"
    d = out / "baraboshkin_par1-2"
    d.mkdir(parents=True)
    for f in ("layer.json", "units.json"):
        shutil.copy2(BB / f, d / f)
    m = out / "mini_test"
    m.mkdir()
    shutil.copy2(ROOT / "fixtures/course/mini_layer.json", m / "layer.json")
    (m / "units.json").write_text(json.dumps({"domain": "geology"}), encoding="utf-8")
    # задания мини-главы — из фикстуры, чтобы проверялись и страницы с заданиями
    (m / "course").mkdir()
    shutil.copy2(ROOT / "fixtures/course/mini_tasks.json", m / "course/tasks.json")
    shutil.copy2(ROOT / "fixtures/course/mini_step_text.json", m / "course/step_text.json")
    for ch in ("baraboshkin_par1-2", "mini_test"):
        build(ch, out_root=out, pages_dir=tmp / "pages", hub=True)
    hub.build_hub(out)
    return out


@pytest.fixture(scope="module")
def browser():
    with playwright_sync.sync_playwright() as p:
        for kw in ({"channel": "msedge"}, {"channel": "chrome"}, {}):
            try:
                b = p.chromium.launch(**kw)
                break
            except Exception:                              # браузера нет — пропускаем, не падаем
                continue
        else:
            pytest.skip("нет браузера для Playwright (msedge/chrome/chromium)")
        yield b
        b.close()


def _pages(out):
    yield "hub", out / "index.html"
    for ch in ("baraboshkin_par1-2", "mini_test"):
        course = out / ch / "course"
        for name in PAGES:
            yield f"{ch}:{name}", course / f"{name}.html"
        for step in sorted(course.glob("step-*.html"))[:2]:
            yield f"{ch}:{step.stem[-24:]}", step


@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("width", [390, 1280])
def test_no_serious_or_critical_axe_violations_and_no_console_errors(site, browser, scheme, width):
    ctx = browser.new_context(viewport={"width": width, "height": 800}, color_scheme=scheme)
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    found = []
    axe = AXE.read_text(encoding="utf-8")
    for label, path in _pages(site):
        page.goto(path.as_uri())
        page.wait_for_timeout(250)
        seen = len(errors)                                  # сообщения самого axe (он читает стили через XHR, на file:// это блокируется) не считаем
        page.add_script_tag(content=axe)
        found += [(label, v["id"], n) for v in page.evaluate(RUN) for n in v["nodes"]]
        del errors[seen:]
    # открытые состояния: меню и окно «страница книги» на странице шага
    step = next(p for _, p in _pages(site) if p.name.startswith("step-baraboshkin"))
    page.goto(step.as_uri())
    page.locator("#open-menu").click()
    page.wait_for_timeout(350)
    seen = len(errors)
    page.add_script_tag(content=axe)
    found += [("меню", v["id"], n) for v in page.evaluate(RUN) for n in v["nodes"]]
    del errors[seen:]
    page.keyboard.press("Escape")
    page.locator(".para .pg:visible").first.click()
    page.wait_for_timeout(450)
    seen = len(errors)
    found += [("окно книги", v["id"], n) for v in page.evaluate(RUN) for n in v["nodes"]]
    del errors[seen:]
    ctx.close()
    assert found == [], "\n".join(f"{l}: {i}: {n}" for l, i, n in found[:12])
    assert errors == [], errors[:3]
