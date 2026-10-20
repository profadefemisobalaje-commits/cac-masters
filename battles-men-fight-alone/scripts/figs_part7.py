"""Figures for Part Seven — The Battles of Standing and Belonging (Chapters 25-27)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Chapter 25
@_fig("fig-25-01")
def fig_25_01():
    d.compare("fig-25-01", "How the assessment arrives", [
        "The question and the immediate answer it requires",
        "The visible markers, read without a question being asked",
        "The comparisons conducted by others in the man's presence",
        "The institutional records that decide his next options",
        "The evaluative vocabulary available for men",
        "The invitations, introductions, and opportunities not extended",
    ], "Where it can be interrupted", [
        "State the position accurately, once, without apology",
        "Reduce the ceremonies at which position is displayed",
        "Reduce exposure to continuous comparison",
        "Obtain the record: applications, work completed, obligations met",
        "Apply your own measure, written and specific",
        "Build the smaller audience and one relationship without assessment",
    ], w=4.7)


# ---------------------------------------------------------------- Chapter 26
@_fig("fig-26-01")
def fig_26_01():
    d.sequence("fig-26-01", [
        "The act|The disclosure, the pursuit, the financial loss, the withheld defence, or the absent assistance. The man's first response is disbelief, because the act is inconsistent with the model he held.",
        "The management of the discovery|The man decides within days whether to confront, to reduce the relationship silently, or to continue as though nothing had occurred. The third option is the most common and the most expensive.",
        "The confrontation, where it occurs|What I know, what it has cost me, and what I intend. The direct form does not require the other man's agreement.",
        "The assessment of the relationship|Which term was relied upon and was not held; was the failure a decision or an incapacity; is the conduct capable of change; what would I require in order to continue? Conducted in writing.",
        "The outcome|Repair, where the act is acknowledged and the terms restated; revision, where the relationship continues on reduced terms; or conclusion, where it ends.",
        "The consolidation|The findings are drawn: the term relied upon, the evidence that was available, what the arrangement should have included, and what remains true about men.",
    ], note="The outcome is determined at the stage of assessment, not at the act. Men who omit that stage move directly from the act to a general conclusion about trust.")


# ---------------------------------------------------------------- Chapter 27
@_fig("fig-27-01")
def fig_27_01():
    d.compare("fig-27-01", "The stage", [
        "One. Identification of one person",
        "Two. Contact without the material",
        "Three. The reciprocal arrangement",
        "Four. The first delivery of material",
        "Five. The professional arrangement",
        "Six. The group",
    ], "What it requires, and what blocks it", [
        "Requires a name. Blocked by the belief that no such person exists.",
        "Requires a small act on any reason at all. Blocked by the requirement that it be significant.",
        "Requires that the man supply something. Blocked by the assumption that the arrangement is one-way.",
        "Requires one small, specific, non-catastrophic item. Blocked by the fear of the whole account.",
        "Requires an appointment and a presenting complaint. Blocked by the belief that the professional route is not for men like him.",
        "Requires a fixed time, a small number, and a rule of confidentiality. Blocked by the absence of an available group.",
    ], w=4.7)
