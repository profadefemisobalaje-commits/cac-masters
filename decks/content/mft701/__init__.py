"""MFT 701 — Fundamentals of Marriage and Family Therapy."""
from __future__ import annotations

from ...theme import Course, SyllabusItem
from .weeks_01_04 import WEEKS as W1
from .weeks_05_08 import WEEKS as W2
from .weeks_09_12 import WEEKS as W3
from .weeks_13_16 import WEEKS as W4

SYLLABUS = [
    SyllabusItem(1, "What Is Marriage and Family Therapy?", "The Field"),
    SyllabusItem(2, "The Systems Revolution", "Systems"),
    SyllabusItem(3, "Cybernetics and the Observing System", "Cybernetics"),
    SyllabusItem(4, "Circularity, Recursion and Relational Logic", "Circularity"),
    SyllabusItem(5, "Homeostasis, Change and the Family Life Cycle", "Life Cycle"),
    SyllabusItem(6, "Boundaries, Subsystems and Triangles", "Structure"),
    SyllabusItem(7, "The Pragmatics of Human Communication", "Communication"),
    SyllabusItem(8, "The Therapist's Stance and the Use of Self", "Stance"),
    SyllabusItem(9, "Attachment and Development Across the Lifespan", "Attachment"),
    SyllabusItem(10, "Culture, Power and the Relational Field", "Culture"),
    SyllabusItem(11, "A Map of the Models", "Models"),
    SyllabusItem(12, "Common Factors and the Mechanisms of Change", "Change"),
    SyllabusItem(13, "The Arc of Therapy: Joining, Assessing, Planning", "The Arc"),
    SyllabusItem(14, "Ethics, Law and Professional Responsibility", "Ethics"),
    SyllabusItem(15, "Research Literacy for the Systemic Clinician", "Evidence"),
    SyllabusItem(16, "Integration and Professional Identity", "Integration"),
]

COURSE = Course(
    code="MFT 701",
    title="Fundamentals of Marriage and Family Therapy",
    short="Fundamentals of MFT",
    semester="Semester I",
    units="1.71",
    syllabus=SYLLABUS,
    weeks=W1 + W2 + W3 + W4,
)
