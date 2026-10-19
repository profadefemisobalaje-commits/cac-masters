"""Diagram toolkit for the lecture decks.

One visual language for every figure in the collection: ink linework on the
same ivory paper as the slides, with the course accent as the only colour
note.  Coordinates run 0–100 across and 0–34.5 up.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import (Circle, FancyArrowPatch, FancyBboxPatch,
                                Polygon, Rectangle, Wedge, Arc)

from .. import theme

FONT = theme.FONTS
FP = {
    "serif": FontProperties(fname=str(FONT / "EBGaramond-Regular.otf")),
    "serif-it": FontProperties(fname=str(FONT / "EBGaramond-Italic.otf")),
    "serif-med": FontProperties(fname=str(FONT / "EBGaramond-Medium.otf")),
    "serif-sem": FontProperties(fname=str(FONT / "EBGaramond-SemiBold.otf")),
    "sans": FontProperties(fname=str(FONT / "SourceSans3-Regular.otf")),
    "sans-light": FontProperties(fname=str(FONT / "SourceSans3-Light.otf")),
    "sans-sem": FontProperties(fname=str(FONT / "SourceSans3-Semibold.otf")),
    "sans-it": FontProperties(fname=str(FONT / "SourceSans3-It.otf")),
}

W, H = 100.0, 34.5


def mix(a: str, b: str, t: float) -> str:
    """Blend two hex colours by t (0 = a, 1 = b).

    Alpha is avoided in most figures: matplotlib composites transparency
    inconsistently onto transparent canvases, which shows up as darkened
    plates when the PNG is placed on the slide.
    """
    ra, ga, ba = theme.hex_rgb(a)
    rb, gb, bb = theme.hex_rgb(b)
    return "#%02X%02X%02X" % (round(ra + (rb - ra) * t),
                              round(ga + (gb - ga) * t),
                              round(ba + (bb - ba) * t))


class Fig:
    def __init__(self, accent: str, accent_soft: str, accent_deep: str,
                 w: float = 10.0, h: float = 3.45):
        self.accent = accent
        self.accent_soft = accent_soft
        self.accent_deep = accent_deep
        self.ink = theme.INK
        self.soft = theme.INK_SOFT
        self.muted = theme.MUTED
        self.gold = theme.GOLD
        self.hair = theme.HAIR
        self.paper = theme.PAPER
        self.fig = plt.figure(figsize=(w, h), dpi=240)
        self.fig.patch.set_facecolor("none")
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, W)
        self.ax.set_ylim(0, H)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

    # -- primitives -----------------------------------------------------
    def txt(self, x, y, s, size=8.0, face="sans", color=None, ha="center",
            va="center", alpha=1.0, style="normal", weight="normal",
            rotation=0, linespacing=1.25):
        return self.ax.text(x, y, s, fontproperties=FP[face], fontsize=size,
                            color=color or self.ink, ha=ha, va=va,
                            alpha=alpha, rotation=rotation,
                            linespacing=linespacing)

    def box(self, x, y, w, h, text="", size=8.2, face="sans", fc=None, ec=None,
            tc=None, lw=0.7, radius=0.8, alpha=1.0, z=2, weight="normal"):
        p = FancyBboxPatch((x, y), w, h,
                           boxstyle=f"round,pad=0,rounding_size={radius}",
                           fc=fc if fc else "none",
                           ec=ec if ec else self.hair, lw=lw, alpha=alpha, zorder=z)
        self.ax.add_patch(p)
        if text:
            self.txt(x + w / 2, y + h / 2, text, size=size, face=face,
                     color=tc or self.ink)
        return p

    def circle(self, cx, cy, r, fc=None, ec=None, lw=0.8, alpha=1.0, z=2):
        c = Circle((cx, cy), r, fc=fc if fc else "none",
                   ec=ec if ec else "none", lw=lw, alpha=alpha, zorder=z)
        self.ax.add_patch(c)
        return c

    def arrow(self, x1, y1, x2, y2, color=None, lw=0.9, rad=0.0, z=3,
              style="-|>", ms=8, ls="-", alpha=1.0):
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                            mutation_scale=ms, lw=lw, color=color or self.soft,
                            connectionstyle=f"arc3,rad={rad}", zorder=z,
                            linestyle=ls, alpha=alpha, shrinkA=2, shrinkB=2)
        self.ax.add_patch(a)
        return a

    def line(self, x1, y1, x2, y2, color=None, lw=0.7, ls="-", z=2, alpha=1.0):
        return self.ax.plot([x1, x2], [y1, y2], color=color or self.hair,
                            lw=lw, ls=ls, zorder=z, alpha=alpha,
                            solid_capstyle="round")[0]

    def label(self, x, y, s, size=6.4, color=None, ha="center", va="center"):
        return self.txt(x, y, s.upper(), size=size, face="sans-sem",
                        color=color or self.gold, ha=ha, va=va)

    def tag(self, x, y, s, fc=None, tc=None, size=6.2, pad=0.35):
        """A small filled label plate."""
        w = max(2.2, len(s) * size * 0.052 + 1.6)
        self.box(x - w / 2, y - 0.9, w, 1.8, fc=fc or self.accent, ec="none",
                 radius=0.35, z=6)
        self.txt(x, y, s.upper(), size=size, face="sans-sem",
                 color=tc or self.paper)

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.fig.savefig(path, transparent=True, dpi=240,
                         bbox_inches=None, pad_inches=0)
        plt.close(self.fig)
        return path
