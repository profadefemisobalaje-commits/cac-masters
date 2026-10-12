"""
compact.py — Build the download edition of the lectures.

    python tools/compact.py            # videos/hd/*.mp4 -> videos/*.mp4
    python tools/compact.py 3 7        # only those lectures

The master files are 30 minutes of slide stills encoded at 24 fps. Two facts
make them about three times larger than they need to be for download:

  * the picture barely changes, so 24 fps is 24 copies of the same frame —
    1 fps is informationally lossless here and cuts the video stream ~88%;
  * the AAC audio is 128 kbps mono, which is ~29 MB of a 53 MB file. At
    64 kbps mono it halves with no perceptible loss on speech.

Resolution is deliberately left at 1920x1080: after the frame-rate change the
video stream is only a few megabytes, so there is nothing to gain by
downscaling and a lot to lose in text legibility.

The masters are kept in videos/hd/. Subtitles and metadata are carried over.

Courtesy: Triune Biblical University Global Extension, USA.
"""

from __future__ import annotations

import glob
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BIN = glob.glob(os.path.join(ROOT, "venv", "lib", "python3.11",
                             "site-packages", "imageio_ffmpeg", "binaries",
                             "ffmpeg-*"))
FFMPEG = next((f for f in BIN if not f.endswith((".py", ".md"))), "ffmpeg")

SRC = os.path.join(ROOT, "videos", "hd")
DST = os.path.join(ROOT, "videos")

FPS = 1
CRF = "26"
ABR = "64k"


def encode(no: int) -> tuple:
    src = os.path.join(SRC, f"lecture-{no:02d}.mp4")
    dst = os.path.join(DST, f"lecture-{no:02d}.mp4")
    if not os.path.exists(src):
        return (no, None, "missing master")
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return (no, os.path.getsize(dst), "already current")

    cmd = [
        FFMPEG, "-y", "-loglevel", "error", "-stats", "-i", src,
        "-map", "0:v", "-map", "0:a", "-map", "0:s",
        "-vf", f"fps={FPS}",
        "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage",
        "-crf", CRF, "-pix_fmt", "yuv420p",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:a", "aac", "-b:a", ABR, "-ac", "1", "-ar", "44100",
        "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
        "-movflags", "+faststart",
        dst,
    ]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(dst):
        return (no, None, r.stderr.strip()[-300:])
    return (no, os.path.getsize(dst), f"{time.time()-t0:.0f}s")


def main() -> None:
    args = [int(a) for a in sys.argv[1:] if a.isdigit()]
    nos = args or list(range(1, 21))
    total_in = total_out = 0
    for n in nos:
        no, size, note = encode(n)
        if size is None:
            print(f"L{no:02d}  FAILED  {note}", flush=True)
            continue
        src = os.path.join(SRC, f"lecture-{no:02d}.mp4")
        sin = os.path.getsize(src) if os.path.exists(src) else 0
        total_in += sin
        total_out += size
        print(f"L{no:02d}  {sin/1048576:6.1f} MB -> {size/1048576:6.1f} MB  "
              f"({100*size/sin:.0f}%)  {note}", flush=True)
    if total_in:
        print(f"\ntotal {total_in/1048576:.0f} MB -> {total_out/1048576:.0f} MB  "
              f"({100*total_out/total_in:.0f}%)", flush=True)


if __name__ == "__main__":
    main()
