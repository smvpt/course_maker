"""Точка входа ingest: md (+PDF) → out/<ch>/units.json; vision подменён."""
import json

import jsonschema  # noqa: F401  (зависимость тестов ядра)
import pypdfium2 as pdfium
import pytest

from contracts import models as m
from pipeline.common import config, io, paths
from pipeline.ingest import figures, run

MD = """<!-- page 1 -->
# Глава 1. Пласт

Абзац о пласте.

Рис. 1. Разрез пласта

<!-- page 2 -->
Второй абзац.
"""


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setattr(paths, "DATA", tmp_path / "data")
    md = tmp_path / "Глава Пласт.md"
    md.write_text(MD, encoding="utf-8")
    return tmp_path, md


def test_run_without_pdf(env):
    tmp, md = env
    run.main(["--md", str(md), "--no-vision"])
    ch = config.slug_id(md.stem)
    cu = io.load(m.ChapterUnits, tmp / "out" / ch / "units.json")
    assert [u.kind for u in cu.units] == ["heading", "paragraph", "figure", "paragraph"]
    assert config.chapter(ch).md == md                     # дальше этапы находят главу по --ch


def test_run_with_pdf_and_vision(env, monkeypatch):
    tmp, md = env
    pdf = pdfium.PdfDocument.new()
    for _ in range(2):
        pdf.new_page(200, 300)
    pdf_path = tmp / "book.pdf"
    pdf.save(str(pdf_path))
    calls = []

    def fake(prompt, vars, schema, tier, images):
        calls.append((prompt, tier, images))
        return schema(description="Разрез: пласт песчаника между глинами.", legend="1 — песчаник", readable=True)
    monkeypatch.setattr(figures, "complete_json", fake)
    monkeypatch.setattr(run.render, "paths", paths)
    run.main(["--md", str(md), "--pdf", str(pdf_path), "--ch", "plast"])
    cu = io.load(m.ChapterUnits, tmp / "out" / "plast" / "units.json")
    fig = [u for u in cu.units if u.kind == "figure"][0]
    assert fig.ext["core"]["figure_description_by_model"] is True
    assert "Легенда: 1 — песчаник" in fig.ext["core"]["figure_description"]
    assert fig.image_path.endswith("p1.png")
    assert calls == [("core/figure_describe", "vision", [tmp / "data" / "pages" / "plast" / "p1.png"])]


def test_pdf_page_mismatch_fails(env):
    tmp, md = env
    pdf = pdfium.PdfDocument.new()
    pdf.new_page(200, 300)
    pdf.save(str(tmp / "one.pdf"))
    with pytest.raises(ValueError, match="страниц"):
        run.main(["--md", str(md), "--pdf", str(tmp / "one.pdf"), "--no-vision"])
