# SEASON 1 — DELIVERABLES & PRODUCTION STATUS

*WHAT YOU MAY NOT KNOW ABOUT …* — thirteen-episode Tier-B deep-dive season.
Spec: `season1/SERIES_BIBLE.md`. Courtesy TRIUNE BIBLICAL UNIVERSITY GLOBAL
EXTENSION USA · Recognition Prof. Adeleke Daniel Durojaiye (PhD).

## Status board

| # | Episode | Script | Slides | Narration | Master MP4 | Notes |
|---|---------|:------:|:------:|:---------:|:----------:|-------|
| 01 | How the Bible Got Its Books | ✅ | ✅ | ✅ 17 clips | ✅ 23:43 / 67.6 MB | delivered (master since lost to sandbox reset — rebuildable from source + `vo/`) |
| 02 | The Trinity: Four Centuries of Argument | ✅ | ✅ | ✅ 19 clips | ✅ 28:56 / 82.3 MB | delivered (rebuildable from source) |
| 03 | One Person, Two Natures | ✅ | ✅ | ✅ 18 clips | ✅ 29:09 / 86.6 MB | **delivered** — see manifest below |
| 04 | Lost in Translation? | — | — | — | — | next |
| 05–13 | (per series bible §3) | — | — | — | — | scheduled |

## Episode 03 manifest — *One Person, Two Natures*

The Council of Chalcedon, and how the church spent a century learning what
**not** to say about Christ.

| Item | Path |
|------|------|
| Final MP4 (1080p, 29:09.83, 86,604,566 B) | `season1/ep03/out/video/final_1080p.mp4` |
| sha256 | `e91c6c1c2507713b55323b3717f1d28ad789d6f6bb8fd2fd9cfba9cfe62c75a6` |
| Time-coded script (38 scenes, 3,880 words) | `season1/ep03/script/ep03-christology-a.md`, `-b.md` |
| Scene model / timeline | `season1/ep03/out/scenes.json`, `out/timeline.json` |
| Slide masters (3840×2160) | `season1/ep03/out/slides/slide_001–038.png` |
| Storyboard | `season1/ep03/out/storyboard.md` |
| Closed captions (220 cues) | `season1/ep03/out/captions.srt` / `.vtt` |
| Mix / score | `season1/ep03/out/audio/mix.wav`, `score.wav` |
| Narration (voice-00, 18 clips) | `season1/ep03/out/audio/narr_00–17.mp3` |
| **Narration durability copy (Git-tracked)** | `season1/ep03/vo/` |
| Player page + static server | `season1/ep03/out/index.html`, `tools/serve_video.js` |
| Player generator (reusable) | `tools/make_player.py` |

**QC (8-point checklist):** dates verified (381 · 431 · 433 · 448 · 449 · 451 ·
553 · 681 · 787) ✅ · contested views steel-manned (Miaphysite one-nature
confession, Nestorius, Theodore of Mopsuestia) ✅ · no invented quotations
(honey-drop line flagged as hostile minutes) ✅ · map labelled schematic ✅ ·
tradition-sensitivity (Miaphysite and Church of the East sections) ✅ ·
captions generated from recorded timeline (220 cues) ✅ · narration −14.2 LUFS,
score ≥10 dB below ✅ · runtime 29:09 ≤ 30:00 Tier-B cap ✅.

## Media-storage rule (learned the hard way)

Sandbox resets wipe everything outside Git, including `out/` and any
non-ignored mirror. Recorded narration is the only irreplaceable asset (TTS
quota-bound), so each episode keeps a **Git-tracked copy in `season1/epNN/vo/`
for the duration of production**, pruned once the master MP4 is delivered and
re-encoded elsewhere. Everything else regenerates from source in ~20 minutes:

```
tools/parse_script.py → chunk_audio.py → (record) → retime.py → score.py
→ build_audio.py → render_slides.py → make_outputs.py → assemble_video.py
→ make_player.py
```
