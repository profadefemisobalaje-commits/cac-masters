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



# ---------------------------------------------------------------------------
# Week 5 - behavioural: functional analysis and the extinction burst
# ---------------------------------------------------------------------------
def fig_05_01():
    fig, ax = F.canvas(4.6, 2.7)
    F.txt(ax, 50, 95, "FUNCTIONAL ANALYSIS: THE ABC SEQUENCE AND THE LOOP THAT MAINTAINS",
          size=6.2, color=F.BRONZE_TEXT, weight="bold")
    ax.plot([20, 80], [91.5, 91.5], color=F.BRONZE, lw=1.0, zorder=3)
    boxes = [
        (18, 62, "A  ANTECEDENT", "what happens just before:\ntask demand in front of peers", F.TEAL_LIGHT, F.TEAL),
        (50, 62, "B  BEHAVIOUR", "what the child does:\n\"stomach ache\", refusal, escape", F.IVORY, F.GREY),
        (82, 62, "C  CONSEQUENCE", "what follows, reliably:\nsent home; demand removed", F.BRONZE_LIGHT, F.BRONZE_TEXT),
    ]
    for cx, cy, t, b, fill, edge in boxes:
        F.box(ax, cx - 15, cy - 12, 30, 24, fill, edge=edge, r=1.6)
        F.txt(ax, cx, cy + 7.5, t, size=6.0, color=edge, weight="bold")
        F.txt(ax, cx, cy - 3, b, size=5.7, color=F.INK)
    F.arrow(ax, (33, 62), (35, 62), color=F.INK, lw=1.0)
    F.arrow(ax, (65, 62), (67, 62), color=F.INK, lw=1.0)
    F.arrow(ax, (82, 49), (50, 30), color="#8C3B2E", lw=1.1, rad=0.25)
    F.txt(ax, 66, 33, "negative reinforcement:\nrelief strengthens the escape", size=5.6,
          color="#8C3B2E", style="italic")
    F.arrow(ax, (44, 30), (18, 49), color="#8C3B2E", lw=1.1, rad=0.25)
    F.txt(ax, 50, 8, "The loop is the target. Change the consequence and the behaviour has\n"
                    "nothing left to earn - but expect the burst in Figure 5.2 first.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-05-01.png")


def fig_05_02():
    import numpy as np
    fig, ax = F.canvas(4.6, 2.7)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    F.txt(ax, 10, 11.4, "THE EXTINCTION BURST: WHY PROGRAMMES ARE ABANDONED TOO EARLY",
          size=6.2, color=F.BRONZE_TEXT, weight="bold")
    x = np.arange(0, 20, 0.05)
    peak = 8.4
    y = np.where(x < 8, 5.0 + 0.12 * np.sin(x),
                 np.where(x < 10.2, 5.0 + (peak - 5.0) * np.exp(-((x - 10.2) ** 2) / 1.9),
                          0.6 + (peak - 0.6) * np.exp(-(x - 10.2) / 3.0)))
    ax.plot([0, 20], [0.35, 0.35], color=F.GREY, lw=0.7, zorder=2)
    ax.plot([0, 0], [0.35, 10.6], color=F.GREY, lw=0.7, zorder=2)
    ax.plot(x, y, color=F.TEAL, lw=1.6, zorder=4)
    ax.axvline(8, ymin=0.03, ymax=0.88, color=F.BRONZE_TEXT, lw=1.0, ls=(0, (4, 3)), zorder=3)
    F.txt(ax, 8.3, 10.4, "intervention begins", size=5.8, color=F.BRONZE_TEXT, weight="bold", ha="left")
    ax.annotate("the burst: behaviour\ngets worse before better", xy=(10.2, 8.3),
                xytext=(13.2, 9.6), fontsize=5.8, color="#8C3B2E", fontstyle="italic",
                arrowprops=dict(arrowstyle="->", lw=0.8, color="#8C3B2E"))
    ax.annotate("abandonment usually\nhappens here - and teaches\nthe child to escalate", xy=(11.4, 5.6),
                xytext=(12.6, 3.0), fontsize=5.8, color=F.GREY, fontstyle="italic",
                arrowprops=dict(arrowstyle="->", lw=0.8, color=F.GREY))
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color(F.GREY)
    ax.spines["bottom"].set_color(F.GREY)
    F.txt(ax, 0.4, 6.0, "rate of\nbehaviour", size=5.6, color=F.GREY, ha="left")
    F.txt(ax, 19.6, -0.9, "sessions", size=5.6, color=F.GREY, ha="right")
    F.save(fig, "fig-05-02.png")


