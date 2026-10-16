#!/usr/bin/env python3
"""Build the complete book PDF.

Pipeline
  1. (optional) regenerate diagrams           scripts/figures.py
  2. Markdown -> Typst for every manuscript file (Pandoc + filters/book.lua)
  3. Assemble build/main.typ (cover, prelims, TOC, body, appendices, back matter)
  4. Pass 1 compile -> extract page text -> generate Tables of Cases / Treaties /
     Legislation and the three indexes with real page numbers
  5. Pass 2 compile -> final/<title>.pdf

Usage:  python book/scripts/build.py [--figures] [--fast]
  --fast  skip the second (indexing) pass
"""
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pypandoc
import typst

BOOK = Path(__file__).resolve().parents[1]
MS = BOOK / "manuscript"
BUILD = BOOK / "build"
FINAL = BOOK / "final"
FILTER = BOOK / "filters" / "book.lua"
FONTS = BOOK / "fonts"
PDF_NAME = "Becoming-a-Doctor-of-International-Energy-and-Natural-Resources-Law.pdf"

sys.path.insert(0, str(BOOK / "scripts"))


def md_files(sub):
    return sorted((MS / sub).glob("*.md"))


def convert(md: Path) -> str:
    return pypandoc.convert_file(
        str(md), "typst", format="markdown-auto_identifiers+smart",
        extra_args=["--lua-filter", str(FILTER), "--wrap=preserve"])


def chunk(name, files):
    out = ['#import "/templates/book.typ": *\n\n']
    for f in files:
        out.append(f"// ---- {f.relative_to(BOOK)} ----\n")
        out.append(convert(f))
        out.append("\n")
    p = BUILD / f"{name}.typ"
    p.write_text("".join(out), encoding="utf-8")
    return p.name


MAIN = r'''
#import "/templates/book.typ": *
#show: setup

// ============================== COVER ======================================
#matter.update("cover")
#page(margin: 0pt, header: none, footer: none, numbering: none, {
  set text(hyphenate: false)
  if __COVER__ != none { place(image(__COVER__, width: 100%, height: 100%, fit: "cover")) }
  else { place(rect(width: 100%, height: 100%, fill: ivory)) }
  place(top + left, dx: 0.55in, dy: 0.6in, block(width: 4.9in, {
    set par(justify: false, leading: 0.32em, first-line-indent: 0pt)
    line(length: 3.2em, stroke: 2pt + bronze)
    v(0.5em)
    text(font: sans, size: 13pt, weight: "semibold", tracking: 0.18em, fill: teal)[BECOMING A DOCTOR OF]
    v(0.35em)
    text(font: serif, size: 29pt, weight: "semibold", fill: teal, tracking: 0.01em)[INTERNATIONAL ENERGY AND NATURAL RESOURCES LAW]
    v(0.6em)
    line(length: 100%, stroke: 0.8pt + bronze)
    v(0.25em)
    text(font: sans, size: 8.6pt, tracking: 0.12em, fill: rgb("#3c4a4f"))[DOCTORAL TEXT AND ADVANCED PROFESSIONAL REFERENCE]
  }))
  place(bottom + left, dx: 0in, dy: 0in, block(width: 100%, fill: teal, inset: (x: 0.55in, y: 0.32in), {
    set par(justify: false, first-line-indent: 0pt)
    text(font: sans, size: 9.2pt, weight: "semibold", tracking: 0.14em, fill: rgb("#F2E3C9"))[TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA]
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
    text(font: sans, size: 15pt, weight: "semibold", fill: teal, tracking: 0.04em)[BECOMING A DOCTOR OF INTERNATIONAL ENERGY AND NATURAL RESOURCES LAW]
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
    text(font: sans, size: 11pt, weight: "semibold", tracking: 0.2em, fill: bronze)[BECOMING A DOCTOR OF]
    v(0.6em)
    text(font: serif, size: 25pt, weight: "semibold", fill: teal)[International Energy and Natural Resources Law]
    v(1.4em)
    text(font: serif, size: 11.5pt, style: "italic", fill: grey)[A Doctoral Text and Advanced Professional Reference on Resource Sovereignty, Energy Transactions, Investment Protection, Environmental and Climate Governance, and International Dispute Resolution]
    v(2.2in)
    text(font: sans, size: 10pt, weight: "semibold", tracking: 0.12em, fill: teal)[TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA]
    v(0.4em)
    text(font: sans, size: 8.5pt, fill: grey)[First Edition · 2026]
  }))
]
#include "copyright.typ"

#include "dedication.typ"
#book-toc()
#include "front_b.typ"
#include "generated_tables.typ"
#list-of(image, "List of Figures and Illustrations")
#list-of(table, "List of Tables and Legal Frameworks")
#include "front_c.typ"

// ============================== MAIN TEXT ==================================
#pagebreak(to: "odd", weak: true)
#set page(numbering: "1")
#counter(page).update(1)
#context [#metadata((kind: "main-start", page: here().page())) <pmark>]
#include "chapters.typ"

// ============================== APPENDICES =================================
#context [#metadata((kind: "appendix-start", page: here().page())) <pmark>]
#include "appendices.typ"

// ============================== BACK MATTER ================================
#context [#metadata((kind: "back-start", page: here().page())) <pmark>]
#include "back.typ"
#include "generated_indexes.typ"
'''


