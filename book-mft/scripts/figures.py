#!/usr/bin/env python3
"""Generate all diagrams for the MFT book.  Run:  python book-mft/scripts/figures.py"""
import math
from figlib import *


# ============================================================== Chapter 1
def fig_01_01():
    vtimeline("fig-01-01", [
        ("1946", "Macy Conferences on cybernetics begin (to 1953)"),
        ("1952", "Bateson communication project, Palo Alto (to 1962)"),
        ("1956", "The 'double bind' hypothesis is published"),
        ("1959", "Mental Research Institute founded; Jackson"),
        ("1960", "Ackerman Institute for Family Therapy, New York"),
        ("1962", "*Family Process*, the first specialist journal"),
        ("1967", "Milan group forms under Selvini Palazzoli"),
        ("1974", "Minuchin, *Families and Family Therapy*"),
        ("1978", "Bowen, *Family Therapy in Clinical Practice*; Milan paradox"),
        ("1980s", "Second-order cybernetics and the observing system"),
        ("1988", "Emotionally focused therapy for couples"),
        ("1990", "White and Epston, *Narrative Means to Therapeutic Ends*"),
        ("1995", "Integrative problem-centred therapy; common-factors debate"),
        ("2018", "Integrative systemic therapy (Pinsof and colleagues)"),
        ("2020s", "Process research, mechanism studies, dissemination science"),
    ], h=5.0, size=7.0)


def fig_01_02():
    f = Fig("fig-01-02", 4.6, 3.9)
    H = f.H
    # --- Panel A: linear causality -----------------------------------------
    f.text(2, H - 4, "(A)  LINEAR CAUSALITY — the individual-diagnosis view",
           size=7.2, color=TEAL, bold=True, ha="left")
    b1 = f.box(2, H - 16, 21, 9.5, "Child's\nescalation", "light", size=7)
    b2 = f.box(28, H - 16, 21, 9.5, "Parental\nsanction", "light", size=7)
    b3 = f.box(54, H - 16, 21, 9.5, "Symptom\nmaintained", "light", size=7)
    harrow(f, b1, b2, color=BRONZE, lw=1.1)
    harrow(f, b2, b3, color=BRONZE, lw=1.1)
    f.text(88, H - 11, "one-way\nsequence", size=6.4, color=GREY, italic=True)
    f.line([2, 98], [H - 21, H - 21], color=BRONZE, lw=0.6, ls="--")

    # --- Panel B: circular causality ---------------------------------------
    f.text(2, H - 26, "(B)  CIRCULAR CAUSALITY — the systemic view",
           size=7.2, color=TEAL, bold=True, ha="left")
    cx, cy, rx, ry = 30, (H - 26) / 2 + 3, 19, 11.5
    nodes = [
        (cx - rx, cy + ry, "Adolescent\nwithdraws"),
        (cx + rx, cy + ry, "Parent insists\non contact"),
        (cx + rx, cy - ry, "Parent feels\nrejected"),
        (cx - rx, cy - ry, "Adolescent feels\ncontrolled"),
    ]
    bw, bh = 15, 8.5
    for i, (x, y, t) in enumerate(nodes):
        f.box(x - bw / 2, y - bh / 2, bw, bh, t, "light" if i % 2 == 0 else "bronzel", size=6.2)
    for i in range(4):
        x1, y1 = nodes[i][0], nodes[i][1]
        x2, y2 = nodes[(i + 1) % 4][0], nodes[(i + 1) % 4][1]
        a1 = math.atan2(y1 - cy, x1 - cx)
        a2 = math.atan2(y2 - cy, x2 - cx)
        f.arrow(cx + (rx + 1) * math.cos(a1), cy + (ry + 1) * math.sin(a1),
                cx + (rx + 1) * math.cos(a2), cy + (ry + 1) * math.sin(a2),
                color=BRONZE, lw=1.2, rad=-0.28)
    f.text(cx, cy, "each act\nis a stimulus\nfor the next", size=6.4, color=TEAL, bold=True)

    # --- Feedback types ------------------------------------------------------
    x0 = 60
    f.box(x0, cy + 6, 37, 9, "NEGATIVE FEEDBACK\ncounteracts deviation — homeostasis, "
                             "resistance to change", "teal", size=6.2)
    f.box(x0, cy - 6, 37, 9, "POSITIVE FEEDBACK\namplifies deviation — escalation, "
                             "crisis, second-order change", "bronze", size=6.2)
    f.arrow(x0 + 18, cy + 4.5, cx + 8, cy + 4.5, color=GREY, lw=0.7, ls="--")
    f.arrow(x0 + 18, cy - 4.5, cx + 8, cy - 4.5, color=GREY, lw=0.7, ls="--")
    f.save()


