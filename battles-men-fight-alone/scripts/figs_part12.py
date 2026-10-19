"""Figures for Part Twelve — From Silent Survival to Purposeful Living (Chapters 41-45)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Chapter 41
@_fig("fig-41-01")
def fig_41_01():
    d.compare("fig-41-01", "The obligation the clause contains", [
        "Provision: the household has what it requires.",
        "Composure: regulation of one's states, and their appropriate conduct in the setting.",
        "Self-sufficiency: capability, and responsibility for what is in one's position.",
        "Control: accountability for the household's position.",
        "Achievement: meaningful work, and products that are real.",
    ], "The addition the clause makes", [
        "Exclusivity, silence, personalisation, and anonymity — so that the man's value is computed at his exhaustion.",
        "Concealment extended into the settings where no requirement exists, and into the man's own access to his states.",
        "That the capability be conducted alone, which removes the instruments on which capability depends.",
        "The conversion of accountability into authority over persons, which reduces the household's information and capacity.",
        "The identification of the man with his position, so that a reduction in the position is a reduction in the man.",
    ], w=4.7, h=4.9)


# ---------------------------------------------------------------- Chapter 42
@_fig("fig-42-01")
def fig_42_01():
    d.sequence("fig-42-01", [
        "The statement|The six sections of the position, in figures, extended by two items: the fact, and the parties who must not learn it. No decision of consequence is taken before it exists.",
        "One person|The party who receives the whole position, including what is concealed from everybody else, together with the decisions the man is inclined to take too quickly.",
        "The household|The four arrangements, conducted before the reductions and on the true position, so that the household's own arrangements are built on the actual size of things.",
        "The professionals|The practitioner, the accountant, the lawyer, the clinician — engaged before the reductions, since reductions conducted without them are frequently conducted in the wrong order.",
        "The reductions, in three layers|First the items nobody sees; then the items some people see, each with a notice; then the items everybody sees, with the household's participation.",
        "The reconstruction at the true level|The position conducted at its actual size: the vigilance removed, the escalation stopped, the decisions taken on the real position.",
    ], note="Each step produces the condition the next requires. The position conducted at its true level is generally more productive than the false one.")


# ---------------------------------------------------------------- Chapter 43
@_fig("fig-43-01")
def fig_43_01():
    d.sequence("fig-43-01", [
        "The permission|A stated availability, in ordinary language, from a named adult: what he will listen to, what he will keep confidential, and the one limit that safety imposes.",
        "The cheap request|The boy's first use of the permission concerns a small matter. It is a test of the arrangement, and it is lost if the adult treats it as unimportant.",
        "The reception|Thanks for the disclosure, acknowledgement of the difficulty, and one question. No immediate solution, no reassurance, no report to another adult.",
        "The action|Something in the world changes after the boy speaks: an appointment is made, a teacher is seen, an instrument is supplied, an arrangement is kept.",
        "The repetition|The adult remains available through the boy's withdrawal, states the availability again after an interval, and makes no demand for an account of the silence.",
    ], note="The sequence fails at the point where any condition is omitted. The most frequent failures are the cheap request dismissed as trivial and the action that never follows.")


@_fig("fig-43-02")
def fig_43_02():
    d.sequence("fig-43-02", [
        "Demonstration|The adult conducts the competence in the boy's presence and names what he is doing, in one or two sentences, at the moment it occurs.",
        "Rehearsal|The boy conducts the competence in a setting of low stakes, while calm, and repeats it until the sentence is available without effort.",
        "Feedback|The adult states what the boy did and what it produced, without evaluating the boy, and states the next attempt where the first failed.",
        "Application|The boy conducts the competence in a setting of real stakes, with the adult available but not present, and with the adult tolerating the failure.",
    ], note="The method is an apprenticeship, not a lesson. Omission of rehearsal produces a boy who can recite the vocabulary; omission of application produces a boy who can use it only in the adult's presence.")


# ---------------------------------------------------------------- Chapter 44
@_fig("fig-44-01")
def fig_44_01():
    d.compare("fig-44-01", "What the event supplies", [
        "Accurate information about the world: the untested assumption, disclosed.",
        "Accurate information about the man: his conduct under pressure, and his actual limit.",
        "The identification of his actual parties — who arrived, and who did not.",
        "The reduction of a fear that had been larger than the event.",
        "A competence that ordinary circumstances would not have required.",
    ], "What the event does not supply", [
        "Meaning. The meaning is assigned, and the assignment is frequently made in the first weeks and never revised.",
        "Permission. Support and time are owed; a licence to reduce other people is not.",
        "Wisdom. This is the chapter's central correction: wisdom is a set of practices, not a deposit.",
        "Community. Support arrives in the first month and is frequently absent by the sixth.",
        "Virtue. Men emerge from severe difficulty more generous and more cruel.",
    ], w=4.75, h=3.95)


@_fig("fig-44-02")
def fig_44_02():
    d.cycle("fig-44-02", [
        "The injury|Something is done, and it is real.",
        "The unacknowledged cost|No apology, no correction, no hearing.",
        "The ledger of the owed|What he is owed, held alone.",
        "The narrowing|Attention contracts; new events are read through old categories.",
        "The confirming arrangement|His conduct produces the evidence for his account.",
    ], centre="The loop", w=4.7, h=4.9, rx=33, size=6.8)
