"""The house slide grammar.

Every deck in the collection is composed from these movements:

  cover · contents · divider · outcomes · arc · concepts · lecture ×3
  figure · vignette · skills · seminar · assignment · readings
  synthesis · next week · colophon

The compositions are content-agnostic: they take a ``Week`` object and lay it
out.  That is what keeps 26 courses visibly part of one imprint.
"""
from __future__ import annotations

from pathlib import Path

from . import layout as L
from . import theme
from .theme import Course

P = theme
NUMERALS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
WORDS = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT",
         "NINE", "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN",
         "FIFTEEN", "SIXTEEN"]


def word(n: int) -> str:
    return WORDS[n - 1] if 1 <= n <= len(WORDS) else str(n)


def _fmt(n: int) -> str:
    return f"{n:02d}"


def _kicker(s: L.Slide, text: str, y: float = 78, x: float | None = None,
            color: str | None = None, w: float = 620):
    s.text(x if x is not None else P.M, y, w, text, size=7.4, weight="semibold",
           color=color or P.GOLD, tracking=2.1, upper=True, leading=1.2)


def _title(s: L.Slide, text: str, y: float = 96, size: float = 30,
           width: float = 824, color: str | None = None, leading: float = 1.08):
    return s.text(P.M, y, width, text, family="display", weight="medium",
                  size=size, color=color or P.INK, leading=leading)


def content_slide(deck, course: Course, week, kicker: str, title: str,
                  standfirst: str | None = None, folio: str = "") -> L.Slide:
    """A content slide in the course frame.

    ``_body_top`` is the first y at which the body of the slide may start; it
    clears the longest possible two-line title + standfirst.
    """
    s = deck.slide()
    s.header(course, f"WEEK {_fmt(week.n)}")
    _kicker(s, kicker)
    h = _title(s, title)
    y = 96 + h + 8
    if standfirst:
        y += s.text(P.M, y, 760, standfirst, size=10.6, weight="light",
                    color=P.MUTED, leading=1.5) + 4
    s.footer(course, folio)
    s._body_top = 150 if not standfirst else max(150, y + 10)
    return s


def _vcenter(block_h: float, top: float, bottom: float) -> float:
    return top + max(0.0, (bottom - top - block_h) / 2)


# --------------------------------------------------------------------------
# 1. Course cover
# --------------------------------------------------------------------------
def course_cover(deck, course: Course, total_weeks: int) -> L.Slide:
    pal = course.palette
    s = deck.dark_slide(kind="cover")
    s.rect(24, 24, P.W - 48, P.H - 48, fill=None, line=pal.gold, lw=0.5, alpha=0.55)
    s.rect(34, 34, P.W - 68, P.H - 68, fill=None, line=pal.gold, lw=0.3, alpha=0.22)

    s.text(P.M, 66, 470, course.programme.upper(), size=7.2, weight="semibold",
           color=pal.gold, tracking=2.2, leading=1.2)
    s.text(P.W - P.M - 240, 66, 240, f"{course.semester.upper()}  ·  {course.year}",
           size=7.2, weight="semibold", color=pal.dark_muted, tracking=1.8,
           align="right", leading=1.2)

    s.text(P.M, 132, 300, course.code, family="display", weight="regular",
           size=58, color=pal.gold, leading=1.0)
    s.hline(P.M, 210, 120, pal.gold, 1.0)
    s.text(P.M, 232, 560, course.title, family="display", weight="medium",
           size=42, color=pal.dark_text, leading=1.08)
    s.text(P.M, 372, 520, f"A {total_weeks}-week lecture series in theory, practice "
           "and professional formation.", size=11.0, weight="light",
           color=pal.dark_muted, leading=1.55)

    n = total_weeks
    x0, x1, y = 660, 892, 296
    step = (x1 - x0) / max(1, n - 1)
    s.hline(x0, y, x1 - x0, pal.gold, 0.4, dash=True)
    for i in range(n):
        s.ellipse(x0 + i * step - 1.5, y - 1.5, 3.0, 3.0, fill=pal.gold, alpha=0.8)
        s.text(x0 + i * step - 6, y + 10, 12, _fmt(i + 1), size=5.6,
               weight="semibold", color=pal.dark_muted, align="center", leading=1.2)
    s.text(x0 - 12, y + 28, 244, f"{total_weeks} SEMINARS  ·  15 SLIDES EACH",
           size=6.4, weight="semibold", color=pal.dark_muted, tracking=1.3,
           align="right", leading=1.2)

    s.hline(P.M, 470, P.W - 2 * P.M, pal.gold, 0.4)
    s.text(P.M, 484, 520, "Lectures  ·  Diagrams  ·  Case vignettes  ·  Skills laboratories",
           size=8.2, color=pal.dark_muted, leading=1.3)
    s.text(P.W - P.M - 240, 486, 240, f"{course.units} UNITS  ·  {course.code}",
           size=7.0, weight="semibold", color=pal.gold, tracking=1.6,
           align="right", leading=1.2)
    s.notes = (f"Course cover. {course.code}, {course.title}. {course.semester}, "
               f"{total_weeks} weeks, {course.units} units as listed in the curriculum.")
    return s


