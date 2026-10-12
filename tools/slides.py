"""
slides.py — Broadcast slide renderer for the CAC Masters lecture series.

Draws 1920x1080 lecture slides with Pillow: university-branded title cards,
bullet slides, case-study panels, two-column comparison, timelines, flow
diagrams and end cards. Rendered at 2x and downsampled for crisp typography.

House style
    Navy   #0A1F44      Gold  #B8912F
    Paper  #F7F4EC      Slate #22303F      Muted #64748B

Courtesy: Triune Biblical University Global Extension, USA.
"""

from __future__ import annotations

import glob
import os
import textwrap
from typing import List, Optional, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# Canvas + palette
# --------------------------------------------------------------------------

W, H = 1920, 1080
SCALE = 2  # supersample factor for antialiased text

NAVY = (10, 31, 68)
NAVY_D = (6, 20, 45)
GOLD = (184, 145, 47)
GOLD_L = (214, 180, 96)
PAPER = (247, 244, 236)
WHITE = (255, 255, 255)
SLATE = (34, 48, 63)
MUTED = (100, 116, 139)
RULE = (210, 200, 178)
OXBLOOD = (128, 42, 42)

MARGIN = 132
HEADER_H = 96
FOOTER_H = 88

UNIVERSITY = "TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA"
SERIES = "WHY YOU MUST STUDY INTERNATIONAL ENERGY AND NATURAL RESOURCES LAW AT ALL PROGRAMME LEVELS"
LECTURER = "Prof. Williams"
COURSE = "International Energy & Natural Resources Law · Global Perspectives"


# --------------------------------------------------------------------------
# Fonts
# --------------------------------------------------------------------------

_FONT_CACHE: dict = {}


def _font_dirs() -> List[str]:
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    dirs = [os.path.join(root, "assets", "fonts")]
    dirs += sorted(glob.glob(
        os.path.join(root, "venv", "lib", "python*", "site-packages",
                     "font_*", "files")))
    dirs += ["/usr/share/fonts/truetype/dejavu"]
    return [d for d in dirs if os.path.isdir(d)]


def _find(name: str) -> Optional[str]:
    for d in _font_dirs():
        for ext in (".ttf", ".otf"):
            p = os.path.join(d, name + ext)
            if os.path.exists(p):
                return p
    return None


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    """kind: serif | serif-bold | serif-it | sans | sans-bold | mono"""
    key = (kind, size * SCALE)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    table = {
        "serif": ["SourceSerifPro-Regular", "DejaVuSerif"],
        "serif-bold": ["SourceSerifPro-Bold", "DejaVuSerif-Bold"],
        "serif-it": ["SourceSerifPro-It", "SourceSerifPro-Regular", "DejaVuSerif"],
        "sans": ["SourceSansPro-Regular", "DejaVuSans"],
        "sans-bold": ["SourceSansPro-Bold", "DejaVuSans-Bold"],
        "sans-semibold": ["SourceSansPro-Semibold", "DejaVuSans-Bold"],
        "sans-light": ["SourceSansPro-Light", "DejaVuSans"],
        "mono": ["DejaVuSansMono"],
    }
    path = None
    for cand in table.get(kind, table["serif"]):
        path = _find(cand)
        if path:
            break
    if path is None:  # last resort
        path = _find("DejaVuSans") or ""
    f = ImageFont.truetype(path, size * SCALE)
    _FONT_CACHE[key] = f
    return f


def tw(draw, text: str, f) -> float:
    return draw.textlength(text, font=f) / SCALE


def wrap(draw, text: str, f, width: float) -> List[str]:
    out: List[str] = []
    for para in str(text).split("\n"):
        if not para.strip():
            out.append("")
            continue
        words, line = para.split(), ""
        for w in words:
            trial = (line + " " + w).strip()
            if tw(draw, trial, f) <= width or not line:
                line = trial
            else:
                out.append(line)
                line = w
        if line:
            out.append(line)
    return out


def _fit(draw, text: str, f, width: float, height: float, start: int = 46,
         floor: int = 24, weight: str = "serif-bold"):
    """Largest font size whose wrapped block fits width x height."""
    size = start
    while size > floor:
        fnt = font(weight, size)
        lines = wrap(draw, text, fnt, width)
        if len(lines) * size * 1.22 <= height:
            return fnt, lines, size
        size -= 2
    return font(weight, floor), wrap(draw, text, font(weight, floor), width), floor


