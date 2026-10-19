# MFT Lecture Decks

A lecture-deck collection for the Master of Marriage and Family Therapy: one
deck per week, sixteen weeks per course, in PowerPoint and vector PDF.

The house style is a sibling of the book project in `../book`: the same
EB Garamond / Source Sans 3 pairing, the same ivory-and-ink ground, with one
accent colour per course so that twenty-six courses read as one imprint rather
than twenty-six brands.

## What is built

| Deliverable | Path | Content |
|---|---|---|
| Weekly deck (PPTX) | `out/MFT-701/MFT-701-Wnn-*.pptx` | 15 slides, native shapes and text |
| Weekly deck (PDF) | `out/MFT-701/MFT-701-Wnn-*.pdf` | same 15 slides, embedded fonts |
| Complete course (PPTX) | `out/MFT-701/MFT-701-Complete-Course.pptx` | 228 slides: cover, contents, 16 weeks, colophon |
| Complete course (PDF) | `out/MFT-701/MFT-701-Complete-Course.pdf` | 228 pages |
| Fonts | `out/MFT-701/_Fonts (install before presenting)/` | install these first (see below) |

## The weekly grammar (15 slides)

1. Week divider — number, title, standfirst, epigraph, keywords
2. Learning outcomes — five, written as observable capabilities
3. Where this week sits — the course as one argument
4. Key concepts — four terms, each with an "in the room" application
5. Lecture I — four propositions plus a clinical implication and a seminar question
6. Lecture II — same structure
7. Figure — a purpose-drawn diagram with a caption
8. Lecture III — same structure
9. Clinical vignette — a fictitious composite with three reflection prompts
10. Skills laboratory — four timed steps and a debrief
11. Seminar — five questions
12. Assessment — major task, criteria, formative work, a note
13. Reading — six sources, the core text marked
14. Synthesis — one sentence on a dark ground
15. Next week — title, preview, and read/annotate/bring

In the bound course edition the closing slide is dropped where another week
follows, so that a divider never repeats the title printed a page earlier; the
last week keeps it. Weekly decks always carry all fifteen.

Speaker notes are attached to the divider, figure, vignette and skills slides.

## Build

```bash
python3 -m venv ~/.venv-deck
~/.venv-deck/bin/pip install python-pptx typst pillow matplotlib pymupdf fonttools

~/.venv-deck/bin/python -m decks.build --course 701            # everything
~/.venv-deck/bin/python -m decks.build --course 701 --weeks 1  # one week, for review
~/.venv-deck/bin/python -m decks.build --course 701 --figures  # redraw diagrams only
```

Run from the repository root.

## How it works

```
decks/
  theme.py            palette, type scale, course metadata, canvas geometry
  layout.py           primitives (rect, rule, ellipse, text, image) + font-metric wrapping
  slides.py           the fifteen compositions, composed from primitives
  render_pptx.py      primitives -> native PowerPoint shapes and text boxes
  render_pdf.py       primitives -> Typst -> vector PDF at the same 960x540 pt canvas
  figures/            matplotlib diagram toolkit
    style.py          shared ink, paper and accent; OFL faces
    archetypes.py     cycle, chain, matrix, layers, spectrum, flow, venn, axes, genogram, hub
    mft701.py         the sixteen figure specifications for MFT 701
  content/            course data: syllabus plus the Week objects
  qa.py               geometry, font-fallback and grammar checks
  build.py            the build driver
```

Text is wrapped here, with the real font files, before it is placed. That means
the PDF and the PPTX share the same line breaks, and PowerPoint has nothing to
re-flow. Both renderers consume the same primitive list, so the two formats are
siblings rather than look-alikes.

New courses: copy `content/mft701/`, change the `Course` and the week data, add
`figures/mftNNN.py`, and add an entry to `theme.ACCENTS`.

## Typography

Install the fonts in `_Fonts (install before presenting)` before opening a
deck. Without them PowerPoint substitutes other faces and the design changes.
Both families are licensed under the SIL Open Font License; the licence files
are included.

## Content discipline

- British spelling; en dashes and true quotation marks throughout.
- Vignettes are explicitly fictitious composites; no real client material.
- Citations are real, standard works. Figures and page numbers are those of the
  editions named; verify against your library's copies before printing.
- The curriculum's `1.71` unit value is reproduced exactly as supplied.
