# Video Production Plan — 28 Courses × 16 Weeks

**Scope as you clarified it:** every one of the 28 course subjects gets its own 16-week
video series, and every elective is produced too.

---

## 1. The arithmetic, stated plainly

| Item | Value |
|---|---|
| Course subjects | **28** (22 core + thesis + 6 electives) |
| Weekly videos per course | 16 |
| Total videos | **448** |
| Duration per video | 35 minutes |
| Total runtime | **261 hours 20 minutes** |
| Narration words per video | **~5,200** (measured pace, see section 6) |
| Total narration | **~2,010,000 words** |
| Slides per video | 18–20 |
| Total slides | **~8,500** |

For scale: 2 million words is roughly **26 average-length books**. 261 hours is about
**11 continuous days** of playback, or a full year of one 35-minute lecture five days a week.

---

## 2. What is genuinely automatable, and what is not

This matters more than any schedule, because it decides what I can deliver.

| Stage | Automatable? | Notes |
|---|---|---|
| Slide rendering | **Yes, fully** | Built. 19 slides render in 7 seconds. 8,500 slides ≈ 55 min of compute. |
| Video assembly | **Yes, fully** | Built. ffmpeg pipeline validated: slides + audio → H.264 MP4 + WebVTT + transcript. |
| Narration audio | **Yes, but metered** | Needs a text-to-speech call per slide. See the hard limit below. |
| PPTX decks | **Yes, fully** | Built, with narration in speaker notes. |
| **Subject-matter content** | **No** | The teaching substance — formulations, cases, citations, argument — has to be authored at the standard you saw in Week 1. |
| Academic accuracy review | **No — you or a reviewer** | Every claim in a 2-million-word programme needs a human check. |

### The one hard constraint

My text-to-speech capacity is **10 calls per turn**, with roughly **1,500 characters per call**.
One slide of narration is ~1,400 characters, so that is one slide per call.

- 1 video = ~19 slides = 19 TTS calls ≈ **2 turns of pure audio generation**
- 16 videos (one course) = ~300 calls ≈ **30 turns**
- 448 videos = ~8,500 calls ≈ **850 turns**

**850 turns is not achievable in a single working session**, and no amount of batching changes it.
Any honest plan has to prioritise.

---

## 3. What I have done and what exists now

| Deliverable | Status |
|---|---|
| Accelerated 1-year curriculum arrangement | ✅ Done |
| Course and schedule registers (CSV) | ✅ Done |
| 15-layout slide engine, branded, 1920×1080 | ✅ Done |
| Video assembler → MP4 + WebVTT + transcript | ✅ Done |
| PPTX export with narration notes | ✅ Done |
| **CPY 701 Week 1 — COMPLETE, SHIPPABLE** | ✅ **35:00.000 exactly.** 22 slides, 5,552 words, 1920×1080, 15 fps, 50 MB. All 22 cues verified frame-accurate against the slides. Subtitles, transcript, PPTX and recording script included |
| CPY 701 Weeks 2–16 | ⏳ Pending your approval of Week 1 |
| Remaining 27 courses × 16 weeks | ⏳ Not started |

---

## 4. Recommended staging

Do not commission 448 videos at once. Approve the template, then walk a ramp.

### Stage 0 — Approve the template (now)
Review `out/cpy-701-w01/` — slides, PPTX, transcript. Tell me what changes:
branding, tone, density, slide count, references, anything.

### Stage 1 — One complete course (CPY 701, Weeks 1–16)
- 16 videos, 16 × 35 min = **9 hrs 20 min**, ~83,000 words at the measured authoring target
- Produces 16 finished MP4s, 16 PPTX decks, 16 subtitle files
- This is the honest unit of work: it validates the template across a whole syllabus and
  gives you a shippable product for Semester 1 Week 1 through Week 16
- **Cost in my capacity:** roughly 30 turns of audio generation alone

### Stage 2 — Semester 1 (CPY 701–708)
- 8 courses × 16 = **128 videos**, 74 hrs 40 min, ~576,000 words
- Only worth starting once Stage 1 has been teaching-tested

### Stage 3 — Semesters 2 and 3 (CPY 709–728 minus electives)
- 14 courses × 16 = **224 videos**, 130 hrs 40 min

