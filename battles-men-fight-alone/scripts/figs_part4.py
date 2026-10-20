"""Figures for Part Four — The Battles of Love and Relationships (Chapters 13-16)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# --------------------------------------------------------------- Chapter 13
@_fig("fig-13-01")
def fig_13_01():
    d.cycle("fig-13-01", [
        "The loss occurs, and the man tells nobody what it costs him",
        "The feeling has no name and no place to be stated",
        "He increases work, drink, or activity to occupy the hours",
        "The grief is not processed, and it waits",
        "It returns as irritability, numbness, or a flatness he cannot explain",
        "He concludes that he has changed, and reduces his attachments further",
    ], centre="Concealed relationship grief")


# --------------------------------------------------------------- Chapter 14
@_fig("fig-14-01")
def fig_14_01():
    d.compare("fig-14-01", "What the man brings to the conversation", [
        "A conclusion he has carried alone, often for years, and a decision to state it once.",
        "A request for understanding that has never been made in specific terms.",
        "A fear that stating the position will be heard as a complaint about her.",
        "The expectation that one conversation will settle a long arrangement.",
    ], "What the conversation requires", [
        "The material stated in sequence, with the conclusion at the end rather than the start.",
        "A specific statement of what he needs: to be heard, to be believed, or to be helped.",
        "A stated distinction between what she did and what he is describing.",
        "A second conversation fixed in advance, so that the first one is not asked to carry everything.",
    ], w=4.7, h=4.5)


# --------------------------------------------------------------- Chapter 15
@_fig("fig-15-01")
def fig_15_01():
    d.sequence("fig-15-01", [
        "The account is opened|Each sacrifice is made on the understanding that it is noticed and that it counts.",
        "The contributions continue unrecorded|Nobody's ledger is written down, and each party's record is kept privately.",
        "The two accounts diverge|She counts what she has done that he has not acknowledged; he counts what he has carried that she has not seen.",
        "The withdrawal begins|Discretionary effort reduces, and the practical arrangements remain in place while the marriage's content does not.",
        "The arrival of the material|One event — a remark, a refusal, an absence — releases the accumulated account, and the quarrel is about the event rather than the ledger.",
    ], note="The ledger is not a fault in either party. It is what happens when a long arrangement is conducted without either party ever stating its balance.")


# --------------------------------------------------------------- Chapter 16
@_fig("fig-16-01")
def fig_16_01():
    d.stairs("fig-16-01", [
        "The acute period|Days to weeks: the injury is overwhelming, and the tasks are safety, sleep, and one person told.",
        "The reconstruction|Weeks to months: the facts are separated from the verdict, the account is written, and activity is restored.",
        "The examination|Months: what the injury says about the people involved, and what it does not say about him.",
        "The restoration|Months to years: the capacity to trust again is exercised in graduated steps rather than decided.",
        "The revision|The injury becomes part of the man's account of himself without being the verdict on it.",
    ], note="The phases overlap and are not followed in a strict sequence; a return to an earlier phase after a new injury is ordinary rather than a failure.")