def fig_01_03():
    """Family structure maps: clear boundaries (A) versus diffuse boundaries (B)."""
    f = Fig("fig-01-03", 4.6, 3.6)
    H = f.H

    def family(x0, w, y0, h, mode):
        """Draw a four-person family map inside the box (x0, y0, w, h)."""
        f.rect(x0, y0, w, h, fc=IVORY, ec=GREY, lw=0.6)
        top = y0 + h
        # generation boundary
        f.line([x0 + 3, x0 + w - 3], [y0 + h * 0.52, y0 + h * 0.52],
               color=GREY, lw=0.5, ls=":")
        f.text(x0 + w - 3, y0 + h * 0.52 + 2.0, "generation boundary", size=5.2,
               color=GREY, ha="right")
        # parental subsystem
        f.box(x0 + 4, top - h * 0.34, w - 8, h * 0.28, "", "light", lw=0.7)
        f.text(x0 + w / 2, top - h * 0.34 + h * 0.24, "parental subsystem", size=5.6,
               color=TEAL, bold=True)
        # sibling subsystem
        f.box(x0 + 4, y0 + 3.5, w - 8, h * 0.28, "", "ivory", lw=0.7)
        f.text(x0 + w / 2, y0 + 2.4, "sibling subsystem", size=5.6, color=GREY, bold=True)
        # figures
        fx, mx = x0 + w * 0.28, x0 + w * 0.70
        fy = top - h * 0.20
        sy, dy = y0 + 9.5, y0 + 9.5
        f.rect(fx - 4, fy - 4, 8, 8, fc=TEAL, ec=TEAL)
        f.text(fx, fy, "F", size=7.5, color=WHITE, bold=True)
        f.circle(mx, fy, 4.2, fc=BRONZE, ec=BRONZE)
        f.text(mx, fy, "M", size=7.5, color=WHITE, bold=True)
        f.rect(fx - 4, sy - 4, 8, 8, fc=IVORY, ec=TEAL, lw=1.1)
        f.text(fx, sy, "S", size=7.5, color=TEAL, bold=True)
        f.circle(mx, dy, 4.2, fc=IVORY, ec=BRONZE, lw=1.1)
        f.text(mx, dy, "D", size=7.5, color=BRONZE, bold=True)
        # descent lines
        f.line([fx, fx], [fy - 4, dy - 6], color=GREY, lw=1.0)
        f.line([mx, mx], [fy - 4, dy - 6], color=GREY, lw=1.0)
        f.line([fx, mx], [fy - 4, fy - 4], color=GREY, lw=1.0)
        f.line([(fx + mx) / 2, (fx + mx) / 2], [fy - 4, y0 + h * 0.40], color=GREY, lw=1.0)
        if mode == "clear":
            return
        # diffuse boundary / enmeshment: mother to son (double diagonal)
        for dx in (-1.0, 1.0):
            f.line([mx - 4.4 + dx, fx + 4.4 + dx], [fy - 4.4, sy + 4.4], color=TEAL, lw=0.9)
        pass
        # coalition: father to daughter (dashed arrow)
        f.arrow(fx + 4.2, fy - 4.4, mx - 4.2, dy + 4.4, color=BRONZE, lw=1.3, ls="--")
        # overt conflict between the partners (zigzag)
        zx = [fx + 6, fx + 8, fx + 10, fx + 12, fx + 14]
        zy = [fy + 5.4, fy + 7.6, fy + 5.4, fy + 7.6, fy + 5.4]
        f.line(zx, zy, color=BRONZE, lw=1.4)

    panel_h = H - 24
    family(3, 45, 17, panel_h, "clear")
    family(52, 45, 17, panel_h, "diffuse")
    f.text(25.5, H - 5, "(A)  CLEAR BOUNDARIES", size=7.0, color=TEAL, bold=True)
    f.text(74.5, H - 5, "(B)  DIFFUSE BOUNDARIES", size=7.0, color=BRONZE, bold=True)
    f.box(3, 2, 94, 12,
          "KEY      ---  subsystem boundary      - - ->  cross-generational coalition      "
          "===  diffuse (enmeshed) boundary      /\\/  overt conflict      □ male    ○ female",
          "ivory", size=5.6, wrap=118)
    f.save()


