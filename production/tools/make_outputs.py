#!/usr/bin/env python3
"""Closed captions (SRT) + storyboard (Markdown) from out/timeline.json."""
import json, os, re

ROOT = os.environ.get("TBUPROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def sentences(txt):
    parts = re.split(r"(?<=[.?!])\s+", txt.strip())
    return [p for p in parts if p]


def srt():
    tl = json.load(open(os.path.join(ROOT, "out", "timeline.json"), encoding="utf-8"))
    cues, n = [], 0
    for s in tl["scenes"]:
        if not s.get("speech_start"):
            continue
        sents = sentences(s["narration"])
        if not sents:
            continue
        tot = sum(len(x.split()) for x in sents)
        t = s["speech_start"]
        span = s["speech_end"] - s["speech_start"]
        for sent in sents:
            d = span * len(sent.split()) / tot
            n += 1
            cues.append((n, t, min(t + d, s["speech_end"]), sent))
            t += d
    with open(os.path.join(ROOT, "out", "captions.srt"), "w", encoding="utf-8") as f:
        for n, a, b, txt in cues:
            f.write(f"{n}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
    print(f"captions.srt: {len(cues)} cues")


def storyboard():
    tl = json.load(open(os.path.join(ROOT, "out", "timeline.json"), encoding="utf-8"))
    L = ["# STORYBOARD — WHAT YOU MAY NOT KNOW ABOUT CHRISTIAN THEOLOGY",
         "", "Courtesy: TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA  ",
         "Special Recognition: Prof. Adeleke Daniel Durojaiye (PhD), President and Chancellor  ",
         "Total runtime 60:00.000 · 1080p30 master · 4K slide masters delivered separately.", ""]
    for s in tl["scenes"]:
        L += [f"## SCENE {s['id']} — {ts(s['start'])[:7]} – {ts(s['end'])[:7]} — SLIDE {s['slide']:03d}",
              f"**{s['title']}**", "",
              f"- **Visual:** {s['visual']}",
              f"- **Animation:** {s['anim']}",
              f"- **Music/Sound:** {s['music']}",
              f"- **On-screen text:** {s['cue'] or '(none)'}",
              f"- **Citation:** {s['cite'] or '(none)'}",
              f"- **Narration:** {s['narration'] or '_(music only)_'}", ""]
    with open(os.path.join(ROOT, "out", "storyboard.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"storyboard.md: {len(tl['scenes'])} scenes")


if __name__ == "__main__":
    srt()
    storyboard()
