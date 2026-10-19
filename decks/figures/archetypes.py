"""Diagram archetypes.

Each function draws one canonical systemic-therapy diagram form in the house
visual language.  Week figures are then small data specifications rather than
bespoke drawing code — which keeps 26 courses visually coherent and makes the
whole collection maintainable.
"""
from __future__ import annotations

import math

from pathlib import Path

from .style import Fig, mix

OUT = Path(__file__).resolve().parents[1] / "figures" / "MFT-701"


def _save(f: Fig, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    return f.save(OUT / (name if name.endswith(".png") else f"{name}.png"))


# --------------------------------------------------------------------------
def cycle(pal, name, nodes, *, centre="", sub="", arrows=None, note=""):
    """A closed feedback loop of 3–6 nodes."""
    f = Fig(pal.accent, pal.accent_soft, pal.accent_deep)
    n = len(nodes)
    cx, cy = 50.0, 17.4
    rx, ry = 31.0, 11.0
    pts = []
    for i in range(n):
        # start at the top and run clockwise on the page
        a = math.pi / 2 - 2 * math.pi * i / n
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))

    bw, bh = 19.0, 4.2
    half_w, half_h = bw / 2 + 0.8, bh / 2 + 0.8

    def edge_point(p, q):
        """Where the line from p toward q leaves p's box."""
        dx, dy = q[0] - p[0], q[1] - p[1]
        if dx == 0 and dy == 0:
            return p
        tx = half_w / abs(dx) if dx else 1e9
        ty = half_h / abs(dy) if dy else 1e9
        t = min(tx, ty)
        return p[0] + dx * t, p[1] + dy * t

    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        sx, sy = edge_point(p, q)
        ex, ey = edge_point(q, p)
        f.arrow(sx, sy, ex, ey, color=pal.accent, lw=0.95, rad=-0.09, ms=9)
        if arrows:
            mx, my = (sx + ex) / 2, (sy + ey) / 2
            nx, ny = mx - cx, my - cy
            m = math.hypot(nx, ny) or 1
            f.txt(mx + nx / m * 2.0, my + ny / m * 2.0, arrows[i], size=6.4,
                  face="serif-it", color=f.soft)

    for i, ((x, y), label) in enumerate(zip(pts, nodes)):
        f.box(x - bw / 2, y - bh / 2, bw, bh, fc=f.paper, ec=f.hair, lw=0.7, radius=0.7)
        f.txt(x + 1.2, y, label, size=7.9, face="serif", color=f.ink)
        f.circle(x - bw / 2 + 2.0, y, 1.05, fc=pal.accent, ec="none", z=6)
        f.txt(x - bw / 2 + 2.0, y - 0.05, str(i + 1), size=5.0,
              face="sans-sem", color=f.paper)

    if centre:
        f.txt(cx, cy + (1.1 if sub else 0), centre, size=8.4, face="serif-it",
              color=pal.accent_deep)
        if sub:
            f.txt(cx, cy - 1.9, sub, size=6.4, face="sans-light", color=f.muted)
    if note:
        f.txt(cx, 1.9, note, size=7.0, face="serif-it", color=f.muted)
    return _save(f, name)


# --------------------------------------------------------------------------
def chain(pal, name, steps, *, note="", marker="→"):
    """A developmental sequence: numbered stages along a spine."""
    f = Fig(pal.accent, pal.accent_soft, pal.accent_deep)
    n = len(steps)
    left, right = 4.5, 95.5
    bw = (right - left) / n - 1.6
    gap = (right - left) / n
    y, bh = 10.8, 15.4
    for i, (label, desc) in enumerate(steps):
        x = left + i * gap
        f.box(x, y, bw, bh, fc=f.paper, ec=f.hair, lw=0.7, radius=0.7)
        f.txt(x + 2.6, y + bh - 2.4, f"{i + 1:02d}", size=5.6, face="sans-sem",
              color=pal.accent, ha="left")
        f.line(x + 1.8, y + bh - 3.9, x + 7.0, y + bh - 3.9, color=pal.hair, lw=0.4)
        f.txt(x + bw / 2, y + bh * 0.63, label, size=9.0, face="serif-med",
              color=f.ink)
        f.txt(x + bw / 2, y + bh * 0.28, desc, size=6.4, face="sans-light",
              color=f.soft, linespacing=1.32)
        if i < n - 1:
            f.arrow(x + bw + 0.5, y + bh / 2, x + bw + gap - bw - 0.5, y + bh / 2,
                    color=pal.accent, lw=0.9, ms=7)
    if note:
        f.txt(50, 6.4, note, size=7.0, face="serif-it", color=f.muted)
    return _save(f, name)


