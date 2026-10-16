"""Generate page-referenced tables (cases, treaties, legislation) and indexes.

The compiled PDF is read page by page; each curated entry in refdata.py carries
one or more search patterns.  Matches in the main text and appendices (arabic
pages) are collected and written as Typst for the next compile pass.
"""
import re
from pathlib import Path

import pymupdf

import refdata


def page_texts(pdf: Path):
    doc = pymupdf.open(str(pdf))
    pages = []
    for p in doc:
        label = re.sub(r"^ageLabel", "", p.get_label() or "")
        t = p.get_text("text")
        t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", t)   # undo hyphenation
        t = re.sub(r"\s+", " ", t)
        t = t.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
        pages.append((label, t))
    return pages


def collect(pages, entries, start, stop):
    out = []
    for entry in entries:
        display, pats = entry[0], entry[1]
        rx = [re.compile(p, re.I if (len(entry) > 2 and entry[2] == "i") else 0) for p in pats]
        hits = []
        for i in range(start, stop):
            label, text = pages[i]
            if any(r.search(text) for r in rx) and label.isdigit():
                n = int(label)
                if n not in hits:
                    hits.append(n)
        if hits:
            out.append((display, hits))
    return out


def compress(nums):
    nums = sorted(set(nums))
    parts, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        parts.append(str(nums[i]) if i == j else f"{nums[i]}–{nums[j]}")
        i = j + 1
    if len(parts) > 14:
        parts = parts[:14] + ["passim"]
    return ", ".join(parts)


def esc(s):
    for a, b in (("\\", "\\\\"), ("#", "\\#"), ("$", "\\$"), ("@", "\\@"), ("<", "\\<"),
                 (">", "\\>"), ("*", "\\*"), ("_", "\\_"), ("[", "\\["), ("]", "\\]"), ("`", "\\`")):
        s = s.replace(a, b)
    return s


def fmt(display):
    # *italic* segments in refdata are rendered with emph
    parts = display.split("*")
    return "".join(f"#emph[{esc(p)}]" if k % 2 else esc(p) for k, p in enumerate(parts))


def table_block(title, intro, groups, two_col=False):
    s = [f'#front-heading([{title}])\n']
    if intro:
        s.append(f"#par(first-line-indent: 0pt)[#text(size: 9pt, style: \"italic\")[{esc(intro)}]]\n#v(0.6em)\n")
    if two_col:
        s.append("#columns(2, gutter: 14pt)[\n")
    for gtitle, items in groups:
        if not items:
            continue
        if gtitle:
            s.append(f'#block(sticky: true, above: 1em, below: 0.5em, text(font: sans, size: 8.6pt, weight: "bold", fill: teal, tracking: 0.08em)[{esc(gtitle.upper())}])\n')
        for display, hits in items:
            s.append(
                f'#block(above: 0.32em, below: 0.32em, par(first-line-indent: 0pt, hanging-indent: 1.2em, justify: false)[#text(size: {"8.6" if two_col else "9"}pt)[{fmt(display)}#box(width: 1fr, repeat[ ])#h(0.4em){compress(hits)}]])\n')
    if two_col:
        s.append("]\n")
    return "".join(s)


def run(pdf: Path, build: Path):
    pages = page_texts(pdf)
    labels = [l for l, _ in pages]
    # main text starts at the first page labelled "1"
    start = next(i for i, l in enumerate(labels) if l == "1")
    # back matter starts at the Bibliography opening page
    stop = len(pages)
    for i in range(start, len(pages)):
        if pages[i][1].strip().startswith("Bibliography") or re.match(r"^\s*\d*\s*Bibliography\b", pages[i][1]):
            stop = i
            break

    def grouped(entries):
        groups = []
        for gtitle, items in entries:
            groups.append((gtitle, sorted(collect(pages, items, start, stop), key=lambda x: x[0].lower().lstrip("*"))))
        return groups

    tables = []
    tables.append(table_block("Table of Cases and Arbitral Awards",
        "Page references are to the main text and appendices. Case names are given in short form; full citations appear in the footnotes at the first substantive reference.",
        grouped(refdata.CASES)))
    tables.append(table_block("Table of Treaties and International Instruments", "",
        grouped(refdata.TREATIES)))
    tables.append(table_block("Table of Legislation and Regulations", "",
        grouped(refdata.LEGISLATION)))
    (build / "generated_tables.typ").write_text('#import "/templates/book.typ": *\n' + "\n".join(tables), encoding="utf-8")

    idx = []
    for title, data in (("Index of Legal Concepts", refdata.INDEX_CONCEPTS),
                        ("Index of Institutions and Organizations", refdata.INDEX_INSTITUTIONS),
                        ("Subject Index", refdata.INDEX_SUBJECT)):
        items = sorted(collect(pages, data, start, stop), key=lambda x: x[0].lower())
        groups = {}
        for d, h in items:
            k = d.lstrip("*")[0].upper()
            groups.setdefault(k, []).append((d, h))
        idx.append('#matter.update("back")\n' + table_block(title, "", sorted(groups.items()), two_col=True))
    (build / "generated_indexes.typ").write_text('#import "/templates/book.typ": *\n' + "\n".join(idx), encoding="utf-8")
    print(f"  indexed {stop - start} pages")