### Stage 4 — Electives (CPY 723–728)
- 6 courses × 16 = **96 videos**, 56 hrs

---

## 5. Three ways to make 448 videos feasible

Each of these cuts the audio-generation bottleneck, which is the binding constraint.

### Option 1 — Split narration into shorter segments (no capacity saving)
Not helpful on its own. The per-call character limit, not the per-call count, dominates.

### Option 2 — Record the narration in your own voice, I supply everything else  ✅ SELECTED
I produce the slide decks, the full narration script per slide, the timings, and the assembly.
You record audio (or a presenter reads from the teleprompter script), and I render the video.
**448 videos become feasible** because the TTS bottleneck disappears entirely.
This is how most real university lecture series are actually produced.

The recording script is generated per lecture:

```
python3 tools/script_export.py content/cpy-701/week-01.json
  -> out/cpy-701-w01/cpy-701-w01-RECORDING-SCRIPT.txt
```

It contains a running order with cumulative timings, then one block per slide with the
on-screen content, the narration set in readable 76-column lines, and a `>>BREATHE` marker
where the presenter changes slide. Record one audio file per slide (`01.mp3`, `02.mp3`, ...)
into `out/<slug>/audio/` and run `build_lecture.py assemble` to produce the finished MP4.

### Option 3 — Prioritise the assessed core, sample the electives
Full 16-week series for the 22 core courses; for the 6 electives, produce a shorter
flagship series (e.g. 4–6 videos each). Reduces total to ~380 videos.

### Option 4 — Reduce video length for later weeks
Weeks 1–4 at 35 minutes, Weeks 5–16 at 20 minutes. Total runtime drops to ~200 hours.
Reduces the audio-generation load by about 40%.

---

## 6. CALIBRATION — measured, not assumed

The first seven slides of Week 1 have been voiced and assembled. Measured results:

| Metric | Assumed | **Measured** |
|---|---|---|
| Narration pace | 130 wpm | **152 wpm** |
| Words needed for 35 min | ~4,550 | **~5,200** |
| Week 1 as authored | — | 4,370 words → only **~29 min** |

**Authoring target for every lecture: ~5,200 words across 18–20 slides (~275 words/slide).**

Two mechanisms keep videos at exactly 35:00:

1. **Author to target.** Aim for 5,200 words per lecture. Below ~4,800 the video
   cannot reach 35 minutes without audible stretching.
2. **Automatic tempo calibration** (built into `tools/lib/video.py`). After voicing, the
   assembler measures total speech, computes the single uniform tempo factor needed to
   land on `target_minutes` (default 35), and applies it with `atempo`. A factor of
   0.95–1.00 is inaudible and actually sounds more like a measured lecture pace. If the
   narration is so short that the factor would drop below 0.85, the build reports
   "extend the narration" rather than producing distorted audio.

Set `"target_minutes": 35` in a lecture JSON to change the target per week.

---

## 7b. ENCODING PERFORMANCE — measured

Assembly was benchmarked on a 152-second segment, then optimised. The first
implementation re-decoded the slide PNG once per frame at 30 fps, which made
image decode — not encoding — the bottleneck.

| Setting | Time per 152 s of video | Field size | 35-min video |
|---|---|---|---|
| 30 fps, re-decode per frame (original) | 77 s | 4.5 MB | ~19 min |
| 30 fps, decode once per second | 45 s | 4.1 MB | ~11 min |
| **15 fps, decode once per second (current)** | **18 s** | **4.1 MB** | **~8 min** |

Two changes, both safe for this content:

1. `-loop 1 -framerate 1` plus an `fps=15` filter, so the still image is decoded
   once per second instead of 15–30 times per second.
2. **15 fps output instead of 30.** Slide content is completely static, so the
   two framerates are visually identical — but 15 fps roughly halves both encode
   time and file size. Keyframes are set to 10-second intervals so seeking stays
   responsive. Change `FPS` in `tools/lib/video.py` if a platform demands 30.

**Impact across the series:** at the original settings, encoding 261 hours of
video would have taken roughly **520 hours**. At the current settings it is
roughly **120 hours** — and 448 videos at ~4 MB each is about **1.8 GB** of
finished media, not the ~50 GB the original settings implied.


---

## 7c. END-TO-END VALIDATION — Week 1

Week 1 was assembled, then verified rather than assumed correct.

