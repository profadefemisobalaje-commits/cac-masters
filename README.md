# cac-masters

Master in Counseling Psychology — accelerated 1-year lecture-video programme (CAC Masters).

## Contents

| Path | Description |
|---|---|
| `curriculum/00-accelerated-1-year-master-plan.md` | The accelerated 12-month curriculum: 3 × 16-week semesters, block delivery, week-by-week calendar, assessment, thesis roadmap |
| `curriculum/01-video-production-plan.md` | Scope, arithmetic and staging for the 448-video series, including the honest capacity limits |
| `content/<course>/week-NN.json` | Authored lecture: slides + narration in one file per week |
| `curriculum/02-week-authoring-guide.md` | **How to write a week: narrative arc, slide mix, word budget, layout reference** |
| `data/branding.json` | **Programme branding — institution and lecturer name. Change here, rebuild, and the whole series restyles.** |
| `data/courses.csv` | All 28 courses with semester, block, teaching weeks, credit hours |
| `data/schedule-52-weeks.csv` | Week-by-week schedule for the full 52-week year |
| `tools/` | Slide engine, PPTX export, narration driver, video assembler |

## Pipeline

```bash
bash tools/setup_env.sh                                  # once per session

python3 tools/build_lecture.py check    content/cpy-701/week-01.json
python3 tools/build_lecture.py slides   content/cpy-701/week-01.json   # PNGs + PPTX
python3 tools/narrate.py       plan     content/cpy-701/week-01.json   # speech-call manifest
python3 tools/narrate.py       status   content/cpy-701/week-01.json   # what audio is missing
python3 tools/narrate.py       merge    content/cpy-701/week-01.json   # chunks -> NN.mp3 per slide
python3 tools/script_export.py          content/cpy-701/week-01.json   # presenter recording script
python3 tools/build_lecture.py assemble content/cpy-701/week-01.json   # MP4 + VTT + transcript
python3 tools/build_lecture.py sidecars content/cpy-701/week-01.json   # rebuild .vtt/.txt only, no re-encode
python3 tools/clean.py --work --all                                    # reclaim build intermediates
```

## Outputs per lecture

| File | Purpose |
|---|---|
| `<slug>.mp4` | 1920×1080, H.264, 30 fps, AAC — ready for LMS or YouTube |
| `<slug>.pptx` | Editable deck with narration in the speaker notes |
| `<slug>.vtt` | WebVTT subtitles, one cue per slide |
| `<slug>.txt` | Transcript with slide markers and segment timings |
| `<slug>-RECORDING-SCRIPT.txt` | Presenter script: running order, timings, narration, `>>BREATHE` slide cues |
| `slides/*.png` | Slide images at 1920×1080 |
| `narration-plan.json` | Chunked speech manifest and progress |
| `build.json` | Manifest: segments, duration, word count |

## Slide layouts available

`title` `section` `outline` `objectives` `bullets` `twocol` `definition` `quote`
`table` `casestudy` `takeaways` `reading` `stats` `process` `end`

Change the whole series' look in one file: `tools/lib/theme.py` (colours, type scale, fonts).

## Status

- [x] Accelerated 1-year curriculum arrangement
- [x] Slide engine, video assembler, PPTX and subtitle export
- [x] CPY 701 Week 1 built as the gold-standard template
- [x] Template approved; narration via presenter recording script
- [x] **CPY 701 Week 1 complete and verified — 35:00.000, all cues frame-accurate**
- [x] Branding: Triune Biblical University Global Extension, USA — Prof. S.M.A. Philips
- [x] **CPY 701 Week 2 complete and verified — 35:00.000, all 20 cues frame-accurate**
- [ ] CPY 701 Weeks 2–16
- [ ] Remaining 27 courses × 16 weeks
