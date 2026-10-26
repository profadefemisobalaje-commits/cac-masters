#!/usr/bin/env python3
"""Build ONE course book of the CAC series.

Each course of the curriculum is a separate volume, sized to carry a full
14-16 week semester: one lecture week per unit, every week carrying outcomes,
key concepts, three lectures, at least one purpose-drawn diagram, worked
examples, a practical, seminar questions, assessment, reading and a synthesis.

Layout:  cac/books/<book>/manuscript/{front,weeks,appendices,back}
         cac/books/<book>/figures/
         cac/books/<book>/final/

Shared design (template, fonts, filter) lives one level up in cac/ and is
reached through the Typst root, so every volume of the series is typeset
identically.

Usage:  ~/.venv/bin/python cac/scripts/build_book.py <book> [--fast] [--no-ua]
"""
import csv
import re
import shutil
import sys
import time
from pathlib import Path

import pypandoc
import typst

CAC = Path(__file__).resolve().parents[1]          # .../cac
TEMPLATE = "handbook.typ"
FILTER = CAC / "filters" / "book.lua"
FONTS = CAC / "fonts"
COURSES = CAC / "courses.csv"

# Titles of the series; keep in step with courses.csv (byte-exact titles).
SERIES = "CAC Masters Series"


def course_rows():
    with COURSES.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def md_files(ms, sub):
    d = ms / sub
    return sorted(d.glob("*.md")) if d.exists() else []


def _plain_alt(cap: str) -> str:
    """Plain-text alternative for a figure, derived from its caption (§5)."""
    cap = cap.split("#figsrc[")[0]
    cap = re.sub(r"#emph\[([^\]]*)\]", r"\1", cap)
    cap = re.sub(r"#[a-zA-Z-]+\[([^\]]*)\]", r"\1", cap)
    cap = cap.replace("---", "-").replace("--", "-")
    cap = re.sub(r"\s+", " ", cap).strip()
    return cap.replace("\\", "").replace('"', "'")


def convert(md: Path) -> str:
    t = pypandoc.convert_file(
        str(md), "typst", format="markdown-auto_identifiers+smart",
        extra_args=["--lua-filter", str(FILTER), "--wrap=preserve"])
    # wrap figure "Source:" notes so the List of Figures can omit them
    t = re.sub(r"(#emph\[Source:\].*?)(\n\s*\]\s*\n\s*\))", r"#figsrc[\1]\2", t, flags=re.S)

    # PDF/UA-1 requires alt text on every image: derive it from the caption.
    def add_alt(m):
        args, cap = m.group("args"), m.group("cap")
        alt = _plain_alt(cap)
        if not alt:
            alt = "Diagram prepared for this edition."
        return (f'#figure(image("{m.group("path")}"{args}, alt: "{alt}"),\n'
                f'  caption: [\n{cap}\n  ]\n)')

    t = re.sub(r'#figure\(image\("(?P<path>[^"]+)"(?P<args>[^)]*)\),\s*\n\s*caption: \[\n'
               r'(?P<cap>.*?)\n\s*\]\s*\n\)', add_alt, t, flags=re.S)
    return t


def chunk(build, name, files):
    out = [f'#import "/templates/{TEMPLATE}": *\n\n']
    for f in files:
        out.append(f"// ---- {f.name} ----\n")
        out.append(convert(f))
        out.append("\n")
    p = build / f"{name}.typ"
    p.write_text("".join(out), encoding="utf-8")
    return p.name


