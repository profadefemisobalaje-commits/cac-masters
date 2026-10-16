# Production Plan — *Becoming a Doctor of International Energy and Natural Resources Law*

Author/publisher line: **TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA** · First Edition 2026 · 6 × 9 in.
Content rules: strictly secular, academic, legally grounded; British spelling; hypothetical exercises
explicitly labelled fictitious; no fabricated quotations; AI images labelled "illustrative image".

## Requirement
* ≥ 300,000 words of **main text** (30 chapters; front and back matter excluded) → target ≥ 10,300 words/chapter.
* Check with `python book/scripts/wordcount.py`.

## Build
```
python3 -m venv ~/.venv && ~/.venv/bin/pip install -r book/requirements.txt
~/.venv/bin/python book/scripts/figures.py        # draw diagrams -> book/figures
~/.venv/bin/python book/scripts/build.py          # 3-pass build with indexes -> book/final/*.pdf
~/.venv/bin/python book/scripts/build.py --fast   # single pass, no indexes
```

## Manuscript conventions (`book/manuscript/chapters/NNx.md`)
* Files are concatenated in sort order; each chapter is split into `NNa.md` … `NNe.md` (5 files, ~2,200+ words each, target ≥ 11,000/chapter). Section titles: see `book/TOC.md` (verbatim).
* First file of a Part starts with `# Title {.part num="I" img="/images/partN.jpg" summary="..."}`.
* Chapter heading: `# Title {.chapter num="5" short="Running head"}`; sections `## 5.1 ...`; subsections `###`.
* Callouts: `::: objectives | casebox | keypoint | comparative | exercise | research | summary | reading | instrument | practice` (optional `title="..."`).
* Each chapter: objectives → introduction → 8 numbered sections → casebox(es) → exercise (hypothetical) → summary → research questions → further reading.
* Figures: `![Caption. *Source:* prepared for this edition.](/figures/fig-NN-MM.png){width=90%}`; drawn in `scripts/figures.py` (functions `fig_NN_MM`).
* Photos (AI-generated, labelled): `/images/photo-*.jpg`, Part openers `/images/partN.jpg`.
* Tables: pipe tables followed by `Table: caption`.

## Front / back matter
* Front (`manuscript/front`, roman pages): 10-foreword, 20-preface, 30-acknowledgements, 40-about,
  45-abbreviations; generated Tables of Cases/Treaties/Legislation; lists of figures/tables; 50-introduction, 60-how-to-use.
* Appendices A–T in `manuscript/appendices` (`# Title {.appendix letter="A"}`).
* Back: 10-bibliography (+ generated indexes from `scripts/refdata.py`).

## Status
See `git log`. Chapters completed are listed by `wordcount.py`.

## Progress log
* Ch1–9 complete (98,147 words after Ch9). Each chapter: 5 files a–e, ~11–13.6k words. Figures to fig-09-01.
* Citation discipline: avoid precise statutory section numbers unless certain; hedge recent events; no invented quotations.
* Next: Ch10 Renewable (fig 10-01 support mechanisms), Ch11 Nuclear (fig 11-01 pillars), Ch12 Hydrogen/CCS (fig 12-01).
* Remaining after chapters: appendices A–T, front matter (foreword, preface, acknowledgements, about, abbreviations, introduction, how-to-use, disclaimer), bibliography, refdata.py, full 3-pass build.
