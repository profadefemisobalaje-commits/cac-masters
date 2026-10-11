#!/usr/bin/env python3
"""Original instrumental score, synthesized from scratch (no samples, no
third-party recordings) — fully owned and licence-clean.  (v2, low-memory)

Writes directly into a 3600 s float32 stereo mix:
  - dignified orchestral-style opening,
  - per-section contemplative beds in varied modes/tempi,
  - restrained transitional stingers at segment boundaries,
  - closing theme resolving to silence at 60:00.
"""
import json, os, wave
import numpy as np

ROOT = os.environ.get("TBUPROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
TOTAL = 3600.0
rng = np.random.default_rng(7)

Dm = [146.83, 174.61, 220.00, 293.66]
F_ = [174.61, 220.00, 261.63, 349.23]
Ad = [110.00, 130.81, 164.81, 220.00]
Gm = [98.00, 116.54, 146.83, 196.00]
C_ = [130.81, 164.81, 196.00, 261.63]
Bb = [116.54, 146.83, 174.61, 233.08]

SECTIONS = {
    "Opening": ([Dm, Bb, F_, C_], 3.2, 0.20, True),
    "1": ([F_, C_, Dm, Bb], 3.6, 0.13, False),
    "2": ([Ad, Dm, F_, C_], 3.6, 0.13, True),
    "3": ([Dm, Gm, Bb, F_], 4.0, 0.14, False),
    "4": ([Ad, F_, C_, Gm], 3.4, 0.13, True),
    "5": ([F_, Ad, Dm, C_], 3.4, 0.13, False),
    "6": ([Gm, Dm, Bb, F_], 3.8, 0.13, False),
    "7": ([Dm, F_, C_, Gm], 4.0, 0.14, False),
    "8": ([Ad, C_, F_, Dm], 3.4, 0.13, True),
    "9": ([F_, Bb, C_, Dm], 3.8, 0.14, False),
    "10": ([C_, F_, Ad, Gm], 3.4, 0.13, True),
    "11": ([Ad, Dm, F_, Bb], 3.6, 0.14, False),
    "12": ([Gm, Ad, Dm, F_], 4.2, 0.13, False),
    "13": ([F_, C_, Gm, C_], 3.0, 0.13, True),
    "14": ([Dm, F_, Bb, C_], 4.4, 0.18, True),
}


def note(freq, dur, amp=0.2, harm=(1, 0.45, 0.22, 0.12, 0.06), vib=0.006, detune=0.0):
    n = int(dur * SR)
    t = np.arange(n, dtype=np.float32) / SR
    f = np.float32(freq * (1 + detune))
    ph = 2 * np.pi * f * t
    if vib:
        ph = ph + np.float32(vib) * 2 * np.pi * np.sin(2 * np.pi * 4.7 * t) * t
    s = np.zeros(n, dtype=np.float32)
    for i, h in enumerate(harm):
        s += np.float32(h / (i + 1)) * np.sin(ph * (i + 1)).astype(np.float32)
    na = max(1, int(0.08 * SR))
    nr = max(1, int(min(0.6, dur * 0.5) * SR))
    s[:na] *= np.linspace(0, 1, na, dtype=np.float32) ** 2
    s[-nr:] *= np.linspace(1, 0, nr, dtype=np.float32) ** 1.5
    return s * np.float32(amp * 0.8)


def bell(freq, dur=2.2, amp=0.10):
    n = int(dur * SR)
    t = np.arange(n, dtype=np.float32) / SR
    s = (np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2.76 * t)
         + 0.25 * np.sin(2 * np.pi * freq * 5.4 * t)).astype(np.float32)
    return (s * np.exp(-t * 2.2) * amp).astype(np.float32)


def add(buf, sig, st_samples, gain=1.0):
    n = len(buf)
    e = min(n, st_samples + len(sig))
    if st_samples >= n or e <= st_samples:
        return
    buf[st_samples:e] += (sig[:e - st_samples] * gain).astype(np.float32)


def main():
    tl = json.load(open(os.path.join(ROOT, "out", "timeline.json"), encoding="utf-8"))
    n = int(TOTAL * SR)
    left = np.zeros(n, dtype=np.float32)
    right = np.zeros(n, dtype=np.float32)
    for seg in tl["segments"]:
        prog, beat, amp, arp = SECTIONS[seg["section"]]
        st0 = int(seg["start"] * SR)
        dur = seg["end"] - seg["start"]
        seglen = int(dur * SR)
        bar = beat * 4
        nb = max(1, int(dur / bar))
        for b in range(nb):
            ch = prog[b % len(prog)]
            bs = st0 + int(b * bar * SR)
            bl = min(int(bar * SR) + int(0.35 * SR), n - bs)
            if bl <= 0:
                continue
            for f in ch:
                s = note(f, bl / SR, amp=amp / len(ch) ** 0.5,
                         detune=(rng.random() - 0.5) * 0.004)
                add(left, s, bs, 1.0)
                add(right, s, bs + int(0.006 * SR), 0.96)
            if arp:
                for i, f in enumerate(ch):
                    off = bs + int((i + 0.5) * bar / (len(ch) + 1) * SR)
                    s = note(f * 2, bar * 0.4, amp=amp * 0.22)
                    add(left, s, off, 0.9)
                    add(right, s, off, 1.0)
        # low drone across segment
        d = note(prog[0][0] / 2, dur, amp=amp * 0.45, harm=(1, 0.3, 0.1), vib=0.0)
        add(left, d, st0)
        add(right, d, st0)
        # sparse bells
        for k in range(int(dur / 24)):
            off = st0 + int((10 + k * 24 + rng.random() * 6) * SR)
            b = bell(prog[k % len(prog)][2] * 2, amp=0.045)
            add(left, b, off, 0.8)
            add(right, b, off, 1.0)
        # transition stinger into next segment
        if seg is not tl["segments"][-1]:
            off = int((seg["end"] - 2.0) * SR)
            s = note(prog[-1][0], 5.0, amp=0.09, harm=(1, 0.4, 0.2))
            s2 = note(prog[-1][2], 5.0, amp=0.06, harm=(1, 0.4, 0.2))
            bb = bell(prog[-1][3], amp=0.05)
            add(left, s, off); add(right, s, off)
            add(left, s2, off + int(0.4 * SR)); add(right, s2, off + int(0.4 * SR))
            add(left, bb, off, 0.8); add(right, bb, off, 1.0)
    # fades
    fi = int(2 * SR)
    left[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)
    right[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)
    fo = int(6 * SR)
    w = (np.linspace(1, 0, fo, dtype=np.float32) ** 1.7)
    left[-fo:] *= w
    right[-fo:] *= w
    peak = max(np.abs(left).max(), np.abs(right).max()) or 1.0
    g = np.float32(0.5 / peak)
    with wave.open(os.path.join(ROOT, "out", "audio", "score.wav"), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        B = 4_000_000
        for i in range(0, n, B):
            j = min(n, i + B)
            blk = np.empty((j - i, 2), dtype=np.float32)
            blk[:, 0] = left[i:j] * g
            blk[:, 1] = right[i:j] * g
            w.writeframes((blk * 32767).astype("<i2").tobytes())
            del blk
    del left, right
    print(f"score.wav written: {TOTAL:.0f}s stereo, peak-normalized to 0.5")


if __name__ == "__main__":
    main()
