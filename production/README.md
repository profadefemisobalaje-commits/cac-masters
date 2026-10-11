# WHAT YOU MAY NOT KNOW ABOUT CHRISTIAN THEOLOGY — Production Source

A 60-minute cinematic educational video podcast.
Courtesy: **TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA**
Special Recognition: **Prof. Adeleke Daniel Durojaiye (PhD), President and Chancellor**

This directory is the **reproducible production source**. All generated media
(slides, narration audio, the final MP4, captions) is produced *from* these files
by the build tools in `tools/`. Generated media lives in `out/` and is git-ignored.

## Deliverable map

| Master-prompt deliverable | Produced by |
|---|---|
| A. Complete time-coded podcast script | `script/*.md` (source of truth) |
| B. 100–120 individual 3840×2160 slides | `tools/render_slides.py` → `out/slides/` |
| C. Storyboard | `tools/make_storyboard.py` → `out/storyboard.md` |
| D. Final 60:00 MP4, H.264/AAC | `tools/assemble_video.py` → `out/video/` |
| E. Narration audio, SRT, thumbnail, YouTube metadata, credits | `out/audio/`, `tools/make_srt.py`, `assets/`, `out/youtube.md`, `out/credits.md` |

## Script convention (machine-parseable)

Each scene block in `script/*.md`:

```
### SCENE <id> | <start> – <end> | SLIDE <nnn>
VISUAL: <visual direction>
ANIM:   <animation / motion direction>
MUSIC:  <music / sound cue>
CUE:    <on-screen text to render on the slide>
CITE:   <citation line, rendered discreetly at slide foot>
NARRATION:
<narration text, or "(none)" for a music-only scene>
```

Start/end are *planned* timecodes. After narration is recorded, the assembler
re-times every scene to the **measured** audio duration, so the delivered
runtime is exactly 60:00 by construction rather than by word-count estimate.

## Build order

1. Author `script/*.md` (sections 00–14).
2. `tools/parse_script.py` → `out/scenes.json`.
3. Record narration (chunked TTS, warm educated conversational English voice).
4. `tools/retiming.py` measures real audio durations and rewrites timecodes.
5. `tools/render_slides.py` renders 4K slides from `scenes.json`.
6. `tools/make_storyboard.py`, `tools/make_srt.py`.
7. `tools/assemble_video.py` → final MP4.

## Assets

- `assets/fonts/` — OFL-licensed variable fonts from the Google Fonts project,
  instantiated to static weights (Cinzel, Cormorant Garamond, EB Garamond,
  Inter, Source Sans 3, Montserrat). Licences in `assets/fonts/raw/OFL-*.txt`.
- Design tokens live in `tools/design.py` (midnight navy, antique gold, ivory,
  deep burgundy, charcoal).
