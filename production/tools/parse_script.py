#!/usr/bin/env python3
"""Parse production/script/*.md scene blocks into out/scenes.json.

Scene block grammar:
    ### SCENE <id> | <start> - <end> | SLIDE <nnn>
    VISUAL: ...
    ANIM:   ...
    MUSIC:  ...
    CUE:    ...
    CITE:   ...
    NARRATION:
    <lines until next block / end>
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_DIR = os.path.join(ROOT, "script")
OUT = os.path.join(ROOT, "out")

HEAD = re.compile(r"^###\s+SCENE\s+(\S+)\s*\|\s*([\d:.]+)\s*[-–]\s*([\d:.]+)\s*\|\s*SLIDE\s+(\d+)", re.I)
FIELD = re.compile(r"^(VISUAL|ANIM|MUSIC|CUE|CITE|SECTION|TITLE)\s*:\s*(.*)$", re.I)


def tc(s):
    """'01:23.5' or '00:01:23.5' -> seconds float."""
    parts = s.strip().split(":")
    parts = [float(p) for p in parts]
    while len(parts) < 3:
        parts.insert(0, 0.0)
    h, m, sec = parts
    return h * 3600 + m * 60 + sec


def parse_file(path):
    scenes, cur = [], None
    mode = None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = HEAD.match(line)
        if m:
            if cur:
                scenes.append(cur)
            cur = {
                "id": m.group(1),
                "start": tc(m.group(2)),
                "end": tc(m.group(3)),
                "slide": int(m.group(4)),
                "visual": "", "anim": "", "music": "", "cue": "", "cite": "",
                "section": "", "narration": "",
            }
            mode = None
            continue
        if cur is None:
            continue
        fm = FIELD.match(line)
        if fm:
            key = fm.group(1).lower()
            cur[key] = fm.group(2).strip()
            mode = None
            continue
        if line.strip().upper().startswith("NARRATION:"):
            mode = "narration"
            continue
        if mode == "narration":
            cur["narration"] += line + "\n"
    if cur:
        scenes.append(cur)
    # SECTION (and file-level context) is declared once per file: inherit forward.
    last = ""
    for s in scenes:
        if s["section"]:
            last = s["section"]
        else:
            s["section"] = last
        s["narration"] = s["narration"].strip()
        if s["narration"].lower() == "(none)":
            s["narration"] = ""
        s["words"] = len(s["narration"].split())
    return scenes


def main():
    os.makedirs(OUT, exist_ok=True)
    files = sorted(glob.glob(os.path.join(SCRIPT_DIR, "*.md")))
    if not files:
        print("no script files found", file=sys.stderr)
        sys.exit(1)
    scenes = []
    for f in files:
        got = parse_file(f)
        for s in got:
            s["file"] = os.path.basename(f)
        scenes.extend(got)
        print(f"{os.path.basename(f):<24} {len(got):>3} scenes  {sum(s['words'] for s in got):>5} words")
    scenes.sort(key=lambda s: s["start"])
    total_words = sum(s["words"] for s in scenes)
    planned = scenes[-1]["end"] if scenes else 0
    meta = {
        "title": "WHAT YOU MAY NOT KNOW ABOUT CHRISTIAN THEOLOGY",
        "courtesy": "TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA",
        "recognition": "Prof. Adeleke Daniel Durojaiye (PhD), President and Chancellor",
        "scenes": scenes,
    }
    with open(os.path.join(OUT, "scenes.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
    print(f"\nTOTAL {len(scenes)} scenes | {total_words} narration words | planned span 0:00-{planned/60:.1f} min")
    print(f"Implied pace at 60:00 target: {total_words/60:.1f} wpm")


if __name__ == "__main__":
    main()