# --------------------------------------------------------------------------
# Canvas helpers
# --------------------------------------------------------------------------


def canvas(bg=PAPER) -> Tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W * SCALE, H * SCALE), bg)
    return img, ImageDraw.Draw(img)


def finish(img: Image.Image) -> Image.Image:
    return img.resize((W, H), Image.LANCZOS)


def text(d, xy, s, f, fill=SLATE, anchor=None):
    d.text((xy[0] * SCALE, xy[1] * SCALE), s, font=f, fill=fill, anchor=anchor)


def rect(d, box, fill=None, outline=None, width=1, radius=0):
    b = [v * SCALE for v in box]
    if radius:
        d.rounded_rectangle(b, radius=radius * SCALE, fill=fill, outline=outline,
                            width=width * SCALE)
    else:
        d.rectangle(b, fill=fill, outline=outline, width=width * SCALE)


def line(d, xy, fill=RULE, width=1):
    d.line([v * SCALE for v in xy], fill=fill, width=width * SCALE)


def glow_rule(d, y, x0=MARGIN, x1=W - MARGIN, color=GOLD, h=4):
    rect(d, [x0, y, x1, y + h], fill=color)


# --------------------------------------------------------------------------
# Chrome
# --------------------------------------------------------------------------


def header(d, lecture_no: int, dark=False):
    fg = WHITE if dark else NAVY
    sub = GOLD_L if dark else GOLD
    rect(d, [0, 0, W, HEADER_H], fill=NAVY if not dark else NAVY_D)
    f = font("sans", 20)
    text(d, (MARGIN, 38), UNIVERSITY, f, fill=(228, 232, 240) if not dark else (200, 208, 220))
    lbl = f"LECTURE {lecture_no:02d}"
    text(d, (W - MARGIN, 38), lbl, font("sans-bold", 20), fill=sub, anchor="ra")
    # gold hairline under header
    rect(d, [0, HEADER_H, W, HEADER_H + 4], fill=GOLD)


def footer(d, idx: int, total: int, progress: float, dark=False):
    y0 = H - FOOTER_H
    rect(d, [0, y0, W, H], fill=NAVY if not dark else NAVY_D)
    rect(d, [0, y0, W, y0 + 4], fill=GOLD)
    f = font("sans", 21)
    text(d, (MARGIN, y0 + 34), f"{LECTURER}  ·  {COURSE}", f, fill=(206, 214, 226))
    text(d, (W - MARGIN, y0 + 34), f"{idx} / {total}", font("sans-bold", 21),
         fill=GOLD_L, anchor="ra")
    # progress bar
    bw = W - 2 * MARGIN
    by = y0 + 62
    rect(d, [MARGIN, by, MARGIN + bw, by + 5], fill=(46, 66, 96))
    rect(d, [MARGIN, by, MARGIN + max(2, bw * progress), by + 5], fill=GOLD)


def bg_paper(d, watermark: Optional[str] = None):
    """Subtle paper treatment with an optional large watermark."""
    rect(d, [0, 0, W, H], fill=PAPER)
    if watermark:
        f = font("serif-bold", 210)
        d.text((W * SCALE / 2, H * SCALE / 2), watermark[:2].upper(),
               font=f, fill=(240, 236, 226), anchor="mm")


def slide_title(d, title: str, kicker: Optional[str] = None, y0: int = HEADER_H + 56):
    y = y0
    if kicker:
        text(d, (MARGIN, y), kicker.upper(), font("sans-bold", 21), fill=GOLD)
        y += 44
    fnt, lines, size = _fit(d, title, font("serif-bold", 1), W - 2 * MARGIN, 150,
                            start=56, floor=32)
    for ln in lines:
        text(d, (MARGIN, y), ln, fnt, fill=NAVY)
        y += int(size * 1.24)
    glow_rule(d, y + 16, h=5)
    return y + 48


# --------------------------------------------------------------------------
# Slide types
# --------------------------------------------------------------------------


