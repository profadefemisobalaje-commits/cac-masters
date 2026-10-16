# Production Plan — *Becoming a Doctor of Marriage and Family Therapy*

Author/publisher line: **TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA** · First Edition 2026 · 6 × 9 in.
Content rules: strictly academic and professional; secular in method (no faith-based or devotional content);
British spelling; hypothetical case material explicitly labelled; no fabricated quotations or sources;
AI photographs labelled "illustrative image (AI-generated)".

## Requirement
* ≥ 8,000 words per course chapter (main text). Check with `python book-mft/scripts/wordcount.py`.
* Figures, diagrams, and photographs placed at the point in the argument where they are needed.

## Build
```
python3 -m venv ~/.venv && ~/.venv/bin/pip install -r book/requirements.txt
~/.venv/bin/python book-mft/scripts/figures.py     # draw diagrams -> book-mft/figures
~/.venv/bin/python book-mft/scripts/build.py       # 2-pass build -> book-mft/final/*.pdf
```

## Manuscript conventions (`book-mft/manuscript/chapters/NNx.md`)
* One file per course chapter set, split `NNa.md` … `NNe.md` (~2,700–4,000 words each).
* Part opener: `# Title {.part num="I" img="/images/part1.jpg" summary="..."}` in the first file of a Part.
* Chapter heading: `# Title {.chapter num="1" short="Running head"}`; sections `## 1.1 ...`; subsections `###`.
* Callouts: `::: objectives | casebox | keypoint | comparative | exercise | research | summary | reading | instrument | practice | illustration`.
* Each chapter: objectives → introduction → 8 numbered sections → case illustrations → applied exercise →
  summary → doctoral research questions → further reading.
* Figures: `![Caption. *Source:* prepared for this edition.](/figures/fig-NN-MM.png){width=92%}`,
  drawn in `scripts/figures.py` (functions `fig_NN_MM`).
* Photographs: `/images/photo-NN-*.jpg`, always captioned "Illustrative image (AI-generated)."
* Tables: pipe table followed by `Table: caption` (caption on the line after the table).

## Status — volume 1
* **Completed: MFT. 901 Advanced Theories of Family Systems** — 15,193 words; 9 diagrams
  (fig-01-01 … fig-01-09), 3 illustrative photographs, part opener and cover art.
* Front matter: foreword, preface, acknowledgements, about, abbreviations, introduction, how-to-use,
  copyright and dedication templates.
* Appendices: A (genogram notation, with notation plate), B (comparative grid of theories + theory-evaluation
  checklist), C (doctoral programme, study pathway, assessment design).
* Back matter: selected bibliography (primary sources, evidence base, critique, professional sources).
* Final PDF: `final/Becoming-a-Doctor-of-Marriage-and-Family-Therapy.pdf` (100 pp).

## Roadmap — remaining courses (one chapter each)
Write in programme order; each chapter is its own Part of the series volume, or a separate volume if the
series is issued course-by-course:
Year 1: MFT. 902 research methods · 903 multicultural · 904 advanced clinical practice · 905 psychopathology ·
906 ethics and law · 907 child and adolescent development · 908 couples therapy techniques.
Year 2: MFT. 909 trauma-informed care · 910 substance abuse and family dynamics · 911 family life cycle ·
912 group therapy · 913 neurobiology of attachment · 914 supervision · 915 assessment and diagnosis ·
916 conflict resolution and mediation.
Year 3: MFT. 917 parenting · 918 integrative approaches · 919 family therapy with LGBTQ+ families ·
920 technology in practice · 921 play therapy · 922 spirituality in family therapy (as academic subject) ·
923 advanced research methodology · 970 dissertation.
Electives: MFT. 924–931.

## Progress log
* Volume 1 (MFT. 901) complete. Figures to fig-01-09 and fig-a-01. Word count verified with `scripts/wordcount.py`.
* Reusable infrastructure: `templates/book.typ` (retitled), `filters/book.lua`, `scripts/figlib.py`,
  `scripts/figures.py`, `scripts/build.py`, `fonts/`. Copy `book-mft/` as the base for the next volume,
  or append chapters to `manuscript/chapters/` for a single omnibus volume.
* Git: do not stage `build/` output. Figures and final PDF are tracked in `book-mft/`.
