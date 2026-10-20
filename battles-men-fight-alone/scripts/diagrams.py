"""Reusable conceptual-diagram idioms for Battles Men Fight Alone.

Built on figlib (matplotlib, 0..100 x-canvas, house palette of teal/bronze/ivory).
Every idiom is conceptual: it illustrates a relationship or experience, never a
measured quantity, and is presented as such in the caption.
"""
import math

from figlib import (Fig, INK, GREY, TEAL, TEAL2, TEAL_L, BRONZE, BRONZE_L, IVORY, WHITE,
                    harrow, varrow, note_band, foot, textwrap)


def label(f, x, y, s, color=BRONZE, size=7.4, ha="center"):
    f.text(x, y, s.upper(), size=size, color=color, ha=ha, bold=True)


def iceberg(name, visible, hidden, w=4.6, h=3.9, visible_label="THE VISIBLE SURFACE",
            hidden_label="THE SUBMERGED REALITY", water_label="the waterline of social presentation"):
    f = Fig(name, w, h)
    water = f.H * 0.52
    f.rect(0, water, 100, f.H - water, fc="#EDF3F5", ec="none")
    f.rect(0, 0, 100, water, fc=TEAL_L, ec="none")
    bw = 52
    bh = f.H * 0.26
    f.box(50 - bw / 2, water + 2.0, bw, bh, visible, "teal", size=8.0)
    label(f, 50, water + bh + 4.6, visible_label, size=7.2)
    f.line([2, 98], [water, water], color=TEAL2, lw=1.0, ls=(0, (4, 3)))
    # the waterline caption gets its own clear band beneath the line
    band = 6.2
    f.text(96, water - band / 2 - 0.4, water_label, size=6.4, color=GREY, ha="right", italic=True)
    n = len(hidden)
    gap = 2.0
    avail = water - 4.0 - band - gap * (n - 1)
    hh = avail / n
    for i, item in enumerate(hidden):
        y = 4.0 + (n - 1 - i) * (hh + gap)
        f.box(4, y, 92, hh, item, "light" if i % 2 == 0 else "bronzel", size=7.6)
    label(f, 50, 1.2, hidden_label, size=7.2)
    f.save()


def cycle(name, items, centre=None, w=4.5, h=4.5, rx=33, ry=None, size=7.2):
    f = Fig(name, w, h)
    ry = ry or (f.H / 2 - 12)
    cy = f.H / 2 + (1.5 if centre else 0)
    n = len(items)
    bh = 11
    pts = []
    for i in range(n):
        ang = math.pi / 2 - 2 * math.pi * i / n
        x = 50 + rx * math.cos(ang)
        y = cy + ry * math.sin(ang)
        pts.append((x, y))
    # keep every box inside the canvas: width is limited by the box nearest an edge
    bw = min(40, 2 * min(min(x, 100 - x) for x, _ in pts) - 3)
    for i, item in enumerate(items):
        x, y = pts[i]
        nxt = pts[(i + 1) % n]
        ang = math.atan2(nxt[1] - y, nxt[0] - x)
        sx = x + (bw / 2 - 2) * math.cos(ang)
        sy = y + (bh / 2 - 1) * math.sin(ang)
        ex = nxt[0] - (bw / 2 - 1) * math.cos(ang)
        ey = nxt[1] - (bh / 2 - 1) * math.sin(ang)
        f.arrow(sx, sy, ex, ey, color=BRONZE, lw=1.1, rad=-0.16)
    for i, item in enumerate(items):
        x, y = pts[i]
        f.box(x - bw / 2, y - bh / 2, bw, bh, item, "light" if i % 2 == 0 else "bronzel", size=size)
    if centre:
        cw, ch = 30, 12
        f.box(50 - cw / 2, cy - ch / 2, cw, ch, centre, "teal", size=size + 0.4, bold=True)
    f.save()


def compare(name, head_l, items_l, head_r, items_r, w=4.6, h=None, size=7.4,
            style_l="bronze", style_r="teal"):
    n = max(len(items_l), len(items_r))
    h = h or (1.05 + 0.42 * (n + 1))
    f = Fig(name, w, h)
    top = f.H - 1.5
    hh = 8.4                       # header band: a fixed, shallow strip
    rh = (top - hh - 1.5) / n      # every item row gets an equal share
    cw = 45
    f.box(2, top - hh, cw, hh, head_l, style_l, size=size + 0.6, bold=True)
    f.box(53, top - hh, cw, hh, head_r, style_r, size=size + 0.6, bold=True)
    for i in range(n):
        y = top - hh - (i + 1) * rh
        if i < len(items_l):
            f.box(2, y + 0.45, cw, rh - 0.9, items_l[i], "ivory", size=size)
        if i < len(items_r):
            f.box(53, y + 0.45, cw, rh - 0.9, items_r[i], "light", size=size)
    f.save()


