#!/usr/bin/env python3
"""Narration driver: plans, tracks and merges per-slide speech audio.

Speech generation has a hard 1500-character limit per call, so long slide
narration is split at sentence boundaries, each chunk is synthesised
separately, and the chunks are concatenated back into one file per slide.

    python3 tools/narrate.py plan   content/cpy-701/week-01.json
    python3 tools/narrate.py status content/cpy-701/week-01.json
    python3 tools/narrate.py merge  content/cpy-701/week-01.json
"""
from __future__ import annotations
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.course import Lecture, ROOT, MEDIA
from lib.video import FFMPEG

LIMIT = 1450          # characters per speech call, with headroom under 1500
OUT = MEDIA


def split_narration(text: str, limit: int = LIMIT) -> list[str]:
    """Split at sentence boundaries, never mid-sentence unless a sentence alone is too long."""
    import re
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, cur = [], ""
    for s in sentences:
        if len(s) > limit:                      # a single enormous sentence
            if cur:
                chunks.append(cur); cur = ""
            words = s.split()
            part = ""
            for w in words:
                if len(part) + len(w) + 1 > limit:
                    chunks.append(part); part = w
                else:
                    part = f"{part} {w}".strip()
            if part:
                cur = part
            continue
        if len(cur) + len(s) + 1 > limit:
            chunks.append(cur); cur = s
        else:
            cur = f"{cur} {s}".strip()
    if cur:
        chunks.append(cur)
    return chunks


def plan(lec: Lecture) -> dict:
    base = os.path.join(OUT, lec.slug, "audio")
    os.makedirs(base, exist_ok=True)
    items = []
    for i, s in enumerate(lec.slides, 1):
        chunks = split_narration(s.get("narration", ""))
        for j, c in enumerate(chunks, 1):
            items.append({
                "slide": i,
                "chunk": j,
                "of": len(chunks),
                "layout": s["layout"],
                "chars": len(c),
                "path": os.path.join(base, f"{i:02d}_c{j}.mp3"),
                "text": c,
            })
    manifest = {
        "slug": lec.slug, "course": lec.course, "week": lec.week,
        "slides": len(lec.slides), "words": lec.word_count,
        "est_minutes": round(lec.est_minutes, 1),
        "calls": len(items), "audio_dir": base, "items": items,
    }
    mp = os.path.join(OUT, lec.slug, "narration-plan.json")
    with open(mp, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"plan: {len(items)} speech calls for {len(lec.slides)} slides "
          f"({lec.word_count} words, ~{lec.est_minutes:.1f} min)")
    print(f"manifest -> {mp}")
    return manifest


def status(lec: Lecture) -> dict:
    mp = os.path.join(OUT, lec.slug, "narration-plan.json")
    manifest = json.load(open(mp, encoding="utf-8"))
    done = [it for it in manifest["items"] if os.path.exists(it["path"]) and os.path.getsize(it["path"]) > 0]
    todo = [it for it in manifest["items"] if it not in done]
    print(f"{lec.slug}: {len(done)}/{len(manifest['items'])} speech chunks present")
    if todo:
        print("next calls needed:")
        for it in todo[:12]:
            print(f"  slide {it['slide']:>2} chunk {it['chunk']}/{it['of']}  {it['chars']:>4}c  {it['path']}")
        if len(todo) > 12:
            print(f"  ... and {len(todo)-12} more")
    # per-slide roll-up
    slides_done = sorted({it["slide"] for it in done if it["chunk"] == it["of"]})
    print(f"slides fully voiced: {len(slides_done)}/{manifest['slides']}")
    return manifest


def merge(lec: Lecture) -> None:
    """Concatenate chunk audio into one file per slide: audio/NN.mp3."""
    mp = os.path.join(OUT, lec.slug, "narration-plan.json")
    manifest = json.load(open(mp, encoding="utf-8"))
    base = manifest["audio_dir"]
    by_slide: dict[int, list[dict]] = {}
    for it in manifest["items"]:
        by_slide.setdefault(it["slide"], []).append(it)
    ok, missing = 0, []
    for i, s in enumerate(lec.slides, 1):
        chunks = sorted(by_slide.get(i, []), key=lambda x: x["chunk"])
        if not chunks or any(not os.path.exists(c["path"]) for c in chunks):
            missing.append(i); continue
        target = os.path.join(base, f"{i:02d}.mp3")
        if len(chunks) == 1:
            subprocess.run([FFMPEG, "-y", "-v", "error", "-i", chunks[0]["path"],
                            "-c:a", "libmp3lame", "-q:a", "4", target], check=True)
        else:
            lst = os.path.join(base, f"_c{i:02d}.txt")
            with open(lst, "w") as f:
                for c in chunks:
                    f.write(f"file '{os.path.abspath(c['path'])}'\n")
            subprocess.run([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0",
                            "-i", lst, "-c:a", "libmp3lame", "-q:a", "4", target], check=True)
            os.remove(lst)
        ok += 1
    print(f"merged {ok}/{len(lec.slides)} slides -> {base}")
    if missing:
        print(f"still missing chunks for slides: {missing}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("plan", "status", "merge"):
        print(__doc__); sys.exit(1)
    lec = Lecture.load(sys.argv[2])
    {"plan": plan, "status": status, "merge": merge}[sys.argv[1]](lec)
