"""
site.py — Build the course index page for the lecture series.

Reads every content/lecture-NN.json, pairs it with whatever has actually been
rendered into videos/ and written into lectures/, and emits a single static
index.html under site/.

    python tools/site.py            -> site/index.html
    python tools/site.py --out DIR  -> DIR/index.html

Courtesy: Triune Biblical University Global Extension, USA.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import slides as S  # noqa: E402

CONTENT = os.path.join(ROOT, "content")
DIST = os.path.join(ROOT, "videos")
LECTURES = os.path.join(ROOT, "lectures")
SLIDES = os.path.join(ROOT, "slides")

TARGET_MIN = 30


def _words(lecture: dict) -> int:
    return sum(len(s.get("narration", "").split()) for s in lecture["slides"])


def _fmt_duration(path: str) -> str:
    """Best-effort duration label; uses ffprobe if available, else file size."""
    if not os.path.exists(path):
        return ""
    try:
        import subprocess
        import shutil
        ff = shutil.which("ffprobe")
        if not ff:
            cand = os.path.join(ROOT, "venv", "lib", "python3.11",
                                "site-packages", "imageio_ffmpeg", "binaries")
            if os.path.isdir(cand):
                ff = next((os.path.join(cand, f) for f in os.listdir(cand)
                           if f.startswith("ffprobe-")), None)
        if ff:
            out = subprocess.run(
                [ff, "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=nw=1:nk=1", path],
                capture_output=True, text=True, timeout=60).stdout.strip()
            secs = float(out)
            return f"{int(secs // 60)}:{int(secs % 60):02d}"
    except Exception:
        pass
    mb = os.path.getsize(path) / (1024 * 1024)
    return f"{mb:.0f} MB"


def collect() -> list:
    rows = []
    for i in range(1, 21):
        p = os.path.join(CONTENT, f"lecture-{i:02d}.json")
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        no = d.get("no", i)
        mp4 = os.path.join(DIST, f"lecture-{no:02d}.mp4")
        md = os.path.join(LECTURES, f"lecture-{no:02d}.md")
        rows.append({
            "no": no,
            "title": d.get("title", ""),
            "subtitle": d.get("subtitle", ""),
            "module": d.get("module", ""),
            "words": _words(d),
            "slides": len(d["slides"]),
            "keywords": d.get("keywords", []),
            "readings": d.get("readings", []),
            "objectives": d.get("objectives", []),
            "has_video": os.path.exists(mp4),
            "video_size": (os.path.getsize(mp4) / (1024 * 1024)) if os.path.exists(mp4) else 0,
            "duration": _fmt_duration(mp4) if os.path.exists(mp4) else "",
            "has_script": os.path.exists(md),
        })
    return rows


CSS = """
:root{
  --navy:#0A1F44; --navy-d:#061428; --gold:#B8912F; --gold-l:#D6B460;
  --paper:#F7F4EC; --slate:#22303F; --muted:#64748B; --rule:#D2C8B2;
  --oxblood:#802A2A;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--slate);
  font:16px/1.65 "Iowan Old Style",Georgia,"Times New Roman",serif;}
