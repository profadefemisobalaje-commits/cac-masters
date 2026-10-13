"""CAC Lecture Studio - narration composer (final).
Builds a ~30-minute orientation lecture per subject from its curriculum
record. Phrasing pools are seeded per course so the 31 lectures read distinct."""
import hashlib

def seed_of(code): return int(hashlib.md5(code.encode()).hexdigest(), 16)

ONES = ["zero","one","two","three","four","five","six","seven","eight","nine"]
def spoken_code(code):
    code = code.replace("*", "")
    pre, num = code.split(".", 1) if "." in code else (code[:3], code[3:])
    return " ".join(l.upper() + "." for l in pre) + " " + " ".join(ONES[int(ch)] if ch.isdigit() else ch for ch in num)

V = {
"welcome": [
 "Welcome, and thank you for being here.",
 "It is a privilege to welcome you to this course.",
 "Welcome. Settle in, because we have meaningful work ahead of us.",
 "Thank you for joining me. This is one of the courses I treasure most in this programme.",
],
"module_open": [
 "We begin with Module {i}: {name}.",
 "Module {i} carries the title {name}.",
 "This brings us to Module {i}, {name}.",
 "Our next milestone is Module {i}: {name}.",
 "Module {i} is where we study {name}.",
 "And now, Module {i} — {name}.",
 "Here is Module {i}, which we call {name}.",
],
"module_mid": [
 "Across {h} hours of video instruction, this module",
 "In the {h} hours devoted to this module, the lecture series",
 "Within this module's {h} hours of recorded lectures, the teaching",
 "This module occupies {h} hours of our video library, and it",
],
"topic_elab": [
 "When we take up {t}, you will see how it appears in real sessions with young clients.",
 "The section on {t} is where many students tell me the course first comes alive.",
 "We will give careful attention to {t}, because it so often decides outcomes in practice.",
 "As we work through {t}, keep your own questions close; this is where theory meets the desk.",
],
"demo": [
 "On camera, you will watch a demonstration built around {t}, paused and annotated so you can see the counselor's reasoning, not just the counselor's actions.",
 "This module includes a filmed demonstration touching {t}, with the practitioner thinking aloud between interventions.",
 "You will also observe a clinical vignette dramatization on {t}, followed by a frame-by-frame debrief.",
],
"takeaway": [
 "Carry one sentence from this module into the next: write it down and keep it.",
 "By the end of this module, you should be able to explain it to a colleague in two minutes; practice that.",
 "Your aim here is simple: be able to say what you would do next, and why, without hesitation.",
],
"watch_for": [
 "Let me tell you what to watch for in this module.",
 "Here is how I suggest you enter this module.",
 "A word about how to study this module well.",
 "Let me prepare you for what this module will ask of you.",
],
"why_matters": [
 "You might ask why this deserves such attention.",
 "Why does this matter so much in practice?",
 "Let me tell you why this module earns its place.",
 "The reason this module matters is simple, and it is profound.",
],
"practice_lead": [
 "Now let us speak about how you will practice what you learn.",
 "Knowledge without practice is incomplete, so let me describe the practical side of this course.",
 "This programme is clinical at heart, and so is this course. Here is how the practical work unfolds.",
],
"assess_lead": [
 "Let me also be transparent about assessment.",
 "How will you know you have mastered this material? Let me explain the assessments.",
 "Assessment in this course is designed to build competence, not merely to measure it.",
],
"succeed_lead": [
 "Before we part, allow me to share how to succeed in this course.",
 "Permit me a few words of guidance on how to study this material well.",
 "Students who thrive in this course share a few habits. Let me pass them to you.",
],
"closing": [
 "Until we meet in the next lecture, go in peace, and go with purpose.",
 "May your study be rich, and may it serve the young lives entrusted to your care.",
 "I look forward to continuing this journey with you. Until then, take good care.",
],
"outcome_note": [
 "In assessment terms, this means you will be asked to demonstrate it, not merely recognize it.",
 "Notice that this outcome is observable; you will show it in writing, in speech, or in practice.",
 "This is one of the outcomes examiners return to most often, so give it honest effort.",
 "Expect this outcome to surface again in your practicum; it is built here so it can be used there.",
],
}

