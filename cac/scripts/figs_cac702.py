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



# ---------------------------------------------------------------------------
# Week 9 - the peer world, inward
# ---------------------------------------------------------------------------
def fig_09_01():
    fig, ax = F.canvas(4.6, 2.8)
    ax.set_xlim(0, 100)
    ax.set_ylim(-8, 102)
    F.txt(ax, 50, 96, "THE PEER WORLD, INWARD: CROWD, CLIQUE, FRIENDSHIP, ROMANCE",
          size=6.0, color=F.BRONZE_TEXT, weight="bold")
    ax.plot([22, 78], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    F.box(ax, 6, 16, 88, 68, "#F2F2F2", edge=F.GREY, r=1.6)
    F.txt(ax, 9, 80, "the crowd: a label and a reputation - loose, public, useful",
          size=5.2, color=F.GREY, ha="left", weight="bold")
    F.box(ax, 14, 24, 72, 50, F.TEAL_LIGHT, edge=F.TEAL, r=1.4)
    F.txt(ax, 17, 70, "the clique: three to nine, chosen, daily", size=5.2,
          color=F.TEAL, ha="left", weight="bold")
    F.box(ax, 24, 32, 52, 34, F.BRONZE_LIGHT, edge=F.BRONZE_TEXT, r=1.2)
    F.txt(ax, 27, 62, "the friendship: two, disclosed, tested", size=5.2,
          color=F.BRONZE_TEXT, ha="left", weight="bold")
    F.box(ax, 34, 40, 32, 18, "#F7EDE9", edge="#8C3B2E", r=1.0)
    F.txt(ax, 50, 49, "romance: two, time,\nbody, risk", size=5.2, color="#8C3B2E", weight="bold")
    F.txt(ax, 50, 6, "Intimacy and risk both deepen toward the centre: the dyad carries\n"
                    "the disclosure - and the heartbreak, and the coercion when it comes.",
          size=5.4, color=F.GREY, style="italic")
    F.save(fig, "fig-09-01.png")


# ---------------------------------------------------------------------------
# Week 10 - Super's stages
# ---------------------------------------------------------------------------
def fig_10_01():
    fig, ax = F.canvas(4.6, 2.6)
    ax.set_xlim(0, 100)
    ax.set_ylim(-10, 102)
    F.txt(ax, 50, 96, "WORK, SCHOOL AND THE LONG HORIZON: SUPER'S STAGES", size=6.2,
          color=F.BRONZE_TEXT, weight="bold")
    F.box(ax, 4, 52, 30, 16, F.TEAL_LIGHT, edge=F.TEAL, r=1.0)
    F.txt(ax, 19, 63, "growth", size=5.6, color=F.TEAL, weight="bold")
    F.txt(ax, 19, 57, "fantasy, interest, capacity", size=4.8, color=F.INK)
    F.box(ax, 34, 52, 32, 16, F.BRONZE_LIGHT, edge=F.BRONZE_TEXT, r=1.0)
    F.txt(ax, 50, 63, "exploration", size=5.6, color=F.BRONZE_TEXT, weight="bold")
    F.txt(ax, 50, 57, "tentative, transition, trial", size=4.8, color=F.INK)
    F.box(ax, 66, 52, 30, 16, "#EDEDED", edge=F.GREY, r=1.0)
    F.txt(ax, 81, 63, "establishment", size=5.6, color=F.GREY, weight="bold")
    F.txt(ax, 81, 57, "the decades after school", size=4.8, color=F.INK)
    F.txt(ax, 19, 46, "childhood", size=5.2, color=F.GREY)
    F.txt(ax, 50, 46, "adolescence and\nemerging adulthood", size=5.2, color=F.GREY)
    F.txt(ax, 81, 46, "adulthood", size=5.2, color=F.GREY)
    ax.annotate("", xy=(96, 36), xytext=(4, 36),
                arrowprops=dict(arrowstyle="->", lw=0.9, color=F.GREY), zorder=3)
    ax.plot([44, 44], [24, 74], color="#8C3B2E", lw=1.0, ls=(0, (3, 2)), zorder=4)
    F.txt(ax, 44, 82, "the adolescent: exploration's first trials -\n"
                     "real choices made before the self is settled", size=5.4,
          color="#8C3B2E", style="italic")
    F.txt(ax, 50, 4, "Super's stages are tasks, not ages: schooling, work and economies move\n"
                    "the boundaries - the sequence holds.", size=5.4, color=F.GREY, style="italic")
    F.save(fig, "fig-10-01.png")


# ---------------------------------------------------------------------------
# Week 11 - the five Cs
# ---------------------------------------------------------------------------
def fig_11_01():
    fig, ax = F.canvas(4.6, 2.8)
    ax.set_xlim(0, 100)
    ax.set_ylim(-8, 102)
    F.txt(ax, 50, 96, "POSITIVE YOUTH DEVELOPMENT: THE FIVE Cs AND THE SIXTH",
          size=6.2, color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    cs = [
        (50, 76, "competence", "skill in valued domains", F.TEAL_LIGHT, F.TEAL),
        (78, 60, "confidence", "worth that survives scores", F.TEAL_LIGHT, F.TEAL),
        (68, 30, "connection", "bonds that hold", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (32, 30, "character", "rules that travel", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (22, 60, "caring", "sympathy in action", "#F7EDE9", "#8C3B2E"),
    ]
    for cx, cy, t, b, fill, edge in cs:
        ax.plot([cx, 50], [cy, 52], color=F.GREY, lw=0.7, zorder=2)
    for cx, cy, t, b, fill, edge in cs:
        F.box(ax, cx - 13, cy - 8, 26, 16, fill, edge=edge, r=1.2)
        F.txt(ax, cx, cy + 3, t, size=5.4, color=edge, weight="bold")
        F.txt(ax, cx, cy - 3, b, size=4.6, color=F.INK)
    F.box(ax, 38, 45, 24, 14, "#FFFFFF", edge=F.INK, r=1.0)
    F.txt(ax, 50, 52, "contribution:\nthe sixth C, outward", size=5.0, color=F.INK, weight="bold")
    F.txt(ax, 50, 6, "The five Cs are not traits to install but products of good settings: programmes\n"
                    "that supply all five move contribution - the sixth C - outward.",
          size=5.4, color=F.GREY, style="italic")
    F.save(fig, "fig-11-01.png")


# ---------------------------------------------------------------------------
# Week 12 - one biology, many clocks
# ---------------------------------------------------------------------------
def fig_12_01():
    fig, ax = F.canvas(4.6, 2.8)
    ax.set_xlim(0, 100)
    ax.set_ylim(-8, 102)
    F.txt(ax, 50, 96, "ONE BIOLOGY, MANY CLOCKS: ADOLESCENCE WORLDWIDE", size=6.2,
          color=F.BRONZE_TEXT, weight="bold")
    cols = [
        (4, "high-income settings", "school to 18 and beyond;\nmarriage late; a long\nmoratorium; the risks:\ninternalising, screens, drift", F.TEAL_LIGHT, F.TEAL),
        (36, "low- and middle-income", "work and marriage arrive\nearly for many; girls'\nschooling the strongest\nprotection; child marriage\npersists where poverty does", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (68, "humanitarian settings", "transitions broken: school,\nhome and clinic lost\ntogether; belonging rebuilt\nfrom nothing; the adolescent\nas carer and earner", "#EDEDED", F.GREY),
    ]
    for x, h, b, fill, edge in cols:
        F.txt(ax, x + 14, 86, h, size=5.6, color=edge, weight="bold")
        F.box(ax, x, 26, 28, 54, fill, edge=edge, r=1.2)
        F.txt(ax, x + 14, 60, b, size=4.9, color=F.INK)
    F.txt(ax, 50, 12, "same puberty, same pruning, same absence of universal storm - different clocks",
          size=5.4, color=F.GREY, style="italic")
    F.txt(ax, 50, 4, "The social clock decides what the biological clock will mean.", size=5.4,
          color=F.GREY, style="italic")
    F.save(fig, "fig-12-01.png")


# ---------------------------------------------------------------------------
# Week 13 - the onset curve
# ---------------------------------------------------------------------------
def fig_13_01():
    fig, ax = F.canvas(4.6, 2.6)
    ax.set_xlim(-2, 72)
    ax.set_ylim(-16, 104)
    F.txt(ax, 35, 98, "MOST DISORDERS BEGIN EARLY: THE CUMULATIVE ONSET CURVE",
          size=6.0, color=F.BRONZE_TEXT, weight="bold")
    ax.fill_between([10, 19], 0, 104, color=F.BRONZE_LIGHT, zorder=1)
    F.txt(ax, 14.5, 90, "adolescence", size=5.2, color=F.BRONZE_TEXT, weight="bold")
    a = np.linspace(0, 70, 80)
    c = 84 / (1 + np.exp(-(a - 15) / 6))
    ax.plot(a, c, color="#8C3B2E", lw=1.6, zorder=3)
    for x, lab in ((15, "half of lifetime onset\nby the mid-teens"),
                   (22, "three quarters\nby the mid-twenties")):
        y = 84 / (1 + np.exp(-(x - 15) / 6))
        ax.plot([x, x], [4, y], color=F.GREY, lw=0.8, ls=(0, (3, 2)), zorder=2)
        F.txt(ax, x - 1.2, y + 5, lab, size=5.0, color=F.GREY, ha="right", style="italic")
    for w in (0, 10, 20, 30, 40, 50, 60):
        ax.plot([w, w], [1.5, 4], color=F.GREY, lw=0.8, zorder=3)
        F.txt(ax, w, -3, str(w), size=5.0, color=F.GREY)
    ax.plot([0, 70], [4, 4], color=F.GREY, lw=0.8, zorder=3)
    F.txt(ax, 40, -9, "age in years - schematic after Kessler et al. (2005): the onset distribution\n"
                      "is why adolescent services are prevention, not merely treatment",
          size=5.2, color=F.GREY, ha="center", style="italic")
    F.save(fig, "fig-13-01.png")


# ---------------------------------------------------------------------------
# Week 14 - the confidentiality circle
# ---------------------------------------------------------------------------
def fig_14_01():
    fig, ax = F.canvas(4.6, 2.8)
    ax.set_xlim(0, 100)
    ax.set_ylim(-8, 102)
    F.txt(ax, 50, 96, "WHAT STAYS, WHAT TRAVELS: THE CONFIDENTIALITY CIRCLE",
          size=6.0, color=F.BRONZE_TEXT, weight="bold")
    F.box(ax, 6, 18, 88, 70, "#F2F2F2", edge=F.GREY, r=1.6)
    F.txt(ax, 50, 83, "must travel: risk to life or to others - said to the child first,\n"
                      "then shared, with the child accompanied", size=5.2, color=F.GREY, weight="bold")
    F.box(ax, 16, 28, 68, 48, F.BRONZE_LIGHT, edge=F.BRONZE_TEXT, r=1.4)
    F.txt(ax, 50, 71, "travels with the child's knowledge: the planned\nfamily conversation, the referral, the report",
          size=5.2, color=F.BRONZE_TEXT, weight="bold")
    F.box(ax, 30, 38, 40, 26, F.TEAL_LIGHT, edge=F.TEAL, r=1.2)
    F.txt(ax, 50, 54, "kept: the child's words -\nthe ordinary rule of the room", size=5.2,
          color=F.TEAL, weight="bold")
    F.txt(ax, 50, 6, "Gillick competence asks whether this child understands this decision -\n"
                    "not whether children in general may decide.", size=5.4, color=F.GREY, style="italic")
    F.save(fig, "fig-14-01.png")


# ---------------------------------------------------------------------------
# Week 15 - the practicum gradient
# ---------------------------------------------------------------------------
def fig_15_01():
    fig, ax = F.canvas(4.6, 2.8)
    ax.set_xlim(0, 100)
    ax.set_ylim(-8, 102)
    F.txt(ax, 50, 96, "ONE METHOD, THREE REGISTERS: THE PRACTICUM GRADIENT", size=6.2,
          color=F.BRONZE_TEXT, weight="bold")
    cols = [
        (4, "age 13", "concrete, short,\nside-by-side, doing;\nthe draw and the walk;\nconsent: the guardian\nplus the child's assent", F.TEAL_LIGHT, F.TEAL),
        (36, "age 15", "the peer register:\nloyalty first, then the\nworry; hot and cold\nsequencing; the card\nin the pocket", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (68, "age 17", "the adult register:\ntheir agenda, their\nwords, their plan; your\nquestions last; consent\ntheir own", "#EDEDED", F.GREY),
    ]
    for x, h, b, fill, edge in cols:
        F.txt(ax, x + 14, 86, h, size=5.8, color=edge, weight="bold")
        F.box(ax, x, 32, 28, 48, fill, edge=edge, r=1.2)
        F.txt(ax, x + 14, 66, b, size=5.0, color=F.INK)
    ax.annotate("", xy=(94, 24), xytext=(6, 24),
                arrowprops=dict(arrowstyle="->", lw=0.9, color=F.GREY), zorder=3)
    F.txt(ax, 50, 16, "concrete and accompanied  -  abstract and autonomous", size=5.2,
          color=F.GREY, weight="bold")
    F.txt(ax, 50, 5, "The method does not change; the register does. What fails at thirteen\n"
                    "is not the therapy but the grammar.", size=5.4, color=F.GREY, style="italic")
    F.save(fig, "fig-15-01.png")


# ---------------------------------------------------------------------------
# Week 16 - the semester in four strands
# ---------------------------------------------------------------------------
def fig_16_01():
    fig, ax = F.canvas(4.6, 2.8)
    ax.set_xlim(0, 100)
    ax.set_ylim(-8, 102)
    F.txt(ax, 50, 96, "THE SEMESTER IN FOUR STRANDS", size=6.4, color=F.BRONZE_TEXT, weight="bold")
    ax.plot([30, 70], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    lanes = [
        (74, "the body and the brain", [1, 2, 3], F.TEAL_LIGHT, F.TEAL),
        (56, "the self and its weather", [4, 5, 6, 7], F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (38, "relationships and contexts", [8, 9, 10, 11, 12], "#EDEDED", F.GREY),
        (20, "practice and integration", [13, 14, 15, 16], "#F7EDE9", "#8C3B2E"),
    ]
    x0, w = 26, 70 / 16
    for y, lab, weeks, fill, edge in lanes:
        F.txt(ax, 3, y + 6, lab, size=5.2, color=edge, ha="left", weight="bold")
        for i in range(16):
            n = i + 1
            f = fill if n in weeks else "#FAFAFA"
            e = edge if n in weeks else "#E4E4E4"
            F.box(ax, x0 + i * w, y, w - 0.5, 12, f, edge=e, r=0.6)
            if n in weeks:
                F.txt(ax, x0 + i * w + (w - 0.5) / 2, y + 6, str(n), size=4.6, color=F.INK)
    F.txt(ax, 50, 6, "Weeks 15 and 16 gather all four strands: the practicum panel and the\n"
                    "examination assume every lane at once.", size=5.4, color=F.GREY, style="italic")
    F.save(fig, "fig-16-01.png")


def main():
    F.set_outdir(OUT)
    for f in (fig_01_01, fig_02_01, fig_03_01, fig_04_01, fig_03_02, fig_05_01, fig_06_01, fig_07_01, fig_08_01,
             fig_09_01, fig_10_01, fig_11_01, fig_12_01, fig_13_01, fig_14_01,
             fig_15_01, fig_16_01):
        f()
    print("Done")


if __name__ == "__main__":
    main()