# --------------------------------------------------------------------------
# 2. Contents
# --------------------------------------------------------------------------
def contents(deck, course: Course) -> L.Slide:
    pal = course.palette
    s = deck.slide()
    s.header(course, "CONTENTS")
    _kicker(s, "THE COURSE IN SIXTEEN MOVEMENTS", 78)
    _title(s, "Contents", 96, size=32)
    s.footer(course, "ii")

    weeks = course.syllabus
    for i, w in enumerate(weeks[:8]):
        _contents_row(s, pal, w, P.M, 164 + i * 40, 372)
    for i, w in enumerate(weeks[8:]):
        _contents_row(s, pal, w, P.M + 428, 164 + i * 40, 372)
    return s


def _contents_row(s, pal, w, x, y, width):
    s.text(x, y + 2, 26, _fmt(w.n), size=7.6, weight="semibold", color=pal.gold,
           tracking=1.1, leading=1.3)
    s.text(x + 28, y, width - 28, w.title, family="display", weight="regular",
           size=11.4, color=pal.ink, leading=1.2)
    s.hline(x, y + 29, width, pal.hair, 0.4)


# --------------------------------------------------------------------------
# 3. Week divider
# --------------------------------------------------------------------------
def divider(deck, course: Course, week) -> L.Slide:
    pal = course.palette
    s = deck.dark_slide(kind="divider",
                        notes=f"Week {week.n}: {week.title}.\n\n{week.standfirst}")
    s.rect(24, 24, P.W - 48, P.H - 48, fill=None, line=pal.gold, lw=0.45, alpha=0.42)

    s.text(560, 92, 348, _fmt(week.n), family="display", weight="regular",
           size=228, color=pal.dark_text, alpha=0.06, align="right", leading=1.0)

    s.text(P.M, 58, 520, f"{course.code}  ·  {course.semester.upper()}  ·  {course.year}",
           size=7.4, weight="semibold", color=pal.gold, tracking=2.3, leading=1.2)
    s.text(P.W - P.M - 220, 58, 220, f"{_fmt(week.n)} / {course.total:02d}",
           size=7.4, weight="semibold", color=pal.dark_muted, tracking=2.0,
           align="right", leading=1.2)

    s.text(P.M, 166, 420, f"WEEK {word(week.n)}", size=8.2, weight="semibold",
           color=pal.gold, tracking=3.0, leading=1.2)
    s.hline(P.M, 188, 84, pal.gold, 0.8)
    th = s.text(P.M, 212, 620, week.title, family="display", weight="medium",
                size=47, color=pal.dark_text, leading=1.05)
    s.text(P.M, 212 + th + 16, 540, week.standfirst, size=11.4, weight="light",
           color=pal.dark_muted, leading=1.55)

    ey = 408
    s.hline(P.M, ey, 40, pal.gold, 0.6)
    eh = s.text(P.M, ey + 12, 520, f"\u201c{week.epigraph}\u201d", family="display",
                italic=True, weight="regular", size=14.0, color=pal.dark_text,
                leading=1.42, alpha=0.94)
    s.text(P.M, ey + 20 + eh, 520, week.epigraph_src.upper(), size=6.7,
           weight="semibold", color=pal.gold, tracking=1.7, leading=1.2)

    kw = "   ·   ".join(k.upper() for k in week.keywords)
    s.text(P.M, 502, 540, kw, size=6.8, weight="semibold", color=pal.dark_muted,
           tracking=1.4, leading=1.2)
    s.text(P.W - P.M - 240, 502, 240, "15 SLIDES  ·  90 MINUTES", size=6.8,
           weight="semibold", color=pal.dark_muted, tracking=1.4, align="right",
           leading=1.2)
    return s