# --------------------------------------------------------------------------
def matrix(pal, name, cols, rows, cells, *, note="", highlight=None):
    """A labelled grid — two-by-two models, typologies, comparison tables."""
    f = Fig(pal.accent, pal.accent_soft, pal.accent_deep)
    left, right = 21.0, 92.0
    top, bottom = 28.0, 5.5
    cw = (right - left) / len(cols)
    ch = (top - bottom) / len(rows)
    for j, c in enumerate(cols):
        f.txt(left + cw * (j + 0.5), top + 2.4, c, size=7.4, face="sans-sem",
              color=pal.gold)
    for i, r in enumerate(rows):
        f.txt(left - 2.4, top - ch * (i + 0.5), r, size=6.8, face="sans",
              color=f.soft, ha="right")
    for i in range(len(rows)):
        for j in range(len(cols)):
            x, y = left + j * cw, top - ch * (i + 1)
            key = (i, j)
            hot = highlight == key
            f.box(x + 1.2, y + 1.2, cw - 2.4, ch - 2.4,
                  fc=pal.accent if hot else mix(f.paper, pal.accent, 0.07),
                  ec=pal.accent if hot else f.hair, lw=0.6, radius=0.6)
            head, body = cells[key]
            f.txt(x + cw / 2, y + ch - 3.4, head, size=8.2, face="serif-med",
                  color=f.paper if hot else f.ink)
            f.txt(x + cw / 2, y + (ch - 3.4) / 2 - 1.0, body, size=6.5,
                  face="sans-light", color=f.paper if hot else f.soft,
                  linespacing=1.35)
    if note:
        f.txt(50, 2.2, note, size=6.8, face="serif-it", color=f.muted)
    return _save(f, name)


# --------------------------------------------------------------------------
def layers(pal, name, tiers, *, note="", side=""):
    """A stack of layers — models of levels, skill hierarchies, structures."""
    f = Fig(pal.accent, pal.accent_soft, pal.accent_deep)
    n = len(tiers)
    left, right = 5.0, 86.0
    top, bottom = 30.0, 5.0
    h = (top - bottom) / n
    for i, (label, desc) in enumerate(tiers):
        y = top - (i + 1) * h
        frac = i / max(1, n - 1)
        width = (right - left) * (1 - 0.30 * frac)
        x = left + ((right - left) - width) / 2
        f.box(x, y + 0.5, width, h - 1.0,
              fc=mix(f.paper, pal.accent, 0.10 + 0.62 * frac),
              ec=mix(f.paper, pal.accent, 0.45), lw=0.5, radius=0.5)
        f.txt(x + width / 2, y + h / 2 + 0.9, label, size=8.6, face="serif-med",
              color=f.paper if frac > 0.55 else f.ink)
        f.txt(x + width / 2, y + h / 2 - 1.9, desc, size=6.5, face="sans-light",
              color=f.paper if frac > 0.55 else f.soft)
    if side:
        f.txt(93.0, (top + bottom) / 2, side, size=6.6, face="sans",
              color=f.muted, ha="center", linespacing=1.5)
    if note:
        f.txt(50, 1.9, note, size=6.8, face="serif-it", color=f.muted)
    return _save(f, name)


