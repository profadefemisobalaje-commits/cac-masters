#!/usr/bin/env python3
"""Render slide decks + posters + manifests for every subject that has data.
Also writes per-subject TTS clip manifests. No audio required."""
import os, sys, json, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
sys.path.insert(0, ROOT)
from engine import compose as CP, assemble as AS

def main():
    files = sorted(glob.glob(os.path.join(ROOT, "data", "subjects", "*.json")))
    os.makedirs(os.path.join(REPO, "out", "scripts"), exist_ok=True)
    for f in files:
        c = json.load(open(f))
        sl = AS.slug(c)
        segs = CP.build_script(c)
        # deck
        AS.render_slides(c, segs, os.path.join(REPO, "out", "work", sl, "slides"), verbose=False)
        # poster from title slide
        os.makedirs(os.path.join(REPO, "out", "posters"), exist_ok=True)
        tp = os.path.join(REPO, "out", "work", sl, "slides", "s01_open_01.png")
        if os.path.exists(tp):
            from PIL import Image
            Image.open(tp).convert("RGB").save(os.path.join(REPO, "out", "posters", f"{sl}.jpg"), quality=88)
        # clip manifest
        man = [{"file": f"{s['id']}_c0", "text": s["clips"][0]} for s in segs]
        json.dump(man, open(os.path.join(REPO, "out", "scripts", f"{sl}_clips.json"), "w"), indent=1)
        tot = sum(len(m["text"]) for m in man)
        print(f"{c['code']:10s} {len(segs):3d} clips {tot:6d} chars ~{tot/970:4.1f}min  -> {sl}")

if __name__ == "__main__":
    main()