# ---------------------------------------------------------------------------
# Week 6 - cognitive model and distortions
# ---------------------------------------------------------------------------
def fig_06_01():
    fig, ax = F.canvas(4.6, 2.9)
    F.txt(ax, 50, 96, "THE COGNITIVE MODEL: WHAT A CHILD THINKS SHAPES WHAT A CHILD FEELS AND DOES",
          size=6.0, color=F.BRONZE_TEXT, weight="bold")
    ax.plot([22, 78], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    nodes = [
        (50, 80, "SITUATION", "called to the board\nin mathematics", F.IVORY, F.GREY),
        (82, 52, "THOUGHT", "\"everyone will see\nme freeze\", hot thought", F.TEAL_LIGHT, F.TEAL),
        (50, 24, "BEHAVIOUR", "say \"I feel sick\",\nleave the room", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (18, 52, "FEELING / BODY", "anxiety 8/10,\nheart racing", F.BRONZE_LIGHT, F.BRONZE_TEXT),
    ]
    for cx, cy, t, b, fill, edge in nodes:
        F.box(ax, cx - 15.5, cy - 10, 31, 20, fill, edge=edge, r=1.6)
        F.txt(ax, cx, cy + 5.5, t, size=5.9, color=edge, weight="bold")
        F.txt(ax, cx, cy - 3, b, size=5.6, color=F.INK)
    for p0, p1 in [((62, 74), (72, 62)), ((80, 41), (62, 30)), ((38, 30), (24, 42)), ((22, 62), (38, 74))]:
        F.arrow(ax, p0, p1, color=F.GREY, lw=0.9)
    F.arrow(ax, (34, 52), (66, 52), color="#8C3B2E", lw=1.0, rad=-0.25)
    F.txt(ax, 50, 55.5, "the maintenance shortcut:\nfeeling confirms thought", size=5.5,
          color="#8C3B2E", style="italic")
    F.txt(ax, 50, 6, "Intervention points: test the hot thought (behavioural experiment), or change\n"
                    "the behaviour so the thought can be tested at all.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-06-01.png")


def fig_06_02():
    fig, ax = F.canvas(4.6, 2.7)
    F.txt(ax, 50, 95, "SIX THINKING TRAPS COMMON IN CHILDREN AND ADOLESCENTS", size=6.4,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([26, 74], [91.5, 91.5], color=F.BRONZE, lw=1.0, zorder=3)
    chips = [
        (25, 70, "CATASTROPHISING", "\"if I stutter, my life\nis over\""),
        (50, 70, "MIND-READING", "\"they all think I am\nstupid\""),
        (75, 70, "ALL-OR-NOTHING", "\"one bad mark means\nI am a failure\""),
        (25, 34, "OVERGENERALISING", "\"it always happens,\neverywhere\""),
        (50, 34, "PERSONALISING", "\"mummy is sad because\nof me\""),
        (75, 34, "EMOTIONAL REASONING", "\"I feel guilty, so\nI must have done it\""),
    ]
    for cx, cy, t, b in chips:
        F.box(ax, cx - 12, cy - 11, 24, 22, F.TEAL_LIGHT if cy > 50 else F.BRONZE_LIGHT,
              edge=F.TEAL if cy > 50 else F.BRONZE_TEXT, r=1.4)
        F.txt(ax, cx, cy + 6, t, size=5.4, weight="bold",
              color=F.TEAL if cy > 50 else F.BRONZE_TEXT)
        F.txt(ax, cx, cy - 3, b, size=5.5, color=F.INK)
    F.txt(ax, 50, 7, "Each trap is a hypothesis to test, not a fault to correct: the experiment is\n"
                     "the treatment, and the child designs it with you.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-06-02.png")


# ---------------------------------------------------------------------------
# Week 7 - third wave: psychological flexibility
# ---------------------------------------------------------------------------
def fig_07_01():
    import numpy as np
    fig, ax = F.canvas(4.6, 3.0)
    F.txt(ax, 50, 96, "PSYCHOLOGICAL FLEXIBILITY: THE SIX PROCESSES OF THE THIRD WAVE", size=6.2,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    ax.add_patch(Circle((50, 50), 11, facecolor=F.TEAL, edgecolor="none", zorder=3))
    F.txt(ax, 50, 52, "FLEXIBILITY", size=6.0, color="#F2E3C9", weight="bold")
    F.txt(ax, 50, 46, "not symptom\nremoval", size=5.2, color="#CFE0E4")
    procs = [
        (90, "ACCEPTANCE", "making room for\nfeeling, not war"),
        (30, "DEFUSION", "\"I am having the thought\nthat I am stupid\""),
        (330, "PRESENT MOMENT", "contact with now,\nnot the story of now"),
        (270, "SELF-AS-CONTEXT", "the observing self:\nI am not my thoughts"),
        (210, "VALUES", "what the child cares\nabout, in the child's words"),
        (150, "COMMITTED ACTION", "small steps toward\nthe valued thing"),
    ]
    for a, t, b in procs:
        cx = 50 + 31 * np.cos(np.radians(a))
        cy = 50 + 31 * np.sin(np.radians(a))
        F.box(ax, cx - 14, cy - 9.5, 28, 19, F.TEAL_LIGHT if a > 180 else F.BRONZE_LIGHT,
              edge=F.TEAL if a > 180 else F.BRONZE_TEXT, r=1.5)
        F.txt(ax, cx, cy + 5, t, size=5.2, weight="bold",
              color=F.TEAL if a > 180 else F.BRONZE_TEXT)
        F.txt(ax, cx, cy - 3.5, b, size=5.1, color=F.INK)
        F.arrow(ax, (50 + 13 * np.cos(np.radians(a)), 50 + 13 * np.sin(np.radians(a))),
                (cx - 10 * np.cos(np.radians(a)), cy - 10 * np.sin(np.radians(a))),
                color=F.GREY, lw=0.7)
    F.txt(ax, 50, 4.5, "After Hayes, Strosahl and Wilson (1999). With adolescents the processes are\n"
                       "taught in the adolescent's own language, never in the hexaflex's.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-07-01.png")


# ---------------------------------------------------------------------------
# Week 8 - person-centred conditions
# ---------------------------------------------------------------------------
def fig_08_01():
    fig, ax = F.canvas(4.6, 2.9)
    F.txt(ax, 50, 96, "THE THREE CONDITIONS: NECESSARY AND SUFFICIENT, OR ASPIRATIONAL?",
          size=6.2, color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    ax.add_patch(Circle((42, 58), 20, facecolor=F.TEAL_LIGHT, edgecolor=F.TEAL, lw=1.0, zorder=2))
    ax.add_patch(Circle((58, 58), 20, facecolor=F.BRONZE_LIGHT, edgecolor=F.BRONZE_TEXT, lw=1.0, zorder=2))
    ax.add_patch(Circle((50, 42), 20, facecolor=F.IVORY, edgecolor=F.GREY, lw=1.0, zorder=2))
    F.txt(ax, 34, 68, "CONGRUENCE", size=5.8, color=F.TEAL, weight="bold")
    F.txt(ax, 34, 63, "the adult is real;\nno professional mask", size=5.3, color=F.INK)
    F.txt(ax, 66, 68, "UNCONDITIONAL\nPOSITIVE REGARD", size=5.4, color=F.BRONZE_TEXT, weight="bold")
    F.txt(ax, 66, 58, "prizing the child\nwithout conditions", size=5.3, color=F.INK)
    F.txt(ax, 50, 30, "EMPATHIC UNDERSTANDING", size=5.6, color=F.INK, weight="bold")
    F.txt(ax, 50, 24, "sensing the child's world\nas the child senses it, and\nchecking that you have", size=5.3, color=F.INK)
    F.txt(ax, 50, 52, "the child\nfeels felt", size=5.4, color=F.INK, weight="bold", )
    F.txt(ax, 50, 6, "Rogers claimed the conditions are sufficient for change. With children the\n"
                     "claim needs the parent in the room: conditions for whom?",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-08-01.png")



# ---------------------------------------------------------------------------
# Week 9 - existential givens in adolescent idiom
# ---------------------------------------------------------------------------
def fig_09_01():
    fig, ax = F.canvas(4.6, 2.9)
    F.txt(ax, 50, 96, "THE FOUR GIVENS, IN ADOLESCENT IDIOM", size=6.8,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([32, 68], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    quads = [
        (26, 68, "MORTALITY", "\"people die. I will.\nso what is the rush for?\"", F.TEAL_LIGHT, F.TEAL),
        (74, 68, "FREEDOM", "\nobody is choosing for me\nand that is the terror\"", F.TEAL_LIGHT, F.TEAL),
        (26, 30, "ISOLATION", "\"no one can actually be\ninside my head\"", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (74, 30, "MEANINGLESSNESS", "\"if it all ends, what was\nany of it for?\"", F.BRONZE_LIGHT, F.BRONZE_TEXT),
    ]
    for cx, cy, t, b, fill, edge in quads:
        F.box(ax, cx - 21, cy - 13, 42, 26, fill, edge=edge, r=1.8)
        F.txt(ax, cx, cy + 8, t, size=6.0, color=edge, weight="bold")
        F.txt(ax, cx, cy - 3, b, size=5.8, color=F.INK)
    ax.add_patch(Circle((50, 49), 10.5, facecolor=F.TEAL, edgecolor="none", zorder=3))
    F.txt(ax, 50, 51, "WHO AM I", size=5.8, color="#F2E3C9", weight="bold")
    F.txt(ax, 50, 45.5, "TO BE?", size=5.8, color="#F2E3C9", weight="bold")
    F.txt(ax, 50, 5.5, "The givens are not pathologies. An adolescent meeting them is developing;\n"
                       "an adolescent alone with them is at risk. The work is company, not correction.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-09-01.png")


# ---------------------------------------------------------------------------
# Week 10 - structural family map and circular causality
# ---------------------------------------------------------------------------
def fig_10_01():
    fig, ax = F.canvas(4.6, 3.0)
    F.txt(ax, 50, 96, "A STRUCTURAL FAMILY MAP: BOUNDARIES ARE THE DIAGNOSIS", size=6.4,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    # parental subsystem
    F.box(ax, 14, 66, 34, 20, F.TEAL_LIGHT, edge=F.TEAL, r=1.6)
    F.txt(ax, 31, 80, "PARENTAL SUBSYSTEM", size=5.6, color=F.TEAL, weight="bold")
    F.txt(ax, 23, 72, "mother", size=6.0, color=F.INK)
    F.txt(ax, 39, 72, "father", size=6.0, color=F.GREY)
    ax.plot([26, 36], [69.5, 69.5], color=F.GREY, lw=0.8, ls=(0, (2, 2)), zorder=4)
    # child
    F.box(ax, 58, 66, 26, 20, F.BRONZE_LIGHT, edge=F.BRONZE_TEXT, r=1.6)
    F.txt(ax, 71, 80, "IDENTIFIED child", size=5.6, color=F.BRONZE_TEXT, weight="bold")
    F.txt(ax, 71, 72, "Daniel, 9", size=6.0, color=F.INK)
    # enmeshed dyad mother-child
    ax.plot([40, 62], [62, 62], color="#8C3B2E", lw=2.0, zorder=4)
    ax.plot([40, 62], [60.5, 60.5], color="#8C3B2E", lw=2.0, zorder=4)
    F.txt(ax, 51, 56, "enmeshed: no privacy,\nno separate position", size=5.5, color="#8C3B2E",
          style="italic")
    # disengaged father
    ax.plot([44, 56], [74, 74], color=F.GREY, lw=1.0, ls=(0, (1.5, 2.5)), zorder=4)
    F.txt(ax, 50, 77.5, "disengaged", size=5.5, color=F.GREY, style="italic")
    # school
    F.box(ax, 14, 22, 30, 16, F.IVORY, edge=F.GREY, r=1.6)
    F.txt(ax, 29, 33, "SCHOOL", size=5.6, color=F.GREY, weight="bold")
    F.txt(ax, 29, 27, "informal exemption\nfrom attendance", size=5.5, color=F.INK)
    ax.plot([44, 66], [30, 64], color=F.GREY, lw=0.9, ls=(0, (3, 2)), zorder=3)
    F.txt(ax, 62, 44, "coalition across\ngenerations", size=5.4, color=F.GREY, style="italic")
    # legend
    F.txt(ax, 58, 22, "double line = enmeshed", size=5.3, color=F.INK, ha="left")
    F.txt(ax, 58, 18, "dotted = disengaged", size=5.3, color=F.INK, ha="left")
    F.txt(ax, 58, 14, "dashed = cross-generation coalition", size=5.3, color=F.INK, ha="left")
    F.txt(ax, 50, 6.5, "The symptom sits in the child; the organisation that maintains it does not.\n"
                       "Draw the map before you invite anyone to a session.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-10-01.png")


def fig_10_02():
    fig, ax = F.canvas(4.6, 2.6)
    F.txt(ax, 50, 95, "CIRCULAR CAUSALITY: THE LOOP, NOT THE PERSON, IS THE PROBLEM", size=6.2,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([22, 78], [91.5, 91.5], color=F.BRONZE, lw=1.0, zorder=3)
    nodes = [
        (25, 66, "child withdraws", F.TEAL_LIGHT, F.TEAL),
        (75, 66, "parent presses / worries", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (75, 30, "child withdraws further", F.TEAL_LIGHT, F.TEAL),
        (25, 30, "parent rescues, then reproaches", F.BRONZE_LIGHT, F.BRONZE_TEXT),
    ]
    for cx, cy, t, fill, edge in nodes:
        F.box(ax, cx - 19, cy - 8, 38, 16, fill, edge=edge, r=1.5)
        F.txt(ax, cx, cy, t, size=5.9, color=F.INK)
    for p0, p1 in [((44, 66), (56, 66)), ((75, 58), (75, 38)), ((56, 30), (44, 30)), ((25, 38), (25, 58))]:
        F.arrow(ax, p0, p1, color=F.GREY, lw=1.0)
    F.txt(ax, 50, 48, "each move is a sensible\nresponse to the previous one", size=5.5,
          color=F.GREY, style="italic")
    F.txt(ax, 50, 8, "Linear questions (who started it?) produce blame. Circular questions\n"
                     "(what happens next, and then who notices?) produce the loop.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-10-02.png")


# ---------------------------------------------------------------------------
# Week 11 - scaling and externalisation
# ---------------------------------------------------------------------------
def fig_11_01():
    fig, ax = F.canvas(4.6, 2.5)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    F.txt(ax, 50, 92, "THE SCALING CONVERSATION: SMALL NUMBERS, REAL MOVEMENT", size=6.4,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([26, 74], [88, 88], color=F.BRONZE, lw=1.0, zorder=3)
    ax.plot([8, 92], [50, 50], color=F.INK, lw=1.1, zorder=3)
    for i in range(11):
        x = 8 + i * 8.4
        ax.plot([x, x], [48, 52], color=F.INK, lw=0.7, zorder=3)
        F.txt(ax, x, 42, str(i), size=5.6, color=F.GREY)
    marks = [(2, "the worst\nit got", F.GREY), (4, "today", F.TEAL), (5, "the next\nsmall step", F.BRONZE_TEXT)]
    for v, lab, col in marks:
        x = 8 + v * 8.4
        ax.add_patch(Circle((x, 50), 2.2, facecolor=col, edgecolor="none", zorder=4))
        F.txt(ax, x, 66 if v == 4 else 74, lab, size=5.6, color=col, weight="bold")
        ax.plot([x, x], [52, 62 if v == 4 else 70], color=col, lw=0.7, ls=(0, (2, 2)), zorder=3)
    F.txt(ax, 8, 26, "0 = the worst it has been", size=5.5, color=F.GREY, ha="left")
    F.txt(ax, 92, 26, "10 = the day after the miracle", size=5.5, color=F.GREY, ha="right")
    F.txt(ax, 50, 10, "The question that does the work: \"what told you it was a 4 and not a 3?\"\n"
                      "The child's answer is the intervention, already in the child's words.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-11-01.png")


def fig_11_02():
    fig, ax = F.canvas(4.6, 2.6)
    F.txt(ax, 50, 95, "EXTERNALISATION: THE CHILD AND THE PROBLEM ARE NOT THE SAME THING",
          size=6.0, color=F.BRONZE_TEXT, weight="bold")
    ax.plot([20, 80], [91.5, 91.5], color=F.BRONZE, lw=1.0, zorder=3)
    F.box(ax, 8, 44, 34, 30, F.TEAL_LIGHT, edge=F.TEAL, r=1.8)
    F.txt(ax, 25, 66, "THE CHILD", size=6.4, color=F.TEAL, weight="bold")
    F.txt(ax, 25, 57, "skills, loyalties, jokes,\nfears, friends, a history\nof getting through things", size=5.6, color=F.INK)
    F.box(ax, 58, 44, 34, 30, "#F7EDE9", edge="#8C3B2E", r=1.8)
    F.txt(ax, 75, 66, "THE PROBLEM", size=6.4, color="#8C3B2E", weight="bold")
    F.txt(ax, 75, 57, "\"the Worry\" - its tricks,\nits favourite times,\nwhat it wants her to do", size=5.6, color=F.INK)
    F.arrow(ax, (42, 59), (58, 59), color=F.GREY, lw=1.0)
    F.txt(ax, 50, 63, "relationship:\ninvited, resisted,\noutwitted", size=5.4, color=F.GREY, style="italic")
    F.box(ax, 25, 12, 50, 16, F.IVORY, edge=F.GREY, r=1.6)
    F.txt(ax, 50, 24, "THE AUDIENCE", size=5.8, color=F.GREY, weight="bold")
    F.txt(ax, 50, 17, "who needs to know that the child outwitted the Worry this week?", size=5.5, color=F.INK)
    F.arrow(ax, (50, 44), (50, 28), color=F.GREY, lw=0.9)
    F.txt(ax, 50, 4, "Externalising is not evasion of responsibility: it is the position from which\n"
                    "responsibility becomes possible.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-11-02.png")


# ---------------------------------------------------------------------------
# Week 12 - cultural formulation
# ---------------------------------------------------------------------------
def fig_12_01():
    fig, ax = F.canvas(4.6, 3.0)
    F.txt(ax, 50, 96, "CULTURAL FORMULATION: FOUR QUESTIONS BEFORE ANY DIAGNOSIS", size=6.2,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    quads = [
        (26, 68, "IDENTITY & LANGUAGE", "who is this child among\ntheir people? in which\nlanguage do they hurt?", F.TEAL_LIGHT, F.TEAL),
        (74, 68, "CONCEPTS OF DISTRESS", "what is this called at\nhome? what does the\nfamily fear it means?", F.TEAL_LIGHT, F.TEAL),
        (26, 30, "STRESSORS & SUPPORTS", "what is pressing, and\nwho and what holds\nthis child up?", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (74, 30, "THE RELATIONSHIP", "what am I to this child?\nwhat does my skin, accent\nand office say first?", F.BRONZE_LIGHT, F.BRONZE_TEXT),
    ]
    for cx, cy, t, b, fill, edge in quads:
        F.box(ax, cx - 21, cy - 13, 42, 26, fill, edge=edge, r=1.8)
        F.txt(ax, cx, cy + 8.5, t, size=5.8, color=edge, weight="bold")
        F.txt(ax, cx, cy - 3, b, size=5.6, color=F.INK)
    ax.add_patch(Circle((50, 49), 10, facecolor=F.TEAL, edgecolor="none", zorder=3))
    F.txt(ax, 50, 51, "THE CHILD", size=5.6, color="#F2E3C9", weight="bold")
    F.txt(ax, 50, 45.5, "IN CONTEXT", size=5.6, color="#F2E3C9", weight="bold")
    F.txt(ax, 50, 5.5, "After the cultural formulation interview structure. The fourth quadrant is the\n"
                       "one practitioners skip, and the one the child experiences first.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-12-01.png")


def main():
    F._register_fonts()
    F.set_outdir(OUT)
    print(f"Drawing CAC.701 figures -> {OUT}")
    for fn in (F.fig_01_01, F.fig_01_02, F.fig_01_03,
               fig_02_01, fig_02_02, fig_03_01, fig_03_02, fig_04_01,
               fig_05_01, fig_05_02, fig_06_01, fig_06_02, fig_07_01, fig_08_01,
               fig_09_01, fig_10_01, fig_10_02, fig_11_01, fig_11_02, fig_12_01):
        fn()
    print("Done")


if __name__ == "__main__":
    main()
