"""Assemble slide images + narration audio into an MP4 lecture video.

Pipeline:  slides.png  +  audio.mp3  ->  {slug}.mp4  (1920x1080, H.264, AAC)
Also writes a WebVTT subtitle file and a timed transcript.
"""
from __future__ import annotations
import json
import os
import subprocess
import wave
from dataclasses import dataclass, field, asdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FFMPEG = os.path.join(ROOT, "tools", "bin", "ffmpeg")
FFPROBE = os.path.join(ROOT, "tools", "bin", "ffprobe")

FPS = 15           # slide content is static, so 15 fps is visually identical to 30
                   # and cuts encode time by ~4x. Keyframes are frequent for seeking.
GOP = 150          # 10 seconds at 15 fps
VIDEO_CODEC = ["-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
               "-crf", "22", "-pix_fmt", "yuv420p"]
AUDIO_CODEC = ["-c:a", "aac", "-b:a", "96k", "-ar", "44100", "-ac", "1"]
PEAK_CEILING = 0.794   # limiter target: AAC overshoots sample peaks by ~0.6 dB,
                       # so this lands the encoded master near -1.6 dBFS


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"cmd failed ({r.returncode}): {' '.join(cmd)}\n{r.stderr[-3000:]}")
    return r


_DUR_RE = None


def duration(path: str) -> float:
    """Media duration in seconds.

    ffprobe is not shipped with the static ffmpeg build, so we read the
    Duration line ffmpeg prints while probing the container, and fall back to
    a byte-exact WAV header read when ffmpeg's line is missing.
    """
    global _DUR_RE
    if _DUR_RE is None:
        import re
        _DUR_RE = re.compile(r"Duration:\s*(\d+):(\d\d):(\d\d(?:\.\d+)?)")
    r = subprocess.run([FFMPEG, "-hide_banner", "-i", path],
                       capture_output=True, text=True)
    m = _DUR_RE.search(r.stderr)
    if m:
        h, mi, s = m.groups()
        return int(h) * 3600 + int(mi) * 60 + float(s)
    if path.lower().endswith(".wav"):
        with wave.open(path, "rb") as w:
            return w.getnframes() / float(w.getframerate())
    raise RuntimeError(f"could not determine duration of {path}")


@dataclass
class Segment:
    """One slide plus the narration that plays over it."""
    index: int
    layout: str
    image: str
    audio: str
    text: str = ""
    pad_lead: float = 0.6      # silence before speech on this slide
    pad_tail: float = 1.2      # silence after speech before cutting
    duration: float = 0.0      # filled in at build time

    @property
    def total(self) -> float:
        return self.duration + self.pad_lead + self.pad_tail


def _fmt_ts(t: float) -> str:
    """Format seconds as HH:MM:SS.mmm.

    Round to whole milliseconds *before* splitting into fields: otherwise a
    value like 2099.9999999 yields second 59.9999, which formats as an invalid
    '60.000' and rolls the minute over wrongly.
    """
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def write_vtt(segments: list[Segment], path: str, wrap_at: int = 62, tempo: float = 1.0):
    """One cue per slide covering its full on-screen time.

    `tempo` must be the same value the video was built with: the on-screen
    duration of a slide is `audio_duration / tempo + padding`, so omitting the
    tempo factor makes every cue drift progressively earlier than the picture.
    """
    out, t = ["WEBVTT", ""], 0.0
    for i, seg in enumerate(segments, 1):
        start, end = t, t + seg.duration / tempo + seg.pad_lead + seg.pad_tail
        out.append(str(i))
        out.append(f"{_fmt_ts(start)} --> {_fmt_ts(end)}")
        words, line, lines = seg.text.split(), "", []
        for w in words:
            if len(line) + len(w) + 1 > wrap_at:
                lines.append(line); line = w
            else:
                line = f"{line} {w}".strip()
        if line:
            lines.append(line)
        out.extend(lines)
        out.append("")
        t = end
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))


def write_transcript(segments: list[Segment], path: str, title: str = "",
                     tempo: float = 1.0):
    """Write the readable transcript with per-slide markers and durations."""
    with open(path, "w", encoding="utf-8") as f:
        if title:
            f.write(f"{title}\n{'=' * len(title)}\n\n")
        for s in segments:
            d = s.duration / tempo + s.pad_lead + s.pad_tail
            f.write(f"[slide {s.index:02d} · {s.layout} · {d:.1f}s]\n{s.text}\n\n")


