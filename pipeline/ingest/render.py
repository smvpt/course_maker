"""Сканы страниц PDF → data/pages/<ch>/p<N>.png. Номер страницы = метка <!-- page N --> = страница PDF (с 1)."""
from pathlib import Path

from pipeline.common import paths

DPI = 110


def render_pages(pdf: Path, pages: list[int], ch: str, dpi: int = DPI) -> dict[int, Path]:
    import pypdfium2 as pdfium

    out = paths.pages_dir(ch)
    out.mkdir(parents=True, exist_ok=True)
    doc = pdfium.PdfDocument(str(pdf))
    n = len(doc)
    bad = [p for p in pages if not 1 <= p <= n]
    if bad:
        raise ValueError(f"в {pdf} {n} страниц, а в главе есть страницы {bad[:5]} — md и PDF не от одной книги?")
    done = {}
    for p in pages:
        f = out / f"p{p}.png"
        if not f.exists():
            doc[p - 1].render(scale=dpi / 72).to_pil().save(f)
        done[p] = f
    doc.close()
    return done
