#!/usr/bin/env python3
"""Measure recorded narration and build out/timeline.json  (v2, chunk-aware).

Placement model:
  * each recorded chunk's real duration is measured with ffmpeg;
  * a chunk's scenes receive speech spans proportional to word count;
  * scenes are laid out sequentially; a scene that STARTS its chunk gets a
    1.0 s lead-in; a continuation scene starts exactly at the cursor (so a
    chunk may flow across a segment boundary without a seam);
  * each 240 s segment receives exactly the pad needed to fill it: leads,
    holds on music-only scenes (weighted 3x), a title hold on the first
    scene and a reflective hold on the last;
  * total is therefore exactly 3600.000 s and segment boundaries land
    exactly on 04:00 multiples.
"""
import json, os, subprocess, sys

ROOT = os.environ.get("TBUPROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = subprocess.run([sys.executable, "-c",
                     "import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())"],
                    capture_output=True, text=True).stdout.strip()
SEG = 240.0
LEAD = 1.0


def dur(path):
    r = subprocess.run([FF, "-hide_banner", "-i", path, "-f", "null", "-"],
                       capture_output=True, text=True)
    t = r.stderr.strip().splitlines()[-1].split("time=")[-1].split(" ")[0]
    h, m, s = t.split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)


def main():
    meta = json.load(open(os.path.join(ROOT, "out", "scenes.json"), encoding="utf-8"))
    plan = json.load(open(os.path.join(ROOT, "out", "audio", "plan.json"), encoding="utf-8"))
    scenes = {s["id"]: s for s in meta["scenes"]}
    for c in plan["chunks"]:
        p = os.path.join(ROOT, c["file"])
        if not os.path.exists(p):
            print(f"MISSING {c['file']}"); sys.exit(1)
        c["dur"] = dur(p)
    speech, chunk_of, first_scene_of = {}, {}, {}
    for c in plan["chunks"]:
        ws = [max(1, len(scenes[i]["narration"].split())) for i in c["scenes"]]
        tot = sum(ws)
        t = 0.0
        first_scene_of[c["index"]] = c["scenes"][0]
        for i, w in zip(c["scenes"], ws):
            d = c["dur"] * w / tot
            speech[i] = d
            chunk_of[i] = c["index"]
            t += d

    segs, order = {}, meta["scenes"]
    for s in order:
        segs.setdefault(s["section"], []).append(s)
    seg_keys = list(segs)

    tl_scenes, chunk_starts, segments = [], {}, []
    for si, key in enumerate(seg_keys):
        members = segs[key]
        seg_start, seg_end = si * SEG, (si + 1) * SEG
        speech_total = sum(speech.get(s["id"], 0.0) for s in members)
        n_leads = sum(1 for s in members
                      if first_scene_of.get(chunk_of.get(s["id"], -1)) == s["id"])
        pad_total = SEG - speech_total - n_leads * LEAD
        if pad_total < 0:
            pad_total = 0.0
        weights = []
        for i, s in enumerate(members):
            w = 1.0
            if s["id"] not in speech:
                w = 3.0            # music-only scene: real hold
            if i == 0:
                w += 2.0           # title hold
            if i == len(members) - 1:
                w += 2.0           # reflective hold
            weights.append(w)
        wsum = sum(weights)
        cursor = seg_start
        for i, s in enumerate(members):
            sd = speech.get(s["id"])
            pad = pad_total * weights[i] / wsum
            if sd is None:
                start, end = cursor, cursor + max(pad, 6.0)
                ss = se = None
            else:
                ci = chunk_of[s["id"]]
                if first_scene_of[ci] == s["id"]:
                    ss = cursor + LEAD
                    if ci not in chunk_starts:
                        chunk_starts[ci] = ss
                else:
                    ss = cursor
                se = ss + sd
                start, end = cursor, se + pad
            tl_scenes.append({
                "id": s["id"], "slide": s["slide"], "section": s["section"],
                "title": s["title"], "start": round(start, 3), "end": round(end, 3),
                "speech_start": None if ss is None else round(ss, 3),
                "speech_end": None if se is None else round(se, 3),
                "narration": s["narration"], "cue": s["cue"], "cite": s["cite"],
                "visual": s["visual"], "anim": s["anim"], "music": s["music"],
            })
            cursor = end
        drift = seg_end - cursor
        if abs(drift) > 0.0005:
            tl_scenes[-1]["end"] = round(tl_scenes[-1]["end"] + drift, 3)
        segments.append({"section": key, "start": seg_start, "end": seg_end})

    chunks = [{"index": c["index"], "file": c["file"],
               "offset": round(chunk_starts[c["index"]], 3),
               "dur": round(c["dur"], 3)}
              for c in plan["chunks"] if c["index"] in chunk_starts]
    out = {"total": 3600.0, "segments": segments, "scenes": tl_scenes, "chunks": chunks}
    json.dump(out, open(os.path.join(ROOT, "out", "timeline.json"), "w",
                        encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"timeline: {len(tl_scenes)} scenes, ends {tl_scenes[-1]['end']:.3f}s")
    for sgm in segments:
        sc = [x for x in tl_scenes if x["section"] == sgm["section"]]
        sp = sum((x["speech_end"] - x["speech_start"]) for x in sc if x["speech_end"])
        print(f"  seg {sgm['section']:<8} {sgm['start']:7.1f}-{sgm['end']:7.1f} "
              f"speech={sp:6.1f}s pad={SEG-sp:6.1f}s")


if __name__ == "__main__":
    main()