# --------------------------------------------------------------------------
# 4. Learning outcomes
# --------------------------------------------------------------------------
def outcomes(deck, course: Course, week, folio: str) -> L.Slide:
    pal = course.palette
    s = content_slide(deck, course, week, "LEARNING OUTCOMES",
                      "By the end of this week", None, folio)
    s.text(P.M, 156, 150, _fmt(week.n), family="display", weight="regular",
           size=62, color=pal.accent, alpha=0.22, leading=1.0)
    s.text(P.M, 230, 130, "SESSION\nOBJECTIVES", size=7.2, weight="semibold",
           color=pal.gold, tracking=1.8, leading=1.4)

    items = [s.text_block(262, 0, 600, o, family="display", weight="regular",
                          size=13.2, color=P.INK, leading=1.32)
             for o in week.outcomes]
    heights = [it.height for it in items]
    gap = max(14.0, min(36.0, (452 - 158 - sum(heights)) / max(1, len(items) - 1)))
    y = 158
    for i, (it, h) in enumerate(zip(items, heights)):
        s.hline(226, y, 634, pal.hair, 0.5)
        s.text(226, y + 13, 30, f"{i + 1:02d}", size=8.0, weight="semibold",
               color=pal.gold, tracking=1.0, leading=1.2)
        s.add(type(it)(**{**it.__dict__, "y": y + 11}))
        y += h + 22 + gap - 14
    s.hline(226, min(y, 470), 634, pal.hair, 0.5)
    s.notes = ("Read the outcomes aloud and connect each to the assessment. "
               "They are written as observable capabilities, not topics.")
    return s


# --------------------------------------------------------------------------
# 5. Course arc
# --------------------------------------------------------------------------
def arc(deck, course: Course, week, folio: str) -> L.Slide:
    pal = course.palette
    s = content_slide(deck, course, week, "WHERE THIS WEEK SITS",
                      "The course as a single argument", None, folio)
    s.text(P.M, 146, 700, "Each week is a movement in one continuous argument: "
           "that persons are intelligible only within the relations that form them.",
           size=10.4, weight="light", color=P.MUTED, leading=1.5)

    weeks = course.syllabus
    cols, cw, gap = 8, 94, 8
    x0, y0 = P.M, 200
    for row in range(2):
        for c in range(cols):
            i = row * cols + c
            if i >= len(weeks):
                break
            w = weeks[i]
            x = x0 + c * (cw + gap)
            y = y0 + row * 118
            current, past = w.n == week.n, w.n < week.n
            if current:
                s.rect(x, y, cw, 96, fill=pal.accent, radius=2)
                num_col, t_col = pal.gold_light, pal.paper
            else:
                s.rect(x, y, cw, 96, fill=pal.paper_alt if past else None,
                       line=None if past else pal.hair, lw=0.4, radius=2)
                num_col = pal.gold if not past else pal.muted
                t_col = pal.ink if past else pal.muted
            s.text(x + 9, y + 9, cw - 18, _fmt(w.n), size=6.8, weight="semibold",
                   color=num_col, tracking=1.1, leading=1.2)
            s.text(x + 9, y + 24, cw - 16, w.short, family="display",
                   weight="medium", size=10.0, color=t_col, leading=1.12)
            if current:
                s.text(x + 9, y + 74, cw - 16, "THIS WEEK", size=5.6,
                       weight="semibold", color=pal.gold_light, tracking=1.2,
                       leading=1.2)


    s.hline(P.M, 442, P.CONTENT_W, pal.hair, 0.5)
    s.text(P.M, 452, 420, "Completed   ·   This week   ·   Ahead", size=6.9,
           weight="semibold", color=pal.muted, tracking=1.6, leading=1.2)
    s.text(P.W - P.M - 380, 452, 380,
           f"{len([w for w in weeks if w.n < week.n])} of {course.total} completed before this session",
           size=6.9, weight="semibold", color=pal.gold, tracking=1.2,
           align="right", leading=1.2)
    s.notes = ("Orient the class: name the argument of the course and locate "
               "today's movement within it.")
    return s


