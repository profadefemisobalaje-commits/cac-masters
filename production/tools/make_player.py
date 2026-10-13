#!/usr/bin/env python3
"""Build a self-contained episode player page into out/.

Reads   out/timeline.json, out/captions.srt, out/slides/slide_001.png,
        out/audio/plan.json (optional), assets/fonts/ttf/*
Writes  out/index.html, out/captions.vtt, out/poster.jpg, out/fonts/*

The page shows the finished video when out/video/final_1080p.mp4 exists, and
falls back to a production dashboard (slide gallery + recorded narration
clips + live encode progress from out/render_status.json) until then.

Usage:  TBUPROJ=/path/to/episode python tools/make_player.py
"""
import json, os, shutil

ROOT = os.environ.get("TBUPROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")  # production/assets
OUT = os.path.join(ROOT, "out")

SERIES = "WHAT YOU MAY NOT KNOW"
SEASON_EP = "SEASON 1 · EPISODE 03"
TITLE = "One Person, Two Natures"
SUBTITLE = "THE COUNCIL OF CHALCEDON — HOW THE CHURCH SPENT A CENTURY LEARNING WHAT NOT TO SAY ABOUT CHRIST"
COURTESY = "A PRESENTATION OF TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA"
RECOGNITION = "RECOGNITION: PROF. ADELEKE DANIEL DUROJAIYE (PHD), PRESIDENT AND CHANCELLOR"
NOTICE = ("Narration {n} of {t} clips recorded. When the last clips land, this page runs the "
          "timing, score and mix, then the 1080p encode — and switches to the video player "
          "(currently: {v}).")
FONTS = ["Cinzel-700.ttf", "Cinzel-900.ttf", "CormorantGaramond-400.ttf",
         "CormorantGaramond-500.ttf", "Inter-400.ttf", "Montserrat-500.ttf"]


