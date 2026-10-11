#!/usr/bin/env python3
"""Re-assemble a lecture atomically, for validating the frame-grid fix.

Assembles to <slug>.tmp.mp4 and only replaces the served master once the new
file is complete, so a viewer streaming the live gallery copy never sees a
half-written file. Used to bring already-finished weeks onto the quantized
timeline introduced in lib/video.quantize_totals.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_lecture as B

_orig_paths = B.paths


def _paths(slug):
    p = _orig_paths(slug)
    p["_final_mp4"] = p["mp4"]
    p["mp4"] = p["mp4"] + ".tmp.mp4"
    return p


def rebuild(week_json: str) -> dict:
    B.paths = _paths
    lec = B.Lecture.load(week_json)
    meta = B.do_assemble(lec)
    p = _orig_paths(lec.slug)
    tmp = p["mp4"] + ".tmp.mp4"
    os.replace(tmp, p["mp4"])
    meta["mp4"] = p["mp4"]
    meta["replaced"] = True
    return meta


if __name__ == "__main__":
    for path in sys.argv[1:]:
        meta = rebuild(path)
        print(f"replaced {meta['mp4']}  {meta['duration_hms']}  "
              f"tempo {meta['tempo']}  segments {meta['segments']}", flush=True)
