"""Figures for Part One — The Silent World of Men (Chapters 1-4)."""
from figlib import Fig, matrix
import diagrams as d

FIGS = {}


def _fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Chapter 1
@_fig("fig-01-01")
def fig_01_01():
    d.iceberg(
        "fig-01-01",
        "What the people around him can see: competence, calm, provision, and the management of everything",
        ["Debt and the fear of financial collapse",
         "A marriage that has gone quiet",
         "Anxiety about the future he cannot voice",
         "A grief he has never spoken about",
         "Doubts about his own worth that never rest",
         "Physical exhaustion he calls ordinary tiredness"],
        visible_label="THE PUBLIC ACCOUNT",
        hidden_label="THE PRIVATE ACCOUNT")


@_fig("fig-01-02")
def fig_01_02():
    d.cycle("fig-01-02", [
        "Distress he cannot name",
        "He judges that speaking would be weak or disloyal",
        "He conceals it and keeps performing",
        "Others read his calm as evidence that all is well",
        "Support is not offered, so isolation deepens",
        "He concludes that he must manage alone",
    ], centre="The silence loop")


@_fig("fig-01-03")
def fig_01_03():
    d.compare(
        "fig-01-03",
        "What achievement can supply", [
            "Respect and public standing",
            "Invitations, titles, and recognition",
            "Being asked for advice",
            "Material security for his household",
            "Evidence of competence that others can see",
        ],
        "What achievement cannot supply", [
            "Someone who asks how he actually is",
            "Permission to admit fear or doubt",
            "Conversations that are not about a task",
            "A person who will tell him the truth",
            "The experience of being known rather than counted upon",
        ], style_r="bronze")


@_fig("fig-01-04")
def fig_01_04():
    matrix("fig-01-04",
           ["Shared readily", "Shared selectively", "Almost never shared"],
           [["Work", "Achievements, plans, promotions", "Uncertainty, unfair treatment",
             "Fear that he is not competent"],
            ["Money", "Major purchases, investments", "Moderate shortfalls",
             "Debt, inability to provide, loss of income"],
            ["Health", "Injuries with a visible cause", "Chronic conditions",
             "Pain that suggests anxiety or depression"],
            ["Marriage", "Anniversaries, milestones", "Ordinary disagreements",
             "Loneliness within the marriage, loss of intimacy"],
            ["Grief", "Funeral arrangements, responsibilities", "Memories with close relatives",
             "The grief itself, especially for a child or a parent"],
            ["Self-image", "Public roles and titles", "Career ambitions",
             "Shame, regret, and the sense of being a fraud"]],
           first_w=15, size=6.9)


@_fig("fig-01-05")
def fig_01_05():
    d.sequence("fig-01-05", [
        "The event or accumulation|A loss, a debt, a diagnosis, a separation, or simply years of pressure.",
        "The private interpretation|What it means about him as a man: that he has failed, is failing, or will fail.",
        "The calculation|Weighing disclosure against what it may cost him at home, at work, and in the community.",
        "The decision to carry it|Silence is chosen, not because he feels nothing, but because speech appears more dangerous.",
        "The cost|Sleep, health, marriage, work, and the ability to feel anything at all.",
    ], note="The process is usually invisible to the man as well as to everyone else; each step is experienced as a fact rather than a choice.")


# ---------------------------------------------------------------- Chapter 2
@_fig("fig-02-01")
def fig_02_01():
    d.pillars("fig-02-01",
              "The manhood examination: what a man believes he is being assessed on",
              ["Provide", "Protect", "Perform", "Endure", "Decide", "Control feelings"],
              "The unspoken syllabus — an assessment with no examiner, no timetable, and no certificate")


@_fig("fig-02-02")
def fig_02_02():
    d.cards("fig-02-02", [
        "The man at the centre|He is the point at which every ring of demand meets, and the party who is expected to answer each of them.",
        "Partner and children|Expectations of provision, presence, and calm.",
        "Extended family|School fees, hospital bills, mediation, hospitality.",
        "Community and association|Contributions, leadership, reputation.",
        "Workplace|Reliability, output, and the absence of complaint.",
    ], cols=2, w=4.6, h=4.4, size=7.2,
       note="The rings are concentric in experience: each one is close enough to be felt, and none of them is entirely outside the man's responsibility.")


@_fig("fig-02-03")
def fig_02_03():
    d.compare("fig-02-03", "Strength as endurance", [
        "Never shows strain",
        "Measures worth in bearing burdens alone",
        "Treats rest as weakness",
        "Silence reads as dependability",
        "Crisis arrives without warning",
    ], "Strength as capacity", [
        "Shows strain to those who can help",
        "Measures worth in responsibility discharged well",
        "Treats rest as maintenance",
        "Truth-telling reads as dependability",
        "Difficulties are addressed while manageable",
    ])


@_fig("fig-02-04")
def fig_02_04():
    d.funnel("fig-02-04", [
        "What society asks of men in general",
        "What his family expects of him in particular",
        "What his workplace assumes about him",
        "What he tells himself he must be",
        "The narrow role he is actually permitted to occupy",
    ], note="Each layer narrows the range of feeling and need that a man is allowed to express.")


