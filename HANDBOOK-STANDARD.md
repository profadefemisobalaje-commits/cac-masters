# Student Handbook Standard — *Comprehensive Lectures*

**Publisher/imprint:** TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA
**Applies to:** the final PDF student handbook that binds the lecture corpus to the curriculum
(`mft/CURRICULUM.md`, `mft/courses.csv`) and to the weekly decks (`decks/`).
**Status:** governing specification. Every deviation must be recorded in the build's `PLAN.md`.

This document names the standard for each layer of the artefact — content, pedagogy, editorial,
typography, accessibility, integrity, legal, archival, and quality assurance — so that a handbook
is auditable rather than merely attractive. Layers 1–7 already exist in this repository as house
practice and are cited from source; layers 8–10 are additions this handbook requires.

---

## 1. Authority and scope

| Rule | Source |
|---|---|
| Course codes, titles, unit values and year allocation are reproduced **exactly as supplied**; never normalised, re-spelled or re-numbered. | `mft/CURRICULUM.md` ("preserved exactly as given"); `decks/README.md` (the `1.71` unit precedent) |
| The curriculum file is the single source of truth for programme structure. The handbook is generated against `mft/courses.csv`, not retyped. | `mft/CURRICULUM.md` |
| A handbook teaches and examines. It **does not confer** a qualification, and says so on the copyright page. | `book-mft/templates/copyright.typ`, "Academic notice" |
| Every lecture in the handbook maps to a curriculum line: `Course code → unit → year → category`. No orphan content. | derived |

**Traceability requirement.** Each lecture unit carries a header block: course code, title, units,
year, week number, notional contact hours, and the outcome codes it serves. A reader (or an
accreditation reviewer) must be able to walk from any page to the curriculum line it satisfies.

## 2. Pedagogical standard

- **Outcomes-based design, constructively aligned** (Biggs): every lecture unit states outcomes as
  *observable capabilities*, and each outcome is matched by teaching content, a formative task and
  an assessed task. An outcome with no assessment is a defect.