# --------------------------------------------------------------------------
# 6. Key concepts
# --------------------------------------------------------------------------
def concepts(deck, course: Course, week, folio: str) -> L.Slide:
    pal = course.palette
    s = content_slide(deck, course, week, "KEY CONCEPTS",
                      "Four ideas to carry into the seminar", None, folio)
    items = []
    for c in week.concepts:
        term, definition = c[0], c[1]
        illustration = c[2] if len(c) > 2 else ""
        items.append((term, definition, illustration))

    n = len(items)
    gap = 16
    cw = (P.CONTENT_W - gap * (n - 1)) / n
    cards = []
    for term, definition, illustration in items:
        t_op = s.text_block(0, 0, cw - 30, term, family="display", weight="medium",
                            size=17.0, color=pal.ink, leading=1.1)
        d_op = s.text_block(0, 0, cw - 30, definition, size=10.3, weight="light",
                            color=P.INK_SOFT, leading=1.58)
        i_op = (s.text_block(0, 0, cw - 34, illustration, family="display",
                             italic=True, weight="regular", size=10.1,
                             color=pal.accent_deep, leading=1.46)
                if illustration else None)
        h = 42 + t_op.height + 26 + d_op.height
        if i_op:
            h += 22 + i_op.height
        cards.append((t_op, d_op, i_op, h))

    height = max(c[3] for c in cards) + 34
    top = _vcenter(height, max(150, s._body_top - 6), 476)
    for i, (t_op, d_op, i_op, h) in enumerate(cards):
        x = P.M + i * (cw + gap)
        s.rect(x, top, cw, height, fill=pal.paper_alt, radius=1.5)
        s.rect(x, top, cw, 2.4, fill=pal.accent)
        s.text(x + 15, top + 18, 60, "CONCEPT", size=6.2, weight="semibold",
               color=pal.muted, tracking=1.6, leading=1.2)
        s.text(x + cw - 34, top + 18, 20, f"{i + 1:02d}", size=6.2,
               weight="semibold", color=pal.gold, tracking=1.0, align="right",
               leading=1.2)
        s.add(type(t_op)(**{**t_op.__dict__, "x": x + 15, "y": top + 40}))
        s.hline(x + 15, top + 40 + t_op.height + 13, cw - 30, pal.hair, 0.4)
        dy = top + 40 + t_op.height + 26
        s.add(type(d_op)(**{**d_op.__dict__, "x": x + 15, "y": dy}))
        if i_op is not None:
            iy = dy + d_op.height + 20
            s.hline(x + 15, iy - 6, 22, pal.gold, 0.6)
            s.add(type(i_op)(**{**i_op.__dict__, "x": x + 15, "y": iy}))
    s.notes = ("Introduce the four terms, then ask students to give a clinical "
               "example of each before moving on.")
    return s


# --------------------------------------------------------------------------
# 7. Lecture
# --------------------------------------------------------------------------
def lecture(deck, course: Course, week, lec: dict, index: int, folio: str) -> L.Slide:
    pal = course.palette
    s = content_slide(deck, course, week, lec["kicker"], lec["title"], None, folio)

    x, w = P.M, 500
    avail_top, avail_bottom = 152, 470
    ops = []
    for lead, body in lec["bullets"]:
        lo = s.text_block(x + 30, 0, w - 30, lead, size=11.0, weight="semibold",
                          color=pal.ink, leading=1.3)
        bo = s.text_block(x + 30, 0, w - 30, body, size=10.0, weight="light",
                          color=P.INK_SOFT, leading=1.48)
        ops.append((lo, bo))
    heights = [lo.height + 3 + bo.height for lo, bo in ops]
    n = len(heights)
    gap = 18.0
    if sum(heights) + gap * (n - 1) > avail_bottom - avail_top:
        gap = max(8.0, (avail_bottom - avail_top - sum(heights)) / max(1, n - 1))
    block = sum(heights) + gap * (n - 1)
    y = avail_top + max(0.0, (avail_bottom - avail_top - block) / 2)
    for i, ((lo, bo), h) in enumerate(zip(ops, heights)):
        s.text(x, y - 1, 26, NUMERALS[i], family="display", weight="medium",
               size=11.5, color=pal.gold, leading=1.2)
        s.add(type(lo)(**{**lo.__dict__, "y": y}))
        s.add(type(bo)(**{**bo.__dict__, "y": y + lo.height + 3}))
        y += h + gap

    # side panel: the proposition to hold, then a question for the seminar
    px, pw = 600, 292
    s.text(px, 152, pw, lec.get("panel_title", "CLINICAL IMPLICATION"), size=6.8,
           weight="semibold", color=pal.gold, tracking=1.8, leading=1.2)
    s.hline(px, 168, 38, pal.gold, 0.6)
    q = lec["panel_text"]
    qh = s.text_block(px, 0, pw, q, family="display", italic=True,
                      weight="regular", size=13.2, color=pal.ink,
                      leading=1.44).height
    s.text(px, 182, pw, q, family="display", italic=True, weight="regular",
           size=13.2, color=pal.ink, leading=1.44)

    # hairline separator
    sy = 182 + qh + 30
    s.hline(px, sy, pw, pal.hair, 0.5)

    prompt = week.seminar[min(index - 1, len(week.seminar) - 1)]
    s.text(px, sy + 16, pw, "PUT TO THE ROOM", size=6.8, weight="semibold",
           color=pal.accent, tracking=1.8, leading=1.2)
    s.text(px, sy + 34, pw, prompt, size=10.2, weight="light", color=P.INK_SOFT,
           leading=1.48)
    s.notes = lec.get("notes", f"Lecture {index}. {lec['title']}.")
    return s


