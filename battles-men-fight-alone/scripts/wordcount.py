#!/usr/bin/env python3
"""Word counts for Battles Men Fight Alone.

Main text = chapters only (front matter, appendices and back matter excluded).
Usage:  python3 scripts/wordcount.py [--all]
"""
import re
import sys
from pathlib import Path
from collections import defaultdict

MS = Path(__file__).resolve().parents[1] / "manuscript"


def words(text):
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)\{[^}]*\}", r"\1", text)   # keep captions
    text = re.sub(r"\{[.#][^}]*\}", "", text)
    text = re.sub(r"^:::.*$", "", text, flags=re.M)
    text = re.sub(r"\[\^[^\]]+\]:?", "", text)
    text = re.sub(r"[#*_>|`]", " ", text)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\u2019.\-\u2013/]*", text))


def main():
    ch = MS / "chapters"
    per, tot = defaultdict(int), 0
    low = []
    for f in sorted(ch.glob("*.md")):
        n = words(f.read_text())
        per[int(f.name[:2])] += n
        tot += n
        pass
    if "--all" in sys.argv:
        for k, n in sorted(per.items()):
            flag = "" if n >= 8000 else "  <-- UNDER 8,000"
            print(f"Chapter {k:2d}: {n:7,d}{flag}")
    else:
        done = sorted(per)
        print(f"Chapters written: {len(done)} (last: {done[-1] if done else '-'})")
        if done:
            print(f"Mean per chapter: {tot // len(done):,d} words")
    print(f"MAIN TEXT TOTAL: {tot:,d} words")
    short = [(k, v) for k, v in sorted(per.items()) if v < 8000]
    if short:
        print("UNDER-LENGTH CHAPTERS:", ", ".join(f"Ch{a} ({b:,d})" for a, b in short))
    for sub in ("front", "appendices", "back"):
        n = sum(words(f.read_text()) for f in (MS / sub).glob("*.md"))
        print(f"  ({sub}: {n:,d} words — not counted)")


main()