def fig_01_04():
    chain("fig-01-04", [
        "Presenting\nsymptom|referred as an\nindividual problem",
        "Observed\nsequence|who does what,\nin what order, in whose\npresence",
        "Function in the\nsystem|what the sequence\nprotects or regulates",
        "Intervention|directive, reframe,\nrestructuring,\nquestioning",
        "Second-order\nchange|the system reorganises;\nsymptom no longer\nnecessary",
    ], h=2.6, size=7.0,
       note="First-order change alters intensity within an unchanged structure; "
            "second-order change alters the rules, boundaries, or premises that generated the sequence.",
       styles=["light", "ivory", "teal", "bronzel", "bronze"])


def fig_01_05():
    """Bowen: the emotional triangle."""
    f = Fig("fig-01-05", 4.6, 3.0)
    H = f.H
    cx, cy, r = 27, H / 2 - 1.5, 16
    pts = [(cx + r * math.cos(math.pi / 2 + 2 * math.pi * i / 3),
            cy + r * math.sin(math.pi / 2 + 2 * math.pi * i / 3)) for i in range(3)]
    labels = ["Partner A", "Partner B", "Third side"]
    for (x, y), lab, col in zip(pts, labels, [TEAL, TEAL, BRONZE]):
        f.circle(x, y, 8.0, fc=col, ec=WHITE, lw=0.8)
        f.text(x, y, lab, size=6.0, color=WHITE, bold=True, wrap=10)
    for i in range(3):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % 3]
        f.line([x1, x2], [y1, y2], color=GREY, lw=1.0, ls="--")
    f.text(cx - 12.0, cy + 2.5, "over-close", size=5.8, color=BRONZE, italic=True, rot=56)
    f.text(cx + 12.5, cy + 2.5, "conflict", size=5.8, color=BRONZE, italic=True, rot=-56)
    f.text(cx, cy - 9.0, "distant or cut off", size=5.8, color=BRONZE, italic=True)
    f.text(pts[2][0], pts[2][1] - 10.4, "child · in-law · work · symptom", size=5.4, color=GREY)
    f.box(58, 3, 40, H - 6,
          "The triangle is the smallest stable relationship system.\n\n"
          "When dyadic tension rises, a third person — or an activity, substance, "
          "or symptom — is recruited to stabilise the pair.\n\n"
          "Triangles are normal. They become clinically significant when rigid, "
          "chronic, and reproduced across generations.",
          "ivory", size=6.0, align="left", wrap=40, lw=0.7)
    f.save()


