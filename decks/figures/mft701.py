"""Signature diagrams for MFT 701 — Fundamentals of Marriage and Family Therapy."""
from __future__ import annotations

from pathlib import Path

from . import archetypes as A
from .style import Fig, mix

OUT = Path(__file__).resolve().parents[1] / "figures" / "MFT-701"


def _fig(pal, name):
    p = pal
    return Fig(p.accent, p.accent_soft, p.accent_deep), OUT / name


# ==========================================================================
def fig_01(pal):
    """The ecology of practice: nested rings with a legend."""
    f, path = _fig(pal, "01-ecology-of-practice.png")
    import math
    cx, cy, R = 20.5, 17.25, 13.2
    f.circle(cx, cy, R, fc=mix(f.paper, f.accent, 0.075), ec=None, z=1)
    f.circle(cx, cy, R * 0.75, fc=f.paper, ec=None, z=1)
    f.circle(cx, cy, R * 0.50, fc=mix(f.paper, f.accent, 0.14), ec=None, z=1)
    for r in (R, R * 0.75, R * 0.50):
        f.circle(cx, cy, r, ec=mix(f.paper, f.accent, 0.55), lw=0.55, z=3)
    f.circle(cx, cy, R * 0.25, fc=f.accent, ec="none", z=2)
    f.txt(cx, cy, "PERSON", size=4.6, face="sans-sem", color=f.paper)

    rows = [
        (29.0, "Culture & institution",
         "Law, faith, economy, school and health systems set the\nconditions under which family life is possible."),
        (21.6, "Kin & community",
         "Extended family, neighbours, congregation and workplace\ndistribute care, obligation and reputation."),
        (14.2, "Couple & family",
         "Attachment, communication, caregiving and conflict\norganise the ordinary business of daily life."),
        (6.8, "Individual",
         "Biology, meaning, symptom and history — the person\nas a whole, never as an isolate."),
    ]
    for y, title, desc in rows:
        dy = y - cy
        dx = math.sqrt(max(0.0, R * R - dy * dy)) if abs(dy) <= R else 0.0
        sx = cx + max(dx, 0.0)
        f.line(sx, y, 38.5, y, color=mix(f.paper, f.accent, 0.55), lw=0.55,
               ls=(0, (1.5, 2.0)), z=4)
        f.circle(sx, y, 0.42, fc=f.accent, ec="none", z=5)
        f.txt(41.2, y + 1.35, title, size=10.4, face="serif-med", color=f.ink, ha="left")
        f.txt(41.2, y - 2.05, desc, size=6.8, face="sans-light", color=f.soft,
              ha="left", linespacing=1.42)
        f.line(41.2, y - 4.65, 96.0, y - 4.65, color=f.hair, lw=0.4)
    return f.save(path)


# ==========================================================================
def fig_02(pal):
    """Parts versus pattern: two rival explanations of the same facts."""
    f, path = _fig(pal, "02-parts-to-pattern.png")
    f.line(50, 2.4, 50, 32.0, color=f.hair, lw=0.5, ls=(0, (2, 3)))

    f.label(25, 31.0, "EXPLANATION BY PARTS")
    f.txt(25, 28.7, "A chain of individual causes", size=7.6, face="serif-it", color=f.muted)

    left = ["Father's drinking", "Mother's vigilance", "Son's mediation", "Daughter's silence"]
    y0, bh, gap = 23.2, 4.0, 1.6
    for i, t in enumerate(left):
        y = y0 - i * (bh + gap)
        f.box(5, y, 40, bh, fc=f.paper, ec=f.hair, radius=0.6)
        f.txt(7.0, y + bh / 2, f"{i + 1:02d}", size=5.8, face="sans-sem",
              color=f.gold, ha="left")
        f.txt(11.0, y + bh / 2, t, size=8.2, face="serif", color=f.ink, ha="left")
        if i < 3:
            f.arrow(25, y - 0.15, 25, y - gap + 0.15, color=f.muted, lw=0.8)
    f.txt(25, 4.0, "The cause precedes the effect.", size=7.0, face="serif-it", color=f.muted)

    f.label(75, 31.0, "EXPLANATION BY PATTERN")
    f.txt(75, 28.7, "A loop that returns to itself", size=7.6, face="serif-it", color=f.muted)

    bw, bh2 = 17.0, 3.8
    nodes = {"tl": (63, 24.2, "Drinking"), "tr": (87, 24.2, "Vigilance"),
             "br": (87, 11.6, "Silence"), "bl": (63, 11.6, "Mediation")}
    for k, (x, y, t) in nodes.items():
        f.box(x - bw / 2, y - bh2 / 2, bw, bh2, fc=f.paper, ec=f.hair, radius=0.6)
        f.txt(x, y, t, size=8.0, face="serif", color=f.ink)

    f.arrow(63 + bw / 2 + 0.4, 24.2, 87 - bw / 2 - 0.4, 24.2, color=f.accent, lw=1.0)
    f.arrow(87, 24.2 - bh2 / 2 - 0.3, 87, 11.6 + bh2 / 2 + 0.3, color=f.accent, lw=1.0)
    f.arrow(87 - bw / 2 - 0.4, 11.6, 63 + bw / 2 + 0.4, 11.6, color=f.accent, lw=1.0)
    f.arrow(63, 11.6 + bh2 / 2 + 0.3, 63, 24.2 - bh2 / 2 - 0.3, color=f.accent, lw=1.0)

    f.txt(75, 18.0, "no first cause", size=7.4, face="serif-it", color=f.accent)
    f.txt(75, 15.8, "only a chosen beginning", size=6.4, face="sans-light", color=f.muted)
    f.txt(75, 4.0, "The effect becomes the next cause.", size=7.0, face="serif-it", color=f.muted)
    return f.save(path)