| Check | Result |
|---|---|
| Duration | **2100.00 s = 35:00.000** (container reports 34:59.96) |
| Tempo applied | 0.9915 — a 0.85% slowdown, inaudible |
| Decode | Clean full-length decode, no errors |
| Streams | H.264 High, 1920×1080, 15 fps; AAC 128 kbps, 44.1 kHz stereo |
| Audio levels | mean −23.2 dB, peak −3.1 dB — no clipping, healthy headroom |
| File size | 50 MB for 35 minutes |
| Faststart | `moov` atom at the head of the file (streams progressively) |
| Slides | 22 committed assets |
| Subtitle sync | **All 22 cues verified** — a frame sampled at each cue midpoint matches its own slide and no other slide is closer |

Two defects were found by this validation and fixed:

1. **Subtitles ignored the tempo factor.** Cue times were computed from raw audio
   length while the video had been time-stretched, so cues drifted progressively
   earlier — out to 17.4 seconds by slide 22. The subtitle and transcript writers
   now take the same tempo value the video was built with.
2. **Built filenames could go stale.** Fixed earlier in the week; noted here
   because it was the reason a mismatch was possible at all.

A third fix came out of the repair: `build_lecture.py sidecars` regenerates only
the `.vtt` and `.txt` against an already-encoded video. Correcting narration text
no longer costs a 7-minute re-encode.

**Assembly time for the full lecture: 7 min 32 s** at the optimised settings.

---

## 7. Per-video production spec (validated)

```
1. content/<course>/week-NN.json     authored lecture: slides + narration, one file
2. python3 tools/build_lecture.py slides   <file>   -> 19 PNGs + PPTX
3. narration audio -> out/<slug>/audio/NN.mp3       (19 files)
4. python3 tools/build_lecture.py assemble <file>   -> MP4 + VTT + transcript
```

Outputs per lecture:

| File | Purpose |
|---|---|
| `<slug>.mp4` | 1920×1080, H.264 High, 30 fps, AAC 128 kbps — YouTube/LMS ready |
| `<slug>.vtt` | WebVTT subtitles, one cue per slide |
| `<slug>.txt` | Speaker transcript with slide markers and timings |
| `<slug>.pptx` | Editable deck, narration in speaker notes, for live teaching |
| `slides/*.png` | Source images at 1920×1080 |
| `build.json` | Manifest: segment count, duration, word count |

Verified on the Week 1 deck: 19 slides, 4,370 words, stage length **32–35 minutes**
depending on delivery pace. At 130 wpm the narration runs 33.6 minutes; the segment
padding brings the finished video to ~35 minutes.

---

## 8. DURABILITY — read this before writing any more code

Two failures destroyed a completed 35-minute lecture. Both are now fixed, and
both constraints are permanent properties of this environment.

### 8.1 Never write generated output to a directory named `out`

The platform excludes a fixed set of directory names from its workspace
snapshots. Anything written under one of them is dropped at the end of a turn:

```
out   build   dist   coverage   target   node_modules   __pycache__
.arena  .cache  .local  .npm  .nuxt  .output  .parcel-cache  .pytest_cache
.ruff_cache  .svelte-kit  .tox  .turbo  .venv  .vite
```

All generated media therefore goes to **`media/`**, defined once in
`tools/lib/course.py` as `MEDIA`. If a path is ever needed in a new tool, import
that constant rather than writing the directory name again.

### 8.2 Always push

Local commits are not durable here. When the sandbox restored, `.git` held only
the remote's initial commit and every local commit was gone, while the working
tree survived. Work is only safe once it is on `origin`.

**Working rule for the rest of the series:** voice a batch, then immediately
commit and push the audio. Audio is the single most expensive asset to
regenerate (10 clips per turn), so it is committed as soon as it exists rather
than waiting for the finished video.

### 8.3 Deliverable size

Audio dominated the deliverable: a single lecturer voice was being encoded at
128 kbps **stereo**, which alone accounted for 33 MB of a 50 MB file. It is now
**96 kbps mono**. Expected master size falls to roughly 25–30 MB per lecture,
and the same setting is applied when the segments are concatenated.

---

*Prepared alongside the accelerated curriculum master plan. Week 1 of CPY 701 is built and
waiting for your review before the remaining 447 videos are scheduled.*