# ---------------------------------------------------------------- Chapter 3
@_fig("fig-03-01")
def fig_03_01():
    d.compare("fig-03-01", "Self-control", [
        "Feels the emotion fully and knows what it is",
        "Chooses the time, place, and manner of its expression",
        "Can describe the feeling to a trusted person",
        "Returns to the emotion later and processes it",
        "Protects others without deceiving them",
    ], "Emotional avoidance", [
        "Pushes the emotion out of awareness",
        "Has no choice about expression: it leaks or erupts",
        "Cannot describe the feeling, even when asked",
        "The emotion resurfaces as tension, irritability, or illness",
        "Protects others by deceiving them and himself",
    ])


@_fig("fig-03-02")
def fig_03_02():
    d.sequence("fig-03-02", [
        "A boy learns which feelings are welcome|Tears are discouraged; fear is mocked; tenderness is not modelled.",
        "Feeling is reclassified|Sadness becomes 'tiredness'; fear becomes 'nothing'; grief becomes 'busyness'.",
        "The body takes over|Sleep changes, shoulders tighten, digestion suffers, blood pressure rises.",
        "The mind takes over|Irritability, numbness, intrusive worry, and a sense that something is wrong that he cannot name.",
        "The relationships take over|Intimacy thins; conversations stay on the surface; those closest to him feel the distance without understanding it.",
    ], note="The sequence is not inevitable, but it is extremely common, and it is reversible at every stage.")


@_fig("fig-03-03")
def fig_03_03():
    d.cards("fig-03-03", [
        "Name the sensation|Before naming a feeling, name what the body is doing: chest, throat, stomach, jaw, shoulders, breath.",
        "Use a graduated scale|Rate the feeling from one to ten; it makes description possible when adjectives are unavailable.",
        "Write one sentence a day|A single honest sentence, kept private, builds the vocabulary that speech requires.",
        "Borrow another man's words|Reading or hearing another man describe the same state supplies language that he does not yet possess.",
    ], cols=2, note="Exercises that build emotional vocabulary, in ascending order of difficulty.")


@_fig("fig-03-04")
def fig_03_04():
    matrix("fig-03-04",
           ["What the man says", "What it frequently encodes", "What could be said instead"],
           [
            ['I am fine.', 'The situation is not safe for the truth, or he has not identified it',
             'I am managing, but something is weighing on me that I have not spoken about.'],
            ['I am just tired.', 'Tension, poor sleep, depression, or grief',
             'I have not been sleeping and I feel low most days. I want that looked at.'],
            ['It is work.', 'An explanation is required, and this one is available',
             'Work is part of it, but it is not the main thing.'],
            ['Do not worry about me.', 'The offer of help is welcomed and cannot yet be accepted',
             'I do need help, but I do not yet know what kind. Let me think and come back to you.'],
            ['It is in the past.', 'The material is present and unaddressed',
             'I have put it away rather than dealt with it.'],
            ['I do not want to burden you.', 'He believes his difficulty is a defect he would be imposing',
             'I would like to tell you something that has been hard for me for a long time.'],
           ],
           first_w=20, size=6.6)


# ---------------------------------------------------------------- Chapter 4
@_fig("fig-04-01")
def fig_04_01():
    d.compare("fig-04-01", "Being surrounded", [
        "Many contacts, colleagues, and dependants",
        "Conversations about work, money, and logistics",
        "Requests made of him daily",
        "Respect and, often, public standing",
        "Company that ends when the meeting ends",
    ], "Being known", [
        "Two or three people who ask how he actually is",
        "Conversations about fear, doubt, and what he wants",
        "Requests made by him, occasionally, and received well",
        "Honesty about his failures without loss of standing",
        "Company that continues when there is nothing to be done",
    ])


@_fig("fig-04-02")
def fig_04_02():
    d.loadbars("fig-04-02", [
        "Dependants relying on his income|1.0",
        "Household decisions that land on him|0.85",
        "Extended-family requests and obligations|0.8",
        "Work expectations outside normal hours|0.7",
        "People who ask how he is|0.15",
        "Hours available for friendship|0.12",
        "Hours available for rest|0.1",
    ])


@_fig("fig-04-03")
def fig_04_03():
    d.cycle("fig-04-03", [
        "Success increases demands on his time",
        "Time for friendship decreases",
        "Conversations become transactional",
        "He learns not to bring problems to anyone",
        "His answers become shorter and more guarded",
        "Friends stop asking",
    ], centre="The success trap")


@_fig("fig-04-04")
def fig_04_04():
    d.stairs("fig-04-04", [
        "One honest sentence|To one trusted person, about one real thing.",
        "A standing arrangement|A weekly walk, call, or meal with a friend, kept as an appointment.",
        "A reciprocal confidant|Someone to whom he speaks, and who speaks to him in return.",
        "A group of men|A discussion group, fellowship, or peer circle with an agreed rule of honesty.",
        "A professional relationship|A counsellor, therapist, or physician who knows his history.",
    ], note="Rebuilding connection proceeds in steps; the first step is small on purpose.")
