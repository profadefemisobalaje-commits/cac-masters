# CPY 701 — Introduction to Counseling Psychology
### Master's Degree in Counseling Psychology · narrated video lecture series

A 16-week, presentation-styled video lecture series with editable decks,
narration scripts and captions. Week 1 is fully produced as the style pilot;
the same pipeline produces every remaining week.

## Contents

| Path | What it is |
|---|---|
| `00-16-Week-Video-Outline.md` | The full 16-week arrangement: modules, weekly topics, learning outcomes, coverage, assessment scheme, reading list, production spec |
| `video/slides/wNN.json` | Slide + narration content for week NN (single source of truth for video, deck, captions) |
| `video/src/render.js` | Slide renderer (SVG → 1920×1080 PNG), design system included |
| `video/src/build_video.py` | Narration chunk planner + MP4 assembler (chapters, SRT captions) |
| `video/src/export_pptx.py` | Editable PowerPoint export of any week's deck |
| `dist/` *(generated, not in Git)* | Rendered slides, audio, `CPY701-WNN-lecture.mp4`, `CPY701-WNN-slides.pptx`, `wNN-captions.srt` |

## Rebuild pipeline (any week)

```bash
cd video
npm install                                   # @resvg/resvg-js
node src/render.js w01                        # slides -> ../dist/slides/w01
python3 src/build_video.py plan w01           # narration scripts -> ../dist/audio/w01/chunk-NN.txt
# (narrate the chunk scripts with the course voice, save as chunk-NN.mp3 in the same folder)
python3 src/build_video.py assemble w01       # -> ../dist/CPY701-W01-lecture.mp4 + captions
python3 src/export_pptx.py w01                # -> ../dist/CPY701-W01-slides.pptx
```

Requirements: Node ≥ 18; Python ≥ 3.9 with `imageio-ffmpeg` (or system ffmpeg);
`python-pptx` for the deck export. Slide typography uses Inter and Poppins
(TrueType) registered in `~/.fonts` — see `video/FONTS.md`.

## Series status

| Week | Topic | Status |
|---|---|---|
| 1 | The Nature and Concept of Counseling Psychology | **Produced** (video + deck + captions) |
| 2 | Historical and Philosophical Development | **Produced** (video + deck + captions) |
| 3 | Relationship to Other Disciplines and Helping Professions | **Produced** (video + deck + captions) |
| 4 | Theoretical Orientations I: Psychodynamic, Humanistic, Existential | **Produced** (video + deck + captions) |
| 5–16 | See `00-16-Week-Video-Outline.md` | Content outlined, production queued |

## Preview player

`preview/` is a small self-contained lecture player for reviewing produced
weeks: slide-synced captions, keyboard controls, per-week outline navigation,
download links, and (where the narrated MP4 is present in `dist/`) a switch to
the full lecture film with embedded WebVTT captions.

```bash
python3 preview/server.py 8000     # range-capable static server
# open http://<host>:8000/preview/
```

`preview/data.js` is regenerated from the rendered decks and caption tracks:

```bash
cd video && .venv/bin/python src/preview_build.py
```