# ==========================================================================
def fig_03(pal):
    """First-order and second-order observation."""
    f, path = _fig(pal, "03-first-second-order.png")
    f.line(50, 2.6, 50, 32.0, color=f.hair, lw=0.5, ls=(0, (2, 3)))

    f.label(25, 31.4, "FIRST-ORDER")
    f.txt(25, 28.9, "The observer stands outside", size=7.6, face="serif-it", color=f.muted)
    f.box(30.5, 23.6, 12.5, 3.4, "Observer", fc=mix(f.paper, f.accent, 0.16),
          ec=f.accent, tc=f.accent_deep, radius=0.5, lw=0.7)

    nodes = [(20.0, 17.9, "Event"), (12.4, 8.6, "Response"), (27.6, 8.6, "Interpretation")]
    for x, y, t in nodes:
        f.box(x - 5.4, y - 1.6, 10.8, 3.2, fc=f.paper, ec=f.hair, radius=0.5)
        f.txt(x, y, t, size=6.6, face="serif", color=f.ink)
    f.arrow(18.8, 16.2, 13.8, 10.3, color=f.soft, lw=0.9, rad=-0.16)
    f.arrow(17.9, 8.6, 22.1, 8.6, color=f.soft, lw=0.9, ms=7)
    f.arrow(26.6, 10.2, 21.3, 16.2, color=f.soft, lw=0.9, rad=-0.16)
    f.arrow(31.4, 23.4, 22.6, 19.2, color=f.accent, lw=0.8, ls=(0, (3, 2)), ms=7)
    f.txt(28.6, 20.4, "observes", size=6.2, face="sans-it", color=f.accent)
    f.txt(25, 2.6, "Description from outside.", size=7.2, face="serif-it", color=f.muted)

    f.label(75, 31.4, "SECOND-ORDER")
    f.txt(75, 28.9, "The observer is in the loop", size=7.6, face="serif-it", color=f.muted)
    cyc = [(75.0, 22.8, "Event"), (85.6, 16.9, "Response"),
           (75.0, 11.0, "Interpretation"), (64.4, 16.9, "Therapist")]
    for x, y, t in cyc:
        accent = t == "Therapist"
        f.box(x - 5.9, y - 1.55, 11.8, 3.1,
              fc=f.accent if accent else f.paper,
              ec=f.accent if accent else f.hair, radius=0.5)
        f.txt(x, y, t, size=6.6, face="serif", color=f.paper if accent else f.ink)

    f.arrow(76.6, 21.6, 83.6, 18.1, color=f.accent, lw=0.9, rad=-0.12)
    f.arrow(85.4, 15.3, 78.4, 12.0, color=f.accent, lw=0.9, rad=-0.12)
    f.arrow(72.6, 12.0, 65.6, 15.4, color=f.accent, lw=0.9, rad=-0.12)
    f.arrow(64.6, 18.2, 71.8, 21.6, color=f.accent, lw=0.9, rad=-0.12)
    f.txt(75, 16.9, "the observing\nsystem", size=6.5, face="sans-light",
          color=f.muted, linespacing=1.3)
    f.txt(75, 2.6, "Description from within.", size=7.2, face="serif-it", color=f.muted)
    return f.save(path)


