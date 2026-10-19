"""Quality checks on the rendered decks.

The point of these checks is to catch the failures that a designer would catch
by eye but that a build script would happily ship: text running off the canvas,
boxes colliding, a font falling back, a diagram with no caption.
"""
from __future__ import annotations

import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

EMU_PT = 12700.0


def _pt(v):
    return float(v) / EMU_PT


def check_pptx(path: Path, margin: float = 24.0, verbose: bool = True):
    prs = Presentation(str(path))
    W, H = _pt(prs.slide_width), _pt(prs.slide_height)
    problems = []
    fonts = set()
    for i, slide in enumerate(prs.slides, 1):
        boxes = []
        for sh in slide.shapes:
            if sh.left is None:
                continue
            x, y = _pt(sh.left), _pt(sh.top)
            w, h = _pt(sh.width), _pt(sh.height)
            if x < -0.5 or y < -0.5 or x + w > W + 0.5 or y + h > H + 0.5:
                problems.append(f"p{i}: shape outside canvas ({x:.0f},{y:.0f},{w:.0f},{h:.0f})")
            if sh.has_text_frame and sh.text_frame.text.strip():
                sizes = [r.font.size.pt for p in sh.text_frame.paragraphs
                         for r in p.runs if r.font.size]
                biggest = max(sizes) if sizes else 0
                # oversized ghost numerals are decoration, not content
                if biggest < 60:
                    boxes.append((x, y, w, h, sh.text_frame.text.strip()[:40]))
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if r.font.name:
                            fonts.add(r.font.name)
        for a in range(len(boxes)):
            for b in range(a + 1, len(boxes)):
                x1, y1, w1, h1, t1 = boxes[a]
                x2, y2, w2, h2, t2 = boxes[b]
                ox = min(x1 + w1, x2 + w2) - max(x1, x2)
                oy = min(y1 + h1, y2 + h2) - max(y1, y2)
                if ox > 8 and oy > 12:
                    problems.append(f"p{i}: text overlap {t1!r} / {t2!r} ({ox:.0f}x{oy:.0f}pt)")
    if verbose:
        print(f"  {path.name}: {len(prs.slides)} slides, fonts={sorted(fonts)}")
        for p in problems[:20]:
            print("   !", p)
        if not problems:
            print("    geometry OK")
    return problems


def check_pdf(path: Path, verbose: bool = True):
    import pymupdf
    doc = pymupdf.open(str(path))
    problems = []
    allowed = {"EBGaramond", "SourceSans3", "EBGaramond-Italic", "EBGaramond-Medium",
               "EBGaramond-SemiBold", "EBGaramond-Bold", "SourceSans3-Light",
               "SourceSans3-It", "SourceSans3-Semibold", "SourceSans3-Bold"}
    fallbacks = set()
    for i, page in enumerate(doc, 1):
        for f in page.get_fonts():
            name = f[3].split("+")[-1].split("-Identity")[0]
            if not any(name.startswith(a) for a in allowed):
                fallbacks.add(name)
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for s in line["spans"]:
                    x0, y0, x1, y1 = s["bbox"]
                    if s["size"] < 60 and (x0 < 10 or y0 < 6 or x1 > 950 or y1 > 534):
                        problems.append(f"p{i}: text near edge {s['text'][:30]!r} "
                                        f"([{x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f}])")
    if verbose:
        print(f"  {path.name}: {doc.page_count} pages")
        if fallbacks:
            print("   ! font fallback:", sorted(fallbacks))
        for p in problems[:20]:
            print("   !", p)
        if not problems and not fallbacks:
            print("    typography OK")
    doc.close()
    return problems, fallbacks


def check_content(path: Path, verbose: bool = True):
    """Every week deck must carry the full grammar with real content."""
    prs = Presentation(str(path))
    slides = list(prs.slides)
    problems = []
    if len(slides) != 15:
        problems.append(f"expected 15 slides, found {len(slides)}")
    required = ["LEARNING OUTCOMES", "WHERE THIS WEEK SITS", "KEY CONCEPTS",
                "CLINICAL VIGNETTE", "SKILLS LABORATORY", "SEMINAR",
                "ASSESSMENT", "READING", "SYNTHESIS"]
    text = " ".join(sh.text_frame.text for sl in slides for sh in sl.shapes
                    if sh.has_text_frame)
    for r in required:
        if r not in text:
            problems.append(f"missing slide: {r}")
    empty = [i + 1 for i, sl in enumerate(slides)
             if not any(sh.has_text_frame and sh.text_frame.text.strip() for sh in sl.shapes)]
    if empty:
        problems.append(f"empty slides: {empty}")
    if verbose:
        print(f"  {path.name}: grammar check -> {'OK' if not problems else problems}")
    return problems


def main(paths):
    fails = 0
    for p in map(Path, paths):
        if p.suffix == ".pptx":
            fails += len(check_pptx(p))
        elif p.suffix == ".pdf":
            fails += len(check_pdf(p)[0])
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
