"""Content objects for a course."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Week:
    n: int
    title: str
    short: str
    standfirst: str
    epigraph: str
    epigraph_src: str
    keywords: list[str]
    outcomes: list[str]
    concepts: list[tuple[str, str]]
    lectures: list[dict]
    figure: dict
    vignette: dict
    skills: dict
    seminar: list[str]
    assignment: dict
    readings: list[tuple[str, str]]
    synthesis: tuple[str, str]
    next: dict
    fig_key: str = ""
    notes: str = ""

    def __post_init__(self):
        if not self.fig_key:
            self.fig_key = f"w{self.n:02d}"


def week(**kw) -> Week:
    return Week(**kw)


def lecture(kicker, title, bullets, panel_text, panel_title="CLINICAL IMPLICATION", notes=""):
    return dict(kicker=kicker, title=title, bullets=bullets, panel_text=panel_text,
                panel_title=panel_title, notes=notes)
