#!/usr/bin/env python3
"""Build the CAC student handbook PDF.

  1. Markdown -> Typst for every manuscript file (Pandoc + filters/book.lua)
  2. Assemble build/main.typ (cover, prelims, TOC, lists, body, appendices, back matter)
  3. Compile -> final/*.pdf, exported to PDF/UA-1 (tagged, accessible) unless --no-ua

Usage:  ~/.venv/bin/python cac/scripts/build.py [--fast] [--no-ua]
"""
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
TEMPLATE = "handbook.typ"
PDF_NAME = "CAC-Student-Handbook-of-Comprehensive-Lectures.pdf"

TITLE = "STUDENT HANDBOOK OF"
TITLE_MAIN = "COMPREHENSIVE LECTURES"
TITLE_MIXED = "Comprehensive Lectures"
SUBTITLE = ("Master in Children and Adolescent Counseling · Complete Lecture Course, "
            "Semesters One to Three, with the Elective Pool")
SUBKICK = "MASTER IN CHILDREN AND ADOLESCENT COUNSELING"
PUBLISHER = "TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA"


def md_files(sub):
    return sorted((MS / sub).glob("*.md"))


def convert(md: Path) -> str:
    t = pypandoc.convert_file(
        str(md), "typst", format="markdown-auto_identifiers+smart",
        extra_args=["--lua-filter", str(FILTER), "--wrap=preserve"])
    # wrap figure "Source:" notes so that the List of Figures can omit them
    import re
    return re.sub(r"(#emph\[Source:\].*?)(\n\s*\]\s*\n\s*\))", r"#figsrc[\1]\2", t, flags=re.S)


def chunk(name, files):
    out = [f'#import "/templates/{TEMPLATE}": *\n\n']
    for f in files:
        out.append(f"// ---- {f.relative_to(BOOK)} ----\n")
        out.append(convert(f))
        out.append("\n")
    p = BUILD / f"{name}.typ"
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
  place(top + left, dx: 0.55in, dy: 0.55in, block(width: 4.9in, {
    set par(justify: false, leading: 0.32em, first-line-indent: 0pt)
    line(length: 3.2em, stroke: 2pt + bronze)
    v(0.5em)
    text(font: sans, size: 12pt, weight: "semibold", tracking: 0.16em, fill: teal)[__TITLE__]
    v(0.3em)
    text(font: serif, size: 25pt, weight: "semibold", fill: teal, tracking: 0.01em)[__TITLEMAIN__]
    v(0.55em)
    line(length: 100%, stroke: 0.8pt + bronze)
    v(0.25em)
    text(font: sans, size: 8.4pt, tracking: 0.1em, fill: rgb("#3c4a4f"))[__SUBKICK__]
  }))
  place(bottom + left, dx: 0in, dy: 0in, block(width: 100%, fill: teal, inset: (x: 0.55in, y: 0.32in), {
    set par(justify: false, first-line-indent: 0pt)
    text(font: sans, size: 8.8pt, weight: "semibold", tracking: 0.12em, fill: rgb("#F2E3C9"))[__PUBLISHER__]
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
#include "chapters.typ"

// ============================== APPENDICES =================================
#pagebreak(to: "odd", weak: true)
#include "appendices.typ"

// ============================== BACK MATTER ================================
#pagebreak(to: "odd", weak: true)
#include "back.typ"
'''


def assemble(cover):
    BUILD.mkdir(exist_ok=True)
    front = md_files("front")
    fb = [f for f in front if f.name < "50"]    # foreword ... abbreviations
    fc = [f for f in front if f.name >= "50"]   # programme overview, how to use
    chunk("front_b", fb)
    chunk("front_c", fc)
    chunk("chapters", md_files("chapters"))
    chunk("appendices", md_files("appendices"))
    chunk("back", md_files("back"))
    for t in ("copyright.typ", "dedication.typ"):
        src = BOOK / "templates" / t
        if src.exists():
            shutil.copy(src, BUILD / t)
        else:
            (BUILD / t).write_text(f'#import "/templates/{TEMPLATE}": *\n', encoding="utf-8")
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


def compile_pdf(out, ua=True):
    t = time.time()
    kw = dict(root=str(BOOK), font_paths=[str(FONTS)])
    if ua:
        kw["pdf_standards"] = ["pdf/ua-1"]
    try:
        typst.compile(str(BUILD / "main.typ"), output=str(out), **kw)
        tag = "PDF/UA-1 tagged" if ua else "untagged"
    except Exception as e:
        if not ua:
            raise
        print(f"  ! PDF/UA-1 export failed ({e}); retrying untagged")
        typst.compile(str(BUILD / "main.typ"), output=str(out), root=str(BOOK),
                      font_paths=[str(FONTS)])
        tag = "untagged (UA export failed)"
    print(f"  compiled {out.name} [{tag}] in {time.time() - t:.1f}s")


def main():
    args = sys.argv[1:]
    ua = "--no-ua" not in args
    cover = "/images/cover.jpg" if (BOOK / "images" / "cover.jpg").exists() else None
    print("Converting manuscript ...")
    assemble(cover)
    FINAL.mkdir(exist_ok=True)
    if "--fast" in args:
        compile_pdf(FINAL / PDF_NAME, ua=ua)
    else:
        print("Pass 1 ...")
        compile_pdf(BUILD / "pass1.pdf", ua=False)
        print("Pass 2 ...")
        compile_pdf(FINAL / PDF_NAME, ua=ua)
    print("Done ->", FINAL / PDF_NAME)


if __name__ == "__main__":
    main()
