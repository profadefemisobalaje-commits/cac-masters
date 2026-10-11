"""Slide layout engine: turns a slide spec dict into a 1920x1080 PIL image.

Layouts: title, section, outline, objectives, bullets, twocol, definition,
quote, table, casestudy, takeaways, reading, stats, process, end.
"""
from __future__ import annotations
import numpy as np
from PIL import Image, ImageDraw
from . import theme as T


# ------------------------------------------------------------------ helpers
def gradient(w: int, h: int, c0: tuple, c1: tuple, angle: str = "diag") -> Image.Image:
    if angle == "h":
        t = np.linspace(0, 1, w)[None, :].repeat(h, 0)
    elif angle == "v":
        t = np.linspace(0, 1, h)[:, None].repeat(w, 1)
    else:
        tx = np.linspace(0, 1, w)[None, :].repeat(h, 0)
        ty = np.linspace(0, 1, h)[:, None].repeat(w, 1)
        t = (tx + ty) / 2
    arr = np.zeros((h, w, 3), np.uint8)
    for i in range(3):
        arr[:, :, i] = (c0[i] + (c1[i] - c0[i]) * t).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def wrap(text: str, fnt, max_w: float) -> list[str]:
    """Word-wrap honouring explicit newlines."""
    out: list[str] = []
    for para in str(text).split("\n"):
        if not para.strip():
            out.append("")
            continue
        cur = ""
        for word in para.split():
            trial = f"{cur} {word}".strip()
            if fnt.getlength(trial) <= max_w or not cur:
                cur = trial
            else:
                out.append(cur)
                cur = word
        if cur:
            out.append(cur)
    return out


def draw_lines(d: ImageDraw.ImageDraw, x, y, lines, fnt, fill, leading, max_lines=None):
    lh = int(fnt.size * leading)
    for i, ln in enumerate(lines if max_lines is None else lines[:max_lines]):
        d.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh


def para(d, x, y, w, text, fnt, fill, leading=T.LINE, max_lines=None):
    lines = wrap(text, fnt, w)
    return draw_lines(d, x, y, lines, fnt, fill, leading, max_lines)


def block_height(d, w, text, fnt, leading=T.LINE) -> int:
    return len(wrap(text, fnt, w)) * int(fnt.size * leading)


def pill(d, x, y, label, fnt, fg, bg, pad_x=22, pad_y=10, radius=None):
    tw = fnt.getlength(label)
    th = fnt.size
    bw, bh = tw + pad_x * 2, th + pad_y * 2
    r = bh // 2 if radius is None else radius
    d.rounded_rectangle([x, y, x + bw, y + bh], radius=r, fill=bg)
    d.text((x + pad_x, y + pad_y - 2), label, font=fnt, fill=fg)
    return bw, bh


# ------------------------------------------------------------------ chrome
def header(d, eyebrow: str, title: str, title_size=None, sub=None):
    """Top bar + title. Returns the y coordinate where content may start."""
    d.rectangle([0, 0, T.W, 10], fill=T.ACCENT)
    f_eb = T.font("med", T.S["eyebrow"])
    d.text((T.MARGIN_X, 62), eyebrow.upper(), font=f_eb, fill=T.ACCENT_DK)
    # eyebrow letter tracking
    y = 108
    ts = title_size or T.S["title"]
    f_t = T.font("bold", ts)
    lines = wrap(title, f_t, T.W - 2 * T.MARGIN_X)
    if len(lines) > 2:
        ts = int(ts * 0.82)
        f_t = T.font("bold", ts)
        lines = wrap(title, f_t, T.W - 2 * T.MARGIN_X)
    y = draw_lines(d, T.MARGIN_X, y, lines, f_t, T.INK, 1.16)
    y += 16
    if sub:
        f_s = T.font("reg", T.S["subtitle"])
        y = para(d, T.MARGIN_X, y, T.W - 2 * T.MARGIN_X - 120, sub, f_s, T.TEXT_MUTED, 1.34)
        y += 10
    d.rectangle([T.MARGIN_X, y + 8, T.MARGIN_X + 96, y + 16], fill=T.ACCENT)
    return y + 62