# ==========================================================================
def fig_04(pal):
    """The recursive sequence."""
    f, path = _fig(pal, "04-recursive-sequence.png")
    nodes = [(27, 25.2, "Tolu's silence", "1"), (73, 25.2, "Mother's vigilance", "2"),
             (73, 9.4, "Father's withdrawal", "3"), (27, 9.4, "Tolu's guilt", "4")]
    bw, bh = 23.0, 4.4
    for x, y, t, n in nodes:
        f.box(x - bw / 2, y - bh / 2, bw, bh, fc=f.paper, ec=f.hair, radius=0.7)
        f.circle(x - bw / 2 + 2.2, y, 1.15, fc=f.accent, ec="none", z=6)
        f.txt(x - bw / 2 + 2.2, y - 0.05, n, size=5.4, face="sans-sem", color=f.paper)
        f.txt(x + 1.6, y, t, size=8.4, face="serif", color=f.ink)

    f.arrow(38.6, 25.8, 61.0, 25.8, color=f.accent, lw=1.0, rad=-0.16)
    f.arrow(73.6, 22.9, 73.6, 11.7, color=f.accent, lw=1.0, rad=-0.16)
    f.arrow(61.4, 9.0, 38.8, 9.0, color=f.accent, lw=1.0, rad=-0.16)
    f.arrow(26.4, 11.7, 26.4, 22.9, color=f.accent, lw=1.0, rad=-0.16)

    f.txt(50, 29.6, "she monitors", size=7.4, face="serif-it", color=f.soft)
    f.txt(82.6, 17.3, "he retreats", size=7.4, face="serif-it", color=f.soft, rotation=270)
    f.txt(50, 4.8, "she feels responsible", size=7.4, face="serif-it", color=f.soft)
    f.txt(18.2, 17.3, "she goes quiet", size=7.4, face="serif-it", color=f.soft, rotation=90)

    f.txt(50, 17.6, "The pattern has no first cause —", size=7.2, face="serif-it", color=f.muted)
    f.txt(50, 15.5, "only a chosen beginning.", size=7.2, face="serif-it", color=f.muted)
    return f.save(path)


# ==========================================================================
def fig_05(pal):
    """Life cycle arc with horizontal and vertical stressors."""
    return A.chain(
        pal, "05-life-cycle.png",
        [("Leaving home", "separation without severance"),
         ("Joining", "two systems become three"),
         ("Young children", "caregiving reorganises the couple"),
         ("Adolescence", "autonomy and renegotiation"),
         ("Launching", "the household contracts"),
         ("Later life", "care reverses")],
        note="Horizontal stressors arrive on schedule; vertical stressors arrive from earlier generations.")


# ==========================================================================
def fig_06(pal):
    """The family triangle."""
    return A.triangle(
        pal, "06-triangle.png",
        "Child (the symptom)", "Mother (pursuit)", "Father (withdrawal)",
        arrows=["protects", "pulls in", "withdraws"],
        centre="the conflict stays\nbetween the parents",
        note="The triangle stabilises the couple and places the burden on the child.")


# ==========================================================================
def fig_07(pal):
    """Report, command and the double bind."""
    f, path = _fig(pal, "07-report-command.png")
    f.label(50, 31.2, "ONE MESSAGE, TWO LEVELS")

    # outer message
    f.box(18.0, 22.2, 64.0, 5.6, fc=f.paper, ec=f.hair, radius=0.7, lw=0.8)
    f.txt(50, 25.0, "\u201cGo out with your friends. I\u2019m fine.\u201d", size=11.4,
          face="serif-it", color=f.ink)
    f.txt(50, 20.0, "the utterance", size=6.5, face="sans-light", color=f.muted)

    # two levels
    f.line(50, 19.2, 50, 16.4, color=f.hair, lw=0.9)
    f.line(26.0, 16.4, 74.0, 16.4, color=f.hair, lw=0.9)
    f.line(26.0, 16.4, 26.0, 14.8, color=f.hair, lw=0.9)
    f.line(74.0, 16.4, 74.0, 14.8, color=f.hair, lw=0.9)

    f.box(6.0, 8.4, 40.0, 6.4, fc=mix(f.paper, f.accent, 0.08), ec=f.hair, radius=0.7)
    f.txt(26.0, 12.8, "REPORT", size=6.4, face="sans-sem", color=f.gold)
    f.txt(26.0, 10.4, "the content: permission is given", size=7.6, face="serif-it", color=f.ink)

    f.box(54.0, 8.4, 40.0, 6.4, fc=mix(f.paper, f.accent, 0.08), ec=f.hair, radius=0.7)
    f.txt(74.0, 12.8, "COMMAND", size=6.4, face="sans-sem", color=f.accent)
    f.txt(74.0, 10.4, "the relationship: do not go", size=7.6, face="serif-it", color=f.ink)

    f.label(50, 4.6, "CONTRADICTION")
    f.txt(50, 2.4, "The receiver cannot obey both, and cannot comment on the contradiction.",
          size=6.9, face="serif-it", color=f.muted)
    return f.save(path)


