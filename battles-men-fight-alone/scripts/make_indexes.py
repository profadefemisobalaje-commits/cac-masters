"""Build the Subject Index for Battles Men Fight Alone.

The compiled PDF is read page by page; every curated entry in indexdata.py
carries one or more regular-expression patterns.  Matches in the main text and
the appendices (arabic-numbered pages) are collected and written as Typst for
the next compile pass.
"""
import re
from pathlib import Path

import pymupdf

import indexdata


def page_texts(pdf: Path):
    doc = pymupdf.open(str(pdf))
    pages = []
    for p in doc:
        label = re.sub(r"^ageLabel", "", p.get_label() or "")
        t = p.get_text("text")
        t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", t)      # undo hyphenation
        t = re.sub(r"\s+", " ", t)
        t = t.replace("\u2019", "'").replace("\u2018", "'").replace("\u2013", "-").replace("\u2014", "-")
        pages.append((label, t))
    return pages


def collect(pages, entries, start, stop):
    out = []
    for entry in entries:
        display, pats = entry[0], entry[1]
        rx = [re.compile(p, re.I) for p in pats]
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


def compress(nums, cap=15):
    nums = sorted(set(nums))
    parts, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        parts.append(str(nums[i]) if i == j else f"{nums[i]}\u2013{nums[j]}")
        i = j + 1
    if len(parts) > cap:
        parts = parts[:cap] + ["passim"]
    return ", ".join(parts)


def esc(s):
    for a, b in (("\\", "\\\\"), ("#", "\\#"), ("$", "\\$"), ("@", "\\@"), ("<", "\\<"),
                 (">", "\\>"), ("*", "\\*"), ("_", "\\_"), ("[", "\\["), ("]", "\\]"), ("`", "\\`")):
        s = s.replace(a, b)
    return s


def fmt(display):
    parts = display.split("*")
    return "".join(f"#emph[{esc(p)}]" if k % 2 else esc(p) for k, p in enumerate(parts))


def run(pdf: Path, build: Path):
    pages = page_texts(pdf)
    labels = [l for l, _ in pages]
    try:
        start = next(i for i, l in enumerate(labels) if l == "1")
    except StopIteration:
        print("  index skipped (page labels not found)")
        return
    stop = len(pages)
    for i in range(start, len(pages)):
        head = pages[i][1].strip()[:120]
        if head.startswith("Glossary of") or "Glossary of Psychological" in head:
            stop = i
            break

    items = sorted(collect(pages, indexdata.SUBJECT, start, stop), key=lambda x: x[0].lower().lstrip("*"))
    groups = {}
    for d, h in items:
        groups.setdefault(d.lstrip("*")[0].upper(), []).append((d, h))

    s = ['#import "/templates/book.typ": *\n', '#matter.update("back")\n']
    s.append('#front-heading([Subject Index], runhead: "Subject Index")\n')
    s.append('#par(first-line-indent: 0pt)[#text(size: 9pt, style: "italic")[Page references are to the numbered pages of the main text and the appendices. Bold entries indicate the principal discussion of a topic.]]\n#v(0.6em)\n')
    s.append("#columns(2, gutter: 14pt)[\n")
    for letter, group in sorted(groups.items()):
        s.append(f'#block(sticky: true, above: 1.0em, below: 0.4em, text(font: sans, size: 8.6pt, weight: "bold", fill: teal)[{esc(letter)}])\n')
        for display, hits in group:
            s.append('#block(above: 0.3em, below: 0.3em, par(first-line-indent: 0pt, hanging-indent: 1.1em, '
                     f'justify: false)[#text(size: 8.4pt)[{fmt(display)}#box(width: 1fr, repeat[ ])#h(0.35em){compress(hits)}]]\n')
    s.append("]\n")
    (build / "generated_indexes.typ").write_text("".join(s), encoding="utf-8")
    print(f"  indexed {stop - start} pages, {len(items)} entries")