def fig_01_06():
    """Multigenerational transmission of differentiation."""
    f = Fig("fig-01-06", 4.6, 3.4)
    H = f.H
    f.text(50, H - 4, "MULTIGENERATIONAL TRANSMISSION PROCESS", size=7.0, color=TEAL, bold=True)
    gens = [
        ("GENERATION 1", "Two reasonably differentiated adults marry. Anxiety is absorbed "
                         "in the marital relationship rather than in a child.", 78, "teal"),
        ("GENERATION 2", "A child is drawn into the parental triangle. Differentiation of self "
                         "is lower; the pattern intensifies.", 48, "teal2"),
        ("GENERATION 3", "A third-generation member develops symptoms — the family's attention "
                         "fixes on the identified patient.", 22, "bronze"),
    ]
    top, bh, gap = H - 8, 15.0, 3.0
    for i, (g, txt, level, st) in enumerate(gens):
        y = top - (i + 1) * bh - i * gap
        f.box(2, y, 26, bh, g, st, size=6.8, bold=True)
        f.text(31, y + bh - 4.2, txt, size=6.2, color=INK, ha="left", va="top", wrap=52)
        # differentiation bar
        f.text(31, y + 2.2, "differentiation of self", size=5.6, color=GREY, ha="left")
        f.rect(60, y + 1.6, 36, 2.6, fc=WHITE, ec=GREY, lw=0.5)
        f.rect(60, y + 1.6, 36 * level / 100, 2.6, fc=TEAL if i < 2 else BRONZE, ec="none")
        if i < 2:
            f.arrow(15, y, 15, y - gap - 0.4, color=BRONZE, lw=1.2)
    f.save()


def fig_01_07():
    """EFT: the negative interaction cycle."""
    f = Fig("fig-01-07", 4.6, 3.4)
    H = f.H
    cx, cy, r = 50, H / 2 - 2, 20
    f.circle(cx, cy, r + 7.5, fc=IVORY, ec=BRONZE, lw=0.8)
    pts = [(cx - r, cy), (cx, cy + r * 0.72), (cx + r, cy), (cx, cy - r * 0.72)]
    labels = [
        "Partner A\nprotests, criticises,\npursues",
        "Partner B\nwithdraws,\ngoes silent",
        "Partner B feels\ninadequate, overwhelmed,\n'never good enough'",
        "Partner A feels\nabandoned, alone,\nunlovable",
    ]
    st = ["teal", "light", "bronze", "bronzel"]
    for (x, y), lab, s in zip(pts, labels, st):
        f.box(x - 17, y - 6.5, 34, 13, lab, s, size=6.0)
    for i in range(4):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % 4]
        ang1 = math.atan2(y1 - cy, x1 - cx)
        ang2 = math.atan2(y2 - cy, x2 - cx)
        f.arrow(cx + (r + 1.5) * math.cos(ang1) * 0.95, cy + (r + 1.5) * math.sin(ang1) * 0.95,
                cx + (r + 1.5) * math.cos(ang2) * 0.95, cy + (r + 1.5) * math.sin(ang2) * 0.95,
                color=BRONZE, lw=1.3, rad=-0.22)
    f.text(cx, cy, "attachment\npanic meets\nattachment\npanic", size=6.2, color=TEAL, bold=True)
    f.save()


def fig_01_08():
    matrix("fig-01-08",
           ["Core construct", "Mechanism of change", "Evidence base"],
           [
               ["Structural", "Boundaries;\nhierarchy; alliances", "Restructuring;\nenactment",
                "Moderate–strong for adolescent and\npsychosomatic presentations"],
               ["Strategic /\nMRI brief", "Interactional sequence;\nfunction of symptom",
                "Directives; reframing;\nparadox", "Moderate; paradox carries\ngreater risk"],
               ["Milan systemic", "Beliefs; circularity;\nfamily game", "Circular questioning;\nneutrality; positive connotation",
                "Limited; small trials and\ncase series"],
               ["Intergenerational\n(Bowen)", "Differentiation;\ntriangles; cut-off", "Genogram; detriangulation;\ncoaching",
                "Moderate; largely\ncorrelational research"],
               ["Contextual\n(Boszormenyi-Nagy)", "Legacy; fairness;\ntrustworthiness", "Multidirected partiality;\nexoneration",
                "Emerging; qualitative and\nsmall-scale studies"],
               ["Experiential\n(Satir; Whitaker)", "Self-worth;\ncommunication stances", "Sculpting; immediacy;\nco-therapy",
                "Limited; historically\ninfluential"],
               ["Emotionally focused\n(Johnson)", "Attachment;\nnegative cycle", "Emotion reprocessing;\ncycle de-escalation",
                "Strong: multiple RCTs and\nmeta-analytic support"],
               ["Cognitive-behavioural\n(Epstein; Baucom)", "Cognitions; behaviour\nexchange", "Communication training;\ncognitive restructuring",
                "Strong: extensive RCT\nliterature"],
           ], h=6.4, size=6.0, first_w=24)


