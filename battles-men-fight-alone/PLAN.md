# Production Plan — *Battles Men Fight Alone*

**Subtitle:** The Hidden Struggles, Silent Sacrifices, Emotional Wounds, and Unspoken Realities of Manhood
**Author:** Prof. Adeleke Daniel Durojaiye (PhD)
**Trim size:** 6 × 9 in. · **Genre:** narrative nonfiction / psychological insight / practical self-development
**Readership:** adult men, couples, parents, counselors, educators, general readers
**Central message:** men can carry serious responsibilities without being expected to endure emotional
suffering in isolation.

## Source documents
| File | Purpose |
| --- | --- |
| `SOURCE.md` | The author's supplied outline, saved verbatim (45 chapters, 12 parts, 20 appendices). |
| `TOC.md` | Authoritative headings for the manuscript workflow — **verbatim titles**. |
| `PLAN.md` | This file: production plan, conventions, progress log. |

## Planned structure (from the supplied outline)
* 12 parts · 45 chapters · Epilogue + Final Reflection
* Front matter: half title, full title, copyright, dedication, acknowledgments, foreword, preface, author's note, introduction, how to use this book
* Appendices A–T (20 practical worksheets, plans, and exercises)
* Back matter: glossary, recommended reading, references and bibliography, subject index, about the author, other publications

## Editorial direction
Narrative nonfiction with compelling, realistic life situations; **original illustrative stories**
(composite characters, clearly framed as illustrative); evidence-informed psychological explanation
(draw on well-established, mainstream findings; no invented studies, statistics, or quotations);
practical exercises in every chapter and the appendices. Warm, dignified, non-accusatory tone that
acknowledges male experience without blaming partners, families, or faith communities. Any real-world
help-seeking information (Appendix Q) must stay current and locally useful (Nigeria, Africa, and
international pathways) with crisis guidance stated carefully.

## Manuscript conventions (planned, mirroring the existing `book/` pipeline)
* `manuscript/chapters/NNa.md … NNe.md` (5 files per chapter, sort order = reading order).
* Part opener in the first file of a part: `# Title {.part num="I" img="/images/part1.jpg" summary="..."}`
* Chapter heading: `# Title {.chapter num="5" short="Running head"}`; sections `## …`; subsections `### …`
* Callouts: `::: objectives | casebox | keypoint | exercise | practice | illustration | summary | reading`
* Each chapter: objectives → opening scene/story → body sections (one per outline bullet) →
  key point box → reflective/practical exercise → chapter summary → further reading.
* Appendices: `# Title {.appendix letter="A"}` in `manuscript/appendices/`.
* Spelling: **British spelling**, consistent with the publisher's house style in this repository.
* Every chapter and appendix ends with something the reader can *do*, not only read.

## Build (planned — to be reused from the sibling `book/` project)
The repository already contains a working Pandoc → Typst → PDF pipeline in `book/scripts/`
(`build.py`, `figures.py`, `figlib.py`, `wordcount.py`), `book/templates/*.typ`, and
`book/filters/book.lua`. When writing begins, this project will adopt that pipeline (new
`scripts/` + `templates/` set, or a parameterised copy) so the PDF is built the same way:
```
python3 -m venv ~/.venv && ~/.venv/bin/pip install -r book/requirements.txt   # existing project
~/.venv/bin/python <scripts>/figures.py      # diagrams (if any)
~/.venv/bin/python <scripts>/build.py        # multi-pass build -> final/*.pdf
```
No build tooling has been created or modified for this book yet.

## Status
* **Saved (this commit):** the author's full outline, verbatim, plus the authoritative TOC and this plan.
* **Not started:** manuscript text, front matter, appendices, back matter, figures, build pipeline.
* Next step is the author's decision: agree target word count per chapter, then write front matter
  (preface, introduction, how-to-use) and Part I, chapters 1–4.
