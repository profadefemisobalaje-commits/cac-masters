#!/usr/bin/env python3
"""Count words in the main text (chapters only; front and back matter excluded)."""
import re, sys
from pathlib import Path
from collections import defaultdict
MS = Path(__file__).resolve().parents[1] / "manuscript"

def words(text):
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)\{[^}]*\}", r"\1", text)   # keep captions, drop paths
    text = re.sub(r"\{[.#][^}]*\}", "", text)                          # attribute blocks
    text = re.sub(r"^:::.*$", "", text, flags=re.M)                     # div fences
    text = re.sub(r"\[\^[^\]]+\]:?", "", text)                          # footnote markers
    text = re.sub(r"[#*_>|`]", " ", text)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.\-–/]*", text))

def main():
    per = defaultdict(int)
    for f in sorted((MS / "chapters").glob("*.md")):
        per[f.name[:2]] += words(f.read_text())
    tot = 0
    for ch, n in sorted(per.items()):
        tot += n
        print(f"Chapter {int(ch):2d}: {n:7,d}")
    print(f"MAIN TEXT TOTAL: {tot:,d} words")
    for sub in ("front", "appendices", "back"):
        n = sum(words(f.read_text()) for f in (MS / sub).glob("*.md"))
        print(f"  ({sub}: {n:,d} words — not counted)")
main()