# --------------------------------------------------------------------------
# 8. Figure
# --------------------------------------------------------------------------
def figure(deck, course: Course, week, path: Path, folio: str) -> L.Slide:
    pal = course.palette
    fig = week.figure
    s = content_slide(deck, course, week, fig["kicker"], fig["title"], None, folio)
    s.image(path, P.M, 152, w=824)
    s.hline(P.M, 446, 824, pal.hair, 0.5)
    s.text(P.M, 455, 560, fig["caption"], family="display", italic=True,
           size=8.8, color=P.INK_SOFT, leading=1.3)
    s.text(P.W - P.M - 240, 455, 240, fig.get("source", "Prepared for this course."),
           size=6.7, weight="semibold", color=pal.muted, tracking=1.1,
           align="right", leading=1.2)
    s.notes = fig.get("notes", "Walk the diagram slowly; name each element before interpreting it.")
    return s


# --------------------------------------------------------------------------
# 9. Clinical vignette
# --------------------------------------------------------------------------
def vignette(deck, course: Course, week, folio: str) -> L.Slide:
    pal = course.palette
    v = week.vignette
    s = content_slide(deck, course, week, "CLINICAL VIGNETTE", v["title"], None, folio)

    body_h = s.text_block(P.M, 0, 452, v["body"], family="display",
                          weight="regular", size=11.2, color=P.INK_SOFT,
                          leading=1.62).height
    by = _vcenter(body_h, 148, 456)
    s.text(P.M, by, 452, v["body"], family="display", weight="regular",
           size=11.2, color=P.INK_SOFT, leading=1.62)

    # prompt panel, height follows its content
    px, pw = 566, 326
    prompts = v["prompts"]
    ph = 44
    for q in prompts:
        ph += s.text_block(px + 42, 0, pw - 62, q, size=9.8, weight="light",
                           color=P.INK, leading=1.42).height + 18
    ph = min(ph + 18, 330)
    s.rect(px, 156, pw, ph, fill=pal.paper_alt, radius=1.5)
    s.rect(px, 156, pw, 2.4, fill=pal.accent)
    s.text(px + 20, 174, pw - 40, "FOR REFLECTION", size=6.8, weight="semibold",
           color=pal.gold, tracking=1.9, leading=1.2)
    y = 200
    for i, q in enumerate(prompts):
        s.text(px + 20, y, 22, f"{i + 1}", size=8.4, weight="semibold",
               color=pal.accent, leading=1.3)
        h = s.text(px + 42, y - 2, pw - 62, q, size=9.8, weight="light",
                   color=P.INK, leading=1.42)
        y += h + 18

    s.text(P.M, 468, 452, v.get("note", "A fictitious composite; identifying details altered."),
           size=7.2, italic=True, color=pal.muted, leading=1.2)
    s.notes = v.get("notes", "Read the vignette, then hold silence for one minute before taking responses.")
    return s


# --------------------------------------------------------------------------
# 10. Skills laboratory
# --------------------------------------------------------------------------
def skills(deck, course: Course, week, folio: str) -> L.Slide:
    pal = course.palette
    sk = week.skills
    s = content_slide(deck, course, week, "SKILLS LABORATORY", sk["title"], None, folio)
    s.text(P.M, 146, 760, sk["intro"], size=10.4, weight="light", color=P.MUTED,
           leading=1.5)

    n = len(sk["steps"])
    gap = 18
    cw = (P.CONTENT_W - gap * (n - 1)) / n
    top = max(206, s._body_top + 48)
    timing = sk.get("timing") or ["10 min"] * n
    for i, (name, text) in enumerate(sk["steps"]):
        x = P.M + i * (cw + gap)
        s.hline(x, top - 14, cw, pal.hair, 0.5)
        s.text(x, top + 4, 40, f"{i + 1:02d}", family="display", weight="regular",
               size=30, color=pal.accent, alpha=0.6, leading=1.0)
        s.text(x, top + 46, cw, name, size=10.4, weight="semibold",
               color=pal.ink, leading=1.28)
        s.text(x, top + 70, cw, text, size=9.3, weight="light",
               color=P.INK_SOFT, leading=1.45)
        s.text(x, max(352, top + 150), cw, timing[i], size=6.8, weight="semibold",
               color=pal.accent, tracking=1.4, leading=1.2)

    s.hline(P.M, 348, P.CONTENT_W, pal.hair, 0.5)
    s.rect(P.M, 392, P.CONTENT_W, 52, fill=pal.accent_soft, radius=1.5)
    s.text(P.M + 18, 407, 96, "DEBRIEF", size=6.8, weight="semibold",
           color=pal.accent_deep, tracking=1.9, leading=1.2)
    s.text(P.M + 112, 403, P.CONTENT_W - 132, sk["debrief"], size=9.6,
           weight="light", color=P.INK, leading=1.4)
    s.notes = sk.get("notes", "Time the exercise strictly: pairs, ten minutes each, then a full-group debrief.")
    return s


