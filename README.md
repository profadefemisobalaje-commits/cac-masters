# cac-masters

**International Energy and Natural Resources Law — a twenty-lecture video course.**

> *Why You Must Study International Energy and Natural Resources Law at All Programme Levels*
>
> Lecturer: **Prof. Williams**
> Courtesy: **TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA**
> Levels: **Undergraduate** and **Postgraduate** · Scope: **Global perspectives**

Twenty lectures, 30 minutes each — 10 hours of instruction, 70,697 words of
narration across 340 slides.

---

## Downloading the videos

The MP4s are generated assets (~1.06 GB) and are **not** committed to git. Start
the course library and download from the page:

```bash
python tools/serve.py --port 8000
# open http://localhost:8000/
```

Every lecture card has a **Download MP4** button (≈53 MB each), and the page ends
with a **Direct downloads** list of all twenty files. The server speaks HTTP
Range, so downloads resume after an interruption and browser playback seeks
properly. Filenames come out clean, e.g.
`Lecture 13 - Climate Change Law and the Future of Fossil Fuels.mp4`.

You can also pull a single file straight from `dist/`:

```
videos/lecture-01.mp4 … videos/lecture-20.mp4
```

---

## Download editions

| Set | Path | Per file | Total |
|---|---|---|---|
| **Download edition** | `videos/lecture-01.mp4` … `lecture-20.mp4` | ~17.7 MB | ~355 MB |
| Masters | `videos/hd/lecture-01.mp4` … `lecture-20.mp4` | ~56 MB | ~1.1 GB |

Both are 1920x1080 with soft English subtitles. The download edition is made
by `tools/compact.py` and is three times smaller with no visible difference:
the picture is a slide that changes every few minutes, so 24 fps is 24 copies
of the same frame and 1 fps is informationally lossless; and the audio drops
from 128 kbps to 64 kbps mono, which is imperceptible on speech.

```bash
venv/bin/python tools/compact.py     # videos/hd/*.mp4 -> videos/*.mp4
```

## A warning about `.gitignore`

Files listed in `.gitignore` are **not** captured in workspace snapshots. An
earlier version of this repo ignored `*.mp4` and `dist/`, so every rendered
lecture was silently discarded at the end of a session and had to be rebuilt
from scratch. The videos now live in `videos/`, which is deliberately *not*
ignored.

Because `venv/` and `voices/` are also un-ignored (so they survive a rollover),
**never run `git add -A` here** — add paths explicitly.

## Rebuilding

```bash
python3 -m venv venv && venv/bin/pip install -r requirements.txt
venv/bin/python tools/fetch_voice.py       # Piper voice, ~63 MB
venv/bin/python tools/pipeline.py        # lectures that already have an MP4 are skipped
venv/bin/python tools/site.py            # regenerate site/index.html
venv/bin/python tools/serve.py           # serve the library
```

Each lecture takes roughly 8–9 minutes: ~5 s of slide rendering, ~4.5 min of
text-to-speech, and ~5 min of encoding.

### Layout

| Path | What it holds |
|---|---|
| `content/lecture-NN.json` | Source of truth — slides, narration, readings, quiz |
| `tools/slides.py` | 1920×1080 slide renderer (Pillow, 2× supersampled) |
| `tools/tts.py` | Piper text-to-speech engine + legal/academic text normaliser |
| `tools/pipeline.py` | End-to-end build: slides → audio → subtitles → MP4 → script |
| `tools/site.py` | Builds the course library page |
| `tools/serve.py` | Static server with HTTP Range support |
| `slides/`, `build/` | Generated: PNGs, WAV/SRT |
| `videos/` | **The deliverable** — 20 MP4s, kept un-ignored so they persist |
| `lectures/` | Markdown reading companion for each lecture |
| `site/` | Generated `index.html` (symlinks `video/` → `dist/`, `script/` → `lectures/`) |

---

## The series

**Foundations**

1. The Case for Studying International Energy and Natural Resources Law
2. What IENRL Is: Scope, Sources and Subjects
3. Permanent Sovereignty over Natural Resources: Right, Duty and Trust
4. The Global Energy Order: Geopolitics, Markets and Law
5. Natural Resources in International Economic Law: Trade, Investment and Development

**The commodity regimes**

6. International Petroleum Law: Concessions, Production Sharing and Joint Ventures
7. International Gas Law and Cross-Border Pipelines
8. Electricity, Regional Power Pools and Cross-Border Energy Trade
9. The Law of the Sea and Offshore Energy Resources
10. Mining and Critical Minerals in International Law
11. Nuclear Energy Law: Non-Proliferation, Safety and Liability

**Cross-cutting themes**

12. Renewable Energy and the International Law of the Energy Transition
13. Climate Change Law and the Future of Fossil Fuels
14. Human Rights, Indigenous Peoples and Resource Extraction
15. Environmental Protection, Biodiversity and the Extractive Sector

**Dispute settlement and the future**

16. Investment Arbitration and the Energy Charter Treaty
17. Corruption, Transparency and the Governance of Resource Revenue
18. International Energy Institutions and Global Governance
19. Energy Poverty, Energy Justice and the Right to Energy
20. Why You Must Study This Subject: Synthesis and Prospect

Every lecture carries a real case — Texaco v Libya, Aminoil v Kuwait,
India — Solar Cells, BP v Libya, Naftogaz v Gazprom, AES v Hungary, North Sea
Continental Shelf, Bangladesh v Myanmar, Bear Creek v Peru, Nuclear Tests,
Eiser v Spain, **SERAC v Nigeria (the Ogoni case)**, Pulp Mills, Yukos v Russia,
**World Duty Free v Kenya**, and **Joseph v City of Johannesburg** — together
with readings, a self-test quiz, and learning outcomes split for undergraduate
and postgraduate students.

---

## Release

`v1.0.0` documents the completed series.
