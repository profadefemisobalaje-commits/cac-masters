"""Build the lecture decks.

    python -m decks.build --course 701            # every authored week + the bound course
    python -m decks.build --course 701 --weeks 1  # one week, for review
    python -m decks.build --course 701 --figures   # redraw diagrams only
"""
from __future__ import annotations

import argparse
import importlib
import re
import sys
from pathlib import Path

import shutil

from . import render_pdf, render_pptx, slides, textures, theme


def slug(text: str, maxlen: int = 60) -> str:
    s = text.replace("&", "and").replace("'", "").replace("’", "")
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")
    return s[:maxlen].rstrip("-")


FONT_BUNDLE = ["EBGaramond-Regular.otf", "EBGaramond-Italic.otf",
               "EBGaramond-Medium.otf", "EBGaramond-SemiBold.otf",
               "EBGaramond-SemiBoldItalic.otf", "EBGaramond-Bold.otf",
               "EBGaramond-BoldItalic.otf", "SourceSans3-Light.otf",
               "SourceSans3-Regular.otf", "SourceSans3-It.otf",
               "SourceSans3-Semibold.otf", "SourceSans3-SemiboldIt.otf",
               "SourceSans3-Bold.otf", "SourceSans3-BoldIt.otf",
               "OFL-EBGaramond.txt", "LICENSE-SourceSans.md"]


def bundle_fonts(dest: Path):
    """Copy the two typefaces (both OFL) beside the decks.

    PowerPoint substitutes fonts that are not installed, which changes the
    look of every slide. Shipping the files with the deck is the only reliable
    way to keep the design intact on another machine.
    """
    dest.mkdir(parents=True, exist_ok=True)
    for name in FONT_BUNDLE:
        src = theme.FONTS / name
        if src.exists():
            shutil.copy2(src, dest / name)
    (dest / "INSTALL-THESE-FONTS.txt").write_text(
        "EB Garamond and Source Sans 3 (both SIL Open Font License).\n\n"
        "Install every .otf file in this folder before opening the decks, or\n"
        "PowerPoint will substitute other fonts and the layout will change.\n\n"
        "Windows: select all .otf files > right-click > Install.\n"
        "macOS:   select all .otf files > double-click > Install Font.\n",
        encoding="utf-8")


def load_course(code: str):
    mod = importlib.import_module(f".content.mft{code}", package="decks")
    return mod.COURSE


def figure_module(code: str):
    return importlib.import_module(f".figures.mft{code}", package="decks")


def make_figures(course, weeks=None):
    mod = figure_module(course.code.split()[-1])
    pal = course.palette
    out = {}
    for n, fn in sorted(mod.FIGURES.items()):
        if weeks and n not in weeks:
            continue
        out[n] = fn(pal)
    return out


def build(code: str, weeks=None, do_figures=True, pdf=True, pptx=True,
          combined=True, verbose=True):
    course = load_course(code)
    root = Path(__file__).resolve().parent / "out" / course.slug
    root.mkdir(parents=True, exist_ok=True)
    bundle_fonts(root / "_Fonts (install before presenting)")
    textures.main()

    figs = make_figures(course, weeks) if do_figures else {}
    if do_figures and not figs:
        figs = make_figures(course, weeks)

    built = []
    for w in course.weeks:
        if weeks and w.n not in weeks:
            continue
        fig_path = figs.get(w.n)
        if fig_path is None:
            print(f"  ! no figure for week {w.n}")
            continue
        deck = slides.week_deck(course, w, fig_path)
        stem = f"{course.slug}-W{w.n:02d}-{slug(w.title)}"
        if pptx:
            p = root / f"{stem}.pptx"
            render_pptx.render(deck, p, f"{course.code} · Week {w.n:02d} — {w.title}")
            if verbose:
                print(f"  pptx  {p.name}  ({p.stat().st_size/1e6:.1f} MB, {len(deck.slides)} slides)")
        if pdf:
            p = root / f"{stem}.pdf"
            render_pdf.render(deck.slides, p, f"{course.code} · Week {w.n:02d} — {w.title}",
                              course.programme)
            if verbose:
                print(f"  pdf   {p.name}  ({p.stat().st_size/1e6:.1f} MB)")
        built.append(w.n)

    if combined and len(course.weeks) >= 1:
        cfigs = make_figures(course, [w.n for w in course.weeks]) if do_figures else figs
        deck = slides.course_deck(course, cfigs)
        stem = f"{course.slug}-Complete-Course"
        if pptx:
            p = root / f"{stem}.pptx"
            render_pptx.render(deck, p, f"{course.code} — {course.title}")
            if verbose:
                print(f"  pptx  {p.name}  ({p.stat().st_size/1e6:.1f} MB, {len(deck.slides)} slides)")
        if pdf:
            p = root / f"{stem}.pdf"
            render_pdf.render(deck.slides, p, f"{course.code} — {course.title}", course.programme)
            if verbose:
                print(f"  pdf   {p.name}  ({p.stat().st_size/1e6:.1f} MB, {render_pdf.page_count(p)} pages)")

    return built


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", default="701")
    ap.add_argument("--weeks", nargs="*", type=int)
    ap.add_argument("--figures", action="store_true", help="redraw diagrams only")
    ap.add_argument("--no-pptx", action="store_true")
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--single", action="store_true", help="skip the bound course edition")
    a = ap.parse_args(argv)

    if a.figures:
        course = load_course(a.course)
        for n, p in make_figures(course, a.weeks).items():
            print(f"  figure week {n}: {p.name}")
        return

    build(a.course, a.weeks, do_figures=True, pdf=not a.no_pdf,
          pptx=not a.no_pptx, combined=not a.single)


if __name__ == "__main__":
    main()
