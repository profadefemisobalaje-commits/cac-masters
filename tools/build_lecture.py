#!/usr/bin/env python3
"""Build one weekly lecture: slides, then video.

    python3 tools/build_lecture.py slides   content/cpy-701/week-01.json
    python3 tools/build_lecture.py assemble content/cpy-701/week-01.json

`slides`   renders every slide to out/<slug>/slides/NN_layout.png and writes a .pptx
`assemble` pairs those slides with out/<slug>/audio/NN.mp3 (produced separately)
           and renders out/<slug>/<slug>.mp4 plus .vtt and .txt
`sidecars` rebuilds only .vtt and .txt against an already built video
"""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import slidekit as SK
from lib.course import Lecture, ROOT, MEDIA
from lib.video import Segment, build_video, write_vtt, write_transcript, duration
from lib import pptx_export

OUT = MEDIA


def paths(slug: str) -> dict:
    base = os.path.join(OUT, slug)
    return {
        "base": base,
        "slides": os.path.join(base, "slides"),
        "audio": os.path.join(base, "audio"),
        "work": os.path.join(base, "work"),
        "mp4": os.path.join(base, f"{slug}.mp4"),
        "pptx": os.path.join(base, f"{slug}.pptx"),
        "vtt": os.path.join(base, f"{slug}.vtt"),
        "txt": os.path.join(base, f"{slug}.txt"),
        "meta": os.path.join(base, "build.json"),
    }


def do_slides(lec: Lecture) -> dict:
    p = paths(lec.slug)
    # wipe first: slide files are named NN_layout.png, so a changed layout or a
    # reordered deck would otherwise leave stale images that silently mis-assemble
    if os.path.isdir(p["slides"]):
        for f in os.listdir(p["slides"]):
            if f.endswith(".png"):
                os.remove(os.path.join(p["slides"], f))
    os.makedirs(p["slides"], exist_ok=True)
    problems = lec.validate()
    if problems:
        print("VALIDATION PROBLEMS:")
        for x in problems:
            print("  -", x)
        if any("missing narration" in x for x in problems):
            return {"ok": False, "problems": problems}
    specs = lec.slide_specs()
    files = []
    for i, spec in enumerate(specs, 1):
        im = SK.render(spec)
        fn = os.path.join(p["slides"], f"{i:02d}_{spec['layout']}.png")
        im.save(fn, optimize=True)
        files.append(fn)
    pptx_export.export(specs, p["pptx"], title=f"{lec.course} — {lec.title}")
    meta = {
        "course": lec.course, "course_title": lec.course_title, "week": lec.week,
        "title": lec.title, "slug": lec.slug, "slides": len(specs),
        "words": lec.word_count, "est_minutes": round(lec.est_minutes, 1),
        "problems": problems,
    }
    # merge: never destroy assemble metadata (tempo, duration) recorded earlier
    if os.path.exists(p["meta"]):
        try:
            old = json.load(open(p["meta"], encoding="utf-8"))
            old.update(meta)
            meta = old
        except (OSError, ValueError):
            pass
    with open(p["meta"], "w") as f:
        json.dump(meta, f, indent=2)
    print(f"slides  {len(files):>3} -> {p['slides']}")
    print(f"pptx         -> {p['pptx']}")
    print(f"words {lec.word_count:>5}  est {lec.est_minutes:5.1f} min")
    return meta


def do_assemble(lec: Lecture) -> dict:
    p = paths(lec.slug)
    specs = lec.slide_specs()
    segs = []
    missing = []
    for i, s in enumerate(lec.slides, 1):
        img = os.path.join(p["slides"], f"{i:02d}_{s['layout']}.png")
        fmt = None
        for ext in (".mp3", ".wav", ".m4a", ".opus", ".aac"):
            cand = os.path.join(p["audio"], f"{i:02d}{ext}")
            if os.path.exists(cand):
                fmt = cand
                break
        if not os.path.exists(img) or not fmt:
            missing.append(i)
            continue
        segs.append(Segment(index=i, layout=s["layout"], image=img, audio=fmt,
                            text=s.get("narration", ""),
                            pad_lead=s.get("pad_lead", 0.7),
                            pad_tail=s.get("pad_tail", 1.6)))
    if missing:
        raise SystemExit(f"missing slide image or audio for slides: {missing}")
    meta = build_video(segs, p["mp4"], p["work"],
                       transcript_path=p["txt"], vtt_path=p["vtt"],
                       title=f"{lec.course} — {lec.title}",
                       target_duration=lec.data.get("target_minutes", 35) * 60)
    meta.update({"course": lec.course, "week": lec.week, "slug": lec.slug,
                 "words": lec.word_count})
    with open(p["meta"], "w") as f:
        json.dump(meta, f, indent=2)
    print(json.dumps(meta, indent=2))
    return meta


def do_sidecars(lec: Lecture) -> dict:
    """Rewrite only the .vtt and .txt against an already built video.

    Useful when narration text was corrected after encoding: subtitles and
    transcript refresh in seconds instead of re-encoding the whole lecture.
    """
    p = paths(lec.slug)
    if not os.path.exists(p["meta"]):
        raise SystemExit("no build.json — run assemble first")
    meta = json.load(open(p["meta"]))
    tempo = meta.get("tempo")
    segs = []
    for i, s in enumerate(lec.slides, 1):
        img = os.path.join(p["slides"], f"{i:02d}_{s['layout']}.png")
        aud = os.path.join(p["audio"], f"{i:02d}.mp3")
        if not os.path.exists(img) or not os.path.exists(aud):
            raise SystemExit(f"missing slide or audio for slide {i}")
        segs.append(Segment(index=i, layout=s["layout"], image=img, audio=aud,
                            text=s.get("narration", ""),
                            pad_lead=s.get("pad_lead", 0.7),
                            pad_tail=s.get("pad_tail", 1.6),
                            duration=duration(aud)))
    if not tempo:
        # tempo was never recorded (e.g. slides rebuilt before assemble).
        # Derive it the same way build_video does, so cues stay in sync.
        speech = sum(x.duration for x in segs)
        padding = sum(x.pad_lead + x.pad_tail for x in segs)
        budget = lec.data.get("target_minutes", 35) * 60 - padding
        tempo = max(0.85, min(1.06, speech / budget)) if budget > 0 else 1.0
        print(f"tempo derived from audio: {tempo:.4f}")
    title = f"{lec.course} — {lec.title}"
    write_vtt(segs, p["vtt"], tempo=tempo)
    write_transcript(segs, p["txt"], title=title, tempo=tempo)
    total = sum(x.duration / tempo + x.pad_lead + x.pad_tail for x in segs)
    meta["vtt"], meta["transcript"] = p["vtt"], p["txt"]
    meta["sidecars_rebuilt"] = True
    json.dump(meta, open(p["meta"], "w"), indent=2)
    print(f"sidecars rebuilt at tempo {tempo}: {p['vtt']}")
    print(f"                                {p['txt']}")
    print(f"covered duration {total:.1f}s ({total/60:.2f} min)")
    return meta


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("slides", "assemble", "check", "sidecars"):
        print(__doc__)
        sys.exit(1)
    lec = Lecture.load(sys.argv[2])
    if sys.argv[1] == "check":
        print(f"{lec.slug}: {len(lec.slides)} slides, {lec.word_count} words, "
              f"~{lec.est_minutes:.1f} min")
        print("problems:", lec.validate() or "none")
    elif sys.argv[1] == "slides":
        do_slides(lec)
    elif sys.argv[1] == "sidecars":
        do_sidecars(lec)
    else:
        do_assemble(lec)
