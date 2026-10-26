#!/usr/bin/env python3
"""Diagrams for CAC. 701 Fundamentals of Counseling Theories (weeks 1-4).

Run:  ~/.venv/bin/python cac/scripts/figs_cac701.py
Output: cac/books/cac701/figures/fig-WW-NN.png
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figures as F
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch

BOOK = Path(__file__).resolve().parents[1]
OUT = BOOK / "books" / "cac701" / "figures"


def _arc(ax, cx, cy, r, a0, a1, colour=F.GREY, lw=0.9, head=True):
    """Curved arrow along an arc from angle a0 to a1 (degrees)."""
    import numpy as np
    p0 = (cx + r * np.cos(np.radians(a0)), cy + r * np.sin(np.radians(a0)))
    p1 = (cx + r * np.cos(np.radians(a1)), cy + r * np.sin(np.radians(a1)))
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>" if head else "-",
                                 mutation_scale=8, linewidth=lw, color=colour,
                                 connectionstyle="arc3,rad=0.25", zorder=3,
                                 shrinkA=2, shrinkB=2))


# ---------------------------------------------------------------------------
# Week 2 — psychodynamic map
# ---------------------------------------------------------------------------
def fig_02_01():
    fig, ax = F.canvas(4.6, 3.0)
    F.txt(ax, 50, 96, "THE PSYCHODYNAMIC MAP: TOPOGRAPHY AND STRUCTURE", size=6.6,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([22, 78], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)

    # left: topography as depth layers
    F.txt(ax, 25, 86, "TOPOGRAPHY", size=6.0, color=F.TEAL, weight="bold")
    layers = [("conscious", 78, F.TEAL_LIGHT, F.TEAL),
              ("preconscious", 64, "#CFE0E4", F.TEAL),
              ("unconscious", 44, "#9FBCC4", "#0B3A45")]
    F.box(ax, 6, 74, 38, 10, layers[0][2], edge=layers[0][3])
    F.txt(ax, 25, 79, layers[0][0], size=6.2, color=F.TEAL)
    F.box(ax, 6, 60, 38, 12, layers[1][2], edge=layers[1][3])
    F.txt(ax, 25, 66, layers[1][0], size=6.2, color=F.TEAL)
    F.box(ax, 6, 18, 38, 40, layers[2][2], edge=layers[2][3])
    F.txt(ax, 25, 40, layers[2][0], size=6.4, color="#0B3A45", weight="bold")
    F.txt(ax, 25, 33, "wishes, fears, memories\nkept out of awareness\nby repression", size=5.7,
          color="#123F4A")
    F.txt(ax, 25, 12, "what the child cannot say,\nthe child enacts", size=5.6,
          color=F.GREY, style="italic")

    # right: structure as three overlapping circles
    F.txt(ax, 73, 86, "STRUCTURE", size=6.0, color=F.TEAL, weight="bold")
    ax.add_patch(Circle((66, 52), 15, facecolor=F.BRONZE_LIGHT, edgecolor=F.BRONZE_TEXT,
                        lw=0.9, zorder=2))
    ax.add_patch(Circle((80, 52), 15, facecolor=F.TEAL_LIGHT, edgecolor=F.TEAL,
                        lw=0.9, zorder=2))
    ax.add_patch(Circle((73, 63), 13, facecolor="#FFFFFF", edgecolor=F.GREY,
                        lw=0.9, zorder=3))
    F.txt(ax, 63, 47, "id", size=7.0, color=F.BRONZE_TEXT, weight="bold")
    F.txt(ax, 63, 42, "impulse,\nwish", size=5.5, color=F.INK)
    F.txt(ax, 83, 47, "superego", size=6.2, color=F.TEAL, weight="bold")
    F.txt(ax, 83, 41, "rule,\nconscience", size=5.5, color=F.INK)
    F.txt(ax, 73, 66, "ego", size=7.0, color=F.INK, weight="bold")
    F.txt(ax, 73, 60.5, "mediates", size=5.5, color=F.GREY)
    F.txt(ax, 73, 12, "anxiety is the signal that the mediation is failing", size=5.6,
          color=F.GREY, style="italic")
    F.save(fig, "fig-02-01.png")


def fig_02_02():
    fig, ax = F.canvas(4.6, 2.9)
    F.txt(ax, 50, 95, "PLAY AS THE CHILD'S LANGUAGE: FOUR CHANNELS OF EVIDENCE",
          size=6.4, color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [91.5, 91.5], color=F.BRONZE, lw=1.0, zorder=3)

    F.box(ax, 38, 42, 24, 18, F.TEAL, r=2.2)
    F.txt(ax, 50, 54, "THE CHILD", size=6.8, color="#F2E3C9", weight="bold")
    F.txt(ax, 50, 48, "at play", size=6.2, color="#CFE0E4", style="italic")

    chans = [
        (16, 74, "CONTENT", "what is enacted:\nthemes, roles, endings", F.TEAL_LIGHT, F.TEAL),
        (84, 74, "RELATIONSHIP", "how you are used:\nhelp, ignore, control, test", F.TEAL_LIGHT, F.TEAL),
        (16, 24, "SYMBOL", "what stands for what:\nthe doorless house", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (84, 24, "REGULATION", "how arousal rises\nand is recovered", F.BRONZE_LIGHT, F.BRONZE_TEXT),
    ]
    for cx, cy, t, b, fill, edge in chans:
        F.box(ax, cx - 15, cy - 11, 30, 22, fill, edge=edge, r=1.6)
        F.txt(ax, cx, cy + 6.5, t, size=6.0, color=edge, weight="bold")
        F.txt(ax, cx, cy - 2.5, b, size=5.8, color=F.INK)
    for sx, sy, ex, ey in ((26, 64, 40, 58), (74, 64, 60, 58), (26, 34, 40, 44), (74, 34, 60, 44)):
        F.arrow(ax, (sx, sy), (ex, ey), color=F.GREY, lw=0.8)
    F.txt(ax, 50, 5.5, "Four channels, four hypotheses. A channel observed once is an anecdote;\n"
                      "a channel observed across sessions is evidence.",
          size=5.7, color=F.GREY, style="italic")
    F.save(fig, "fig-02-02.png")


# ---------------------------------------------------------------------------
# Week 3 — attachment
# ---------------------------------------------------------------------------
def fig_03_01():
    fig, ax = F.canvas(4.6, 3.1)
    F.txt(ax, 50, 96, "ORGANISED AND DISORGANISED ATTACHMENT AT TWELVE MONTHS",
          size=6.4, color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)

    x0, x1, y0, y1 = 16, 92, 16, 84
    ax.plot([x0, x1], [y0, y0], color=F.INK, lw=0.9, zorder=3)
    ax.plot([x0, x0], [y0, y1], color=F.INK, lw=0.9, zorder=3)
    F.arrow(ax, (x1, y0), (x1 + 4, y0), color=F.INK, lw=0.9)
    F.arrow(ax, (x0, y1), (x0, y1 + 4), color=F.INK, lw=0.9)
    F.txt(ax, 55, 10.5, "AVOIDANCE  →  (deactivating: minimise the signal)", size=5.8,
          color=F.INK, weight="bold")
    F.txt(ax, 7, 52, "RESISTANCE  →", size=5.8, color=F.INK, weight="bold", )
    F.txt(ax, 7, 47, "(heighten the signal)", size=5.2, color=F.GREY)

    quads = [
        (34, 66, "RESISTANT (C)", "high resistance, low avoidance:\ndistress amplified, comfort\nrefused or half-taken", F.IVORY, F.GREY),
        (74, 66, "DISORGANISED (D)", "no coherent strategy: approach\nthen freeze, stilling,\ncontradiction", "#F7EDE9", "#8C3B2E"),
        (34, 32, "SECURE (B)", "low avoidance, low resistance:\ndistress shown, comfort\naccepted, play resumes", F.TEAL_LIGHT, F.TEAL),
        (74, 32, "AVOIDANT (A)", "high avoidance, low resistance:\ndistress masked, comfort not\nsought, play as shield", F.IVORY, F.GREY),
    ]
    for cx, cy, t, b, fill, edge in quads:
        F.box(ax, cx - 17, cy - 12, 34, 24, fill, edge=edge, r=1.6)
        F.txt(ax, cx, cy + 7, t, size=6.2, color=edge, weight="bold")
        F.txt(ax, cx, cy - 3, b, size=5.7, color=F.INK)
    F.txt(ax, 50, 4.5, "After Ainsworth, Blehar, Waters and Wall (1978); category D added by\n"
                       "Main and Solomon (1990). Percentages vary by sample and by risk.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-03-01.png")


def fig_03_02():
    fig, ax = F.canvas(4.6, 3.0)
    F.txt(ax, 50, 96, "THE SECURE-BASE CYCLE", size=6.8, color=F.BRONZE_TEXT, weight="bold")
    ax.plot([36, 64], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)

    ax.add_patch(Circle((50, 50), 12, facecolor=F.TEAL, edgecolor="none", zorder=2))
    F.txt(ax, 50, 53, "CAREGIVER", size=6.2, color="#F2E3C9", weight="bold")
    F.txt(ax, 50, 47, "sensitive,\npredictable", size=5.6, color="#CFE0E4")

    nodes = [
        (50, 84, "EXPLORE", "the child goes out\nto the world", 90),
        (82, 50, "SIGNAL", "distress or need\nis expressed", 0),
        (50, 16, "SAFE HAVEN", "comfort is given\nand taken", 270),
        (18, 50, "REGULATE", "arousal falls; the\nbody settles", 180),
    ]
    for cx, cy, t, b, a in nodes:
        F.box(ax, cx - 14, cy - 9, 28, 18, F.TEAL_LIGHT if a in (90, 270) else F.BRONZE_LIGHT,
              edge=F.TEAL if a in (90, 270) else F.BRONZE_TEXT, r=1.6)
        F.txt(ax, cx, cy + 4.5, t, size=6.0, weight="bold",
              color=F.TEAL if a in (90, 270) else F.BRONZE_TEXT)
        F.txt(ax, cx, cy - 3, b, size=5.6, color=F.INK)
    import numpy as np
    for a0, a1 in ((70, 20), (340, 290), (250, 200), (160, 110)):
        _arc(ax, 50, 50, 33, a0, a1, colour=F.GREY, lw=0.9)
    F.txt(ax, 50, 4.0, "A cycle that completes teaches the child that distress is survivable and\n"
                      "the world is worth exploring. A cycle that breaks teaches the opposite.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-03-02.png")


# ---------------------------------------------------------------------------
# Week 4 — mentalisation
# ---------------------------------------------------------------------------
def fig_04_01():
    fig, ax = F.canvas(4.6, 2.9)
    F.txt(ax, 50, 95, "THE MENTALISING LOOP IN A SESSION WITH A CHILD", size=6.6,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([26, 74], [91.5, 91.5], color=F.BRONZE, lw=1.0, zorder=3)

    steps = [
        (18, 70, "1  OBSERVE", "behaviour, face,\nplay, silence", F.TEAL_LIGHT, F.TEAL),
        (50, 78, "2  INFER", "what is the child\nfeeling and wanting?", F.TEAL_LIGHT, F.TEAL),
        (82, 70, "3  CHECK OWN STATE", "what am I feeling,\nand whose is it?", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (82, 32, "4  RESPOND MARKED", "mirrored but not\nidentical; named", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (50, 24, "5  CHILD SEEN", "a mind holding a mind;\narousal becomes meaning", F.TEAL, F.TEAL),
        (18, 32, "6  REPEAT", "thousands of times,\nacross childhood", F.IVORY, F.GREY),
    ]
    for cx, cy, t, b, fill, edge in steps:
        F.box(ax, cx - 15, cy - 9.5, 30, 19, fill, edge=edge, r=1.6)
        tc = "#F2E3C9" if fill == F.TEAL else edge
        bc = "#FFFFFF" if fill == F.TEAL else F.INK
        F.txt(ax, cx, cy + 5, t, size=5.9, color=tc, weight="bold")
        F.txt(ax, cx, cy - 3, b, size=5.6, color=bc)
    for p0, p1 in [((33, 74), (35, 76)), ((65, 78), (67, 74)), ((82, 60), (82, 42)),
                   ((67, 28), (65, 26)), ((35, 24), (33, 28)), ((18, 42), (18, 60))]:
        F.arrow(ax, p0, p1, color=F.GREY, lw=0.9)
    F.txt(ax, 50, 5.0, "When the loop runs, the child learns that minds can hold minds.\n"
                      "When it fails — flat, frightened or frightening responding — it does not.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-04-01.png")


def main():
    F._register_fonts()
    F.set_outdir(OUT)
    print(f"Drawing CAC.701 figures -> {OUT}")
    for fn in (F.fig_01_01, F.fig_01_02, F.fig_01_03,
               fig_02_01, fig_02_02, fig_03_01, fig_03_02, fig_04_01):
        fn()
    print("Done")


if __name__ == "__main__":
    main()
