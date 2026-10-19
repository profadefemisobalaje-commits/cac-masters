"""Figures for Part Five — The Battles of Family and Fatherhood (Chapters 17-20)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Chapter 17
@_fig("fig-17-01")
def fig_17_01():
    d.rings("fig-17-01", "The father", [
        "Children: provision, protection, guidance, and example",
        "Partner: the marriage, its intimacy, and its shared decisions",
        "His own parents: respect, care in illness, and financial support",
        "Extended family and community: contributions, mediation, and standing",
    ], w=4.7, h=4.4)


# ---------------------------------------------------------------- Chapter 18
@_fig("fig-18-01")
def fig_18_01():
    d.compare("fig-18-01", "The husband's role", [
        "Is the household's income and its decision-maker",
        "Manages relatives, institutions, and disputes",
        "Remains composed and does not require anything",
        "Is consulted about matters of consequence",
        "Is known by what he provides and manages",
    ], "The husband's person", [
        "Knows what he wants and can say it",
        "Is known by his wife beyond his function",
        "Has interests and relationships of his own",
        "Can be uncertain and can be looked after",
        "Is known by what he thinks, fears, and values",
    ], w=4.7)


# ---------------------------------------------------------------- Chapter 19
@_fig("fig-19-01")
def fig_19_01():
    d.sequence("fig-19-01", [
        "The occasion|A death, a departure, an illness, poverty, displacement, or a household in conflict.",
        "The role is taken up|The child assumes provision, care, protection, or the household's emotional load — without a discussion and without a date.",
        "The consequence becomes the child's|The child bears the outcome rather than merely the task, and childhood ends at that point.",
        "The arrangement is maintained|Competence is rewarded, the household depends on it, and the position is held into adult life.",
        "The material becomes visible|When the obligation ends — through bereavement, retirement, or the last child's completion — the arrangement loses its justification and the costs appear.",
    ], note="The sequence is not fixed. The arrangement can be revised at any stage, and the work described in this chapter is the revision.")


# ---------------------------------------------------------------- Chapter 20
@_fig("fig-20-01")
def fig_20_01():
    d.sequence("fig-20-01", [
        "Accumulation|Years of competent, unacknowledged contribution, and no problem is experienced. The intervention available at this stage: disclosure of the cost, stated as information.",
        "Recognition of the pattern|One event makes the arrangement visible, generally another person's contribution being thanked in his presence. The intervention: name the position to the household.",
        "Withdrawal of discretionary effort|The obligations continue and the voluntary contributions stop. This is the last stage at which a single conversation is usually sufficient.",
        "Contempt|The grievance transfers to the persons of the household. Professional help is indicated, and the condition is difficult to reverse alone.",
        "Alternative audience|Recognition is obtained outside the household: a position, a group, or another person.",
        "The arrival of the material|The obligations reduce, and the man discovers that he cannot name a relationship in which he is valued.",
    ], w=4.6, h=5.8, size=6.8, note="Each stage is described first; the intervention that remains available at that stage follows it.")
