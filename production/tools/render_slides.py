#!/usr/bin/env python3
"""Render every slide at 3840x2160 from out/scenes.json.  (v2)

Archetypes:
  SECTION_TITLE  first scene of each section (big numeral + title)
  TITLE_CARD     programme title cards
  RECOGNITION    presidential recognition cards
  REFLECT        insight + question reflective cards
  TIMELINE       dated markers on a drawn line
  TABLE          comparative columns
  MAP            stylized route map (faint landmass, labelled nodes)
  RADIAL         central concept with radiating nodes
  QUADRANT       2x2 posture grid
  CUE_LIST       default: title + CUE items (term/gloss aware)
Each slide is a single full-frame visual (no collages).
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import design as D

ROOT = os.environ.get("TBUPROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out", "slides")
os.makedirs(OUT, exist_ok=True)

SECTION_TITLES = {
    "Opening": "OPENING CEREMONY",
    "1": "THEOLOGY IS MORE THAN RELIGIOUS OPINION",
    "2": "CHRISTIANITY DID NOT BEGIN WITH A COMPLETE BIBLE",
    "3": "THE TRINITY AND ITS HISTORICAL DEVELOPMENT",
    "4": "THE BIBLE WAS WRITTEN ACROSS DIFFERENT CULTURES AND LANGUAGES",
    "5": "THE EARLY CHURCH WAS MORE DIVERSE THAN MANY IMAGINE",
    "6": "WHY CHRISTIANS HAVE DIFFERENT BIBLICAL CANONS",
    "7": "THE HISTORICAL DEVELOPMENT OF CHRISTIAN DOCTRINE",
    "8": "BIBLICAL INTERPRETATION IS MORE COMPLEX THAN QUOTING VERSES",
    "9": "SALVATION HAS BEEN UNDERSTOOD IN DIFFERENT WAYS",
    "10": "THE RELATIONSHIP BETWEEN FAITH, REASON, AND SCIENCE",
    "11": "WOMEN, AFRICA, AND OVERLOOKED VOICES IN CHRISTIAN HISTORY",
    "12": "WHAT CHRISTIAN THEOLOGY ACTUALLY SAYS ABOUT THE END TIMES",
    "13": "COMMON THEOLOGICAL MISCONCEPTIONS",
    "14": "FINAL REFLECTIONS AND CLOSING",
}

GEO = {
    "Jerusalem": (35.2, 31.8), "Antioch": (36.2, 36.2), "Alexandria": (29.9, 31.2),
    "Rome": (12.5, 41.9), "Carthage": (10.3, 36.9), "Edessa": (38.8, 37.2),
    "Ephesus": (27.3, 37.9), "Constantinople": (28.9, 41.0), "Hippo": (7.8, 36.9),
    "Aksum": (38.7, 14.1), "Nubia": (33.7, 16.9), "Persia": (44.6, 33.1),
    "Gaul": (4.8, 45.8), "Armenia": (44.5, 40.2), "Georgia": (44.8, 42.3),
    "Ethiopia": (39.7, 9.1), "Egypt": (31.2, 26.8), "Syria": (38.0, 35.0),
    "Central Asia": (66.9, 39.6),
}
LAND = [
    [(-10, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 30), (43, 12), (50, 12),
     (50, 4), (-15, 4), (-17, 21)],
    [(-10, 36), (-9, 43), (-2, 48), (5, 52), (15, 54), (30, 52), (40, 48), (45, 42),
     (40, 36), (30, 36), (20, 36), (10, 38)],
    [(26, 36), (36, 37), (45, 40), (52, 36), (50, 28), (43, 28), (35, 28)],
]
MAP_SCENES = {"39", "40", "83", "84"}
TABLE_SCENES = {"47", "49"}


def proj(lon, lat):
    x = D.MARGIN + 200 + (lon + 18) / 72 * (D.CONTENT_W - 400)
    y = 620 + (54 - lat) / 50 * 1020
    return x, y


def header(d, slide_no):
    f = D.font("heading", 500, 30)
    d.text((D.MARGIN, 232), "WHAT YOU MAY NOT KNOW ABOUT CHRISTIAN THEOLOGY",
           font=f, fill=(150, 138, 108))
    f2 = D.font("heading", 600, 30)
    t = f"SLIDE {slide_no:03d}"
    d.text((D.W - D.MARGIN - D.text_w(d, t, f2), 232), t, font=f2, fill=(150, 138, 108))


def title_block(d, title, y=400, size=80):
    f = D.font("display", 700, size)
    lines = D.wrap(d, title.upper(), f, D.CONTENT_W)[:2]
    for ln in lines:
        d.text((D.MARGIN, y), ln, font=f, fill=D.IVORY)
        y += int(size * 1.28)
    D.rule(d, D.MARGIN, D.MARGIN + 400, y + 6, D.GOLD, 5)
    return y + 60


def split(it):
    for sep in (" — ", " - "):
        if sep in it:
            a, b = it.split(sep, 1)
            return a.strip(), b.strip()
    return it.strip(), None


def cue_items(d, items, y, big=False):
    ft = D.font("heading", 600, 60 if big else 50)
    fg = D.font("body", 300, 46 if big else 40)
    for it in [i for i in items if i.strip()][:6]:
        term, gloss = split(it)
        d.polygon([(D.MARGIN + 18, y + 26), (D.MARGIN + 34, y + 10),
                   (D.MARGIN + 50, y + 26), (D.MARGIN + 34, y + 42)], fill=D.GOLD)
        d.text((D.MARGIN + 70, y), term, font=ft, fill=D.IVORY)
        y += (74 if big else 62)
        if gloss:
            for ln in D.wrap(d, gloss, fg, D.CONTENT_W - 90)[:2]:
                d.text((D.MARGIN + 70, y), ln, font=fg, fill=D.IVORY_DIM)
                y += (60 if big else 54)
            y += 30
        else:
            y += 34
    return y


def arch_section_title(d, sec):
    num = "00" if sec == "Opening" else ("14" if sec == "14" else sec)
    f = D.font("display", 700, 300)
    d.text((D.MARGIN, 760), num, font=f, fill=D.GOLD)
    nw = D.text_w(d, num, f)
    ft = D.font("display", 700, 96)
    y = 830
    for ln in D.wrap(d, SECTION_TITLES.get(sec, "").upper(), ft, D.CONTENT_W - nw - 260):
        d.text((D.MARGIN + nw + 160, y), ln, font=ft, fill=D.IVORY)
        y += 120
    D.rule(d, D.MARGIN + nw + 160, D.MARGIN + nw + 640, y + 20, D.GOLD, 5)


def arch_reflect(d, items):
    y = 700
    if items:
        fq = D.font("quote", 500, 76, italic=True)
        for ln in D.wrap(d, items[0], fq, D.CONTENT_W - 300):
            D.center(d, ln, fq, y, D.GOLD)
            y += 108
        y += 50
        D.rule(d, D.W / 2 - 200, D.W / 2 + 200, y, D.GOLD, 3)
        y += 80
    for extra in items[1:]:
        fb = D.font("body", 400, 52)
        for ln in D.wrap(d, extra, fb, D.CONTENT_W - 500):
            D.center(d, ln, fb, y, D.IVORY)
            y += 76
        y += 30


def arch_timeline(d, title, items):
    y = title_block(d, title, 400, 76)
    y0 = 1240
    D.rule(d, D.MARGIN + 100, D.W - D.MARGIN - 100, y0, D.GOLD, 5)
    n = len(items)
    for i, it in enumerate(items):
        x = D.MARGIN + 100 + (i + 0.5) * (D.CONTENT_W - 200) / n
        d.ellipse([x - 15, y0 - 15, x + 15, y0 + 15], fill=D.GOLD)
        term, gloss = split(it)
        above = (i % 2 == 0)
        ft = D.font("heading", 600, 46)
        fg = D.font("body", 300, 36)
        tw = D.text_w(d, term, ft)
        d.text((x - tw / 2, y0 - 140 if above else y0 + 90), term, font=ft, fill=D.IVORY)
        if gloss:
            for j, ln in enumerate(D.wrap(d, gloss, fg, 640)[:2]):
                gw = D.text_w(d, ln, fg)
                d.text((x - gw / 2, (y0 - 88 + j * 48) if above else (y0 + 152 + j * 48)),
                       ln, font=fg, fill=D.IVORY_DIM)


def arch_table(d, title, items):
    title_block(d, title, 400, 76)
    cols = [i for i in items if split(i)[1]][:3]
    extra = [i for i in items if i not in cols]
    cw = (D.CONTENT_W - 120) / 3
    y = 800
    for i, c in enumerate(cols):
        term, gloss = split(c)
        x = D.MARGIN + 60 + i * cw
        d.rectangle([x, y, x + cw - 60, y + 520], outline=D.GOLD, width=3)
        ft = D.font("display", 700, 58)
        yy = y + 60
        for ln in D.wrap(d, term.upper(), ft, cw - 140):
            d.text((x + 50, yy), ln, font=ft, fill=D.GOLD)
            yy += 76
        fg = D.font("body", 400, 44)
        yy = y + 250
        for ln in D.wrap(d, gloss, fg, cw - 140):
            d.text((x + 50, yy), ln, font=fg, fill=D.IVORY)
            yy += 62
    if extra:
        D.center(d, extra[0], D.font("body", 300, 40), y + 600, D.IVORY_DIM)


def arch_radial(d, title, items):
    import math
    title_block(d, title, 380, 72)
    cx, cy = D.W / 2, 1240
    fr = D.font("display", 700, 64)
    d.ellipse([cx - 260, cy - 110, cx + 260, cy + 110], outline=D.GOLD, width=4)
    D.center(d, items[0].split(" — ")[0].upper() if " — " in items[0] else "THEOLOGY",
             fr, cy - 40, D.GOLD)
    nodes = items[1:] if " — " in items[0] else items
    n = len(nodes)
    for i, it in enumerate(nodes[:6]):
        ang = -math.pi / 2 + i * 2 * math.pi / min(n, 6)
        nx, ny = cx + 1250 * math.cos(ang), cy + 560 * math.sin(ang)
        d.line([cx + 260 * math.cos(ang), cy + 110 * math.sin(ang), nx, ny],
               fill=(120, 100, 60), width=3)
        term, gloss = split(it)
        ft = D.font("heading", 600, 52)
        fg = D.font("body", 300, 36)
        tw = D.text_w(d, term, ft)
        bx = nx - tw / 2
        d.ellipse([nx - 12, ny - 12, nx + 12, ny + 12], fill=D.GOLD)
        d.text((bx, ny - 96), term, font=ft, fill=D.IVORY)
        if gloss:
            for j, ln in enumerate(D.wrap(d, gloss, fg, 620)[:2]):
                gw = D.text_w(d, ln, fg)
                d.text((nx - gw / 2, ny + 34 + j * 46), ln, font=fg, fill=D.IVORY_DIM)


def arch_quadrant(d, title, items):
    title_block(d, title, 380, 72)
    x0, y0 = D.MARGIN + 60, 780
    cw, ch = (D.CONTENT_W - 180) / 2, 520
    for i, it in enumerate(items[:4]):
        term, gloss = split(it)
        x = x0 + (i % 2) * (cw + 60)
        y = y0 + (i // 2) * (ch + 60)
        d.rectangle([x, y, x + cw, y + ch], outline=(90, 80, 60), width=3)
        ft = D.font("display", 700, 62)
        d.text((x + 60, y + 60), term.upper(), font=ft, fill=D.GOLD)
        fg = D.font("body", 400, 44)
        yy = y + 190
        for ln in D.wrap(d, gloss or "", fg, cw - 140)[:4]:
            d.text((x + 60, yy), ln, font=fg, fill=D.IVORY)
            yy += 62


def arch_map(d, title, items):
    title_block(d, title, 380, 72)
    for poly in LAND:
        d.polygon([proj(lo, la) for lo, la in poly], fill=(17, 31, 52))
    fl = D.font("body", 300, 30)
    d.text((D.W - D.MARGIN - 620, 1690), "stylized route map — not to scale",
           font=fl, fill=(110, 105, 95))
    pts = {}
    for it in items:
        names = [p.strip() for p in re.split(r"[—-]\s*|,\s*", it)]
        for name in names:
            for key in GEO:
                if key.lower() == name.lower() or key.lower() in name.lower():
                    if key not in pts:
                        pts[key] = ""
                    break
    order = list(pts)
    for a, b in zip(order, order[1:]):
        x1, y1 = proj(*GEO[a])
        x2, y2 = proj(*GEO[b])
        for t in range(24):
            tt = t / 24
            d.ellipse([x1 + (x2 - x1) * tt - 2, y1 + (y2 - y1) * tt - 2,
                       x1 + (x2 - x1) * tt + 2, y1 + (y2 - y1) * tt + 2], fill=(120, 100, 60))
    fn = D.font("heading", 600, 44)
    for name in order:
        x, y = proj(*GEO[name])
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=D.GOLD)
        d.ellipse([x - 24, y - 24, x + 24, y + 24], outline=(200, 162, 74, 110), width=2)
        d.text((x + 34, y - 24), name, font=fn, fill=D.IVORY)


def arch_title_card(d, items):
    y = 700
    D.center(d, "TRIUNE  BIBLICAL  UNIVERSITY  GLOBAL  EXTENSION  USA",
             D.font("heading", 500, 54), y, D.GOLD, 14)
    y += 150
    ft = D.font("display", 700, 128)
    for ln in ["WHAT YOU MAY NOT KNOW", "ABOUT CHRISTIAN THEOLOGY"]:
        D.center(d, ln, ft, y, D.IVORY)
        y += 170
    D.rule(d, D.W / 2 - 420, D.W / 2 + 420, y, D.GOLD, 5)
    y += 80
    D.center(d, "A 60-Minute Cinematic Educational Video Podcast",
             D.font("title_alt", 500, 72), y, D.IVORY)
    for extra in items[1:]:
        y += 120
        D.center(d, extra, D.font("body", 400, 48), y, D.GOLD_SOFT)


def arch_recognition(d, items):
    y = 640
    D.center(d, "SPECIAL  RECOGNITION", D.font("heading", 500, 48), y, D.GOLD, 12)
    y += 120
    D.rule(d, D.W / 2 - 300, D.W / 2 + 300, y, D.GOLD, 3)
    y += 90
    D.center(d, "Prof. Adeleke Daniel Durojaiye (PhD)", D.font("display", 700, 116), y, D.IVORY)
    y += 170
    D.center(d, "PRESIDENT  AND  CHANCELLOR", D.font("heading", 500, 56), y, D.GOLD_SOFT, 8)
    y += 110
    D.center(d, "TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA",
             D.font("body", 400, 46), y, D.IVORY_DIM)
    for extra in items[3:]:
        y += 100
        D.center(d, extra, D.font("quote", 500, 52, italic=True), y, D.GOLD)


BESPOKE = {"3": arch_title_card, "4": arch_recognition, "6": arch_recognition}
DATE_RE = re.compile(r"(CE\b|BCE\b|c\.\s*\d|\d{3,4}s\b)")


def main():
    meta = json.load(open(os.path.join(ROOT, "out", "scenes.json"), encoding="utf-8"))
    scenes = meta["scenes"]
    seen = set()
    first_of_section = set()
    for s in scenes:
        if s["section"] not in seen:
            seen.add(s["section"])
            first_of_section.add(s["id"])
    for s in scenes:
        sid, sec = s["id"], s["section"]
        items = [i.strip() for i in s["cue"].split("|")] if s["cue"] else []
        glossed = [i for i in items if split(i)[1]]
        img = D.new_canvas()
        D.frame(img)
        d = ImageDraw.Draw(img)
        header(d, s["slide"])
        if sid in BESPOKE:
            BESPOKE[sid](d, items)
        elif s["title"].upper().startswith("MAP — "):
            arch_map(d, s["title"][6:], items)
        elif s["title"].upper().startswith("TABLE — "):
            arch_table(d, s["title"][8:], items)
        elif s["title"].upper().startswith("TIMELINE — "):
            arch_timeline(d, s["title"][11:], items)
        elif sid in first_of_section and sec != "Opening":
            arch_section_title(d, sec)
        elif sec == "Opening":
            arch_reflect(d, ([s["title"]] + items) if items else [s["title"]])
        elif sid in TABLE_SCENES:
            arch_table(d, s["title"], items)
        elif sid in MAP_SCENES:
            arch_map(d, s["title"], items)
        elif len(items) >= 3 and all(DATE_RE.search(i) for i in items[:4]):
            arch_timeline(d, s["title"], items)
        elif len(items) == 4 and len(glossed) == 4:
            arch_quadrant(d, s["title"], items)
        elif len(items) >= 6 and len(glossed) >= 5:
            arch_radial(d, s["title"], items)
        elif len(items) == 2 and len(items[0]) > 60:
            arch_reflect(d, items)
        elif items:
            n = len(items)
            y = title_block(d, s["title"], 400, 80 if n > 4 else 88)
            cue_items(d, items, max(y + 60, 760 if n <= 4 else y + 60), big=(n <= 4))
        else:
            arch_reflect(d, [s["title"]])
        if s["cite"] and s["cite"] != "(none)":
            D.footnote(d, s["cite"])
        D.save(img, os.path.join(OUT, f"slide_{s['slide']:03d}.png"))
    print(f"rendered {len(scenes)} slides -> {OUT}")


if __name__ == "__main__":
    main()