def cards(name, items, cols=2, w=4.6, h=None, size=7.4, note=None):
    rows = (len(items) + cols - 1) // cols
    h = h or (0.5 + 0.52 * rows + (0.45 if note else 0))
    f = Fig(name, w, h)
    top = f.H - (1.6 + (1.2 if note else 0))
    gap = 1.8
    cw = (100 - 4 - gap * (cols - 1)) / cols
    rh = (top - 2.0 - note_band(f, note)) / rows
    styles = ("light", "bronzel", "ivory")
    for i, it in enumerate(items):
        r, c = divmod(i, cols)
        y = top - (r + 1) * rh
        head, _, body = it.partition("|")
        txt = head + (("\n" + body) if body else "")
        f.box(2 + c * (cw + gap), y + 0.5, cw, rh - 1.0, txt, styles[i % 3], size=size)
    foot(f, note, size=6.6)
    f.save()


def stairs(name, steps, w=4.6, h=3.4, size=7.4, note=None):
    f = Fig(name, w, h)
    base = 3.0 + note_band(f, note)
    n = len(steps)
    gap = 1.4
    bw = (100 - 4 - gap * (n - 1)) / n
    avail = max(6.0, f.H - 2.0 - base)
    for i, s in enumerate(steps):
        frac = 0.45 if n == 1 else 0.45 + 0.55 * (i / (n - 1))
        bh = avail * frac
        x = 2 + i * (bw + gap)
        head, _, body = s.partition("|")
        txt = head + (("\n" + body) if body else "")
        f.box(x, base, bw, bh, txt, "teal" if i == n - 1 else ("light" if i % 2 == 0 else "bronzel"),
              size=size)
        if i:
            prev = avail * (0.45 + 0.55 * ((i - 1) / (n - 1))) if n > 1 else avail
            f.arrow(x - gap + 0.15, base + prev, x - 0.15, base + bh, color=BRONZE, lw=1.1)
    foot(f, note, size=6.6)
    f.save()


def balance(name, left_label, left_items, right_label, right_items, w=4.6, h=3.8, size=7.2):
    f = Fig(name, w, h)
    beam_y = f.H * 0.62
    tilt = 5.5
    f.poly([(50 - 3.4, beam_y - 12), (50 + 3.4, beam_y - 12), (50, beam_y - 1.5)], fc=TEAL, ec=TEAL)
    f.line([8, 92], [beam_y - tilt * 0.6, beam_y + tilt * 0.6], color=TEAL, lw=2.6)
    f.text(50, beam_y - 15.5, "load carried", size=6.6, color=GREY, italic=True)
    f.box(3, beam_y + 2.2, 42, 4.6, left_label, "bronze", size=size + 0.4, bold=True)
    f.box(55, beam_y - 7.0, 42, 4.6, right_label, "teal", size=size + 0.4, bold=True)
    n = max(len(left_items), len(right_items))
    rh = (beam_y - 6.0) / (n + 0.4)
    for i in range(n):
        if i < len(left_items):
            f.box(3, beam_y + 8.4 + i * (rh + 0.4), 42, rh, left_items[i], "bronzel", size=size - 0.2)
        if i < len(right_items):
            f.box(55, beam_y - 9.2 - (i + 1) * (rh + 0.4) - 0.0, 42, rh, right_items[i], "light",
                  size=size - 0.2)
    f.save()


def pillars(name, roof, pillars_list, base, w=4.6, h=3.8, size=7.2):
    f = Fig(name, w, h)
    top = f.H - 1.5
    f.box(4, top - 9.0, 92, 8.4, roof, "teal", size=size + 1.0, bold=True)
    n = len(pillars_list)
    gap = 2.0
    cw = (92 - gap * (n - 1)) / n
    ph = f.H * 0.42
    py = 12.0
    for i, p in enumerate(pillars_list):
        f.box(4 + i * (cw + gap), py, cw, ph, p, "light" if i % 2 == 0 else "bronzel", size=size)
    f.box(4, 3.0, 92, 7.2, base, "bronze", size=size, bold=True)
    f.save()


