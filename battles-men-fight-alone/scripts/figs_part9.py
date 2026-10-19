"""Figures for Part Nine — The Battles of Leadership, Power, and Responsibility (Chapters 31-33)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Chapter 31
@_fig("fig-31-01")
def fig_31_01():
    d.compare("fig-31-01", "The load the position creates", [
        "The decision burden: every matter is final and every decision affects households.",
        "The example burden: the man is the standard continuously, without off hours.",
        "The morale burden: he holds the group's state while holding his own.",
        "The boundary burden: nothing else in the arrangement will set the limit.",
        "The accumulated confidences: other people's material, brought to him and left with him.",
    ], "The arrangement each one requires", [
        "Retrieved information: the five questions asked monthly of named people.",
        "The place where he is not the leader, and the refusal of office within it.",
        "A peer arrangement of equivalent leaders, with a rule of confidentiality.",
        "The written boundary: hours, days, travel, and what will not be moved.",
        "A professional arrangement outside the line, whose confidentiality is an obligation.",
    ], w=4.7, h=4.6)


# ---------------------------------------------------------------- Chapter 32
@_fig("fig-32-01")
def fig_32_01():
    d.compare("fig-32-01", "What the absolute requirement costs", [
        "The bluff: the answer supplied without the information, which ends the enquiry.",
        "The arrested learning: the questions never asked in public, and the gap that persists.",
        "The distorted information: bad news stops travelling upward to the man.",
        "The withdrawal of others: the household manages alone and the children select.",
    ], "What the protocol supplies", [
        "Part one: what I know, stated accurately and without amplification.",
        "Part two: what I do not know, stated plainly, in the same register.",
        "Part three: what happens next — who knows, by what means, and by when.",
        "The five questions, asked monthly of named people, and recorded.",
    ], w=4.7, h=4.5)


# ---------------------------------------------------------------- Chapter 33
@_fig("fig-33-01")
def fig_33_01():
    d.compare("fig-33-01", "How the role is acquired", [
        "Step one: the man becomes competent or solvent.",
        "Step two: the first request is met, reasonably, once.",
        "Step three: the record is established — this man can be asked.",
        "Step four: the requests multiply, across relatives and settings.",
        "Step five: the refusal becomes unacceptable and expensive.",
        "Step six: the man's own material accumulates without any arrangement.",
    ], "What distributes the load", [
        "The written inventory: one month of every demand, with the total.",
        "The family's own arrangement: contributions allocated by the family.",
        "The referral map: the institutions and practitioners who should hold it.",
        "The stated terms: the amount, the condition, the duration.",
        "The arrangements for the man: a confidant, a group, a professional.",
        "The household's participation: the cost counted and decided, not absorbed.",
    ], w=4.7, h=4.6)
