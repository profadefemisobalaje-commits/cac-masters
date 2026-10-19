"""A tiny absolute-positioned layout engine.

Slides are described once as a list of primitives (rectangles, rules, text,
images).  The PPTX and PDF renderers consume the same list, so the two
deliverables are siblings rather than look-alikes.

Text is pre-wrapped here using the actual font files and real font metrics.
That buys three things: no text overflow in PowerPoint, identical line breaks
in both formats, and typographic control (avoiding one-word last lines).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from PIL import ImageFont

from . import theme


# --------------------------------------------------------------------------
# Font metrics
# --------------------------------------------------------------------------
_FONT_CACHE: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font_path(family: str, weight: str = "regular", italic: bool = False) -> Path:
    key = (family, weight, italic)
    if key not in theme.FONT_FILES:
        key = (family, "regular", italic) if (family, "regular", italic) in theme.FONT_FILES else (family, "regular", False)
    return theme.FONTS / theme.FONT_FILES[key]


def _pil(family: str, weight: str, italic: bool, size: float) -> ImageFont.FreeTypeFont:
    path = font_path(family, weight, italic)
    k = (str(path), max(1, int(round(size * 4))))   # measure at 4x for precision
    if k not in _FONT_CACHE:
        _FONT_CACHE[k] = ImageFont.truetype(str(path), max(1, int(round(size * 4))))
    return _FONT_CACHE[k]


def measure(s: str, family: str, weight: str, italic: bool, size: float,
            tracking: float = 0.0) -> float:
    if not s:
        return 0.0
    f = _pil(family, weight, italic, size)
    return (f.getlength(s) / 4.0) + tracking * max(0, len(s) - 1)


def wrap(s: str, family: str, weight: str, italic: bool, size: float,
         width: float, tracking: float = 0.0) -> list[str]:
    """Greedy wrap with a widow guard, measured in real font units."""
    out: list[str] = []
    for para in s.split("\n"):
        words = para.split()
        if not words:
            out.append("")
            continue
        line: list[str] = []
        for w in words:
            trial = " ".join(line + [w])
            if not line or measure(trial, family, weight, italic, size, tracking) <= width:
                line.append(w)
            else:
                out.append(" ".join(line))
                line = [w]
        if line:
            out.append(" ".join(line))
    # widow guard: pull a word down if the last line is a lonely scrap
    if len(out) >= 2:
        last = out[-1]
        wl = measure(last, family, weight, italic, size, tracking)
        if wl < width * 0.16 and len(last.split()) == 1 and len(out[-2].split()) > 2:
            prev = out[-2].split()
            out[-2] = " ".join(prev[:-1])
            out[-1] = prev[-1] + " " + last
    return out


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------
@dataclass
class Rect:
    x: float
    y: float
    w: float
    h: float
    fill: str | None = None
    alpha: float = 1.0
    line: str | None = None
    lw: float = 0.6
    radius: float = 0.0

    kind = "rect"


@dataclass
class Rule:
    x1: float
    y1: float
    x2: float
    y2: float
    color: str
    lw: float = 0.6
    dash: str | None = None

    kind = "rule"


@dataclass
class Text:
    x: float
    y: float
    w: float
    lines: list[str]
    family: str
    weight: str
    italic: bool
    size: float
    color: str
    leading: float = 1.4
    align: str = "left"
    tracking: float = 0.0
    alpha: float = 1.0

    kind = "text"

    @property
    def line_height(self) -> float:
        return self.size * self.leading

    @property
    def height(self) -> float:
        return len(self.lines) * self.line_height

    def line_x(self, i: int) -> float:
        if self.align == "left":
            return self.x
        txt_w = measure(self.lines[i], self.family, self.weight, self.italic,
                        self.size, self.tracking)
        if self.align == "center":
            return self.x + (self.w - txt_w) / 2
        return self.x + self.w - txt_w


@dataclass
class Image:
    path: str
    x: float
    y: float
    w: float
    h: float

    kind = "image"


@dataclass
class Ellipse:
    x: float
    y: float
    w: float
    h: float
    fill: str | None = None
    alpha: float = 1.0
    line: str | None = None
    lw: float = 0.6

    kind = "ellipse"


# --------------------------------------------------------------------------
# Slide / Deck
# --------------------------------------------------------------------------
@dataclass
class Slide:
    ops: list = field(default_factory=list)
    bg: str = theme.PAPER
    texture: str | None = None
    notes: str = ""
    kind: str = "content"

    # -- primitives ------------------------------------------------------
    def rect(self, x, y, w, h, fill=None, alpha=1.0, line=None, lw=0.6, radius=0.0):
        self.ops.append(Rect(x, y, w, h, fill, alpha, line, lw, radius))
        return self

    def ellipse(self, x, y, w, h, fill=None, alpha=1.0, line=None, lw=0.6):
        self.ops.append(Ellipse(x, y, w, h, fill, alpha, line, lw))
        return self

    def rule(self, x1, y1, x2, y2, color=None, lw=0.6, dash=None):
        self.ops.append(Rule(x1, y1, x2, y2, color or theme.GOLD, lw, dash))
        return self

    def hline(self, x, y, w, color=None, lw=0.6, dash=None):
        return self.rule(x, y, x + w, y, color, lw, dash)

    def vline(self, x, y, h, color=None, lw=0.6, dash=None):
        return self.rule(x, y, x, y + h, color, lw, dash)

    def text(self, x, y, w, s, *, family="body", weight="regular", italic=False,
             size=11.0, color=None, leading=1.45, align="left", tracking=0.0,
             alpha=1.0, upper=False, dry=False) -> float:
        s = s.upper() if upper else s
        lines = wrap(s, family, weight, italic, size, w, tracking)
        op = Text(x, y, w, lines, family, weight, italic, size,
                  color or theme.INK, leading, align, tracking, alpha)
        if not dry:
            self.ops.append(op)
        return op.height

    def text_block(self, x, y, w, s, **kw) -> Text:
        """Return the Text op itself (useful for measuring before placing)."""
        s = s.upper() if kw.pop("upper", False) else s
        family = kw.pop("family", "body")
        weight = kw.pop("weight", "regular")
        italic = kw.pop("italic", False)
        size = kw.pop("size", 11.0)
        tracking = kw.pop("tracking", 0.0)
        leading = kw.pop("leading", 1.45)
        align = kw.pop("align", "left")
        color = kw.pop("color", theme.INK)
        alpha = kw.pop("alpha", 1.0)
        lines = wrap(s, family, weight, italic, size, w, tracking)
        return Text(x, y, w, lines, family, weight, italic, size, color,
                    leading, align, tracking, alpha)

    def add(self, op):
        self.ops.append(op)
        return op

    def image(self, path, x, y, w=None, h=None):
        from PIL import Image as PILImage
        with PILImage.open(path) as im:
            iw, ih = im.size
        if w is None and h is not None:
            w = h * iw / ih
        if h is None and w is not None:
            h = w * ih / iw
        self.ops.append(Image(str(path), x, y, w, h))
        return self

    # -- branded furniture ----------------------------------------------
    def header(self, course, kicker_right: str | None = None, rule=True):
        self.text(theme.M, 30, 560, f"{course.code}  ·  {course.short.upper()}",
                  size=7.4, weight="semibold", color=theme.MUTED,
                  tracking=1.9, upper=True, leading=1.2)
        if kicker_right:
            self.text(theme.W - theme.M - 260, 30, 260, kicker_right,
                      size=7.4, weight="semibold", color=theme.GOLD,
                      tracking=1.9, upper=True, align="right", leading=1.2)
        if rule:
            self.hline(theme.M, 45, theme.CONTENT_W, theme.HAIR, 0.5)
        return self

    def footer(self, course, folio: str):
        self.hline(theme.M, 500, theme.CONTENT_W, theme.HAIR, 0.5)
        self.text(theme.M, 508, 620, f"{course.programme}  ·  {course.semester}",
                  size=7.2, color=theme.MUTED, tracking=0.4, leading=1.2)
        self.text(theme.W - theme.M - 140, 508, 140, folio,
                  size=7.2, color=theme.MUTED, align="right",
                  tracking=1.2, leading=1.2)
        return self


class Deck:
    def __init__(self, course: theme.Course):
        self.course = course
        self.slides: list[Slide] = []

    def slide(self, bg=None, texture=None, notes="", kind="content") -> Slide:
        pal = self.course.palette
        s = Slide(bg=bg or pal.paper,
                  texture=texture if texture is not None else (theme.ASSETS / "paper.jpg"),
                  notes=notes, kind=kind)
        if str(s.texture) == str(theme.ASSETS / "dark.jpg"):
            pass
        self.slides.append(s)
        return s

    def dark_slide(self, notes="", kind="dark") -> Slide:
        return self.slide(bg=self.course.palette.dark,
                          texture=theme.ASSETS / "dark.jpg", notes=notes, kind=kind)
