#!/usr/bin/env python3
"""Assemble the final MP4 from slides + mix.wav.

 1. build 2048x1152 JPEG proxies of the 4K slides (zoom headroom, fast encode);
 2. per scene: slow cinematic push-in via zoompan at 1920x1080/30fps;
 3. concat segments (stream copy);
 4. mux with out/audio/mix.wav -> out/video/final_1080p.mp4, cut at 3600.0 s.
Run in background: ~15-40 min on 2 cores.
"""
import json, os, subprocess, sys

ROOT = os.environ.get("TBUPROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
FF = subprocess.run([PY, "-c", "import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())"],
                    capture_output=True, text=True).stdout.strip()
SLIDES = os.path.join(ROOT, "out", "slides")
PROXY = os.path.join(ROOT, "out", "proxies")
SEGDIR = os.path.join(ROOT, "out", "segs")
VID = os.path.join(ROOT, "out", "video")
for d in (PROXY, SEGDIR, VID):
    os.makedirs(d, exist_ok=True)
FPS = 30


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        raise SystemExit(f"failed: {' '.join(cmd[:8])}")


def main():
    tl = json.load(open(os.path.join(ROOT, "out", "timeline.json"), encoding="utf-8"))
    scenes = tl["scenes"]
    # 1. proxies
    from PIL import Image
    for s in scenes:
        p = os.path.join(PROXY, f"p_{s['slide']:03d}.jpg")
        if not os.path.exists(p):
            im = Image.open(os.path.join(SLIDES, f"slide_{s['slide']:03d}.png"))
            im = im.resize((2048, 1152), Image.LANCZOS)
            im.save(p, quality=90)
    print(f"proxies ready ({len(scenes)})")
    # 2. per-scene encode with slow push-in
    for i, s in enumerate(scenes):
        dur = s["end"] - s["start"]
        frames = max(1, int(round(dur * FPS)))
        out = os.path.join(SEGDIR, f"seg_{i:03d}.mp4")
        if os.path.exists(out) and abs(os.path.getmtime(out) - 0) > 0 and os.path.getsize(out) > 10000:
            continue
        run([FF, "-y", "-hide_banner", "-loglevel", "error",
             "-i", os.path.join(PROXY, f"p_{s['slide']:03d}.jpg"),
             "-vf", (f"zoompan=z='min(1.0+0.03*on/{frames},1.03)':"
                     f"d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                     f"s=1920x1080:fps={FPS},format=yuv420p"),
             "-frames:v", str(frames),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
             "-g", "300", "-an", out])
        if i % 10 == 0:
            print(f"  encoded {i+1}/{len(scenes)}")
    # 3. concat
    lst = os.path.join(SEGDIR, "list.txt")
    with open(lst, "w") as f:
        for i in range(len(scenes)):
            f.write(f"file 'seg_{i:03d}.mp4'\n")
    silent = os.path.join(VID, "video_silent.mp4")
    run([FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat",
         "-safe", "0", "-i", lst, "-c", "copy", silent])
    # 4. mux
    final = os.path.join(VID, "final_1080p.mp4")
    run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", silent,
         "-i", os.path.join(ROOT, "out", "audio", "mix.wav"),
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-t", "3600", "-movflags", "+faststart", final])
    print(f"FINAL: {final}")


if __name__ == "__main__":
    main()
