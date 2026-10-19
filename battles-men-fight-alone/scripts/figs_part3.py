"""Figures for Part Three — The Financial Battles Men Fight (Chapters 9-12)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Chapter 9
@_fig("fig-09-01")
def fig_09_01():
    d.stairs("fig-09-01", [
        "The four pressures|Household expectations, the community's account of him, the children's schooling, and the comparison with his peers.",
        "The first borrowing|The gap is covered once, on the understanding that it is temporary.",
        "The escalation|Each period is covered by the next arrangement, and the total is held only in the man's head.",
        "The concealment|The accounts are kept separately, the questions are answered without the figures, and the household plans on a position it has not been shown.",
        "The interruption point|A facility is called, a letter arrives, or the man cannot state the total. This is the point at which the spiral stops being manageable.",
    ], note="The spiral is mechanical rather than moral: each step is a reasonable response to the one before it, and the whole is invisible until the total is written down.")


# --------------------------------------------------------------- Chapter 10
@_fig("fig-10-01")
def fig_10_01():
    d.loadbars("fig-10-01", [
        "The household: rent, food, school fees, medical costs|1.0",
        "Parents: maintenance, treatment, and the family house|0.82",
        "Siblings and their children: fees, rent, and emergencies|0.66",
        "The wider kin: funerals, weddings, and legal matters|0.52",
        "The community and the association: dues and contributions|0.44",
        "The man's own reserve and retirement|0.3",
        "People from whom he may ask for help|0.12",
    ])


# --------------------------------------------------------------- Chapter 11
@_fig("fig-11-01")
def fig_11_01():
    d.compare("fig-11-01", "Society's definition of a successful man", [
        "Comparative: success is measured against the men around him, so the standard moves whenever his position does.",
        "Public: the evidence must be visible — the house, the vehicle, the title, the school, the office.",
        "Borrowed timetable: the milestones are dated against an economy and a generation that are not his own.",
        "Single-domain: career position is treated as the whole of the verdict on the man.",
    ], "An individual definition that will hold", [
        "Stated in domains rather than in one: work, household, health, contribution, and conduct.",
        "Measured against his own previous position, not against a moving comparison group.",
        "Answered by items the audience cannot see, so it survives the loss of a title.",
        "Reviewed annually, in writing, against what he actually did.",
    ], w=4.7, h=4.4)


# --------------------------------------------------------------- Chapter 12
@_fig("fig-12-01")
def fig_12_01():
    d.sequence("fig-12-01", [
        "Step one: sleep and one medical item|Address sleep first, and complete one deferred medical matter. Both are attainable without altering a single commitment to anybody else.",
        "Step two: the hour count and the ceiling|Record actual hours for two weeks, write a ceiling, and choose one category of work to eliminate.",
        "Step three: family presence and one relationship|Schedule the minimum allocations with the household, and reinstate one friendship in which he is not the provider.",
        "Step four: structure and transition|Establish the non-work element that will supply identity, and begin the plan for financial provision and for the shape of later working life.",
    ], note="A sustainable life is built in sequence rather than announced all at once. Each step is completed before the next is attempted.")