def funnel(name, items, w=4.6, h=3.6, size=7.2, note=None):
    f = Fig(name, w, h)
    top = f.H - (2.0 + (1.4 if note else 0))
    n = len(items)
    rh = (top - 3.0 - note_band(f, note)) / n
    for i, it in enumerate(items):
        wid = 96 - i * (62.0 / max(1, n - 1)) if n > 1 else 96
        y = top - (i + 1) * rh
        f.box(50 - wid / 2, y + 0.6, wid, rh - 1.2, it, "teal" if i == n - 1 else ("light" if i % 2 == 0 else "bronzel"),
              size=size)
    if note:
        f.text(50, 1.0, note, size=6.6, color=GREY, italic=True, wrap=98, va="bottom")
    f.save()


def loadbars(name, items, w=4.6, h=None, size=7.2, note="conceptual illustration — bar lengths are not measurements"):
    h = h or (0.7 + 0.4 * len(items) + 0.5)
    f = Fig(name, w, h)
    top = f.H - 2.0
    rh = (top - 2.0 - note_band(f, note)) / len(items)
    n = len(items)
    for i, it in enumerate(items):
        label_txt, _, weight = it.partition("|")
        frac = float(weight or (1.0 - i * 0.12))
        y = top - (i + 1) * rh
        bw = 62 * frac
        f.box(2, y + 0.5, 30, rh - 1.0, label_txt, "white", size=size, align="left")
        f.rect(33, y + 0.5, bw, rh - 1.0, fc=TEAL if frac > 0.7 else (TEAL2 if frac > 0.45 else BRONZE),
               alpha=0.9 if frac > 0.7 else 0.75)
        f.rect(33 + bw, y + 0.5, 62 - bw, rh - 1.0, fc=TEAL_L)
    foot(f, note, wrap=105)
    f.save()


def rings(name, centre_label, ring_labels, w=4.6, h=4.2, size=7.0):
    """Concentric bands: the man at the centre, each ring of demands around him.

    Every label is auto-fitted to the band it sits in, so long labels shrink
    rather than spilling across the ring boundaries.
    """
    f = Fig(name, w, h)
    cy, cx = f.H / 2, 50
    n = len(ring_labels)
    rmax = min(44, f.H / 2 - 3)
    band = rmax / n
    for i in range(n):
        r = band * (i + 1)
        f.circle(cx, cy, r, fc="#FFFFFF" if i % 2 == 0 else TEAL_L, ec=TEAL2 if i % 2 else BRONZE,
                 lw=1.0, alpha=0.55 if i else 1.0)
    # the centre: a box inscribed in the innermost band
    side = 1.36 * band
    f.box(cx - side / 2, cy - side / 2, side, side, centre_label, "teal", size=size, bold=True)
    for i, lab in enumerate(ring_labels):
        rm = band * (i + 0.5)
        tsize = size
        for _ in range(14):
            wr = max(6, int((1.5 * rm) * f.unit_pt / (0.5 * tsize)))
            lines = textwrap.wrap(lab, wr) or [""]
            if len(lines) * tsize * 1.15 * 1.2 <= 1.5 * band * f.unit_pt or tsize <= 4.6:
                break
            tsize -= 0.2
        ang = math.pi / 2 - 2 * math.pi * i / n
        x = cx + rm * math.cos(ang) * 0.62
        y = cy + rm * math.sin(ang) * 0.62
        f.text(x, y, "\n".join(lines), size=tsize, color=INK)
    f.save()


def sequence(name, steps, w=4.6, h=None, size=7.2, note=None, styles=None):
    """Vertical chain of boxes with downward arrows (a progression of stages)."""
    h = h or (0.8 + 0.44 * len(steps) + (0.5 if note else 0))
    f = Fig(name, w, h)
    top = f.H - 2.0
    gap = 2.4
    n = len(steps)
    bh = (top - 2.5 - note_band(f, note) - gap * (n - 1)) / n
    boxes = []
    for i, s in enumerate(steps):
        y = top - (i + 1) * bh - i * gap
        head, _, body = s.partition("|")
        st = (styles or [])[i] if styles else ("teal" if i == 0 else ("bronze" if i == n - 1 else "light"))
        boxes.append(f.box(6, y, 88, bh, head + (("\n" + body) if body else ""), st, size=size))
    for a, b in zip(boxes, boxes[1:]):
        f.arrow(a[0] + a[2] / 2, a[1], b[0] + b[2] / 2, b[1] + b[3], color=BRONZE, lw=1.2)
    foot(f, note)
    f.save()