def fig_01_09():
    vflow("fig-01-09", [
        "1. Define the system and the problem\nWho is affected, in which relationships, and with what external constraints?",
        "2. Formulate across levels\nStructure and boundaries; interactional sequence; meaning and narrative; emotion and attachment; culture and context.",
        "3. Select mechanisms of change\nMatch the formulation to interventions with plausible and, where possible, demonstrated mechanisms.",
        "4. Sequence and dose the treatment\nOrder the work; agree the goals, frequency, and expected duration; build in review points.",
        "5. Monitor, evaluate, and revise\nUse standardised measures, session feedback, and outcome data; re-formulate or refer when there is no change.",
    ], h=6.2, size=7.0, w=4.6)


# ============================================================== Appendix A
def fig_A_01():
    """Standard genogram notation plate."""
    f = Fig("fig-a-01", 4.6, 4.9)
    H = f.H

    def head(y, text):
        f.text(3, y, text, size=7.0, color=TEAL, bold=True, ha="left")

    def square(x, y, s=6.4, double=False, cross=False):
        f.rect(x - s / 2, y - s / 2, s, s, fc=WHITE, ec=TEAL, lw=1.1)
        if double:
            f.rect(x - s / 2 + 1.4, y - s / 2 + 1.4, s - 2.8, s - 2.8, fc="none", ec=TEAL, lw=0.8)
        if cross:
            f.line([x - s / 2 - 1, x + s / 2 + 1], [y + s / 2 + 1, y - s / 2 - 1], color=INK, lw=1.0)

    def circle(x, y, s=6.4, double=False, cross=False, diamond=False):
        if diamond:
            f.poly([(x, y + s * 0.78), (x + s * 0.78, y), (x, y - s * 0.78), (x - s * 0.78, y)],
                   fc=WHITE, ec=TEAL, lw=1.1)
        else:
            f.circle(x, y, s / 2, fc=WHITE, ec=TEAL, lw=1.1)
            if double:
                f.circle(x, y, s / 2 - 1.4, fc="none", ec=TEAL, lw=0.8)
        if cross:
            f.line([x - s / 2 - 0.6, x + s / 2 + 0.6], [y + s / 2 + 0.6, y - s / 2 - 0.6],
                   color=INK, lw=1.0)

    def lab(x, y, text):
        f.text(x, y, text, size=5.2, color=GREY)

    # ---------- 1. persons (heading 96, symbols 87, labels 81) --------------
    head(96, "PERSONS")
    y = 87
    square(9, y); lab(9, 81, "male")
    circle(25, y); lab(25, 81, "female")
    circle(41, y, diamond=True); lab(41, 81, "gender not recorded")
    square(57, y, double=True); lab(57, 81, "index person")
    circle(73, y, cross=True); lab(73, 81, "deceased")
    f.poly([(89, y + 3.4), (94, y - 3.0), (84, y - 3.0)], fc=WHITE, ec=TEAL, lw=1.1)
    lab(89, 81, "pregnancy")

    # ---------- 2. couple relationships (heading 73, symbols 63, labels 56) --
    head(73, "COUPLE RELATIONSHIPS")
    y = 63

    def couple(x, text, style):
        square(x - 7, y); circle(x + 7, y)
        f.line([x - 3.6, x + 3.6], [y, y], color=INK, lw=1.1, ls="--" if style == "cohabit" else "-")
        if style == "divorce":
            for off in (-1.0, 1.0):
                f.line([x + off - 0.7, x + off + 0.7], [y + 2.4, y - 2.4], color=INK, lw=1.1)
        if style == "separate":
            f.line([x - 0.6, x + 0.8], [y + 2.4, y - 2.4], color=INK, lw=1.1)
        lab(x, 56, text)

    couple(15, "marriage", "married")
    couple(50, "divorce", "divorce")
    couple(83, "separation", "separate")

    # ---------- 3. descent (heading 45, parents 36, children 27, labels 21) --
    head(45, "DESCENT")
    square(16, 36); circle(28, 36)
    f.line([19.5, 24.5], [36, 36], color=INK, lw=1.1)
    f.line([22, 22], [36, 31.5], color=INK, lw=1.1)
    f.line([10, 44], [31.5, 31.5], color=INK, lw=1.1)
    for cx, text, dash in [(10, "biological", "-"), (22, "adopted", "--"),
                           (34, "twin", "-"), (44, "foster", ":")]:
        f.line([cx, cx], [31.5, 28.6], color=INK, lw=1.0, ls=dash)
        square(cx, 26.0, s=5.6)
        lab(cx, 21.0, text)

    # ---------- 4. emotional relationships -----------------------------------
    head(16.0, "EMOTIONAL RELATIONSHIPS")
    y4 = 8.5
    labels = ["close", "fused /\nenmeshed", "distant", "conflict", "cutoff", "asymmetric"]
    xs = [9, 25, 41, 57, 76, 91]
    for x, name in zip(xs, labels):
        if name == "close":
            for off in (-0.9, 0.9):
                f.line([x - 6, x + 6], [y4 + off, y4 + off], color=INK, lw=0.9)
        elif name.startswith("fused"):
            for off in (-1.5, 0, 1.5):
                f.line([x - 6, x + 6], [y4 + off, y4 + off], color=INK, lw=0.9)
        elif name == "distant":
            f.line([x - 6, x + 6], [y4, y4], color=INK, lw=1.0, ls=":")
        elif name == "conflict":
            f.line([x - 6, x - 3.5, x - 1, x + 1.5, x + 4, x + 6],
                   [y4, y4 + 2.2, y4 - 2.2, y4 + 2.2, y4 - 2.2, y4], color=INK, lw=1.0)
        elif name == "cutoff":
            f.line([x - 6, x - 1.4], [y4, y4], color=INK, lw=1.0)
            f.line([x + 1.4, x + 6], [y4, y4], color=INK, lw=1.0)
            for xb in (x - 1.4, x + 1.4):
                f.line([xb, xb], [y4 + 2.2, y4 - 2.2], color=INK, lw=1.0)
        else:
            f.line([x - 6, x + 5], [y4, y4], color=INK, lw=1.0)
            f.arrow(x + 3.2, y4, x + 6, y4, color=INK, lw=1.0)
    f.text(9, 2.6, "close", size=5.0, color=GREY)
    f.text(25, 2.6, "fused or enmeshed", size=5.0, color=GREY)
    f.text(41, 2.6, "distant", size=5.0, color=GREY)
    f.text(57, 2.6, "conflict", size=5.0, color=GREY)
    f.text(76, 2.6, "cutoff", size=5.0, color=GREY)
    f.text(91, 2.6, "asymmetric", size=5.0, color=GREY)
    f.save()



