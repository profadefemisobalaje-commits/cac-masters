"""
pipeline.py — End-to-end lecture production line.

    content/lecture-NN.json
        -> slides/lecture-NN/*.png      (broadcast 1920x1080 stills)
        -> build/lecture-NN/            (per-slide + master audio, .srt)
        -> dist/lecture-NN.mp4          (30:00 lecture, soft subtitles)
        -> lectures/lecture-NN.md       (reading companion / full script)

Duration is calibrated automatically: narration is synthesised sentence by
sentence, the speaking rate is adjusted once if necessary, and the remaining
time is distributed across inter-sentence breaths and inter-slide pauses so
that every lecture lands on its 30-minute target.

Courtesy: Triune Biblical University Global Extension, USA.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import slides as S  # noqa: E402
from tts import PiperVoice, write_wav  # noqa: E402

TARGET = 1800.0          # 30 minutes
BUMPER_S = 5.0           # branded bumper, silent
END_HOLD = 7.0           # hold on the end card after the last words
FPS = 24

FFMPEG = os.path.join(ROOT, ".venv", "lib", "python3.11", "site-packages",
                      "imageio_ffmpeg", "binaries")
FFMPEG = next((os.path.join(FFMPEG, f) for f in os.listdir(FFMPEG)
               if f.startswith("ffmpeg-")), "ffmpeg") if os.path.isdir(FFMPEG) else "ffmpeg"


# --------------------------------------------------------------------------
# Sentence splitting
# --------------------------------------------------------------------------

_ABBR = (r"(?<!\bMr)(?<!\bMrs)(?<!\bDr)(?<!\bSt)(?<!\bNo)(?<!\bArt)(?<!\bpara)"
         r"(?<!\be\.g)(?<!\bi\.e)(?<!\betc)(?<!\bcf)(?<!\bG\.A)(?<!\bI\.C\.J)"
         r"(?<!\bU\.N)(?<!\bU\.S)(?<!\bE\.U)(?<!\bvs)(?<!\bVol)(?<!\bpp)(?<!\bp)")


def split_sentences(text: str) -> list:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        return []
    parts = re.split(rf"{_ABBR}(?<=[.!?])\s+(?=[\"'\u201cA-Z(])", text)
    out, buf = [], ""
    for p in parts:
        if len(p) < 22 and buf:
            buf += " " + p
        else:
            if buf:
                out.append(buf)
            buf = p
    if buf:
        out.append(buf)
    return out


# --------------------------------------------------------------------------
# Narration
# --------------------------------------------------------------------------


class Narrator:
    def __init__(self):
        self.v = PiperVoice()
        self.sr = self.v.sample_rate
        self.cache: dict = {}

    def synth(self, text: str, length_scale: float) -> list:
        """Return [(np.ndarray audio, str display_text), ...] per sentence.

        Each sentence is phonemised on its own so that the *original* wording
        stays paired with its audio — needed for readable subtitles.
        """
        out = []
        for display in split_sentences(text):
            key = (display, round(length_scale, 3))
            if key not in self.cache:
                parts = [self.v.speak_sentence(p, length_scale=length_scale)
                         for p in self.v.sentences(display)]
                self.cache[key] = (np.concatenate(parts)
                                   if parts else np.zeros(0, np.float32))
            out.append((self.cache[key], display))
        return out


# --------------------------------------------------------------------------
# Subtitles
# --------------------------------------------------------------------------


def _chunks(text: str, n: int = 78) -> list:
    words = text.split()
    out, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


def fmt_ts(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------


def build(lecture: dict, workdir: str, keep_wav: bool = False,
          verbose: bool = True) -> dict:
    no = lecture["no"]
    ldir = os.path.join(ROOT, "slides", f"lecture-{no:02d}")
    bdir = os.path.join(ROOT, "build", f"lecture-{no:02d}")
    os.makedirs(ldir, exist_ok=True)
    os.makedirs(bdir, exist_ok=True)

    nar = Narrator()
    sr = nar.sr
    items = lecture["slides"]

    def log(*a):
        if verbose:
            print(f"  [L{no:02d}]", *a, flush=True)

    # ---- 1. synthesise at the base rate, then calibrate -------------------
    ls = 1.18
    for attempt in range(3):
        audio = []          # per slide: list of (array, text)
        for sl in items:
            audio.append(nar.synth(sl.get("narration", ""), ls))
        speech = sum(float(len(a) / sr) for sl in audio for a, _ in sl)
        n_sent = sum(len(sl) for sl in audio)
        n_gaps = max(0, n_sent - len(items))
        n_pause = len(items)
        budget = TARGET - BUMPER_S - END_HOLD
        slack = budget - speech

        nominal = n_gaps * 0.34 + n_pause * 1.00
        hi = n_gaps * 0.55 + n_pause * 3.40
        lo = n_gaps * 0.22 + n_pause * 0.50
        if lo <= slack <= hi:
            break
        want = budget - (n_gaps * 0.40 + n_pause * 1.60)
        ls = round(ls * (want / max(speech, 1.0)), 3)
        ls = float(np.clip(ls, 1.02, 1.50))
        log(f"recalibrating speaking rate -> length_scale={ls}")
    else:
        log("note: rate settled at length_scale="
            f"{ls} ({sum(len(s.get('narration','').split()) for s in items)} words)")

    # ---- 2. solve the pause budget ----------------------------------------
    CAP = 5.50  # a long pause between slides is far better than draggy speech
    sent_gap = 0.34
    slide_pause = (slack - n_gaps * sent_gap) / max(n_pause, 1)
    if slide_pause > CAP:
        slide_pause = CAP
        sent_gap = (slack - n_pause * slide_pause) / max(n_gaps, 1)
    elif slide_pause < 0.50:
        slide_pause = 0.50
        sent_gap = (slack - n_pause * slide_pause) / max(n_gaps, 1)
    sent_gap = float(np.clip(sent_gap, 0.16, 1.40))

    # ---- 3. assemble audio, derive slide durations, render slides ---------
    track = [np.zeros(int(BUMPER_S * sr), dtype=np.float32)]
    timeline = [("bumper", 0.0, BUMPER_S)]
    t = BUMPER_S
    total = len(items)
    subs, entries, srt_i = [], [], 1

    for i, sl in enumerate(items):
        segs, durs = [], []
        for arr, _ in audio[i]:
            segs.append(arr)
            segs.append(np.zeros(int(sent_gap * sr), dtype=np.float32))
            durs.append(float(len(arr) / sr))
        if segs:
            segs.pop()  # trailing gap belongs to the slide pause
        body = np.concatenate(segs) if segs else np.zeros(0, np.float32)
        spoken = float(len(body) / sr)
        if sl["type"] == "end":
            pause = END_HOLD
        elif sl["type"] == "bumper":
            pause = BUMPER_S
        else:
            pause = slide_pause
        dur = spoken + pause
        track.append(body)
        track.append(np.zeros(int(pause * sr), dtype=np.float32))

        # subtitles: distribute chunks across the spoken span
        display = [txt for _, txt in audio[i]] if audio[i] else []
        spans, run = [], 0.0
        for arr, _ in audio[i]:
            spans.append(float(len(arr) / sr))
        tot_sp = sum(spans) or 1.0
        cursor = t
        for k, (arr, txt) in enumerate(audio[i]):
            share = (spans[k] / tot_sp) * spoken
            cs = _chunks(txt)
            if cs:
                step = share / len(cs)
                for c in cs:
                    subs.append((srt_i, cursor, cursor + step, c))
                    srt_i += 1
                    cursor += step
            cursor += sent_gap
        t += dur
        timeline.append((sl["type"], t - dur, dur))

        ctx = {"lecture_no": no, "idx": i + 1, "total": total,
               "progress": (i + 1) / total,
               "objectives": lecture.get("objectives", [])}
        img = S.render(sl, ctx)
        p = os.path.join(ldir, f"{i:02d}_{sl['type']}.png")
        img.save(p, optimize=True)
        entries.append(p)
        log(f"slide {i+1:02d}/{total} {sl['type']:<10} {dur:7.2f}s")

    total_dur = t

    # ---- 4. write assets ---------------------------------------------------
    full = np.concatenate(track)
    wav = os.path.join(bdir, "narration.wav")
    write_wav(wav, full, sr)

    # A closing cue keeps -shortest from truncating the video on the subtitle
    # track, which would otherwise end with the last spoken sentence.
    subs.append((len(subs) + 1, max(0.0, t - 3.0), t + 30.0, "[End of lecture]"))
    srt = os.path.join(bdir, "lecture.srt")
    with open(srt, "w", encoding="utf-8") as f:
        for i, a, b, c in subs:
            f.write(f"{i}\n{fmt_ts(a)} --> {fmt_ts(b)}\n{c}\n\n")

    # The concat demuxer needs the final file repeated to signal the end; give
    # that repeat a negligible duration so it does not extend the lecture.
    lst = os.path.join(bdir, "list.txt")
    with open(lst, "w", encoding="utf-8") as f:
        f.write("ffconcat version 1.0\n")
        for p, (typ, st, dd) in zip(entries, timeline[1:]):
            f.write(f"file '{p}'\nduration {dd:.3f}\n")
        f.write(f"file '{entries[-1]}'\nduration 0.040\n")
        f.write(f"file '{entries[-1]}'\n")

    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    out = os.path.join(ROOT, "dist", f"lecture-{no:02d}.mp4")
    title = f"Lecture {no:02d} — {lecture['title']}"
    cmd = [
        FFMPEG, "-y", "-loglevel", "error", "-stats",
        "-f", "concat", "-safe", "0", "-i", lst,
        "-i", wav, "-i", srt,
        "-map", "0:v", "-map", "1:a", "-map", "2:s",
        "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
        "-crf", "23", "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:a", "aac", "-b:a", "128k", "-ac", "1", "-ar", "44100",
        "-c:s", "mov_text",
        "-movflags", "+faststart",
        "-metadata", f"title={title}",
        "-metadata", f"artist={S.LECTURER}",
        "-metadata", f"album={S.SERIES}",
        "-metadata", f"album_artist={S.UNIVERSITY}",
        "-metadata:s:s:0", "language=eng",
        "-shortest", out,
    ]
    log("encoding video...")
    t0 = time.time()
    import subprocess
    rc = subprocess.run(cmd, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL).returncode
    if rc != 0:
        raise RuntimeError(f"ffmpeg failed ({rc}) for lecture {no}")
    log(f"encoded in {time.time()-t0:.0f}s -> {out}")

    if not keep_wav:
        os.remove(wav)

    return {
        "no": no, "title": lecture["title"], "duration": total_dur,
        "slides": total, "subtitles": len(subs),
        "words": sum(len(sl.get("narration", "").split()) for sl in items),
        "length_scale": ls, "sent_gap": sent_gap, "slide_pause": slide_pause,
        "mp4": out, "size_mb": os.path.getsize(out) / 1e6,
    }


# --------------------------------------------------------------------------
# Reading companion
# --------------------------------------------------------------------------


def write_markdown(lecture: dict, timing: dict) -> str:
    no = lecture["no"]
    os.makedirs(os.path.join(ROOT, "lectures"), exist_ok=True)
    p = os.path.join(ROOT, "lectures", f"lecture-{no:02d}.md")
    L = []
    A = L.append
    A(f"# Lecture {no:02d} — {lecture['title']}")
    A("")
    A(f"**{lecture['subtitle']}**")
    A("")
    A(f"> **Series:** {S.SERIES}  ")
    A(f"> **Module:** {lecture['module']}  ")
    A(f"> **Lecturer:** {S.LECTURER}, {S.UNIVERSITY}  ")
    A(f"> **Duration:** 30 minutes · **Slides:** {timing['slides']} · "
      f"**Narration:** {timing['words']:,} words  ")
    A(f"> **Video:** `dist/lecture-{no:02d}.mp4`")
    A("")
    A("---")
    A("")
    A("## Learning Outcomes")
    A("")
    for i, o in enumerate(lecture["objectives"], 1):
        A(f"{i}. {o}")
    A("")
    A("## Lecture Script")
    A("")
    clock = 0.0
    for i, sl in enumerate(lecture["slides"]):
        t = sl["type"]
        title = sl.get("title") or sl.get("case") or sl.get("quote", "")[:80]
        A(f"### {i+1:02d}. {title} `{t}`")
        A("")
        if t == "objectives":
            for o in sl.get("items", []):
                A(f"- {o}")
            A("")
        if t == "bullets":
            for it in sl.get("items", []):
                A(f"- {it}")
            A("")
        if t == "two-col":
            A(f"**{sl['left_h']}**")
            for it in sl["left"]:
                A(f"- {it}")
            A("")
            A(f"**{sl['right_h']}**")
            for it in sl["right"]:
                A(f"- {it}")
            A("")
        if t == "levels":
            A("**Undergraduate level**")
            for it in sl["ug"]:
                A(f"- {it}")
            A("")
            A("**Postgraduate level**")
            for it in sl["pg"]:
                A(f"- {it}")
            A("")
        if t == "timeline":
            for yr, ev in sl.get("events", []):
                A(f"- **{yr}** — {ev}")
            A("")
        if t == "diagram":
            for nd in sl.get("nodes", []):
                A(f"- {nd}")
            A("")
        if t == "case":
            A(f"*{sl['case']}*")
            A("")
            A(sl["body"])
            A("")
            if sl.get("holding"):
                A(f"> **Holding / significance.** {sl['holding']}")
                A("")
        if t == "quote":
            A(f"> {sl['quote']}")
            A(">")
            A(f"> — {sl['attribution']}")
            A("")
        if t == "summary":
            for pt in sl.get("points", []):
                A(f"- {pt}")
            A("")
            A(f"> **The one thing to remember.** {sl['takeaway']}")
            A("")
        if sl.get("note"):
            A(f"*On-screen note:* {sl['note']}")
            A("")
        if sl.get("narration"):
            A("**Narration**")
            A("")
            for para in sl["narration"].split("\n"):
                A(para)
            A("")
    A("## Required and Recommended Reading")
    A("")
    for r in lecture["readings"]:
        A(f"- {r}")
    A("")
    A("## Self-Test")
    A("")
    for k, q in enumerate(lecture["quiz"], 1):
        A(f"{k}. {q['q']}")
        for j, o in enumerate(q["options"]):
            mark = " ✓" if j == q["answer"] else ""
            A(f"    {'abcdefghij'[j]}) {o}{mark}")
        A("")
        A(f"   *{q['explain']}*")
        A("")
    A("---")
    A("")
    A(f"*{S.UNIVERSITY} · {S.COURSE} · Delivered by {S.LECTURER}*")
    A("")
    open(p, "w", encoding="utf-8").write("\n".join(L))
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lectures", nargs="*", help="lecture numbers; default = all")
    ap.add_argument("--keep-wav", action="store_true")
    ap.add_argument("--no-md", action="store_true")
    a = ap.parse_args()

    files = sorted(__import__("glob").glob(os.path.join(ROOT, "content", "lecture-*.json")))
    wanted = set(int(x) for x in a.lectures) if a.lectures else None
    results = []
    for f in files:
        lec = json.load(open(f, encoding="utf-8"))
        if wanted is not None and lec["no"] not in wanted:
            continue
        out_mp4 = os.path.join(ROOT, "dist", f"lecture-{lec['no']:02d}.mp4")
        if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 10 * 1024 * 1024:
            print(f"\n=== Lecture {lec['no']:02d}: {lec['title']} — already rendered, "
                  f"skipping ===", flush=True)
            continue
        print(f"\n=== Lecture {lec['no']:02d}: {lec['title']} ===", flush=True)
        t0 = time.time()
        timing = build(lec, ROOT, keep_wav=a.keep_wav)
        if not a.no_md:
            write_markdown(lec, timing)
        timing["wall"] = time.time() - t0
        results.append(timing)
        print(f"  -> {timing['duration']/60:.2f} min | {timing['size_mb']:.0f} MB | "
              f"{timing['words']} words | ls={timing['length_scale']} | "
              f"{timing['wall']:.0f}s wall", flush=True)

    if results:
        os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
        json.dump(results, open(os.path.join(ROOT, "build", "manifest.json"), "w"), indent=2)
        print("\nSUMMARY")
        for r in results:
            print(f"  L{r['no']:02d}  {r['duration']/60:5.2f} min  "
                  f"{r['words']:5d} words  {r['size_mb']:6.1f} MB  {r['slides']:2d} slides")


if __name__ == "__main__":
    main()
