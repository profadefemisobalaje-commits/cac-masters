"""Small diagram toolkit for the book's figures (matplotlib).

All figures share one visual language: deep teal, bronze, ivory, Source Sans.
Coordinates are in a 0..100 (x) by 0..H (y) canvas, origin bottom-left.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon, Rectangle, Wedge
import textwrap as _tw


class textwrap:
    @staticmethod
    def wrap(s, w):
        # Whole words only: a box that is too narrow for the text is a content
        # problem, and mid-word breaks read as a typesetting fault.
        return _tw.wrap(s, w, break_long_words=False, break_on_hyphens=False)


BOOK = Path(__file__).resolve().parents[1]
OUT = BOOK / "figures"
OUT.mkdir(exist_ok=True)

for f in (BOOK / "fonts").glob("SourceSans3-*.otf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams["font.family"] = "Source Sans 3"

TEAL = "#0F4C5C"
TEAL2 = "#2F7F8F"
TEAL_L = "#E3EEF0"
BRONZE = "#9C6B30"
BRONZE_L = "#F4EADB"
IVORY = "#FBF8F1"
INK = "#1B1B1B"
GREY = "#5E6468"
WHITE = "#FFFFFF"

STYLES = {
    "teal": (TEAL, WHITE, TEAL),
    "teal2": (TEAL2, WHITE, TEAL2),
    "light": (TEAL_L, INK, TEAL),
    "bronze": (BRONZE, WHITE, BRONZE),
    "bronzel": (BRONZE_L, INK, BRONZE),
    "ivory": (IVORY, INK, GREY),
    "white": (WHITE, INK, TEAL),
}


class Fig:
    def __init__(self, name, w=4.6, h=3.0, H=None):
        self.name = name
        self.unit_pt = w * 72 / 100
        self.H = H if H is not None else 100 * h / w
        self.fig, self.ax = plt.subplots(figsize=(w, h))
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, self.H)
        self.ax.axis("off")
        self.fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)

    def box(self, x, y, w, h, text, style="light", size=8.5, wrap=None, bold=False, align="center", radius=1.2, lw=0.9):
        fc, tc, ec = STYLES[style]
        p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                           fc=fc, ec=ec, lw=lw)
        self.ax.add_patch(p)
        ha = {"center": "center", "left": "left"}[align]
        tx = x + w / 2 if align == "center" else x + 1.5
        t = self.ax.text(tx, y + h / 2, "", ha=ha, va="center", fontsize=size, color=tc,
                         fontweight="bold" if bold else "normal", linespacing=1.15)
        # Shrink the type until the wrapped text measures inside the box.  The
        # measurement uses the renderer, so it is exact rather than estimated.
        try:
            r = self.fig.canvas.get_renderer()
            box_px = h * self.ax.get_window_extent().height / self.H
        except Exception:
            r, box_px = None, None
        fitted = size
        for _ in range(18):
            wr = wrap or max(6, int((w - 1.6) * self.unit_pt / (0.5 * fitted)))
            lines = []
            for para in text.split("\n"):
                lines.extend(textwrap.wrap(para, wr) or [""])
            t.set_text("\n".join(lines))
            t.set_fontsize(fitted)
            if r is None:
                break
            bb = t.get_window_extent(renderer=r)
            if bb.height <= box_px * 0.94 or fitted <= 4.4:
                break
            fitted -= 0.2
        return (x, y, w, h)

    def text(self, x, y, s, size=8, color=INK, ha="center", va="center", bold=False, italic=False, wrap=None, rot=0):
        if wrap:
            s = "\n".join(textwrap.wrap(s, wrap))
        self.ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, rotation=rot,
                     fontweight="bold" if bold else "normal", fontstyle="italic" if italic else "normal",
                     linespacing=1.15)

    def arrow(self, x1, y1, x2, y2, color=GREY, lw=1.1, style="-|>", rad=0.0, ls="-"):
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=9,
                            color=color, lw=lw, connectionstyle=f"arc3,rad={rad}", linestyle=ls,
                            shrinkA=0, shrinkB=0)
        self.ax.add_patch(a)

    def line(self, xs, ys, color=GREY, lw=1.0, ls="-"):
        self.ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle="round", zorder=0.5)

    def circle(self, x, y, r, fc=TEAL_L, ec=TEAL, lw=1.0, alpha=1.0):
        self.ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=3))

    def poly(self, pts, fc=TEAL_L, ec=TEAL, lw=0.8, alpha=1.0):
        self.ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=lw, alpha=alpha))

    def rect(self, x, y, w, h, fc=TEAL_L, ec="none", lw=0.8, alpha=1.0):
        self.ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, alpha=alpha))

    def title(self, s, y=None):
        # Figure titles are carried by the book caption; in-image titles are suppressed
        # to avoid duplication and to keep a clean, publisher-style appearance.
        return

    def save(self):
        self.ax.set_aspect("equal")
        self.fig.savefig(OUT / f"{self.name}.png", dpi=300, facecolor="white")
        plt.close(self.fig)


def harrow(f, b1, b2, **kw):
    """Arrow from right edge of box b1 to left edge of box b2."""
    x1, y1, w1, h1 = b1
    x2, y2, w2, h2 = b2
    f.arrow(x1 + w1, y1 + h1 / 2, x2, y2 + h2 / 2, **kw)


def note_band(f, note, wrap=98, size=6.4):
    """Height (canvas units) that a bottom note occupies, so boxes can clear it."""
    if not note:
        return 0.0
    lines = len(textwrap.wrap(note, wrap)) or 1
    return lines * size * 1.2 / f.unit_pt + 2.2


def foot(f, note, wrap=98, size=6.4, y=1.0):
    """Draw a small italic note at the foot of a figure."""
    if note:
        f.text(50, y, note, size=size, color=GREY, italic=True, wrap=wrap, va="bottom")


def varrow(f, b1, b2, **kw):
    """Arrow from bottom of b1 to top of b2."""
    x1, y1, w1, h1 = b1
    x2, y2, w2, h2 = b2
    f.arrow(x1 + w1 / 2, y1, x2 + w2 / 2, y2 + h2, **kw)


def chain(name, steps, title=None, h=2.4, styles=None, size=8, note=None):
    """Horizontal process chain."""
    f = Fig(name, 4.6, h)
    n = len(steps)
    gap = 2.2
    w = (100 - 4 - gap * (n - 1)) / n
    y = f.H * 0.28
    bh = f.H * 0.44
    boxes = []
    for i, s in enumerate(steps):
        st = styles[i] if styles else ("teal" if i % 2 == 0 else "light")
        head, _, body = s.partition("|")
        b = f.box(2 + i * (w + gap), y, w, bh, head + ("\n" + body if body else ""), st, size=size)
        boxes.append(b)
    for a, b in zip(boxes, boxes[1:]):
        harrow(f, a, b, color=BRONZE, lw=1.3)
    if title:
        f.title(title, y=f.H - 2.5)
    if note:
        f.text(50, f.H * 0.12, note, size=7, color=GREY, italic=True, wrap=130)
    f.save()


def vflow(name, steps, title=None, w=4.6, h=6.0, side=None, size=8.2):
    """Vertical decision/process flow with optional side notes."""
    f = Fig(name, w, h)
    n = len(steps)
    top = f.H - (7 if title else 3)
    gap = 2.2
    bh = (top - 3 - gap * (n - 1)) / n
    bw = 52 if side else 76
    x = 4 if side else 12
    boxes = []
    for i, s in enumerate(steps):
        y = top - (i + 1) * bh - i * gap
        st = "teal" if i == 0 else ("bronze" if i == n - 1 else "light")
        b = f.box(x, y, bw, bh, s, st, size=size)
        boxes.append(b)
        if side and side[i]:
            f.box(x + bw + 4, y + bh * 0.1, 100 - x - bw - 6, bh * 0.8, side[i], "ivory", size=size - 1)
            f.arrow(x + bw, y + bh / 2, x + bw + 4, y + bh / 2, color=GREY, lw=0.8, style="-")
    for a, b in zip(boxes, boxes[1:]):
        varrow(f, a, b, color=BRONZE, lw=1.2)
    if title:
        f.title(title, y=f.H - 3)
    f.save()


def hub(name, centre, spokes, title=None, w=4.6, h=4.6, size=7.8, rx=37, ry=None):
    """Central box with surrounding boxes (contract webs, institutional maps)."""
    import math
    f = Fig(name, w, h)
    cy = f.H / 2 - (2 if title else 0)
    ry = ry or (f.H / 2 - 9)
    cw, ch = 24, 11
    c = f.box(50 - cw / 2, cy - ch / 2, cw, ch, centre, "teal", size=size + 0.6, bold=True)
    n = len(spokes)
    for i, s in enumerate(spokes):
        ang = math.pi / 2 - 2 * math.pi * i / n
        x = 50 + rx * math.cos(ang)
        y = cy + ry * math.sin(ang)
        bw, bh = 24, 12
        f.line([50, x], [cy, y], color=BRONZE, lw=0.9)
        f.box(x - bw / 2, y - bh / 2, bw, bh, s, "light" if i % 2 == 0 else "bronzel", size=size)
    f.box(50 - cw / 2, cy - ch / 2, cw, ch, centre, "teal", size=size + 0.6, bold=True)
    if title:
        f.title(title, y=f.H - 2.5)
    f.save()


def matrix(name, cols, rows, title=None, w=4.6, h=None, size=7.4, first_w=22):
    """Grid diagram: header row + labelled rows of cells."""
    nr = len(rows)
    h = h or (0.9 + 0.48 * (nr + 1))
    f = Fig(name, w, h)
    top = f.H - (6 if title else 1.5)
    rh = (top - 1.5) / (nr + 1)
    nc = len(cols)
    cw = (100 - 2 - first_w) / nc
    for j, c in enumerate(cols):
        f.box(1 + first_w + j * cw + 0.4, top - rh + 0.4, cw - 0.8, rh - 0.8, c, "teal", size=size, bold=True)
    for i, r in enumerate(rows):
        y = top - (i + 2) * rh
        f.box(1 + 0.4, y + 0.4, first_w - 0.8, rh - 0.8, r[0], "bronze", size=size, bold=True)
        for j, cell in enumerate(r[1:]):
            f.box(1 + first_w + j * cw + 0.4, y + 0.4, cw - 0.8, rh - 0.8, cell,
                  "light" if i % 2 == 0 else "ivory", size=size - 0.4)
    if title:
        f.title(title, y=f.H - 2.8)
    f.save()


def timeline(name, events, title=None, w=4.6, h=4.4, size=6.9):
    f = Fig(name, w, h)
    y0 = f.H / 2 - 2
    f.line([3, 97], [y0, y0], color=TEAL, lw=2.2)
    n = len(events)
    for i, (yr, label) in enumerate(events):
        x = 4 + i * (92 / (n - 1))
        up = i % 2 == 0
        f.circle(x, y0, 0.75, fc=BRONZE, ec=WHITE, lw=0.8)
        yy = y0 + (8 if up else -8)
        f.line([x, x], [y0, yy], color=BRONZE, lw=0.7)
        f.text(x, yy + (1.8 if up else -1.8), yr, size=size + 0.8, color=TEAL, bold=True)
        f.text(x, yy + (8.5 if up else -8.5), label, size=size, color=INK, wrap=15)
    if title:
        f.title(title, y=f.H - 2.5)
    f.save()


def layers(name, items, title=None, w=4.6, h=4.2, size=8, pyramid=True):
    """Stacked layers / pyramid (top item narrowest)."""
    f = Fig(name, w, h)
    n = len(items)
    top = f.H - (7 if title else 2)
    lh = (top - 2) / n
    for i, (lab, desc) in enumerate(items):
        y = top - (i + 1) * lh
        if pyramid:
            inset = (n - 1 - i) * 0 + (i) * 0
            wid = 30 + i * (60 / max(1, n - 1))
        else:
            wid = 90
        x = 50 - wid / 2
        st = ["teal", "teal2", "light", "bronzel", "ivory", "light", "bronzel"][i % 7]
        f.box(x, y + 0.5, wid, lh - 1, f"{lab}" + (f"\n{desc}" if desc else ""), st, size=size)
    if title:
        f.title(title, y=f.H - 3)
    f.save()


def vtimeline(name, events, w=4.6, h=None, size=7.2):
    """Vertical timeline: year on the left, event on the right."""
    n = len(events)
    h = h or (0.3 + 0.27 * n)
    f = Fig(name, w, h)
    top, bot = f.H - 2, 2
    step = (top - bot) / (n - 1)
    f.line([16, 16], [bot, top], color=TEAL, lw=1.8)
    for i, (yr, label) in enumerate(events):
        y = top - i * step
        f.circle(16, y, 0.9, fc=BRONZE, ec=WHITE, lw=0.6)
        f.text(13, y, yr, size=size + 0.4, color=TEAL, bold=True, ha="right")
        f.text(20, y, label, size=size, color=INK, ha="left")
    f.save()