# --------------------------------------------------------------------------
def spectrum(pal, name, left_label, right_label, marks, *, note=""):
    """A continuum with positioned markers."""
    f = Fig(pal.accent, pal.accent_soft, pal.accent_deep)
    x0, x1, y = 10.0, 90.0, 17.0
    f.line(x0, y, x1, y, color=mix(f.paper, pal.accent, 0.55), lw=1.1)
    for t in (0.0, 0.5, 1.0):
        x = x0 + (x1 - x0) * t
        f.line(x, y - 0.8, x, y + 0.8, color=pal.accent, lw=1.0)
    f.txt(x0, y + 9.6, left_label, size=7.0, face="sans-sem", color=f.soft, ha="left")
    f.txt(x1, y + 9.6, right_label, size=7.0, face="sans-sem", color=f.soft, ha="right")
    for i, (pos, label, desc) in enumerate(marks):
        x = x0 + (x1 - x0) * pos
        up = i % 2 == 0
        f.circle(x, y, 1.0, fc=pal.accent, ec=f.paper, lw=0.7, z=6)
        ty = y + 4.0 if up else y - 8.6
        f.txt(x, ty + 1.1, label, size=7.4, face="serif-med", color=f.ink)
        f.txt(x, ty - 2.0, desc, size=6.1, face="sans-light", color=f.soft,
              linespacing=1.3)
        f.line(x, y + (1.2 if up else -1.2), x, ty - 1.8,
               color=f.hair, lw=0.5, ls=(0, (1.4, 1.7)))
    if note:
        f.txt(50, 2.0, note, size=6.9, face="serif-it", color=f.muted)
    return _save(f, name)


# --------------------------------------------------------------------------
def flow(pal, name, root, branches, *, note=""):
    """A decision tree: one root, three to five branches, outcomes below."""
    f = Fig(pal.accent, pal.accent_soft, pal.accent_deep)
    f.box(35.0, 25.2, 30.0, 4.4, root, fc=pal.accent, ec="none", radius=0.6, size=9.2)
    n = len(branches)
    x0, x1 = 11.0, 89.0
    step = (x1 - x0) / max(1, n - 1) if n > 1 else 0
    bw = 21.0
    for i, (label, outcome) in enumerate(branches):
        x = (x0 + i * step) if n > 1 else 50.0
        f.arrow(50.0, 25.0, x, 20.2, color=pal.accent, lw=0.85, ms=7)
        f.box(min(max(x - bw / 2, 1.0), 99.0 - bw), 15.8, bw, 4.2, label,
              fc=f.paper, ec=f.hair, radius=0.6, size=7.8)
        f.arrow(x, 15.6, x, 11.6, color=f.hair, lw=0.7, ms=6, style="-|>")
        f.txt(x, 9.4, outcome, size=6.4, face="sans-light", color=f.soft,
              linespacing=1.35)
    if note:
        f.txt(50, 3.6, note, size=6.9, face="serif-it", color=f.muted)
    return _save(f, name)


# --------------------------------------------------------------------------
def venn(pal, name, sets, *, centre="", note=""):
    """Two or three overlapping domains."""
    f = Fig(pal.accent, pal.accent_soft, pal.accent_deep)
    cx, cy = 50.0, 17.8
    if len(sets) == 2:
        centres = [(cx - 6.6, cy), (cx + 6.6, cy)]
        r = 10.4
    else:
        centres = [(cx, cy + 4.6), (cx - 7.0, cy - 3.9), (cx + 7.0, cy - 3.9)]
        r = 9.4
    for i, (x, y) in enumerate(centres):
        f.circle(x, y, r, fc=None, ec=None, z=1)
    # fills first, outlines last, so overlaps read evenly
    for (x, y) in centres:
        c = f.circle(x, y, r, fc=mix(f.paper, pal.accent, 0.13), ec=None, z=2)
        c.set_alpha(None)
    for (x, y) in centres:
        f.circle(x, y, r, ec=mix(f.paper, pal.accent, 0.62), lw=0.7, z=8)
    gx = sum(p[0] for p in centres) / len(centres)
    gy = sum(p[1] for p in centres) / len(centres)
    for (x, y), (label, desc) in zip(centres, sets):
        dx, dy = x - gx, y - gy
        m = math.hypot(dx, dy) or 1
        lx, ly = x + dx / m * (r * 0.52), y + dy / m * (r * 0.52)
        f.txt(lx, ly + 0.9, label, size=7.4, face="serif-med", color=f.ink)
        f.txt(lx, ly - 1.7, desc, size=5.9, face="sans-light", color=f.soft)
    if centre:
        f.txt(cx, cy - 1.6, centre, size=7.4, face="serif-it", color=pal.accent_deep)
    if note:
        f.txt(50, 3.2, note, size=6.9, face="serif-it", color=f.muted)
    return _save(f, name)


