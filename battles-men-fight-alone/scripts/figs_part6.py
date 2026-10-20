"""Figures for Part Six — The Battles Nobody Sees (Chapters 21-24)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Chapter 21
@_fig("fig-21-01")
def fig_21_01():
    d.compare("fig-21-01", "Conduct that widens the gap", [
        "Explains the position rather than stating it",
        "Declines the occasions at which questions are asked",
        "Compares the private account with other men's surfaces",
        "Carries the material alone and does not test it aloud",
        "Postpones the disclosure to a later and better moment",
    ], "Conduct that narrows the gap", [
        "States the position accurately, once, without apology",
        "Names the material to one person who can hold it",
        "Compares conduct and effort, not standing and surfaces",
        "Tests the account aloud in a setting with no stake in it",
        "Discloses at the level the man can afford, now",
    ], w=4.7)


# ---------------------------------------------------------------- Chapter 22
@_fig("fig-22-01")
def fig_22_01():
    d.cycle("fig-22-01", [
        "The cue|A time, a place, a state, or a person. The recurrence that begins the episode.",
        "The private episode|The behaviour occurs out of view, and the concealment begins with it.",
        "The relief|The function is served — an hour of quiet, an hour of escape, a discharge of tension.",
        "The account|The episode is added to the private record and is not recounted to anybody.",
        "The shame|The record grows, and the man's estimate of himself falls with it.",
        "The isolation|The material is withheld from everyone, and the withholding removes the correction.",
    ], centre="The cycle", w=4.5, h=4.5)


# ---------------------------------------------------------------- Chapter 23
@_fig("fig-23-01")
def fig_23_01():
    d.sequence("fig-23-01", [
        "Use|The behaviour is chosen, is under the man's control, and has not displaced anything. Required: an accurate count of the frequency and the function it serves.",
        "Misuse|Consequences begin — sleep, money, obligations, temper — while the behaviour remains controllable. Required: an honest account to one person and a change of arrangement.",
        "Early dependence|The behaviour is required rather than chosen: it is used to manage a state and the man has begun to conceal it. Required: structured change, a treatment assessment, and the removal of the cue.",
        "Established dependence|Control has been lost in specific and measurable respects, and the concealment is now habitual. Required: professional treatment, assessment of related conditions, and the disclosure to the household.",
        "Late stage|Physical or functional consequences have arrived, and the arrangements of the man's life have been reorganised around the behaviour. Required: treatment, medical care, and reconstruction of the arrangements.",
    ], note="The window in which a change of pattern is achievable without professional treatment closes earlier than most men assume — generally within the period described in the third stage.")


# ---------------------------------------------------------------- Chapter 24
@_fig("fig-24-01")
def fig_24_01():
    d.iceberg(
        "fig-24-01",
        "What others see: the position, the title, the income, the household",
        [
            "The roles that occupied the days: the position, the trade, the office, the shift.",
            "The standing the position supplied: being consulted, being expected, being addressed by a title.",
            "The structure the work supplied: the hours, the place, the people, the purpose of the morning.",
            "The material the work supplied: the income, the household's arrangements, the plans it funded.",
            "The account the man held of himself: the sentence he used to describe who he is.",
        ],
        w=4.7, h=4.6,
        visible_label="WHAT IS REMOVED FIRST — THE VISIBLE POSITION",
        hidden_label="WHAT THE RECONSTRUCTION REQUIRES — MEANING, MATERIAL, RELATIONSHIP",
        water_label="the point at which the role is removed",
    )
