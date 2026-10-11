#!/usr/bin/env python3
"""Generate the narration recording script for a lecture.

This is the deliverable that makes a 448-video series practical: a presenter
can read it straight to camera, or record it as audio, and the numbers on each
slide tell them exactly how long to spend.

    python3 tools/script_export.py content/cpy-701/week-01.json
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.course import Lecture, ROOT, MEDIA, branding

WPM = 152.0          # measured pace of the reference voice
PAD = 1.15           # seconds of lead-in plus tail-out per slide


def block(spec: dict) -> list[str]:
    """One-line summary of what is on the slide, for the presenter."""
    l = spec.get("layout")
    out = []
    if spec.get("subtitle"):
        out.append(f"  on screen: {spec['subtitle']}")
    if l in ("bullets",):
        for b in spec.get("bullets", [])[:8]:
            t = b if isinstance(b, str) else b.get("t", "")
            out.append(("    • " if isinstance(b, str) or b.get("lvl", 0) == 0 else "      – ") + t)
    elif l == "twocol":
        for c in spec.get("columns", []):
            out.append(f"  {c['h']}:")
            for it in c["items"]:
                out.append("    • " + (it if isinstance(it, str) else it.get("t", "")))
    elif l == "table":
        out.append("  columns: " + " | ".join(spec["columns"]))
        for r in spec.get("rows", []):
            out.append("    " + " | ".join(r))
    elif l == "stats":
        for st in spec.get("stats", []):
            out.append(f"    {st['v']} — {st['l']}")
    elif l == "process":
        for i, st in enumerate(spec.get("steps", []), 1):
            out.append(f"    {i}. {st['h']}: {st['b']}")
    elif l in ("objectives", "outline", "takeaways"):
        for i, it in enumerate(spec.get("items", []), 1):
            out.append(f"    {i}. {it if isinstance(it, str) else it.get('t','')}")
    elif l == "reading":
        for it in spec.get("items", []):
            out.append("    • " + (it if isinstance(it, str) else it.get("t", "")))
    elif l == "definition":
        out.append(f"    TERM: {spec['term']}")
    elif l == "quote":
        out.append(f"    {spec['quote'][:120]}...")
    elif l == "casestudy":
        out.append(f"    {len(spec.get('paragraphs', []))} paragraphs, "
                   f"{len(spec.get('questions', []))} discussion questions")
    return out


def script(lec: Lecture) -> str:
    total_words = lec.word_count
    speech_min = total_words / WPM
    per = []
    for s in lec.slides:
        w = len(s.get("narration", "").split())
        per.append(w / WPM + PAD / 60.0)   # minutes
    total = sum(per)
    L = []
    L.append("=" * 78)
    L.append(f"NARRATION RECORDING SCRIPT")
    L.append(f"{lec.course} — {lec.course_title}")
    L.append(f"{lec.title}")
    L.append("=" * 78)
    L.append("")
    L.append(f"institution      {lec.data.get('institution') or branding().get('institution','')}")
    L.append(f"presenter        {lec.data.get('lecturer') or branding().get('lecturer','')}")
    L.append(f"target runtime   {lec.data.get('target_minutes',35)}:00")
    L.append(f"slides           {len(lec.slides)}")
    L.append(f"narration        {total_words:,} words")
    L.append(f"measured pace    {WPM:.0f} words per minute")
    L.append(f"projected speech {speech_min:.1f} min  (+ per-slide beats = {total/60:.1f} min)")
    L.append("")
    L.append("HOW TO USE")
    L.append("  1. Each block below is one slide. Read the narration at a measured,")
    L.append("     unhurried pace — the timings assume about 152 words per minute.")
    L.append("  2. When you reach '>>BREATHE', pause and change slide.")
    L.append("  3. Do not read the 'ON SCREEN' lines aloud. They are there so you")
    L.append("     know what the audience is looking at while you speak.")
    L.append("  4. Record the audio as one file per slide (01.mp3, 02.mp3, ...) and")
    L.append("     run:  python3 tools/build_lecture.py assemble <this week>.json")
    L.append("")
    L.append("RUNNING ORDER")
    L.append(f"  {'slide':>5}  {'layout':<12} {'words':>6}  {'time':>7}  title")
    L.append(f"  {'-'*5}  {'-'*12} {'-'*6}  {'-'*7}  {'-'*40}")
    acc = 0.0
    for i, (s, dur) in enumerate(zip(lec.slides, per), 1):
        t0 = acc
        acc += dur
        title = s.get("title") or s.get("term") or s.get("eyebrow") or ""
        L.append(f"  {i:>5}  {s['layout']:<12} {len(s.get('narration','').split()):>6}  "
                 f"{int(t0//60):02d}:{int(t0%60):02d}  {title[:40]}")
    L.append("")
    L.append("=" * 78)
    L.append("")
    acc = 0.0
    for i, (s, dur) in enumerate(zip(lec.slides, per), 1):
        t0, acc = acc, acc + dur
        title = s.get("title") or s.get("term") or ""
        L.append("-" * 78)
        L.append(f"SLIDE {i} of {len(lec.slides)}   |   {s['layout'].upper()}   |   "
                 f"{int(dur//60):02d}:{int(dur%60):02d}   |   {int(t0//60):02d}:{int(t0%60):02d} in")
        L.append("-" * 78)
        if title:
            L.append(f"TITLE: {title}")
        if s.get("eyebrow"):
            L.append(f"EYEBROW: {s['eyebrow']}")
        for line in block(s):
            L.append(line)
        L.append("")
        L.append("NARRATION")
        n = s.get("narration", "").strip()
        # keep paragraph breaks, wrap at 76 columns for reading
        for para in n.split("\n\n"):
            words, line = para.split(), ""
            for w in words:
                if len(line) + len(w) + 1 > 76:
                    L.append(line); line = w
                else:
                    line = f"{line} {w}".strip()
            if line:
                L.append(line)
            L.append("")
        L.append(">>BREATHE  —  advance to the next slide")
        L.append("")
    L.append("=" * 78)
    L.append("END OF SCRIPT")
    L.append("=" * 78)
    return "\n".join(L)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(1)
    lec = Lecture.load(sys.argv[1])
    text = script(lec)
    outdir = os.path.join(MEDIA, lec.slug)
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, f"{lec.slug}-RECORDING-SCRIPT.txt")
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"script -> {p}")
    print(f"  {len(lec.slides)} slides, {lec.word_count:,} words, "
          f"projected {lec.word_count/WPM + len(lec.slides)*PAD/60:.1f} min")