def build_video(segments: list[Segment], out_mp4: str, workdir: str,
                transcript_path: str | None = None, vtt_path: str | None = None,
                title: str = "", target_duration: float | None = None,
                min_tempo: float = 0.85, max_tempo: float = 1.06) -> dict:
    """Concat slide+audio segments into a single MP4. Returns build metadata.

    If `target_duration` is given (e.g. 2100 for a 35-minute lecture) the
    narration is time-stretched with a single uniform tempo factor so the
    finished video lands on the target. Slowing speech slightly also makes the
    delivery sit closer to a natural lecture pace.
    """
    os.makedirs(workdir, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(out_mp4)) or ".", exist_ok=True)
    for f in os.listdir(workdir):
        if f.endswith((".mp4", ".m4a", ".wav", ".txt")):
            try: os.remove(os.path.join(workdir, f))
            except OSError: pass

    # 0. measure, then decide a single tempo factor for the whole lecture
    for seg in segments:
        seg.duration = duration(seg.audio)
    padding = sum(s.pad_lead + s.pad_tail for s in segments)
    speech = sum(s.duration for s in segments)
    tempo, tempo_note = 1.0, ""
    if target_duration:
        budget = target_duration - padding
        if speech > 0:
            wanted = speech / budget
            if wanted < min_tempo:
                tempo_note = (f"narration is {speech:.0f}s but budget is {budget:.0f}s; "
                              f"clamping tempo to {min_tempo} — extend the narration")
                tempo = min_tempo
            elif wanted < 0.995:
                tempo = wanted
                tempo_note = f"slowed to {tempo:.3f} to reach {target_duration/60:.1f} min"
            elif wanted > 1.005 and wanted <= max_tempo:
                tempo = wanted
                tempo_note = (f"sped up to {tempo:.3f} to reach "
                              f"{target_duration/60:.1f} min exactly")
            elif wanted > max_tempo:
                tempo_note = (f"narration is {speech:.0f}s but budget is {budget:.0f}s; "
                              f"over target by {speech-budget:.0f}s and speeding up "
                              f"{wanted:.2f}x would sound rushed — trim the narration")

    # 1. per-segment assets. Audio goes through a LOSSLESS intermediate (WAV):
    #    padding and tempo-shifting are done once in PCM, and the whole lecture's
    #    audio is encoded to AAC exactly once at the end. Encoding per segment
    #    and again at concat put the audio through three lossy generations,
    #    which compounds inter-sample overshoot (peaks crept from -0.7 dBFS in
    #    the source up to -0.002 dBFS) and degrades quality for no benefit.
    audio_parts, video_parts = [], []
    for seg in segments:
        filters = []
        if abs(tempo - 1.0) > 0.004:
            filters.append(f"atempo={tempo:.5f}")
        d = seg.duration / tempo
        filters.append(f"adelay={int(seg.pad_lead*1000)}|{int(seg.pad_lead*1000)}")
        filters.append(f"apad=pad_dur={seg.pad_tail}")
        total = d + seg.pad_lead + seg.pad_tail

        wav = os.path.join(workdir, f"a{seg.index:03d}.wav")
        run([FFMPEG, "-y", "-v", "error", "-i", seg.audio,
             "-af", ",".join(filters), "-t", f"{total:.3f}",
             "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "1", wav])
        audio_parts.append(wav)

        # video-only segment; MPEG-TS is unusable here because this static
        # ffmpeg build segfaults reading it
        part = os.path.join(workdir, f"v{seg.index:03d}.mp4")
        run([FFMPEG, "-y", "-v", "error",
             "-loop", "1", "-framerate", "1", "-i", seg.image,
             "-vf", f"fps={FPS},scale=1920:1080,format=yuv420p",
             "-t", f"{total:.3f}",
             "-r", str(FPS), "-fps_mode", "cfr", "-an",
             *VIDEO_CODEC, "-g", str(GOP),
             "-video_track_timescale", "90000",
             part])
        video_parts.append(part)

    # 2. concatenate the video streams losslessly
    vlist = os.path.join(workdir, "vconcat.txt")
    with open(vlist, "w") as f:
        for p in video_parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    joined_v = os.path.join(workdir, "joined_video.mp4")
    run([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", vlist,
         "-c", "copy", "-an", joined_v])

    # 3. concatenate the audio in PCM, then encode to AAC once, with a true-peak
    #    ceiling of -1 dBFS so the master keeps headroom for downstream processing
    alist = os.path.join(workdir, "aconcat.txt")
    with open(alist, "w") as f:
        for p in audio_parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    joined_a = os.path.join(workdir, "joined_audio.wav")
    run([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", alist,
         "-c", "copy", joined_a])

    # 4. final mux: video copied, audio encoded once
    run([FFMPEG, "-y", "-v", "error", "-i", joined_v, "-i", joined_a,
         "-map", "0:v:0", "-map", "1:a:0",
         # level=disabled is essential: alimiter auto-levels the output by
         # default, applying makeup gain that defeats the ceiling entirely.
         "-c:v", "copy", "-af", f"alimiter=level=disabled:limit={PEAK_CEILING}",
         *AUDIO_CODEC, "-movflags", "+faststart", out_mp4])

    total = sum(s.duration / tempo + s.pad_lead + s.pad_tail for s in segments)
    meta = {
        "output": out_mp4, "segments": len(segments),
        "duration_seconds": round(total, 2),
        "duration_hms": _fmt_ts(total).split(".")[0],
        "width": 1920, "height": 1080, "fps": FPS, "title": title,
        "tempo": round(tempo, 5), "speech_seconds": round(speech, 1),
        "target_duration": target_duration, "tempo_note": tempo_note,
    }
    if vtt_path:
        write_vtt(segments, vtt_path, tempo=tempo)
        meta["vtt"] = vtt_path
    if transcript_path:
        write_transcript(segments, transcript_path, title=title, tempo=tempo)
        meta["transcript"] = transcript_path

    for p in video_parts + audio_parts:
        try: os.remove(p)
        except OSError: pass
    return meta
