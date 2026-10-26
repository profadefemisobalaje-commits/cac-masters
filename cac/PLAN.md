# Production Plan — *Student Handbook of Comprehensive Lectures*
## Master in Children and Adolescent Counseling (CAC)

Author/publisher line: **TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA** · First Edition 2026 · 6 × 9 in.
Governing specification: **`HANDBOOK-STANDARD.md`** at the repository root. Every rule below is an
instance of that standard; where they differ, the standard wins and this file is corrected.

Content rules: academic and professional; British spelling in the handbook's own prose; APA 7th for
citations and the reference list; hypothetical case material explicitly labelled fictitious; no
fabricated quotations, sources, statistics or page numbers; AI photographs labelled
"Illustrative image (AI-generated)"; safeguarding duties stated as jurisdiction-dependent.

## Source of truth
* `cac/CURRICULUM.md` — the supplied curriculum, verbatim, plus the queries for the registrar.
* `cac/courses.csv` — machine-readable copy. **31 course entries · 1.6 units each · 49.6 units.**
* The programme overview in the handbook is **generated from `courses.csv`** by
  `scripts/programme.py`, never retyped. Codes, titles and unit values must match byte-for-byte.

## Structure
* **Four parts:** I — First Semester (chapters 1–9) · II — Second Semester (10–16) ·
  III — Third Semester (17–23, including CAC. 760 Master Thesis) · IV — Elective pool (24–31).
* **Chapters are numbered sequentially 1–31**, not by course code, because `CAC. 701` is used twice
  in the supplied curriculum. The course code, semester and unit value are printed on every chapter
  opener and in the running head, so traceability to `courses.csv` is preserved (§1).
* **Six lecture units per course chapter.** 1.6 units ≈ 24 notional learning hours → 6 units × 4 hours,
  split lecture / seminar / supervised or independent study. Each unit follows the fifteen-part
  weekly grammar of §2 of the standard.
* Each unit: outcomes → where it sits → key concepts → Lectures I–III → figure → vignette → skills
  laboratory → seminar questions → assessment → reading → synthesis → next unit.

## Chapter map
| # | Code | Title | Semester |
|---|---|---|---|
| 1 | CAC. 701 | Fundamentals of Counseling Theories | 1 |
| 2 | CAC. 701 | Child Development Theories | 1 |
| 3 | CAC. 702 | Adolescent Development | 1 |
| 4 | CAC. 703 | Ethics in Counseling | 1 |
| 5 | CAC. 704 | Counseling Techniques and Skills | 1 |
| 6 | CAC. 705 | Group Counseling for Children and Adolescents | 1 |
| 7 | CAC. 706 | Family Systems Therapy | 1 |
| 8 | CAC. 707 | Play Therapy Techniques | 1 |
| 9 | CAC. 708 | Fundamentals of Counseling Theories | 1 |
| 10 | CAC. 709 | Crisis Intervention Strategies | 2 |
| 11 | CAC. 710 | Multicultural Counseling | 2 |
| 12 | CAC. 711 | Assessment and Diagnosis in Children and Adolescents | 2 |
| 13 | CAC. 712 | Behavioral Interventions | 2 |
| 14 | CAC. 713 | School Counseling Practices | 2 |
| 15 | CAC. 714 | Substance Abuse Counseling | 2 |
| 16 | CAC. 715 | Trauma-Informed Care | 2 |
| 17 | CAC. 716 | Mindfulness and Stress Reduction | 3 |
| 18 | CAC. 717 | Research Methods in Counseling | 3 |
| 19 | CAC. 718 | Consultation in School Settings | 3 |
| 20 | CAC. 719 | Special Education and Counseling | 3 |
| 21 | CAC. 720 | Child and Adolescent Psychopathology | 3 |
| 22 | CAC. 721 | Research Methodology | 3 |
| 23 | CAC. 760 | Master Thesis | 3 |
| 24 | CAC. 722 | Developmental Disabilities and Counseling | Elective |
| 25 | CAC. 723 | Legal Issues in Counseling | Elective |
| 26 | CAC. 724 | Community Resources and Referrals | Elective |
| 27 | CAC. 725 | Technology in Counseling | Elective |
| 28 | CAC. 726 | Internship in Child and Adolescent Counseling | Elective |
| 29 | CAC. 727 | Professional Identity and Development | Elective |
| 30 | CAC. 728 | Parent-Child Interaction Therapy | Elective |
| 31 | CAC. 729 | Advanced Topics in Counseling Children and Adolescents | Elective |