# --------------------------------------------------------------------------
# 11. Seminar questions
# --------------------------------------------------------------------------
def seminar(deck, course: Course, week, folio: str) -> L.Slide:
    pal = course.palette
    s = content_slide(deck, course, week, "SEMINAR", "Questions for discussion",
                      "Choose three. The best questions are the ones the room cannot settle quickly.",
                      folio)
    items = [s.text_block(P.M + 34, 0, 776, q, family="display", weight="regular",
                          size=13.4, color=P.INK, leading=1.3)
             for q in week.seminar]
    heights = [it.height for it in items]
    gap = max(12.0, min(30.0, (462 - 164 - sum(heights)) / max(1, len(items) - 1)))
    y = 164
    for i, (it, h) in enumerate(zip(items, heights)):
        s.hline(P.M, y, P.CONTENT_W, pal.hair, 0.5)
        s.text(P.M, y + 14, 30, f"{i + 1:02d}", size=8.2, weight="semibold",
               color=pal.gold, tracking=1.0, leading=1.2)
        s.add(type(it)(**{**it.__dict__, "y": y + 11}))
        y += h + 26 + gap - 14
    s.hline(P.M, min(y, 470), P.CONTENT_W, pal.hair, 0.5)
    s.notes = "Do not answer these yourself. Ask for a position, then ask what evidence would change it."
    return s


# --------------------------------------------------------------------------
# 12. Assignment
# --------------------------------------------------------------------------
def assignment(deck, course: Course, week, folio: str) -> L.Slide:
    pal = course.palette
    a = week.assignment
    s = content_slide(deck, course, week, "ASSESSMENT", "This week's work", None, folio)

    left_w = 458
    crit = a.get("criteria") or []
    top, bottom = max(178, s._body_top + 28), 424

    # Fit the column: shrink the type and the gap until it sits inside the frame.
    for scale, cgap in ((1.0, 16), (1.0, 12), (0.96, 12), (0.93, 10), (0.90, 10)):
        t_size, b_size, c_size = 20.0 * scale, 10.3 * scale, 9.4 * scale
        title_op = s.text_block(P.M, 0, left_w, a["major_title"], family="display",
                                weight="medium", size=t_size, color=pal.ink, leading=1.18)
        text_op = s.text_block(P.M, 0, left_w, a["major_text"], size=b_size,
                               weight="light", color=P.INK_SOFT, leading=1.52)
        crit_ops = [s.text_block(P.M + 22, 0, left_w - 22, c, size=c_size,
                                 weight="light", color=P.INK_SOFT, leading=1.4)
                    for c in crit]
        crit_h = (sum(o.height for o in crit_ops) + cgap * (len(crit_ops) - 1) + 34
                  if crit_ops else 0)
        left_h = title_op.height + 12 + text_op.height + 12 + 14 + crit_h
        if left_h <= bottom - top:
            break

    ly = _vcenter(left_h, top, bottom)
    s.text(P.M, ly - 24, 160, "MAJOR ASSIGNMENT", size=6.8, weight="semibold",
           color=pal.gold, tracking=1.9, leading=1.2)
    s.add(type(title_op)(**{**title_op.__dict__, "y": ly}))
    ty = ly + title_op.height + 11
    s.add(type(text_op)(**{**text_op.__dict__, "y": ty}))
    s.text(P.M, ty + text_op.height + 12, left_w, a["major_meta"].upper(),
           size=7.0, weight="semibold", color=pal.accent, tracking=1.4, leading=1.2)
    if crit_ops:
        cy = ty + text_op.height + 12 + 16
        s.hline(P.M, cy, left_w, pal.hair, 0.5)
        s.text(P.M, cy + 11, 180, "ASSESSED ON", size=6.5, weight="semibold",
               color=pal.gold, tracking=1.8, leading=1.2)
        cy += 28
        for i, op in enumerate(crit_ops):
            s.text(P.M, cy + 1, 16, f"{i + 1}", size=7.4, weight="semibold",
                   color=pal.accent, leading=1.3)
            s.add(type(op)(**{**op.__dict__, "y": cy - 1}))
            cy += op.height + cgap

    x2 = 596
    fy = max(178, s._body_top + 28)
    s.text(x2, fy, 220, "FORMATIVE WORK", size=6.8, weight="semibold",
           color=pal.gold, tracking=1.9, leading=1.2)
    s.hline(x2, fy + 16, 36, pal.gold, 0.6)
    yy = fy + 32
    for i, t in enumerate(a["tasks"]):
        s.text(x2, yy, 20, f"{i + 1}", size=8.2, weight="semibold",
               color=pal.accent, leading=1.3)
        h = s.text(x2 + 20, yy - 2, 208, t, size=9.5, weight="light",
                   color=P.INK_SOFT, leading=1.44)
        yy += h + 18

    s.rect(P.M, 440, P.CONTENT_W, 44, fill=pal.paper_alt, radius=1.5)
    s.rect(P.M, 440, 2.4, 44, fill=pal.gold)
    s.text(P.M + 20, 451, 70, "NOTE", size=6.6, weight="semibold",
           color=pal.gold, tracking=1.8, leading=1.2)
    s.text(P.M + 84, 449, P.CONTENT_W - 110, a["note"], size=8.8, italic=True,
           color=P.INK_SOFT, leading=1.36)
    s.notes = ("State the submission route and deadline aloud; students consistently "
               "misread the word count as a target rather than a ceiling.")
    return s


