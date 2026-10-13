"""
volumes.py — Bundle the lectures into pushable multi-lecture volumes.

    python tools/volumes.py            # -> videos/IENRL-volume-N.mp4 x4

Why this exists: GitHub refuses any file larger than 100 MB, so the 352 MB
single-file course can never be pushed. Five lectures at the download-edition
bitrate is ~89 MB, which fits.

Streams are copied, never re-encoded, so quality is identical to the
individual lectures and this costs seconds rather than hours. Chapters are
written from measured durations so each volume is navigable.

Courtesy: Triune Biblical University Global Extension, USA.
"""

from __future__ import annotations

import glob
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BIN = glob.glob(os.path.join(ROOT, "venv", "lib", "python3.11",
                             "site-packages", "imageio_ffmpeg", "binaries",
                             "ffmpeg-*"))
FFMPEG = next((f for f in BIN if not f.endswith((".py", ".md"))), "ffmpeg")

SRC = os.path.join(ROOT, "videos")
TMP = os.path.join(ROOT, "build")
LIMIT = 100 * 1024 * 1024  # GitHub's hard per-file ceiling


def duration(path: str) -> float:
    r = subprocess.run([FFMPEG, "-hide_banner", "-i", path],
                       capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        raise RuntimeError(f"cannot read duration: {path}")
    h, mi, s = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(s)


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace("=", "\\=").replace(";", "\\;")\
            .replace("#", "\\#").replace("\n", "\\\n")


def build_volume(nos: list, name: str) -> dict:
    os.makedirs(TMP, exist_ok=True)
    lst = os.path.join(TMP, f"{name}.txt")
    met = os.path.join(TMP, f"{name}.meta")
    out = os.path.join(SRC, f"{name}.mp4")

    with open(lst, "w") as f:
        f.write("ffconcat version 1.0\n")
        for n in nos:
            f.write(f"file '{os.path.join(SRC, f'lecture-{n:02d}.mp4')}'\n")

    lines = [";FFMETADATA1"]
    t = 0.0
    for n in nos:
        d = json.load(open(os.path.join(ROOT, "content", f"lecture-{n:02d}.json")))
        dur = duration(os.path.join(SRC, f"lecture-{n:02d}.mp4"))
        lines += ["[CHAPTER]",
                  "TIMEBASE=1/1000",
                  f"START={int(t*1000)}",
                  f"END={int((t+dur)*1000)}",
                  f"title=Lecture {n:02d} - {esc(d['title'])}",
                  ""]
        t += dur
    open(met, "w").write("\n".join(lines))

    cmd = [FFMPEG, "-y", "-loglevel", "error", "-stats",
           "-f", "concat", "-safe", "0", "-i", lst,
           "-i", met, "-map_metadata", "1",
           "-map", "0:v", "-map", "0:a",
           "-c", "copy", "-movflags", "+faststart", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out):
        raise RuntimeError(r.stderr.strip()[-400:])

    size = os.path.getsize(out)
    return {"name": name, "out": out, "size": size,
            "hours": duration(out) / 3600, "ok": size < LIMIT}


def main() -> None:
    groups = [list(range(1, 6)), list(range(6, 11)),
              list(range(11, 16)), list(range(16, 21))]
    results = []
    for i, g in enumerate(groups, 1):
        name = f"IENRL-volume-{i}"
        r = build_volume(g, name)
        results.append(r)
        flag = "fits" if r["ok"] else "TOO BIG for GitHub"
        print(f"{name}: {r['hours']:.2f} h  {r['size']/1048576:.1f} MB  "
              f"({len(g)} lectures)  {flag}", flush=True)

    bad = [r for r in results if not r["ok"]]
    print()
    if bad:
        print(f"WARNING: {len(bad)} volume(s) exceed the 100 MB GitHub limit "
              f"and must not be pushed.")
    else:
        print(f"all {len(results)} volumes under 100 MB - safe to push")


if __name__ == "__main__":
    main()
