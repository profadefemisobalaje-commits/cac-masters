"""CAC Lecture Studio - rendering core: fonts, motifs, slide layouts.

Slides are rendered at 1920x1080 then downscaled to 1280x720 (Lanczos)
so type and rules stay razor sharp at 720p.
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "fonts")
W, H = 1920, 1080          # supersample canvas
OUT_W, OUT_H = 1280, 720   # delivery resolution

_FCACHE = {}
def font(name, size, weight=None):
    key = (name, size, weight)
    if key not in _FCACHE:
        f = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
        if weight is not None:
            try: f.set_variation_by_axes([weight])
            except Exception: pass
        _FCACHE[key] = f
    return _FCACHE[key]

def F_SERIF(size, w=600):   return font("PlayfairDisplay.ttf", size, w)
def F_SERIF_IT(size, w=600):return font("PlayfairDisplay-Italic.ttf", size, w)
def F_CAPS(size, w=600):    return font("Cinzel.ttf", size, w)
def F_SANS(size, w=500):    return font("Montserrat.ttf", size, w)

def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

def mix(c1, c2, t):
    a, b = hx(c1), hx(c2)
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if ImageDraw.Draw(Image.new("P",(2,2))).textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def vgrad(w, h, c0, c1, c2=None):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        col = mix(c0, c1, t) if t < 0.62 or c2 is None else mix(c1, c2, (t-0.62)/0.38)
        for x in range(w): px[x, y] = col
    return img

def vignette(img, strength=0.35):
    ov = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(ov)
    cx, cy = img.size[0]/2, img.size[1]/2
    rmax = math.hypot(cx, cy)
    for r in range(int(rmax), 0, -6):
        a = int(255 * strength * max(0.0, (r/rmax - 0.55) / 0.45))
        d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=min(a,255))
    ov = ov.filter(ImageFilter.GaussianBlur(60))
    dark = Image.new("RGB", img.size, (0,0,0))
    return Image.composite(dark, img, ov)

def noise(img, amt=7, seed=4):
    rnd = random.Random(seed)
    px = img.load()
    w, h = img.size
    for _ in range(w*h//220):
        x, y = rnd.randrange(w), rnd.randrange(h)
        r, g, b = px[x, y]
        dv = rnd.randint(-amt, amt)
        px[x, y] = (max(0,min(255,r+dv)), max(0,min(255,g+dv)), max(0,min(255,b+dv)))
    return img

def rule(d, x0, y, x1, color, wpx=2, cap=True):
    d.line([x0, y, x1, y], fill=color, width=wpx)
    if cap:
        d.ellipse([x0-4, y-4, x0+4, y+4], fill=color)
        d.ellipse([x1-4, y-4, x1+4, y+4], fill=color)

def diamond(d, cx, cy, r, color):
    d.polygon([(cx, cy-r), (cx+r, cy), (cx, cy+r), (cx-r, cy)], fill=color)

# ---------------------------------------------------------------- motifs
def motif(draw, name, cx, cy, S, acc, acc2, alpha_layer=None):
    """Draw a parametric vector motif centred at (cx, cy), size S."""
    t = draw if alpha_layer is None else alpha_layer
    if name == "laurel":
        for side in (-1, 1):
            for i in range(9):
                a = math.radians(115 + i*16)
                r = S*0.46
                x = cx + side*math.cos(a)*r*0.55* (i/9+0.35)
                y = cy - math.sin(a)*r + i*S*0.012
                t.ellipse([x-S*0.05, y-S*0.02, x+S*0.05, y+S*0.02], fill=acc)
    elif name == "growth":
        pts = [(cx-S*0.42, cy+S*0.34)]
        for i in range(1, 9):
            xx = cx - S*0.42 + i*S*0.105
            yy = cy + S*0.34 - S*0.62*(i/8)**1.7
            pts.append((xx, yy))
        t.line(pts, fill=acc, width=max(3, int(S*0.02)))
        for i, p in enumerate(pts[::2]): t.ellipse([p[0]-5, p[1]-5, p[0]+5, p[1]+5], fill=acc2)
    elif name == "risingpath":
        for i in range(6):
            x0 = cx - S*0.44 + i*S*0.16; y0 = cy + S*0.32 - i*S*0.12
            t.line([x0, y0, x0+S*0.10, y0-S*0.07], fill=acc, width=max(3,int(S*0.018)))
            t.ellipse([x0+S*0.10-5, y0-S*0.07-5, x0+S*0.10+5, y0-S*0.07+5], fill=acc2)
    elif name == "scales":
        t.line([cx, cy-S*0.34, cx, cy+S*0.30], fill=acc, width=max(3,int(S*0.02)))
        t.line([cx-S*0.36, cy-S*0.22, cx+S*0.36, cy-S*0.22], fill=acc, width=max(3,int(S*0.02)))
        for s in (-1, 1):
            x = cx + s*S*0.36
            t.line([x, cy-S*0.22, x, cy+S*0.02], fill=acc, width=2)
            t.arc([x-S*0.13, cy-S*0.02, x+S*0.13, cy+S*0.22], 0, 180, fill=acc, width=max(3,int(S*0.02)))
    elif name == "bridge":
        t.arc([cx-S*0.4, cy-S*0.2, cx+S*0.4, cy+S*0.42], 180, 360, fill=acc, width=max(3,int(S*0.02)))
        t.line([cx-S*0.46, cy+S*0.2, cx+S*0.46, cy+S*0.2], fill=acc, width=max(3,int(S*0.02)))
        for i in range(7):
            x = cx-S*0.39 + i*S*0.13
            t.line([x, cy+S*0.2, x, cy+S*0.06], fill=acc2, width=2)
    elif name == "circles":
        n = 8
        for i in range(n):
            a = 2*math.pi*i/n - math.pi/2
            x, y = cx + math.cos(a)*S*0.34, cy + math.sin(a)*S*0.34
            t.ellipse([x-S*0.07, y-S*0.07, x+S*0.07, y+S*0.07], outline=acc, width=3)
        t.ellipse([cx-S*0.08, cy-S*0.08, cx+S*0.08, cy+S*0.08], fill=acc2)
    elif name == "rings":
        for i, rr in enumerate((0.18, 0.30, 0.42)):
            t.ellipse([cx-S*rr, cy-S*rr, cx+S*rr, cy+S*rr], outline=acc if i%2==0 else acc2, width=3)
    elif name == "puzzle":
        s = S*0.22
        t.rounded_rectangle([cx-s*1.6, cy-s*1.1, cx+s*0.4, cy+s*0.9], radius=10, outline=acc, width=3)
        t.rounded_rectangle([cx-s*0.4, cy-s*0.1, cx+s*1.6, cy+s*1.9], radius=10, outline=acc2, width=3)
        t.ellipse([cx-s*0.75, cy-s*0.35, cx-s*0.25, cy+s*0.15], outline=acc, width=3)
    elif name == "beacon":
        x0, y0 = cx, cy+S*0.34
        t.polygon([(x0-S*0.09, y0), (x0+S*0.09, y0), (x0+S*0.05, y0-S*0.5), (x0-S*0.05, y0-S*0.5)], outline=acc, width=3)
        for a in range(-70, 71, 28):
            rad = math.radians(a-90)
            t.line([x0+math.cos(rad)*S*0.16, y0-S*0.5+math.sin(rad)*S*0.16,
                    x0+math.cos(rad)*S*0.46, y0-S*0.5+math.sin(rad)*S*0.46], fill=acc2, width=3)
    elif name == "globe":
        t.ellipse([cx-S*0.38, cy-S*0.38, cx+S*0.38, cy+S*0.38], outline=acc, width=3)
        t.ellipse([cx-S*0.16, cy-S*0.38, cx+S*0.16, cy+S*0.38], outline=acc2, width=2)
        t.line([cx-S*0.38, cy, cx+S*0.38, cy], fill=acc, width=2)
        t.arc([cx-S*0.38, cy-S*0.20, cx+S*0.38, cy+S*0.20], 20, 160, fill=acc2, width=2)
    elif name == "steps":
        for i in range(5):
            x = cx-S*0.4+i*S*0.17; y = cy+S*0.3-i*S*0.14
            t.line([x, y, x+S*0.13, y], fill=acc, width=max(3,int(S*0.02)))
            t.line([x+S*0.13, y, x+S*0.13, y-S*0.14], fill=acc2, width=2)
    elif name == "book":
        t.line([cx, cy-S*0.26, cx, cy+S*0.28], fill=acc2, width=2)
        for s in (-1, 1):
            t.arc([cx+s*S*0.02-(S*0.4 if s<0 else 0), cy-S*0.28,
                   cx+s*S*0.02+(0 if s<0 else S*0.4), cy+S*0.30], 200 if s<0 else -20, 340 if s<0 else 160, fill=acc, width=3)
    elif name == "wave":
        for k in range(3):
            pts = []
            for i in range(0, 41):
                x = cx-S*0.44 + i*S*0.022
                y = cy - S*0.1 + k*S*0.14 + math.sin(i*0.5 + k)*S*0.05
                pts.append((x, y))
            t.line(pts, fill=acc if k != 1 else acc2, width=3)
    elif name == "lotus":
        for a in (-60, -30, 0, 30, 60):
            rad = math.radians(a-90)
            t.ellipse([cx+math.cos(rad)*S*0.1-S*0.09, cy+math.sin(rad)*S*0.1-S*0.16,
                       cx+math.cos(rad)*S*0.1+S*0.09, cy+math.sin(rad)*S*0.1+S*0.16], outline=acc, width=3)
        t.ellipse([cx-S*0.06, cy+S*0.06, cx+S*0.06, cy+S*0.18], fill=acc2)
    elif name == "lens":
        t.ellipse([cx-S*0.3, cy-S*0.3, cx+S*0.18, cy+S*0.18], outline=acc, width=max(3,int(S*0.022)))
        t.line([cx+S*0.14, cy+S*0.14, cx+S*0.42, cy+S*0.42], fill=acc, width=max(4,int(S*0.03)))
        t.line([cx-S*0.18, cy-S*0.06, cx+S*0.02, cy-S*0.06], fill=acc2, width=2)
    elif name == "compass":
        t.ellipse([cx-S*0.36, cy-S*0.36, cx+S*0.36, cy+S*0.36], outline=acc, width=3)
        t.polygon([(cx, cy-S*0.26), (cx+S*0.07, cy+S*0.1), (cx, cy+S*0.02), (cx-S*0.07, cy+S*0.1)], fill=acc2)
    elif name == "star":
        pts = []
        for i in range(10):
            rr = S*0.4 if i % 2 == 0 else S*0.17
            a = math.pi*i/5 - math.pi/2
            pts.append((cx+math.cos(a)*rr, cy+math.sin(a)*rr))
        t.polygon(pts, outline=acc, width=3)
    elif name == "brain":
        t.arc([cx-S*0.34, cy-S*0.3, cx+S*0.3, cy+S*0.3], 140, 400, fill=acc, width=3)
        for i, yy in enumerate((cy-S*0.12, cy, cy+S*0.12)):
            t.arc([cx-S*0.3, yy-8, cx, yy+16], 30, 210, fill=acc2, width=2)
    elif name == "quill":
        t.line([cx-S*0.3, cy+S*0.34, cx+S*0.3, cy-S*0.34], fill=acc, width=3)
        t.arc([cx-S*0.05, cy-S*0.42, cx+S*0.42, cy+S*0.05], 200, 350, fill=acc2, width=3)
        t.arc([cx-S*0.42, cy-S*0.05, cx+S*0.05, cy+S*0.42], 20, 170, fill=acc2, width=3)
    elif name == "seal":
        t.ellipse([cx-S*0.4, cy-S*0.4, cx+S*0.4, cy+S*0.4], outline=acc, width=3)
        t.ellipse([cx-S*0.32, cy-S*0.32, cx+S*0.32, cy+S*0.32], outline=acc2, width=2)
        for i in range(12):
            a = math.pi*i/6
            t.line([cx+math.cos(a)*S*0.34, cy+math.sin(a)*S*0.34, cx+math.cos(a)*S*0.4, cy+math.sin(a)*S*0.4], fill=acc, width=2)
    elif name == "sprout":
        t.line([cx, cy+S*0.4, cx, cy-S*0.05], fill=acc2, width=3)
        t.arc([cx-S*0.3, cy-S*0.35, cx+S*0.02, cy-S*0.02], 120, 300, fill=acc, width=3)
        t.arc([cx-S*0.02, cy-S*0.35, cx+S*0.3, cy-S*0.02], 240, 60, fill=acc, width=3)
    elif name == "gavel":
        t.line([cx-S*0.3, cy+S*0.3, cx+S*0.2, cy-S*0.2], fill=acc, width=max(4,int(S*0.03)))
        t.rounded_rectangle([cx+S*0.05, cy-S*0.4, cx+S*0.42, cy-S*0.14], radius=6, outline=acc, width=3)
        t.line([cx-S*0.34, cy+S*0.38, cx+S*0.05, cy+S*0.38], fill=acc2, width=3)
    elif name == "network":
        nodes = [(cx, cy-S*0.3), (cx+S*0.32, cy-S*0.05), (cx+S*0.2, cy+S*0.3), (cx-S*0.2, cy+S*0.3), (cx-S*0.32, cy-S*0.05), (cx, cy)]
        for i in range(5):
            t.line([nodes[i], nodes[5]], fill=acc2, width=2)
            t.line([nodes[i], nodes[(i+1)%5]], fill=acc, width=2)
        for n_ in nodes: t.ellipse([n_[0]-6, n_[1]-6, n_[0]+6, n_[1]+6], fill=acc)
    elif name == "circuit":
        t.rectangle([cx-S*0.2, cy-S*0.2, cx+S*0.2, cy+S*0.2], outline=acc, width=3)
        for i, a in enumerate(((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1))):
            x2, y2 = cx+a[0]*S*0.4, cy+a[1]*S*0.4
            t.line([cx+a[0]*S*0.2, cy+a[1]*S*0.2, x2, y2], fill=acc2, width=2)
            t.ellipse([x2-4, y2-4, x2+4, y2+4], fill=acc)
    elif name == "badge":
        t.ellipse([cx-S*0.32, cy-S*0.36, cx+S*0.32, cy+S*0.28], outline=acc, width=3)
        t.polygon([(cx-S*0.16, cy+S*0.2), (cx-S*0.22, cy+S*0.46), (cx, cy+S*0.34), (cx+S*0.22, cy+S*0.46), (cx+S*0.16, cy+S*0.2)], fill=acc2)
    elif name == "shield":
        t.polygon([(cx-S*0.3, cy-S*0.34), (cx+S*0.3, cy-S*0.34), (cx+S*0.3, cy+S*0.05), (cx, cy+S*0.38), (cx-S*0.3, cy+S*0.05)], outline=acc, width=3)
        t.line([cx, cy-S*0.34, cx, cy+S*0.38], fill=acc2, width=2)
    elif name == "heart":
        t.arc([cx-S*0.32, cy-S*0.28, cx+S*0.02, cy+S*0.06], 180, 360, fill=acc, width=3)
        t.arc([cx-S*0.02, cy-S*0.28, cx+S*0.32, cy+S*0.06], 180, 360, fill=acc, width=3)
        t.line([cx-S*0.31, cy-S*0.1, cx, cy+S*0.36], fill=acc, width=3)
        t.line([cx+S*0.31, cy-S*0.1, cx, cy+S*0.36], fill=acc, width=3)
    elif name == "infinity":
        t.arc([cx-S*0.42, cy-S*0.18, cx-S*0.02, cy+S*0.18], 90, 450, fill=acc, width=3)
        t.arc([cx+S*0.02, cy-S*0.18, cx+S*0.42, cy+S*0.18], 270, 630, fill=acc, width=3)
    elif name == "lamp":
        t.arc([cx-S*0.2, cy-S*0.34, cx+S*0.2, cy+S*0.06], 180, 360, fill=acc, width=3)
        t.line([cx-S*0.12, cy+S*0.06, cx-S*0.12, cy+S*0.2], fill=acc2, width=2)
        t.line([cx+S*0.12, cy+S*0.06, cx+S*0.12, cy+S*0.2], fill=acc2, width=2)
        t.line([cx-S*0.16, cy+S*0.24, cx+S*0.16, cy+S*0.24], fill=acc, width=3)
        for a in (-50, 0, 50):
            rad = math.radians(a-90)
            t.line([cx+math.cos(rad)*S*0.26, cy-S*0.14+math.sin(rad)*S*0.26, cx+math.cos(rad)*S*0.38, cy-S*0.14+math.sin(rad)*S*0.38], fill=acc2, width=2)
    else:
        t.ellipse([cx-S*0.3, cy-S*0.3, cx+S*0.3, cy+S*0.3], outline=acc, width=3)
    return t
