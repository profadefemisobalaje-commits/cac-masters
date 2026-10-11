"""Extend Week 1 of CPY 701 to the 35-minute authoring target (~5,200 words).

Adds three slides and their narration:
  - Common Misconceptions (after the scope-of-practice table)
  - What the Evidence Says (after the scientist-practitioner demands)
  - How You Will Be Assessed (before the takeaways)
"""
import json
import sys

PATH = "content/cpy-701/week-01.json"
doc = json.load(open(PATH, encoding="utf-8"))

MISCONCEPTIONS = {
    "layout": "twocol",
    "title": "Common Misconceptions",
    "eyebrow": "Key Concept 5",
    "subtitle": "Each of these beliefs is widespread, and each of them damages either access to care or the quality of it.",
    "columns": [
        {"h": "What people often believe", "items": [
            "Counseling is only for people with serious mental illness.",
            "A counselor mainly listens and then gives advice.",
            "Counseling is essentially the same as talking to a friend or a religious leader.",
            "It only works if you already believe in it.",
        ]},
        {"h": "What is actually the case", "items": [
            "It addresses the whole range of functioning, from a career decision to severe distress.",
            "Listening is a disciplined, trained skill, and advice-giving is generally avoided on purpose.",
            "Natural support is genuinely valuable, but it carries no confidentiality duty, no ethical code and no outcome measurement.",
            "Outcomes are measurable, and they are comparable across treatments.",
        ]},
    ],
    "narration": "Before we leave definition behind, let me address five beliefs that you will meet constantly, in your family, in your church or mosque, in your workplace, and, I am sorry to say, sometimes in your own head. Each of them is widespread, and each of them does real damage. The first misconception is that counseling is only for people with serious mental illness. This belief keeps millions of people away from help, because nobody wants to be told they are mad, and in many communities the stigma attached to that label is severe. The truth is that this profession addresses the full range of human functioning, from a twenty-two year old choosing a career, to a couple navigating a difficult transition, to a person in acute crisis. Coming to see a counseling psychologist is not a declaration that something is deeply wrong with you. It is a decision to use a professional resource for a problem that professional training happens to address. The second misconception is that a counselor mainly listens and then gives advice. Listening is indeed central, but it is a disciplined, trained skill, not a passive one. And advice-giving is generally avoided on purpose, which surprises many students. Rogers' argument, which we have already met, is that the client's own agency is the mechanism of change. If I tell you what to do, I have borrowed your problem for an hour and handed it straight back. If instead I help you clarify what you want and what stands in the way, the change belongs to you and it outlives the session. The third misconception is that counseling is essentially the same as talking to a friend or a religious leader. Let me be careful here, because this is not a claim that professional help is superior to the support of people who love you. It is a claim about what is different. Your friend is not bound by confidentiality, is not obliged by an ethical code, is not trained to assess risk, is not required to keep records, and is not measuring whether what they are doing is working. Those five differences are the profession. The fourth misconception is that it only works if you already believe in it. This is partly true of every treatment, medicine included, and it is called the placebo effect. But it is not the whole story. Psychotherapy produces measurable change that persists, and the effect is larger than placebo alone. The fifth misconception, which I meet in students as often as in the public, is that all psychological treatments are equally effective and therefore it does not matter what you learn. It matters a great deal. We will come to the evidence in a few minutes."
}

