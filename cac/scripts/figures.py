#!/usr/bin/env python3
"""Draw the handbook's diagrams into cac/figures/.

Every figure is a function fig_NN_MM() writing fig-NN-MM.png, where NN is the chapter
number. Style: the house palette (teal ink, bronze accent, ivory ground), Source Sans 3
from cac/fonts, 300 dpi, sized to sit inside a 6 x 9 in type area.

Usage:  ~/.venv/bin/python cac/scripts/figures.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

BOOK = Path(__file__).resolve().parents[1]
FIGS = BOOK / "figures"
FONTS = BOOK / "fonts"

TEAL = "#0F4C5C"
TEAL_LIGHT = "#E3EEF0"
BRONZE = "#9C6B30"
BRONZE_TEXT = "#8A5A26"
BRONZE_LIGHT = "#F4EADB"
IVORY = "#FBF8F1"
INK = "#1B1B1B"
GREY = "#5E6468"
RUST = "#8C3B2E"
WHITE = "#FFFFFF"

W, H = 4.6, 3.1          # inches at 300 dpi -> 1380 x 930 px
DPI = 300


def _register_fonts():
    for f in sorted(FONTS.glob("*.otf")):
        font_manager.fontManager.addfont(str(f))
    plt.rcParams["font.family"] = "Source Sans 3"
    plt.rcParams["text.color"] = INK
    plt.rcParams["axes.linewidth"] = 0.8


def canvas(w=W, h=H):
    fig = plt.figure(figsize=(w, h), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    fig.patch.set_facecolor(WHITE)
    return fig, ax


def box(ax, x, y, w, h, fill, edge=None, r=1.6, lw=0.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                linewidth=lw, facecolor=fill,
                                edgecolor=edge if edge else "none", zorder=2))


def txt(ax, x, y, s, size=7.2, color=INK, weight="regular", ha="center", va="center",
        style="normal", spacing=None, zorder=4):
    kw = dict(fontsize=size, color=color, fontweight=weight, ha=ha, va=va,
              fontstyle=style, zorder=zorder)
    ax.text(x, y, s, **kw)
    if spacing:
        pass


def arrow(ax, p1, p2, color=GREY, lw=0.9, style="-|>", rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=8,
                                 linewidth=lw, color=color, zorder=3,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=1, shrinkB=1))


OUTDIR = {"dir": FIGS}


def set_outdir(path):
    OUTDIR["dir"] = Path(path)


def save(fig, name):
    OUTDIR["dir"].mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTDIR["dir"] / name, dpi=DPI, facecolor=WHITE)
    plt.close(fig)
    print("  drew", name)


# ---------------------------------------------------------------------------
# Chapter 1 — CAC. 701 Fundamentals of Counseling Theories
# ---------------------------------------------------------------------------
def fig_01_01():
    """The four questions every counselling theory answers."""
    fig, ax = canvas(4.6, 3.3)
    txt(ax, 50, 95, "THE FOUR QUESTIONS A THEORY MUST ANSWER", size=7.0,
        color=BRONZE_TEXT, weight="bold")
    ax.plot([34, 66], [91.5, 91.5], color=BRONZE, lw=1.1, zorder=3)

    centre = (50, 52)
    box(ax, centre[0] - 17, centre[1] - 11, 34, 22, TEAL, r=2.4)
    txt(ax, 50, 57.5, "THE CASE", size=7.4, color="#F2E3C9", weight="bold")
    txt(ax, 50, 51, "What is this child's\nproblem, and what\nmaintains it?",
        size=6.6, color=WHITE)
    txt(ax, 50, 43.5, "formulation", size=6.2, color="#BFD4D9", style="italic")

    quads = [
        (25, 76, "1  HUMAN NATURE", "How does a child\ndevelop, and what\ngoes wrong?", TEAL_LIGHT, TEAL),
        (75, 76, "2  MAINTENANCE", "What keeps the\nproblem in place\nright now?", TEAL_LIGHT, TEAL),
        (25, 26, "3  MECHANISM", "By what process\ndoes change\nactually happen?", BRONZE_LIGHT, BRONZE_TEXT),
        (75, 26, "4  METHOD", "What does the\ncounsellor do, in\nwhat order?", BRONZE_LIGHT, BRONZE_TEXT),
    ]
    for cx, cy, title, body, fill, edge in quads:
        box(ax, cx - 20, cy - 12.5, 40, 25, fill, edge=edge, r=1.8)
        txt(ax, cx, cy + 8, title, size=6.2, color=edge, weight="bold")
        txt(ax, cx, cy - 2.5, body, size=6.5, color=INK)

    for sx, sy, ex, ey in ((44, 64.5, 35.0, 61.0), (56, 64.5, 65.0, 61.0),
                           (44, 37.5, 35.0, 41.0), (56, 37.5, 65.0, 41.0)):
        arrow(ax, (sx, sy), (ex, ey), color=GREY, lw=0.8)

    txt(ax, 50, 4.5, "A theory that cannot answer all four is a vocabulary, not a treatment.",
        size=6.3, color=GREY, style="italic")
    save(fig, "fig-01-01.png")


def fig_01_02():
    """Common factors and specific ingredients: where outcome variance sits."""
    fig, ax = canvas(4.6, 2.9)
    txt(ax, 50, 93, "WHAT ACCOUNTS FOR OUTCOME IN PSYCHOTHERAPY", size=7.0,
        color=BRONZE_TEXT, weight="bold")
    ax.plot([30, 70], [89, 89], color=BRONZE, lw=1.1, zorder=3)

    bars = [
        ("Extratherapeutic\nchange", 40, TEAL, "events in the child's life,\nnot caused by therapy"),
        ("Relationship\nand expectation", 30, "#2E6E7E", "alliance, empathy, goals,\nhope, credibility"),
        ("Placebo,\nhope, expectancy", 15, BRONZE_TEXT, "the ritual of being treated"),
        ("Model-specific\ntechnique", 15, "#B08954", "the ingredient the theory\nclaims as its own"),
    ]
    left, y0, bh = 8, 46, 13
    for label, pct, colour, note in bars:
        w = pct * 0.84
        box(ax, left, y0, w, bh, colour, r=0.8)
        txt(ax, left + w / 2, y0 + bh / 2, f"{pct}%", size=7.4, color=WHITE, weight="bold")
        left += w
    txt(ax, 50, 40.5, "APPROXIMATE SHARE OF VARIANCE IN OUTCOME", size=5.9, color=GREY,
        weight="bold")

    legend = [
        (12, 26, "extratherapeutic", TEAL),
        (36, 26, "relationship", "#2E6E7E"),
        (60, 26, "expectancy", BRONZE_TEXT),
        (84, 26, "technique", "#B08954"),
    ]
    for lx, ly, lab, colour in legend:
        box(ax, lx - 5, ly - 2.2, 10, 4.4, colour, r=0.6)
        txt(ax, lx, ly - 7.5, lab, size=6.0, color=INK)

    txt(ax, 50, 8.5, "Schematic, after Lambert (1992) and Frank and Frank (1991). Percentages are\n"
                     "illustrative of the argument, not a measurement, and are contested.",
        size=5.9, color=GREY, style="italic")
    save(fig, "fig-01-02.png")


def fig_01_03():
    """The theory-comparison grid the student keeps."""
    fig, ax = canvas(4.6, 3.0)
    txt(ax, 50, 96, "THE THEORY-COMPARISON GRID", size=7.0, color=BRONZE_TEXT, weight="bold")
    ax.plot([36, 64], [92.5, 92.5], color=BRONZE, lw=1.1, zorder=3)

    rows = ["View of the child", "Theory of the problem", "Mechanism of change",
            "Principal methods", "Evidence and limits"]
    cols = ["Psychodynamic", "Behavioural / CBT", "Person-centred", "Systemic"]
    top, bot = 86.0, 22.0
    n = len(rows)
    rh = (top - bot) / n
    label_w = 22.0
    grid_x0 = label_w + 2.0
    cw = (98.0 - grid_x0) / len(cols)

    # row-label column
    box(ax, 2, bot, label_w, top - bot, TEAL_LIGHT, r=1.0)
    for i, r in enumerate(rows):
        y = top - i * rh
        txt(ax, 4, y - rh / 2, r, size=6.1, color=TEAL, weight="bold", ha="left")

    # approach columns
    for j, c in enumerate(cols):
        x = grid_x0 + j * cw
        fill = WHITE if j % 2 == 0 else IVORY
        box(ax, x, bot, cw - 1.4, top - bot, fill, edge="#D8DEDF", r=1.0)
        txt(ax, x + (cw - 1.4) / 2, top + 3.6, c, size=6.1, color=BRONZE_TEXT, weight="bold")
        for i in range(1, n):
            y = top - i * rh
            ax.plot([x, x + cw - 1.4], [y, y], color="#E3E7E8", lw=0.6, zorder=3)

    txt(ax, 50, 9.0, "One row per question, one column per approach; completed by the student\n"
                     "across the programme and reproduced from memory at the end of it.",
        size=5.9, color=GREY, style="italic")
    txt(ax, 50, 4.0, "Cells are left blank by design: the grid is the student's own work.",
        size=5.6, color=GREY, style="italic")
    save(fig, "fig-01-03.png")


REGISTRY = {
    "01": [fig_01_01, fig_01_02, fig_01_03],
}


def main():
    _register_fonts()
    print("Drawing CAC handbook figures ...")
    for fns in REGISTRY.values():
        for fn in fns:
            fn()
    print("Done ->", FIGS)


if __name__ == "__main__":
    main()
