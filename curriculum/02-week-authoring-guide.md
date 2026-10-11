# Week Authoring Guide

How to write one weekly lecture. Follow this and a week lands on 35:00 without
adjustment. Derived from the two weeks built and measured so far.

---

## 1. The numbers that matter

| Quantity | Target | Why |
|---|---|---|
| **Narration words** | **5,150 – 5,400** | Measured voice pace is 152 wpm. Below ~5,050 the assembler must stretch audio past 0.85× and the build warns; above ~5,450 it must speed up past 1.06× and the build refuses. |
| Slides | 18 – 22 | ~275 words per slide. Fewer slides means longer stretches on one image. |
| Spoken time | 2,032 – 2,130 s | The budget is 2,100 s minus per-slide padding. |
| Implied tempo | 0.98 – 1.01 | Anything outside this means the narration needs editing, not the settings. |

Check before voicing:

```bash
python3 tools/build_lecture.py check content/cpy-701/week-NN.json
```

The `est` figure it prints is speech only. Add ~2.3 s per slide for padding to
get the projected video length.

---

## 2. Narrative arc

Every week follows the same five-part shape. This is what makes 35 minutes feel
like a lecture rather than a list.

| Slides | Part | Job |
|---|---|---|
| 1–2 | **Opening** | Title, then objectives. State the single claim the lecture argues for. |
| 3–7 | **Part One — the problem** | Define the thing, show why it matters, correct the common misunderstanding. |
| 8–12 | **Part Two — the substance** | The main body. History, mechanisms, classification, or method. |
| 13–17 | **Part Three — the evidence and the application** | What the research actually shows, then a case applying it. |
| 18–20 | **Close** | Takeaways, reading list with a journal prompt, end slide pointing to next week. |

Rules that came out of Weeks 1 and 2:

- **One argument per lecture.** Week 1 argued that counseling psychology is
  defined by functioning, strengths and context rather than by symptoms. Week 2
  argued that traditions differ in their assumptions, not their techniques. State
  the argument on slide 1 and return to it in the takeaways.
- **Name the uncertainty.** Every week includes at least one limitation, and one
  place where the evidence is weaker than the field implies. This is a
  scientist-practitioner programme; it should sound like one.
- **One case, applied from several angles.** Weeks 1 and 2 both end the body with
  a vignette. The case is where the abstractions become professional judgement.
- **Do not speak the lecturer or institution name in the narration.** Only slide 1
  shows it. This means a rebrand never invalidates recorded audio — confirmed when
  Week 1 was rebranded and no re-recording was needed.

---

## 3. Vocabulary for the narration

Write for the ear, not the eye.

| Do | Don't |
|---|---|
| Spell dates as words: "nineteen forty two" | "1942" |
| Spell numbers that carry emphasis: "eighty five per cent" | "85%" |
| Short sentences. One idea each. | Long subordinate clauses |
| "Notice what this means for your training." | "It is important to note that..." |
| Direct address: "I want you to be able to..." | Passive: "It should be understood that..." |
| Signal structure: "First... Second... Third..." | Unmarked lists |

Numbers in the form "0.7 standard deviations" should be written out as words
("zero point seven standard deviations") or rephrased, because the speech engine
reads bare numerals inconsistently.

**Avoid clinical detail in the narration that a content filter may decline.**
One Week 1 line describing a client's panic presentation was declined and had to
be rephrased to "a client you are treating for anxiety". Prefer general clinical
language in narration; put specific detail on the slide, where it is safe.

---

## 4. Slide layout reference

15 layouts. Each takes the keys listed; all accept `narration`, `pad_lead`,
`pad_tail`, and auto-get footers.

| Layout | Required keys | Use for |
|---|---|---|
| `title` | `title` | Slide 1 only |
| `section` | `number`, `title` | Part dividers. `number` renders as a right-side watermark. |
| `objectives` | `title`, `items[]` | Tick-box list. Slide 2. |
| `bullets` | `title`, `bullets[]` | Main content. Items are strings or `{t, lvl, strong, sub}`. |
| `twocol` | `title`, `columns[{h, items[]}]` | Comparisons. Exactly two columns. |
| `definition` | `title`, `term`, `body` | Key concepts. Optional `source`, `footnote`. |
| `table` | `title`, `columns[]`, `rows[][]` | Optional `widths[]` must sum to 1.0. |
| `stats` | `title`, `stats[{v, l}]` | 3–4 large figures. Optional `note`. |
| `process` | `title`, `steps[{h, b}]` | Sequenced stages. 4–6 steps. |
| `quote` | `quote`, `attribution` | One quotation, set large. |
| `casestudy` | `title`, `paragraphs[]` | Optional `questions[]` in gold. |
| `takeaways` | `title`, `items[]` | 4–6 items. Measured and centred. |
| `reading` | `title`, `items[]` | Items are strings or `{t, italic}`. |
| `end` | `title` | Optional `body`, `next[]`. Last slide. |

Slide-level extras: `"alt": true` for an off-white background, `pad_lead` and
`pad_tail` to override the 0.7 s / 1.6 s defaults.

---

## 5. Build sequence

```bash
# 1. write the lecture JSON, then sanity-check the word count
python3 tools/build_lecture.py check content/cpy-701/week-03.json

# 2. render slides, PPTX and the contact sheet for visual review
python3 tools/build_lecture.py slides content/cpy-701/week-03.json

# 3. split narration into speech calls under the 1,500-character limit
python3 tools/narrate.py plan content/cpy-701/week-03.json
python3 tools/narrate.py status content/cpy-701/week-03.json   # what is missing

# 4. voice each call, then merge chunks into one file per slide
python3 tools/narrate.py merge content/cpy-701/week-03.json

# 5. assemble. Lands on target_minutes automatically.
python3 tools/build_lecture.py assemble content/cpy-701/week-03.json

# 6. if narration text changed after encoding, refresh captions in seconds
python3 tools/build_lecture.py sidecars content/cpy-701/week-03.json

# 7. reclaim space
python3 tools/clean.py --work
```

---

## 6. Voice capacity

Speech generation is limited to **10 clips per turn**. A 35-minute week needs
**30–34 clips**, so **one week takes 3–4 turns of voicing**. Plan for it rather
than discovering it mid-week. If narration is shorter per slide the count drops;
splitting a slide's narration into more, shorter chunks does not help, because
the per-call character limit is what governs.

For the full 448-video series this is the binding constraint, which is why the
recording-script route exists: `tools/script_export.py` produces a presenter
script that can be voiced in bulk outside this pipeline.

---

## 7. Validation before shipping a week

1. `ffmpeg -v error -i <slug>.mp4 -f null -` — must print nothing.
2. Duration reported by the build must equal `target_minutes × 60`.
3. Sample a frame at each cue midpoint and confirm it matches its own slide.
   Reusable check: see section 7c of the production plan.
4. Confirm audio peaks below 0 dBFS (`volumedetect`).
5. Confirm the contact sheet has the right number of slides and no blank frames.