MAIN = r'''
#import "/templates/handbook.typ": *
#show: setup

// ============================== COVER ======================================
#matter.update("cover")
#page(margin: 0pt, header: none, footer: none, numbering: none, {
  set text(hyphenate: false)
  if __COVER__ != none { place(image(__COVER__, width: 100%, height: 100%, fit: "cover")) }
  else { place(rect(width: 100%, height: 100%, fill: ivory)) }
  place(top + left, dx: 0.55in, dy: 0.5in, block(width: 4.9in, {
    set par(justify: false, leading: 0.3em, first-line-indent: 0pt)
    text(font: sans, size: 7.6pt, weight: "semibold", tracking: 0.24em, fill: bronze-text)[__SERIES__]
    v(0.4em)
    line(length: 3.2em, stroke: 2pt + bronze)
    v(0.45em)
    text(font: sans, size: 11.4pt, weight: "semibold", tracking: 0.14em, fill: teal)[__TITLE__]
    v(0.3em)
    text(font: serif, size: 23pt, weight: "semibold", fill: teal, tracking: 0.01em)[__TITLEMAIN__]
    v(0.5em)
    line(length: 100%, stroke: 0.8pt + bronze)
    v(0.25em)
    text(font: sans, size: 8.2pt, tracking: 0.1em, fill: rgb("#3c4a4f"))[__SUBKICK__]
  }))
  place(bottom + left, dx: 0in, dy: 0in, block(width: 100%, fill: teal, inset: (x: 0.55in, y: 0.32in), {
    set par(justify: false, first-line-indent: 0pt)
    text(font: sans, size: 8.6pt, weight: "semibold", tracking: 0.12em, fill: rgb("#F2E3C9"))[__PUBLISHER__]
  }))
})
#page(header: none, footer: none, numbering: none)[]

// ============================ PRELIMINARIES ================================
#matter.update("front")
#set page(numbering: "i")
#counter(page).update(1)
#page(header: none, footer: none)[
  #opening-marker
  #v(2.3in)
  #set text(hyphenate: false)
  #align(center, block(width: 85%, {
    set par(justify: false, first-line-indent: 0pt, leading: 0.45em)
    text(font: sans, size: 13pt, weight: "semibold", fill: teal, tracking: 0.04em)[__TITLEUPPER__]
  }))
]
#page(header: none, footer: none)[#opening-marker]
#page(header: none, footer: none)[
  #opening-marker
  #set par(justify: false, first-line-indent: 0pt)
  #set text(hyphenate: false)
  #v(1.1in)
  #align(center, block(width: 92%, {
    set par(leading: 0.45em)
    line(length: 3em, stroke: 1.6pt + bronze)
    v(1.2em)
    text(font: sans, size: 10.5pt, weight: "semibold", tracking: 0.18em, fill: bronze-text)[__TITLE__]
    v(0.6em)
    text(font: serif, size: 24pt, weight: "semibold", fill: teal)[__TITLEMIXED__]
    v(1.3em)
    text(font: serif, size: 11pt, style: "italic", fill: grey)[__SUBTITLE__]
    v(1.9in)
    text(font: sans, size: 9.4pt, weight: "semibold", tracking: 0.1em, fill: teal)[__PUBLISHER__]
    v(0.4em)
    text(font: sans, size: 8.5pt, fill: grey)[First Edition · 2026]
  }))
]
#include "copyright.typ"
#include "dedication.typ"
#book-toc()
#include "front_b.typ"
#list-of(image, "List of Figures and Illustrations")
#list-of(table, "List of Tables")
#include "front_c.typ"

// ============================== MAIN TEXT ==================================
#pagebreak(to: "odd", weak: true)
#set page(numbering: "1")
#counter(page).update(1)
#include "weeks.typ"

// ============================== APPENDICES =================================
#pagebreak(to: "odd", weak: true)
#include "appendices.typ"

// ============================== BACK MATTER ================================
#pagebreak(to: "odd", weak: true)
#include "back.typ"
'''


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(1)
    book = args[0]
    BOOK = CAC / "books" / book
    if not BOOK.is_dir():
        print(f"no such book: {BOOK}")
        sys.exit(1)
    meta = {}
    for line in (BOOK / "BOOK.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("- "):
            k, _, v = line[2:].partition(": ")
            meta[k.strip()] = v.strip()
    code = meta.get("code", book)
    title = meta.get("title", book)
    semester = meta.get("semester", "")
    units = meta.get("units", "1.6")

    MS = BOOK / "manuscript"
    BUILD = BOOK / "build"
    FINAL = BOOK / "final"
    BUILD.mkdir(exist_ok=True)
    FINAL.mkdir(exist_ok=True)

    print(f"Building {code} — {title}")
    front = md_files(MS, "front")
    fb = [f for f in front if f.name < "50"]
    fc = [f for f in front if f.name >= "50"]
    chunk(BUILD, "front_b", fb)
    chunk(BUILD, "front_c", fc)
    chunk(BUILD, "weeks", md_files(MS, "weeks"))
    chunk(BUILD, "appendices", md_files(MS, "appendices"))
    chunk(BUILD, "back", md_files(MS, "back"))
    for t in ("copyright.typ", "dedication.typ"):
        src = BOOK / "templates" / t if (BOOK / "templates" / t).exists() else CAC / "templates" / t
        shutil.copy(src, BUILD / t)

    words = title.split()
    main_title = " ".join(words[:1]) if False else title
    sub = (f"{code} · {semester} Semester · {units} units · A complete lecture course "
           f"for a sixteen-week semester")
    main = (MAIN.replace("__COVER__", "none")
                .replace("__SERIES__", SERIES.upper())
                .replace("__TITLEUPPER__", title.upper())
                .replace("__TITLEMAIN__", title.upper())
                .replace("__TITLEMIXED__", title)
                .replace("__SUBTITLE__", sub)
                .replace("__SUBKICK__", "MASTER IN CHILDREN AND ADOLESCENT COUNSELING")
                .replace("__TITLE__", code)
                .replace("__PUBLISHER__", "TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA"))
    (BUILD / "main.typ").write_text(main, encoding="utf-8")

    ua = "--no-ua" not in flags
    pdf = FINAL / f"{book}.pdf"

    def compile_pdf(out, ua):
        t = time.time()
        kw = dict(root=str(CAC), font_paths=[str(FONTS)])
        if ua:
            kw["pdf_standards"] = ["ua-1"]
        try:
            typst.compile(str(BUILD / "main.typ"), output=str(out), **kw)
            tag = "PDF/UA-1" if ua else "untagged"
        except Exception as e:
            if not ua:
                raise
            print(f"  ! PDF/UA-1 export failed ({e}); retrying untagged")
            typst.compile(str(BUILD / "main.typ"), output=str(out),
                          root=str(CAC), font_paths=[str(FONTS)])
            tag = "untagged (UA failed)"
        print(f"  compiled {out.name} [{tag}] in {time.time() - t:.1f}s")

    if "--fast" in flags:
        compile_pdf(pdf, ua)
    else:
        print("Pass 1 ...")
        compile_pdf(BUILD / "pass1.pdf", False)
        print("Pass 2 ...")
        compile_pdf(pdf, ua)
    print("Done ->", pdf)


if __name__ == "__main__":
    main()
