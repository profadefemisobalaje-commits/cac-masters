# Lecture-Style Slideshow Video with Voiceover — Master Prompt

> **Purpose:** Reusable prompt for generating a lecture-style slideshow video (MP4, 480p) with voiceover,
> plus optional PPTX/PDF slides and a DOCX script.
>
> **How to use:** Copy the block below, fill every `[ ... ]` placeholder, then paste it into the
> agent chat. Anything left as `[ ... ]` is treated as "decide it for me and state your choices".

---

## The Prompt

Create a lecture-style slideshow video with voiceover.

**COURSE / SUBJECT:**
[Use Course Subject]

**LESSON TITLE:**
[Use Each Weekly Topic]

**LEARNERS:**
[Master's degree Level]

**LEARNING OBJECTIVES (2–4):**
By the end, learners should be able to:
1. [e.g. "Define photosynthesis"]
2. [e.g. "Write the word equation"]
3. [e.g. "Explain why light and chlorophyll are needed"]

**DURATION:**
[30 minutes]

**LECTURE OUTLINE (or write "you structure it"):**
- Slide 1 – Title & hook: [a question or surprising fact to open]
- Slide 2 – Objectives
- Slide 3 – Key concept 1: [...]
- Slide 4 – Key concept 2: [...]
- Slide 5 – Worked example / diagram: [...]
- Slide 6 – Common mistakes or misconceptions
- Slide 7 – Summary / recap
- Slide 8 – Quick quiz question or assignment

**SLIDE STYLE:**
- Look: [clean academic / whiteboard sketch / modern flat infographic / dark tech theme]
- Colours: [e.g. navy & white, school brand colours]
- Aspect ratio: [16:9 for projector-YouTube / 9:16 for phone]
- Include: [bullet points, labelled diagrams, formulas, slide numbers, your name/institution footer]

**VOICEOVER:**
- Voice: [female], accent: [American / neutral]
- Language: [English]
- Pace & tone: [teacher-like]
- Script: [paste your lecture notes] or "write the script from the outline above"

**ON-SCREEN TEXT:**
[Key terms to highlight, definitions to show verbatim, formulas, references]

**EXTRAS:**
- Motion: [subtle zoom, simple fades, bullet points appear one by one]
- Reference material to base it on: [attach PDF/notes/textbook chapter if any]
- Lecturer's name & institution for the title slide: [...]

**Output:** MP4, 480p (+ optional: the slides as a PPTX/PDF, and the script as a DOCX)

---

## Field reference (what to fill in)

| Field | Notes |
| --- | --- |
| Course / Subject | The module the lesson belongs to |
| Lesson title | One weekly topic per video |
| Learners | Degree level controls depth and assumed prior knowledge |
| Objectives | 2–4 measurable verbs (define, write, explain, derive, compare) |
| Duration | Drives pacing: ~130–150 spoken words per minute |
| Outline | 8 slides is the default; add more for longer lessons |
| Style | Pick one look and stay consistent across all slides |
| Aspect ratio | 16:9 = projector/YouTube, 9:16 = phone/Shorts |
| Voice | Gender, accent, and language are hard constraints on the TTS voice |
| Script | Can be generated from the outline if notes are not supplied |
| On-screen text | Definitions must match the script verbatim |
| Motion | Subtle only — heavy motion distracts from lecture content |
| Output | MP4 480p baseline; PPTX/PDF slides and DOCX script are optional extras |

## Production checklist

- [ ] Every objective is revisited in the summary slide
- [ ] Every diagram label is readable at 480p
- [ ] Voiceover has no filler ("um", "you know", "so basically")
- [ ] Formulas appear on screen exactly as spoken
- [ ] Slide numbers and footer present on every slide except the title
- [ ] Quiz/assignment slide includes a clear submission instruction
- [ ] Final runtime is within ±10% of the target duration
