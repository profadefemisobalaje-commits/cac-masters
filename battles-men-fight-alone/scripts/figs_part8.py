"""Figures for Part Eight — The Battles of Loss, Regret, and Broken Dreams (Chapters 28-30)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Chapter 28
@_fig("fig-28-01")
def fig_28_01():
    d.sequence("fig-28-01", [
        "The dream is set down|Not in a decision but in a sequence: an obligation arrives, the plan is postponed to a date that is never fixed, and the postponement is repeated until the dream is no longer advanced.",
        "The dream is carried open|It occupies the space of a live plan while offering none of the activity of one. Two comparisons operate continuously: with the men who went, and with the version of the man who took the path.",
        "The cost of carrying it open|The man's actual life is measured against a standard composed of the dream's benefits and none of its costs, and is found deficient. The material is available to every trigger: an announcement, an obituary, a reunion, a song.",
        "The two legitimate endings — the closing|The account written in the past tense, the accounting of the alternative's costs, one witness, and a dated marker. Both sentences are held together: I set this down and would decide the same; what I built is real and counted.",
        "The two legitimate endings — the first step|For a dream that remains genuinely available: the content is separated from the form, one small first step is identified, and a date within thirty days is set. A pending dream receives the step or it is closed.",
    ], note="The position to be avoided is the dream that receives neither the step nor the closing. It is the most expensive of all the positions described in this chapter.")


# ---------------------------------------------------------------- Chapter 29
@_fig("fig-29-01")
def fig_29_01():
    d.compare("fig-29-01", "The corrective mode", [
        "The material is examined once and then held as information.",
        "It supplies a standard the man acts upon in comparable situations.",
        "It is stable across states: low mood, drink, and anniversaries do not alter it.",
        "The man's ordinary goods are not affected by it.",
        "Its conduct is visible: the man intervenes, attends, speaks, repays.",
    ], "The punitive mode", [
        "The material is replayed without alteration, frequently for decades.",
        "It alters no conduct; its only product is the man's private condition.",
        "It escalates with low mood, drink, and anniversaries.",
        "The man's ordinary goods are treated as illegitimate or unearned.",
        "Its conduct is avoidance: the place, the person, and the subject are declined.",
    ], w=4.7, h=4.4)


# ---------------------------------------------------------------- Chapter 30
@_fig("fig-30-01")
def fig_30_01():
    d.sequence("fig-30-01", [
        "The loss occurs|A death, a leaving, an ending. The man's first business is practical: the arrangements, the costs, the household, the obligations. The activity is real and it occupies the days.",
        "The activity ends|The burial is complete, the visitors have stopped coming, the household's arrangements have been made. There is nothing left that requires the man, and the quiet arrives.",
        "The private season|The material arrives without a listener. The man is composed in public and occupied in private, and the difference between his presentation and his state widens — the gap described in Section 21.2.",
        "The audience problem|The man's grief is unwitnessed: the people who knew the deceased are carrying their own, the man's position forbids the display, and the occasion has passed. The material is held but not shared.",
        "The reconstruction|The loss is brought into the man's arrangements: a witness, a date or place of remembrance, the material stated in the terms the man actually holds it, and the household's own arrangements restored.",
    ], note="The private season is not a failure of strength. It is a normal season made longer by the absence of an audience.")