def pick(pool, seed, salt): return pool[(seed + salt) % len(pool)]

def _t(parts, target=1490):
    txt = " ".join(p.strip() for p in parts if p).replace("  ", " ")
    if len(txt) <= target: return txt
    # cut at the last sentence boundary that fits
    cut = txt[:target]
    for sep in (". ", "! ", "? "):
        idx = cut.rfind(sep)
        if idx != -1:
            return cut[:idx+1].strip()
    return cut.strip()

def build_script(c):
    S = seed_of(c["code"]); sc = spoken_code(c["code"]); seg = []
    n_mod = len(c["modules"]); total_h = c["hours"]; outc = c["outcomes"]
    figs = c["figures"]
    if figs and isinstance(figs[0], str):
        figs = list(zip(figs[0::2], figs[1::2]))
    c = dict(c); c["figures"] = figs

    seg.append(dict(id="s01_open", slides=[("opener",{},1.0),("title",{},2.0)],
        text=_t([
            pick(V["welcome"], S, 1),
            f"This is {sc}, {c['title']}, presented by Triune Biblical University Global Extension USA within the Master in Children and Adolescent Counseling programme.",
            f"Over {c['hours']} hours of professionally recorded video instruction, carrying 1.6 course units, this course belongs to the {c['sem'].lower()} of your degree.",
            f"{c['tagline']}",
            c.get("welcome",""),
            "This opening lecture is your orientation. In the next half hour I will tell you what this course is, why it matters, whose shoulders we stand on, what you will be able to do by the end of it, and precisely how every module, demonstration, and assessment fits together.",
            "I will also share the study habits that separate strong students from struggling ones, and the rhythm of a sustainable semester.",
            "And let me tell you what this programme is forming. Not merely graduates with a certificate, but counselors whose judgment can be trusted with a child's inner life. Every course on your semester list serves that single end, and this one is a cornerstone of it.",
            "Take notes, and listen to the whole lecture before you plan your weeks. This half hour will save you many hours later."
        ])))

    seg.append(dict(id="s02_agenda", slides=[("agenda",{},1.2),("stats",{},1.1)],
        text=_t([
            "Let me first show you what this orientation covers, so you can follow the movement of the lecture.",
            "We will move through several stations. First, a story from real practice that reveals why this course exists, and the case companions who will travel with us through the whole series. Second, the portrait of the course itself: its intellectual territory and the great questions it asks. Third, the voices and figures whose work we will inherit. Fourth, the learning outcomes, stated clearly, so you know exactly what competence looks like here. Fifth, a guided tour of every module, including how the video hours are allocated. Sixth, the clinical demonstrations, the practical components, and the assessments. And finally, how to study this course well and how it connects to the rest of your degree.",
            f"A word about numbers. You see {total_h} hours of video, 1.6 course units, and {n_mod} modules. Those are not arbitrary figures. Every hour is placed where theory, demonstration, or practice most demands it, and the module map later in this lecture will show you exactly how.",
            "With that map in hand, let us begin at the beginning, with a moment from practice."
        ])))

    seg.append(dict(id="s03_vignette", slides=[("vignette",{},1.0),("bullets",("CASE COMPANIONS","The Young Clients Who Will Teach Us"),1.1)],
        text=_t([
            "Listen carefully to this scene, and imagine yourself inside it.",
            c["vignette"],
            "Sit with the scene for a moment. What would you say next? What would you avoid doing? What would you need to know, about development, about ethics, about technique, before you could act with confidence?",
            "Give that young person a name in your mind, because they are the first of our case companions. Across the full lecture series we will return again and again to companion cases like these: " + "; ".join(c.get("cases", ["the young person from our opening scene", "a family learning new patterns together", "an adolescent searching for a durable identity"])) + ".",
            f"Each module will ask, in its own way: what does this material change for them? Hold that question, because everything in {c['title']} exists for moments exactly like the one I just described. When you finish this course, you will meet such moments prepared, not improvised. That is the promise of this course, and it is a promise we intend to keep."
        ])))

    seg.append(dict(id="s04_why", slides=[("heading",("WHY THIS COURSE MATTERS","Formation for Real Practice"),0.8),("bullets",("WHY THIS COURSE MATTERS","Three Reasons This Course Matters"),1.4)],
        text=_t([
            "Why does this course matter so much in a master's programme devoted to children and adolescents?",
            "I will give you three reasons, and I ask you to weigh each one. " + " ".join(f"Reason {i+1}: {r}." for i, r in enumerate(c["importance"])),
            "Before I continue, let us also set down two misconceptions you may carry. " + " ".join(f"Misconception {i+1}: {m}." for i, m in enumerate(c.get("misconceptions", ["that the material is merely academic", "that one method fits every child"]))) + " Set those down at the door; they will not serve you here.",
            f"Put the three reasons together and you see the design of the whole. This course is where knowledge becomes readiness. The {total_h} hours before you are an investment in the moments when a child, an adolescent, or a family will be depending on what you know and who you have become.",
            "That is a sobering thought, and it is meant to be. Let it make you a serious student."
        ])))

    seg.append(dict(id="s05_portrait", slides=[("heading",("THE COURSE PORTRAIT","Intellectual Territory"),0.8),("bullets",("THE COURSE PORTRAIT","The Territory We Will Cover"),1.4)],
        text=_t([
            "Now, the portrait of the course itself.",
            c["description"],
            "Notice what this description implies. It implies that you will not be a passive viewer. You will be asked to think, to compare, to judge between options, and to defend your judgments with evidence and with ethics.",
            "It also implies integration. Nothing in this course stands alone. Every idea reaches toward real young people in real settings, in clinics and classrooms, in homes and congregations, and in the quiet corners where young hearts ask their hardest questions.",
            "And it implies humility before the evidence. Where the research base is strong, we will say so plainly; where it is emerging, we will say that too. You deserve a course that distinguishes conviction from preference, and this one will."
        ])))

    seg.append(dict(id="s06_questions", slides=[("bullets",("THE GREAT QUESTIONS","Questions That Guide Us"),1.2)],
        text=_t([
            "Every serious course is organized around great questions. Ours are these.",
            " ".join(f"Question {i+1}: {q}" + ("" if q.strip().endswith("?") else ".") for i, q in enumerate(c["questions"])),
            "You will notice these questions returning in every module, like a melody that gathers harmonies as it goes. By the final lecture, you will be answering them with confidence, with evidence, and with professional humility.",
            "Write the questions on the first page of your notes and return to them each week. A course organized by questions keeps you honest; a course organized by trivia keeps you busy. We have chosen the former.",
            "Now, before we meet the outcomes, let me introduce the company of thinkers whose shoulders we will stand on."
        ])))

    seg.append(dict(id="s06b_figures", slides=[("bullets",("VOICES WE WILL MEET","Figures Who Shaped This Field"),1.3),("bullets",("WHERE THIS KNOWLEDGE LIVES","Settings for Your Future Practice"),1.0)],
        text=_t([
            "No discipline is built by anonymous hands. In this course you will meet the figures whose work made our work possible.",
            " ".join(f"{n}, {w}." for n, w in c["figures"]),
            "When you learn their ideas, you are joining a conversation across generations. Learn their names, learn what each one insisted upon, and learn one criticism of each; admiration without critique is not scholarship.",
            "And where does this knowledge live once you graduate? It lives here: " + "; ".join(c["settings"]) + ".",
            "Wherever you eventually serve, the content of this course was designed to travel with you."
        ])))

    half = (len(outc)+1)//2
    for k, chunk in enumerate([outc[:half], outc[half:]]):
        base = 0 if k == 0 else half
        slides = [("outcome",(base+i+1, len(outc), o[0], o[1]),1.35) for i, o in enumerate(chunk)]
        intro = ("These are the learning outcomes, the abilities this course promises to build in you. Let me walk through them one by one, because they are the contract between this course and you." if k==0
                 else "Let us continue with the remaining outcomes.")
        body = " ".join(f"Outcome {base+i+1}: {o[0]}. {o[1]} {pick(V['outcome_note'], S, base+i)}" for i, o in enumerate(chunk))
        outro = ("Hold these outcomes in view as we tour the modules; you will see exactly where each one is built." if k==0
                 else "Taken together, these outcomes describe a counselor who is thoughtful, skilled, and trustworthy. That is the graduate this programme intends to form.")
        seg.append(dict(id=f"s07_outcomes_{'a' if k==0 else 'b'}", slides=slides,
                        text=_t([intro, body, outro])))

    for i, (name, h, topics, why) in enumerate(c["modules"], 1):
        opener = pick(V["module_open"], S, i).format(i=i, name=name)
        mid = pick(V["module_mid"], S, i+3).format(h=h)
        wm = pick(V["why_matters"], S, i+5)
        lead = "Let me show you the road we will travel together, module by module, and let the map stay open beside you as we go." if i == 1 else ""
        topic_text = " ".join(pick(V["topic_elab"], S, i*3+j).format(t=t) for j, t in enumerate(topics))
        demo = pick(V["demo"], S, i*5+1).format(t=topics[0].lower() if topics else name.lower())
        take = pick(V["takeaway"], S, i*7+2)
        seg.append(dict(id=f"s09_mod{i:02d}",
                        slides=[("heading",(f"MODULE {i} OF {n_mod}", name),0.75),("module",(i, n_mod, name, h, topics, why),1.7)],
                        text=_t([
                            lead, opener,
                            f"{mid} {' covers ' if i%2 else ' moves through '}" + "; ".join(topics) + ".",
                            topic_text,
                            f"{demo}",
                            f"{wm} {why}",
                            f"{take} {pick(V['watch_for'], S, i+7)} This module leans on what came before it and prepares what follows; that deliberate sequencing is the backbone of the whole course. When our companion cases appear in this module's exercises, slow down; they carry more than they say. When you finish the module, return to them and ask what you could now do for them that you could not do before."
                        ])))

    seg.append(dict(id="s15_rehearsal", slides=[("heading",("A GUIDED REHEARSAL","Practicing the Five-Step Rhythm"),0.8),("bullets",("A GUIDED REHEARSAL","Notice · Name · Choose · Consult · Act"),1.3)],
        text=_t([
            "Before we reach the practical details, let us rehearse together, so you feel the rhythm this course will build into you.",
            "Return to our young companion from the opening scene. Step one, notice: describe only what you can see and hear, without judgment. The drawings have darkened; the silence has grown; the outbursts are new. Step two, name: attach the concepts this course gives you, drawing on " + c["modules"][1][0] + " and " + c["modules"][3][0] + ". Naming is diagnosis in the broad, careful sense.",
            "Step three, choose: hold two or three possible responses in mind at once, and weigh them honestly. Step four, consult: check the ethics code, the culture of the family, and your supervisor's calendar, in that order of humility. And step five, act and reflect: intervene, then write down what the moment taught you.",
            "Notice, name, choose, consult, act. Five steps, practiced until they are reflex. That rhythm is the heartbeat of the whole series, and by your final lecture you will run it without thinking, which is exactly what a child in crisis needs from you."
        ])))

    seg.append(dict(id="s16_practice", slides=[("bullets",("CLINICAL PRACTICE","Learning by Doing"),1.15),("bullets",("ASSESSMENT","How Competence Is Shown"),1.15)],
        text=_t([
            pick(V["practice_lead"], S, 2),
            c["practicum"][0],
            "Here are its components. " + " ".join(f"{p}. " for p in c["practicum"][1]),
            "Throughout the series you will also watch filmed clinical demonstrations: sessions paused at decision points, the practitioner thinking aloud, the supervisor commenting, and the same scene replayed so you can compare first impressions with trained observation. Demonstrations are not entertainment; they are supervised eyes.",
            "Treat every rehearsal as real service, because one day, without warning, it will be.",
            pick(V["assess_lead"], S, 4),
            c["assessment"][0],
            "The assessments are: " + "; ".join(c["assessment"][1]) + ".",
            "My counsel is simple: begin each assessment the week it is assigned, not the week it is due. Mastery in counseling is built in steady layers, not in midnight surges."
        ])))

    seg.append(dict(id="s17_succeed", slides=[("bullets",("HOW TO SUCCEED","Habits of Strong Students"),1.15),("roadmap",{},1.25)],
        text=_t([
            pick(V["succeed_lead"], S, 6),
            " ".join(f"Habit {i+1}: {t}." for i, t in enumerate(c["tips"])),
            "Students also ask three questions so often that I answer them now. First: is this course mostly theory or mostly practice? It is both, woven together; the theory tells you why, the practice shows you how, and the assessments require both at once. Second: how much should I read beyond the videos? Read the assigned sources deeply rather than widely; one chapter owned is worth ten skimmed. Third: will this prepare me for supervised practice and internship? It is designed precisely as the foundation for them; your internship hours remain separate and sacred, but this course makes those hours count.",
            c["integration"],
            f"Remember the figure you saw at the start: {total_h} hours of video. Spread across a semester, that is roughly five to six hours of lecture a week, plus your reflection and practice. Plan your calendar around it now, and the course will reward you."
        ])))

    seg.append(dict(id="s17b_faith", slides=[("heading",("FAITH AND VOCATION","Serving With the Whole Person"),0.8),("bullets",("FAITH AND VOCATION","The Vocation Before You"),1.1)],
        text=_t([
            "One more dimension belongs in this orientation, and it is dear to our institution.",
            c["faith"],
            "This university believes that rigorous science and sincere faith do not compete; they keep each other honest. Bring both to this course. Your young clients will sense the difference between a technician and a person whose work flows from conviction.",
            "Vocation is not a decoration we hang on the wall. It is the reason we study carefully, practice humbly, and refuse to waste a single hour of the trust placed in us. Let that be the spirit in which you take this course."
        ])))

    weeks = 15
    per_week = round(total_h / weeks, 1)
    seg.append(dict(id="s17c_library", slides=[("bullets",("THE VIDEO LIBRARY","How to Watch These Lectures"),1.1),("stats",{},0.8)],
        text=_t([
            "Because this entire course is delivered as professionally recorded video lectures, let me teach you how to watch them well.",
            "First, watch actively, with your notebook open and the pause button under your thumb. Pause after every major point and restate it in your own words; that single habit doubles retention.",
            "Second, watch demonstrations twice. The first viewing is for the flow of the session; the second is for the technique, the timing, and the counselor's choices.",
            "Third, keep a running case file on our companion cases, so your learning accumulates in one place rather than scattering across thirty notebooks. Fourth, form a viewing covenant with one or two classmates: watch alone, then meet to compare notes and rehearse skills aloud.",
            f"Finally, pace the library deliberately. {total_h} hours of video across roughly fifteen weeks means about {per_week} hours a week; a steady rhythm beats a heroic binge. A little each week, deeply watched, will carry you further than marathon weekends."
        ])))

    seg.append(dict(id="s18_close", slides=[("closing",{},1.5),("credits",{},1.2)],
        text=_t([
            "And so we arrive at the close of this orientation.",
            f"You now know what {c['title']} is, why it matters, whose shoulders we stand on, what it promises to build in you, and how its {n_mod} modules and {total_h} hours are arranged to do that building. You know how you will practice, how you will be assessed, and how strong students study.",
            "In the first full lecture of the series, we enter Module 1 together, notes open and map in hand, and the real work begins.",
            c["closing"],
            pick(V["closing"], S, 7),
            f"This has been {sc}, {c['title']}, an introductory lecture of Triune Biblical University Global Extension USA, Master in Children and Adolescent Counseling. {c['hours']} hours of video instruction, 1.6 course units, {c['sem']}."
        ])))

    for s in seg:
        assert len(s["text"]) <= 1500, (s["id"], len(s["text"]))
        s["clips"] = [s.pop("text")]
    return seg

if __name__ == "__main__":
    import json, sys
    for f in sys.argv[1:]:
        c = json.load(open(f))
        segs = build_script(c)
        tot = sum(len(s['text']) for s in segs)
        print(f, tot, "chars in", len(segs), "segments ~", round(tot/970,1), "min of speech")
