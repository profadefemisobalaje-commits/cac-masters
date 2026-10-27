"""Diagrams for CAC. 702 Adolescent Development (volume 3)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figures as F

OUT = Path(__file__).resolve().parents[1] / "books" / "cac702" / "figures"


# ---------------------------------------------------------------------------
# Week 1 - the widening gap
# ---------------------------------------------------------------------------
def fig_01_01():
    fig, ax = F.canvas(4.6, 2.7)
    ax.set_xlim(1892, 2028)
    ax.set_ylim(2, 30.5)
    F.txt(ax, 1960, 28.5, "THE WIDENING GAP: BIOLOGY EARLIER, ADULTHOOD LATER", size=6.2,
          color=F.BRONZE_TEXT, weight="bold", ha="center")
    d = np.linspace(1900, 2020, 60)
    bio = 16.5 - 4.6 / (1 + np.exp(-(d - 1935) / 12))
    soc = 20.5 + 4.5 / (1 + np.exp(-(d - 1975) / 18))
    ax.fill_between(d, bio, soc, color=F.TEAL_LIGHT, zorder=1)
    ax.plot(d, bio, color=F.TEAL, lw=1.5, zorder=3)
    ax.plot(d, soc, color=F.BRONZE_TEXT, lw=1.5, zorder=3)
    F.txt(ax, 1908, 11.2, "puberty onset (average, girls)", size=5.4, color=F.TEAL, ha="left")
    F.txt(ax, 1908, 22.0, "social adulthood: work, marriage,\nhousehold of one's own", size=5.4,
          color=F.BRONZE_TEXT, ha="left")
    F.txt(ax, 1985, 17.5, "the gap:\nadolescence", size=5.8, color=F.TEAL, weight="bold")
    for w in (1900, 1940, 1980, 2020):
        ax.plot([w, w], [8.6, 9.6], color=F.GREY, lw=0.8, zorder=3)
        F.txt(ax, w, 7.4, str(w), size=5.2, color=F.GREY)
    ax.plot([1900, 2020], [9.6, 9.6], color=F.GREY, lw=0.8, zorder=3)
    F.txt(ax, 1960, 5.0, "Adolescence lengthens from both ends: bodies mature earlier, and the\n"
                         "markers of adulthood recede with schooling and economies.",
          size=5.5, color=F.GREY, style="italic", ha="center")
    F.save(fig, "fig-01-01.png")


# ---------------------------------------------------------------------------
# Week 2 - the axis
# ---------------------------------------------------------------------------
def fig_02_01():
    fig, ax = F.canvas(4.6, 2.7)
    F.txt(ax, 50, 96, "THE AXIS THAT WAKES: HYPOTHALAMUS, PITUITARY, GONADS", size=6.2,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    F.box(ax, 34, 72, 32, 14, F.TEAL, r=1.6)
    F.txt(ax, 50, 79, "HYPOTHALAMUS", size=6.0, color="#F2E3C9", weight="bold")
    F.box(ax, 34, 48, 32, 14, F.TEAL_LIGHT, edge=F.TEAL, r=1.6)
    F.txt(ax, 50, 55, "PITUITARY", size=6.0, color=F.TEAL, weight="bold")
    F.box(ax, 34, 24, 32, 14, F.BRONZE_LIGHT, edge=F.BRONZE_TEXT, r=1.6)
    F.txt(ax, 50, 31, "GONADS / ADRENALS", size=6.0, color=F.BRONZE_TEXT, weight="bold")
    F.arrow(ax, (50, 72), (50, 62), color=F.INK, lw=1.0)
    F.arrow(ax, (50, 48), (50, 38), color=F.INK, lw=1.0)
    F.txt(ax, 56, 67, "GnRH, pulsing first at night", size=5.4, color=F.INK, ha="left")
    F.txt(ax, 56, 43, "LH, FSH", size=5.4, color=F.INK, ha="left")
    ax.plot([34, 22, 22, 34], [31, 31, 79, 79], color=F.GREY, lw=0.9, ls=(0, (3, 2)), zorder=3)
    ax.add_patch(FancyArrowPatch((29, 79), (34, 79), arrowstyle="-|>", mutation_scale=8,
                                 color=F.GREY, lw=0.9, zorder=3))
    F.txt(ax, 20, 55, "feedback:\nthe hormones\nreport back", size=5.3, color=F.GREY,
          style="italic", ha="right")
    F.txt(ax, 50, 10, "Puberty is not one event but a conversation: the brain's pulse pattern\n"
                     "changes first, in sleep, years before anything is visible.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-02-01.png")


# ---------------------------------------------------------------------------
# Week 3 - dual systems
# ---------------------------------------------------------------------------
def fig_03_01():
    fig, ax = F.canvas(4.6, 2.7)
    ax.set_xlim(8, 26)
    ax.set_ylim(-12, 102)
    F.txt(ax, 17, 96, "DUAL SYSTEMS: REWARD RISES FAST, CONTROL RISES SLOW", size=6.2,
          color=F.BRONZE_TEXT, weight="bold", ha="center")
    a = np.linspace(9, 25, 80)
    reward = 20 + 70 * np.exp(-((a - 15.5) ** 2) / 14)
    control = 18 + 2.6 * a
    ax.fill_between(a, np.minimum(reward, control), np.maximum(reward, control),
                    where=(reward > control), color="#F7EDE9", zorder=1)
    ax.plot(a, reward, color="#8C3B2E", lw=1.5, zorder=3)
    ax.plot(a, control, color=F.TEAL, lw=1.5, zorder=3)
    F.txt(ax, 11.6, 92, "reward sensitivity", size=5.5, color="#8C3B2E", ha="left")
    F.txt(ax, 20.8, 90, "cognitive control", size=5.5, color=F.TEAL, ha="left")
    ax.annotate("the gap: the years of\npeak vulnerability - and\nof peak learning", xy=(15.8, 68),
                xytext=(14, 16), fontsize=5.5, color="#8C3B2E", fontstyle="italic",
                arrowprops=dict(arrowstyle="->", lw=0.8, color="#8C3B2E"))
    for w in (10, 14, 18, 22, 25):
        ax.plot([w, w], [2, 4.5], color=F.GREY, lw=0.8, zorder=3)
        F.txt(ax, w, -1.5, str(w), size=5.2, color=F.GREY)
    ax.plot([9, 25], [4.5, 4.5], color=F.GREY, lw=0.8, zorder=3)
    F.txt(ax, 17, -6, "age in years - after Casey, Getz and Galvan (2008) and Steinberg (2008)",
          size=5.4, color=F.GREY, ha="center", style="italic")
    F.save(fig, "fig-03-01.png")


# ---------------------------------------------------------------------------
# Week 4 - hot and cold cognition
# ---------------------------------------------------------------------------
def fig_04_01():
    fig, ax = F.canvas(4.6, 2.6)
    ax.set_xlim(0, 100)
    ax.set_ylim(-4, 102)
    F.txt(ax, 50, 96, "HOT AND COLD: THE SAME MIND IN TWO WEATHERS", size=6.4,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([26, 74], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    groups = [("child\n(10)", 20), ("adolescent\n(15)", 50), ("adult\n(25)", 80)]
    cold = [42, 74, 78]
    hot = [30, 44, 70]
    for (lab, cx), c, h in zip(groups, cold, hot):
        F.box(ax, cx - 12, 20, 10, c * 0.62, F.TEAL_LIGHT, edge=F.TEAL, r=1.0)
        F.box(ax, cx + 2, 20, 10, h * 0.62, "#F7EDE9", edge="#8C3B2E", r=1.0)
        F.txt(ax, cx - 7, 20 + c * 0.62 + 3.5, "cold", size=5.2, color=F.TEAL, weight="bold")
        F.txt(ax, cx + 7, 20 + h * 0.62 + 3.5, "hot", size=5.2, color="#8C3B2E", weight="bold")
        F.txt(ax, cx, 12, lab, size=5.6, color=F.INK)
    F.txt(ax, 50, 5, "Cold: alone, unhurried, no audience. Hot: peers watching, feelings up, now.\n"
                     "The adolescent-adult gap nearly closes in the cold and widens in the heat.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-04-01.png")


# ---------------------------------------------------------------------------
# Week 5 - Marcia's statuses
# ---------------------------------------------------------------------------
def fig_05_01():
    fig, ax = F.canvas(4.6, 2.8)
    F.txt(ax, 50, 96, "IDENTITY STATUSES: EXPLORATION AND COMMITMENT, CROSSED", size=6.2,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    cells = [
        (28, 62, "MORATORIUM", "exploring,\nnot yet committed:\nthe honest crisis", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (72, 62, "ACHIEVEMENT", "explored and\ncommitted: the self\nauthored, not received", F.TEAL_LIGHT, F.TEAL),
        (28, 26, "DIFFUSION", "neither exploring\nnor committed: the\nquestion not yet asked", "#EDEDED", F.GREY),
        (72, 26, "FORECLOSURE", "committed without\nexploring: the self\nreceived, not authored", "#F7EDE9", "#8C3B2E"),
    ]
    for cx, cy, t, b, fill, edge in cells:
        F.box(ax, cx - 20, cy - 14, 40, 28, fill, edge=edge, r=1.4)
        F.txt(ax, cx, cy + 8, t, size=5.6, color=edge, weight="bold")
        F.txt(ax, cx, cy - 4, b, size=5.2, color=F.INK)
    ax.annotate("", xy=(4.5, 74), xytext=(4.5, 14),
                arrowprops=dict(arrowstyle="->", lw=0.9, color=F.GREY), zorder=3)
    ax.text(2.6, 44, "commitment rises upward", fontsize=5.0, color=F.GREY,
            fontweight="bold", ha="center", va="center", rotation=90, zorder=4)
    ax.annotate("", xy=(90, 44), xytext=(10, 44),
                arrowprops=dict(arrowstyle="->", lw=0.9, color=F.GREY), zorder=3)
    F.txt(ax, 50, 46.5, "exploration rises rightward", size=5.0, color=F.GREY, weight="bold")
    F.txt(ax, 50, 8, "Statuses are positions, not traits: the same adolescent is in moratorium\n"
                     "on faith, foreclosure on vocation and achievement on friendship.",
          size=5.5, color=F.GREY, style="italic")
    F.save(fig, "fig-05-01.png")


# ---------------------------------------------------------------------------
# Week 6 - esteem trajectories
# ---------------------------------------------------------------------------
def fig_06_01():
    fig, ax = F.canvas(4.6, 2.6)
    ax.set_xlim(7.7, 19.3)
    ax.set_ylim(-14, 102)
    F.txt(ax, 13.5, 96, "SELF-ESTEEM: THE EARLY-ADOLESCENT DIP AND ITS GAP", size=6.2,
          color=F.BRONZE_TEXT, weight="bold", ha="center")
    a = np.linspace(8, 19, 60)
    boys = 62 - 9 * np.exp(-((a - 12.5) ** 2) / 3.2) + 1.1 * (a - 8)
    girls = 60 - 15 * np.exp(-((a - 12.8) ** 2) / 3.4) + 1.15 * (a - 8)
    ax.plot(a, boys, color=F.TEAL, lw=1.5, zorder=3)
    ax.plot(a, girls, color="#8C3B2E", lw=1.5, zorder=3)
    F.txt(ax, 17.2, boys[-1] + 3, "boys", size=5.5, color=F.TEAL, ha="center")
    F.txt(ax, 17.2, girls[-1] - 5, "girls", size=5.5, color="#8C3B2E", ha="center")
    ax.annotate("the dip: new school, new\nmirrors, puberty's timing", xy=(12.6, 50),
                xytext=(9.2, 26), fontsize=5.5, color=F.GREY, fontstyle="italic",
                arrowprops=dict(arrowstyle="->", lw=0.8, color=F.GREY))
    for w in (8, 10, 12, 14, 16, 18):
        ax.plot([w, w], [3, 5.5], color=F.GREY, lw=0.8, zorder=3)
        F.txt(ax, w, -2, str(w), size=5.2, color=F.GREY)
    ax.plot([8, 19], [5.5, 5.5], color=F.GREY, lw=0.8, zorder=3)
    F.txt(ax, 13.5, -8, "age in years - the pattern, not the level, is the finding",
          size=5.4, color=F.GREY, ha="center", style="italic")
    F.save(fig, "fig-06-01.png")


# ---------------------------------------------------------------------------
# Week 8 - jurisdiction across domains
# ---------------------------------------------------------------------------
def fig_08_01():
    fig, ax = F.canvas(4.6, 2.8)
    F.txt(ax, 50, 96, "WHO DECIDES WHAT: JURISDICTION MOVES, DOMAIN BY DOMAIN", size=6.2,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    rows = [
        ("moral and safety matters", 0.72, 0.20, 0.08),
        ("conventional matters", 0.45, 0.33, 0.22),
        ("personal matters", 0.22, 0.30, 0.48),
    ]
    y = 74
    for lab, par, shared, ado in rows:
        F.txt(ax, 4, y + 9, lab, size=5.6, color=F.INK, ha="left", weight="bold")
        F.box(ax, 10, y, 80 * par, 8, F.TEAL_LIGHT, edge=F.TEAL, r=0.9)
        F.box(ax, 10 + 80 * par, y, 80 * shared, 8, F.BRONZE_LIGHT, edge=F.BRONZE_TEXT, r=0.9)
        F.box(ax, 10 + 80 * (par + shared), y, 80 * ado, 8, "#EDEDED", edge=F.GREY, r=0.9)
        y -= 17
    F.txt(ax, 24, 30, "parent", size=5.4, color=F.TEAL, weight="bold")
    F.txt(ax, 50, 30, "shared", size=5.4, color=F.BRONZE_TEXT, weight="bold")
    F.txt(ax, 76, 30, "adolescent", size=5.4, color=F.GREY, weight="bold")
    F.txt(ax, 50, 18, "Bars read left to right at age fifteen. The developmental work of\n"
                      "adolescence is the movement of these boundaries - fastest in the\n"
                      "personal domain, which is why the fights are about rooms and phones.",
          size=5.5, color=F.GREY, style="italic")
    F.save(fig, "fig-08-01.png")



# ---------------------------------------------------------------------------
# Week 3 (second figure) - the sleep mismatch
# ---------------------------------------------------------------------------
def fig_03_02():
    fig, ax = F.canvas(4.6, 2.6)
    ax.set_xlim(17.2, 39.0)
    ax.set_ylim(-8, 102)
    F.txt(ax, 28, 95, "THREE CLOCKS THAT DO NOT AGREE: THE ADOLESCENT MORNING", size=6.2,
          color=F.BRONZE_TEXT, weight="bold", ha="center")
    bands = [
        ("child's biological sleep", 20.5, 31.0, 66, F.TEAL_LIGHT, F.TEAL),
        ("adolescent's biological sleep", 23.5, 32.0, 48, F.BRONZE_LIGHT, F.BRONZE_TEXT),
        ("the school day", 31.5, 38.0, 30, "#EDEDED", F.GREY),
    ]
    for lab, a, b, y, fill, edge in bands:
        F.txt(ax, 18.4, y + 7.5, lab, size=5.5, color=edge, ha="left", weight="bold")
        F.box(ax, a, y, b - a, 7, fill, edge=edge, r=0.9)
    ax.plot([31.5, 31.5], [26, 76], color="#8C3B2E", lw=1.0, ls=(0, (3, 2)), zorder=4)
    F.txt(ax, 31.9, 80, "07:30 - the bell rings while the\nadolescent body is still asleep",
          size=5.4, color="#8C3B2E", ha="left", style="italic")
    for h, lab in ((18, "18:00"), (22, "22:00"), (26, "02:00"), (30, "06:00"), (34, "10:00"), (38, "14:00")):
        ax.plot([h, h], [12, 14.5], color=F.GREY, lw=0.8, zorder=3)
        F.txt(ax, h, 9.5, lab, size=5.2, color=F.GREY)
    ax.plot([18, 38], [14.5, 14.5], color=F.GREY, lw=0.8, zorder=3)
    F.txt(ax, 28, 1.5, "The phase delay is biological, not behavioural: melatonin onset shifts\n"
                    "later at puberty. Early bells therefore tax the youngest adolescents most.",
          size=5.5, color=F.GREY, style="italic", ha="center")
    F.save(fig, "fig-03-02.png")



# ---------------------------------------------------------------------------
# Week 7 - the internalising gap
# ---------------------------------------------------------------------------
def fig_07_01():
    fig, ax = F.canvas(4.6, 2.6)
    ax.set_xlim(7.7, 19.3)
    ax.set_ylim(-16, 102)
    F.txt(ax, 13.5, 96, "THE INTERNALISING GAP: SAME STORM, TWO WEATHERS", size=6.2,
          color=F.BRONZE_TEXT, weight="bold", ha="center")
    a = np.linspace(8, 19, 60)
    girls = 18 + 62 / (1 + np.exp(-(a - 12.6) / 1.5))
    boys = 16 + 30 / (1 + np.exp(-(a - 13.4) / 2.2))
    ax.fill_between(a, boys, girls, where=(girls > boys), color="#F7EDE9", zorder=1)
    ax.plot(a, girls, color="#8C3B2E", lw=1.5, zorder=3)
    ax.plot(a, boys, color=F.TEAL, lw=1.5, zorder=3)
    F.txt(ax, 17.6, girls[-1] + 2, "girls", size=5.5, color="#8C3B2E", ha="center")
    F.txt(ax, 17.6, boys[-1] - 5, "boys", size=5.5, color=F.TEAL, ha="center")
    ax.annotate("the gap opens with puberty:\nnot a difference in feeling,\nbut in what feeling is\n"
                "allowed to become", xy=(14, 52), xytext=(9.0, 30), fontsize=5.4,
                color="#8C3B2E", fontstyle="italic",
                arrowprops=dict(arrowstyle="->", lw=0.8, color="#8C3B2E"))
    for w in (8, 10, 12, 14, 16, 18):
        ax.plot([w, w], [3, 5.5], color=F.GREY, lw=0.8, zorder=3)
        F.txt(ax, w, -2, str(w), size=5.2, color=F.GREY)
    ax.plot([8, 19], [5.5, 5.5], color=F.GREY, lw=0.8, zorder=3)
    F.txt(ax, 13.5, -8, "age in years - schematic of the cohort pattern (after Hyde,\n"
                          "Mezulis & Abramson, 2008): levels vary by sample; the gap does not",
          size=5.3, color=F.GREY, ha="center", style="italic")
    F.save(fig, "fig-07-01.png")


def main():
    F.set_outdir(OUT)
    for f in (fig_01_01, fig_02_01, fig_03_01, fig_04_01, fig_03_02, fig_05_01, fig_06_01, fig_07_01, fig_08_01):
        f()
    print("Done")


if __name__ == "__main__":
    main()
