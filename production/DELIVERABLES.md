# DELIVERABLES INDEX
## WHAT YOU MAY NOT KNOW ABOUT CHRISTIAN THEOLOGY
Courtesy: TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA
Special Recognition: Prof. Adeleke Daniel Durojaiye (PhD), President and Chancellor

Verified master: `out/video/final_1080p.mp4`
- Duration **01:00:00.00** exactly (15 segments, boundaries on 04:00 multiples)
- Video H.264 (High), 1920×1080, 30 fps, yuv420p, 16:9
- Audio AAC-LC, 48 kHz stereo, 192 kb/s
- Narration −16 LUFS; original score bed ≈ −30 dBFS (≈11–12 dB below speech)
- 173 MB

| # | Deliverable | Path |
|---|---|---|
| A | Complete time-coded script (111 scenes, 6,733 words) | `script/*.md` |
| A' | Machine-readable scenes | `out/scenes.json` |
| A'' | Measured timeline (exact 3600.000 s) | `out/timeline.json` |
| B | 111 individual 3840×2160 slide masters (no collages) | `out/slides/slide_001.png … slide_111.png` |
| C | Storyboard (scene, timestamps, slide, narration, visual, animation, music, citations) | `out/storyboard.md` |
| D | Final MP4 | `out/video/final_1080p.mp4` |
| E1 | Separate narration track (−16 LUFS) | `out/audio/narration_track.wav` |
| E2 | Full narration+score mix | `out/audio/mix.wav` |
| E3 | Original licence-clean score | `out/audio/score.wav` |
| E4 | Closed captions (434 cues) | `out/captions.srt` |
| E5 | Podcast thumbnail 1280×720 | `out/assets/thumbnail.png` |
| E6 | YouTube title, description, chapters, tags | `out/youtube.md` |
| E7 | Credits & scholarly references | `out/credits.md` |
| — | Editable presentation source (design system + generators) | `tools/*.py` |

## Reproducibility
`tools/parse_script.py` → `tools/chunk_audio.py` → (record) → `tools/retime.py`
→ `tools/score.py` → `tools/build_audio.py` → `tools/render_slides.py`
→ `tools/make_outputs.py` → `tools/assemble_video.py`

## Integrity
- Opening encomium uses only the supplied name, office and institution; no
  invented awards, appointments or rankings.
- Historical claims carry on-screen citations; contested matters are
  attributed; popular myths (Nicaea choosing the canon, English-original
  Bible, uniform early church) are corrected, not repeated.
- Stylized maps and artistic reconstructions are labelled as such on screen.
- Typography: SIL OFL faces (Cinzel, Cormorant Garamond, EB Garamond, Inter,
  Montserrat, Source Sans 3). Music and narration synthesized for this
  production; no third-party media reused.