- **Outcome verbs** taken from the revised Bloom taxonomy; banned openers for outcomes: *understand,
  know, appreciate, be aware of, learn about*. Required form: verb + object + criterion
  ("Formulate a structural diagnosis of a three-generation case, naming the boundary crossings that
  sustain it").
- **Credit-hour convention:** 3 units ≈ 45 notional learning hours (Carnegie unit), split as
  lecture / seminar / supervised practice / independent study. The split is printed per course.
- **Lecture-unit grammar — the weekly structure already fixed for the decks**
  (`decks/README.md`), which the handbook adopts as its weekly skeleton:

  1. week divider (number, title, standfirst, epigraph, keywords) · 2. learning outcomes (five,
  observable) · 3. where this week sits (the course as one argument) · 4. key concepts (four terms,
  each with an "in the room" application) · 5–6, 8. lectures I–III (four propositions each, plus a
  clinical implication and a seminar question) · 7. figure (purpose-drawn diagram, captioned) ·
  9. clinical vignette (fictitious composite, three reflection prompts) · 10. skills laboratory
  (four timed steps and a debrief) · 11. seminar (five questions) · 12. assessment (major task,
  criteria, formative work) · 13. reading (six sources, core text marked) · 14. synthesis (one
  sentence) · 15. next week (title, preview, read/annotate/bring).

- **Semester span — 14 to 16 weeks.** Every course volume is a complete lecture course for one
  semester: **sixteen weeks** as the series norm (fourteen teaching weeks, week 15 an integration
  and practicals week, week 16 revision and examination preparation). A volume that cannot carry a
  sixteen-week semester is incomplete, whatever its length.
- **Per-week word floor (University directive of 27 October 2026): no week of any course
  subject shall be less than 8,000 words.** Each volume declares the floor in its `BOOK.md`
  (`week-floor: 8000`) and the QA gate enforces it week by week from volume 4 onward. Coverage
  still governs structure: every week must carry a complete four-hour lecture — outcomes, three
  lectures, at least one diagram, worked examples, a practical, seminar questions, assessment,
  reading and a synthesis — and the floor is filled with teaching substance (extended lectures,
  further worked examples, case sequences, statutes and codes quoted, seminar material), never
  with padding. A week a tutor could not teach from is a defect; a week below the floor is now
  also a defect.
- **Illustration is mandatory, not decorative.** Every week carries at least one purpose-drawn
  diagram placed at the point in the argument where it is needed; where a real or realistic image
  aids understanding (a play-therapy room, a classroom, an observation setting, an instrument
  plate), one is included and labelled per §6. A week with no figure must justify the absence in
  the build log.
- **Examples and practicals are mandatory.** Every lecture sequence ends in a worked example drawn
  from practice with children or adolescents, and every week carries a practical — a timed skills
  exercise, a formulation task, a role-play, an observation, or an analysis of supplied material —
  with a debrief. Theory without a practical is not taught in this series.

- **Contact-hour transparency** for online delivery: state synchronous vs asynchronous time, and the
  assessment window, for each week.

## 3. Editorial standard

- **British spelling throughout**; `lang: "en"`, `region: "gb"` in the Typst setup
  (`book-mft/templates/book.typ`), old-style numerals in body text, lining numerals in tables and
  headings.
- En dashes for ranges and relationships; true quotation marks; spaced em-dash parentheticals. No
  doubled hyphens, no straight quotes (`decks/README.md`, "Content discipline").
- Terms of art **bold at first definition**, indexed thereafter (`book-mft/manuscript/front/60-how-to-use.md`).
- Citation style: **house Oxford-derived form** — `Surname Initials, *Title* (edn, Publisher year)` —
  as used in `book-mft/manuscript/back/10-bibliography.md`. *Alternative for a psychology-facing
  handbook: APA 7th.* The choice is global; mixing is a defect. (Decision recorded in §11.)
- **Arbiter for anything the house style does not cover:** *Chicago Manual of Style*, 17th ed. —
  numbers, dates, titles of works, punctuation of quotations, bibliographic order.
- Headings are numbered by chapter and section (`## 5.1`, `### 5.1.2`); no unnumbered headings below
  level 2 in main matter.
- Voice: academic and professional, second person only in the "how to use" matter and in exercise
  instructions.

## 4. Covers

Each volume opens with a designed front cover and closes with a back cover in the house
palette. Cover art is drawn per edition (vector line work, no stock or generated imagery):
a motif proper to the volume — the confluence of lineages for volume 1, growth rings for
volume 2 — keeping the upper third of the page calm for the typographic block. The front
cover carries the series line with volume number, course code, title, programme line and
the imprint band. The back cover carries the volume blurb, its strand list, the imprint
and the series statement. Covers carry no running heads, no folios and no outline
entries, and the cover image carries alt text for PDF/UA-1.

## 4. Production and typographic standard

| Element | Specification | Source |
|---|---|---|
| Typesetting engine | Typst, driven from Markdown via Pandoc + `filters/book.lua` | `book-mft/scripts/build.py` |
| Trim size | **6 × 9 in** for the reading edition; **US Letter / A4** if the handbook is also issued as a workbook | `book-mft/PLAN.md` |
| Body face | EB Garamond 10.6 pt, justified, leading 0.6 em, first-line indent 1.15 em | `templates/book.typ` |
| Display face | Source Sans 3 (headings, running heads, captions, tables, callout labels) | `templates/book.typ` |
| Font licensing | Both families **SIL OFL**; licence files shipped in `fonts/` and named on the copyright page; 100 % embedded in the PDF | `book-mft/fonts/`, `decks/README.md` |
| Margins | inside 0.85 in, outside 0.68 in, top 0.86 in, bottom 0.80 in, binding left | `templates/book.typ` |
| Running heads | verso = volume title, recto = chapter short title; suppressed on opening pages; 7.6 pt Source Sans 3, tracked, bronze rule beneath | `templates/book.typ` |
| Pagination | front matter roman, main and back matter arabic; every part/chapter/appendix opens recto (`pagebreak(to: "odd")`) | `templates/book.typ` |
| Numbering | figures and tables numbered **per chapter** (`fig-N.M`); tables captioned above, figures below | `templates/book.typ`, `60-how-to-use.md` |
| Callouts | the fixed set: `objectives`, `casebox`, `keypoint`, `comparative`, `exercise`, `research`, `summary`, `reading`, `instrument`, `practice`, `illustration` | `templates/book.typ` |
| Figures | vector diagrams drawn by `scripts/figures.py` → `figures/fig-NN-MM.png`, caption + `*Source:* prepared for this edition.` | `book-mft/PLAN.md` |
| Photographs | AI-generated only, captioned **"Illustrative image (AI-generated)."** | `book-mft/PLAN.md` |
| PDF metadata | `set document(title:, author:, keywords:)` — title, imprint as author, subject keywords, language `en-GB` | `templates/book.typ` |
| Navigation | bookmark tree to heading level 3; hyperlinked TOC, list of figures, list of tables, indexes | `templates/book.typ` |
| Build | 3-pass when indexes are generated, 2-pass otherwise; indexes and cross-references resolved before release | `book/scripts/build.py`, `PLAN.md` |

### 4.1 Palette — WCAG contrast audit (measured, this edition)

| Ink | White | Ivory `#FBF8F1` | Teal-light `#E3EEF0` | Bronze-light `#F4EADB` | Verdict |
|---|---|---|---|---|---|
| Ink `#1B1B1B` | 17.2 | 16.2 | 14.6 | 14.5 | pass AAA |
| Teal `#0F4C5C` | 9.5 | 9.0 | 8.0 | 8.0 | pass AAA |
| Grey `#5E6468` | 6.0 | 5.7 | 5.1 | 5.0 | pass AA |
| **Bronze `#9C6B30`** | **4.6** | **4.3** | **3.9** | **3.9** | **fails AA on ivory and on both tint grounds** |

**Required correction for the handbook.** Bronze is used for 7.8–9 pt callout labels, part openers,
figure numbers and rules — i.e. small text on tinted grounds, where WCAG 2.2 AA requires 4.5:1.
Darken the bronze ink used for *text* to **`#8A5A26`** (5.9 on white, 5.5 on ivory, 5.0 on teal-light,
4.9 on bronze-light). The existing `#9C6B30` may remain for rules, fills and other non-text elements,
where only the 3:1 non-text contrast criterion applies.

## 5. Accessibility standard (new — not yet specified in this repository)

- **Conformance target: WCAG 2.2 Level AA**, applied to the PDF as a document.
- **Tagged PDF (PDF/UA-1, ISO 14289-1)**: structure tree, correct heading hierarchy with no skipped
  levels, arteact tagging for decorative rules and ghost numerals, `/Lang` = `en-GB`, document title
  set, "DisplayDocTitle" preferred.
- **Alternative text on every informative figure**; decorative images marked artefact/`null` alt.
  Figure captions are not a substitute for alt text.
- **Reading order** verified by extraction (single-column body order; callouts read in place).
- **Colour is never the only channel**: callouts carry a printed label (`objectives`, `casebox`, …),
  not just an accent colour; diagrams carry textual labels, not colour-coded meaning alone.
- **Contrast**: 4.5:1 for body and caption text, 3:1 for rules and diagram strokes (see §4.1).
- **Minimum type**: 7.6 pt is the floor (running heads); no content text below 8.2 pt.
- **No colour-dependent assessment material**; tables carry header rows that repeat across page
  breaks; no text in images.
- US institutional drivers to note on the copyright page or in the front matter: **Section 504 /
  ADA**, and **Section 508 (29 U.S.C. § 794d)** where the institution receives federal funds.
- Accessibility statement: contact route for alternative formats, and a statement that the PDF is
  tagged and screen-reader tested.

## 6. Academic integrity standard

- **No fabricated quotations, sources, statistics or page numbers.** Citations are real, standard
  works; figures and page numbers are those of the editions named and are verified before printing
  (`decks/README.md`; `book/PLAN.md`, "Citation discipline").
- Uncertain statutory or doctrinal detail is **hedged or omitted**, never invented
  (`book/PLAN.md`).
- **Hypothetical material is labelled**: vignettes and exercises are fictitious composites, marked as
  such at the point of use and in the copyright page notice. No real client, patient or student
  material.
- **AI-generated imagery is labelled** at every instance ("Illustrative image (AI-generated)").
- **Standardised instruments**: named, described, not reproduced; copyright status and publisher
  terms noted in an `instrument` callout (`60-how-to-use.md`).
- Reporting of research findings is summary-level, with an explicit instruction to consult the
  original publication ("Research notice").
- Where sources are contested, the contest is stated rather than resolved silently.

## 7. Legal and institutional standard

The copyright page carries, verbatim in structure, the notices already drafted in
`book-mft/templates/copyright.typ`:

1. **Academic notice** — teaching text; confers no qualification.
2. **Professional notice** — nothing authorises practice beyond the reader's training, competence,
   licensure and lawful scope; readers must obtain current codes and statutes; law stated as
   understood at the date of writing.
3. **Research notice** — findings summarised; consult originals.
4. **Hypothetical material** — fictitious, teaching use only, resemblance coincidental.
5. **Illustrations** — diagrams prepared for the edition; AI photographs labelled.

Plus: full imprint line, edition statement, printing line, `© 2026 Triune Biblical University Global
Extension USA. All rights reserved.`, the brief-quotation exception, ISBN (print) and ISBN
(electronic) per **ISO 2108**, typesetting and trim-size colophon, and the OFL font credit.
If student data or submissions appear in any example: **FERPA** applies and the material must be
de-identified and consented — otherwise exclude it.

## 8. Archival and distribution standard (new)

- **Release PDF:** the reading edition, tagged, fonts embedded, bookmarked — the file students get.
- **Archival master:** a **PDF/A-2b (ISO 19005-2)** conversion of the release PDF, held outside Git
  with the edition record; no transparency, no JS, no encryption, all fonts embedded.
- **File naming:** `Title-Handbook-ed1-YYYY.pdf`, kebab-case, matching the existing
  `final/*.pdf` convention.
- **Size discipline:** final PDFs are staged only at the final build
  (`git add -A <project> ':!<project>/final'`, per `book/PLAN.md`); build output is ignored
  (`.gitignore`).
- **Version control of the text:** the manuscript is the source of truth in Git; the PDF is a
  derived artefact, never hand-edited. Every release is a tag with a changelog.

## 9. Quality-assurance gate — definition of done

Automated (extend `decks/qa.py` and `scripts/wordcount.py` to the handbook):

- [ ] **Coverage and the week floor.** Every week carries all fifteen parts of the grammar; every
      week carries at least one figure, at least one worked example and one practical; no week is
      a stub. Where the volume's `BOOK.md` sets `week-floor` (8,000 words by the directive of
      27 October 2026), `qa_book.py` fails any week below the floor; volumes released before the
      directive carry no floor field and report lengths for information only.
