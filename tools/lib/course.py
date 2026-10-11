"""Content model for a weekly lecture.

A lecture is a JSON document:

{
  "course": "CPY 701",
  "course_title": "Introduction to Counseling Psychology",
  "week": 3,
  "title": "Week 3 — The Scientist-Practitioner Model",
  "references": [...],
  "slides": [ { ...slidekit spec..., "narration": "spoken words" }, ... ]
}

The `narration` field is what gets synthesised to audio; the rest of the spec
is what gets drawn. Keeping them on the same object guarantees they stay in
sync, and the build script refuses to ship a slide with no narration.
"""
from __future__ import annotations
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT = os.path.join(ROOT, "content")
BRANDING_PATH = os.path.join(ROOT, "data", "branding.json")

# Generated media goes in a directory whose name is NOT on the platform's
# list of non-persisted directories (out, build, dist, coverage, target,
# node_modules). Anything written to those names is silently dropped at the
# end of a turn, which destroyed a completed lecture once.
MEDIA = os.path.join(ROOT, "media")


def branding() -> dict:
    """Programme-wide branding defaults, so no lecture hard-codes them."""
    try:
        with open(BRANDING_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"institution": "", "lecturer": "", "programme": ""}


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


class Lecture:
    def __init__(self, data: dict, source_path: str | None = None):
        self.data = data
        self.source_path = source_path
        self.course = data["course"]
        self.course_title = data.get("course_title", "")
        self.week = int(data["week"])
        self.title = data["title"]
        self.slides = data["slides"]

    # ---------------------------------------------------------------- identity
    @property
    def slug(self) -> str:
        return f"{slug(self.course)}-w{self.week:02d}"

    @property
    def folder(self) -> str:
        return f"{slug(self.course)}"

    @property
    def char_count(self) -> int:
        """Characters of narration across all slides.

        Characters predict synthesised duration far better than words do:
        measured across the first three lectures the rate is 62.9, 64.0 and
        61.9 ms/char, a spread of 3 percent, whereas words per minute drifted
        from 154 to 163 over the same three. Longer words simply take longer to
        say, so the word count misleads as soon as the vocabulary changes.
        """
        return sum(len(s.get("narration", "")) for s in self.data["slides"])

    @property
    def word_count(self) -> int:
        return sum(len(s.get("narration", "").split()) for s in self.slides)

    #: Measured pace of the reference voice: 63.5 ms per character of text,
    #: pooled across the first three lectures (62.9, 64.0, 61.9).
    MS_PER_CHAR = 0.0635

    @property
    def est_speech(self) -> float:
        """Estimated narration duration in seconds."""
        return self.char_count * self.MS_PER_CHAR

    @property
    def est_minutes(self) -> float:
        """Estimated speech duration at the measured pace of the reference voice."""
        return self.est_speech / 60.0

    # ---------------------------------------------------------------- validate
    def validate(self) -> list[str]:
        problems = []
        if not self.slides:
            problems.append("no slides")
        for i, s in enumerate(self.slides, 1):
            if not s.get("layout"):
                problems.append(f"slide {i}: missing layout")
            if not s.get("narration", "").strip():
                problems.append(f"slide {i} ({s.get('layout')}): missing narration")
            if s.get("layout") not in ("title", "section", "quote", "end") and not s.get("title"):
                problems.append(f"slide {i} ({s.get('layout')}): missing title")
        return problems

    # ---------------------------------------------------------------- build
    def footer(self, i: int) -> dict:
        return {
            "footer_left": f"{self.course} · Week {self.week}",
            "footer_right": f"{i} / {len(self.slides)}",
        }

    def slide_specs(self) -> list[dict]:
        """Slide dicts with footers injected and narration stripped."""
        out = []
        for i, s in enumerate(self.slides, 1):
            spec = {k: v for k, v in s.items() if k != "narration"}
            f = self.footer(i)
            spec.setdefault("footer_left", f["footer_left"])
            spec.setdefault("footer_right", f["footer_right"])
            if spec.get("layout") == "title":
                b = branding()
                spec.setdefault("institution",
                                self.data.get("institution") or b.get("institution", ""))
                spec.setdefault("course", f"{self.course} — {self.course_title}")
                spec.setdefault("week", f"Week {self.week} of 16")
                spec.setdefault("lecturer",
                                self.data.get("lecturer") or b.get("lecturer", ""))
                spec.setdefault("duration", "35 minutes")
            out.append(spec)
        return out

    @classmethod
    def load(cls, path: str) -> "Lecture":
        with open(path, encoding="utf-8") as f:
            return cls(json.load(f), path)

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)


def course_index() -> list[dict]:
    """Read the course register and return one record per course."""
    import csv
    path = os.path.join(ROOT, "data", "courses.csv")
    seen, out = set(), []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            code = row["course_code"].strip()
            if not code or code in seen or "not selected" in row["type"]:
                continue
            if row["type"] == "Thesis" and code in seen:
                continue
            seen.add(code)
            out.append({
                "code": code,
                "title": row["course_title"].strip(),
                "semester": row["semester"].strip(),
                "type": row["type"].strip(),
                "track": row["track"].strip(),
            })
    return out