def assemble(cover):
    BUILD.mkdir(exist_ok=True)
    # The front matter is split so that the TOC and lists sit in the conventional places.
    front = md_files("front")
    fb = [f for f in front if "10" <= f.name < "50"]  # foreword ... tables
    fc = [f for f in front if f.name >= "50"]         # introduction, how to use
    chunk("front_b", fb)
    chunk("front_c", fc)
    chunk("chapters", md_files("chapters"))
    chunk("appendices", md_files("appendices"))
    chunk("back", md_files("back"))
    for t in ("copyright.typ", "dedication.typ"):
        shutil.copy(BOOK / "templates" / t, BUILD / t)
    gen = BUILD / "generated_indexes.typ"
    for name in ("generated_indexes.typ", "generated_tables.typ"):
        if not (BUILD / name).exists():
            (BUILD / name).write_text('#import "/templates/book.typ": *\n// generated in pass 2\n')
    cov = f'"{cover}"' if cover else "none"
    (BUILD / "main.typ").write_text(MAIN.replace("__COVER__", cov), encoding="utf-8")


def compile_pdf(out):
    t = time.time()
    typst.compile(str(BUILD / "main.typ"), output=str(out), root=str(BOOK),
                  font_paths=[str(FONTS)])
    print(f"  compiled {out.name} in {time.time() - t:.1f}s")


def main():
    args = sys.argv[1:]
    if "--figures" in args:
        subprocess.run([sys.executable, str(BOOK / "scripts" / "figures.py")], check=True)
    cover = "/images/cover.jpg" if (BOOK / "images" / "cover.jpg").exists() else None
    print("Converting manuscript ...")
    assemble(cover)
    FINAL.mkdir(exist_ok=True)
    p1 = BUILD / "pass1.pdf"
    print("Pass 1 ...")
    compile_pdf(p1)
    if "--fast" in args:
        shutil.copy(p1, FINAL / PDF_NAME)
        return
    import make_indexes
    print("Indexing ...")
    make_indexes.run(p1, BUILD)
    print("Pass 2 ...")
    p2 = BUILD / "pass2.pdf"
    compile_pdf(p2)
    # A third pass guarantees that page numbers are stable after the indexes are inserted
    make_indexes.run(p2, BUILD)
    compile_pdf(FINAL / PDF_NAME)
    print("Done ->", FINAL / PDF_NAME)


if __name__ == "__main__":
    main()