# --------------------------------------------------------------------------
# 13. Reading list
# --------------------------------------------------------------------------
def readings(deck, course: Course, week, folio: str) -> L.Slide:
    pal = course.palette
    s = content_slide(deck, course, week, "READING", "Before the next seminar",
                      "Read the core text closely. Skim the rest for argument and method.",
                      folio)
    cols = [week.readings[:3], week.readings[3:6]]
    for ci, col in enumerate(cols):
        x = P.M + ci * 428
        entries = []
        for i, (tag, cite) in enumerate(col):
            entries.append((tag, s.text_block(x, 0, 384, cite, size=9.4,
                                              weight="light", color=P.INK_SOFT,
                                              leading=1.4)))
        heights = [e[1].height for e in entries]
        top, bottom = 158, 456
        gap = max(24.0, min(80.0, (bottom - top - sum(heights)) / max(1, len(entries))))
        y = top
        for (tag, op), h in zip(entries, heights):
            core = tag.upper() == "CORE"
            s.hline(x, y, 384, pal.hair, 0.5)
            s.text(x, y + 12, 384, tag.upper(), size=6.5, weight="semibold",
                   color=pal.accent if core else pal.muted, tracking=1.7, leading=1.2)
            s.add(type(op)(**{**op.__dict__, "y": y + 28}))
            y += h + 34 + gap - 26
        s.hline(x, min(y - gap + 26, bottom), 384, pal.hair, 0.5)
    s.notes = "Name the core reading and the one idea students should extract from it."
    return s


# --------------------------------------------------------------------------
# 14. Synthesis
# --------------------------------------------------------------------------
def synthesis(deck, course: Course, week, folio: str) -> L.Slide:
    pal = course.palette
    s = deck.dark_slide(kind="dark")
    s.text(P.M, 66, 400, "SYNTHESIS", size=7.4, weight="semibold", color=pal.gold,
           tracking=2.4, leading=1.2)
    q = week.synthesis[0]
    lines = L.wrap(f"\u201c{q}\u201d", "display", "regular", True, 30, 700)
    block_h = len(lines) * 30 * 1.28
    y = _vcenter(block_h, 120, 420)
    s.text(130, y, 700, f"\u201c{q}\u201d", family="display", italic=True,
           weight="regular", size=30, color=pal.dark_text, leading=1.28,
           align="center")
    s.hline(430, y + block_h + 26, 100, pal.gold, 0.8)
    s.text(330, y + block_h + 44, 300, week.synthesis[1].upper(), size=7.1,
           weight="semibold", color=pal.gold, tracking=2.0, align="center",
           leading=1.2)
    s.text(P.M, 502, 400, f"{course.code}  ·  WEEK {_fmt(week.n)}", size=6.7,
           weight="semibold", color=pal.dark_muted, tracking=1.6, leading=1.2)
    s.notes = "Close on the sentence, not on a summary. Let it sit."
    return s


