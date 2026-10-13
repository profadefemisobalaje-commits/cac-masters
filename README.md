# CAC Masters — Professional Video Lecture Library

**Triune Biblical University · Global Extension USA**
**Programme:** Master in Children and Adolescent Counseling (100% Online)
**Format:** Professionally designed 720p video lectures · unique design template per course · voice narration

This repository contains a complete, production-ready **Lecture Studio** that designs, scripts, narrates,
and renders a super-luxurious presentation-styled video lecture for **every course subject** in the
Master in Children and Adolescent Counseling programme, respecting each subject's recommended video hours.

## What is here

- `studio/data/subjects/*.json` — full curriculum records for **all 31 subjects**
  (First Semester, Second Semester, Third Semester, and all 8 Electives): code, title, semester,
  recommended video hours, units, tagline, case vignette, description, guiding questions, learning
  outcomes, module-by-module hour allocation, practicum, assessment, study habits, faith integration,
  and a **unique visual style** (layout, motif, palette).
- `studio/engine/` — the rendering + narration + assembly engine:
  - `render_core.py` — premium typography (Playfair Display, Cinzel, Montserrat), vector motifs, gradients.
  - `slides.py` — the slide layout system (title, agenda, outcomes, modules, roadmap, closing, credits…).
  - `compose.py` — the narration composer: turns each curriculum record into a ~22–30 min lecture script.
  - `assemble.py` — renders slides, times them to narration, adds crossfades, encodes sharp 720p MP4.
- `studio/bin/` — runners:
  - `make_all_decks.py` — render every subject's deck, poster, and TTS clip manifest.
  - `render_course.py <subject.json>` — assemble one full video lecture.
  - `make_gallery.py` — build the browseable library site.
- `out/` — generated artifacts (not snapshotted): `videos/`, `posters/`, `scripts/`, `index.html`.

## The design system

Every subject receives a **distinct template**: its own palette, layout (hero / band / split / card),
and vector motif (laurel, growth curve, scales, bridge, circles, rings, puzzle, beacon, globe, lens,
steps, lamp, wave, heart, lotus, quill, compass, sprout, brain, network, circuit, badge, shield,
infinity, gavel, seal…). Slides render at 1920×1080 and downscale to a crisp **1280×720**.

## Video hours

Each subject's narration and module map carry its recommended hours (e.g. CAC.704 = 24h, CAC.707 = 24h,
CAC.760 = 12h). The full planned library sums to **608 hours** as supplied. The orientation video for each
subject states its hours, units, and module-hour allocation.

## Narration

Narration is generated with Arena's speech engine (two registered narrators: a feminine lead for
Semesters 1 & 3 and a masculine lead for Semester 2 & Electives). The speech engine enforces a
**session quota (~10 clips)**. Because of that quota, narration is produced in batches across sessions.
Each subject's exact narration text is saved in `out/scripts/<course>_clips.json`, and the assembler
voices every segment whose clip exists, holding remaining segments as readable on-screen text so each
video is always complete and correctly timed. Re-run `render_course.py` after generating more clips to
upgrade a video to fully-narrated.

## Produce a video

```
./.venv/bin/python studio/bin/render_course.py studio/data/subjects/cac701.json
```

Serve the library: `cd out && python3 -m http.server 8080`.
