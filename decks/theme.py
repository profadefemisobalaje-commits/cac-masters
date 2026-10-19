"""House style for the MFT lecture-deck collection.

A single design system, modulated by one accent colour per course.  The
typographic pairing (EB Garamond for display, Source Sans 3 for text) and the
ivory/ink/bronze palette are shared with the book project in ``book/`` so that
the two bodies of work read as one imprint.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "book" / "fonts"
ASSETS = ROOT / "decks" / "assets"

# Canvas -------------------------------------------------------------------
# 960 x 540 pt == 13.333 x 7.5 in (16:9).  One point on the page is one point
# in the PDF, which keeps the two renderers in the same coordinate system.
W, H = 960.0, 540.0
M = 68.0                      # outer margin
CONTENT_W = W - 2 * M         # 824

# Type ---------------------------------------------------------------------
FONT_FILES = {
    ("display", "regular", False): "EBGaramond-Regular.otf",
    ("display", "medium", False): "EBGaramond-Medium.otf",
    ("display", "semibold", False): "EBGaramond-SemiBold.otf",
    ("display", "bold", False): "EBGaramond-Bold.otf",
    ("display", "regular", True): "EBGaramond-Italic.otf",
    ("display", "medium", True): "EBGaramond-Italic.otf",
    ("display", "semibold", True): "EBGaramond-SemiBoldItalic.otf",
    ("display", "bold", True): "EBGaramond-BoldItalic.otf",
    ("body", "light", False): "SourceSans3-Light.otf",
    ("body", "regular", False): "SourceSans3-Regular.otf",
    ("body", "semibold", False): "SourceSans3-Semibold.otf",
    ("body", "bold", False): "SourceSans3-Bold.otf",
    ("body", "light", True): "SourceSans3-It.otf",
    ("body", "regular", True): "SourceSans3-It.otf",
    ("body", "semibold", True): "SourceSans3-SemiboldIt.otf",
    ("body", "bold", True): "SourceSans3-BoldIt.otf",
}

FAMILY = {"display": "EB Garamond", "body": "Source Sans 3"}

# Palette ------------------------------------------------------------------
PAPER = "#F8F3E9"
PAPER_ALT = "#F1E8D8"
INK = "#16262C"
INK_SOFT = "#33474D"
MUTED = "#5D6A6C"
HAIR = "#D9CDB6"
GOLD = "#A9843F"
GOLD_LIGHT = "#C9AF7E"
DARK = "#0C181D"
DARK_2 = "#12262E"
DARK_TEXT = "#F3ECDD"
DARK_MUTED = "#A79E8A"


@dataclass(frozen=True)
class Palette:
    """A course palette: one accent, everything else constant."""

    accent: str
    accent_soft: str
    accent_deep: str
    paper: str = PAPER
    paper_alt: str = PAPER_ALT
    ink: str = INK
    ink_soft: str = INK_SOFT
    muted: str = MUTED
    hair: str = HAIR
    gold: str = GOLD
    gold_light: str = GOLD_LIGHT
    dark: str = DARK
    dark_2: str = DARK_2
    dark_text: str = DARK_TEXT
    dark_muted: str = DARK_MUTED


# Per-course accents.  Each is a deep, print-friendly hue that reads as a
# variation on the same imprint rather than a different brand.
ACCENTS = {
    "701": ("#7C3140", "#EDE0E1", "#4E1B26"),   # mulberry
    "702": ("#A0522D", "#F2E4DA", "#6B331A"),   # terracotta
    "703": ("#2E6B5E", "#DFEAE6", "#1B433B"),   # verdigris
    "704": ("#23395B", "#DFE4EC", "#14243C"),   # oxford
    "705": ("#4A5A6A", "#E3E7EA", "#2E3A45"),   # slate
    "706": ("#8A5A2B", "#EFE5D8", "#5C3A19"),   # bronze
    "707": ("#5B3A5E", "#E9E1EA", "#3A2340"),   # plum
    "708": ("#9A7328", "#F0E8D5", "#6A4D16"),   # ochre
    "709": ("#2F5D50", "#DFE9E4", "#1C3D34"),   # pine
    "710": ("#7A3B4A", "#EDE1E5", "#4E212C"),   # rosewood
    "711": ("#B07A2A", "#F3E9D7", "#7A5114"),   # saffron
    "712": ("#A34A2A", "#F2E2DA", "#6D2D16"),   # ember
    "713": ("#4F5D34", "#E6E9DD", "#333D1E"),   # moss
    "714": ("#3A3F6B", "#E2E3EE", "#232647"),   # indigo
    "715": ("#1F5A63", "#DDE9EA", "#123A41"),   # teal
    "716": ("#2B4C7E", "#E0E6EF", "#193152"),   # cobalt
    "717": ("#3F4A4F", "#E2E5E6", "#283034"),   # graphite
    "718": ("#7B2D3A", "#EDE0E2", "#4F1A24"),   # garnet
    "719": ("#A9762B", "#F1E7D5", "#774E14"),   # amber
    "720": ("#5E2A35", "#E9DEE0", "#3C161E"),   # burgundy
    "721": ("#405A66", "#E0E6E9", "#273B44"),   # steel
    "722": ("#6B6B3A", "#E9E9DC", "#454522"),   # olive
    "723": ("#A9553F", "#F1E3DE", "#733422"),   # coral
    "724": ("#26343A", "#DFE3E5", "#121B1F"),   # ink
    "725": ("#57406E", "#E7E2ED", "#382747"),   # violet
    "726": ("#23485C", "#DEE7EC", "#142F3D"),   # marine
    "727": ("#9A4F5A", "#F0E1E4", "#642C34"),   # rose
}


def palette_for(code: str) -> Palette:
    key = "".join(ch for ch in code if ch.isdigit())[-3:]
    accent, soft, deep = ACCENTS.get(key, ACCENTS["701"])
    return Palette(accent=accent, accent_soft=soft, accent_deep=deep)


@dataclass
class SyllabusItem:
    n: int
    title: str
    short: str


@dataclass
class Course:
    code: str            # "MFT 701"
    title: str
    short: str           # running-head abbreviation
    semester: str        # "Semester I"
    units: str           # as printed in the curriculum
    syllabus: list = field(default_factory=list)   # all weeks (titles)
    weeks: list = field(default_factory=list)      # weeks with content
    year: str = "2026"
    programme: str = "Master of Marriage and Family Therapy"

    @property
    def total(self) -> int:
        return len(self.syllabus) or len(self.weeks)

    @property
    def slug(self) -> str:
        return self.code.replace(" ", "-")

    @property
    def palette(self) -> Palette:
        return palette_for(self.code)


def hex_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
