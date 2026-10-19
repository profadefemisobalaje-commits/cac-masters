"""Render the same layout primitives to a vector PDF with Typst.

Pages are 960 x 540 pt, the exact geometry of the PPTX canvas, so the PDF is a
true sibling of the deck: same grid, same line breaks, same figures, but with
embedded fonts and vector diagrams suitable for print.
"""
from __future__ import annotations

import re
from pathlib import Path

import typst

from . import layout as L
from . import theme

BUILD = theme.ROOT / "decks" / "build"


def _q(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _col(h: str, alpha: float = 1.0) -> str:
    base = f'rgb("{h}")'
    if alpha >= 0.999:
        return base
    return f"{base}.transparentize({(1 - alpha) * 100:.2f}%)"


def _face(family: str, weight: str, italic: bool):
    """Typst (family, weight, style).

    Typst resolves the typographic family (name ID 16), so the sub-family
    names used by PowerPoint ("EB Garamond Medium") must become a base family
    plus a weight token here.
    """
    style = '"italic"' if italic else '"normal"'
    if family == "display":
        if weight == "bold":
            return '"EB Garamond"', '"bold"', style
        if weight == "semibold":
            return '"EB Garamond"', '"semibold"', style
        if weight == "medium":
            return '"EB Garamond"', '"medium"', style
        return '"EB Garamond"', '"regular"', style
    if weight == "light":
        if italic:
            return '"Source Sans 3"', '"regular"', style
        return '"Source Sans 3"', '"light"', style
    if weight == "semibold":
        return '"Source Sans 3"', '"semibold"', style
    if weight == "bold":
        return '"Source Sans 3"', '"bold"', style
    return '"Source Sans 3"', '"regular"', style


def _img(p: str) -> str:
    p = Path(p).resolve()
    try:
        rel = p.relative_to(theme.ROOT)
    except ValueError:
        rel = p
    return "/" + str(rel).replace("\\", "/")


def _ops_to_typst(s: L.Slide, page_fill: str, texture: str | None) -> str:
    out: list[str] = []
    out.append(f'#page(margin: 0pt, fill: {_col(page_fill)})[')
    if texture and Path(texture).exists():
        out.append(f'  #place(dx: 0pt, dy: 0pt, image({_q(_img(texture))}, width: 960pt, height: 540pt))')

    # ground: rectangles, ellipses, rules
    for op in s.ops:
        if op.kind == "rect":
            stroke = f'(paint: {_col(op.line)}, thickness: {op.lw}pt)' if op.line else "none"
            radius = f"radius: {op.radius}pt, " if op.radius else ""
            out.append(
                f'  #place(dx: {op.x:.2f}pt, dy: {op.y:.2f}pt, '
                f'rect(width: {op.w:.2f}pt, height: {op.h:.2f}pt, {radius}'
                f'fill: {_col(op.fill) if op.fill else "none"}, stroke: {stroke}))'
            )
        elif op.kind == "ellipse":
            stroke = f'(paint: {_col(op.line)}, thickness: {op.lw}pt)' if op.line else "none"
            out.append(
                f'  #place(dx: {op.x:.2f}pt, dy: {op.y:.2f}pt, '
                f'ellipse(width: {op.w:.2f}pt, height: {op.h:.2f}pt, '
                f'fill: {_col(op.fill) if op.fill else "none"}, stroke: {stroke}))'
            )
        elif op.kind == "rule":
            if abs(op.y2 - op.y1) < 0.01:
                x, y = min(op.x1, op.x2), op.y1 - op.lw / 2
                w, h = abs(op.x2 - op.x1), max(op.lw, 0.35)
            elif abs(op.x2 - op.x1) < 0.01:
                x, y = op.x1 - op.lw / 2, min(op.y1, op.y2)
                w, h = max(op.lw, 0.35), abs(op.y2 - op.y1)
            else:
                continue
            out.append(
                f'  #place(dx: {x:.2f}pt, dy: {y:.2f}pt, '
                f'rect(width: {w:.2f}pt, height: {h:.2f}pt, fill: {_col(op.color)}, stroke: none))'
            )

    # images
    for op in s.ops:
        if op.kind == "image":
            out.append(
                f'  #place(dx: {op.x:.2f}pt, dy: {op.y:.2f}pt, '
                f'image({_q(_img(op.path))}, width: {op.w:.2f}pt, height: {op.h:.2f}pt))'
            )

    # text
    for op in s.ops:
        if op.kind != "text":
            continue
        fam, wt, style = _face(op.family, op.weight, op.italic)
        for i, line in enumerate(op.lines):
            x = op.line_x(i)
            y = op.y + i * op.line_height + (op.line_height - op.size) * 0.30
            out.append(
                f'  #place(dx: {x:.2f}pt, dy: {y:.2f}pt, text(font: {fam}, '
                f'size: {op.size:.2f}pt, fill: {_col(op.color, op.alpha)}, '
                f'tracking: {op.tracking:.2f}pt, weight: {wt}, style: {style}, lang: "en", '
                f'{_q(line)}))'
            )
    out.append("]")
    return "\n".join(out)


def render(slides: list[L.Slide], path: Path, title: str, author: str,
           subject: str = "Lecture deck") -> Path:
    BUILD.mkdir(parents=True, exist_ok=True)
    body = "\n\n".join(_ops_to_typst(s, s.bg, s.texture) for s in slides)
    src = f"""#set page(width: 960pt, height: 540pt, margin: 0pt)
#set document(title: {_q(title)}, author: {_q(author)})
#set text(lang: "en")
{body}
"""
    typ_path = BUILD / (path.stem + ".typ")
    typ_path.write_text(src, encoding="utf-8")
    pdf = typst.compile(str(typ_path), font_paths=[str(theme.FONTS)],
                        root=str(theme.ROOT))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(pdf)
    return path


def page_count(pdf_path: Path) -> int:
    import pymupdf
    with pymupdf.open(pdf_path) as doc:
        return doc.page_count
