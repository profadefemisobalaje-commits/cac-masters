"""Curated Subject Index terms for Battles Men Fight Alone.

Each entry: (display, [regex patterns]).  Patterns are matched case-insensitively
against the text of the compiled PDF, page by page, across the main text and the
appendices.  Keep patterns distinctive enough to avoid false positives; use
several alternatives where a concept is expressed in more than one way.
"""

SUBJECT = [
    # --- Part I: the silent world of men -------------------------------------
    ("achievement, loneliness of", [r"loneliness behind achievement", r"lonely at the top of his own achievement"]),
    ("adult development, stages of", [r"adult development"]),
    ("appearance, management of", [r"manag(?:e|ing) appearances", r"keeping up appearances"]),
    ("concealment of distress", [r"conceal(?:ment|ing|ed)? (?:his|their|the)? ?(?:struggles|distress|pain|difficulties)", r"hidden (?:struggle|pain|battle)"]),
    ("crying, men and", [r"men (?:and|who) cry", r"crying without shame", r"cry alone"]),
    ("emotional (in)expressiveness", [r"emotional (?:inexpressiveness|expressiveness|restriction)"]),
    ("emotional avoidance versus self-control", [r"avoidance (?:and|versus|vs\.?) self-control", r"self-control (?:and|versus) avoidance"]),
    ("emotional suppression", [r"emotional suppression", r"suppress(?:ion|ing|ed) (?:of )?(?:emotion|feelings|grief|pain)"]),
    ("gender norms and masculinity", [r"masculine (?:norm|norms|ideal|script)", r"norms of masculinity", r"masculinity norms"]),
    ("help-seeking, barriers to", [r"help[- ]seeking", r"reluctan(?:ce|t) to (?:ask for|seek) help"]),
    ("isolation, social", [r"social isolation", r"socially isolated"]),
    ("loneliness in men", [r"male loneliness", r"loneliness (?:among|in|of) men"]),
    ("masculinity, traditional", [r"traditional masculinity", r"traditional (?:view|model|conception) of manhood"]),
    ("self-reliance, exaggerated", [r"self-reliance", r"handle (?:it|everything) alone"]),
    ("silence, strategic", [r"strategic silence", r"silence (?:as|became) a (?:survival|strategy)"]),
    ("strength, redefined", [r"redefin(?:e|ing) strength", r"strength beyond endurance"]),
    ("vulnerability", [r"vulnerabilit(?:y|ies)"]),

    # --- Part II: the mind ---------------------------------------------------
    ("anxiety in men", [r"anxiety (?:in men|hidden|beneath)", r"hidden anxiety"]),
    ("cognitive behavioural therapy (CBT)", [r"cognitive behavioural therapy", r"\bCBT\b"]),
    ("depression in men", [r"depression (?:in men|behind|hidden|among men)"]),
    ("emotional numbness", [r"emotional numbness", r"numbness"]),
    ("fear of failure", [r"fear of failure"]),
    ("impostor feelings", [r"impostor (?:feelings|phenomenon|syndrome|experience)"]),
    ("intrusive thoughts", [r"intrusive thoughts"]),
    ("irritability as a symptom", [r"irritability (?:as|instead)", r"depression (?:may|often|can) (?:appear|present) (?:as )?irritab"]),
    ("medication, antidepressant", [r"antidepressant"]),
    ("perfectionism", [r"perfectionis(?:m|t)"]),
    ("psychotherapy", [r"psychotherap(?:y|ist)"]),
    ("self-concept", [r"self-concept"]),
    ("self-criticism, internalised", [r"internal critic", r"negative internal dialogue", r"self-criticis(?:m|e)"]),
    ("self-doubt", [r"self-doubt"]),
    ("shame, psychology of", [r"\bshame\b"]),
    ("suicidal thoughts", [r"suicidal (?:thoughts|ideation|feelings)", r"thoughts of suicide"]),
    ("therapy, talking", [r"talking (?:therapy|treatment)", r"counselling and psychotherapy"]),
    ("worry, persistent", [r"persistent worry"]),

    # --- Part III: money -----------------------------------------------------
    ("debt and emotional strain", [r"debt (?:and|, ) ?(?:anxiety|stress|shame)", r"problem debt"]),
    ("financial hardship, shame of", [r"financial (?:hardship|shame|difficulty)"]),
    ("financial boundaries", [r"financial boundar"]),
    ("financial planning, shared", [r"shared financial planning", r"family budget meeting"]),
    ("financial recovery", [r"financial recovery", r"rebuild(?:ing)? financial"]),
    ("money and self-worth", [r"money and (?:self-worth|identity|worth)"]),
    ("overwork", [r"overwork(?:ed|ing)?"]),
    ("provider burnout", [r"provider burnout"]),
    ("provider role", [r"provider (?:role|expectations|pressure|identity)"]),
    ("success, redefined", [r"definition of success", r"redefin(?:e|ing) success"]),
    ("unemployment, psychological effects of", [r"unemploy(?:ment|ed)"]),
    ("underemployment", [r"underemploy(?:ment|ed)"]),
    ("work-life balance", [r"work[- ]life balance", r"work[- ]life boundaries"]),

    # --- Part IV: love and relationships ------------------------------------
    ("betrayal", [r"\bbetray(?:al|ed|ing)\b"]),
    ("communication in marriage", [r"marital communication", r"communication in marriage", r"couple communication"]),
    ("conflict resolution", [r"conflict resolution"]),
    ("couples therapy", [r"couples therapy", r"couple therapy", r"marriage counselling"]),
    ("heartbreak", [r"heartbreak", r"breakup", r"break-up"]),
    ("intimacy, emotional", [r"emotional intimacy"]),
    ("marital disconnection", [r"emotional (?:disconnection|distance) (?:between|in) (?:spouses|marriage|partners)"]),
    ("rejection, effects of", [r"\brejection\b"]),
    ("resentment, unspoken", [r"unspoken resentment", r"resentment"]),
    ("trust, rebuilding", [r"rebuild(?:ing)? trust"]),

    # --- Part V: family and fatherhood --------------------------------------
    ("absent father", [r"absent father", r"emotionally (?:absent|distant) father"]),
    ("appreciation, need for", [r"unappreciated", r"feeling (?:invisible|unappreciated)"]),
    ("emotional availability in fatherhood", [r"emotional(?:ly)? availab(?:le|ility) (?:as a father|in fatherhood|to (?:his|the) child)"]),
    ("fatherhood, burdens of", [r"fatherhood"]),
    ("parentification", [r"parentification", r"parentified"]),
    ("paternal mental health", [r"paternal (?:mental health|depression)"]),
    ("role reversal in childhood", [r"role reversal (?:in|during) childhood"]),
    ("unmet childhood needs", [r"unmet childhood needs"]),

    # --- Part VI: identity and self-worth -----------------------------------
    ("addiction", [r"\baddiction\b", r"addictive"]),
    ("alcohol use", [r"alcohol (?:use|dependence|misuse)"]),
    ("behavioural change, sustainable", [r"sustainable (?:behavioural|behavioral) change"]),
    ("body image in men", [r"body (?:image|dissatisfaction)"]),
    ("coping mechanisms, harmful", [r"(?:harmful|destructive|maladaptive) coping"]),
    ("emotional regulation", [r"emotional regulation", r"emotion regulation"]),
    ("gambling", [r"gambling"]),
    ("identity crisis", [r"identity (?:crisis|crises)"]),
    ("midlife transition", [r"midlife", r"mid-life"]),
    ("procrastination", [r"procrastination"]),
    ("recovery from addiction", [r"relapse prevention", r"recovery (?:from|programme|pathway)"]),
    ("substance use", [r"substance (?:use|misuse|dependence)"]),
    ("twelve-step programmes", [r"twelve[- ]step", r"12[- ]step"]),

    # --- Part VII: society ---------------------------------------------------
    ("comparison, social", [r"social comparison"]),
    ("dignity, defence of", [r"\bdignity\b"]),
    ("friendship, male", [r"male (?:friendship|friendships)", r"friendship networks? of men"]),
    ("humiliation, public", [r"public humiliation", r"humiliat(?:ion|ed|ing)"]),
    ("mentorship", [r"mentor(?:ship|ing)?\b"]),
    ("peer support", [r"peer support"]),
    ("respect, social", [r"social (?:respect|status)"]),
    ("social support networks", [r"support network", r"support networks"]),
    ("status anxiety", [r"status (?:anxiety|competition)"]),

    # --- Part VIII: loss, regret, broken dreams -----------------------------
    ("ambiguous loss", [r"ambiguous loss"]),
    ("bereavement", [r"bereave(?:ment|d|s)?"]),
    ("disenfranchised grief", [r"disenfranchised grief"]),
    ("grief in men", [r"(?:male|men'?s?) grief", r"grieving (?:in silence|without an audience|alone)"]),
    ("grief, delayed", [r"delayed grief", r"complicated grief"]),
    ("regret", [r"regret(?:s|ted|ting)?"]),
    ("self-forgiveness", [r"self-forgiveness"]),
    ("unrealised ambition", [r"unrealis(?:ed|able) (?:ambition|potential)", r"abandoned (?:ambition|dream)"]),

    # --- Part IX: leadership -------------------------------------------------
    ("compassion fatigue", [r"compassion fatigue"]),
    ("decision fatigue", [r"decision fatigue"]),
    ("delegation", [r"delegation", r"delegating"]),
    ("emotional labour", [r"emotional labou?r"]),
    ("executive loneliness", [r"(?:executive|leadership) (?:loneliness|isolation)"]),
    ("humility, intellectual", [r"intellectual humility"]),
    ("leadership pressure", [r"loneliness of leadership", r"leadership pressure"]),
    ("over-responsibility", [r"over[- ]responsib(?:ility|le)"]),

    # --- Part X: healing ----------------------------------------------------
    ("burnout", [r"\bburnout\b"]),
    ("crisis plan, personal", [r"crisis (?:plan|support plan)"]),
    ("help, asking for", [r"asking for help", r"seeking help"]),
    ("professional help, when to seek", [r"professional (?:help|support)"]),
    ("psychiatrist", [r"psychiatrist"]),
    ("rest and guilt", [r"rest (?:and|without) guilt", r"guilt about rest"]),
    ("self-care plan", [r"self-care plan"]),
    ("self-compassion", [r"self-compassion"]),
    ("sleep and health", [r"sleep (?:hygiene|quality|deprivation)"]),
    ("stress, chronic", [r"chronic stress"]),
    ("stigma of mental health care", [r"stigma"]),
    ("trauma, psychological", [r"trauma(?:tic)?"]),

    # --- Part XI: rebuilding -------------------------------------------------
    ("accountability", [r"accountab(?:le|ility)"]),
    ("assertiveness", [r"assertive(?:ness)?"]),
    ("boundaries, personal", [r"personal boundaries", r"healthy boundaries"]),
    ("emotional intelligence", [r"emotional intelligence"]),
    ("personal agency", [r"\bagency\b"]),
    ("resilience", [r"resilience"]),
    ("setbacks, recovering from", [r"setback"]),
    ("values-based living", [r"values-based", r"values, not feelings"]),

    # --- Part XII: beyond the battle ----------------------------------------
    ("authenticity", [r"authenticity", r"authentic life"]),
    ("boys and emotional learning", [r"boys (?:learn|are taught)", r"teaching boys"]),
    ("emotional maturity", [r"emotional maturity"]),
    ("fathers modelling emotion", [r"fathers? (?:as|who) model", r"modelling emotional"]),
    ("gender stereotypes, challenging", [r"gender stereotype"]),
    ("intergenerational transmission", [r"intergenerational", r"generation to the next"]),
    ("legacy and mentoring", [r"\blegacy\b"]),
    ("schools and emotional education", [r"schools? (?:can|and) (?:teach|emotional)"]),
    ("wisdom through adversity", [r"adversity"]),

    # --- Appendices and tools ------------------------------------------------
    ("30-day plan", [r"30-day"]),
    ("90-day plan", [r"90-day"]),
    ("anger management", [r"anger (?:management|regulation)"]),
    ("journaling", [r"journal(?:ing)?\b"]),
    ("relaxation and breathing exercises", [r"breathing (?:exercise|practice)", r"grounding exercise"]),
    ("self-assessment tools", [r"self-assessment"]),
    ("values clarification", [r"values clarification", r"personal values"]),
]