- [ ] Every course volume maps one-to-one to a `courses.csv` row; code, title, units byte-exact.
- [ ] Grammar check: all fifteen parts present in every lecture unit; no empty units.
- [ ] Geometry check: no text outside the type area, no overflowing callout, no orphaned heading.
- [ ] Font check: **no fallback faces** in the compiled PDF; only EB Garamond / Source Sans 3 subsets.
- [ ] Contrast check: all text pairs ≥ 4.5:1; bronze text corrected per §4.1.
- [ ] Structure check: tagged PDF, `/Lang` set, heading levels unbroken, every figure has alt text.
- [ ] Cross-reference check: 3-pass build, no unresolved references, no `??` in indexes or lists.
- [ ] Link check: internal links resolve; external links are DOI/URL-stable or removed.
- [ ] Spelling check: British forms only (`-ise`, `-our`, `programme`, `behavioural`); no US variants
      except inside quoted titles and proper names.
- [ ] Integrity check: no unlabelled hypothetical; no unlabelled AI image; spot-verify a random
      sample of 10 citations against the named editions.

Human sign-off (recorded in the build's `PLAN.md`): academic reviewer, copy-editor, accessibility
reviewer, registrar's office (curriculum accuracy), publisher.

## 10. Front and back matter (fixed order)

Half title · title · copyright (with the §7 notices) · dedication · **How to use this handbook**
(addressed separately to student, seminar leader, supervisor, examiner) · contents · list of figures ·
list of tables · list of abbreviations · programme overview (years, units, progression, assessment
framework) · **main matter: one part per year, one chapter per course, lecture units inside** ·
appendices (genogram notation, comparative grids, assessment criteria, study pathway, academic
calendar, technical requirements for online study, accessibility statement) · bibliography · indexes
(subject, names, instruments) · errata · colophon.

## 11. Decisions recorded for this handbook

| Decision | Recorded value |
|---|---|
| **Programme** | Master in Children and Adolescent Counseling (**CAC**) — not the MFT doctoral text |
| **Source of truth** | `cac/CURRICULUM.md`, `cac/courses.csv` (31 course entries, 1.6 units each, 49.6 units total) |
| **Scope** | **Full curriculum**, published as **one volume per course** (31 volumes), each a complete lecture course for a sixteen-week semester |
| **Trim** | **6 × 9 in** reading edition; reuses the house Typst template family |
| **Citation style** | **APA 7th edition** — field norm for counselling psychology. Governs in-text citations, the reference list, and DOI/URL form. Where an existing house bibliography is imported it is restyled, not mixed. |
| **Licensing** | **All rights reserved**, with the brief-quotation exception; the five copyright notices of §7 apply |
| **Publisher line** | TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA · First Edition 2026 |
| **Structure** | One **part per semester**; one **chapter per course**; **lecture units** inside each chapter following the fifteen-part grammar of §2 |

### APA 7th — handbook-specific rulings

- In-text: author–date, `(Ainsworth, 1978)`; three or more authors shortened from first citation
  `(Minuchin et al., 1967)`; direct quotations carry a page or paragraph locator.
- Reference list: hanging indent, alphabetical by first author surname, DOIs as `https://doi.org/…`,
  no "Retrieved from" unless the source is designed to change.
- The handbook prints **only works actually cited**; no padding bibliography. Every entry is verified
  against a real edition (§6).
- Standardised instruments are cited to their publisher and their copyright status noted; they are
  described, not reproduced.
- APA spelling is American, but §3 fixes **British spelling for the handbook's own prose**. Quoted
  titles, journal names and direct quotations keep their original American spelling. This ruling is
  deliberate and is stated in the "How to use this handbook" matter so it is not read as
  inconsistency.

## 12. Subject-specific layer — counselling minors

The CAC programme teaches practice with children and adolescents. That imports obligations the MFT
and law volumes do not carry, and the handbook must state them on its face rather than in a footnote.

- **Safeguarding is a first-class structural element.** A dedicated `safeguard` callout is added to
  the house callout set. It carries: the risk to recognise, the immediate action, the reporting
  route, and the record to keep. Every lecture unit touching abuse, neglect, self-harm, risk to
  others, or disclosure carries one.
- **Mandated reporting.** The handbook teaches the *structure* of mandated reporting — duty, trigger,
  timeframe, immunity, record — and states plainly that the operative duty is that of the
  **jurisdiction in which the student practises**, which must be checked locally. No jurisdiction's
  timeframes are asserted as universal.
- **Consent, assent and confidentiality with minors.** Parental/guardian consent versus the child's
  assent; the limits of confidentiality and how those limits are disclosed *to the child* in
  age-appropriate language; records, custody disputes, and subpoenas.
- **School settings.** Dual relationships, employee versus clinician role conflict, teacher referrals,
  and the boundary between educational support and therapy (relevant to CAC. 713, 718, 719).
- **Competence limits.** Assessment and diagnosis are taught as requiring supervised practice and
  licensure; the handbook confers no authority to diagnose (the §7 academic and professional notices).
- **Vignettes involving minors** are fictitious composites, labelled at the point of use, with ages
  and identifying detail altered; no real client material, ever.
- **Online delivery.** Telehealth with minors adds guardian consent, location-of-child verification,
  and an emergency-contact plan; these appear in the relevant units and in the technical requirements
  appendix.
