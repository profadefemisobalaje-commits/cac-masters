#!/usr/bin/env python3
"""Build Battles Men Fight Alone (6 x 9 in) as a print-ready PDF.

Pipeline
  1. (optional) regenerate diagrams           scripts/figures.py
  2. Markdown -> Typst for every manuscript file (Pandoc + filters/book.lua)
  3. Assemble build/main.typ (cover, prelims, TOC, lists, body, appendices, back matter)
  4. Compile pass 1 -> extract page text -> build the Subject Index with real page numbers
  5. Compile pass 2 and 3 (page numbers stabilise)

Usage:  ~/.venv/bin/python scripts/build.py [--figures] [--fast]
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
PDF_NAME = "Battles-Men-Fight-Alone.pdf"

sys.path.insert(0, str(BOOK / "scripts"))


def md_files(sub):
    return sorted((MS / sub).glob("*.md"))


TABLEFIG = re.compile(r"(#figure\(\n  align\(center\)\[#table\(.*?\n  \)\])\n\)", re.S)


def convert(md: Path) -> str:
    t = pypandoc.convert_file(
        str(md), "typst", format="markdown-auto_identifiers+smart",
        extra_args=["--lua-filter", str(FILTER), "--wrap=preserve"])
    # pandoc wraps captionless pipe tables in a figure with no kind and no
    # caption; label them as tables so they stay out of the List of Figures
    return TABLEFIG.sub(r"\1, kind: table, caption: none\n)", t)


def chunk(name, files):
    out = ['#import "/templates/book.typ": *\n\n']
    for f in files:
        out.append(f"// ---- {f.relative_to(BOOK)} ----\n")
        out.append(convert(f))
        out.append("\n")
    (BUILD / f"{name}.typ").write_text("".join(out), encoding="utf-8")


MAIN = r'''
#import "/templates/book.typ": *
#show: setup

// ============================== COVER ======================================
#matter.update("cover")
#page(margin: 0pt, header: none, footer: none, numbering: none, {
  set text(hyphenate: false)
  if __COVER__ != none { place(image(__COVER__, width: 100%, height: 100%, fit: "cover")) }
  else { place(rect(width: 100%, height: 100%, fill: teal)) }
  place(top + left, dx: 0.5in, dy: 0.55in, block(width: 5.0in, {
    set par(justify: false, leading: 0.32em, first-line-indent: 0pt)
    text(font: sans, size: 8.6pt, weight: "semibold", tracking: 0.2em, fill: rgb("#F2E3C9"))[PROF. ADELEKE DANIEL DUROJAIYE (PHD)]
    v(0.9em)
    line(length: 3.2em, stroke: 2pt + bronze)
    v(0.7em)
    text(font: sans, size: 34pt, weight: "semibold", fill: white, tracking: 0.01em)[BATTLES MEN]
    v(0.1em)
    text(font: sans, size: 34pt, weight: "semibold", fill: white, tracking: 0.01em)[FIGHT ALONE]
    v(0.9em)
    line(length: 100%, stroke: 0.8pt + bronze)
    v(0.5em)
    set par(leading: 0.52em)
    text(font: serif, size: 12.4pt, style: "italic", fill: rgb("#EFE6D6"))[The Hidden Struggles, Silent Sacrifices, Emotional Wounds, and Unspoken Realities of Manhood]
  }))
  place(bottom + left, dx: 0.5in, dy: -0.55in, block(width: 5.0in, {
    set par(justify: false, first-line-indent: 0pt)
    line(length: 100%, stroke: 0.6pt + rgb("#F2E3C9"))
    v(0.4em)
    text(font: sans, size: 8.4pt, weight: "semibold", tracking: 0.16em, fill: rgb("#F2E3C9"))[TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA]
  }))
})
#page(header: none, footer: none, numbering: none)[]

// ============================ PRELIMINARIES ================================
#matter.update("front")
#set page(numbering: "i")
#counter(page).update(1)
// Half title
#page(header: none, footer: none)[
  #opening-marker
  #v(2.6in)
  #set text(hyphenate: false)
  #align(center, block(width: 85%, {
    set par(justify: false, first-line-indent: 0pt, leading: 0.45em)
    text(font: sans, size: 15pt, weight: "semibold", fill: teal, tracking: 0.04em)[BATTLES MEN FIGHT ALONE]
  }))
]
#page(header: none, footer: none)[#opening-marker]
// Full title
#page(header: none, footer: none)[
  #opening-marker
  #set par(justify: false, first-line-indent: 0pt)
  #set text(hyphenate: false)
  #v(1.05in)
  #align(center, block(width: 92%, {
    set par(leading: 0.45em)
    line(length: 3em, stroke: 1.6pt + bronze)
    v(1.2em)
    text(font: sans, size: 20pt, weight: "semibold", fill: teal)[Battles Men Fight Alone]
    v(0.9em)
    text(font: serif, size: 12pt, style: "italic", fill: grey)[The Hidden Struggles, Silent Sacrifices, Emotional Wounds, and Unspoken Realities of Manhood]
    v(1.6em)
    text(font: sans, size: 11pt, weight: "semibold", tracking: 0.06em, fill: teal)[Prof. Adeleke Daniel Durojaiye (PhD)]
    v(1.9in)
    text(font: sans, size: 10pt, weight: "semibold", tracking: 0.12em, fill: teal)[TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA]
    v(0.4em)
    text(font: sans, size: 8.5pt, fill: grey)[First Edition · 2026]
  }))
]
#include "copyright.typ"

#include "dedication.typ"
#book-toc()
#include "front_b.typ"
#list-of(image, "List of Figures and Illustrations")
#list-of(table, "List of Tables", note: "The numbered tables are the principal exhibits of each chapter, ordered by chapter and by sequence within it. Short working tables — checklists, inventories, and the blank schedules a reader completes — appear in the text unnumbered and are not listed here.")
#include "front_c.typ"

// ============================== MAIN TEXT ==================================
#pagebreak(to: "odd", weak: true)
#set page(numbering: "1")
#counter(page).update(1)
#context [#metadata((kind: "main-start", page: here().page())) <pmark>]
#include "chapters.typ"
#include "concluding.typ"

// ============================== APPENDICES =================================
#context [#metadata((kind: "appendix-start", page: here().page())) <pmark>]
#include "appendices.typ"

// ============================== BACK MATTER ================================
#context [#metadata((kind: "back-start", page: here().page())) <pmark>]
#include "back_a.typ"
#include "generated_indexes.typ"
#include "back_b.typ"
'''


def assemble(cover):
    BUILD.mkdir(exist_ok=True)
    front = md_files("front")
    chunk("front_b", [f for f in front if "10" <= f.name < "50"])
    chunk("front_c", [f for f in front if f.name >= "50"])
    chunk("chapters", md_files("chapters"))
    chunk("concluding", md_files("concluding"))
    chunk("appendices", md_files("appendices"))
    back = md_files("back")
    chunk("back_a", [f for f in back if f.name < "40"])
    chunk("back_b", [f for f in back if f.name >= "40"])
    for t in ("copyright.typ", "dedication.typ"):
        shutil.copy(BOOK / "templates" / t, BUILD / t)
    if not (BUILD / "generated_indexes.typ").exists():
        (BUILD / "generated_indexes.typ").write_text('#import "/templates/book.typ": *\n// generated in pass 2\n')
    cov = f'"{cover}"' if cover else "none"
    (BUILD / "main.typ").write_text(MAIN.replace("__COVER__", cov), encoding="utf-8")


def compile_pdf(out):
    t = time.time()
    typst.compile(str(BUILD / "main.typ"), output=str(out), root=str(BOOK),
                  font_paths=[str(FONTS)])
    print(f"  compiled {out.name} in {time.time() - t:.1f}s")


def strip_blank_page_furniture(path):
    """A page left blank by a recto break should carry no running head or folio.

    Typst's `pagebreak(to: "odd")` creates such pages but still applies the
    header/footer, so any page whose entire content is a folio plus an upper-case
    running head (and a header rule) is cleared.
    """
    import re
    import pymupdf

    doc = pymupdf.open(path)
    cleared = []
    for page in doc:
        if page.get_images():
            continue
        lines = [l.strip() for l in page.get_text().splitlines() if l.strip()]
        if len(lines) != 2:
            continue
        if not any(re.fullmatch(r"\d{1,4}", l) for l in lines):
            continue
        other = [l for l in lines if not re.fullmatch(r"\d{1,4}", l)][0]
        if not re.fullmatch(r"[A-Z0-9 ·:\-–—'’.,&]+", other):
            continue
        if not any(abs(dr["rect"].height) < 4 and dr["rect"].width > 200
                   for dr in page.get_drawings()):
            continue
        page.add_redact_annot(page.rect)
        cleared.append(page.number + 1)
    for number in cleared:
        doc[number - 1].apply_redactions()
    if cleared:
        tmp = path.with_name(path.stem + ".tmp.pdf")
        doc.save(tmp, garbage=3, deflate=True)
        doc.close()
        tmp.replace(path)
        print(f"  cleared running head and folio from {len(cleared)} blank pages")
    else:
        doc.close()

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
    make_indexes.run(p2, BUILD)
    print("Pass 3 (final) ...")
    compile_pdf(FINAL / PDF_NAME)
    strip_blank_page_furniture(FINAL / PDF_NAME)
    print("Done ->", FINAL / PDF_NAME)


if __name__ == "__main__":
    main()
