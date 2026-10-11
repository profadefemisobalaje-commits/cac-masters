"""Render one slide of every layout type into out/demo/ for visual QA."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import slidekit as SK
from PIL import Image

F = {"footer_left": "CPY 701 · Week 1", "footer_right": "n / 14"}

SPECS = [
 {"layout":"title","course":"CPY 701","title":"Introduction to Counseling Psychology",
  "subtitle":"Week 1 — What Counseling Psychology Is","week":"Week 1 of 16",
  "lecturer":"Prof. S.M.A. Philips","institution":"Triune Biblical University Global Extension, USA","duration":"35 minutes",**F},
 {"layout":"section","number":"1","eyebrow":"Part One","title":"Defining the Field",
  "subtitle":"What counseling psychology is, and what it is not.",**F},
 {"layout":"objectives","title":"Learning Objectives","eyebrow":"By the end of this lecture","items":[
   "Define counseling psychology and distinguish it from clinical psychology and psychiatry.",
   "Trace the historical development of the profession from vocational guidance to evidence-based practice.",
   "Describe the scientist-practitioner model and its implications for training.",
   "Identify the core values and ethical commitments of the profession.",
   "Explain the scope of practice in the Nigerian and African context."],**F},
 {"layout":"bullets","title":"The Three Mental Health Professions","eyebrow":"Concept 1.2",
  "subtitle":"Overlapping but distinct scopes of practice.","bullets":[
   {"t":"Psychiatry — a medical specialty","strong":True},
   {"t":"Diagnoses and prescribes medication; five-year medical training plus residency.","lvl":1},
   {"t":"Counseling psychology — a psychological specialty","strong":True},
   {"t":"Focuses on normative development, prevention, and brief interventions.","lvl":1},
   {"t":"Clinical psychology — a psychological specialty","strong":True},
   {"t":"Historically oriented toward severe psychopathology and long-term treatment.","lvl":1}],**F},
 {"layout":"definition","title":"What Is Counseling Psychology?","eyebrow":"Key Concept",
  "term":"Counseling Psychology",
  "body":"A psychological specialty that facilitates personal and interpersonal functioning across the lifespan, with a focus on emotional, social, vocational, educational, health-related, developmental and organisational concerns.",
  "source":"Adapted from the Society of Counseling Psychology (Division 17, APA).",
  "footnote":"Note the emphasis on the lifespan, on strengths rather than deficits, and on functioning rather than disorder.",**F},
 {"layout":"twocol","title":"Core Commitments of the Specialty","eyebrow":"Concept 1.4","columns":[
   {"h":"Values","items":["Respect for human dignity","Strengths-based orientation",
    "Cultural humility","Social justice advocacy"]},
   {"h":"Practices","items":["Assessment and diagnosis","Individual and group psychotherapy",
    "Career and vocational counselling","Prevention and psychoeducation"]}],**F},
 {"layout":"table","title":"Scope of Practice Compared","eyebrow":"Table 1.1",
  "columns":["Profession","Degree","Prescribes?","Primary focus"],
  "widths":[0.24,0.24,0.18,0.34],
  "rows":[["Psychiatrist","MD / MBBS","Yes","Biological treatment of mental disorder"],
          ["Clinical psychologist","PhD / DPsych","No","Psychopathology and assessment"],
          ["Counseling psychologist","MA / MSc / PhD","No","Lifespan functioning and prevention"],
          ["Counsellor","BA / MA","No","Supportive and developmental work"]],**F},
 {"layout":"casestudy","title":"Vignette: Tolu, Age 29","eyebrow":"Case Vignette","paragraphs":[
   "Tolu is a 29-year-old bank officer who presents with persistent worry about job security, difficulty sleeping, and a sense that she is 'stuck'. She has no history of psychiatric hospitalisation and no current substance use. She says she wants 'someone to talk to about where my life is going.'",
   "She is unsure whether she needs 'a doctor or a counsellor'."],
  "questions":["Which profession is the most appropriate point of entry, and why?",
               "What assessment questions would you ask before deciding?"],**F},
 {"layout":"stats","title":"The Scale of the Need","eyebrow":"Context","stats":[
   {"v":"1 in 4","l":"people will experience a mental health problem in their lifetime"},
   {"v":"<10%","l":"receive any form of professional care in low-income settings"},
   {"v":"1.4M","l":"estimated mental health workforce gap across Africa"},
   {"v":"70%","l":"of the global treatment gap sits in low- and middle-income countries"}],
  "note":"These figures frame why task-shifting and expanded counselling capacity matter in the Nigerian context.",**F},
 {"layout":"process","title":"The Scientist-Practitioner Cycle","eyebrow":"Concept 1.6",
  "subtitle":"How research and practice inform each other.","steps":[
   {"h":"Observe","b":"Client work raises a question"},
   {"h":"Read","b":"Appraise the best available evidence"},
   {"h":"Plan","b":"Integrate evidence, values, context"},
   {"h":"Act","b":"Deliver the intervention with fidelity"},
   {"h":"Measure","b":"Monitor outcomes each session"},
   {"h":"Feed back","b":"Share what was learned"}],**F},
 {"layout":"quote","title":"","eyebrow":"",
  "quote":"Counseling psychology is not merely the application of technique. It is a disciplined relationship in the service of another person's growth.",
  "attribution":"Carl R. Rogers, 1961",**F},
 {"layout":"takeaways","title":"Key Takeaways","eyebrow":"Summary","items":[
   "Counseling psychology is a distinct psychological specialty centred on lifespan functioning, prevention and strengths.",
   "It is differentiated from psychiatry by training and prescribing rights, and from clinical psychology by historical emphasis rather than by sharp boundaries.",
   "The scientist-practitioner model commits the profession to evidence-informed practice.",
   "In Nigeria and across Africa, the specialty carries an added mandate of access, task-shifting and cultural relevance."],**F},
 {"layout":"reading","title":"Required Reading for This Week","eyebrow":"Reading List","items":[
   "Gelso, C. J., Nutt Williams, E., & Fretz, B. R. (2014). Counseling Psychology (3rd ed.). American Psychological Association. — Chapter 1.",
   "Woolfe, R., Strawbridge, S., Douglas, B., & Kasket, E. (2019). Handbook of Counselling Psychology (4th ed.). SAGE. — Chapter 1.",
   "Philips, S. M. A. (2024). Counselling Psychology: Scope, Training and Practice. Triune Biblical University Press.",
   "Journal of Counseling Psychology — browse the current issue and note one empirical study that interests you.",
   "American Psychological Association. (2017). Ethical Principles of Psychologists and Code of Conduct. — Sections A and B."],**F},
 {"layout":"end","title":"End of Week 1","eyebrow":"Thank You",
  "body":"Next week we examine the theoretical foundations that shape how counselors understand human change.",
  "next":["Read Gelso et al., Chapter 2 before the next session.",
          "Submit your reflective journal entry by Friday 23:59.",
          "Begin your thesis topic exploration — Milestone 1 opens in Week 9."],**F},
]

if __name__ == "__main__":
    out = "media/demo"
    os.makedirs(out, exist_ok=True)
    imgs = []
    for i, sp in enumerate(SPECS):
        im = SK.render(sp)
        p = f"{out}/{i:02d}_{sp['layout']}.png"
        im.save(p)
        imgs.append((sp['layout'], im))
        print("ok", p)
    # contact sheet: 3 cols
    cols, tw, th = 3, 640, 360
    rows = (len(imgs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (230, 234, 238))
    for i, (_, im) in enumerate(imgs):
        sheet.paste(im.resize((tw - 8, th - 8), Image.LANCZOS), ((i % cols) * tw + 4, (i // cols) * th + 4))
    sheet.save(f"{out}/_contact-sheet.png")
    print("contact sheet ->", f"{out}/_contact-sheet.png")