a{color:var(--navy);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
header.hero{background:var(--navy);color:#fff;padding:64px 0 56px;
  background-image:linear-gradient(160deg,#0A1F44 0%,#061428 100%);}
header.hero .eyebrow{color:var(--gold-l);text-transform:uppercase;
  letter-spacing:.22em;font-size:12px;font-weight:700;font-family:system-ui,sans-serif}
header.hero h1{font-size:clamp(30px,4.4vw,50px);line-height:1.14;margin:18px 0 12px;font-weight:600}
header.hero .sub{font-size:19px;color:#CBD5E1;max-width:62ch;margin:0 0 26px}
.meta{display:flex;flex-wrap:wrap;gap:28px;border-top:1px solid rgba(255,255,255,.16);
  padding-top:22px;font-family:system-ui,sans-serif;font-size:13px;color:#94A3B8}
.meta b{display:block;color:#fff;font-weight:600;font-size:14px;margin-bottom:2px}
.ribbon{background:var(--gold);color:var(--navy-d);padding:9px 0;
  font-family:system-ui,sans-serif;font-size:12.5px;letter-spacing:.05em;text-align:center;font-weight:600}
section{padding:54px 0}
h2.sec{font-size:14px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);
  font-family:system-ui,sans-serif;margin:0 0 22px;font-weight:700}
.overview{font-size:18px;max-width:74ch}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:18px;margin:34px 0 0}
.stat{background:#fff;border:1px solid var(--rule);border-radius:8px;padding:18px 20px}
.stat .n{font-size:30px;font-weight:600;color:var(--navy);line-height:1}
.stat .l{font-family:system-ui,sans-serif;font-size:11.5px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--muted);margin-top:8px}
ol.lectures{list-style:none;padding:0;margin:0;display:grid;gap:14px}
li.lec{background:#fff;border:1px solid var(--rule);border-radius:8px;
  display:grid;grid-template-columns:96px 1fr 150px;gap:0;overflow:hidden}
li.lec.pending{opacity:.72;border-style:dashed}
.num{background:var(--navy);color:var(--gold-l);display:flex;flex-direction:column;
  align-items:center;justify-content:center;font-family:system-ui,sans-serif;padding:16px 0}
.num .big{font-size:27px;font-weight:700;line-height:1}
.num .sm{font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.75;margin-top:6px}
.body{padding:18px 22px}
.body h3{margin:0 0 6px;font-size:19px;font-weight:600;color:var(--navy)}
.body p{margin:0 0 10px;font-size:15px;color:#3C4A57}
.kw{font-family:system-ui,sans-serif;font-size:11.5px;color:var(--muted)}
.kw span{display:inline-block;background:#F1EDE3;border-radius:20px;padding:2px 10px;margin:3px 5px 0 0}
.side{padding:18px 20px;border-left:1px solid var(--rule);background:#FCFAF5;
  font-family:system-ui,sans-serif;font-size:12.5px;color:var(--muted);
  display:flex;flex-direction:column;justify-content:center;gap:9px}
.side .row{display:flex;justify-content:space-between;gap:10px}
.side .row b{color:var(--slate);font-weight:600}
.btn{display:block;text-align:center;margin-top:4px;padding:8px 10px;border-radius:5px;
  background:var(--navy);color:#fff;font-weight:600;font-size:12.5px}
.btn:hover{background:var(--navy-d);text-decoration:none}
.btn.ghost{background:transparent;color:var(--navy);border:1px solid var(--rule)}
.btn.ghost:hover{background:#fff}
.btn.gold{background:var(--gold);color:var(--navy-d)}
.btn.gold:hover{background:var(--gold-l)}
.btn.off{background:#E7E2D6;color:var(--muted);cursor:not-allowed}
.downloads{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:8px 18px;
  background:#fff;border:1px solid var(--rule);border-radius:8px;padding:20px 24px;margin-top:6px}
.downloads a{display:block;font-size:14.5px;padding:5px 0;border-bottom:1px dotted var(--rule)}
.downloads a::before{content:"↓ ";color:var(--gold);font-weight:700}
.note{font-family:system-ui,sans-serif;font-size:13.5px;color:var(--muted);margin:0 0 16px}
li.lec.pending .num{background:#8A93A5}
footer{background:var(--navy-d);color:#94A3B8;padding:44px 0;font-size:13.5px;
  font-family:system-ui,sans-serif}
footer b{color:#fff}
@media(max-width:820px){
  li.lec{grid-template-columns:72px 1fr}
  .side{grid-column:1/-1;border-left:0;border-top:1px solid var(--rule)}
}
"""


def _esc(s: str) -> str:
    return html.escape(str(s or ""))


def build(rows: list, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    done = [r for r in rows if r["has_video"]]
    total_min = len(rows) * TARGET_MIN
    words = sum(r["words"] for r in rows)
    slides = sum(r["slides"] for r in rows)

    h = []
    h.append("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">")
    h.append("<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">")
    h.append(f"<title>{_esc(S.SERIES)} — {_esc(S.LECTURER)}</title>")
    h.append(f"<style>{CSS}</style></head><body>")

    # ---------------- hero ----------------
    h.append(f"""<header class="hero"><div class="wrap">
<div class="eyebrow">Lecture series · {_esc(S.UNIVERSITY)}</div>
<h1>{_esc(S.SERIES)}</h1>
<p class="sub">A twenty-lecture course on why international energy and natural resources
law must be studied at every programme level, taught with reference to the practice of
states, investors, communities and tribunals across every region of the world.</p>
<div class="meta">
  <div><b>{_esc(S.LECTURER)}</b>Lecturer</div>
  <div><b><a style="color:var(--gold-l)" href="video/IENRL-complete-course.mp4?dl=1"
     download="IENRL-complete-course.mp4">Download the complete course (one MP4)</a></b>Single file</div>
  <div><b>{len(rows)} lectures · {total_min} hours</b>Format</div>
  <div><b>Undergraduate &amp; Postgraduate</b>Programme levels</div>
  <div><b>Global perspectives</b>Scope</div>
  <div><b>{_esc(S.UNIVERSITY)}</b>Courtesy</div>
</div></div></header>""")
    h.append(f'<div class="ribbon">{_esc(S.UNIVERSITY)} · {_esc(S.LECTURER)} · '
             f'{len(done)} of {len(rows)} lectures rendered</div>')

    # ---------------- overview ----------------
    h.append('<div class="wrap"><section>')
    h.append('<h2 class="sec">The course</h2>')
    h.append(f"""<p class="overview">Energy and natural resources are the material basis of
every economy, and the law governing them is the most consequential body of legal rules
that most lawyers never study. This series takes the field in four movements: the
foundations of sovereignty, trade and investment; the commodity regimes of petroleum,
gas, electricity, the sea, mining and nuclear energy; the cross-cutting themes of the
energy transition, climate change, human rights and the environment; and the
settlement of disputes together with the distribution of the benefits and burdens of
extraction. Every lecture is a complete thirty-minute class with slides, narration and
subtitles, and each closes with a case, a set of readings, and differentiated
objectives for undergraduate and postgraduate students.</p>""")
    h.append('<div class="stats">')
    for n, l in [(f"{len(rows)}", "Lectures"), (f"{total_min} h", "Total runtime"),
                 (f"{words:,}", "Words of narration"),
                 (f"{slides}", "Slides"),
                 (f"{len(done)}/{len(rows)}", "Videos rendered")]:
        h.append(f'<div class="stat"><div class="n">{n}</div><div class="l">{l}</div></div>')
    h.append('</div></section></div>')

    # ---------------- lecture list ----------------
    h.append('<div class="wrap"><section>')
    h.append('<h2 class="sec">Lectures</h2>')
    h.append('<ol class="lectures">')
    for r in rows:
        cls = "lec" if r["has_video"] else "lec pending"
        h.append(f'<li class="{cls}" id="lecture-{r["no"]:02d}">')
        h.append(f'<div class="num"><div class="big">{r["no"]:02d}</div>'
                 f'<div class="sm">Lecture</div></div>')
        h.append('<div class="body">')
        h.append(f'<h3>{_esc(r["title"])}</h3>')
        h.append(f'<p>{_esc(r["subtitle"])}</p>')
        h.append(f'<div class="kw">{_esc(r["module"])}</div>')
        if r["keywords"]:
            h.append('<div class="kw">' + "".join(
                f"<span>{_esc(k)}</span>" for k in r["keywords"][:6]) + '</div>')
        h.append('</div>')
        h.append('<div class="side">')
        h.append(f'<div class="row"><span>Words</span><b>{r["words"]:,}</b></div>')
        h.append(f'<div class="row"><span>Slides</span><b>{r["slides"]}</b></div>')
        if r["has_video"]:
            h.append(f'<div class="row"><span>Runtime</span><b>{_esc(r["duration"])}</b></div>')
            h.append(f'<div class="row"><span>Size</span><b>{r["video_size"]:.0f} MB</b></div>')
            h.append(f'<a class="btn" href="video/lecture-{r["no"]:02d}.mp4">Watch</a>')
            h.append(f'<a class="btn gold" href="video/lecture-{r["no"]:02d}.mp4?dl=1">'
                     f'Download MP4</a>')
        else:
            h.append('<div class="row"><span>Status</span><b>In production</b></div>')
            h.append('<span class="btn off">Watch</span>')
        if r["has_script"]:
            h.append(f'<a class="btn ghost" href="script/lecture-{r["no"]:02d}.md?dl=1">'
                     f'Script</a>')
        h.append('</div></li>')
    h.append('</ol></section></div>')

    # ---------------- direct downloads ----------------
    h.append('<div class="wrap"><section>')
    h.append('<h2 class="sec">Direct downloads</h2>')
    total_mb = sum(r["video_size"] for r in rows)
    whole = os.path.join(DIST, "IENRL-complete-course.mp4")
    if os.path.exists(whole):
        wmb = os.path.getsize(whole) / (1024 * 1024)
        h.append(f'<div class="downloads"><a href="video/IENRL-complete-course.mp4?dl=1" '
                 f'download="IENRL-complete-course.mp4"><b>The complete course — one file, '
                 f'20 chapters</b> <span style="color:var(--muted)">· {wmb:.0f} MB</span></a></div>')
    h.append(f'<p class="note">Right-click and choose “Save link as”, or click to download. '
             f'Each file is a self-contained H.264/AAC MP4 with soft English subtitles. '
             f'Total {total_mb/1024:.2f} GB across {len(rows)} files.</p>')
    h.append('<div class="downloads">')
    for r in rows:
        if not r["has_video"]:
            continue
        name = f"Lecture {r['no']:02d} — {r['title']}"
        h.append(f'<a href="video/lecture-{r["no"]:02d}.mp4?dl=1" '
                 f'download="{_esc(name)}.mp4">{_esc(name)} '
                 f'<span style="color:var(--muted)">· {r["video_size"]:.0f} MB</span></a>')
    h.append('</div></section></div>')

    # ---------------- footer ----------------
    stamp = datetime.now(timezone.utc).strftime("%d %B %Y")
    h.append(f"""<footer><div class="wrap">
<p><b>{_esc(S.SERIES)}</b></p>
<p>{_esc(S.LECTURER)} · {_esc(S.UNIVERSITY)}</p>
<p>Narration, slides and subtitles generated for this course. Generated {stamp}.</p>
</div></footer>""")
    h.append('</body></html>')

    path = os.path.join(out_dir, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(h))
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the lecture series index page.")
    ap.add_argument("--out", default=os.path.join(ROOT, "site"))
    a = ap.parse_args()
    rows = collect()
    p = build(rows, a.out)
    print(f"wrote {p}  ({len(rows)} lectures, "
          f"{sum(1 for r in rows if r['has_video'])} with video)")


if __name__ == "__main__":
    main()
