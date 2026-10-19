"""Figures for Part Two — The Battles of the Mind (Chapters 5-8)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Chapter 5
@_fig("fig-05-01")
def fig_05_01():
    d.compare(
        "fig-05-01",
        "The surface others see", [
            "Decisiveness and command of detail",
            "Long hours and thorough preparation",
            "Calm under pressure",
            "Meticulous records and follow-up",
            "No complaints, no excuses",
        ],
        "The internal operation", [
            "Continuous rehearsal of what may go wrong",
            "Sleep lost to anticipation of failure",
            "Repeated checking of work and decisions",
            "Fear that a mistake will be discovered",
            "Tension held in the body, and alcohol to sleep",
        ])


@_fig("fig-05-02")
def fig_05_02():
    d.cards("fig-05-02", [
        "Income and security|Whether the work will continue; whether the salary will cover the month; whether the business will survive the quarter.",
        "Provision for dependants|School fees, medical costs, family obligations, and the arithmetic that does not close.",
        "Family relationships|A child who is drifting; a marriage that has gone quiet; a parent who is failing.",
        "Reputation and standing|What others will think; what will be said if the situation becomes known.",
        "Health|A symptom that has been ignored; a fear of a diagnosis; the body's ordinary signals read as threats.",
        "The future|Ageing, retirement, the loss of capability, and the question of what comes next.",
    ], cols=2, note="The domains that consume the attention of men under sustained strain. Source: composite illustration prepared for this edition.")


@_fig("fig-05-03")
def fig_05_03():
    d.cycle("fig-05-03", [
        "An event, act, or failure",
        "Interpretation: this reveals something about me",
        "Concealment to prevent exposure",
        "Withdrawal from those who might see it",
        "Absence of any correcting information",
        "Confirmation that the self is defective",
    ], centre="The shame cycle")


@_fig("fig-05-04")
def fig_05_04():
    matrix("fig-05-04",
           ["What it means in practice"],
           [["Risk question", "A direct question about thoughts of self-harm. Being asked is standard practice, not an accusation."],
            ["Account", "What has been happening, for how long, and what has made it better or worse."],
            ["History", "Health, family, work, relationships, sleep, alcohol, previous episodes, losses and trauma."],
            ["Formulation", "An explanation of what the clinician thinks is happening, in plain language."],
            ["Plan", "What the treatment is, how long it may take, what to expect, and what to do if matters worsen."],
            ["Review", "A date on which the plan will be reassessed, and a route for contact before then."]],
           first_w=20, size=6.8)


# ---------------------------------------------------------------- Chapter 6
@_fig("fig-06-01")
def fig_06_01():
    d.compare(
        "fig-06-01",
        "How depression is often described", [
            "Persistent sadness and tearfulness",
            "Loss of interest and pleasure",
            "Feelings of hopelessness and guilt",
            "Withdrawal from social contact",
            "Difficulty concentrating and deciding",
        ],
        "How it frequently appears in men", [
            "Irritability, anger, and low tolerance of noise or interruption",
            "Working longer, drinking more, taking risks",
            "Physical complaints: fatigue, pain, digestive problems",
            "Withdrawal into work rather than from it",
            "Emotional flatness and a sense of nothing mattering",
        ], style_r="bronze")


@_fig("fig-06-02")
def fig_06_02():
    d.cycle("fig-06-02", [
        "Low mood and depleted energy",
        "Withdrawal from people and activities",
        "Loss of the routines and contacts that sustain mood",
        "Fewer rewards, less light, less company",
        "Mood worsens and the effort required rises",
        "Further withdrawal",
    ], centre="The withdrawal cycle")


@_fig("fig-06-03")
def fig_06_03():
    d.stairs("fig-06-03", [
        "The load increases|Longer hours, more obligations, less sleep.",
        "Effort is increased|The man works harder to compensate, and reports nothing.",
        "The body reports|Sleep, appetite, tension, and pain become noticeable.",
        "Interest disappears|Nothing gives pleasure; the man concludes he has changed.",
        "Function is preserved|Work continues; the house continues; no alarm is raised.",
        "The point of no return|A small additional burden produces a collapse.",
    ], note="The warning sequence in male depression. The characteristic feature is that function is preserved longest and deteriorates last.")


@_fig("fig-06-04")
def fig_06_04():
    d.cards("fig-06-04", [
        "Talking treatments|Cognitive behavioural therapy, interpersonal therapy, and related approaches with substantial evidence for depression.",
        "Medication|Antidepressant medication, effective for moderate and severe depression, usually in combination with talking treatment.",
        "Structured self-management|Behavioural activation, exercise, sleep restoration, and activity planning, which are effective components of treatment.",
        "Peer and community support|Groups, fellowships, and mentoring, which reduce isolation and support adherence to treatment.",
        "Practical intervention|Addressing debt, housing, employment, and family crises, which frequently remove the load that maintains the depression.",
        "Crisis planning|A written plan, agreed in advance, for what to do if matters worsen or thoughts of self-harm appear.",
    ], cols=2, note="Components of evidence-based care for depression, combined according to severity and circumstances.")


# ---------------------------------------------------------------- Chapter 7
@_fig("fig-07-01")
def fig_07_01():
    d.compare(
        "fig-07-01",
        "Worth fused with performance", [
            "Self-regard rises and falls with results",
            "A lost contract feels like a personal verdict",
            "Failure cannot be described without shame",
            "Rest feels like evidence of decline",
            "Success produces no satisfaction, only relief",
        ],
        "Worth independent of performance", [
            "Self-regard survives a bad quarter",
            "A lost contract is a business event with consequences",
            "Failure can be examined and reported",
            "Rest is maintenance of the capacity to perform",
            "Success produces satisfaction that can be enjoyed",
        ])


@_fig("fig-07-02")
def fig_07_02():
    d.cycle("fig-07-02", [
        "Achievement is reached",
        "A more successful comparator is noticed",
        "The standard is revised upwards",
        "Effort increases and satisfaction declines",
        "Achievement is reached again, without pleasure",
    ], centre="The comparison spiral")


@_fig("fig-07-03")
def fig_07_03():
    d.sequence("fig-07-03", [
        "A standard is absorbed from family, culture, or peers|What a man must be to be respected.",
        "A setback occurs|A lost job, a failed business, a debt, a disappointment.",
        "The setback is interpreted as a verdict on the self|Not 'this failed' but 'I am a failure'.",
        "Shame follows, and concealment with it|The failure is hidden from those who might help.",
        "The situation deteriorates in isolation|And the original interpretation appears to be confirmed.",
    ], note="The pathway from a setback to a private crisis. The point of intervention is the third stage.")


@_fig("fig-07-04")
def fig_07_04():
    d.cards("fig-07-04", [
        "Separate the event from the self|Write down what happened in the third person, as an observer would describe it.",
        "Establish the actual position|Debts, obligations, resources, and options, on paper, without interpretation.",
        "Reduce the burden in order|Deal with the largest threat to survival first, then the rest.",
        "Report to one person|A spouse, a trusted relative, a professional, or a mentor, with a prepared account.",
        "Set a review date|A date on which the position will be reassessed, so that the failure has an end.",
    ], cols=2, note="The practical sequence for recovering from a serious disappointment or failure.")


# ---------------------------------------------------------------- Chapter 8
@_fig("fig-08-01")
def fig_08_01():
    d.rings("fig-08-01", "The man", [
        "Role: what he does and provides",
        "Reputation: what others believe about him",
        "Inner standards: what he thinks he must be",
        "Identity: the values and history he owns",
    ])


@_fig("fig-08-02")
def fig_08_02():
    d.sequence("fig-08-02", [
        "A standard is set, often unreachable|Raised by a demanding parent, a competitive school, or a family expectation.",
        "Performance is measured against the standard|Each result is examined for evidence of inadequacy.",
        "A voice is internalised|The critic's sentences become the man's own, and are spoken without being noticed.",
        "Evidence of competence is discounted|Success is attributed to luck, circumstance, or the absence of real tests.",
        "The verdict becomes permanent|The man concludes that he is an impostor and that exposure is inevitable.",
    ], note="The formation of the internal critic, and the process by which genuine achievement ceases to count.")


@_fig("fig-08-03")
def fig_08_03():
    d.compare(
        "fig-08-03",
        "The internal critic", [
            "You will never manage this",
            "They will find out eventually what you are",
            "Anyone could have done what you did",
            "You were lucky, not capable",
            "One mistake and they will all know",
        ],
        "A realistic internal voice", [
            "This is difficult, and I have handled difficult things before",
            "I have evidence of competence, and I also have limits",
            "The work I did was mine, and it produced the result it produced",
            "Circumstances helped, and my decisions contributed",
            "Mistakes are expected, and mine have been survivable so far",
        ], style_l="bronze", style_r="teal")


@_fig("fig-08-04")
def fig_08_04():
    d.cards("fig-08-04", [
        "Keep an evidence file|A written record of outcomes, decisions, and praise, kept for the days when the memory supplies only failures.",
        "Change the standard of evidence|Judge yourself by what a fair observer with the same information would conclude.",
        "Name the critic|Recognise whose voice is speaking, and when it first spoke.",
        "Separate the task from the self|'This draft is weak' rather than 'I am weak'.",
        "Collect testimony|Ask three people who know your work to state what you actually do well, and write it down.",
        "Tolerate the discomfort of being seen|Confidence grows through exposure to being visible and surviving it.",
    ], cols=2, note="Methods for building realistic confidence, drawn from cognitive behavioural practice.")
