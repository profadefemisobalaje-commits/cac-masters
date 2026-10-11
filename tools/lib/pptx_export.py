"""Export the same slide specs to a PowerPoint deck for live teaching.

Kept deliberately simple: the PNG is the truth, and each PPTX slide is the
rendered image behind a selectable-text box carrying the narration notes.
"""
from __future__ import annotations
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from . import slidekit as SK
from . import theme as T


def export(specs: list[dict], path: str, title: str = "", narration: bool = True):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    tmp = os.path.join(os.path.dirname(os.path.abspath(path)), "_pptx_tmp.png")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    for i, spec in enumerate(specs, 1):
        im = SK.render(spec)
        im.save(tmp, optimize=True)
        slide = prs.slides.add_slide(blank)
        slide.shapes.add_picture(tmp, 0, 0, width=prs.slide_width, height=prs.slide_height)
        notes = spec.get("narration") if narration else None
        if notes:
            tf = slide.notes_slide.notes_text_frame
            tf.text = notes
            for p in tf.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(12)
    if os.path.exists(tmp):
        os.remove(tmp)
    prs.save(path)
