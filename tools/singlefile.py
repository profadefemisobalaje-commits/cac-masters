"""
singlefile.py — The whole course as one MP4 that GitHub will accept.

    python tools/singlefile.py        # -> videos/IENRL-complete-course-single.mp4

GitHub refuses any file above 100 MB, so the 352 MB stream-copy version
(IENRL-complete-course.mp4) can only ever live in the workspace. This builds a
deliberately lean edition that fits, by spending the bitrate where it matters:

  * 1 fps — the picture is a slide that changes every few minutes, so 24 fps
    (or even 2 fps) is duplicated frames. This costs nothing perceptually.
  * 720p rather than 1080p — at 1 fps the video is a small share of the file,
    but halving it frees roughly 40 MB for audio, which is what actually
    carries a lecture.
  * ~16 kbps mono at 22.05 kHz — speech remains entirely intelligible; the
    96 kbps full-quality audio is what pushes the master past the limit.

Chapters are preserved so the ten-hour file stays navigable.

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
OUT = os.path.join(SRC, "IENRL-complete-course-single.mp4")
LIMIT = 100 * 1024 * 1024

WIDTH, HEIGHT = 1280, 720
FPS = 1
VCRF = "38"
ABR = "14k"
AR = "22050"


def duration(path: str) -> float:
    r = subprocess.run([FFMPEG, "-hide_banner", "-i", path],
                       capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        raise RuntimeError(f"cannot read duration: {path}")
    h, mi, s = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(s)


def esc(s: str) -> str:
    return (s.replace("\\", "\\\\").replace("=", "\\=")
             .replace(";", "\\;").replace("#", "\\#").replace("\n", "\\\n"))


def main() -> None:
    os.makedirs(TMP, exist_ok=True)
    lst = os.path.join(TMP, "single.txt")
    met = os.path.join(TMP, "single.meta")

    with open(lst, "w") as f:
        f.write("ffconcat version 1.0\n")
        for n in range(1, 21):
            f.write(f"file '{os.path.join(SRC, f'lecture-{n:02d}.mp4')}'\n")

    lines = [";FFMETADATA1"]
    t = 0.0
    for n in range(1, 21):
        d = json.load(open(os.path.join(ROOT, "content", f"lecture-{n:02d}.json")))
        dur = duration(os.path.join(SRC, f"lecture-{n:02d}.mp4"))
        lines += ["[CHAPTER]", "TIMEBASE=1/1000",
                  f"START={int(t*1000)}", f"END={int((t+dur)*1000)}",
                  f"title=Lecture {n:02d} - {esc(d['title'])}", ""]
        t += dur
    open(met, "w").write("\n".join(lines))

    cmd = [
        FFMPEG, "-y", "-loglevel", "error", "-stats",
        "-f", "concat", "-safe", "0", "-i", lst,
        "-i", met, "-map_metadata", "1",
        "-map", "0:v", "-map", "0:a", "-map", "0:s",
        "-vf", f"fps={FPS},scale={WIDTH}:{HEIGHT}",
        "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage",
        "-crf", VCRF, "-pix_fmt", "yuv420p",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:a", "aac", "-b:a", ABR, "-ac", "1", "-ar", AR,
        "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
        "-movflags", "+faststart",
        "-metadata", "title=International Energy and Natural Resources Law - "
                     "complete course",
        "-metadata", "artist=Prof. Williams",
        "-metadata", "album=TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA",
        OUT,
    ]
    print(f"encoding 20 lectures -> {OUT}", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(OUT):
        raise SystemExit(r.stderr.strip()[-500:])

    size = os.path.getsize(OUT)
    hrs = duration(OUT) / 3600
    print(f"\ndone: {size/1048576:.1f} MB  {hrs:.2f} hours  "
          f"({100*size/LIMIT:.0f}% of the GitHub limit)", flush=True)
    print("SAFE TO PUSH" if size < LIMIT else "TOO BIG - do not push")


if __name__ == "__main__":
    main()