EVIDENCE = {
    "layout": "bullets",
    "title": "What the Evidence Says",
    "eyebrow": "Research Spotlight",
    "subtitle": "Five findings every trainee in this programme should be able to state from memory.",
    "bullets": [
        {"t": "Psychotherapy works, and the effect is substantial", "strong": True},
        {"t": "Meta-analytic estimates place the average effect at roughly 0.7 to 0.8 standard deviations — comparable to, or larger than, many medical interventions in routine use.", "lvl": 1},
        {"t": "The alliance predicts outcome across every orientation", "strong": True},
        {"t": "Agreement on goals, agreement on tasks, and the bond between client and clinician predict outcome regardless of the model being used.", "lvl": 1},
        {"t": "Common factors and specific techniques both matter", "strong": True},
        {"t": "The long-running debate between them is a false dichotomy in practice. Effective treatment deliberately uses both.", "lvl": 1},
        {"t": "Transplanting an evidence base without cultural adaptation costs you engagement", "strong": True},
        {"t": "Adapting interventions to the client's cultural context reliably improves retention and outcome for minoritised populations.", "lvl": 1},
        {"t": "The therapist is a measurable source of variance", "strong": True},
        {"t": "Some clinicians consistently achieve better outcomes than others, and the gap can be narrowed with feedback and deliberate practice.", "lvl": 1},
    ],
    "narration": "Now the evidence, because everything I have said so far could be dismissed as professional self-description. Five findings, and I want you to be able to state each of them from memory, with the reasoning behind it. First. Psychotherapy works, and the effect is substantial. When you pool hundreds of trials, the average effect of psychological treatment is somewhere around zero point seven to zero point eight standard deviations. That number means very little until you compare it, so let me compare it. It is comparable to, and in many cases larger than, the effect sizes reported for widely used medical interventions, including several that are routinely prescribed in this country. If you would not describe a drug with that effect size as merely talking, you should not describe psychotherapy that way either. Second. The therapeutic alliance predicts outcome across every theoretical orientation. This is one of the most replicated findings in the whole field. Whatever model you practise, the agreement you reach with your client about what the goals are, the agreement you reach about what tasks you will both do to pursue those goals, and the quality of the bond between you, all predict how well the client does. Notice what this means for your training. It means that your relational skill is not a soft extra sitting on top of your technique. It is an evidence-based component of treatment in its own right. Third, common factors and specific techniques both matter, and the long argument about which is doing the work is a false dichotomy in practice. The alliance may be a common factor, but I cannot build an alliance in the abstract. I build it while doing something, and what I do is the specific technique. Effective clinicians deliberately use both. Fourth. Transplanting an evidence base without cultural adaptation costs you engagement. The trials that established the protocols were largely conducted on European and North American samples. When interventions are sensitively adapted to the client's cultural context, retention and outcome reliably improve for minoritised groups. That finding is the empirical foundation for the multicultural commitment I described earlier. Fifth, and most uncomfortably for you as a trainee, the therapist is a measurable source of variance. Some clinicians consistently achieve better outcomes than others with comparable caseloads, and, crucially, most clinicians believe they are already above average, which cannot be true of all of them. The gap can be narrowed, but only by measuring your own outcomes and using that feedback deliberately. That is the scientist-practitioner cycle again, and it is why I keep returning to it."
}

ASSESSMENT = {
    "layout": "table",
    "title": "How You Will Be Assessed in CPY 701",
    "eyebrow": "Course Administration",
    "subtitle": "Continuous assessment carries 40 per cent; the end-of-block examination carries 60 per cent.",
    "columns": ["Component", "Weight", "Format", "Due"],
    "widths": [0.26, 0.12, 0.36, 0.26],
    "rows": [
        ["Reflective journal", "10%", "400–600 words per entry, submitted weekly", "Weeks 2–16"],
        ["Seminar presentation", "10%", "15-minute presentation plus questions", "Allocated in Week 1"],
        ["Mid-block test", "10%", "60-minute written paper", "Week 2"],
        ["Skills laboratory", "10%", "Recorded micro-counselling session with peer feedback", "Week 3"],
        ["Block examination", "60%", "Written examination covering Weeks 1–4", "Week 4"],
    ],
    "narration": "Finally, the practical matter of how this course is assessed, because I want no one to be surprised in Week Four. Continuous assessment carries forty per cent and the end-of-block examination carries sixty per cent. Your reflective journal is worth ten per cent, and I mean it when I say it is the component students most often underestimate. Four to six hundred words per week from Week Two onward, submitted weekly. It is not a summary of the lecture. It is your thinking about the lecture, and I will be looking for evidence that you have argued with the material rather than copied it. Your seminar presentation is ten per cent, fifteen minutes followed by questions, and allocations will be made by the end of this week. Prepare it as though your colleagues have read the same texts you have, because they will have. The mid-block test in Week Two carries ten per cent and covers the material from Weeks One and Two only. The skills laboratory in Week Three carries ten per cent and involves a recorded micro-counselling session with peer feedback. I want to be direct about that one, because being recorded is uncomfortable for almost everyone. The discomfort is part of the training. You cannot develop counselling skill from reading about it, and you cannot see what you actually do without watching yourself do it. Finally, the block examination in Week Four carries sixty per cent and covers Weeks One to Four. One administrative note. If a placement or an illness prevents you from meeting a deadline, tell me before the deadline, not after it. In a compressed twelve-month programme there is very little slack, and a problem disclosed early is almost always solvable, while a problem disclosed late usually is not."
}

# insert before (0-based) the section-2 divider, the section-4 divider, and the takeaways
doc["slides"].insert(7, MISCONCEPTIONS)
doc["slides"].insert(14, EVIDENCE)
doc["slides"].insert(18, ASSESSMENT)

words = sum(len(s.get("narration", "").split()) for s in doc["slides"])
print(f"slides: {len(doc['slides'])}   words: {words}   est @152wpm: {words/152:.1f} min")
print(f"projected video with padding: {(words/152 + len(doc['slides'])*2.3)/60:.1f} min")
json.dump(doc, open(PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("written", PATH)
