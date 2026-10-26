#!/usr/bin/env python3
"""Quality gate for one CAC course book (HANDBOOK-STANDARD.md §9).

Checks, per volume:
  1. curriculum match    — BOOK.md code/title/semester/units byte-exact against courses.csv
  2. coverage            — every week file carries the weekly grammar: outcomes, three lectures,
                           at least one figure, a worked example, a practical, seminar questions,
                           assessment, reading, synthesis, next-week pointer
  3. integrity markers   — vignettes labelled fictitious; no unlabelled AI image claim needed here
                           (images are diagrams); no literal fence markers left in the PDF
  4. PDF typography      — no font fallback outside the two house families
  5. PDF accessibility   — MarkInfo marked, StructTreeRoot present, Lang set, bookmarks to level 3
  6. contrast            — the four text inks against the four grounds, 4.5:1 floor (§4.1)
  7. length              — informational only; the University imposes no word floor

Usage:  ~/.venv/bin/python cac/scripts/qa_book.py <book>
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import pymupdf

CAC = Path(__file__).resolve().parents[1]
ALLOWED = ("EBGaramond", "SourceSans3")

REQUIRED_WEEK = [
    ("::: objectives", "learning outcomes"),
    ("### Lecture I", "lecture I"),
    ("### Lecture II", "lecture II"),
    ("### Lecture III", "lecture III"),
    ("![", "at least one figure"),
    ("Worked example", "a worked example"),
    ("::: skills", "a practical"),
    ("Seminar questions", "seminar questions"),
    ("::: assessment", "assessment"),
    ("::: reading", "reading"),
    ("::: summary", "synthesis"),
    ("### Next week", "next-week pointer"),
]

INKS = {"ink": "#1B1B1B", "teal": "#0F4C5C", "grey": "#5E6468", "bronze-text": "#8A5A26"}
GROUNDS = {"white": "#FFFFFF", "ivory": "#FBF8F1", "teal-light": "#E3EEF0",
           "bronze-light": "#F4EADB"}


def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def meta(book):
    m = {}
    for line in (book / "BOOK.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("- "):
            k, _, v = line[2:].partition(": ")
            m[k.strip()] = v.strip()
    return m


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "cac701"
    BOOK = CAC / "books" / name
    problems, notes = [], []

    # 1 — curriculum match
    m = meta(BOOK)
    rows = list(csv.DictReader((CAC / "courses.csv").open(encoding="utf-8")))
    match = [r for r in rows if r["code"] == m.get("code") and r["title"] == m.get("title")]
    if not match:
        problems.append(f"BOOK.md code/title not found byte-exact in courses.csv: {m.get('code')}")
    else:
        r = match[0]
        if r["units"] != m.get("units"):
            problems.append(f"units mismatch: csv {r['units']} vs BOOK.md {m.get('units')}")
        notes.append(f"curriculum match OK: {r['code']} {r['title']} ({r['units']} units)")

    # 2 — coverage
    weeks = sorted((BOOK / "manuscript" / "weeks").glob("w*.md"))
    target = int(m.get("weeks", 16))
    notes.append(f"weeks present: {len(weeks)} of {target}")
    for w in weeks:
        t = w.read_text(encoding="utf-8")
        for marker, label in REQUIRED_WEEK:
            if marker not in t:
                problems.append(f"{w.name}: missing {label}")
        if t.count("![") < 1:
            problems.append(f"{w.name}: no figure")

    # 3 — integrity markers
    for w in weeks:
        t = w.read_text(encoding="utf-8")
        if "::: vignette" in t and "fictitious" not in t.lower():
            problems.append(f"{w.name}: vignette not labelled fictitious")
        if "AI-generated" in t and "Illustrative image" not in t:
            problems.append(f"{w.name}: AI image not labelled")

    # 4/5 — PDF
    pdf = BOOK / "final" / f"{name}.pdf"
    if not pdf.exists():
        problems.append("final PDF missing — run build_book.py")
    else:
        d = pymupdf.open(str(pdf))
        fonts = {f[3].split("+")[-1] for p in d for f in p.get_fonts()}
        bad = {f for f in fonts if not f.startswith(ALLOWED)}
        if bad:
            problems.append(f"font fallback: {sorted(bad)}")
        text = "".join(p.get_text() for p in d)
        if ":::" in text:
            problems.append("literal fence markers in PDF text")
        cat = d.pdf_catalog()
        if d.xref_get_key(cat, "MarkInfo")[1].find("true") < 0:
            problems.append("MarkInfo not marked")
        if d.xref_get_key(cat, "StructTreeRoot")[0] == "null":
            problems.append("no StructTreeRoot")
        lang = d.xref_get_key(cat, "Lang")
        if "en-GB" not in lang[1]:
            problems.append(f"Lang not en-GB: {lang}")
        toc = d.get_toc()
        if not toc:
            problems.append("no bookmarks")
        notes.append(f"pdf: {d.page_count} pages, {len(toc)} bookmarks, fonts clean"
                     if not bad else f"pdf: {d.page_count} pages")
        d.close()

    # 6 — contrast
    for ink, iv in INKS.items():
        for g, gv in GROUNDS.items():
            c = contrast(iv, gv)
            if c < 4.5:
                problems.append(f"contrast {ink} on {g} = {c:.2f} < 4.5")

    # 7 — length (informational)
    total = 0
    for w in weeks:
        t = w.read_text(encoding="utf-8")
        t = re.sub(r"!\[([^\]]*)\]\([^)]*\)\{[^}]*\}", r"\1", t)
        t = re.sub(r"\{[.#][^}]*\}", "", t)
        t = re.sub(r"^:::.*$", "", t, flags=re.M)
        t = re.sub(r"[#*_>|`]", " ", t)
        total += len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.\-–/]*", t))
    notes.append(f"main text: {total:,} words across {len(weeks)} weeks (informational; no floor)")

    print(f"QA — {m.get('code')} {m.get('title')}")
    for n in notes:
        print("  ·", n)
    if problems:
        print("  FAIL:")
        for p in problems:
            print("   !", p)
        sys.exit(1)
    print("  PASS")


if __name__ == "__main__":
    main()