# ==========================================================================
def fig_08(pal):
    """Joining and observing: the reflexive position."""
    return A.spectrum(
        pal, "08-reflexive-position.png",
        "JOINING", "OBSERVING",
        [(0.14, "Over-identification", "lost in the family's story"),
         (0.50, "The reflexive position", "affected and able to describe"),
         (0.86, "Detachment", "safe, but useless")],
        note="The therapist moves along the continuum within a single session, not once for all.")


# ==========================================================================
def fig_09(pal):
    """The attachment cycle."""
    return A.cycle(
        pal, "09-attachment-cycle.png",
        ["Threat", "Proximity seeking", "Care received", "Exploration"],
        arrows=["the child signals", "the caregiver responds", "security restored",
                "the world is re-entered"],
        centre="a secure base",
        sub="the loop that builds security",
        note="Repetition of the loop builds expectation; interruption without repair produces strategy or disorganisation.")


# ==========================================================================
def fig_10(pal):
    """The intersecting field."""
    return A.hub(
        pal, "10-intersecting-field.png",
        "The family's\nposition",
        [("Culture", "meaning and practice"), ("Economy", "time, housing, risk"),
         ("Gender", "care and obligation"), ("Faith", "belonging and authority"),
         ("Legal status", "rights and exposure")],
        note="No single axis explains a family's constraints. Locate the intersections that matter here.")


# ==========================================================================
def fig_11(pal):
    """A map of the schools: present interaction vs history, meaning vs structure."""
    return A.quad_axes(
        pal, "11-map-of-schools.png",
        "FOCUS ON MEANING", "FOCUS ON STRUCTURE",
        "present interaction", "history and development",
        [(0.26, 0.26, "Narrative", "re-author the problem"),
         (0.74, 0.30, "Structural", "reorganise the system"),
         (0.62, 0.18, "Strategic", "interrupt the sequence"),
         (0.84, 0.55, "EFT / CBFT", "new emotional experience"),
         (0.70, 0.84, "Multigenerational", "work through the past"),
         (0.30, 0.80, "Psychodynamic", "make the unconscious conscious")],
        note="The axes are questions, not a league table: where does this model look, and what does it ask you to change?")


# ==========================================================================
def fig_12(pal):
    """What accounts for change."""
    return A.stack(
        pal, "12-change-variance.png",
        [(35, "Client & context", "the clinician does not control these"),
         (30, "Alliance", "the working relationship"),
         (15, "Expectancy", "hope, rationale, credibility"),
         (20, "Model & technique", "specific ingredients")],
        note="Indicative distribution after common-factors models. The clinician controls only part of the field — and that part matters.")


# ==========================================================================
def fig_13(pal):
    """The arc of therapy."""
    return A.chain(
        pal, "13-arc-of-therapy.png",
        [("Joining", "safety and consent"),
         ("Assessing", "pattern, risk, resource"),
         ("Planning", "negotiated goals"),
         ("Working", "interrupting and rehearsing"),
         ("Ending", "consolidation and review")],
        note="The movements recur. Assessment continues to the last session; the ending is anticipated from the first.")


# ==========================================================================
def fig_14(pal):
    """An ethical decision pathway."""
    return A.flow(
        pal, "14-ethical-pathway.png",
        "An ethical dilemma",
        [("Identify", "duties, parties, risk"),
         ("Consult", "supervisor, law, code"),
         ("Weigh", "two frameworks compared"),
         ("Act & record", "decision, reasons, review")],
        note="The pathway does not remove the difficulty. It makes the reasoning visible, and therefore reviewable.")


# ==========================================================================
def fig_15(pal):
    """From question to evidence to practice."""
    return A.chain(
        pal, "15-evidence-to-practice.png",
        [("Question", "what do I need to know?"),
         ("Design", "what could answer it?"),
         ("Appraisal", "how strong is the answer?"),
         ("Applicability", "does it fit this family?"),
         ("Judgement", "what will I do, and why?")],
        note="Most errors occur at the fourth step: the study is sound, but the family is not in it.")


# ==========================================================================
def fig_16(pal):
    """The integrative position."""
    return A.hub(
        pal, "16-integrative-position.png",
        "The integrative\nposition",
        [("Theory", "what you believe"), ("Method", "what you do"),
         ("Ethics", "what constrains you"), ("Evidence", "what you can defend"),
         ("Culture", "where you stand")],
        note="A defensible practice is the point at which these meet — and the conflicts between them are named.")


FIGURES = {
    1: fig_01, 2: fig_02, 3: fig_03, 4: fig_04,
    5: fig_05, 6: fig_06, 7: fig_07, 8: fig_08,
    9: fig_09, 10: fig_10, 11: fig_11, 12: fig_12,
    13: fig_13, 14: fig_14, 15: fig_15, 16: fig_16,
}
