#!/usr/bin/env python3
"""Build the complete book PDF.

  1. (optional) regenerate diagrams        scripts/figures.py
  2. Markdown -> Typst for every manuscript file (Pandoc + filters/book.lua)
  3. Assemble build/main.typ (cover, prelims, TOC, body, appendices, back matter)
  4. Compile -> final/Becoming-a-Doctor-of-Marriage-and-Family-Therapy.pdf

Usage:  python book-mft/scripts/build.py [--figures]
"""
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
PDF_NAME = "Becoming-a-Doctor-of-Marriage-and-Family-Therapy.pdf"

TITLE = "BECOMING A DOCTOR OF"
TITLE_MAIN = "MARRIAGE AND FAMILY THERAPY"
TITLE_MIXED = "Marriage and Family Therapy"
SUBTITLE = ("A Doctoral Text and Advanced Professional Reference on Family Systems Theory, "
            "Couple and Family Assessment, Clinical Practice, Supervision, and Research "
            "in Marriage and Family Therapy")
SUBKICK = "DOCTORAL TEXT AND ADVANCED PROFESSIONAL REFERENCE"
PUBLISHER = "TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA"


def md_files(sub):
    return sorted((MS / sub).glob("*.md"))


def convert(md: Path) -> str:
    t = pypandoc.convert_file(
        str(md), "typst", format="markdown-auto_identifiers+smart",
        extra_args=["--lua-filter", str(FILTER), "--wrap=preserve"])
    # wrap figure "Source:" notes so the List of Figures can omit them
    return re.sub(r"(#emph\[Source:\].*?)(\n\s*\]\s*\n\s*\))", r"#figsrc[\1]\2", t, flags=re.S)


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
    text(font: sans, size: 13pt, weight: "semibold", tracking: 0.18em, fill: teal)[__TITLE__]
    v(0.35em)
    text(font: serif, size: 27pt, weight: "semibold", fill: teal, tracking: 0.01em)[__TITLEMAIN__]
    v(0.6em)
    line(length: 100%, stroke: 0.8pt + bronze)
    v(0.25em)
    text(font: sans, size: 8.6pt, tracking: 0.12em, fill: rgb("#3c4a4f"))[__SUBKICK__]
  }))
  place(bottom + left, dx: 0in, dy: 0in, block(width: 100%, fill: teal, inset: (x: 0.55in, y: 0.32in), {
    set par(justify: false, first-line-indent: 0pt)
    text(font: sans, size: 9.2pt, weight: "semibold", tracking: 0.14em, fill: rgb("#F2E3C9"))[__PUBLISHER__]
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
    text(font: sans, size: 15pt, weight: "semibold", fill: teal, tracking: 0.04em)[__TITLEUPPER__]
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
    text(font: sans, size: 11pt, weight: "semibold", tracking: 0.2em, fill: bronze)[__TITLE__]
    v(0.6em)
    text(font: serif, size: 25pt, weight: "semibold", fill: teal)[__TITLEMIXED__]
    v(1.4em)
    text(font: serif, size: 11.5pt, style: "italic", fill: grey)[__SUBTITLE__]
    v(2.0in)
    text(font: sans, size: 10pt, weight: "semibold", tracking: 0.12em, fill: teal)[__PUBLISHER__]
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
#list-of(table, "List of Tables")
#include "front_c.typ"

// ============================== MAIN TEXT ==================================
#pagebreak(to: "odd", weak: true)
#set page(numbering: "1")
#counter(page).update(1)
#context [#metadata((kind: "main-start", page: here().page())) <pmark>]
#include "chapters.typ"

// ============================== APPENDICES =================================
#pagebreak(to: "odd", weak: true)
#context [#metadata((kind: "appendix-start", page: here().page())) <pmark>]
#include "appendices.typ"

// ============================== BACK MATTER ================================
#pagebreak(to: "odd", weak: true)
#context [#metadata((kind: "back-start", page: here().page())) <pmark>]
#include "back.typ"
'''


def assemble(cover):
    BUILD.mkdir(exist_ok=True)
    # Front matter is split so that the TOC and lists sit in the conventional places.
    front = md_files("front")
    fb = [f for f in front if f.name < "50"]   # foreword ... about
    fc = [f for f in front if f.name >= "50"]  # introduction, how to use
    chunk("front_b", fb)
    chunk("front_c", fc)
    chunk("chapters", md_files("chapters"))
    chunk("appendices", md_files("appendices"))
    chunk("back", md_files("back"))
    for t in ("copyright.typ", "dedication.typ"):
        shutil.copy(BOOK / "templates" / t, BUILD / t)
    if not (BUILD / "generated_tables.typ").exists():
        (BUILD / "generated_tables.typ").write_text(
            '#import "/templates/book.typ": *\n// generated during build\n')
    cov = f'"{cover}"' if cover else "none"
    main = (MAIN.replace("__COVER__", cov)
                .replace("__TITLEUPPER__", f"{TITLE} {TITLE_MAIN}")
                .replace("__TITLEMAIN__", TITLE_MAIN)
                .replace("__TITLEMIXED__", TITLE_MIXED)
                .replace("__SUBTITLE__", SUBTITLE)
                .replace("__SUBKICK__", SUBKICK)
                .replace("__TITLE__", TITLE)
                .replace("__PUBLISHER__", PUBLISHER))
    (BUILD / "main.typ").write_text(main, encoding="utf-8")


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
    # Two passes: pass 1 stabilises the layout, pass 2 writes final page numbers.
    print("Pass 1 ...")
    compile_pdf(BUILD / "pass1.pdf")
    print("Pass 2 ...")
    compile_pdf(FINAL / PDF_NAME)
    print("Done ->", FINAL / PDF_NAME)


if __name__ == "__main__":
    main()