def title_card(lecture_no: int, title: str, subtitle: str, module: str,
               idx: int, total: int, progress: float) -> Image.Image:
    img, d = canvas(NAVY)
    # diagonal gold wash
    for i in range(120):
        a = int(26 * (1 - i / 120))
        d.line([(0, (H - i * 9) * SCALE), (W * SCALE, (H - i * 9 - 260) * SCALE)],
               fill=(GOLD[0], GOLD[1], GOLD[2]), width=1 * SCALE)
    rect(d, [0, 0, 420, H], fill=NAVY_D)

    text(d, (MARGIN, 150), UNIVERSITY, font("sans-bold", 23), fill=GOLD_L)
    glow_rule(d, 196, x1=MARGIN + 300, h=4)

    text(d, (MARGIN, 258), f"LECTURE {lecture_no:02d}", font("sans-bold", 30), fill=GOLD)
    text(d, (MARGIN, 306), module.upper(), font("sans", 24), fill=(170, 186, 208))

    fnt, lines, size = _fit(d, title, font("serif-bold", 1), W - 2 * MARGIN - 260, 320,
                            start=78, floor=44)
    y = 390
    for ln in lines:
        text(d, (MARGIN, y), ln, fnt, fill=WHITE)
        y += int(size * 1.16)

    if subtitle:
        sf, slines, ss = _fit(d, subtitle, font("serif-it", 1), W - 2 * MARGIN - 420, 190,
                              start=36, floor=24, weight="serif-it")
        yy = y + 30
        for ln in slines:
            text(d, (MARGIN, yy), ln, sf, fill=(196, 208, 226))
            yy += int(ss * 1.4)

    # series strip
    rect(d, [0, H - 250, W, H - 246], fill=GOLD)
    text(d, (MARGIN, H - 210), SERIES, font("sans-bold", 24), fill=(228, 216, 190))
    text(d, (MARGIN, H - 168), "GLOBAL PERSPECTIVES  ·  A TWENTY-PART LECTURE SERIES",
         font("sans", 22), fill=(150, 168, 194))
    text(d, (MARGIN, H - 118), f"Delivered by {LECTURER}", font("serif-bold", 28), fill=WHITE)
    return finish(img)


def section_card(lecture_no: int, num: str, title: str, idx: int, total: int,
                 progress: float) -> Image.Image:
    img, d = canvas(NAVY_D)
    rect(d, [0, 0, 8, H], fill=GOLD)
    text(d, (MARGIN + 40, 300), num, font("serif-bold", 180), fill=(38, 60, 96))
    fnt, lines, size = _fit(d, title, font("serif-bold", 1), W - 2 * MARGIN - 200, 340,
                            start=68, floor=38)
    y = 470
    for ln in lines:
        text(d, (MARGIN + 40, y), ln, fnt, fill=WHITE)
        y += int(size * 1.2)
    glow_rule(d, y + 28, x0=MARGIN + 40, x1=W - MARGIN, h=4)
    footer(d, idx, total, progress, dark=True)
    return finish(img)


def bullets(lecture_no: int, title: str, items: Sequence[str], idx: int, total: int,
            progress: float, kicker: Optional[str] = None,
            note: Optional[str] = None) -> Image.Image:
    img, d = canvas()
    bg_paper(d)
    header(d, lecture_no)
    y = slide_title(d, title, kicker)
    avail_h = H - FOOTER_H - 40 - y
    n = len(items)
    gap = 26
    size = 38
    while size > 22:
        f = font("serif", size)
        total_h = 0
        ok = True
        wrapped = []
        for it in items:
            ls = wrap(d, it, f, W - 2 * MARGIN - 56)
            wrapped.append(ls)
            total_h += len(ls) * size * 1.34 + gap
            if total_h > avail_h:
                ok = False
                break
        if ok:
            break
        size -= 2
    f = font("serif", size)
    for it in items:
        ls = wrap(d, it, f, W - 2 * MARGIN - 56)
        # gold marker
        rect(d, [MARGIN, y + size * 0.34, MARGIN + 14, y + size * 0.34 + 14], fill=GOLD)
        for j, ln in enumerate(ls):
            text(d, (MARGIN + 42, y), ln, f, fill=SLATE)
            y += int(size * 1.34)
        y += gap
    if note:
        rect(d, [MARGIN, H - FOOTER_H - 108, W - MARGIN, H - FOOTER_H - 40],
             fill=(238, 232, 216), radius=6)
        nf = font("serif-it", 27)
        text(d, (MARGIN + 28, H - FOOTER_H - 84), note, nf, fill=OXBLOOD)
    footer(d, idx, total, progress)
    return finish(img)