## Build
```
python3 -m venv ~/.venv && ~/.venv/bin/pip install pypandoc-binary typst pillow matplotlib
~/.venv/bin/python cac/scripts/programme.py     # regenerate front/50-programme.md from courses.csv
~/.venv/bin/python cac/scripts/build.py         # 2-pass build, PDF/UA-1 -> cac/final/*.pdf
~/.venv/bin/python cac/scripts/build.py --fast  # single pass, for review
~/.venv/bin/python cac/scripts/wordcount.py     # per-chapter word counts against the 8,000 floor
```

## Manuscript conventions (`cac/manuscript/chapters/NNx.md`)
* Files sorted lexicographically; chapter NN split `NNa.md` … `NNf.md` (one lecture unit per file).
* Part opener in the first file of each part:
  `# Title {.part num="I" summary="..."}`.
* Chapter heading:
  `# Title {.chapter num="1" short="Running head" code="CAC. 701" semester="First" units="1.6"}`.
* Lecture unit: `# Title {.unit num="1" week="1" hours="4"}`.
* Sections inside a unit `## …`; sub-sections `###`.
* Callouts: `::: objectives | keypoint | casebox | vignette | skills | comparative | exercise |
  research | assessment | summary | reading | instrument | practice | safeguard | illustration`.
  **Fence syntax rule:** a titled callout must be written `::: {.kind title=Words_with_underscores}` —
  dotted class inside braces, title unquoted with underscores. Pandoc's `smart` extension curls
  quoted attribute values before the div parse (breaking them), and a bare class inside braces is
  not a class; the filter restores underscores to spaces in the printed label.
* References: `::: refs` (APA 7th, hanging indent) at the end of each chapter and in the back matter.
* Figures: `![Caption. *Source:* prepared for this edition.](/figures/fig-NN-MM.png){width=92%}`,
  with alt text in the caption text (PDF/UA-1 requirement).
* Tables: pipe table followed by `Table: caption` (caption set above the table).

## Definition of done
See §9 of `HANDBOOK-STANDARD.md`. The build must pass: word-count floor, curriculum match,
fifteen-part grammar per unit, geometry, **no font fallback**, contrast (bronze text `#8A5A26`),
tagged PDF/UA-1 structure, resolved cross-references, British-spelling check, and the integrity
sample.

## Status — the series

One volume per course, 31 volumes. Build with `scripts/build_book.py <slug>`, QA with
`scripts/qa_book.py <slug>`. A volume is released to `cac/books/<slug>/final/` only when its QA
gate passes.

| # | Slug | Course | Weeks done | Status |
|---|---|---|---|---|
| 1 | cac701 | CAC. 701 Fundamentals of Counseling Theories | 4 of 16 | in progress — weeks 1–4 typeset, QA passing |
| 2 | cac701b | CAC. 701 Child Development Theories | 0 | queued |
| 3 | cac702 | CAC. 702 Adolescent Development | 0 | queued |
| 4 | cac703 | CAC. 703 Ethics in Counseling | 0 | queued |

Remaining volumes follow in curriculum order (see the chapter map above for codes and titles).

## Progress log
* Curriculum captured verbatim in `cac/CURRICULUM.md` and `cac/courses.csv`; five registrar queries
  recorded (duplicate `CAC. 701`, duplicated title at `CAC. 708`, 9·7·7 semester loading,
  `CAC. 717`/`CAC. 721` overlap, the uniform `1.6` unit value). None silently corrected.
* Series architecture: one volume per course under `cac/books/<slug>/`, shared design in
  `cac/templates/handbook.typ`, PDF/UA-1 export, QA gate `scripts/qa_book.py`.
* Volume 1 (cac701): front matter, weeks 1–4 (psychodynamic and attachment lineage begun), eight
  diagrams, 58 pages, QA passing. Weeks 5–16 to follow, then volumes 2 onward.
* Git: `cac/build/` and `cac/books/*/build/` are ignored; per-volume release PDFs are committed
  with the volume they belong to.