# --------------------------------------------------------------------------
def quad_axes(pal, name, xlo, xhi, ylo, yhi, points, *, note="", xlabel="", ylabel=""):
    """A two-axis field with named positions — for models and typologies.

    xlo/xhi label the two ends of the horizontal axis, ylo/yhi the two ends of
    the vertical one.  ``points`` are (x, y, label, description) with x and y
    in 0–1.
    """
    f = Fig(pal.accent, pal.accent_soft, pal.accent_deep)
    left, right, bottom, top = 20.0, 92.0, 9.0, 28.0
    f.arrow(left, bottom, right + 1.0, bottom, color=mix(f.paper, pal.accent, 0.55), lw=0.9, ms=8)
    f.arrow(left, bottom, left, top + 1.0, color=mix(f.paper, pal.accent, 0.55), lw=0.9, ms=8)

    f.txt(left + 0.6, 6.2, xlo, size=6.9, face="sans-sem", color=f.soft, ha="left")
    f.txt(right, 6.2, xhi, size=6.9, face="sans-sem", color=f.soft, ha="right")
    f.txt(left - 1.9, bottom - 0.3, ylo, size=6.6, face="serif-it", color=f.muted, ha="right")
    f.txt(left - 1.9, top, yhi, size=6.6, face="serif-it", color=f.muted, ha="right")

    f.line(left, (bottom + top) / 2, right, (bottom + top) / 2, color=f.hair, lw=0.4, ls=(0, (2, 3)))
    f.line((left + right) / 2, bottom, (left + right) / 2, top, color=f.hair, lw=0.4, ls=(0, (2, 3)))

    for x, y, label, desc in points:
        px = left + (right - left) * x
        py = bottom + (top - bottom) * y
        f.circle(px, py, 1.0, fc=pal.accent, ec=f.paper, lw=0.7, z=6)
        f.txt(px + 2.2, py + 0.8, label, size=7.6, face="serif-med", color=f.ink, ha="left")
        f.txt(px + 2.2, py - 1.6, desc, size=6.4, face="sans-light", color=f.soft,
              ha="left", linespacing=1.3)
    if note:
        f.txt(52, 2.2, note, size=6.9, face="serif-it", color=f.muted)
    return _save(f, name)


# --------------------------------------------------------------------------
def triangle(pal, name, top, left, right, *, arrows=None, note="", centre=""):
    """A three-position configuration with directed links."""
    f = Fig(pal.accent, pal.accent_soft, pal.accent_deep)
    pts = {"top": (50.0, 25.4), "left": (25.0, 9.4), "right": (75.0, 9.4)}
    labels = {"top": top, "left": left, "right": right}
    bw, bh = 26.0, 5.0
    for k, (x, y) in pts.items():
        f.box(x - bw / 2, y - bh / 2, bw, bh, fc=f.paper, ec=f.hair, lw=0.8, radius=0.7)
        f.txt(x, y, labels[k], size=8.6, face="serif-med", color=f.ink)

    def edge(a, b):
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        return ax + dx * 0.30, ay + dy * 0.30, ax + dx * 0.70, ay + dy * 0.70

    for i, (a, b) in enumerate([("top", "left"), ("left", "right"), ("right", "top")]):
        sx, sy, ex, ey = edge(a, b)
        f.arrow(sx, sy, ex, ey, color=pal.accent, lw=0.9, ms=8)
        if arrows:
            f.txt((sx + ex) / 2 + 1.6, (sy + ey) / 2 + 0.9, arrows[i], size=6.6,
                  face="serif-it", color=f.soft)
    if centre:
        f.txt(50, 18.4, centre, size=7.4, face="serif-it", color=pal.accent_deep,
              linespacing=1.35)
    if note:
        f.txt(50, 3.2, note, size=6.9, face="serif-it", color=f.muted)
    return _save(f, name)