def footer(d, left: str, right: str):
    y = T.H - 58
    d.rectangle([T.MARGIN_X, y - 20, T.W - T.MARGIN_X, y - 19], fill=T.RULE)
    f = T.font("reg", T.S["footer"])
    d.text((T.MARGIN_X, y), left, font=f, fill=T.TEXT_MUTED)
    d.text((T.W - T.MARGIN_X - f.getlength(right), y), right, font=f, fill=T.TEXT_MUTED)


def bg(d, alt=False):
    d.rectangle([0, 0, T.W, T.H], fill=T.PAPER_ALT if alt else T.PAPER)


# ------------------------------------------------------------------ layouts
def lay_title(d, s):
    img = gradient(T.W, T.H, T.INK, T.INK_DEEP, "diag")
    d._image.paste(img, (0, 0))
    d.rectangle([0, 0, T.W, 12], fill=T.ACCENT)
    # decorative panels
    x = T.MARGIN_X
    f_inst = T.font("med", 30)
    inst = str(s.get("institution", "")).upper()
    # long institution names shrink rather than overrun the canvas
    while inst and f_inst.getlength(inst) > T.W - 2 * x and f_inst.size > 18:
        f_inst = T.font("med", f_inst.size - 2)
    if inst:
        d.text((x, 150 + (30 - f_inst.size) / 2), inst, font=f_inst, fill=T.ACCENT)
    f_code = T.font("bold", 34)
    d.text((x, 210), s.get("course", ""), font=f_code, fill=T.GOLD)
    f_t = T.font("bold", T.S["title_xl"])
    lines = wrap(s.get("title", ""), f_t, T.W - 2 * x)
    if len(lines) > 3:
        f_t = T.font("bold", 66)
        lines = wrap(s.get("title", ""), f_t, T.W - 2 * x)
    y = draw_lines(d, x, 300, lines, f_t, T.TEXT_LIGHT, 1.12)
    y += 26
    d.rectangle([x, y, x + 140, y + 8], fill=T.ACCENT)
    y += 44
    if s.get("subtitle"):
        f_s = T.font("reg", 36)
        y = para(d, x, y, T.W - 2 * x - 80, s["subtitle"], f_s, (170, 194, 214), 1.36)
    y += 30
    meta = [m for m in [s.get("week"), s.get("lecturer"), s.get("duration")] if m]
    if meta:
        f_m = T.font("reg", 26)
        d.text((x, y), "   |   ".join(meta), font=f_m, fill=(140, 168, 192))
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_section(d, s):
    img = gradient(T.W, T.H, T.INK_DEEP, T.INK, "h")
    d._image.paste(img, (0, 0))
    d.rectangle([0, 0, 16, T.H], fill=T.ACCENT)
    x = T.MARGIN_X + 56
    # oversized numeral as a watermark on the right, never colliding with text
    n = s.get("number")
    wm_w = 0
    if n:
        f_n = T.font("bold", 340)
        lbl = str(n)
        wm_w = f_n.getlength(lbl) + 120
        d.text((T.W - T.MARGIN_X - f_n.getlength(lbl), 250), lbl, font=f_n, fill=(30, 66, 96))
    f_eb = T.font("med", 28)
    d.text((x, 372), s.get("eyebrow", "SECTION").upper(), font=f_eb, fill=T.GOLD)
    f_t = T.font("bold", T.S["title_l"])
    tw = T.W - x - T.MARGIN_X - wm_w
    lines = wrap(s.get("title", ""), f_t, tw)
    y = draw_lines(d, x, 430, lines, f_t, T.TEXT_LIGHT, 1.16)
    y += 30
    d.rectangle([x, y, x + 120, y + 7], fill=T.ACCENT)
    if s.get("subtitle"):
        y += 42
        para(d, x, y, tw, s["subtitle"], T.font("reg", 32), (168, 192, 212), 1.4)
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def _numbered(d, s, marker="num"):
    bg(d, s.get("alt", False))
    y = header(d, s.get("eyebrow", ""), s["title"])
    items = s["items"]
    n = len(items)
    avail = T.CONTENT_BOTTOM - y
    f = T.font("reg", T.S["bullet"])
    f_n = T.font("bold", 30)
    gap = 22 if n <= 6 else 14
    # cap the row pitch so short lists do not stretch across the full slide
    rowh = min(136, (avail - gap * (n - 1)) / n)
    block = rowh * n + gap * (n - 1)
    y = y + max(0, (avail - block) / 2) if block < avail else y
    for i, it in enumerate(items):
        ty = int(y + i * (rowh + gap))
        cy = ty + 6
        if marker == "num":
            d.rounded_rectangle([T.MARGIN_X, cy - 6, T.MARGIN_X + 56, cy + 52], radius=12, fill=T.INK)
            lbl = f"{i+1:02d}"
            d.text((T.MARGIN_X + (56 - f_n.getlength(lbl)) / 2, cy + 8), lbl, font=f_n, fill=T.WHITE)
        else:
            d.rounded_rectangle([T.MARGIN_X + 10, cy + 10, T.MARGIN_X + 30, cy + 30], radius=5,
                                fill=None, outline=T.ACCENT, width=4)
        tx = T.MARGIN_X + 84
        tw = T.W - tx - T.MARGIN_X
        lines = wrap(it, f, tw)
        maxl = max(1, int((rowh + gap - 6) // int(f.size * T.LINE)))
        draw_lines(d, tx, ty, lines, f, T.TEXT, T.LINE, max_lines=maxl)
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_outline(d, s):
    _numbered(d, s, "num")


def lay_objectives(d, s):
    _numbered(d, s, "tick")


def lay_bullets(d, s):
    bg(d, s.get("alt", False))
    y = header(d, s.get("eyebrow", ""), s["title"], sub=s.get("subtitle"))
    f = T.font("reg", T.S["bullet"])
    fb = T.font("bold", T.S["bullet_s"])
    f2 = T.font("reg", T.S["body_s"])
    items = s["bullets"]
    for it in items:
        if isinstance(it, str):
            it = {"t": it, "lvl": 0}
        lvl = it.get("lvl", 0)
        fnt = f if lvl == 0 else f2
        strong = it.get("strong", False)
        if strong:
            fnt = fb
        indent = T.MARGIN_X + (T.BULLET_INDENT if lvl == 0 else T.BULLET_LVL2_INDENT)
        tw = T.W - indent - T.MARGIN_X
        lines = wrap(it["t"], fnt, tw)
        need = len(lines) * int(fnt.size * T.LINE) + (18 if lvl == 0 else 10)
        if y + need > T.CONTENT_BOTTOM:
            break
        if lvl == 0:
            d.rounded_rectangle([T.MARGIN_X, y + 13, T.MARGIN_X + 14, y + 27], radius=4, fill=T.ACCENT)
        else:
            d.rectangle([T.MARGIN_X + 62, y + 18, T.MARGIN_X + 72, y + 24], fill=T.TEXT_MUTED)
        y = draw_lines(d, indent, y, lines, fnt, T.TEXT if lvl == 0 else T.TEXT_MUTED, T.LINE)
        y += 18 if lvl == 0 else 10
        if it.get("sub"):
            fs = T.font("reg", T.S["caption"] + 2)
            y = para(d, indent, y - 4, tw, it["sub"], fs, T.TEXT_MUTED, 1.36) + 12
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_twocol(d, s):
    bg(d, s.get("alt", False))
    y = header(d, s.get("eyebrow", ""), s["title"])
    gapx = 56
    cw = (T.W - 2 * T.MARGIN_X - gapx) / 2
    d.rectangle([T.MARGIN_X + cw + gapx / 2 - 1, y, T.MARGIN_X + cw + gapx / 2, T.CONTENT_BOTTOM], fill=T.RULE)
    for ci, col in enumerate(s["columns"][:2]):
        cx = T.MARGIN_X + ci * (cw + gapx)
        cy = y
        fh = T.font("bold", 34)
        d.text((cx, cy), col["h"], font=fh, fill=T.ACCENT_DK)
        cy += 58
        d.rectangle([cx, cy - 18, cx + 64, cy - 14], fill=T.ACCENT)
        cy += 22
        f = T.font("reg", T.S["body_s"])
        for it in col["items"]:
            if isinstance(it, str):
                it = {"t": it}
            lines = wrap(it["t"], f, cw - 34)
            if cy + len(lines) * int(f.size * T.LINE) > T.CONTENT_BOTTOM:
                break
            d.rounded_rectangle([cx, cy + 12, cx + 10, cy + 22], radius=3, fill=T.ACCENT)
            cy = draw_lines(d, cx + 30, cy, lines, f, T.TEXT, T.LINE) + 16
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_definition(d, s):
    bg(d, s.get("alt", False))
    y = header(d, s.get("eyebrow", "KEY CONCEPT"), s["title"], sub=s.get("subtitle"))
    box_h = T.CONTENT_BOTTOM - y - (0 if not s.get("footnote") else 96)
    d.rounded_rectangle([T.MARGIN_X, y, T.W - T.MARGIN_X, y + box_h], radius=20, fill=T.PAPER)
    d.rounded_rectangle([T.MARGIN_X, y, T.W - T.MARGIN_X, y + box_h], radius=20, outline=T.RULE, width=2)
    d.rectangle([T.MARGIN_X, y, T.MARGIN_X + 12, y + box_h], fill=T.ACCENT)
    tx = T.MARGIN_X + 64
    tw = T.W - tx - T.MARGIN_X - 48
    ty = y + 52
    f_term = T.font("bold", 46)
    ty = draw_lines(d, tx, ty, wrap(s["term"], f_term, tw), f_term, T.INK, 1.2) + 26
    f = T.font("reg", T.S["body"] + 2)
    ty = para(d, tx, ty, tw, s["body"], f, T.TEXT, 1.5)
    if s.get("source"):
        ty += 22
        fs = T.font("italic", T.S["caption"])
        para(d, tx, ty, tw, s["source"], fs, T.TEXT_MUTED, 1.3)
    if s.get("footnote"):
        fnote = T.font("reg", T.S["body_s"])
        para(d, T.MARGIN_X, y + box_h + 34, T.W - 2 * T.MARGIN_X, s["footnote"], fnote, T.TEXT_MUTED, 1.36)
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_quote(d, s):
    bg(d, True)
    y = 96
    d.rectangle([0, 0, T.W, 10], fill=T.ACCENT)
    if s.get("eyebrow"):
        d.text((T.MARGIN_X, y), s["eyebrow"].upper(), font=T.font("med", T.S["eyebrow"]), fill=T.ACCENT_DK)
        y += 66
    if s.get("title"):
        f_t = T.font("bold", T.S["title_s"])
        y = draw_lines(d, T.MARGIN_X, y, wrap(s["title"], f_t, T.W - 2 * T.MARGIN_X), f_t, T.INK, 1.16) + 20
    # quote block sits in the vertical middle of the remaining space
    f_q = T.font("light", T.S["quote"])
    tw = T.W - 2 * T.MARGIN_X - 120
    lines = wrap(s["quote"], f_q, tw)
    lh = int(f_q.size * 1.45)
    block_h = len(lines) * lh
    f_a = T.font("med", 28)
    attr_h = 40 if s.get("attribution") else 0
    top = y + max(60, (T.CONTENT_BOTTOM - y - block_h - attr_h) / 2)
    draw_lines(d, T.MARGIN_X + 90, top, lines, f_q, T.INK, 1.45)
    d.rectangle([T.MARGIN_X, top, T.MARGIN_X + 8, top + block_h], fill=T.GOLD)
    if s.get("attribution"):
        d.text((T.MARGIN_X + 90, top + block_h + 22), "— " + s["attribution"], font=f_a, fill=T.ACCENT_DK)
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_table(d, s):
    bg(d, s.get("alt", False))
    y = header(d, s.get("eyebrow", ""), s["title"], sub=s.get("subtitle"))
    rows = s["rows"]
    cols = s["columns"]
    tw = T.W - 2 * T.MARGIN_X
    ncol = len(cols)
    widths = s.get("widths") or [1 / ncol] * ncol
    xs, acc = [], T.MARGIN_X
    for wf in widths:
        xs.append(acc)
        acc += tw * wf
    fh = T.font("bold", 27)
    hr = y + 62
    d.rectangle([T.MARGIN_X, y, T.W - T.MARGIN_X, hr], fill=T.INK)
    for i, c in enumerate(cols):
        d.text((xs[i] + 20, y + 16), c, font=fh, fill=T.WHITE)
    f = T.font("reg", 26)
    # natural row height, capped, then the whole table is centred in the content area
    lh = int(26 * 1.3)
    need = max(len(wrap(c, f, tw * widths[ci] - 34)) for row in rows for ci, c in enumerate(row[:ncol]))
    rowh = min(max(58, need * lh + 30), (T.CONTENT_BOTTOM - hr) / max(1, len(rows)))
    table_h = rowh * len(rows)
    hr = max(hr, hr + ((T.CONTENT_BOTTOM - hr) - table_h) / 2)
    for ri, row in enumerate(rows):
        ry = hr + ri * rowh
        if ri % 2 == 0:
            d.rectangle([T.MARGIN_X, ry, T.W - T.MARGIN_X, ry + rowh], fill=T.PAPER_ALT)
        d.rectangle([T.MARGIN_X, ry, T.W - T.MARGIN_X, ry + 1], fill=T.RULE)
        for ci, cell in enumerate(row[:ncol]):
            cw = tw * widths[ci] - 34
            ff = T.font("med", 26) if ci == 0 else f
            lines = wrap(cell, ff, cw)
            maxl = max(1, int(rowh // int(ff.size * 1.3)))
            draw_lines(d, xs[ci] + 20, ry + (rowh - min(len(lines), maxl) * lh) / 2,
                       lines, ff, T.TEXT, 1.3, max_lines=maxl)
    d.rectangle([T.MARGIN_X, hr + len(rows) * rowh, T.W - T.MARGIN_X, hr + len(rows) * rowh + 2], fill=T.INK)
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_casestudy(d, s):
    bg(d, s.get("alt", False))
    y = header(d, s.get("eyebrow", "CASE VIGNETTE"), s["title"])
    box_h = T.CONTENT_BOTTOM - y
    d.rounded_rectangle([T.MARGIN_X, y, T.W - T.MARGIN_X, y + box_h], radius=18, fill=(252, 248, 238))
    d.rounded_rectangle([T.MARGIN_X, y, T.W - T.MARGIN_X, y + box_h], radius=18, outline=(238, 222, 188), width=2)
    d.rectangle([T.MARGIN_X, y, T.MARGIN_X + 12, y + box_h], fill=T.GOLD)
    tx, tw = T.MARGIN_X + 56, T.W - 2 * T.MARGIN_X - 104
    ty = y + 40
    f = T.font("reg", T.S["body"])
    for p in s["paragraphs"]:
        ty = para(d, tx, ty, tw, p, f, T.TEXT, 1.46) + 20
    if s.get("questions"):
        ty += 8
        d.rectangle([tx, ty, tx + 70, ty + 5], fill=T.GOLD)
        ty += 26
        fq = T.font("med", T.S["body_s"])
        for q in s["questions"]:
            lines = wrap(q, fq, tw - 34)
            d.rounded_rectangle([tx, ty + 12, tx + 9, ty + 21], radius=3, fill=T.GOLD)
            ty = draw_lines(d, tx + 30, ty, lines, fq, T.ACCENT_DK, 1.34) + 12
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_takeaways(d, s):
    bg(d, True)
    y = header(d, s.get("eyebrow", "KEY TAKEAWAYS"), s["title"])
    items = s["items"]
    n = len(items)
    gap = 24
    rowh = (T.CONTENT_BOTTOM - y - gap * (n - 1)) / n
    f = T.font("reg", T.S["body"])
    for i, it in enumerate(items):
        ty = int(y + i * (rowh + gap))
        d.rounded_rectangle([T.MARGIN_X, ty, T.W - T.MARGIN_X, ty + rowh], radius=14, fill=T.PAPER)
        d.rounded_rectangle([T.MARGIN_X, ty, T.W - T.MARGIN_X, ty + rowh], radius=14, outline=T.RULE, width=2)
        d.rounded_rectangle([T.MARGIN_X, ty, T.MARGIN_X + 8, ty + rowh], radius=4, fill=T.ACCENT)
        f_n = T.font("bold", 34)
        d.text((T.MARGIN_X + 40, ty + (rowh - 34) / 2 - 2), f"{i+1}", font=f_n, fill=T.ACCENT)
        lines = wrap(it, f, T.W - 2 * T.MARGIN_X - 200)
        maxl = max(1, int(rowh // int(f.size * T.LINE)))
        draw_lines(d, T.MARGIN_X + 140, ty + (rowh - min(len(lines), maxl) * int(f.size * T.LINE)) / 2,
                   lines, f, T.TEXT, T.LINE, max_lines=maxl)
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_reading(d, s):
    bg(d, s.get("alt", False))
    y = header(d, s.get("eyebrow", "REQUIRED READING"), s["title"])
    f = T.font("reg", T.S["body_s"])
    fi = T.font("italic", T.S["body_s"])
    for it in s["items"]:
        if isinstance(it, str):
            it = {"t": it}
        fnt = fi if it.get("italic") else f
        lines = wrap(it["t"], fnt, T.W - 2 * T.MARGIN_X - 60)
        if y + len(lines) * int(fnt.size * 1.42) > T.CONTENT_BOTTOM:
            break
        d.rounded_rectangle([T.MARGIN_X, y + 13, T.MARGIN_X + 12, y + 25], radius=3, fill=T.ACCENT)
        y = draw_lines(d, T.MARGIN_X + 44, y, lines, fnt, T.TEXT, 1.42) + 26
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_stats(d, s):
    bg(d, s.get("alt", False))
    y = header(d, s.get("eyebrow", ""), s["title"], sub=s.get("subtitle"))
    stats = s["stats"][:4]
    n = len(stats)
    gapx = 42
    cw = (T.W - 2 * T.MARGIN_X - gapx * (n - 1)) / n
    for i, st in enumerate(stats):
        cx = T.MARGIN_X + i * (cw + gapx)
        d.rounded_rectangle([cx, y, cx + cw, y + 300], radius=18, fill=T.PAPER)
        d.rounded_rectangle([cx, y, cx + cw, y + 300], radius=18, outline=T.RULE, width=2)
        d.rectangle([cx, y, cx + cw, y + 8], fill=T.ACCENT if i % 2 == 0 else T.GOLD)
        f_v = T.font("bold", T.S["stat"] if len(st["v"]) <= 5 else 64)
        d.text((cx + (cw - f_v.getlength(st["v"])) / 2, y + 66), st["v"], font=f_v, fill=T.INK)
        f_l = T.font("med", 24)
        lines = wrap(st["l"], f_l, cw - 40)
        ly = y + 200
        for j, ln in enumerate(lines[:3]):
            d.text((cx + (cw - f_l.getlength(ln)) / 2, ly + j * 32), ln, font=f_l, fill=T.TEXT_MUTED)
    if s.get("note"):
        para(d, T.MARGIN_X, y + 340, T.W - 2 * T.MARGIN_X, s["note"], T.font("reg", T.S["body_s"]), T.TEXT, 1.44)
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_process(d, s):
    bg(d, s.get("alt", False))
    y = header(d, s.get("eyebrow", ""), s["title"], sub=s.get("subtitle"))
    steps = s["steps"]
    n = len(steps)
    gapx = 30
    cw = (T.W - 2 * T.MARGIN_X - gapx * (n - 1)) / n
    # measure the tallest card, then centre the whole band in the content area
    r = min(50, cw * 0.28)
    fs = int(r * 0.86)
    f_h = T.font("med", 29)
    f_b = T.font("reg", 25)
    head_lines = max(len(wrap(st["h"], f_h, cw - 20)) for st in steps)
    body_lines = max(len(wrap(st["b"], f_b, cw - 24)) for st in steps)
    band = 2 * r + 40 + head_lines * 38 + 16 + body_lines * 33
    top = y + max(40, (T.CONTENT_BOTTOM - y - band) / 2)
    d.rectangle([T.MARGIN_X + cw / 2, top + r - 2, T.W - T.MARGIN_X - cw / 2, top + r + 4], fill=T.RULE)
    for i, st in enumerate(steps):
        cx = T.MARGIN_X + i * (cw + gapx)
        d.ellipse([cx + cw / 2 - r, top, cx + cw / 2 + r, top + 2 * r],
                  fill=T.ACCENT if i % 2 == 0 else T.INK)
        f_n = T.font("bold", fs)
        lbl = str(i + 1)
        d.text((cx + cw / 2 - f_n.getlength(lbl) / 2, top + r - fs * 0.72), lbl, font=f_n, fill=T.WHITE)
        lines = wrap(st["h"], f_h, cw - 20)
        hy = top + 2 * r + 40
        for j, ln in enumerate(lines):
            d.text((cx + cw / 2 - f_h.getlength(ln) / 2, hy + j * 38), ln, font=f_h, fill=T.INK)
        lines = wrap(st["b"], f_b, cw - 24)
        by = hy + head_lines * 38 + 16
        for j, ln in enumerate(lines):
            d.text((cx + cw / 2 - f_b.getlength(ln) / 2, by + j * 33), ln, font=f_b, fill=T.TEXT_MUTED)
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


def lay_end(d, s):
    img = gradient(T.W, T.H, T.INK_DEEP, T.INK, "diag")
    d._image.paste(img, (0, 0))
    d.rectangle([0, T.H - 12, T.W, T.H], fill=T.ACCENT)
    x = T.MARGIN_X
    f_eb = T.font("med", 30)
    d.text((x, 300), s.get("eyebrow", "END OF LECTURE").upper(), font=f_eb, fill=T.GOLD)
    f_t = T.font("bold", 76)
    y = draw_lines(d, x, 356, wrap(s["title"], f_t, T.W - 2 * x), f_t, T.TEXT_LIGHT, 1.16)
    y += 30
    d.rectangle([x, y, x + 130, y + 8], fill=T.ACCENT)
    y += 50
    if s.get("body"):
        y = para(d, x, y, T.W - 2 * x - 100, s["body"], T.font("reg", 32), (168, 192, 212), 1.42)
        y += 36
    for it in s.get("next", []):
        f = T.font("reg", 29)
        d.rounded_rectangle([x, y + 12, x + 11, y + 23], radius=3, fill=T.GOLD)
        y = para(d, x + 38, y, T.W - 2 * x - 60, it, f, (196, 214, 230), 1.4) + 14
    footer(d, s.get("footer_left", ""), s.get("footer_right", ""))


LAYOUTS = {
    "title": lay_title, "section": lay_section, "outline": lay_outline,
    "objectives": lay_objectives, "bullets": lay_bullets, "twocol": lay_twocol,
    "definition": lay_definition, "quote": lay_quote, "table": lay_table,
    "casestudy": lay_casestudy, "takeaways": lay_takeaways, "reading": lay_reading,
    "stats": lay_stats, "process": lay_process, "end": lay_end,
}


def render(spec: dict) -> Image.Image:
    """Render one slide spec to a PIL image."""
    img = Image.new("RGB", (T.W, T.H), T.PAPER)
    d = ImageDraw.Draw(img)
    d._image = img  # allow layouts to paste gradients
    fn = LAYOUTS.get(spec.get("layout", "bullets"))
    if fn is None:
        raise ValueError(f"unknown layout: {spec.get('layout')}")
    fn(d, spec)
    return img