def two_col(lecture_no: int, title: str, left_h: str, left: Sequence[str],
            right_h: str, right: Sequence[str], idx: int, total: int,
            progress: float, kicker: Optional[str] = None) -> Image.Image:
    img, d = canvas()
    bg_paper(d)
    header(d, lecture_no)
    y = slide_title(d, title, kicker)
    colw = (W - 2 * MARGIN - 70) / 2
    gap = 20
    size = 33
    while size > 20:
        f = font("serif", size)
        lh = sum(len(wrap(d, i, f, colw - 46)) * size * 1.34 + gap for i in left)
        rh = sum(len(wrap(d, i, f, colw - 46)) * size * 1.34 + gap for i in right)
        if max(lh, rh) <= H - FOOTER_H - 60 - y:
            break
        size -= 2
    f = font("serif", size)
    for x, head, items in ((MARGIN, left_h, left), (MARGIN + colw + 70, right_h, right)):
        yy = y
        rect(d, [x, yy, x + colw, yy + 66], fill=NAVY, radius=4)
        hf, hl, hs = _fit(d, head, font("sans-bold", 1), colw - 44, 44, start=30, floor=20,
                          weight="sans-bold")
        text(d, (x + 22, yy + 33), head if len(hl) == 1 else hl[0], hf, fill=WHITE, anchor="lm")
        yy += 92
        for it in items:
            rect(d, [x, yy + size * 0.36, x + 10, yy + size * 0.36 + 10], fill=GOLD)
            for ln in wrap(d, it, f, colw - 46):
                text(d, (x + 30, yy), ln, f, fill=SLATE)
                yy += int(size * 1.34)
            yy += gap
    footer(d, idx, total, progress)
    return finish(img)


def objectives(lecture_no: int, title: str, items: Sequence[str], idx: int,
               total: int, progress: float, kicker="By the end of this lecture you should be able to") -> Image.Image:
    img, d = canvas()
    bg_paper(d)
    header(d, lecture_no)
    y = slide_title(d, title, "LEARNING OUTCOMES")
    text(d, (MARGIN, y), kicker, font("serif-it", 30), fill=MUTED)
    y += 74
    avail = H - FOOTER_H - 50 - y
    gap = 30
    size = 34
    while size > 22:
        f = font("serif", size)
        th = sum(len(wrap(d, i, f, W - 2 * MARGIN - 120)) * size * 1.34 + gap for i in items)
        if th <= avail:
            break
        size -= 2
    f = font("serif", size)
    for k, it in enumerate(items, 1):
        cy = y
        d.ellipse([MARGIN * SCALE, cy * SCALE, (MARGIN + 62) * SCALE, (cy + 62) * SCALE],
                  fill=NAVY)
        text(d, (MARGIN + 31, cy + 31), str(k), font("sans-bold", 30), fill=GOLD, anchor="mm")
        for j, ln in enumerate(wrap(d, it, f, W - 2 * MARGIN - 120)):
            text(d, (MARGIN + 92, cy + (0 if k else 0)), ln, f, fill=SLATE)
            cy += int(size * 1.34)
        y = cy + gap
    footer(d, idx, total, progress)
    return finish(img)


def quote_slide(lecture_no: int, quote: str, attribution: str, idx: int, total: int,
                progress: float, kicker: Optional[str] = None) -> Image.Image:
    img, d = canvas()
    bg_paper(d)
    header(d, lecture_no)
    if kicker:
        text(d, (MARGIN, HEADER_H + 54), kicker.upper(), font("sans-bold", 21), fill=GOLD)
    text(d, (MARGIN, HEADER_H + 110), "\u201c", font("serif-bold", 190), fill=GOLD_L)
    fnt, lines, size = _fit(d, quote, font("serif-it", 1), W - 2 * MARGIN - 120, 470,
                            start=52, floor=28, weight="serif-it")
    y = HEADER_H + 300
    for ln in lines:
        text(d, (MARGIN + 60, y), ln, fnt, fill=NAVY)
        y += int(size * 1.42)
    glow_rule(d, y + 30, x0=MARGIN + 60, x1=MARGIN + 460, h=4)
    text(d, (MARGIN + 60, y + 66), attribution, font("sans-bold", 30), fill=MUTED)
    footer(d, idx, total, progress)
    return finish(img)