# --------------------------------------------------------------------------
# 15. Next week
# --------------------------------------------------------------------------
def next_week(deck, course: Course, week, folio: str) -> L.Slide:
    pal = course.palette
    nxt = week.next
    s = deck.dark_slide(kind="dark")
    s.rect(24, 24, P.W - 48, P.H - 48, fill=None, line=pal.gold, lw=0.4, alpha=0.35)
    s.text(P.M, 60, 500, "NEXT WEEK" if nxt.get("n") else "AFTER THE COURSE",
           size=7.6, weight="semibold", color=pal.gold, tracking=2.6, leading=1.2)
    if nxt.get("n"):
        s.text(P.W - P.M - 200, 58, 200, f"{_fmt(nxt['n'])} / {course.total:02d}",
               size=7.2, weight="semibold", color=pal.dark_muted, tracking=1.8,
               align="right", leading=1.2)
    s.hline(P.M, 86, 96, pal.gold, 0.8)
    s.text(P.M, 112, 680, nxt["title"], family="display", weight="medium",
           size=38, color=pal.dark_text, leading=1.08)

    items = [s.text_block(P.M + 26, 0, 520, pre, size=11.0, weight="light",
                          color=pal.dark_muted, leading=1.5)
             for pre in nxt["preview"]]
    total_h = sum(it.height for it in items) + 18 * (len(items) - 1)
    y = _vcenter(total_h, 196, 330)
    for it in items:
        s.text(P.M, y + 1, 20, "—", size=10, color=pal.gold, leading=1.4)
        s.add(type(it)(**{**it.__dict__, "y": y - 2}))
        y += it.height + 18
    if nxt.get("n"):
        s.hline(P.M, 404, P.CONTENT_W, pal.gold, 0.4, dash=True)
        prep = [("READ", nxt.get("read", "The core reading for the session.")),
                ("ANNOTATE", nxt.get("annotate", "One passage that troubles you.")),
                ("BRING", nxt.get("bring", "One question for the seminar."))]
        colw = P.CONTENT_W / 3
        for i, (label, text) in enumerate(prep):
            x = P.M + i * colw
            s.text(x, 420, 70, label, size=6.6, weight="semibold", color=pal.gold,
                   tracking=1.9, leading=1.2)
            s.text(x, 438, colw - 30, text, size=9.4, weight="light",
                   color=pal.dark_muted, leading=1.4)
    else:
        s.hline(P.M, 396, 150, pal.gold, 0.6)
        s.text(P.M, 408, 620, "Continue in supervision. Keep reading. "
               "Teach what you have learned.", size=10.2, weight="light",
               color=pal.dark_muted, leading=1.45)
    s.text(P.W - P.M - 300, 486, 300, f"{course.code}  ·  {course.title.upper()}",
           size=6.4, weight="semibold", color=pal.dark_muted, tracking=1.2,
           align="right", leading=1.25)
    s.notes = "Set the reading before students leave the room."
    return s


# --------------------------------------------------------------------------
# 16. Colophon
# --------------------------------------------------------------------------
def colophon(deck, course: Course) -> L.Slide:
    pal = course.palette
    s = deck.dark_slide(kind="colophon")
    s.rect(24, 24, P.W - 48, P.H - 48, fill=None, line=pal.gold, lw=0.45, alpha=0.45)
    s.text(P.M, 206, 824, "Set in EB Garamond & Source Sans 3", family="display",
           italic=True, size=26, color=pal.dark_text, align="center", leading=1.3)
    s.hline(430, 264, 100, pal.gold, 0.8)
    s.text(P.M, 284, 824, f"{course.programme}  ·  {course.code}  ·  {course.year}",
           size=7.4, weight="semibold", color=pal.gold, tracking=2.0,
           align="center", leading=1.3)
    s.text(P.M, 326, 824, "Lecture decks for a graduate programme in marriage and family therapy.",
           size=9.4, weight="light", color=pal.dark_muted, align="center", leading=1.4)
    return s


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------
def week_slides(deck, course: Course, week, fig_path: Path, *, bound: bool = False):
    total = course.total
    folio = f"{week.n:02d} / {total:02d}"
    divider(deck, course, week)
    outcomes(deck, course, week, folio)
    arc(deck, course, week, folio)
    concepts(deck, course, week, folio)
    lecture(deck, course, week, week.lectures[0], 1, folio)
    lecture(deck, course, week, week.lectures[1], 2, folio)
    figure(deck, course, week, fig_path, folio)
    lecture(deck, course, week, week.lectures[2], 3, folio)
    vignette(deck, course, week, folio)
    skills(deck, course, week, folio)
    seminar(deck, course, week, folio)
    assignment(deck, course, week, folio)
    readings(deck, course, week, folio)
    synthesis(deck, course, week, folio)
    # In the bound edition the next divider follows immediately, so the
    # "next week" slide would repeat its title on the page after.  Keep it
    # only at the end of the course, where it closes the book.
    if not bound or week.n == course.total:
        next_week(deck, course, week, folio)


def week_deck(course: Course, week, fig_path: Path) -> L.Deck:
    deck = L.Deck(course)
    week_slides(deck, course, week, fig_path)
    return deck


def course_deck(course: Course, figs: dict[int, Path]) -> L.Deck:
    deck = L.Deck(course)
    course_cover(deck, course, course.total)
    contents(deck, course)
    for w in course.weeks:
        week_slides(deck, course, w, figs[w.n], bound=True)
    colophon(deck, course)
    return deck
