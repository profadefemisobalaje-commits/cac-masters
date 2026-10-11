#!/usr/bin/env python3
"""Assemble narration+score mix from out/timeline.json (float32, low-memory).

 1. decode each recorded chunk to mono 44.1 kHz PCM;
 2. place at its timeline offset in a 3600 s buffer;
 3. loudness-normalize narration to -16 LUFS (podcast standard);
 4. add the original score bed well below speech so narration dominates;
 5. write out/audio/mix.wav (stereo).
"""
import json, os, subprocess, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
FF = subprocess.run([sys.executable, "-c",
                     "import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())"],
                    capture_output=True, text=True).stdout.strip()


def decode(path):
    tmp = path + ".pcm.wav"
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", path,
                    "-ac", "1", "-ar", str(SR), tmp], check=True)
    with wave.open(tmp) as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
    os.remove(tmp)
    return data.astype(np.float32) / 32768.0


def read_wav(path):
    with wave.open(path) as w:
        n = w.getnframes(); ch = w.getnchannels()
        d = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float32) / 32768.0
    return d.reshape(-1, ch) if ch == 2 else d


def main():
    tl = json.load(open(os.path.join(ROOT, "out", "timeline.json"), encoding="utf-8"))
    total = int(tl["total"] * SR)
    buf = np.zeros(total, dtype=np.float32)
    for c in tl["chunks"]:
        d = decode(os.path.join(ROOT, c["file"]))
        st = int(c["offset"] * SR)
        en = min(total, st + len(d))
        buf[st:en] += d[:en - st]
    raw = os.path.join(ROOT, "out", "audio", "narration_raw.wav")
    with wave.open(raw, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((buf * 32767).astype("<i2").tobytes())
    del buf
    norm = os.path.join(ROOT, "out", "audio", "narration_norm.wav")
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", raw,
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), norm],
                   check=True)
    narr = read_wav(norm)
    score_path = os.path.join(ROOT, "out", "audio", "score.wav")
    if os.path.exists(score_path):
        sc = read_wav(score_path)[:len(narr)]
        if len(sc) < len(narr):
            sc = np.vstack([sc, np.zeros((len(narr) - len(sc), 2), np.float32)])
        m = sc.mean(axis=1) * 0.30      # duck: speech dominates
        del sc
        left = narr + m
        right = narr + np.roll(m, 480)  # slight width
        del m
    else:
        left = right = narr
    mix = os.path.join(ROOT, "out", "audio", "mix.wav")
    with wave.open(mix, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        B = 4_000_000
        for i in range(0, len(left), B):
            j = min(len(left), i + B)
            blk = np.empty((j - i, 2), dtype=np.float32)
            blk[:, 0] = np.tanh(left[i:j] * 1.05) * 0.95
            blk[:, 1] = np.tanh(right[i:j] * 1.05) * 0.95
            w.writeframes((blk * 32767).astype("<i2").tobytes())
            del blk
    del left, right
    print(f"mix.wav written: {len(narr)/SR:.1f}s stereo")


if __name__ == "__main__":
    main()