# ============================================================== Chapter 2
def fig_02_01():
    chain("fig-02-01", [
        "Clinical concern|What uncertainty matters?",
        "Question|Who, what, when, where?",
        "Design|What evidence can answer it?",
        "Analysis|What comparison or interpretation?",
        "Conclusion|What claim is warranted?",
    ], h=2.55, size=7.1,
       note="Iterate with feasibility, participant priorities, and ethical review; revise the question when evidence demands it.")


def fig_02_02():
    matrix("fig-02-02",
           ["Quantitative", "Qualitative", "Mixed methods"],
           [
               ("Typical question", "How much? Is there an association?", "How is it experienced or made meaningful?", "How much, and how/why in context?"),
               ("Evidence", "Scores, counts, observations", "Accounts, interaction, documents", "Integrated numerical and textual evidence"),
               ("Strength", "Estimate patterns and uncertainty", "Explain meaning and process", "Connect outcome with context and experience"),
               ("Caution", "Measurement and model assumptions", "Context and researcher interpretation", "Integration must be planned, not decorative"),
           ], h=3.45, size=6.2, first_w=19)


def fig_02_03():
    chain("fig-02-03", [
        "Descriptive|Characterise a pattern",
        "Observational|Estimate association",
        "Quasi-experimental|Use a defensible comparison",
        "Randomised|Allocate intervention by chance",
    ], h=2.75, size=6.8,
       note="Not a universal quality ranking: choose the design that fits the question, context, ethics, and assumptions.")


