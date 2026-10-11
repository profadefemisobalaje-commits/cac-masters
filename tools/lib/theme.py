"""Design tokens for the CPY lecture-video series.

One place to change colour, type and geometry for all 448 lectures.
Canvas is 1920x1080 (16:9), rendered at 2x for crisp video downscale.
"""
from __future__ import annotations
import os
from PIL import ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT_DIR = os.path.join(ROOT, "assets", "fonts")

# ---------------------------------------------------------------- canvas
W, H = 1920, 1080
SUPERSAMPLE = 1          # render at native 1920x1080
MARGIN_X = 104
MARGIN_TOP = 0
CONTENT_TOP = 214        # first pixel below the header band
CONTENT_BOTTOM = H - 96  # last pixel above the footer rule

# ---------------------------------------------------------------- palette
INK        = (15, 42, 68)        # navy - headings, header band
INK_DEEP   = (10, 29, 47)        # gradient end
ACCENT     = (13, 148, 148)      # teal - rules, bullets, emphasis
ACCENT_DK  = (9, 108, 110)
GOLD       = (214, 158, 54)      # highlight / callout
PAPER      = (255, 255, 255)
PAPER_ALT  = (246, 249, 251)     # subtle panel
RULE       = (219, 228, 235)
TEXT       = (28, 39, 51)
TEXT_MUTED = (106, 122, 138)
TEXT_LIGHT = (232, 240, 247)
WHITE      = (255, 255, 255)

# ---------------------------------------------------------------- type
FONTS = {
    "light":  "Roboto-Light.ttf",
    "reg":    "Roboto-Regular.ttf",
    "italic": "Roboto-Italic.ttf",
    "med":    "Roboto-Medium.ttf",
    "bold":   "Roboto-Bold.ttf",
    "bi":     "Roboto-BoldItalic.ttf",
    "mono":   "DejaVuSansMono.ttf",
}
_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    key = (weight, size)
    if key not in _cache:
        path = os.path.join(FONT_DIR, FONTS.get(weight, FONTS["reg"]))
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


# ---------------------------------------------------------------- type scale
S = {
    "eyebrow":   26,
    "title_xl":  82,
    "title_l":   62,
    "title":     52,
    "title_s":   44,
    "subtitle":  32,
    "body":      31,
    "body_s":    28,
    "bullet":    30,
    "bullet_s":  30,
    "caption":   24,
    "footer":    20,
    "quote":     42,
    "stat":      92,
}

# ---------------------------------------------------------------- spacing
GAP = 18
LINE = 1.42          # line-height multiplier for body copy
BULLET_INDENT = 46
BULLET_LVL2_INDENT = 96


def mix(a: tuple, b: tuple, t: float) -> tuple:
    """Linear blend between two RGB colours; t=0 -> a, t=1 -> b."""
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))