# --------------------------------------------------------------------------
def stack(pal, name, segments, *, note="", title=""):
    """A single horizontal bar divided into labelled proportions."""
    f = Fig(pal.accent, pal.accent_soft, pal.accent_deep)
    left, right, y, h = 5.0, 95.0, 14.0, 7.0
    total = sum(s[0] for s in segments) or 1.0
    x = left
    for i, (value, label, desc) in enumerate(segments):
        w = (right - left) * value / total
        frac = i / max(1, len(segments) - 1)
        f.box(x, y, w, h, fc=mix(f.paper, pal.accent, 0.14 + 0.60 * frac),
              ec=f.paper, lw=1.2, radius=0.0)
        f.txt(x + w / 2, y + h / 2 + 1.0, f"{value:g}%", size=10.0, face="serif-med",
              color=f.paper if frac > 0.45 else f.ink)
        f.txt(x + w / 2, y + 2.0, label, size=6.6, face="sans-light",
              color=f.paper if frac > 0.45 else f.soft)
        f.txt(x + w / 2, y - 3.2, desc, size=6.5, face="sans-light", color=f.muted,
              linespacing=1.3)
        f.line(x + 3.0, y - 1.6, x + w - 3.0, y - 1.6, color=pal.accent, lw=0.5)
        x += w
    if title:
        f.txt(50, 27.4, title, size=8.2, face="serif-med", color=f.ink)
    if note:
        f.txt(50, 2.2, note, size=6.9, face="serif-it", color=f.muted)
    return _save(f, name)


# --------------------------------------------------------------------------
def hub(pal, name, centre, spokes, *, note=""):
    """A central idea with surrounding components."""
    f = Fig(pal.accent, pal.accent_soft, pal.accent_deep)
    cx, cy = 50.0, 18.0
    rx, ry = 29.0, 7.6
    f.circle(cx, cy, 5.6, fc=pal.accent, ec="none", z=3)
    f.txt(cx, cy, centre, size=7.4, face="sans-sem", color=f.paper, linespacing=1.3)
    n = len(spokes)
    for i, (label, desc) in enumerate(spokes):
        a = math.pi / 2 - 2 * math.pi * i / n
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        f.line(cx + 6.6 * math.cos(a), cy + 6.6 * math.sin(a),
               x - 1.6 * math.cos(a), y - 1.4 * math.sin(a),
               color=pal.accent, lw=0.6, ls=(0, (2, 2)), z=2)
        f.circle(x, y, 0.85, fc=pal.accent, ec=f.paper, lw=0.6, z=5)
        ca, sa = math.cos(a), math.sin(a)
        if abs(ca) > 0.55:
            ha = "left" if ca > 0 else "right"
            lx = x + (1.6 if ca > 0 else -1.6)
            f.txt(lx, y + 0.9, label, size=7.4, face="serif-med", color=f.ink, ha=ha)
            f.txt(lx, y - 1.4, desc, size=6.4, face="sans-light", color=f.soft, ha=ha)
        elif sa > 0:
            f.txt(x, y + 3.6, label, size=7.4, face="serif-med", color=f.ink)
            f.txt(x, y + 1.6, desc, size=6.4, face="sans-light", color=f.soft)
        else:
            f.txt(x, y - 2.4, label, size=7.4, face="serif-med", color=f.ink)
            f.txt(x, y - 4.4, desc, size=6.4, face="sans-light", color=f.soft)
    if note:
        f.txt(50, 2.6, note, size=6.9, face="serif-it", color=f.muted)
    return _save(f, name)