def case_slide(lecture_no: int, title: str, case_name: str, body: str,
               holding: Optional[str], idx: int, total: int, progress: float,
               kicker="CASE STUDY") -> Image.Image:
    img, d = canvas()
    bg_paper(d)
    header(d, lecture_no)
    y = slide_title(d, title, kicker)
    # case panel
    top = y
    bot = H - FOOTER_H - 40
    rect(d, [MARGIN, top, W - MARGIN, bot], fill=(255, 253, 247), outline=RULE,
         width=2, radius=8)
    rect(d, [MARGIN, top, MARGIN + 10, bot], fill=OXBLOOD, radius=0)
    text(d, (MARGIN + 52, top + 40), case_name, font("sans-bold", 29), fill=OXBLOOD)
    line(d, [MARGIN + 52, top + 92, W - MARGIN - 52, top + 92], fill=RULE, width=2)
    fnt, lines, size = _fit(d, body, font("serif", 1), W - 2 * MARGIN - 110,
                            (bot - top) - (250 if holding else 130), start=31, floor=22)
    yy = top + 124
    for ln in lines:
        text(d, (MARGIN + 52, yy), ln, fnt, fill=SLATE)
        yy += int(size * 1.42)
    if holding:
        htop = bot - 168
        rect(d, [MARGIN + 52, htop, W - MARGIN - 52, bot - 34], fill=(239, 233, 214), radius=6)
        text(d, (MARGIN + 76, htop + 28), "HOLDING / SIGNIFICANCE",
             font("sans-bold", 21), fill=GOLD)
        hf, hl, hs = _fit(d, holding, font("serif-it", 1), W - 2 * MARGIN - 160, 78,
                          start=27, floor=20, weight="serif-it")
        z = htop + 68
        for ln in hl:
            text(d, (MARGIN + 76, z), ln, hf, fill=NAVY)
            z += int(hs * 1.4)
    footer(d, idx, total, progress)
    return finish(img)


def levels_slide(lecture_no: int, title: str, ug: Sequence[str], pg: Sequence[str],
                 idx: int, total: int, progress: float) -> Image.Image:
    return two_col(lecture_no, title, "UNDERGRADUATE LEVEL", list(ug),
                   "POSTGRADUATE LEVEL", list(pg), idx, total, progress,
                   kicker="WHY THIS LECTURE MATTERS AT EVERY PROGRAMME LEVEL")


def timeline_slide(lecture_no: int, title: str, events: Sequence[Tuple[str, str]],
                   idx: int, total: int, progress: float) -> Image.Image:
    img, d = canvas()
    bg_paper(d)
    header(d, lecture_no)
    y = slide_title(d, title, "CHRONOLOGY")
    axis_y = y + 300
    n = len(events)
    span = W - 2 * MARGIN
    step = span / (n - 1) if n > 1 else span
    line(d, [MARGIN, axis_y, W - MARGIN, axis_y], fill=GOLD, width=5)
    for i, (yr, ev) in enumerate(events):
        x = MARGIN + i * step
        d.ellipse([(x - 15) * SCALE, (axis_y - 15) * SCALE,
                   (x + 15) * SCALE, (axis_y + 15) * SCALE], fill=NAVY, outline=GOLD,
                  width=4 * SCALE)
        above = (i % 2 == 0)
        fy = axis_y - 70 if above else axis_y + 70
        text(d, (x, fy if above else fy - 14), yr, font("sans-bold", 32), fill=NAVY,
             anchor="mm" if above else "mm")
        lines = wrap(d, ev, font("serif", 25), step - 46)
        if above:
            yy = fy - 46 - (len(lines) - 1) * 34
        else:
            yy = fy + 30
        for ln in lines:
            text(d, (x, yy), ln, font("serif", 25), fill=SLATE, anchor="ma")
            yy += 34
    footer(d, idx, total, progress)
    return finish(img)


