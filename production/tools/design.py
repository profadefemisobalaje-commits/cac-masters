"""Premium presentation design system for
'WHAT YOU MAY NOT KNOW ABOUT CHRISTIAN THEOLOGY'.

Design master: 3840 x 2160 (16:9). Colours, type scale and layout primitives.
"""
from PIL import Image, ImageDraw, ImageFont

# ---- Master canvas ----
W, H = 3840, 2160
MARGIN = 200            # safe margin for broadcast / player chrome
CONTENT_W = W - 2 * MARGIN

# ---- Palette (master prompt, section 6) ----
NAVY       = (10, 22, 40)      # midnight navy  — authority, depth
NAVY_DEEP  = (5, 12, 24)       # vignette / gradient base
GOLD       = (200, 162, 74)    # antique gold   — premium scholarly accent
GOLD_SOFT  = (216, 190, 138)
IVORY      = (245, 241, 230)   # readability, timeless elegance
BURG       = (110, 20, 35)     # deep burgundy  — selective accents
CHARCOAL   = (43, 43, 43)      # sophisticated contrast
IVORY_DIM  = (196, 194, 186)
NAVY_MID   = (22, 40, 66)

FONT_DIR = "/home/user/cac-masters/production/assets/fonts/ttf/"

FACES = {
    "display":  "Cinzel",                 # main titles
    "title_alt":"CormorantGaramond",
    "heading":  "Montserrat",             # supporting headings
    "body":     "Inter",                  # body text
    "quote":    "EBGaramond",             # biblical quotations
}


def font(kind, weight=400, size=48, italic=False):
    fam = FACES[kind]
    if italic:
        fam += "-Italic"
    return ImageFont.truetype(FONT_DIR + f"{fam}-{weight}.ttf", size)


def new_canvas():
    """Midnight-navy canvas with a soft radial deepening toward the corners."""
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    steps = 26
    for i in range(steps, 0, -1):
        t = i / steps
        r = int(t * (W * 0.72))
        col = tuple(int(NAVY[j] * (1 - 0.45 * t) + NAVY_DEEP[j] * 0.45 * t) for j in range(3))
        d.ellipse([cx - r, cy - int(r * 9 / 16), cx + r, cy + int(r * 9 / 16)], fill=col)
    return img


def frame(img, width=3, inset=150, color=GOLD, alpha=90):
    """Restrained gold keyline frame."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([inset, inset, W - inset, H - inset],
                 outline=color + (alpha,), width=width)
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"), (0, 0))
    return img


def rule(d, x0, x1, y, color=GOLD, width=5):
    d.line([x0, y, x1, y], fill=color, width=width)


def text_w(d, txt, f):
    return d.textlength(txt, font=f)


def center(d, txt, f, y, fill=IVORY, tracking=0):
    """Centred single line. tracking = extra px between chars."""
    if tracking:
        widths = [d.textlength(c, font=f) for c in txt]
        total = sum(widths) + tracking * (len(txt) - 1)
        x = (W - total) / 2
        for c, w in zip(txt, widths):
            d.text((x, y), c, font=f, fill=fill)
            x += w + tracking
    else:
        w = text_w(d, txt, f)
        d.text(((W - w) / 2, y), txt, font=f, fill=fill)


def wrap(d, txt, f, max_w):
    """Greedy word wrap to a list of lines."""
    lines, cur = [], ""
    for word in txt.split():
        trial = (cur + " " + word).strip()
        if text_w(d, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para_center(d, txt, f, y, fill=IVORY, max_w=CONTENT_W, leading=1.42):
    lines = wrap(d, txt, f, max_w)
    for ln in lines:
        center(d, ln, f, y, fill)
        y += int(f.size * leading)
    return y


def para_left(d, txt, f, x, y, fill=IVORY, max_w=CONTENT_W, leading=1.45):
    for ln in wrap(d, txt, f, max_w):
        d.text((x, y), ln, font=f, fill=fill)
        y += int(f.size * leading)
    return y


def lower_third(d, section_no, section_title, y=H - 330):
    """Consistent section lower-third: number in gold, title in ivory."""
    fnum = font("display", 700, 64)
    ftit = font("heading", 600, 58)
    d.text((MARGIN, y), f"{section_no:02d}", font=fnum, fill=GOLD)
    nw = text_w(d, f"{section_no:02d}", fnum)
    d.line([MARGIN + nw + 40, y + 12, MARGIN + nw + 40, y + 70], fill=GOLD, width=3)
    d.text((MARGIN + nw + 80, y + 6), section_title.upper(), font=ftit, fill=IVORY)


def footnote(d, txt, y=H - 215):
    """Discreet citation at slide foot."""
    f = font("body", 300, 34)
    d.text((MARGIN, y), txt, font=f, fill=IVORY_DIM)


def save(img, path):
    img.convert("RGB").save(path, optimize=True)
