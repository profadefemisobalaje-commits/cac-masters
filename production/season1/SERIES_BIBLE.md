# SEASON 1 SERIES BIBLE
## "WHAT YOU MAY NOT KNOW ABOUT …" — Thirteen Deep Dives
Courtesy: TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA
Special Recognition: Prof. Adeleke Daniel Durojaiye (PhD), President and Chancellor

## 1. Brand (unified, per producer decision)
- **Title family:** `WHAT YOU MAY NOT KNOW ABOUT <SUBJECT>` on every episode.
- **Opening (10–14 s):** brand sting — score motif (D-minor opening figure,
  shortened), title card in Cinzel, single courtesy line
  "TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA". No full presidential
  encomium in episodes; the recognition line appears once, small, on the
  end card of every episode.
- **Closing (20–25 s):** reflective card → next-episode teaser line →
  end card with courtesy + recognition line + END OF EPISODE.
- **Palette / type / voice / score family:** identical to the flagship
  (`tools/design.py`, `tools/score.py`, voice-00). No per-tier restyling.
- **Slide grammar:** section lower-thirds replaced by episode lower-thirds
  ("EP 01 · SCENE n"); citations discreet at slide foot; stylized maps and
  reconstructions always labelled.

## 2. Runtime tiers
- Deep dive (Tier B): 22–30 min, 34–42 scenes, ~3,300–4,200 narration words.
- Flagship (Tier A) and seminars (Tier D) keep the 60-min grammar.
- Shorts (Tier C), if commissioned later: 8–12 min, single-misconception arc.

## 3. Episode slate
| Ep | Title | Thesis | Core references |
|---|---|---|---|
| 01 | How the Bible Got Its Books | Canon is a process of composition, circulation, and recognition — not a single vote. | Metzger; Ehrman (as foil); Athanasius Ep. 39; Eusebius HE 3.25 |
| 02 | The Trinity: Four Centuries of Argument | The doctrine is biblical reflection hardened in controversy, not a proof-text. | Pelikan vol. 1; Ayres, Nicaea and Its Legacy |
| 03 | One Person, Two Natures | Chalcedon's four negatives guard a mystery rather than explain it. | Chadwick; Leo's Tome; Chalcedonian Definition |
| 04 | Lost in Translation? | Meaning is carried by language, genre, and context; translation is judgement. | Barr, Semantics of Biblical Language |
| 05 | The Church Before Constantine | Order and diversity coexisted long before imperial patronage. | Chadwick; Bauer (as foil); Ignatius, Didache |
| 06 | Three Shelves | Canonical differences are traditions of reception, each reasoned. | Deuterocanon studies; Trent session 4; Septuagint scholarship |
| 07 | Councils | Councils settle boundaries, not every question; reception does the rest. | Davis, The First Seven Councils |
| 08 | How to Read a Verse | Hermeneutical method is the difference between citation and evidence. | Thiselton; historical-critical method literature |
| 09 | Saved | One confession, many grammars: ransom, satisfaction, substitution, theosis. | Aulén; Trent decree; Joint Declaration on Justification |
| 10 | Faith and Science | A history of cooperation, conflict, and category discipline. | Barbour; Lindberg; Galileo documents |
| 11 | The Women the Sources Name | Women appear in the sources as agents; silence is transmission, not evidence. | Romans 16; Perpetua; Egeria |
| 12 | Africa and the East | Christianity's intellectual centre was polycentric for a millennium. | Alexandrian/Carthaginian/Syriac studies; Ephrem |
| 13 | The Last Things | Eschatology is hope and ethics; timetables are later additions. | Collins, Apocalypticism; Revelation scholarship |

## 4. Cadence and pipeline
Fortnightly release. Per episode: author `script/*.md` → parse → record
(chunked TTS, cap-aware) → retime → score bed → mix → render slides →
storyboard + SRT → assemble 1080p master. One working session per episode
once narration is recorded; narration recording spans two cap-cycles.

## 5. Quality-control checklist (per episode, mandatory)
1. Dates, councils, persons verified against the listed references.
2. Contested interpretations attributed; opposing views steel-manned.
3. No invented quotations, manuscripts, scholars, or statistics.
4. Reconstructions and stylized maps labelled on screen.
5. Tradition-sensitivity read (Protestant / Catholic / Orthodox self-descriptions).
6. Captions match recorded audio (generated from measured timeline).
7. Loudness: narration −16 LUFS; score ≥10 dB below.
8. Runtime within tier; boundaries land on clean chapter marks.

## 6. File layout
`season1/epNN/script/*.md` (source of truth), `season1/epNN/out/` (generated,
ignored). Tools accept `TBUPROJ` env to retarget any project directory.