def diagram_slide(lecture_no: int, title: str, nodes: Sequence[str],
                  idx: int, total: int, progress: float,
                  kicker: Optional[str] = None, vertical: bool = False) -> Image.Image:
    img, d = canvas()
    bg_paper(d)
    header(d, lecture_no)
    y = slide_title(d, title, kicker)
    n = len(nodes)
    top, bot = y + 10, H - FOOTER_H - 40
    if vertical:
        bh = (bot - top - 26 * (n - 1)) / n
        for i, nd in enumerate(nodes):
            by = top + i * (bh + 26)
            rect(d, [MARGIN, by, W - MARGIN, by + bh], fill=(255, 253, 247),
                 outline=GOLD if i == n - 1 else RULE, width=3, radius=6)
            rect(d, [MARGIN, by, MARGIN + 8, by + bh], fill=NAVY if i < n - 1 else GOLD)
            fnt, lines, size = _fit(d, nd, font("serif", 1), W - 2 * MARGIN - 110, bh - 30,
                                    start=30, floor=19)
            zy = by + (bh - len(lines) * size * 1.3) / 2
            for ln in lines:
                text(d, (MARGIN + 52, zy), ln, fnt, fill=SLATE)
                zy += int(size * 1.3)
            if i < n - 1:
                cx = W / 2
                d.polygon([((cx - 16) * SCALE, (by + bh + 4) * SCALE),
                           ((cx + 16) * SCALE, (by + bh + 4) * SCALE),
                           (cx * SCALE, (by + bh + 24) * SCALE)], fill=GOLD)
    else:
        cols = 2 if n > 3 else n
        rows = (n + cols - 1) // cols
        cw = (W - 2 * MARGIN - 40 * (cols - 1)) / cols
        rh = (bot - top - 30 * (rows - 1)) / rows
        for i, nd in enumerate(nodes):
            r, c = divmod(i, cols)
            bx = MARGIN + c * (cw + 40)
            by = top + r * (rh + 30)
            rect(d, [bx, by, bx + cw, by + rh], fill=(255, 253, 247),
                 outline=GOLD if i == n - 1 else RULE, width=3, radius=6)
            rect(d, [bx, by, bx + cw, by + 7], fill=NAVY if i < n - 1 else GOLD)
            fnt, lines, size = _fit(d, nd, font("serif", 1), cw - 90, rh - 40,
                                    start=30, floor=18)
            zy = by + (rh - len(lines) * size * 1.3) / 2
            for ln in lines:
                text(d, (bx + 46, zy), ln, fnt, fill=SLATE)
                zy += int(size * 1.3)
    footer(d, idx, total, progress)
    return finish(img)


def end_card(lecture_no: int, next_title: str, idx: int, total: int,
             progress: float) -> Image.Image:
    img, d = canvas(NAVY)
    text(d, (W / 2, 250), "END OF LECTURE", font("sans-bold", 34), fill=GOLD, anchor="mm")
    text(d, (W / 2, 340), f"{LECTURER}", font("serif-bold", 62), fill=WHITE, anchor="mm")
    text(d, (W / 2, 412), COURSE, font("serif-it", 32), fill=(186, 200, 220), anchor="mm")
    glow_rule(d, 476, x0=W / 2 - 300, x1=W / 2 + 300, h=4)
    text(d, (W / 2, 560), "NEXT IN THIS SERIES", font("sans-bold", 24), fill=GOLD, anchor="mm")
    fnt, lines, size = _fit(d, next_title, font("serif-bold", 1), W - 400, 200,
                            start=46, floor=28)
    z = 620
    for ln in lines:
        text(d, (W / 2, z), ln, fnt, fill=WHITE, anchor="ma")
        z += int(size * 1.32)
    text(d, (W / 2, H - 190), UNIVERSITY, font("sans-bold", 25), fill=(160, 178, 204),
         anchor="mm")
    text(d, (W / 2, H - 146), "Global Perspectives  ·  All programme levels",
         font("sans", 24), fill=(140, 158, 184), anchor="mm")
    return finish(img)


def bumper(lecture_no: int, title: str) -> Image.Image:
    img, d = canvas(NAVY_D)
    for i in range(90):
        d.line([(0, (i * 12) * SCALE), (W * SCALE, (i * 12 - 300) * SCALE)],
               fill=(GOLD[0], GOLD[1], GOLD[2]), width=1 * SCALE)
    text(d, (W / 2, 430), UNIVERSITY, font("sans-bold", 30), fill=GOLD, anchor="mm")
    glow_rule(d, 486, x0=W / 2 - 260, x1=W / 2 + 260, h=3)
    text(d, (W / 2, 560), "A TWENTY-PART LECTURE SERIES", font("sans", 26),
         fill=(165, 182, 206), anchor="mm")
    text(d, (W / 2, 646), f"LECTURE {lecture_no:02d}", font("serif-bold", 96),
         fill=WHITE, anchor="mm")
    fnt, lines, size = _fit(d, title, font("serif-it", 1), W - 400, 150, start=38,
                            floor=24, weight="serif-it")
    z = 740
    for ln in lines:
        text(d, (W / 2, z), ln, fnt, fill=(200, 212, 230), anchor="ma")
        z += int(size * 1.35)
    return finish(img)


