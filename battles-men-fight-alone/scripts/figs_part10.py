"""Figures for Part Ten — Healing the Man Behind the Silence (Chapters 34-37)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Chapter 34
@_fig("fig-34-01")
def fig_34_01():
    d.compare("fig-34-01", "The three criteria and three mechanisms", [
        "Criterion one: the silence no longer protects what it was meant to protect.",
        "Criterion two: the material is operating somewhere — body, temper, attention, avoidance.",
        "Criterion three: maintaining the silence has become an activity in the man's life.",
        "Mechanism one: suppression removes expression and leaves the physiological load.",
        "Mechanism two: concealment consumes attention and reduces working capacity.",
        "Mechanism three: conduct alters — avoidance, compensating behaviour, severity at home.",
    ], "Where the requirement changes", [
        "Where the material is operating in the man's body or judgement, an arrangement is required.",
        "Where the household is affected by consequences it cannot explain, the fact must be supplied.",
        "Where the cost is rising with delay, the rate of increase is set by the delay itself.",
        "Five dangerous silences: a risk to life, an addiction, violence, a medical condition, a financial collapse.",
        "The first of these requires today's professional assessment, not a plan.",
        "The others require the four decisions and the four-part statement.",
    ], w=4.7, h=4.8)


# ---------------------------------------------------------------- Chapter 35
@_fig("fig-35-01")
def fig_35_01():
    d.compare("fig-35-01", "The four costs of asking", [
        "Standing: real in the competitive setting, the exchange among men, the regulated post, the small community, and the family whose structure is the man's assistance.",
        "Dependence: real, and managed by the professional arrangement, the reciprocal arrangement, the stated terms, and the group.",
        "Obligation: real, discharged by terms agreed at the time, and generally smaller than the account the man has already established in the other direction.",
        "Exposure: real; managed by the graduated form and the choice of recipient.",
    ], "What makes a request answerable", [
        "Part one: the specific thing, stated as a task rather than as a condition.",
        "Part two: the reason, in one sentence, without the history.",
        "Part three: the scale and the limit — the hours, the amount, the number of occasions.",
        "Part four: what the man will do himself, and when he will report back.",
    ], w=4.7, h=4.7)


# ---------------------------------------------------------------- Chapter 36
@_fig("fig-36-01")
def fig_36_01():
    d.sequence("fig-36-01", [
        "Condition one — safety and stability|Physical safety, sleep, food, shelter and medical care, the absence of an active emergency, and at least one arrangement that can hold what will be surfaced. This condition comes first, and the work returns to it whenever an event removes it.",
        "Condition two — the account|The material described in a form the man can produce and available to at least one recipient beyond him: the written record, the spoken account to a witness or a professional, the account in a group. What is described is what occurred, in sequence, with the facts.",
        "Condition three — mourning and the conduct of what was lost|The loss acknowledged at its actual size and marked in the man's own form: the date, the place, the witness, the conduct in the person's name. A loss that has not been counted keeps the material invested in an account in which it does not appear.",
        "Condition four — reconnection|The man takes up something that requires him and that is not the material: the arrangements of Chapter 27, the measures of Chapters 24, 25 and 28, the conduct of Chapter 29, the household's life. Recovery is completed here and not in the material.",
    ], note="The first measure of progress is the existence of the arrangements, not the state of the man. The stages are conducted in parallel as well as in sequence, and a return to the first condition after a loss of stability is normal.")


# ---------------------------------------------------------------- Chapter 37
@_fig("fig-37-01")
def fig_37_01():
    d.compare("fig-37-01", "Why rest is refused", [
        "The man's account of himself is what he does: stopping feels like a pause in standing, not in activity.",
        "The rule that worth equals output, with a short accounting period, so rest registers as a loss.",
        "The household's requirement as the man understands it — generally more demanding than anything stated.",
        "The environment's reinforcement: continuous work is rewarded and its absence is recorded informally.",
        "The two prohibitions: on stopping, and on being restored.",
    ], "What the arrangement requires", [
        "The sleep specification: hours, conditions, the telephone out of the room.",
        "The daily measure: one category, fixed time, small enough to keep.",
        "The weekly specification: the non-working period, with the telephone's arrangement.",
        "The annual specification, plus the written boundary of Chapter 31.5.",
        "The stated arrangement with the household: what changes, what does not, what is required.",
    ], w=4.7, h=4.7)
