#!/usr/bin/env python3
"""Generate the Lecture Library gallery (index.html) from rendered decks/videos."""
import os, sys, json, glob
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "studio"))
OUT = os.path.join(REPO, "out")

SEM_ORDER = ["First Semester", "Second Semester", "Third Semester", "Electives"]

def main():
    metas = []
    for jf in sorted(glob.glob(os.path.join(OUT, "videos", "*_lecture.json"))):
        metas.append(json.load(open(jf)))
    decks = []
    for pf in sorted(glob.glob(os.path.join(OUT, "posters", "*.jpg"))):
        sl = os.path.basename(pf)[:-4]
        decks.append(sl)
    # load subject titles from data
    titles = {}
    for jf in glob.glob(os.path.join(REPO, "studio", "data", "subjects", "*.json")):
        c = json.load(open(jf))
        from engine.assemble import slug
        titles[slug(c)] = c
    html = []
    html.append(HEAD)
    # videos section
    html.append("<section class='hero'><div class='kicker'>TRIUNE BIBLICAL UNIVERSITY · GLOBAL EXTENSION USA</div>")
    html.append("<h1>Master in Children &amp; Adolescent Counseling</h1>")
    html.append("<p class='sub'>Professionally designed 720p video-lecture library · unique template per course · voice narration</p>")
    html.append(f"<p class='stats'>{len(metas)} video lecture(s) · {len(decks)} designed course deck(s) · 608 planned library hours</p>")
    totals = {}
    for jf in glob.glob(os.path.join(REPO, "studio", "data", "subjects", "*.json")):
        c = json.load(open(jf))
        totals[c["sem"]] = totals.get(c["sem"], 0) + c["hours"]
    html.append("<div class='hours'>")
    for sem in SEM_ORDER:
        if sem in totals:
            html.append(f"<div class='hcell'><div class='hnum'>{totals[sem]}</div><div class='hlab'>{sem}</div></div>")
    html.append(f"<div class='hcell total'><div class='hnum'>{sum(totals.values())}</div><div class='hlab'>Total Library Hours</div></div></div>")
    html.append("</section>")
    if metas:
        html.append("<h2 class='sec'>Video Lectures (720p)</h2><div class='grid'>")
        for m in metas:
            state = m.get("state", "full")
            label = {"full": "fully narrated", "partial": "narrated + on-screen text", "silent": "on-screen text"}.get(state, state)
            html.append(f"""<a class='card' href='videos/{m["video"]}'><img src='posters/{os.path.basename(m["poster"])}' alt=''>
            <div class='cbody'><div class='code'>{m['code']}</div><div class='ct'>{m['title']}</div>
            <div class='cmeta'>{m['sem']} · {m['hours']}h planned · {round(m['duration']/60,1)} min · {label}</div></div></a>""")
        html.append("</div>")
    html.append("<h2 class='sec'>Course Design Templates (720p)</h2><div class='grid'>")
    for sl in decks:
        c = titles.get(sl)
        if not c: continue
        html.append(f"""<div class='card deck'><img src='posters/{sl}.jpg' alt=''>
        <div class='cbody'><div class='code'>{c['code']}</div><div class='ct'>{c['title']}</div>
        <div class='cmeta'>{c['sem']} · {c['hours']}h · unique template</div></div></div>""")
    html.append("</div>")
    html.append(FOOT)
    open(os.path.join(OUT, "index.html"), "w").write("\n".join(html))
    print("gallery written:", len(metas), "videos,", len(decks), "decks")

HEAD = """<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>CAC Masters — Lecture Library</title><style>
*{margin:0;box-sizing:border-box}body{background:#0b0e14;color:#e8e3d8;font-family:Georgia,serif}
.hero{padding:70px 8% 40px;text-align:center;background:linear-gradient(180deg,#101827,#0b0e14)}
.kicker{letter-spacing:.35em;font-size:11px;color:#c9a227;text-transform:uppercase}
h1{font-size:44px;margin:14px 0 8px;font-weight:600}
.sub{color:#a9a294;font-style:italic}.stats{margin-top:14px;color:#c9a227;font-size:13px;letter-spacing:.12em}
.hours{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:26px}
.hcell{border:1px solid #2a3242;border-radius:10px;padding:14px 26px;background:#121826}
.hnum{font-size:30px;color:#c9a227}.hlab{font-size:11px;letter-spacing:.18em;color:#8b93a3;text-transform:uppercase;margin-top:4px}
.hcell.total{border-color:#c9a227}
.sec{padding:36px 8% 8px;font-size:22px;color:#e8e3d8;border-top:1px solid #1d2430;margin-top:24px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px;padding:18px 8% 40px}
.card{background:#121826;border:1px solid #232c3d;border-radius:10px;overflow:hidden;text-decoration:none;color:inherit;transition:.2s}
.card:hover{transform:translateY(-3px);border-color:#c9a227}
.card img{width:100%;display:block}
.cbody{padding:14px 16px 18px}
.code{color:#c9a227;font-size:12px;letter-spacing:.2em}
.ct{font-size:17px;margin:6px 0}
.cmeta{color:#8b93a3;font-size:12px}
footer{padding:30px 8%;color:#66707f;font-size:12px;border-top:1px solid #1d2430}
</style></head><body>"""
FOOT = """<footer>CAC Lecture Studio · Triune Biblical University Global Extension USA · Master in Children and Adolescent Counseling · 100% Online · 608 planned video hours</footer></body></html>"""

if __name__ == "__main__":
    main()