def fig_02_04():
    f = Fig("fig-02-04", 4.6, 3.0)
    f.text(50, f.H - 5, "DEPENDENCE IN MFT DATA", size=7.2, color=TEAL, bold=True)
    # nested boxes
    f.box(4, 4, 92, 36, "", "ivory", size=6)
    f.text(50, 37, "SERVICE / CLINIC", size=6.5, color=TEAL, bold=True)
    f.box(10, 9, 80, 24, "", "light", size=6)
    f.text(50, 30, "THERAPIST", size=6.2, color=TEAL, bold=True)
    f.box(17, 13, 66, 13, "", "bronzel", size=6)
    f.text(50, 23, "FAMILY / DYAD", size=6.2, color=BRONZE, bold=True)
    f.circle(35, 17, 3.1, fc=TEAL_L, ec=TEAL)
    f.circle(65, 17, 3.1, fc=BRONZE_L, ec=BRONZE)
    f.text(35, 17, "A", size=6, color=TEAL, bold=True)
    f.text(65, 17, "B", size=6, color=BRONZE, bold=True)
    f.arrow(39, 17, 61, 17, color=BRONZE, lw=1.1, style="<->")
    f.text(50, 6.0, "Members are interdependent; repeated measures add another level.", size=6.1, color=GREY, italic=True)
    f.save()


def fig_02_05():
    f = Fig("fig-02-05", 4.6, 3.2)
    f.text(50, f.H - 5, "HYPOTHESISED PATHWAYS IN AN INTERVENTION STUDY", size=7.0, color=TEAL, bold=True)
    # nodes in x-y
    a = f.box(4, 23, 23, 11, "Baseline context\n(severity, resources)", "ivory", size=6.4)
    b = f.box(38, 23, 23, 11, "Intervention\n(assigned condition)", "teal", size=6.5)
    c = f.box(72, 23, 23, 11, "Outcome\n(relational change)", "bronze", size=6.5)
    d = f.box(38, 5, 23, 10, "Proposed process\n(alliance / interaction)", "light", size=6.1)
    f.arrow(27, 28.5, 38, 28.5, color=GREY, lw=1.0)
    f.arrow(61, 28.5, 72, 28.5, color=BRONZE, lw=1.2)
    f.arrow(49.5, 23, 49.5, 15, color=TEAL, lw=1.0)
    f.arrow(61, 10, 78, 23, color=TEAL, lw=1.0)
    f.arrow(16, 23, 39, 14, color=GREY, lw=0.9, ls="--")
    f.arrow(27, 25, 72, 25, color=GREY, lw=0.7, ls=":", rad=-0.28)
    f.text(49, 2, "Arrows encode hypotheses; temporal order and confounding must be addressed.", size=5.8, color=GREY, italic=True)
    f.save()


if __name__ == "__main__":
    import sys
    only = sys.argv[1:] or None
    for name, fn in sorted(globals().items()):
        if name.startswith("fig_") and callable(fn):
            if only and not any(name.startswith("fig_" + o.replace("-", "_")) for o in only):
                continue
            fn()
            print("  drew", name)
