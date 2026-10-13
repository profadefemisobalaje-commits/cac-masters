"""CAC Lecture Studio - slide layouts. Every slide renders at 1920x1080 and
downscales to 1280x720 for crisp 720p delivery."""
import os, math
from PIL import Image, ImageDraw, ImageFilter
from . import render_core as rc

UNI = "TRIUNE BIBLICAL UNIVERSITY  ·  GLOBAL EXTENSION USA"
PROG = "MASTER IN CHILDREN AND ADOLESCENT COUNSELING"

def _spaced(d, xy, text, fnt, fill, gap=6, anchor="la"):
    x, y = xy
    widths = [d.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + gap*(len(text)-1)
    if anchor == "ma": x -= total/2
    elif anchor == "ra": x -= total
    for ch, wch in zip(text, widths):
        d.text((x, y), ch, font=fnt, fill=fill)
        x += wch + gap

def canvas(st):
    img = rc.vgrad(rc.W, rc.H, st["bg0"], st["bg1"], "#05070C")
    img = rc.vignette(img, 0.42)
    return img, ImageDraw.Draw(img)

def finalize(img, st, page=None, total=None):
    d = ImageDraw.Draw(img)
    acc = st["acc"]
    d.line([96, rc.H-84, rc.W-96, rc.H-84], fill=rc.mix(st["acc"], st["bg1"], 0.55), width=2)
    _spaced(d, (96, rc.H-64), UNI, rc.F_CAPS(17), rc.mix(acc, st["ink"], 0.25), gap=3)
    _spaced(d, (rc.W-96, rc.H-64), st.get("code", PROG), rc.F_CAPS(17), rc.mix(acc, st["bg1"], 0.15), gap=3, anchor="ra")
    if page:
        d.text((rc.W-96, rc.H-110), f"{page:02d}", font=rc.F_SERIF(26, 700), fill=acc, anchor="ra")
    img = rc.noise(img, 6)
    out = img.resize((rc.OUT_W, rc.OUT_H), Image.LANCZOS)
    return out

def badge_hours(d, x, y, hours, acc, ink):
    d.rounded_rectangle([x, y, x+292, y+92], radius=10, outline=acc, width=2)
    d.text((x+146, y+30), str(hours), font=rc.F_SERIF(44, 700), fill=ink, anchor="mm")
    _spaced(d, (x+146, y+68), "VIDEO HOURS", rc.F_CAPS(13), acc, gap=3, anchor="ma")

# --------------------------------------------------------------- slides
def slide_opener(st):
    img, d = canvas(st)
    cy = rc.H//2
    d.ellipse([rc.W//2-170, cy-170, rc.W//2+170, cy+170], outline=st["acc"], width=3)
    d.ellipse([rc.W//2-150, cy-150, rc.W//2+150, cy+150], outline=rc.mix(st["acc"], st["ink"], 0.5), width=1)
    rc.motif(d, st["motif"], rc.W//2, cy, 210, st["acc"], st["acc2"])
    _spaced(d, (rc.W//2, cy+240), UNI, rc.F_CAPS(22), st["acc"], gap=4, anchor="ma")
    _spaced(d, (rc.W//2, cy+292), PROG, rc.F_CAPS(30), st["ink"], gap=7, anchor="ma")
    return finalize(img, st)

def slide_title(st, c, variant=None):
    img, d = canvas(st)
    v = variant or st["layout"]
    acc, ink = st["acc"], st["ink"]
    if v == "band":
        d.rectangle([0, 0, 460, rc.H], fill=rc.mix(st["bg0"], "#000000", 0.35))
        d.line([460, 0, 460, rc.H], fill=acc, width=3)
        rc.motif(d, st["motif"], 230, 430, 300, acc, st["acc2"])
        badge_hours(d, 84, 800, st["hours"], acc, ink)
        tx = 560
        _spaced(d, (tx, 208), st["code"] + "   ·   " + st["sem"].upper(), rc.F_CAPS(26), acc, gap=5)
        lines = _title_lines(d, st["title"], rc.F_SERIF(104, 700), rc.W - tx - 130)
        y = 300
        for ln in lines:
            d.text((tx, y), ln, font=rc.F_SERIF(104, 700), fill=ink); y += 122
        rc.rule(d, tx, y+14, tx+380, acc, 3)
        d.text((tx, y+52), st["tagline"], font=rc.F_SERIF_IT(40, 500), fill=rc.mix(st["acc2"], ink, 0.55))
        _spaced(d, (tx, rc.H-220), "AN INTRODUCTION TO THE COURSE", rc.F_CAPS(24), rc.mix(acc, ink, 0.3), gap=6)
    elif v == "split":
        d.polygon([(rc.W-760, 0), (rc.W, 0), (rc.W, rc.H), (rc.W-980, rc.H)], fill=rc.mix(st["bg1"], acc, 0.14))
        d.line([(rc.W-760, 0), (rc.W-980, rc.H)], fill=acc, width=3)
        rc.motif(d, st["motif"], rc.W-380, 400, 330, acc, st["acc2"])
        badge_hours(d, rc.W-540, 780, st["hours"], acc, ink)
        _spaced(d, (110, 190), st["code"] + "  ·  " + st["sem"].upper(), rc.F_CAPS(26), acc, gap=5)
        lines = _title_lines(d, st["title"], rc.F_SERIF(100, 700), 1050)
        y = 286
        for ln in lines:
            d.text((110, y), ln, font=rc.F_SERIF(100, 700), fill=ink); y += 118
        rc.rule(d, 110, y+10, 470, acc, 3)
        d.text((110, y+48), st["tagline"], font=rc.F_SERIF_IT(38, 500), fill=rc.mix(st["acc2"], ink, 0.55))
    elif v == "card":
        d.rounded_rectangle([140, 130, rc.W-140, rc.H-150], radius=6, outline=acc, width=2)
        d.rounded_rectangle([158, 148, rc.W-158, rc.H-168], radius=4, outline=rc.mix(acc, st["bg1"], 0.5), width=1)
        for cx_, cy_ in ((140,130),(rc.W-140,130),(140,rc.H-150),(rc.W-140,rc.H-150)):
            rc.diamond(d, cx_, cy_, 10, acc)
        rc.motif(d, st["motif"], rc.W//2, 320, 240, acc, st["acc2"])
        _spaced(d, (rc.W//2, 480), st["code"] + "  ·  " + st["sem"].upper(), rc.F_CAPS(26), acc, gap=6, anchor="ma")
        lines = _title_lines(d, st["title"], rc.F_SERIF(92, 700), rc.W-480)
        y = 540
        for ln in lines:
            d.text((rc.W//2, y), ln, font=rc.F_SERIF(92, 700), fill=ink, anchor="ma"); y += 108
        d.text((rc.W//2, y+18), st["tagline"], font=rc.F_SERIF_IT(36, 500), fill=rc.mix(st["acc2"], ink, 0.55), anchor="mm")
        badge_hours(d, rc.W//2-146, rc.H-330, st["hours"], acc, ink)
    else:  # hero / archive
        d.ellipse([rc.W//2-430, 60, rc.W//2+430, 920], outline=rc.mix(acc, st["bg1"], 0.45), width=2)
        rc.motif(d, st["motif"], rc.W//2, 300, 230, acc, st["acc2"])
        _spaced(d, (rc.W//2, 470), st["code"], rc.F_CAPS(30), acc, gap=8, anchor="ma")
        lines = _title_lines(d, st["title"], rc.F_SERIF(96, 700), rc.W-420)
        y = 540
        for ln in lines:
            d.text((rc.W//2, y), ln, font=rc.F_SERIF(96, 700), fill=ink, anchor="ma"); y += 112
        rc.rule(d, rc.W//2-200, y+16, rc.W//2+200, acc, 3)
        d.text((rc.W//2, y+56), st["tagline"], font=rc.F_SERIF_IT(38, 500), fill=rc.mix(st["acc2"], ink, 0.55), anchor="mm")
        badge_hours(d, 150, 150, st["hours"], acc, ink)
        _spaced(d, (rc.W-150, 176), st["sem"].upper(), rc.F_CAPS(22), rc.mix(acc, ink, 0.3), gap=4, anchor="ra")
    return finalize(img, st)

def _title_lines(d, text, fnt, max_w):
    return rc.wrap(text, fnt, max_w)[:3]

def slide_agenda(st, items, kicker="IN THIS SESSION"):
    img, d = canvas(st)
    acc, ink = st["acc"], st["ink"]
    _spaced(d, (140, 120), kicker, rc.F_CAPS(26), acc, gap=6)
    rc.rule(d, 140, 172, 560, acc, 2)
    y = 240
    for i, it in enumerate(items, 1):
        d.text((150, y), f"{i:02d}", font=rc.F_SERIF(52, 700), fill=acc)
        d.text((260, y+12), it, font=rc.F_SANS(40, 500), fill=ink)
        y += 92
    rc.motif(d, st["motif"], rc.W-330, rc.H//2+40, 300, rc.mix(acc, st["bg1"], 0.15), rc.mix(st["acc2"], st["bg1"], 0.2))
    return finalize(img, st, page=2)

def slide_stats(st, stats):
    img, d = canvas(st)
    acc, ink = st["acc"], st["ink"]
    _spaced(d, (rc.W//2, 130), "THE COURSE AT A GLANCE", rc.F_CAPS(28), acc, gap=7, anchor="ma")
    rc.rule(d, rc.W//2-180, 184, rc.W//2+180, acc, 2)
    n = len(stats); cw = (rc.W-360)//n
    for i, (big, lab) in enumerate(stats):
        cx = 180 + cw*i + cw//2
        d.text((cx, 400), str(big), font=rc.F_SERIF(150, 700), fill=ink, anchor="mm")
        _spaced(d, (cx, 520), lab.upper(), rc.F_CAPS(20), acc, gap=4, anchor="ma")
        if i < n-1: d.line([180+cw*(i+1), 330, 180+cw*(i+1), 540], fill=rc.mix(acc, st["bg1"], 0.5), width=2)
    return finalize(img, st, page=3)

def slide_vignette(st, text, attrib):
    img, d = canvas(st)
    acc, ink = st["acc"], st["ink"]
    d.rectangle([0, 0, 24, rc.H], fill=acc)
    d.text((170, 170), "\u201C", font=rc.F_SERIF(240, 700), fill=rc.mix(acc, st["bg1"], 0.15))
    lines = rc.wrap(text, rc.F_SERIF_IT(52, 500), rc.W-460)
    y = 330
    for ln in lines:
        d.text((240, y), ln, font=rc.F_SERIF_IT(52, 500), fill=ink); y += 74
    rc.rule(d, 240, y+36, 540, acc, 2)
    _spaced(d, (240, y+66), attrib.upper(), rc.F_CAPS(22), acc, gap=4)
    return finalize(img, st, page=4)

def slide_heading(st, kicker, title, page=None):
    img, d = canvas(st)
    acc, ink = st["acc"], st["ink"]
    d.rectangle([0, rc.H//2-190, rc.W, rc.H//2+190], fill=rc.mix(st["bg1"], acc, 0.10))
    d.line([0, rc.H//2-190, rc.W, rc.H//2-190], fill=acc, width=2)
    d.line([0, rc.H//2+190, rc.W, rc.H//2+190], fill=acc, width=2)
    _spaced(d, (rc.W//2, rc.H//2-110), kicker, rc.F_CAPS(26), acc, gap=7, anchor="ma")
    lines = rc.wrap(title, rc.F_SERIF(86, 700), rc.W-360)[:2]
    y = rc.H//2-30
    for ln in lines:
        d.text((rc.W//2, y), ln, font=rc.F_SERIF(86, 700), fill=ink, anchor="ma"); y += 100
    rc.diamond(d, 140, rc.H//2, 8, acc)
    rc.diamond(d, rc.W-140, rc.H//2, 8, acc)
    return finalize(img, st, page=page)

def slide_bullets(st, kicker, title, items, page=None, lead=None):
    img, d = canvas(st)
    acc, ink = st["acc"], st["ink"]
    _spaced(d, (140, 108), kicker, rc.F_CAPS(24), acc, gap=6)
    d.text((140, 156), title, font=rc.F_SERIF(64, 700), fill=ink)
    rc.rule(d, 140, 250, 620, acc, 3)
    y = 320
    if lead:
        for ln in rc.wrap(lead, rc.F_SERIF_IT(34, 500), rc.W-360):
            d.text((150, y), ln, font=rc.F_SERIF_IT(34, 500), fill=rc.mix(st["acc2"], ink, 0.6)); y += 48
        y += 18
    step = min(96, max(64, (rc.H-170-y)//max(len(items),1)))
    fnt = rc.F_SANS(36 if len(items) <= 6 else 32, 500)
    for it in items:
        rc.diamond(d, 162, y+20, 9, acc)
        for j, ln in enumerate(rc.wrap(it, fnt, rc.W-440)[:2]):
            d.text((206, y + j*44), ln, font=fnt, fill=ink)
        y += step
    rc.motif(d, st["motif"], rc.W-260, 210, 170, rc.mix(acc, st["bg1"], 0.2), rc.mix(st["acc2"], st["bg1"], 0.25))
    return finalize(img, st, page=page)

def slide_outcome(st, idx, total, title, body, page=None):
    img, d = canvas(st)
    acc, ink = st["acc"], st["ink"]
    d.text((150, 130), f"{idx:02d}", font=rc.F_SERIF(190, 700), fill=rc.mix(acc, st["bg1"], 0.12))
    d.text((150, 150), f"{idx:02d}", font=rc.F_SERIF(190, 700), fill=None, stroke=acc, stroke_width=2)
    _spaced(d, (420, 160), f"LEARNING OUTCOME {idx} OF {total}", rc.F_CAPS(24), acc, gap=5)
    d.text((420, 216), title, font=rc.F_SERIF(58, 700), fill=ink)
    rc.rule(d, 420, 310, 800, acc, 3)
    y = 380
    for ln in rc.wrap(body, rc.F_SANS(38, 400), rc.W-600):
        d.text((420, y), ln, font=rc.F_SANS(38, 400), fill=rc.mix(ink, st["bg1"], 0.12)); y += 56
    rc.motif(d, st["motif"], 230, 660, 220, rc.mix(acc, st["bg1"], 0.25), rc.mix(st["acc2"], st["bg1"], 0.3))
    return finalize(img, st, page=page)

def slide_module(st, idx, total, name, hours, points, why, page=None):
    img, d = canvas(st)
    acc, ink = st["acc"], st["ink"]
    d.rounded_rectangle([120, 96, 560, 236], radius=8, outline=acc, width=2)
    _spaced(d, (340, 132), f"MODULE {idx} OF {total}", rc.F_CAPS(22), acc, gap=5, anchor="ma")
    d.text((340, 178), f"{hours} video hours", font=rc.F_SERIF_IT(30, 500), fill=rc.mix(st["acc2"], ink, 0.6), anchor="mm")
    d.text((610, 118), name, font=rc.F_SERIF(58, 700), fill=ink)
    rc.rule(d, 140, 286, rc.W-140, acc, 2, cap=False)
    y = 350
    for it in points:
        rc.diamond(d, 170, y+20, 8, acc)
        for j, ln in enumerate(rc.wrap(it, rc.F_SANS(34, 500), rc.W-560)[:2]):
            d.text((212, y+j*44), ln, font=rc.F_SANS(34, 500), fill=ink)
        y += 88
    y += 12
    d.rounded_rectangle([140, y-10, rc.W-140, y+150], radius=8, fill=rc.mix(st["bg1"], acc, 0.10), outline=rc.mix(acc, st["bg1"], 0.4), width=1)
    wy = y+18
    for ln in rc.wrap(why, rc.F_SERIF_IT(32, 500), rc.W-380)[:3]:
        d.text((190, wy), ln, font=rc.F_SERIF_IT(32, 500), fill=rc.mix(st["acc2"], ink, 0.65)); wy += 44
    return finalize(img, st, page=page)

def slide_roadmap(st, modules, page=None):
    img, d = canvas(st)
    acc, ink = st["acc"], st["ink"]
    _spaced(d, (140, 96), "THE LEARNING JOURNEY", rc.F_CAPS(26), acc, gap=6)
    d.text((140, 142), "Module Map and Video Hour Allocation", font=rc.F_SERIF(52, 700), fill=ink)
    rc.rule(d, 140, 230, 700, acc, 3)
    max_h = max(m[1] for m in modules)
    avail = rc.W - 1120 - 260
    y = 296
    step = min(96, (rc.H-170-y)//max(len(modules),1))
    for i, (name, h) in enumerate(modules):
        d.text((140, y-6), f"{i+1:02d}", font=rc.F_SERIF(34, 700), fill=acc)
        lbl = name if d.textlength(name, font=rc.F_SANS(29, 600)) < 980 else rc.wrap(name, rc.F_SANS(29, 600), 980)[0] + "…"
        d.text((210, y-2), lbl, font=rc.F_SANS(29, 600), fill=ink)
        bw = max(46, int(avail * h / max_h))
        d.rounded_rectangle([1120, y-4, 1120+bw, y+30], radius=8,
                            fill=rc.mix(acc, st["bg1"], 0.30 + 0.45*((i % 3)/2)), outline=acc, width=1)
        d.text((1130+bw, y-4), f" {h}h", font=rc.F_SANS(27, 600), fill=rc.mix(acc, ink, 0.4))
        y += step
    _spaced(d, (140, rc.H-128), f"TOTAL  ·  {sum(m[1] for m in modules)} VIDEO HOURS", rc.F_CAPS(22), acc, gap=5)
    return finalize(img, st, page=page)

def slide_closing(st, c, line, page=None):
    img, d = canvas(st)
    acc, ink = st["acc"], st["ink"]
    d.ellipse([rc.W//2-190, 150, rc.W//2+190, 530], outline=acc, width=3)
    d.ellipse([rc.W//2-168, 172, rc.W//2+168, 508], outline=rc.mix(acc, ink, 0.4), width=1)
    rc.motif(d, st["motif"], rc.W//2, 340, 230, acc, st["acc2"])
    y = 610
    for ln in rc.wrap(line, rc.F_SERIF_IT(44, 500), rc.W-560):
        d.text((rc.W//2, y), ln, font=rc.F_SERIF_IT(44, 500), fill=ink, anchor="ma"); y += 60
    _spaced(d, (rc.W//2, y+40), "TRIUNE BIBLICAL UNIVERSITY · GLOBAL EXTENSION USA", rc.F_CAPS(24), acc, gap=5, anchor="ma")
    return finalize(img, st, page=page)

def slide_credits(st, c):
    img, d = canvas(st)
    acc, ink = st["acc"], st["ink"]
    rows = [
        ("PROGRAMME", "Master in Children and Adolescent Counseling"),
        ("COURSE", f'{st["code"]} — {st["title"]}'),
        ("VIDEO LIBRARY", f'{st["hours"]} hours of recorded instruction  ·  1.6 course units'),
        ("DELIVERY", "100% Online  ·  Professional Video Lectures"),
        ("INSTITUTION", "Triune Biblical University Global Extension USA"),
    ]
    y = 220
    _spaced(d, (rc.W//2, 130), "COURSE CREDITS", rc.F_CAPS(28), acc, gap=8, anchor="ma")
    for lab, val in rows:
        _spaced(d, (rc.W//2, y), lab, rc.F_CAPS(20), acc, gap=5, anchor="ma")
        d.text((rc.W//2, y+40), val, font=rc.F_SANS(36, 500), fill=ink, anchor="ma")
        y += 128
    return finalize(img, st)

def blend(a, b, t):
    return Image.blend(a.convert("RGB"), b.convert("RGB"), t)
