"""
combine.py — Join the twenty lectures into one continuous MP4.

    python tools/compact.py    # (prerequisite) build videos/*.mp4
    python tools/combine.py    # -> videos/IENRL-complete-course.mp4

Streams are copied, not re-encoded, so this is a remux and costs seconds
rather than hours. Chapter markers are written from the real measured
durations, which is what makes a ten-hour file navigable: the viewer can jump
straight to any lecture.

Courtesy: Triune Biblical University Global Extension, USA.
"""

from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BIN = glob.glob(os.path.join(ROOT, "venv", "lib", "python3.11",
                             "site-packages", "imageio_ffmpeg", "binaries",
                             "ffmpeg-*"))
FFMPEG = next((f for f in BIN if not f.endswith((".py", ".md"))), "ffmpeg")

SRC = os.path.join(ROOT, "videos")
OUT = os.path.join(SRC, "IENRL-complete-course.mp4")


def duration(path: str) -> float:
    r = subprocess.run([FFMPEG, "-hide_banner", "-i", path],
                       capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        raise RuntimeError(f"could not read duration of {path}")
    h, mnt, s = (float(x) for x in m.groups())
    return h * 3600 + mnt * 60 + s


def main() -> None:
    parts = []
    for n in range(1, 21):
        p = os.path.join(SRC, f"lecture-{n:02d}.mp4")
        if not os.path.exists(p):
            sys.exit(f"missing {p} — run tools/compact.py first")
        d = json.load(open(os.path.join(ROOT, "content",
                                        f"lecture-{n:02d}.json"), encoding="utf-8"))
        parts.append((p, d.get("title", f"Lecture {n:02d}"), n))

    print("measuring durations…", flush=True)
    spans, t = [], 0.0
    for p, title, n in parts:
        d = duration(p)
        print(f"  L{n:02d} {d/60:6.2f} min  {title}", flush=True)
        spans.append((t, t + d, title, n))
        t += d

    lst = os.path.join(ROOT, "build", "combine_list.txt")
    os.makedirs(os.path.dirname(lst), exist_ok=True)
    with open(lst, "w", encoding="utf-8") as f:
        f.write("ffconcat version 1.0\n")
        for p, _, _ in parts:
            f.write(f"file '{p}'\n")

    meta = os.path.join(ROOT, "build", "combine_chapters.txt")
    with open(meta, "w", encoding="utf-8") as f:
        f.write(";FFMETADATA1\n")
        for start, end, title, n in spans:
            f.write("[CHAPTER]\nTIMEBASE=1/1000\n"
                    f"START={int(start*1000)}\nEND={int(end*1000)}\n"
                    f"title=Lecture {n:02d} — {title}\n\n")

    print(f"\njoining {len(parts)} files -> {OUT}", flush=True)
    cmd = [
        FFMPEG, "-y", "-loglevel", "error", "-stats",
        "-f", "concat", "-safe", "0", "-i", lst,
        "-i", meta,
        "-map", "0:v", "-map", "0:a", "-map", "0:s",
        "-map_metadata", "1",
        "-c", "copy",
        "-movflags", "+faststart",
        "-metadata", "title=International Energy and Natural Resources Law — "
                     "complete 20-lecture course",
        "-metadata", "artist=Prof. Williams",
        "-metadata", "album_artist=TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA",
        "-metadata", "comment=20 lectures, 10 hours. Use the chapter menu to jump "
                     "between lectures.",
        OUT,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(OUT):
        sys.exit("combine failed:\n" + r.stderr[-2000:])

    size = os.path.getsize(OUT) / (1024 * 1024)
    print(f"\ndone: {size:.0f} MB, {duration(OUT)/3600:.2f} hours, "
          f"{len(spans)} chapters", flush=True)


if __name__ == "__main__":
    main()
