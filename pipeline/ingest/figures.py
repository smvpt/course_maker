"""Описание рисунков vision-моделью — только для подписей, у которых нет описания от конвертера md."""
from typing import Optional

from pydantic import BaseModel

from contracts.models import ChapterUnits
from pipeline.llm import complete_json


class FigureDescription(BaseModel):
    description: str
    legend: Optional[str] = None
    readable: bool
    unreadable: Optional[str] = None


def describe_figures(cu: ChapterUnits, page_images: dict[int, object], page_text: dict[int, str]) -> int:
    n = 0
    for u in cu.units:
        core = u.ext.setdefault("core", {})
        if u.kind != "figure" or not u.figure_ref or "figure_description" in core:
            continue
        if u.page_pdf not in page_images:
            raise ValueError(f"{u.unit_id}: нет скана страницы {u.page_pdf}")
        d = complete_json("core/figure_describe", {"caption": u.text, "page_text": page_text[u.page_pdf]},
                          schema=FigureDescription, tier="vision", images=[page_images[u.page_pdf]])
        text = d.description + (f"\nЛегенда: {d.legend}" if d.legend else "")
        core.update(figure_description=text, figure_description_by_model=True, figure_description_source="vision")
        if not d.readable:
            core["needs_scan"] = d.unreadable or "рисунок не читается на скане"
        n += 1
    return n
