#!/usr/bin/env python3
"""Count words in the CAC handbook main text (course chapters only).

Front matter, appendices and back matter are reported separately and excluded
from the total, per HANDBOOK-STANDARD.md §9.
"""
import re
from pathlib import Path
from collections import defaultdict

MS = Path(__file__).resolve().parents[1] / "manuscript"
TARGET = 8000  # words per course chapter


def words(text):
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)\{[^}]*\}", r"\1", text)   # keep captions, drop paths
    text = re.sub(r"\{[.#][^}]*\}", "", text)                        # attribute blocks
    text = re.sub(r"^:::.*$", "", text, flags=re.M)                  # div fences
    text = re.sub(r"\[\^[^\]]+\]:?", "", text)                       # footnote markers
    text = re.sub(r"[#*_>|`]", " ", text)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.\-–/]*", text))


def main():
    per = defaultdict(int)
    order = []
    for f in sorted((MS / "chapters").glob("*.md")):
        m = re.match(r"(\d+)", f.name)
        key = m.group(1) if m else f.name
        if key not in per:
            order.append(key)
        per[key] += words(f.read_text())
    tot = 0
    print(f"Course chapters (target: >= {TARGET:,} words each)")
    for ch in order:
        n = per[ch]
        flag = "OK" if n >= TARGET else "SHORT"
        print(f"  {ch}: {n:7,d} words  [{flag}]")
        tot += n
    print(f"MAIN TEXT TOTAL: {tot:,d} words")
    for sub in ("front", "appendices", "back"):
        d = MS / sub
        if d.exists():
            n = sum(words(f.read_text()) for f in sorted(d.glob("*.md")))
            print(f"  ({sub}: {n:,d} words — not counted)")


if __name__ == "__main__":
    main()
