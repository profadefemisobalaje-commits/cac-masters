"""MFT 701 — Weeks 1–4."""
from ..model import lecture, week

WEEKS = [

# ==========================================================================
week(
    n=1,
    title="What Is Marriage and Family Therapy?",
    short="The Field",
    standfirst="A discipline is defined less by whom it treats than by how it thinks.",
    epigraph="A family is not the backdrop against which a life is lived; it is the medium in which a person becomes intelligible.",
    epigraph_src="Course epigraph",
    keywords=["Relation", "Context", "Practice"],
    outcomes=[
        "Distinguish couple and family therapy from individually oriented practice by unit of treatment, explanatory logic and clinical method.",
        "Reconstruct the professionalisation of the field and account for its contemporary identity within mental health systems.",
        "Apply a biopsychosocial-spiritual frame to a presenting problem without collapsing one level into another.",
        "Explain why relational ethics and cultural accountability are constitutive of systemic practice, not additions to it.",
        "Formulate a first, defensible rationale for working relationally.",
    ],
    concepts=[
        ("The relational unit",
         "The couple, family or caregiving system — not only the identified patient — is the unit of assessment and the object of intervention.",
         "In the room: you ask who else is affected before you ask what is wrong."),
        ("Systemic epistemology",
         "An account of problems located in recursive patterns of interaction and context rather than inside a single mind.",
         "In the room: the question shifts from why to what happens next."),
        ("Biopsychosocial-spiritual frame",
         "A multi-level formulation integrating biology, meaning, relationship, community and faith.",
         "In the room: no single level is allowed to become the whole story."),
        ("Professional identity",
         "An internalised accountability to a discipline's knowledge, ethics and public mandate.",
         "In the room: you can name the tradition you are working from."),
    ],
    lectures=[
        lecture(
            "Lecture I · Foundations",
            "Three ways of defining a field",
            [
                ("Who is in the room",
                 "MFT treats couples, families and larger caregiving systems. Individuals may be seen, but always through a relational lens."),
                ("Where the problem lives",
                 "Distress is formulated as maintained by recursive interaction and context, not by a single defective mind."),
                ("What the therapist does",
                 "The clinician engages the system directly: joining, enacting, reframing and designing relational experiments."),
                ("Why the distinction matters",
                 "The same presentation can yield an individual or a systemic formulation — and the formulation governs the intervention."),
            ],
            "A useful test: if the family were in the room, what would we notice that we cannot see with one person alone?",
        ),
        lecture(
            "Lecture II · History",
            "From movement to profession",
            [
                ("Three tributaries",
                 "Child guidance, marriage counselling and post-war psychiatry converged in the 1950s into a self-conscious field."),
                ("The cybernetic vocabulary",
                 "Bateson's research group and the Palo Alto clinicians supplied the language of feedback, sequence and system."),
                ("Institutionalisation",
                 "Training standards, codes of ethics and licensure converted a movement into an accountable profession."),
                ("Contemporary plurality",
                 "The field is now systemic, evidence-informed, culturally accountable and theoretically plural."),
            ],
            "Professional identity is not loyalty to one model. It is accountability to a tradition and to the people it serves.",
        ),
        lecture(
            "Lecture III · Framework",
            "The biopsychosocial-spiritual frame",
            [
                ("Biological",
                 "Temperament, neurodevelopment, sleep, illness, medication and substance use shape what a family can do."),
                ("Psychological",
                 "Attachment, emotion regulation, trauma and meaning-making organise how distress is experienced and expressed."),
                ("Social",
                 "Kinship, economy, gender, migration, housing and discrimination distribute risk and resource across a family."),
                ("Spiritual",
                 "Faith, ritual, belonging and moral conviction can be either a primary resource or a site of conflict."),
            ],
            "Assessment fails whenever one level is allowed to become the whole story.",
        ),
    ],
    figure=dict(
        kicker="Figure 01 · The field",
        title="The ecology of practice",
        caption="The family is nested in kin, community and culture. Each level can be a site of risk, a source of resource, or both at once.",
        source="Prepared for this course.",
        notes="Point to the centre, then move outward. Ask: at which ring is this family most stuck, and at which ring is it most resourced?",
    ),
    vignette=dict(
        title="The Adeyemi family",
        body=("Mrs Adeyemi books an appointment for her fourteen-year-old daughter, Tolu, whose school refusal "
              "has lasted a term. Tolu is quiet and polite in the room. Her father, a long-distance driver, attends "
              "every third session and believes the problem is spiritual. Her paternal grandmother, who lives with "
              "the family, disagrees. The parents argue about discipline in front of Tolu, who has learned to end "
              "the argument by becoming unwell. The family's pastor has offered to pray with them and has referred "
              "them to you."),
        prompts=[
            "What does an individual formulation miss that a systemic formulation can see?",
            "Where would you place the problem — and who in this family would disagree with you?",
            "Which level of the biopsychosocial-spiritual frame is least visible in this referral, and what would you ask to find it?",
        ],
        notes="Read slowly. Ask for observations before interpretations; the family's own theory of the problem is clinical data.",
    ),
    skills=dict(
        title="Formulating at three levels",
        intro=("In pairs, take a case you are currently carrying, or the vignette above. Write three formulations of the same "
               "problem, then compare what each one makes actionable."),
        steps=[
            ("Individual", "Formulate the problem as an intrapsychic process. Note what the account explains and what it silences."),
            ("Relational", "Re-describe the same problem as a circular pattern between people. Identify the sequence and its function."),
            ("Contextual", "Place the pattern in its social, economic, cultural and spiritual conditions. Who carries the cost?"),
            ("Comparative", "Decide which formulation you would act on first, and state the evidence that would change your mind."),
        ],
        timing=["12 min", "12 min", "12 min", "12 min"],
        debrief=("Notice where the individual account feels more 'real' to you. That preference is part of your clinical signature — "
                 "and worth examining."),
    ),
    seminar=[
        "If a family refuses to attend, is the work still family therapy?",
        "What is gained, and what is lost, when the identified patient is treated as the problem?",
        "Is 'systemic' a theory, a method or a professional identity? Can it be all three without confusion?",
        "How should a therapist hold religious explanations of distress without either dismissing or endorsing them?",
        "Which of the four levels in the biopsychosocial-spiritual frame is most often over-weighted in your own setting, and why?",
    ],
    assignment=dict(
        major_title="Position statement: why relational practice?",
        major_text=("Write a first, argued statement of your rationale for working relationally. Draw on at least three sources "
                    "from the reading list and one piece of clinical or personal observation. The statement should be defensible, "
                    "not confessional: make claims and support them."),
        major_meta="800 words · 20% of final grade · due Friday, 17:00",
        tasks=[
            "Annotate the core reading: mark one claim you accept, one you doubt and one you do not understand.",
            "Draw a three-generation genogram of your own family, then write 250 words on what the exercise revealed about your assumptions.",
            "Bring one referral to the skills laboratory; you will formulate it at three levels.",
        ],
        criteria=[
            "A clear claim, stated in the first paragraph and sustained.",
            "Use of three sources that are actually read, not merely cited.",
            "One concrete observation, clinical or personal, used as evidence.",
            "A stated limit: the strongest objection to your own position.",
        ],
        note=("The genogram is a learning instrument, not a clinical disclosure. Share only what you choose; no one will be required "
              "to expose personal material."),
    ),
    readings=[
        ("Core", "Nichols, M. P., & Davis, S. D. (2016). The essentials of family therapy (6th ed.). Pearson."),
        ("Survey", "Goldenberg, I., Stanton, M., & Goldenberg, H. (2017). Family therapy: An overview (9th ed.). Cengage."),
        ("Practice", "Wetchler, J. L., & Hecker, L. L. (2015). An introduction to marriage and family therapy (2nd ed.). Routledge."),
        ("Ethics", "Doherty, W. J. (1995). Soul searching: Why psychotherapy must promote moral responsibility. Basic Books."),
        ("Code", "American Association for Marriage and Family Therapy. (2015). Code of ethics. AAMFT."),
        ("Context", "Nwoye, A. (2015). What is African psychology the psychology of? Theory & Psychology, 25(1), 96–116."),
    ],
    synthesis=("The person is not the unit of suffering; the relation is the unit of repair.",
               "Course synthesis"),
    next=dict(
        n=2,
        title="The Systems Revolution",
        read="Bateson, Steps to an Ecology of Mind — the introduction.",
        annotate="One passage where Bateson refuses a simple cause.",
        bring="A problem you have described linearly.",
        preview=[
            "Why the analytic habit of thought made family therapy almost unthinkable.",
            "Bertalanffy, general systems theory and the importation of organismic thinking.",
            "What changes when the observer is included in the system being observed.",
        ],
    ),
),

# ==========================================================================
week(
    n=2,
    title="The Systems Revolution",
    short="Systems",
    standfirst="The most consequential idea in the field is not a technique but a change in what counts as a unit.",
    epigraph="The unit of survival is organism plus environment.",
    epigraph_src="Gregory Bateson, Steps to an Ecology of Mind (1972)",
    keywords=["Whole", "Relation", "Emergence"],
    outcomes=[
        "Explain the shift from analytic to systemic explanation, and why it was revolutionary rather than merely fashionable.",
        "Describe the core claims of general systems theory: wholeness, interdependence, organisation and emergence.",
        "Distinguish open from closed systems and identify feedback in ordinary clinical description.",
        "Critique the systems metaphor: what it illuminates and what it allows clinicians to overlook.",
        "Apply a systemic lens to a problem that is usually individualised.",
    ],
    concepts=[
        ("System",
         "A set of elements in interaction whose organisation produces properties that none of the elements possesses alone.",
         "In the room: you describe the household, not just the child."),
        ("Emergence",
         "Patterns that arise from interaction and cannot be predicted from the parts considered in isolation.",
         "In the room: the argument appears only when the three of them are together."),
        ("Open system",
         "A system that exchanges information, energy or members with its environment, and is therefore capable of transformation.",
         "In the room: a new job, a birth or a migration changes the family's rules."),
        ("Equifinality",
         "The same end state may be reached from different beginnings, and different ends from the same beginning.",
         "In the room: two very different families arrive at the same symptom."),
    ],
    lectures=[
        lecture(
            "Lecture I · Epistemology",
            "The analytic habit and its limits",
            [
                ("Decomposition",
                 "Clinical science tends to explain wholes by breaking them into parts and attributing causality to the parts."),
                ("The identified patient",
                 "Individual diagnosis locates pathology inside a person and treats surrounding relationships as background."),
                ("What remains unexplained",
                 "Patterns that persist across persons, and symptoms that appear to serve a function in a household, resist the analytic account."),
                ("The systemic wager",
                 "Re-describe the same facts at the level of relationship, organisation and context — then see what becomes actionable."),
            ],
            "The question is not whether the individual is real, but whether the individual is a sufficient unit of explanation.",
        ),
        lecture(
            "Lecture II · Theory",
            "General systems theory, imported",
            [
                ("Bertalanffy's claim",
                 "Organisms are organised wholes whose properties cannot be reduced to isolated parts; organisation itself is explanatory."),
                ("Interdependence",
                 "A change in one element propagates through the system and returns to alter the element that changed."),
                ("Open systems",
                 "Families exchange information, resources and members with their environment; they are not sealed machines."),
                ("Equifinality and multifinality",
                 "Similar beginnings can produce different outcomes, and different beginnings similar outcomes — so prediction is probabilistic."),
            ],
            "Systems theory gave clinicians a vocabulary for what they had already seen: that a family is not the sum of its members.",
        ),
        lecture(
            "Lecture III · Critique",
            "What the metaphor hides",
            [
                ("Stability over change",
                 "Early systems writing over-weighted homeostasis and under-described conflict, power and transformation."),
                ("The missing observer",
                 "First-order cybernetics described systems from outside; the therapist's own position went unexamined."),
                ("The missing body",
                 "Systems language can become so abstract that biology, trauma and material deprivation disappear from view."),
                ("Critical use",
                 "Use systems thinking as an instrument of description, not as a total philosophy of persons."),
            ],
            "Every metaphor illuminates a field and casts a shadow. Learn to see the shadow.",
        ),
    ],
    figure=dict(
        kicker="Figure 02 · Diagram",
        title="From parts to pattern",
        caption="The same clinical facts, described twice: as a chain of individual causes, and as a pattern that sustains itself across persons.",
        source="Prepared for this course.",
        notes="Ask students which description is 'truer'. Then ask which is more useful — and for whom.",
    ),
    vignette=dict(
        title="The silent dinner table",
        body=("A father drinks most evenings. The mother monitors his mood and quietly manages the household around it. "
              "Their eldest son has become the family's negotiator; the youngest has stopped speaking at dinner. "
              "The referral names the father's drinking. In the first session the family describes a home in which "
              "everyone is careful, no one is direct and the children have learned to read the sound of a car in the drive."),
        prompts=[
            "Write the individual formulation: what is the problem, and where does it live?",
            "Now write the systemic formulation: what pattern holds the drinking, the vigilance and the silence together?",
            "What would each formulation make you do first — and what might each one miss?",
        ],
        notes="Hold both formulations without resolving them. The point is to feel the difference in clinical leverage.",
    ),
    skills=dict(
        title="The re-description exercise",
        intro=("Work in threes with a single symptom statement. Re-describe it at four levels, then test each description for what it "
               "makes possible in the room."),
        steps=[
            ("Intrapsychic", "State the symptom as an internal process. Identify the mechanism and the individual target of change."),
            ("Dyadic", "Re-state it as a sequence between two people. Name who does what, when, and what follows."),
            ("Triadic", "Introduce a third person: what does the triangle protect, and who is recruited into it?"),
            ("Contextual", "Situate the sequence in its material, cultural and institutional conditions."),
        ],
        debrief=("Which level did your group reach last? Most clinicians stop at the dyad. The context is usually where the leverage is."),
    ),
    seminar=[
        "Is systems theory a description of reality or a useful fiction?",
        "What kinds of suffering become invisible when everything is described as a system?",
        "Does 'the family is a system' commit us to treating the family as a patient?",
        "How would a systems thinker explain a symptom that benefits no one in the family?",
        "What is the difference between interdependence and mutual responsibility?",
    ],
    assignment=dict(
        major_title="A systems re-description",
        major_text=("Take a published case or a case from your placement. Write the individual formulation first, then a systemic "
                    "re-description of the same facts. Conclude with a judgement about which account is more defensible and why. "
                    "The essay is assessed on the quality of the re-description, not on loyalty to systems theory."),
        major_meta="900 words · 25% of final grade · due in two weeks",
        tasks=[
            "Map one feedback loop from the case, with every arrow labelled.",
            "Identify one fact the systemic account cannot explain.",
            "Bring a one-paragraph case summary for peer review.",
        ],
        criteria=[
            "Fidelity: the systemic account is built from the same facts, not new ones.",
            "Mechanism: every arrow in the loop is labelled with an observable behaviour.",
            "Judgement: a defended conclusion about which account is more useful here.",
            "Restraint: an honest statement of what the systemic account cannot explain.",
        ],
        note="A good re-description is not a rejection of the individual. It is an argument about the level at which change is possible.",
    ),
    readings=[
        ("Core", "Bateson, G. (1972). Steps to an ecology of mind. Chandler."),
        ("Theory", "von Bertalanffy, L. (1968). General system theory: Foundations, development, applications. Braziller."),
        ("Classic", "Watzlawick, P., Beavin, J. H., & Jackson, D. D. (1967). Pragmatics of human communication. Norton."),
        ("History", "Hoffman, L. (1981). Foundations of family therapy. Basic Books."),
        ("Survey", "Nichols, M. P., & Davis, S. D. (2016). The essentials of family therapy (6th ed.). Pearson."),
        ("Science", "Capra, F., & Luisi, P. L. (2014). The systems view of life. Cambridge University Press."),
    ],
    synthesis=("The system is not a thing to be treated; it is a way of seeing what treatment is for.",
               "Course synthesis"),
    next=dict(
        n=3,
        title="Cybernetics and the Observing System",
        read="Watzlawick, Beavin & Jackson, Pragmatics — the opening chapter.",
        annotate="One axiom you find either obvious or troubling.",
        bring="A sequence you have observed and can describe without blame.",
        preview=[
            "Feedback, control and the machinery of stability.",
            "Von Foerster and the move from first-order to second-order cybernetics.",
            "Why the therapist is never outside the system being described.",
        ],
    ),
),

# ==========================================================================
week(
    n=3,
    title="Cybernetics and the Observing System",
    short="Cybernetics",
    standfirst="The observer is not a window on the system. The observer is part of what the system becomes.",
    epigraph="One cannot not communicate.",
    epigraph_src="Watzlawick, Beavin & Jackson, Pragmatics of Human Communication (1967)",
    keywords=["Feedback", "Observer", "Reflexivity"],
    outcomes=[
        "Distinguish negative from positive feedback and identify both in clinical sequences.",
        "Explain the difference between first-order and second-order cybernetics.",
        "Describe how the therapist's own observations and interventions alter the system being observed.",
        "Critique the claim to therapeutic neutrality from a cybernetic and ethical standpoint.",
        "Practise reflexive questioning that includes the therapist's contribution.",
    ],
    concepts=[
        ("Feedback",
         "Information about a system's output that returns to modify its input, regulating either stability or escalation.",
         "In the room: her silence produces his pursuit, which produces her silence."),
        ("Homeostasis",
         "The tendency of a system to maintain its organisation within a range, often by correcting deviation.",
         "In the room: every attempt at change is met by a quiet return to the familiar."),
        ("Second-order cybernetics",
         "The cybernetics of observing systems: the observer is included in the description of what is observed.",
         "In the room: your hypothesis has already changed what the family says."),
        ("Reflexivity",
         "The disciplined use of one's own reactions and position as data about the relational system.",
         "In the room: your irritation is information, not a personal failing."),
    ],
    lectures=[
        lecture(
            "Lecture I · Mechanism",
            "Feedback: the basic mechanism",
            [
                ("Negative feedback",
                 "Deviation is detected and corrected: the thermostat, the curfew, the parent who checks a sleeping child."),
                ("Positive feedback",
                 "Deviation is amplified: the more he withdraws, the more she pursues; the more she pursues, the more he withdraws."),
                ("Circularity of effect",
                 "An output becomes an input elsewhere in the system; effects are never only downstream."),
                ("Clinical reading",
                 "Symptoms can be understood as feedback signals that regulate distance, conflict or care in a relational system."),
            ],
            "The question is not 'what caused this?' but 'what is this maintaining, and at what cost?'",
        ),
        lecture(
            "Lecture II · History",
            "From first order to second order",
            [
                ("Wiener and the Macy conferences",
                 "Cybernetics named the study of control and communication in animal and machine; clinicians borrowed its grammar."),
                ("First-order practice",
                 "The therapist observes and corrects a system from outside, as though standing on neutral ground."),
                ("Von Foerster's turn",
                 "If observation is itself an operation of the system, then the observer cannot be excluded from the account."),
                ("Consequences for therapy",
                 "Assessment becomes intervention; the therapist's hypotheses, language and presence change what the family can say."),
            ],
            "You cannot describe a family without changing the conditions under which it is described.",
        ),
        lecture(
            "Lecture III · Practice",
            "Reflexivity in the consulting room",
            [
                ("The therapist in the loop",
                 "Every question selects a domain of observation and makes some answers more available than others."),
                ("Neutrality reconsidered",
                 "Neutrality is not indifference or the absence of a position; it is curiosity disciplined by accountability."),
                ("Use of self",
                 "Boredom, anxiety, irritation and rescue fantasies are data about the relational field, not private failures."),
                ("Ethical reflexivity",
                 "Power, culture and institutional context shape what counts as a problem and who is entitled to define it."),
            ],
            "Objectivity is not the absence of a position; it is the disciplined awareness of one.",
        ),
    ],
    figure=dict(
        kicker="Figure 03 · Diagram",
        title="First-order and second-order observation",
        caption="In first-order cybernetics the observer stands outside the loop. In second-order cybernetics the observer's distinctions enter the system and alter it.",
        source="Prepared for this course.",
        notes="Draw the two loops side by side on the board. Ask: where is the therapist in each picture?",
    ),
    vignette=dict(
        title="The therapist who became the third side",
        body=("A mother complains that her husband is emotionally absent. The therapist, moved by her account, begins to "
              "ask the husband why he withdraws. By the third session the husband is monosyllabic and the mother is "
              "grateful for the therapist's understanding. The therapist notices that the sessions have begun to "
              "reproduce the family's own triangle: two close, one excluded."),
        prompts=[
            "What feedback did the therapist's curiosity produce in the system?",
            "How would a second-order account describe the therapist's contribution?",
            "What might the therapist do differently in the next session, and what would that risk?",
        ],
        notes="This is the pivot of the session. Let students recognise themselves in the therapist before critiquing her.",
    ),
    skills=dict(
        title="Observing the observer",
        intro=("In triads, role-play a short session. The third person tracks the therapist's observable choices — seating, first "
               "question, who is interrupted, whose account is amplified."),
        steps=[
            ("Set", "Therapist, family member and observer agree on a 12-minute role-play with a simple presenting complaint."),
            ("Track", "The observer records every therapist move that selects one person's account over another's."),
            ("Feed back", "The observer reports only what was observable, without interpretation, in two minutes."),
            ("Reflect", "The therapist names one contribution they can now see, and one they would repeat."),
        ],
        timing=["6 min", "12 min", "12 min", "6 min"],
        debrief=("Reflexivity is not self-blame. It is the recovery of choice where habit had made choice invisible."),
    ),
    seminar=[
        "Can a therapist ever be outside the system?",
        "Is neutrality possible, or only a useful fiction?",
        "What is the difference between reflexivity and self-absorption?",
        "How should a therapist's religious or moral convictions enter a session?",
        "When does the observer's influence become an ethical problem rather than an epistemological fact?",
    ],
    assignment=dict(
        major_title="Reflexive journal: the observer in the room",
        major_text=("Keep a structured journal across three clinical or role-play encounters. For each, record what you noticed, "
                    "what you did, what the system did next and what you now think your presence made possible. Conclude with "
                    "one pattern in your own practice."),
        major_meta="700 words · 15% of final grade · submitted weekly",
        tasks=[
            "One page per encounter: observation, intervention, response, reflection.",
            "Mark one moment where your own emotion shaped a clinical choice.",
            "Bring one excerpt (anonymised) to the seminar.",
        ],
        criteria=[
            "Specificity: an observable moment, not a general impression.",
            "Candour: one contribution of your own you would rather not have made.",
            "Analysis: what your presence made possible in the system.",
            "Pattern: one recurring tendency named across the three entries.",
        ],
        note="The journal is assessed for disciplined observation, not for confession or self-criticism.",
    ),
    readings=[
        ("Core", "Watzlawick, P., Beavin, J. H., & Jackson, D. D. (1967). Pragmatics of human communication. Norton."),
        ("Founding", "Wiener, N. (1948). Cybernetics: Or control and communication in the animal and the machine. MIT Press."),
        ("Second order", "von Foerster, H. (2003). Understanding understanding. Springer."),
        ("Method", "Cecchin, G. (1987). Hypothesizing, circularity, and neutrality revisited. Family Process, 26(4), 405–413."),
        ("History", "Hoffman, L. (1981). Foundations of family therapy. Basic Books."),
        ("Context", "Bateson, G. (1972). Steps to an ecology of mind. Chandler."),
    ],
    synthesis=("Objectivity is not the absence of a position; it is the disciplined awareness of one.",
               "Course synthesis"),
    next=dict(
        n=4,
        title="Circularity, Recursion and Relational Logic",
        read="Selvini Palazzoli et al., 'Hypothesizing—Circularity—Neutrality'.",
        annotate="The sentence that changes how you will ask your next question.",
        bring="A case in which two people punctuate the same sequence differently.",
        preview=[
            "Why 'who started it?' is usually the wrong question.",
            "Punctuation, sequence and the politics of the first cause.",
            "Circular questioning as a clinical method.",
        ],
    ),
),

# ==========================================================================
week(
    n=4,
    title="Circularity, Recursion and Relational Logic",
    short="Circularity",
    standfirst="Linear causality asks who is to blame. Circular causality asks what keeps the pattern going.",
    epigraph="The difference between a cause and a pattern is the difference between a verdict and a way forward.",
    epigraph_src="Course epigraph",
    keywords=["Sequence", "Punctuation", "Meaning"],
    outcomes=[
        "Distinguish linear from circular causality and explain the clinical consequences of each.",
        "Analyse how punctuation — where one draws the beginning of a sequence — distributes blame and power.",
        "Map a recursive sequence across at least three people.",
        "Construct circular and difference questions that open new descriptions.",
        "Use circularity without dissolving responsibility or erasing harm.",
    ],
    concepts=[
        ("Circular causality",
         "An account in which effects return to modify their causes, so that a pattern sustains itself over time.",
         "In the room: the pattern, not the person, becomes the object of inquiry."),
        ("Punctuation",
         "The arbitrary but consequential selection of a starting point in a continuous sequence of interaction.",
         "In the room: each partner begins the story at the moment that casts the other as author."),
        ("Recursive sequence",
         "A repeating cycle of behaviour, interpretation and response that reproduces itself across time and persons.",
         "In the room: you draw the loop on paper and the couple recognises it."),
        ("Circular questioning",
         "A method of asking about differences, comparisons and observations from multiple perspectives within a system.",
         "In the room: 'What would your mother say your father thinks is happening?'"),
    ],
    lectures=[
        lecture(
            "Lecture I · Logic",
            "Two causalities, two ethics",
            [
                ("Linear causality",
                 "A cause precedes an effect. It is indispensable for medicine, law and accountability — and dangerous when it becomes the only description."),
                ("Circular causality",
                 "Effects feed back into causes. The pattern, not the person, becomes the object of explanation."),
                ("The cost of circularity",
                 "If everyone is partly responsible, no one may be accountable; circular accounts can obscure violence and asymmetry."),
                ("Clinical judgement",
                 "Use circularity to open possibility, and linearity to name harm and assign responsibility where it belongs."),
            ],
            "Circularity is an instrument for understanding, not a moral position. Never use it to neutralise accountability.",
        ),
        lecture(
            "Lecture II · Politics",
            "Punctuation and the ownership of the beginning",
            [
                ("Who started it",
                 "Each partner punctuates the sequence at the point that casts the other as initiator."),
                ("Punctuation as power",
                 "The person whose account of the beginning is accepted gains the moral advantage of the victim."),
                ("The therapist's punctuation",
                 "The first question, the case note and the treatment plan each select a beginning and distribute responsibility."),
                ("Reframing the sequence",
                 "Move the punctuation from a person to a pattern: 'What happens next?' rather than 'Why did you do that?'"),
            ],
            "Every punctuation is a small theory of responsibility. Ask who benefits from the beginning you have chosen.",
        ),
        lecture(
            "Lecture III · Method",
            "Circular questioning",
            [
                ("Difference questions",
                 "Ask one person how another would answer: 'If your mother were here, what would she say you do next?'"),
                ("Comparative questions",
                 "Ask about better and worse times: 'When was this pattern least strong, and what was different?'"),
                ("Hypothetical questions",
                 "Ask about imagined futures: 'If this changed tomorrow, who would notice first?'"),
                ("Observer questions",
                 "Ask about the system's observation of itself: 'What do you think your father thinks is happening here?'"),
            ],
            "A good circular question makes the family's own observing system visible to itself.",
        ),
    ],
    figure=dict(
        kicker="Figure 04 · Diagram",
        title="The recursive sequence",
        caption="A four-step sequence in which each person's solution becomes the next person's problem, and the pattern returns to its starting point.",
        source="Prepared for this course.",
        notes="Trace the loop with a finger, then ask where each person would punctuate it. The disagreement is the clinical material.",
    ),
    vignette=dict(
        title="Who started it?",
        body=("A couple presents after a decade of escalating arguments. He says she criticises him the moment he walks "
              "in. She says he walks past her without greeting and disappears into his phone. Both accounts are accurate. "
              "Both are incomplete. In the session, each interrupts the other to correct the record, and the therapist "
              "can feel the pull to adjudicate."),
        prompts=[
            "Where does each partner punctuate the sequence, and what does that punctuation protect?",
            "What would change if the therapist refused to decide who started it?",
            "How would you name the pattern without implying that the harm each partner feels is unreal?",
        ],
        notes="Do not resolve the argument. Ask the couple to describe the sequence as a third thing that happens to them both.",
    ),
    skills=dict(
        title="The circular questioning triad",
        intro=("In threes, with one interviewer, one family member and one observer, practise asking questions that invite the "
               "system to observe itself. The observer tracks only the questions, not the answers."),
        steps=[
            ("Warm-up", "Ask three difference questions about a minor household routine. Notice how the answers become comparative."),
            ("Deepen", "Ask one hypothetical future question and one observer question about a recurring conflict."),
            ("Reflect", "The 'family member' reports which question opened something and which closed it down."),
            ("Rewrite", "The interviewer rewrites one closed question into a circular one and tests it."),
        ],
        timing=["8 min", "16 min", "8 min", "8 min"],
        debrief=("Students often discover that their most helpful question was the one they were most afraid to ask. Ask why."),
    ),
    seminar=[
        "Can circular causality and moral responsibility coexist?",
        "When does systemic explanation become a way of excusing harm?",
        "What does it mean to say that a symptom 'serves a function' — and who decides?",
        "Are circular questions neutral, or do they carry a theory of the problem?",
        "How would you apply circular thinking to a context of structural injustice, where power is not symmetrical?",
    ],
    assignment=dict(
        major_title="Ten circular questions and a rationale",
        major_text=("Write ten circular questions for a case of your choice, grouped by type — difference, comparative, hypothetical "
                    "and observer questions. For each, state what new description you hope it will make available and what risk "
                    "it carries. Submit the case summary separately and anonymously."),
        major_meta="1,000 words · 25% of final grade · due Friday",
        tasks=[
            "Identify three punctuations in the case, one per participant.",
            "Record one sequence as a loop diagram with at least four nodes.",
            "Bring one question to test in the skills laboratory.",
        ],
        criteria=[
            "Range: all four question types are represented and correctly named.",
            "Purpose: each question states the description it hopes to open.",
            "Risk: each question names what it could damage or foreclose.",
            "Craft: no question could be answered with a bare yes or no.",
        ],
        note="A question that could be answered 'yes' or 'no' is not yet a circular question. Rewrite it until it invites comparison.",
    ),
    readings=[
        ("Core", "Selvini Palazzoli, M., Boscolo, L., Cecchin, G., & Prata, G. (1980). Hypothesizing—circularity—neutrality: Three guidelines for the conductor of the session. Family Process, 19(1), 3–12."),
        ("Method", "Tomm, K. (1988). Interventive interviewing: Part III. Intending to ask lineal, circular, strategic, or reflexive questions? Family Process, 27(1), 1–15."),
        ("Classic", "Watzlawick, P., Beavin, J. H., & Jackson, D. D. (1967). Pragmatics of human communication. Norton."),
        ("Survey", "Nichols, M. P., & Davis, S. D. (2016). The essentials of family therapy (6th ed.). Pearson."),
        ("History", "Hoffman, L. (1981). Foundations of family therapy. Basic Books."),
        ("Critique", "Hare-Mustin, R. T. (1994). Discourses in the mirrored room: A postmodern analysis of therapy. Family Process, 33(1), 19–35."),
    ],
    synthesis=("To ask 'what happens next?' is already to practise systemically.",
               "Course synthesis"),
    next=dict(
        n=5,
        title="Homeostasis, Change and the Family Life Cycle",
        read="Carter & McGoldrick, The Expanded Family Life Cycle — chapters 1–2.",
        annotate="One stage transition in your own family of origin.",
        bring="A family whose crisis coincided with a life-cycle transition.",
        preview=[
            "Why families resist the very changes they ask for.",
            "Morphostasis, morphogenesis and the uses of crisis.",
            "Carter and McGoldrick's life-cycle framework, and its cultural limits.",
        ],
    ),
),
]