def main():
    tlp = os.path.join(OUT, "timeline.json")
    if os.path.exists(tlp):
        tl = json.load(open(tlp, encoding="utf-8"))
        scenes = tl["scenes"]
        total = tl.get("total") or scenes[-1]["end"]
    else:  # pre-timeline: page still boots from scenes.json
        sc = json.load(open(os.path.join(OUT, "scenes.json"), encoding="utf-8"))
        scenes = sc["scenes"] if isinstance(sc, dict) else sc
        total = 0
        for s in scenes:
            s.setdefault("start", "")
            s.setdefault("end", "")
            s.setdefault("title", "")

    # ---- captions.vtt from captions.srt ----
    srt_path = os.path.join(OUT, "captions.srt")
    if os.path.exists(srt_path):
        srt = open(srt_path, encoding="utf-8").read()
        import re
        vtt = re.sub(r"(\d\d:\d\d:\d\d),(\d\d\d)", r"\1.\2", srt)
        open(os.path.join(OUT, "captions.vtt"), "w", encoding="utf-8").write("WEBVTT\n\n" + vtt)

    # ---- poster from slide 1 ----
    try:
        from PIL import Image
        im = Image.open(os.path.join(OUT, "slides", "slide_001.png")).resize((1920, 1080), Image.LANCZOS)
        im.save(os.path.join(OUT, "poster.jpg"), quality=88)
    except Exception as e:  # noqa
        print("poster skipped:", e)

    # ---- fonts ----
    fdir = os.path.join(OUT, "fonts")
    os.makedirs(fdir, exist_ok=True)
    for f in FONTS:
        src = os.path.join(ASSETS, "fonts", "ttf", f)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(fdir, f))

    def hhmmss(t):
        t = float(t); h = int(t // 3600); m = int(t % 3600 // 60); s = int(t % 60)
        return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"

    chapters = []
    if total:
        chapters = [{"t": float(s["start"]), "label": hhmmss(s["start"]),
                     "title": s.get("title", ""), "n": s.get("id", "")} for s in scenes]

    # ---- production dashboard pieces ----
    slides = []
    for s in scenes:
        n = int(s["slide"])
        p = os.path.join(OUT, "proxies", f"p_{n:03d}.jpg")
        slides.append({"n": n, "title": s.get("title", ""), "t": hhmmss(s["start"]) if total else "",
                       "src": f"proxies/p_{n:03d}.jpg" if os.path.exists(p) else f"slides/slide_{n:03d}.png"})
    clips = []
    plan = os.path.join(OUT, "audio", "plan.json")
    NCHUNKS = 0
    if os.path.exists(plan):
        pj = json.load(open(plan, encoding="utf-8"))
        NCHUNKS = len(pj["chunks"])
        for i, c in enumerate(pj["chunks"]):
            f = os.path.join(OUT, "audio", f"narr_{i:02d}.mp3")
            if os.path.exists(f):
                clips.append({"i": f"{i:02d}", "scenes": " · ".join(c["scenes"]),
                              "chars": len(c["text"]), "src": f"audio/narr_{i:02d}.mp3"})

    chap_json = json.dumps(chapters, ensure_ascii=False)
    slide_json = json.dumps(slides, ensure_ascii=False)
    clip_json = json.dumps(clips, ensure_ascii=False)

    html = TEMPLATE
    for k, v in {
        "__SERIES__": SERIES, "__SEASON_EP__": SEASON_EP, "__TITLE__": TITLE,
        "__SUBTITLE__": SUBTITLE, "__COURTESY__": COURTESY, "__RECOGNITION__": RECOGNITION,
        "__RUNTIME__": hhmmss(total) if total else "IN PRODUCTION", "__CHAP__": chap_json, "__SLIDES__": slide_json,
        "__NOTICE__": NOTICE.format(n=len(clips), t=NCHUNKS, v=("ready" if os.path.exists(os.path.join(OUT,"video","final_1080p.mp4")) else "still encoding")),
        "__CLIPS__": clip_json, "__NSCENES__": str(len(scenes)), "__NCLIPS__": str(len(clips)),
    }.items():
        html = html.replace(k, v)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print(f"player: {os.path.join(OUT, 'index.html')} ({len(scenes)} scenes, {len(clips)} clips, runtime {hhmmss(total)})")


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__SERIES__ ABOUT __TITLE__ — Season 1, Episode 03</title>
<style>
@font-face{font-family:Cinzel;src:url(fonts/Cinzel-700.ttf);font-weight:700}
@font-face{font-family:Cinzel;src:url(fonts/Cinzel-900.ttf);font-weight:900}
@font-face{font-family:Cormorant;src:url(fonts/CormorantGaramond-400.ttf);font-weight:400}
@font-face{font-family:Cormorant;src:url(fonts/CormorantGaramond-500.ttf);font-weight:500}
@font-face{font-family:Inter;src:url(fonts/Inter-400.ttf)}
@font-face{font-family:Mont;src:url(fonts/Montserrat-500.ttf)}
:root{--navy:#0a1628;--gold:#c8a24a;--gold2:#d8be8a;--ivory:#f5f1e6;--dim:#c4c2ba;--burg:#6e1423}
*{box-sizing:border-box}
body{margin:0;background:linear-gradient(180deg,#050c18,#0a1628 40%,#0d1b2f);color:var(--ivory);
     font-family:Cormorant,Georgia,serif;line-height:1.55}
.wrap{max-width:1180px;margin:0 auto;padding:38px 26px 90px}
.kicker{font-family:Mont,sans-serif;letter-spacing:.34em;font-size:11px;color:var(--gold);margin:0 0 10px}
h1{font-family:Cinzel,serif;font-weight:900;font-size:clamp(26px,4.4vw,52px);margin:0 0 6px;letter-spacing:.03em}
h1 .sm{display:block;font-size:.42em;font-weight:700;letter-spacing:.22em;color:var(--gold2);margin-top:8px}
.sub{font-family:Mont,sans-serif;font-size:12px;letter-spacing:.16em;color:var(--dim);max-width:900px;margin:14px 0 22px}
.rule{height:2px;background:linear-gradient(90deg,var(--gold),rgba(200,162,74,.05));margin:22px 0 26px}
.grid{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:26px;align-items:start}
@media(max-width:900px){.grid{grid-template-columns:1fr}}
.card{background:rgba(255,255,255,.035);border:1px solid rgba(200,162,74,.28);border-radius:10px;padding:16px 18px}
video{width:100%;background:#000;border-radius:8px;border:1px solid rgba(200,162,74,.35)}
.meta{font-family:Mont,sans-serif;font-size:11.5px;letter-spacing:.12em;color:var(--dim);margin:12px 0 0}
.badge{display:inline-block;font-family:Mont,sans-serif;font-size:10.5px;letter-spacing:.2em;
       border:1px solid var(--gold);color:var(--gold);border-radius:999px;padding:5px 12px;margin-right:8px}
h2{font-family:Cinzel,serif;font-size:19px;letter-spacing:.08em;color:var(--gold2);margin:30px 0 12px}
ol.ch{list-style:none;margin:0;padding:0;max-height:420px;overflow:auto}
ol.ch li{display:flex;gap:10px;padding:7px 8px;border-bottom:1px solid rgba(255,255,255,.06);cursor:pointer;font-size:15px}
ol.ch li:hover{background:rgba(200,162,74,.09)}
ol.ch .t{font-family:Mont,sans-serif;font-size:11px;color:var(--gold);min-width:56px;padding-top:3px}
.slides{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;margin-top:8px}
.slides figure{margin:0;background:#050c18;border:1px solid rgba(200,162,74,.2);border-radius:8px;overflow:hidden}
.slides img{width:100%;display:block}
.slides figcaption{font-family:Mont,sans-serif;font-size:10.5px;letter-spacing:.1em;color:var(--dim);padding:7px 9px}
.clips{display:grid;gap:9px;margin-top:8px}
.clip{display:grid;grid-template-columns:64px 1fr 250px;gap:12px;align-items:center;
      background:rgba(255,255,255,.03);border:1px solid rgba(200,162,74,.18);border-radius:8px;padding:9px 12px}
@media(max-width:700px){.clip{grid-template-columns:1fr}}
.clip .n{font-family:Cinzel,serif;color:var(--gold);font-size:17px}
.clip .s{font-family:Mont,sans-serif;font-size:10.5px;letter-spacing:.1em;color:var(--dim)}
audio{width:100%;height:32px}
.notice{border-left:3px solid var(--gold);background:rgba(200,162,74,.09);padding:12px 16px;font-size:16px}
.bar{height:6px;background:rgba(255,255,255,.09);border-radius:4px;overflow:hidden;margin-top:10px}
.bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--gold),var(--gold2))}
footer{margin-top:46px;border-top:1px solid rgba(200,162,74,.25);padding-top:20px;
       font-family:Mont,sans-serif;font-size:10.5px;letter-spacing:.18em;color:var(--dim)}
footer b{color:var(--gold2);font-weight:500}
</style></head><body><div class="wrap">
<p class="kicker">__SERIES__ · __SEASON_EP__</p>
<h1>__TITLE__<span class="sm">__SUBTITLE__</span></h1>
<p class="sub">NARRATED DEEP DIVE · RUNTIME __RUNTIME__ · __NSCENES__ SCENES · ORIGINAL SYNTHESIZED SCORE · CLOSED CAPTIONS</p>
<div class="rule"></div>

<div id="playerbox" class="card" style="display:none">
  <video id="v" controls preload="metadata" poster="poster.jpg" crossorigin="anonymous">
    <source src="video/final_1080p.mp4" type="video/mp4">
    <track kind="captions" srclang="en" label="English" src="captions.vtt" default>
  </video>
  <p class="meta" id="vmeta"></p>
</div>

<div id="wip">
  <div class="card">
    <span class="badge" id="state">IN PRODUCTION</span>
    <span class="badge" id="nb">NARRATION __NCLIPS__ CLIPS</span>
    <p class="notice" style="margin-top:14px" id="noticeline">__NOTICE__</p>
    <div class="bar"><i id="prog"></i></div>
    <p class="meta" id="progtext">checking encode progress…</p>
  </div>

  <h2>Narration clips</h2>
  <div class="clips" id="clips"></div>

  <h2>Storyboard — 38 slides (2048px previews; 4K masters)</h2>
  <div class="slides" id="slides"></div>
</div>

<div id="finalbox" style="display:none">
  <h2>Chapters</h2>
  <ol class="ch" id="ch"></ol>
</div>

<footer>
  <p><b>__COURTESY__</b></p>
  <p><b>__RECOGNITION__</b></p>
  <p style="margin-top:12px">SOURCES INCLUDED ON SCREEN · DATES VERIFIED · CONTESTED VIEWS STEEL-MANNED · LABELLED RECONSTRUCTIONS</p>
</footer>
</div>
<script>
const CH=__CHAP__, SL=__SLIDES__, CL=__CLIPS__;
/* view helpers */
const fmt=s=>{const h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=Math.floor(s%60);
  return (h?h+":":"")+String(m).padStart(h?2:1,"0")+":"+String(x).padStart(2,"0")};
document.getElementById('clips').innerHTML=CL.map(c=>`<div class="clip"><div class="n">${c.i}</div>
  <div><div>Narration chunk ${c.i}</div><div class="s">SCENES ${c.scenes}</div></div>
  <audio controls preload="none" src="${c.src}"></audio></div>`).join('');
document.getElementById('slides').innerHTML=SL.map(s=>`<figure><img loading="lazy" src="${s.src}" alt="Slide ${s.n} ${s.title}">
  <figcaption>${String(s.n).padStart(2,'0')} · ${s.t} · ${s.title.toUpperCase()}</figcaption></figure>`).join('');
const ch=document.getElementById('ch');
ch.innerHTML=CH.map((c,i)=>`<li data-t="${c.t}"><span class="t">${c.label}</span><span>${c.title}</span></li>`).join('');
ch.onclick=e=>{const li=e.target.closest('li'); if(!li) return; const v=document.getElementById('v');
  v.currentTime=parseFloat(li.dataset.t); v.play(); window.scrollTo({top:0,behavior:'smooth'})};

async function pollStatus(){
  try{const r=await fetch('render_status.json?ts='+Date.now(),{cache:'no-store'});
    if(!r.ok) throw 0; const j=await r.json();
    const pct=j.total? Math.round(100*j.segs/j.total):0;
    document.getElementById('prog').style.width=pct+'%';
    document.getElementById('progtext').textContent=`encode: ${j.segs}/${j.total} scenes (${pct}%)`+
      (j.started?` · elapsed ${j.elapsed_min} min`:'');
  }catch(e){document.getElementById('progtext').textContent='encode finished or status unavailable';}
}
async function checkVideo(){
  try{const r=await fetch('video/final_1080p.mp4',{method:'HEAD',cache:'no-store'});
    if(r.ok && (+r.headers.get('content-length')||0) > 20e6){ ready(+r.headers.get('content-length')); return true; }
  }catch(e){}
  return false;
}
function ready(bytes){
  document.getElementById('wip').style.display='none';
  document.getElementById('playerbox').style.display='block';
  document.getElementById('finalbox').style.display='block';
  document.getElementById('state').textContent='READY';
  document.getElementById('vmeta').textContent=
    `RUNTIME __RUNTIME__ · ${(bytes/1048576).toFixed(1)} MB · 1080p · STEREO 48 kHz · CAPTIONS INCLUDED`;
  document.querySelector('#playerbox').scrollIntoView({behavior:'smooth',block:'start'});
}
(async()=>{ if(await checkVideo()) return; pollStatus();
  const iv=setInterval(async()=>{ await pollStatus(); if(await checkVideo()) clearInterval(iv); },5000);
  // build the status file even if absent
})();
</script></body></html>
"""

if __name__ == "__main__":
    main()
