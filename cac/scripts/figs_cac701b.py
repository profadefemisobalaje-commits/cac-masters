"""Diagrams for CAC. 701 Child Development Theories (volume 2)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figures as F
from matplotlib.patches import Circle

OUT = Path(__file__).resolve().parents[1] / "books" / "cac701b" / "figures"


# ---------------------------------------------------------------------------
# Week 1 - the ecology of development
# ---------------------------------------------------------------------------
def fig_01_01():
    fig, ax = F.canvas(4.6, 3.1)
    F.txt(ax, 50, 96, "THE CHILD IN CONTEXT: DEVELOPMENT HAS AN ADDRESS", size=6.4,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([26, 74], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    cx, cy = 50, 48
    rings = [
        (38, "#EDF2F3", "MACROSYSTEM: culture, law, economy, belief"),
        (29, "#E2EBEC", "EXOSYSTEM: parent's work, school board, church"),
        (20, "#D5E3E5", "MESOSYSTEM: home-school-clinic links"),
        (11, F.TEAL_LIGHT, "MICROSYSTEM: family, class, peers"),
    ]
    for r, fill, _ in rings:
        ax.add_patch(Circle((cx, cy), r, facecolor=fill, edgecolor="#B9C8CA",
                            linewidth=0.8, zorder=1))
    ax.add_patch(Circle((cx, cy), 5.5, facecolor=F.TEAL, edgecolor="none", zorder=2))
    F.txt(ax, cx, cy, "THE\nCHILD", size=5.6, color="#F2E3C9", weight="bold", zorder=4)
    F.txt(ax, cx, cy + 15.5, "microsystem", size=5.4, color=F.TEAL, weight="bold")
    F.txt(ax, cx, cy + 24.5, "mesosystem", size=5.4, color=F.TEAL, weight="bold")
    F.txt(ax, cx, cy + 33.5, "exosystem", size=5.4, color=F.GREY, weight="bold")
    F.txt(ax, cx, cy + 42, "MACROSYSTEM: culture, law, economy, belief", size=5.6,
          color=F.GREY, weight="bold")
    F.txt(ax, 6, 6, "chronosystem: the dimension of time - the move, the war, the pandemic,\n"
                    "the year the family's income stopped. After Bronfenbrenner (1979).",
          size=5.5, color=F.GREY, style="italic", ha="left")
    F.save(fig, "fig-01-01.png")


# ---------------------------------------------------------------------------
# Week 2 - prenatal timeline and teratogen sensitivity
# ---------------------------------------------------------------------------
def fig_02_01():
    fig, ax = F.canvas(4.6, 2.8)
    ax.set_xlim(-1, 41)
    ax.set_ylim(0, 100)
    F.txt(ax, 20, 95, "BEFORE BIRTH: STAGES AND WINDOWS OF SENSITIVITY", size=6.4,
          color=F.BRONZE_TEXT, weight="bold", ha="center")
    ax.plot([6, 34], [91, 91], color=F.BRONZE, lw=1.0, zorder=3)
    stages = [(0, 2, "germinal", F.TEAL_LIGHT, F.TEAL),
              (2, 8, "embryonic", F.BRONZE_LIGHT, F.BRONZE_TEXT),
              (8, 38, "fetal", "#E7EDEE", F.GREY)]
    for a, b, name, fill, edge in stages:
        F.box(ax, a, 76, b - a, 10, fill, edge=edge, r=1.2)
    F.txt(ax, 20, 70.5, "germinal 0-2 wks   ·   embryonic 2-8 wks   ·   fetal 8-38 wks",
          size=5.6, color=F.INK, weight="bold", ha="center")
    organs = [
        ("brain", 3, 16, 38, "#8C3B2E"),
        ("heart", 3, 6, None, "#8C3B2E"),
        ("arms and legs", 4, 8, None, F.BRONZE_TEXT),
        ("eyes", 4, 8, None, F.BRONZE_TEXT),
        ("teeth", 6, 10, None, F.GREY),
    ]
    y = 66
    for name, a, b, ext, col in organs:
        F.txt(ax, 2.6, y + 2.2, name, size=5.4, color=F.INK, ha="right")
        F.box(ax, a, y, b - a, 4.4, col, r=0.8)
        if ext:
            F.box(ax, b, y, ext - b, 4.4, "#D9A79B", r=0.8)
        y -= 9
    for w in (0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40):
        ax.plot([w, w], [12, 14.5], color=F.GREY, lw=0.8, zorder=3)
        F.txt(ax, w, 8.5, str(w), size=5.2, color=F.GREY)
    ax.plot([0, 40], [14.5, 14.5], color=F.GREY, lw=0.8, zorder=3)
    F.txt(ax, 20, 3.5, "weeks from conception - solid bar: greatest sensitivity; "
                       "pale extension (brain): sensitivity continues",
          size=5.4, color=F.GREY, ha="center", style="italic")
    F.save(fig, "fig-02-01.png")


# ---------------------------------------------------------------------------
# Week 3 - Piaget's staircase
# ---------------------------------------------------------------------------
def fig_03_01():
    fig, ax = F.canvas(4.6, 2.9)
    F.txt(ax, 50, 96, "PIAGET: KNOWLEDGE IS BUILT, STAIR BY STAIR", size=6.4,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([28, 72], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    steps = [
        (6, 12, "SENSORIMOTOR\n0-2 yrs", "object permanence;\nlearning by acting", F.TEAL_LIGHT, F.TEAL),
        (29, 30, "PREOPERATIONAL\n2-7 yrs", "symbol and pretend play;\ncentration, egocentrism", F.TEAL_LIGHT, F.TEAL),
        (52, 48, "CONCRETE OPERATIONAL\n7-11 yrs", "conservation, reversibility;\nlogic tied to the tangible", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        (75, 66, "FORMAL OPERATIONAL\n11 yrs +", "hypothetical-deductive\nreasoning; ideals", F.BRONZE_LIGHT, F.BRONZE_TEXT),
    ]
    for x, y, t, b, fill, edge in steps:
        F.box(ax, x, y, 21, 20, fill, edge=edge, r=1.4)
        F.txt(ax, x + 10.5, y + 15, t, size=5.2, color=edge, weight="bold")
        F.txt(ax, x + 10.5, y + 7, b, size=5.0, color=F.INK)
    F.txt(ax, 50, 6, "The stairs are an idealisation: children reason above the step on familiar\n"
                     "material and below it on strange material (horizontal decalage).",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-03-01.png")


# ---------------------------------------------------------------------------
# Week 4 - the zone of proximal development
# ---------------------------------------------------------------------------
def fig_04_01():
    fig, ax = F.canvas(4.6, 2.7)
    F.txt(ax, 50, 96, "THE ZONE OF PROXIMAL DEVELOPMENT: WHAT ASSESSMENT MISSES", size=6.2,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    cx, cy = 50, 47
    ax.add_patch(Circle((cx, cy), 33, facecolor="#EDF2F3", edgecolor="#B9C8CA", lw=0.8, zorder=1))
    ax.add_patch(Circle((cx, cy), 22, facecolor=F.BRONZE_LIGHT, edgecolor=F.BRONZE, lw=0.9, zorder=1))
    ax.add_patch(Circle((cx, cy), 11, facecolor=F.TEAL_LIGHT, edgecolor=F.TEAL, lw=0.9, zorder=1))
    F.txt(ax, cx, cy + 2, "what the child\ndoes alone", size=5.6, color=F.TEAL, weight="bold")
    F.txt(ax, cx, cy + 16.5, "the zone: what the child does\nwith a scaffolded partner", size=5.6,
          color=F.BRONZE_TEXT, weight="bold")
    F.txt(ax, cx, cy + 27.5, "not yet, even with help", size=5.5, color=F.GREY, weight="bold")
    F.txt(ax, 50, 6, "Testing alone measures yesterday's development; testing with help measures\n"
                     "tomorrow's. Teach into the zone, then withdraw the scaffold step by step.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-04-01.png")


# ---------------------------------------------------------------------------
# Week 5 - executive function and theory of mind
# ---------------------------------------------------------------------------
def fig_05_01():
    fig, ax = F.canvas(4.6, 3.0)
    F.txt(ax, 50, 97, "EXECUTIVE FUNCTION AND THE DISCOVERY OF OTHER MINDS", size=6.2,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([24, 76], [93.5, 93.5], color=F.BRONZE, lw=1.0, zorder=3)
    comps = [
        (18, "INHIBITORY\nCONTROL", "stopping the\nprepotent response", F.TEAL_LIGHT, F.TEAL),
        (50, "WORKING\nMEMORY", "holding and using\ninformation in mind", F.TEAL_LIGHT, F.TEAL),
        (82, "COGNITIVE\nFLEXIBILITY", "shifting set;\nseeing the other way", F.BRONZE_LIGHT, F.BRONZE_TEXT),
    ]
    for cx, t, b, fill, edge in comps:
        F.box(ax, cx - 14, 66, 28, 22, fill, edge=edge, r=1.4)
        F.txt(ax, cx, 82, t, size=5.4, color=edge, weight="bold")
        F.txt(ax, cx, 72, b, size=5.2, color=F.INK)
        F.arrow(ax, (cx, 66), (50 + (cx - 50) * 0.3, 58), color=F.GREY, lw=0.8)
    F.box(ax, 22, 46, 56, 12, F.TEAL, r=1.6)
    F.txt(ax, 50, 52, "EXECUTIVE FUNCTION: the air-traffic control of the classroom", size=5.8,
          color="#F2E3C9", weight="bold")
    ax.plot([8, 92], [36, 36], color=F.GREY, lw=0.8, zorder=3)
    ages = [(12, "2 yrs", "desire psychology:\n\"she wants\""),
            (33, "3 yrs", "belief talk, but false\nbelief still fails"),
            (56, "4-5 yrs", "false belief passes:\nmind represents, not copies"),
            (80, "6-8 yrs", "second-order belief:\n\"he thinks that she thinks\"")]
    for x, a, b in ages:
        ax.plot([x, x], [34.5, 37.5], color=F.GREY, lw=0.8, zorder=3)
        F.txt(ax, x, 31.5, a, size=5.4, color=F.GREY, weight="bold")
        F.txt(ax, x, 24, b, size=5.2, color=F.INK)
    F.txt(ax, 50, 12, "theory-of-mind timeline (after Wellman, Cross & Watson, 2001):\n"
                      "language, siblings and conversation shift the timing by months, not stages",
          size=5.5, color=F.GREY, style="italic")
    F.save(fig, "fig-05-01.png")


# ---------------------------------------------------------------------------
# Week 6 - goodness of fit
# ---------------------------------------------------------------------------
def fig_06_01():
    fig, ax = F.canvas(4.6, 2.8)
    F.txt(ax, 50, 96, "GOODNESS OF FIT: THE SAME CHILD, TWO ENVIRONMENTS", size=6.4,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([26, 74], [92.5, 92.5], color=F.BRONZE, lw=1.0, zorder=3)
    for px, title, env, out, edge in [
        (26, "POOR FIT", "highly reactive child\nx hurried, critical home",
         "escalation: protest meets\npressure; both conclude\nthe other is the problem", "#8C3B2E"),
        (74, "GOOD FIT", "the same child\nx predictable, warm, unhurried home",
         "mastery: reactivity becomes\nvigour; the child learns\nthat the world is workable", F.TEAL),
    ]:
        F.box(ax, px - 22, 40, 44, 46, F.IVORY if edge is F.TEAL else "#F7EDE9",
              edge=edge, r=1.6)
        F.txt(ax, px, 80, title, size=6.0, color=edge, weight="bold")
        F.txt(ax, px, 68, env, size=5.4, color=F.INK)
        F.txt(ax, px, 52, out, size=5.3, color=F.INK)
    F.txt(ax, 50, 26, "Temperament is not destiny and not diagnosis: it is one half of a\n"
                      "transaction. After Thomas and Chess (1977): the question is never\n"
                      "\"what is wrong with this child?\" but \"what does this child need?\"",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-06-01.png")


# ---------------------------------------------------------------------------
# Week 7 - language milestones and red flags
# ---------------------------------------------------------------------------
def fig_07_01():
    fig, ax = F.canvas(4.6, 2.8)
    ax.set_xlim(-2, 62)
    ax.set_ylim(0, 100)
    F.txt(ax, 30, 95, "LANGUAGE: MILESTONES AND THE POINTS OF NO WAITING", size=6.4,
          color=F.BRONZE_TEXT, weight="bold", ha="center")
    ax.plot([10, 50], [91, 91], color=F.BRONZE, lw=1.0, zorder=3)
    ax.plot([0, 60], [52, 52], color=F.GREY, lw=0.9, zorder=3)
    ms = [
        (2, "cooing"), (6, "babbling"), (12, "first words"),
        (18, "50 words;\ntwo-word combos"), (27, "telegraphic\nspeech"),
        (36, "grammar\nexplosion"), (50, "narrative:\nstories of self"),
    ]
    for i, (m, label) in enumerate(ms):
        up = i % 2 == 0
        ax.plot([m, m], [52, 60 if up else 44], color=F.TEAL, lw=0.9, zorder=3)
        ax.add_patch(Circle((m, 52), 1.4, facecolor=F.TEAL, edgecolor="none", zorder=4))
        F.txt(ax, m, 66 if up else 36, label, size=5.2, color=F.INK)
    for w in (0, 12, 24, 36, 48, 60):
        ax.plot([w, w], [16, 18.5], color=F.GREY, lw=0.8, zorder=3)
        F.txt(ax, w, 12.5, f"{w} mo", size=5.2, color=F.GREY)
    ax.plot([0, 60], [18.5, 18.5], color=F.GREY, lw=0.8, zorder=3)
    flags = [(12, "no babbling\nor gesture"), (18, "no single\nword"), (24, "no two-word\ncombinations")]
    for m, label in flags:
        ax.plot([m, m], [18.5, 24], color="#8C3B2E", lw=1.0, ls=(0, (2, 2)), zorder=3)
        F.txt(ax, m + 1.5, 27, label, size=5.0, color="#8C3B2E", ha="left")
    F.txt(ax, 30, 4, "red flags are referral points, not diagnoses: absence at these ages\n"
                     "warrants hearing test and specialist assessment, never waiting",
          size=5.5, color=F.GREY, style="italic", ha="center")
    F.save(fig, "fig-07-01.png")


# ---------------------------------------------------------------------------
# Week 8 - Erikson's childhood crises
# ---------------------------------------------------------------------------
def fig_08_01():
    fig, ax = F.canvas(4.6, 3.0)
    F.txt(ax, 50, 97, "ERIKSON: THE CRISES OF CHILDHOOD AND WHAT EACH LEAVES BEHIND", size=6.0,
          color=F.BRONZE_TEXT, weight="bold")
    ax.plot([22, 78], [93.5, 93.5], color=F.BRONZE, lw=1.0, zorder=3)
    rows = [
        ("0-1", "trust v. mistrust", "hope", F.TEAL_LIGHT, F.TEAL),
        ("1-3", "autonomy v. shame and doubt", "will", F.TEAL_LIGHT, F.TEAL),
        ("3-6", "initiative v. guilt", "purpose", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        ("6-12", "industry v. inferiority", "competence", F.BRONZE_LIGHT, F.BRONZE_TEXT),
        ("12-18", "identity v. role confusion", "fidelity", "#DDE7E9", F.TEAL),
    ]
    y = 84
    for age, crisis, virtue, fill, edge in rows:
        F.box(ax, 8, y - 12, 84, 12, fill, edge=edge, r=1.2)
        F.txt(ax, 14, y - 6, age, size=5.6, color=edge, weight="bold", ha="left")
        F.txt(ax, 46, y - 6, crisis, size=5.8, color=F.INK, weight="bold")
        F.txt(ax, 86, y - 6, virtue, size=5.6, color=edge, weight="bold", ha="right")
        y -= 15
    F.txt(ax, 50, 6, "Each crisis is resolved in favour of one pole or the other, and the balance\n"
                     "is carried forward: a counsellor meets not a stage but a history of balances.",
          size=5.6, color=F.GREY, style="italic")
    F.save(fig, "fig-08-01.png")


def main():
    F.set_outdir(OUT)
    for f in (fig_01_01, fig_02_01, fig_03_01, fig_04_01, fig_05_01, fig_06_01,
              fig_07_01, fig_08_01):
        f()
    print("Done")


if __name__ == "__main__":
    main()
