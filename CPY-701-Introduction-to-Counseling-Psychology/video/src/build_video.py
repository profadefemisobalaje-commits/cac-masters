#!/usr/bin/env python3
"""
CPY 701 - Introduction to Counseling Psychology
Video assembler.

Steps:
  plan    : read dist/slides/<week>/manifest.json, group slide narrations into
            <=1500-char audio chunks, write chunk scripts + build plan (JSON).
  assemble: given generated chunk audio files (dist/audio/<week>/chunk-NN.*),
            measure durations, allocate per-slide times, and mux the narrated
            1080p MP4 with chapter markers, SRT captions and a poster frame.

Requires: imageio-ffmpeg (pip install imageio-ffmpeg) or system ffmpeg.
"""
import json, os, subprocess, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))          # .../CPY-701-.../
DIST = os.path.join(ROOT, 'dist')

def ffmpeg_exe():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return 'ffmpeg'

def probe(path):
    out = subprocess.run([ffmpeg_exe(), '-i', path, '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    for ln in out.splitlines():
        if 'Duration:' in ln:
            h, m, s = ln.split('Duration:')[1].split(',')[0].strip().split(':')
            return float(h) * 3600 + float(m) * 60 + float(s)
    raise RuntimeError('cannot probe ' + path)

# ---------------------------------------------------------------- plan
def plan(week):
    man = json.load(open(os.path.join(DIST, 'slides', week, 'manifest.json')))
    slides = man['slides']
    chunks, cur, cur_chars = [], [], 0
    for s in slides:
        n = s['narration'].strip()
        if cur and cur_chars + 1 + len(n) > 1490:
            chunks.append(cur); cur, cur_chars = [], 0
        cur.append(s); cur_chars += (1 if cur_chars else 0) + len(n)
    if cur:
        chunks.append(cur)
    out = os.path.join(DIST, 'audio', week)
    os.makedirs(out, exist_ok=True)
    plan_chunks = []
    for i, ch in enumerate(chunks, 1):
        text = ' '.join(s['narration'].strip() for s in ch)
        open(os.path.join(out, f'chunk-{i:02d}.txt'), 'w').write(text + '\n')
        plan_chunks.append({'chunk': i, 'text': text, 'chars': len(text),
                            'slides': [s['i'] for s in ch],
                            'files': [s['file'] for s in ch],
                            'captions': [c for s in ch for c in caption_sentences(s['narration'])]})
    p = {'week': week, 'title': man['title'], 'chunks': plan_chunks,
         'total_chars': sum(c['chars'] for c in plan_chunks)}
    json.dump(p, open(os.path.join(out, 'plan.json'), 'w'), indent=2)
    print(f"{week}: {len(slides)} slides -> {len(plan_chunks)} audio chunks "
          f"({p['total_chars']} chars). scripts in {out}")
    return p

def caption_sentences(narr):
    """Split narration into SRT-sized caption cues (~90 chars)."""
    words, cues, cur = narr.split(), [], ''
    for w in words:
        if cur and len(cur) + 1 + len(w) > 88 and cur.count(' ') >= 6:
            cues.append(cur.strip()); cur = ''
        cur += (' ' if cur else '') + w
    if cur.strip():
        cues.append(cur.strip())
    return cues

# ---------------------------------------------------------------- assemble
def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms//3600000:02d}:{ms//3600000%60:02d}:{ms//360000%1000//60:02d},{ms%1000:03d}"

def assemble(week):
    adir = os.path.join(DIST, 'audio', week)
    p = json.load(open(os.path.join(adir, 'plan.json')))
    sdir = os.path.join(DIST, 'slides', week)
    # 1. concat chunk audio -> narration track
    audio_files = []
    for ch in p['chunks']:
        cand = [f for f in os.listdir(adir)
                if f.startswith(f"chunk-{ch['chunk']:02d}") and f.split('.')[-1] in ('mp3', 'wav', 'm4a', 'aac', 'ogg', 'opus', 'flac')]
        if not cand:
            sys.exit(f"missing audio for chunk {ch['chunk']} in {adir}")
        audio_files.append(os.path.join(adir, sorted(cand)[0]))
    concat_list = os.path.join(adir, 'concat.txt')
    with open(concat_list, 'w') as fh:
        for f in audio_files:
            fh.write(f"file '{f}'\n")
    narr = os.path.join(adir, 'narration.mp3')
    subprocess.run([ffmpeg_exe(), '-y', '-f', 'concat', '-safe', '0', '-i', concat_list,
                    '-c', 'copy', narr], check=True, capture_output=True)
    chunk_dur = [probe(f) for f in audio_files]
    # 2. per-slide durations: proportional to narration chars inside each chunk
    man = json.load(open(os.path.join(sdir, 'manifest.json')))
    narr_chars = {s['i']: max(1, len(s['narration'])) for s in man['slides']}
    slide_dur = {}
    for ch, d in zip(p['chunks'], chunk_dur):
        tot = sum(narr_chars[i] for i in ch['slides'])
        for i in ch['slides']:
            slide_dur[i] = d * narr_chars[i] / tot
    # 3. concat demuxer input
    conc = os.path.join(adir, 'slides.txt')
    with open(conc, 'w') as fh:
        for s in man['slides']:
            fh.write(f"file '{os.path.join(sdir, s['file'])}'\nduration {slide_dur[s['i']]:.3f}\n")
        fh.write(f"file '{os.path.join(sdir, man['slides'][-1]['file'])}'\n")
    # 4. SRT captions
    cues, t = [], 0.0
    for ch, d in zip(p['chunks'], chunk_dur):
        tot = sum(len(c) for c in ch['captions']) or 1
        for c in ch['captions']:
            dur = d * len(c) / tot
            cues.append((t, t + dur, c)); t += dur
    srtp = os.path.join(DIST, week + '-captions.srt')
    with open(srtp, 'w') as fh:
        for k, (a, b, c) in enumerate(cues, 1):
            fh.write(f"{k}\n{srt_time(a)} --> {srt_time(b)}\n{c}\n\n")
    # 5. chapters
    chp = os.path.join(adir, 'chapters.txt')
    with open(chp, 'w') as fh:
        fh.write(';FFMETADATA1\n')
        acc = 0.0
        titles = {s['i']: s.get('title') or s.get('slug') or '' for s in man['slides']}
        for k, (ch, d) in enumerate(zip(p['chunks'], chunk_dur), 1):
            label = titles[ch['slides'][0]].replace('=', ' ')[:60] or f'Part {k}'
            fh.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(acc*1000)}\nEND={int((acc+d)*1000)}\n"
                     f"title={k}. {label}\n")
            acc += d
    # 6. mux
    outmp4 = os.path.join(DIST, f'CPY701-{week.upper()}-lecture.mp4')
    cmd = [ffmpeg_exe(), '-y', '-f', 'concat', '-safe', '0', '-i', conc,
           '-i', narr, '-i', chp,
           '-map', '0:v', '-map', '1:a', '-map_metadata', '2',
           '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
           '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2',
           '-movflags', '+faststart', '-shortest', outmp4]
    subprocess.run(cmd, check=True, capture_output=True)
    total = probe(outmp4)
    print(f"{week}: assembled {outmp4}  ({total/60:.1f} min, {os.path.getsize(outmp4)/1e6:.1f} MB)")
    print(f"captions: {srtp} ({len(cues)} cues)")
    return outmp4

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'plan'
    week = sys.argv[2] if len(sys.argv) > 2 else 'w01'
    if cmd == 'plan':
        plan(week)
    elif cmd == 'assemble':
        assemble(week)
