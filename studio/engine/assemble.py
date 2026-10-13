"""CAC Lecture Studio - video assembly.
Renders a course's segment slides, times them to the generated narration
clips, adds crossfades, and encodes a sharp 720p MP4."""
import json, os, re, subprocess, shutil
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
import sys
sys.path.insert(0, ROOT)
from engine import render_core as rc, slides as SL, compose as CP

def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def slug(c): return c["code"].replace(".", "").replace("*", "X").lower()

def duration(path):
    r = subprocess.run([ffmpeg(), "-i", path, "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", r.stderr)
    h, mn, s = m.groups()
    return int(h)*3600 + int(mn)*60 + float(s)

def render_slides(c, segs, outdir, verbose=True):
    """Render every segment's slides. Returns list of png paths in order."""
    os.makedirs(outdir, exist_ok=True)
    st = dict(c["style"]); st["code"] = c["code"]; st["hours"] = c["hours"]; st["sem"] = c["sem"]
    st["title"] = c["title"]; st["tagline"] = c["tagline"]
    paths = []
    for s in segs:
        for j, (kind, args, w) in enumerate(s["slides"]):
            p = os.path.join(outdir, f"{s['id']}_{j:02d}.png")
            if not os.path.exists(p):
                img = _make(kind, args, st, c)
                img.save(p)
                if verbose: print("  slide", p)
            paths.append(p)
    return paths

def _make(kind, args, st, c):
    if kind == "opener":  return SL.slide_opener(st)
    if kind == "title":   return SL.slide_title(st, c)
    if kind == "agenda":
        return SL.slide_agenda(st, ["A Story From Practice", "The Course Portrait",
            "Learning Outcomes", "Module-by-Module Tour", "Clinical & Practical Work",
            "Assessment", "How to Succeed"])
    if kind == "stats":
        return SL.slide_stats(st, [(c["hours"], "Video Hours"), ("1.6", "Course Units"),
                                   (len(c["modules"]), "Modules"), (len(c["outcomes"]), "Outcomes")])
    if kind == "vignette":
        return SL.slide_vignette(st, c["vignette"], c.get("vignette_attr", "A moment from practice"))
    if kind == "heading":
        return SL.slide_heading(st, *args)
    if kind == "bullets":
        kn, ti = args
        if ti.startswith("Three Reasons"): items = c["importance"]
        elif ti.startswith("The Territory"): items = [c["description"][i:i+118].strip() for i in range(0, min(len(c["description"]), 354), 118)]
        elif ti.startswith("Questions"): items = c["questions"]
        elif ti.startswith("Figures"):
            figs = c["figures"]
            if figs and isinstance(figs[0], str): figs = list(zip(figs[0::2], figs[1::2]))
            items = [f"{n} — {w}" for n, w in figs]
        elif ti.startswith("Settings"): items = c["settings"]
        elif ti.startswith("Learning by Doing"): items = c["practicum"][1]
        elif ti.startswith("How Competence"): items = c["assessment"][1]
        elif ti.startswith("Habits"): items = c["tips"]
        elif ti.startswith("Notice ·"): items = [
            "Notice: describe only what you can see and hear",
            "Name: attach the course concepts that truly fit",
            "Choose: weigh two or three possible responses",
            "Consult: check ethics, culture, and supervision",
            "Act and reflect: intervene, then review what the moment taught"]
        elif ti.startswith("The Young Clients"): items = c.get("cases", ["the young person from our opening scene", "a family learning new patterns together", "an adolescent searching for a durable identity"])
        elif ti.startswith("The Vocation"): items = [c["faith"][:150], c["faith"][150:300] or "Bring competence and conviction together in one disciplined life.", "This course forms the person as much as the professional."]
        else: items = c["tips"]
        return SL.slide_bullets(st, kn, ti, items)
    if kind == "outcome":
        idx, tot, ti, body = args
        return SL.slide_outcome(st, idx, tot, ti, body)
    if kind == "module":
        i, n, name, h, topics, why = args
        return SL.slide_module(st, i, n, name, h, topics, why)
    if kind == "roadmap":
        return SL.slide_roadmap(st, [(m[0], m[1]) for m in c["modules"]])
    if kind == "closing":
        return SL.slide_closing(st, c, c["closing"])
    if kind == "credits":
        return SL.slide_credits(st, c)
    raise ValueError(kind)

FPS = 25
def crossfade_frames(a_path, b_path, outdir, k, n=10):
    a = Image.open(a_path).convert("RGB"); b = Image.open(b_path).convert("RGB")
    ps = []
    for i in range(1, n+1):
        p = os.path.join(outdir, f"xf_{k:03d}_{i:02d}.png")
        SL.blend(a, b, i/(n+1)).save(p); ps.append(p)
    return ps

def build_video(c, segs, audio_dir, workdir, outpath, silent=False):
    slide_dir = os.path.join(workdir, "slides"); os.makedirs(slide_dir, exist_ok=True)
    slide_paths = render_slides(c, segs, slide_dir)
    # timing
    CBREATH = 0.35
    def reading(t): return max(6.0, len(t)/13.0)
    durs, clip_files, narrated_flags = [], [], []
    for s in segs:
        aps = [os.path.join(audio_dir, f"{s['id']}_c{k}.mp3") for k in range(len(s["clips"]))]
        present = aps and all(os.path.exists(p) for p in aps)
        clip_files.append(aps if present else [])
        narrated_flags.append(present)
        if present:
            durs.append(sum(duration(p) for p in aps) + CBREATH*(len(aps)-1))
        else:
            durs.append(reading(" ".join(s["clips"])))
    have_all = all(narrated_flags); have_any = any(narrated_flags)
    LEAD, TAIL, GAP = 0.9, 2.0, 0.6
    timeline = []  # (png, seconds)
    idx = 0
    for si, s in enumerate(segs):
        seg_total = durs[si]
        ws = [w for _,_,w in s["slides"]]
        tot_w = sum(ws)
        alloc = [max(2.6, seg_total*w/tot_w) for w in ws]
        drift = seg_total - sum(alloc)
        alloc[-1] += drift
        for j in range(len(ws)):
            timeline.append((slide_paths[idx], alloc[j])); idx += 1
        if si < len(segs)-1: timeline.append((slide_paths[idx-1], GAP))
    timeline.insert(0, (slide_paths[0], LEAD)); timeline.append((slide_paths[-1], TAIL))
    # write concat with crossfades
    xf_dir = os.path.join(workdir, "xf"); os.makedirs(xf_dir, exist_ok=True)
    concat = os.path.join(workdir, "concat.txt"); lines = []
    def add(p, d): lines.append(f"file '{p}'\nduration {d:.3f}")
    for i, (p, d) in enumerate(timeline):
        add(p, max(d, 0.5))
        if i+1 < len(timeline) and timeline[i+1][0] != p:
            xfs = crossfade_frames(p, timeline[i+1][0], xf_dir, i)
            for xp in xfs: add(xp, 1/FPS)
    lines.append(f"file '{timeline[-1][0]}'")
    open(concat, "w").write("\n".join(lines))
    video_total = sum(d for _, d in timeline) + (len(timeline)-1)*(10/FPS)
    # audio track (voice where clips exist; readable silence elsewhere)
    track = os.path.join(workdir, "track.wav"); parts = os.path.join(workdir, "aparts")
    os.makedirs(parts, exist_ok=True)
    def silence(p, t):
        subprocess.run([ffmpeg(), "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
                        "-t", str(t), "-c:a", "pcm_s16le", p], check=True, capture_output=True)
    plist, n = [], 0
    silence(f"{parts}/lead.wav", LEAD); plist.append(f"{parts}/lead.wav")
    for si, aps in enumerate(clip_files):
        if aps:
            for k, ap in enumerate(aps):
                w = f"{parts}/{n:02d}.wav"; n += 1
                subprocess.run([ffmpeg(), "-y", "-i", ap, "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", w],
                               check=True, capture_output=True)
                plist.append(w)
                if k < len(aps)-1:
                    b = f"{parts}/br{n}.wav"; n += 1
                    silence(b, CBREATH); plist.append(b)
        else:
            s0 = f"{parts}/sil{n}.wav"; n += 1
            silence(s0, durs[si]); plist.append(s0)
        if si < len(segs)-1:
            g = f"{parts}/gap{n}.wav"; n += 1
            silence(g, GAP); plist.append(g)
    silence(f"{parts}/tail.wav", TAIL + 1.0)
    plist.append(f"{parts}/tail.wav")
    open(f"{parts}/list.txt","w").write("".join(f"file '{p}'\n" for p in plist))
    subprocess.run([ffmpeg(), "-y", "-f", "concat", "-safe", "0", "-i", f"{parts}/list.txt",
                    "-c:a", "pcm_s16le", track], check=True, capture_output=True)
    audio_args = ["-i", track, "-c:a", "aac", "-b:a", "160k"]
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    cmd = [ffmpeg(), "-y", "-f", "concat", "-safe", "0", "-i", concat] + audio_args + [
        "-vf", f"scale=1280:720,format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-tune", "stillimage",
        "-t", f"{video_total:.2f}", "-movflags", "+faststart", outpath]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:]); raise SystemExit("encode failed")
    return outpath, video_total, ("full" if have_all else "partial" if have_any else "silent")

def render_course(json_path, silent=False, out_root=None):
    c = json.load(open(json_path))
    segs = CP.build_script(c)
    sl = slug(c)
    out_root = out_root or os.path.join(REPO, "out")
    audio_dir = os.path.join(ROOT, "audio", sl)
    workdir = os.path.join(out_root, "work", sl)
    outpath = os.path.join(out_root, "videos", f"{sl}_lecture.mp4")
    p, total, have = build_video(c, segs, audio_dir, workdir, outpath, silent=silent)
    # poster
    poster = os.path.join(out_root, "posters", f"{sl}.jpg")
    title_png = os.path.join(workdir, "slides", "s01_open_01.png")
    if os.path.exists(title_png): Image.open(title_png).convert("RGB").save(poster, quality=88)
    meta = dict(code=c["code"], title=c["title"], sem=c["sem"], hours=c["hours"],
                tagline=c["tagline"], duration=round(total,1), state=have,
                video=os.path.basename(p), poster=os.path.basename(poster))
    json.dump(meta, open(os.path.join(out_root, "videos", f"{sl}_lecture.json"), "w"), indent=1)
    shutil.rmtree(workdir, ignore_errors=True)
    print(f"DONE {p}  ({total/60:.1f} min, narrated={have})")
    return p
