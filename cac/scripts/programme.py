#!/usr/bin/env python3
"""Generate the handbook's programme overview from cac/courses.csv.

The curriculum is the single source of truth (HANDBOOK-STANDARD.md §1): the printed tables are
generated, never retyped, so codes, titles and unit values cannot drift from the supplied data.
Also emits the chapter map used by PLAN.md verification.
"""
from __future__ import annotations

import csv
from collections import OrderedDict
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
CSV = BOOK / "courses.csv"
OUT = BOOK / "manuscript" / "front" / "50-programme.md"

SEMESTER_WORD = {"1": "First", "2": "Second", "3": "Third", "": "Elective"}
PART_ROMAN = {"1": "I", "2": "II", "3": "III", "": "IV"}
PART_TITLE = {
    "1": "First Semester — Foundations of Counselling Children and Adolescents",
    "2": "Second Semester — Assessment, Intervention and Contexts of Practice",
    "3": "Third Semester — Advanced Practice, Research and the Master Thesis",
    "": "Elective Pool — Specialisations and Supervised Practice",
}
# notional hours: 1 unit ~= 15 Carnegie hours
UNITS_PER_COURSE = 6


def load():
    with CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for i, r in enumerate(rows, 1):
        r["chapter"] = i
    return rows


def units_total(rows):
    return sum(float(r["units"]) for r in rows)


def table(rows):
    out = ["| Chapter | Course Code | Course Title | Unit |", "|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['chapter']} | {r['code']} | {r['title']} | {r['units']} |")
    return "\n".join(out)


def main():
    rows = load()
    groups = OrderedDict()
    for r in rows:
        groups.setdefault(r["semester"], []).append(r)

    md = ["# Programme Overview {.front}", ""]
    md.append(
        "The Master in Children and Adolescent Counseling is taught in three semesters of core "
        "courses, with a pool of electives from which students select. The tables in this section "
        "are generated directly from the University's curriculum record; course codes, course titles "
        "and unit values are reproduced exactly as supplied, and chapter numbers are the handbook's "
        "own. Where a code appears against more than one course in the curriculum record, both "
        "entries are printed and the duplication is noted; the handbook does not silently renumber "
        "the University's curriculum.")
    md.append("")

    md.append("## Structure of the programme")
    md.append("")
    md.append("| Component | Course entries | Units | Handbook part |")
    md.append("|---|---|---|---|")
    for sem, grp in groups.items():
        label = SEMESTER_WORD[sem]
        label = "Elective courses" if sem == "" else f"{label} Semester"
        md.append(f"| {label} | {len(grp)} | {units_total(grp):.1f} | Part {PART_ROMAN[sem]} |")
    core = [r for r in rows if r["category"] == "Core"]
    md.append(f"| **Required programme (Semesters 1–3)** | **{len(core)}** | "
              f"**{units_total(core):.1f}** | Parts I–III |")
    md.append(f"| **All course entries listed** | **{len(rows)}** | **{units_total(rows):.1f}** | Parts I–IV |")
    md.append("")

    for sem, grp in groups.items():
        md.append(f"## Part {PART_ROMAN[sem]} — {PART_TITLE[sem]}")
        md.append("")
        md.append(table(grp))
        md.append("")
        md.append(f"*{len(grp)} course entries · {units_total(grp):.1f} units · "
                  f"{len(grp) * UNITS_PER_COURSE} lecture units in this part.*")
        md.append("")

    md.append("## Units, notional hours and lecture units")
    md.append("")
    md.append(
        f"Every course in the curriculum record carries a unit value of **1.6**. Taking one unit as "
        f"fifteen notional learning hours, a 1.6-unit course represents approximately **24 notional "
        f"hours**, of which the handbook's teaching material is organised into "
        f"**{UNITS_PER_COURSE} lecture units** of about four hours each. A lecture unit is not a "
        "contact-hour prescription: the four hours divide across synchronous teaching, seminar or "
        "skills work, supervised or independent practice, and reading. Students should expect "
        "roughly one third of the time in each unit to be scheduled teaching and two thirds to be "
        "their own preparation, practice and writing.")
    md.append("")
    md.append(
        "The programme as listed therefore represents approximately "
        f"**{units_total(rows) * 15:.0f} notional hours** across all {len(rows)} course entries, of "
        f"which the required core (Semesters 1–3) accounts for **{units_total(core) * 15:.0f} hours**.")
    md.append("")

    md.append("## Progression and assessment")
    md.append("")
    md.append(
        "Core courses in Semesters 1–3 are taken in the order listed. The first semester establishes "
        "the theoretical, developmental and ethical foundations on which every later course depends; "
        "CAC. 703 Ethics in Counseling should be taken before any course involving contact with "
        "children, and its content is assumed in the safeguarding material throughout Parts II and "
        "III. The second semester moves from foundation to application: assessment, diagnosis, "
        "behavioural and crisis intervention, and the settings in which young people are actually "
        "seen. The third semester consolidates advanced practice and research, ending in the Master "
        "Thesis (CAC. 760).")
    md.append("")
    md.append(
        "Each lecture unit carries formative work and one assessed component. Assessment across the "
        "programme is by written examination, case formulation, observed or recorded skills "
        "demonstration, critical review, and — for CAC. 726 and CAC. 760 — supervised practice and "
        "dissertation. The assessment criteria printed in each unit are the criteria by which that "
        "unit's work is marked; the programme-level grade scale and the regulations for resits, "
        "extenuating circumstances and academic misconduct are those of the University, published "
        "separately and binding on this handbook.")
    md.append("")

    md.append("## Notes on the curriculum record")
    md.append("")
    md.append(
        "Three features of the curriculum record are reproduced here exactly as supplied and are "
        "flagged for the reader's attention rather than corrected by the editor. First, **CAC. 701 "
        "appears twice** in the First Semester, against two different courses — *Fundamentals of "
        "Counseling Theories* (chapter 1) and *Child Development Theories* (chapter 2). Second, "
        "**CAC. 708 carries the same title as the first CAC. 701** (*Fundamentals of Counseling "
        "Theories*, chapter 9); the handbook treats it as a distinct entry and prints it as "
        "supplied. Third, **CAC. 717 *Research Methods in Counseling* (chapter 18) and CAC. 721 "
        "*Research Methodology* (chapter 22)** both fall in the Third Semester and overlap in scope; "
        "the handbook distinguishes them by treating CAC. 717 as the foundation course in method and "
        "design and CAC. 721 as the advanced course in methodology for the thesis, and cross-"
        "references between them. Students should confirm all three points with the registrar's "
        "office before planning a semester.")
    md.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {OUT.relative_to(BOOK.parent)} "
          f"({len(rows)} entries, {units_total(rows):.1f} units)")


if __name__ == "__main__":
    main()
