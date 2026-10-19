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
