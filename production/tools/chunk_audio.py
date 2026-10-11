#!/usr/bin/env python3
"""Build the narration recording plan: out/audio/plan.json.

Chunks are cut ONLY at scene boundaries (never mid-scene) so that each
recorded clip maps to a known set of scenes; within a clip, scene durations
are later distributed in proportion to word count against the MEASURED clip
duration. Keeps every chunk under the TTS per-call character limit.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMIT = 1480  # chars per generate_speech call (hard cap 1500)

meta = json.load(open(os.path.join(ROOT, "out", "scenes.json"), encoding="utf-8"))
scenes = meta["scenes"]

chunks, cur = [], None
for s in scenes:
    txt = s["narration"].strip()
    if not txt:
        continue  # music-only scene: no clip
    add = len(txt) + (1 if cur else 0)
    if cur and len(cur["text"]) + add > LIMIT:
        chunks.append(cur)
        cur = None
    if cur is None:
        cur = {"segment": s["section"], "scenes": [], "text": "", "chars": 0}
    if cur["text"]:
        cur["text"] += "\n\n"
    cur["text"] += txt
    cur["scenes"].append(s["id"])
if cur:
    chunks.append(cur)

for i, c in enumerate(chunks):
    c["index"] = i
    c["chars"] = len(c["text"])
    c["file"] = f"out/audio/narr_{i:02d}.mp3"

os.makedirs(os.path.join(ROOT, "out", "audio"), exist_ok=True)
json.dump({"limit": LIMIT, "chunks": chunks},
          open(os.path.join(ROOT, "out", "audio", "plan.json"), "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)

import sys
lo = int(sys.argv[1]) if len(sys.argv) > 1 else 0
hi = int(sys.argv[2]) if len(sys.argv) > 2 else len(chunks)
print(f"{len(chunks)} chunks total; printing [{lo},{hi})")
for c in chunks[lo:hi]:
    print(f"\n===== CHUNK {c['index']:02d} | seg {c['segment']} | scenes {','.join(c['scenes'])} | {c['chars']} chars =====")
    print(c["text"])
