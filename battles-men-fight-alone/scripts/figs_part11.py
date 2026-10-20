"""Figures for Part Eleven — Rebuilding a Man's Life (Chapters 38-40)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Chapter 38
@_fig("fig-38-01")
def fig_38_01():
    d.sequence("fig-38-01", [
        "The first period — four tasks|Safety, including the man's life and his household's. Information: the written statement of the position, before any decision of consequence. The triage of the obligations into the legally unavoidable, the negotiable, and the moral. One ally who knows the whole position.",
        "The errors that set the starting position|Concealment; panic borrowing; the rapid sale of assets; the isolated major decision; the revenge and litigation impulse; drinking and numbing; the attempt to restore the former position immediately.",
        "The reckoning|The six sections: the assets, the liabilities, the income and the requirements, the capacities, the obligations of standing, and what remains intact — completed with the accurate description of the position and the account of the failure.",
        "The reconstruction, in order|One: stabilise the position. Two: restore income. Three: settle the obligations. Four: restore standing. Five: the relationships and the household. Six: the new construction.",
        "The household|The disclosure with the statement and the plan; the household's own arrangements; the household's role in the reconstruction; the household's own people and rest. The reconstruction is conducted with the household and not around it.",
    ], note="The order is mechanical rather than temperamental: the settlement requires the income, the standing requires the settlement, and the largest opportunities require the standing.")


# ---------------------------------------------------------------- Chapter 39
@_fig("fig-39-01")
def fig_39_01():
    d.compare("fig-39-01", "The six stages to coldness", [
        "The man's states are met with a consequence, and concealment produces a better outcome.",
        "He acquires the composed exterior, and it is rewarded.",
        "The technique is extended into the settings where it has no function: marriage, household, friendship, himself.",
        "He stops registering the states: tiredness for grief, irritation for fear, nothing for what he cannot name.",
        "The states are discharged elsewhere, generally into the household.",
        "He becomes the exterior: the position, the function, the provision, and nothing outside it.",
    ], "The four competences of strength", [
        "Registration: the capacity to identify the state, its trigger, and its likely effect on conduct.",
        "Regulation: holding the state without suppressing it or being conducted by it.",
        "Expression: stating the material where stating it is useful, at the level the setting permits.",
        "Endurance: carrying what is unresolved, through a period, without dumping it on others.",
    ], w=4.7, h=4.8)


# ---------------------------------------------------------------- Chapter 40
@_fig("fig-40-01")
def fig_40_01():
    d.cards("fig-40-01", [
        "The first list: what I keep|The obligations actually owed, each with its arrangement. In a man's own audit this list is generally larger than his fear of the exercise suggests.",
        "The second list: what I set down|The obligations that were never his; the positions held for standing; the arrangements maintained through inertia; the conduct that consumes time without producing anything. Releases take three forms: the closure, the transfer, the reduction.",
        "The third list: what I take up|The unfinished item still available; the item never begun; the relationship to be constructed rather than maintained; the conduct that is the man's own. Each must be specific, dated, and stated with a first step.",
        "The four questions|Is it owed? Do I want it? Would I take it up now? What would its ending require?",
    ], note="The third list is conducted first. A man who has taken something up conducts the reductions as the rearrangement of his life rather than as the surrender of it.", cols=2)