def summary_slide(lecture_no: int, title: str, points: Sequence[str],
                  takeaway: str, idx: int, total: int,
                  progress: float) -> Image.Image:
    img, d = canvas()
    bg_paper(d)
    header(d, lecture_no)
    y = slide_title(d, title, "SYNTHESIS")
    avail = H - FOOTER_H - 210 - y
    gap = 24
    size = 34
    while size > 22:
        f = font("serif", size)
        th = sum(len(wrap(d, i, f, W - 2 * MARGIN - 60)) * size * 1.34 + gap for i in points)
        if th <= avail:
            break
        size -= 2
    f = font("serif", size)
    for it in points:
        rect(d, [MARGIN, y + size * 0.34, MARGIN + 14, y + size * 0.34 + 14], fill=NAVY)
        for ln in wrap(d, it, f, W - 2 * MARGIN - 60):
            text(d, (MARGIN + 42, y), ln, f, fill=SLATE)
            y += int(size * 1.34)
        y += gap
    rect(d, [MARGIN, H - FOOTER_H - 176, W - MARGIN, H - FOOTER_H - 48],
         fill=NAVY, radius=8)
    text(d, (MARGIN + 40, H - FOOTER_H - 146), "THE ONE THING TO REMEMBER",
         font("sans-bold", 21), fill=GOLD)
    tf, tl, ts = _fit(d, takeaway, font("serif-it", 1), W - 2 * MARGIN - 100, 74,
                      start=30, floor=21, weight="serif-it")
    z = H - FOOTER_H - 114
    for ln in tl:
        text(d, (MARGIN + 40, z), ln, tf, fill=WHITE)
        z += int(ts * 1.36)
    footer(d, idx, total, progress)
    return finish(img)


# --------------------------------------------------------------------------
# Dispatch
# --------------------------------------------------------------------------


def render(slide: dict, ctx: dict) -> Image.Image:
    """Render one slide dict. ctx carries lecture_no, idx, total, progress."""
    t = slide.get("type", "bullets")
    ln, idx, total, prog = ctx["lecture_no"], ctx["idx"], ctx["total"], ctx["progress"]
    if t == "title":
        return title_card(ln, slide["title"], slide.get("subtitle", ""),
                          slide.get("module", ""), idx, total, prog)
    if t == "bumper":
        return bumper(ln, slide.get("title", ""))
    if t == "section":
        return section_card(ln, slide.get("num", ""), slide["title"], idx, total, prog)
    if t == "bullets":
        return bullets(ln, slide["title"], slide["items"], idx, total, prog,
                       slide.get("kicker"), slide.get("note"))
    if t == "two-col":
        return two_col(ln, slide["title"], slide["left_h"], slide["left"],
                       slide["right_h"], slide["right"], idx, total, prog,
                       slide.get("kicker"))
    if t == "objectives":
        return objectives(ln, slide["title"],
                          slide.get("items") or ctx.get("objectives", []),
                          idx, total, prog,
                          slide.get("kicker", "By the end of this lecture you should be able to"))
    if t == "quote":
        return quote_slide(ln, slide["quote"], slide["attribution"], idx, total, prog,
                           slide.get("kicker"))
    if t == "case":
        return case_slide(ln, slide["title"], slide["case"], slide["body"],
                          slide.get("holding"), idx, total, prog, slide.get("kicker"))
    if t == "levels":
        return levels_slide(ln, slide["title"], slide["ug"], slide["pg"], idx, total, prog)
    if t == "timeline":
        return timeline_slide(ln, slide["title"], slide["events"], idx, total, prog)
    if t == "diagram":
        return diagram_slide(ln, slide["title"], slide["nodes"], idx, total, prog,
                             slide.get("kicker"), slide.get("vertical", False))
    if t == "summary":
        return summary_slide(ln, slide["title"], slide["points"], slide["takeaway"],
                             idx, total, prog)
    if t == "end":
        return end_card(ln, slide.get("next", ""), idx, total, prog)
    raise ValueError(f"unknown slide type: {t}")
