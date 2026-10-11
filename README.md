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
dist/lecture-01.mp4 … dist/lecture-20.mp4
```

---

## Rebuilding

```bash
pip install -r requirements.txt        # or use the existing .venv
python tools/pipeline.py 1 2 3 … 20    # lectures that already have an MP4 are skipped
python tools/site.py                   # regenerate site/index.html
python tools/serve.py                  # serve the library
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
| `slides/`, `build/`, `dist/` | Generated: PNGs, WAV/SRT, MP4s |
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
