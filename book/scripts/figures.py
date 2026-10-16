#!/usr/bin/env python3
"""Generate all diagrams for the book.  Run:  python book/scripts/figures.py"""
import math
from figlib import *


# ----------------------------------------------------------------- Chapter 1
def fig_01_01():
    f = Fig("fig-01-01", 4.6, 3.5)
    cx, cy = 50, f.H / 2
    labels = [
        ("Public international law", "sources · state responsibility ·\nlaw of the sea · watercourses"),
        ("International economic law", "trade · investment ·\nfinance · taxation"),
        ("Environmental & climate law", "prevention · EIA ·\nUNFCCC · Paris Agreement"),
        ("Comparative & domestic law", "constitutions · petroleum,\nmining & electricity statutes"),
        ("Transnational commercial law", "model contracts · arbitration ·\nproject finance"),
    ]
    for i in range(5):
        a = math.pi / 2 + 2 * math.pi * i / 5
        f.circle(cx + 12 * math.cos(a), cy + 12 * math.sin(a), 13, fc=TEAL_L if i % 2 == 0 else BRONZE_L,
                 ec=TEAL if i % 2 == 0 else BRONZE, lw=0.7, alpha=0.6)
    f.circle(cx, cy, 11.5, fc=TEAL, ec=TEAL)
    f.text(cx, cy, "INTERNATIONAL\nENERGY AND\nNATURAL\nRESOURCES LAW", size=7.0, color=WHITE, bold=True)
    for i, (h, d) in enumerate(labels):
        a = math.pi / 2 + 2 * math.pi * i / 5
        x, y = cx + 35 * math.cos(a), cy + 30 * math.sin(a)
        x = min(max(x, 17), 83)
        f.text(x, y + 2.2, h, size=7.4, color=TEAL if i % 2 == 0 else BRONZE, bold=True)
        f.text(x, y - 2.4, d, size=6.4, color=GREY)
    f.save()


def fig_01_02():
    vtimeline("fig-01-02", [
        ("1901", "D'Arcy concession granted by Persia"),
        ("1938", "Mexican oil nationalisation; the Hull formula"),
        ("1951", "Iranian nationalisation; Anglo-Iranian Oil Co (ICJ, 1952)"),
        ("1960", "OPEC founded at the Baghdad Conference"),
        ("1962", "UNGA Resolution 1803: permanent sovereignty"),
        ("1974", "NIEO Declaration and CERDS; IEA established"),
        ("1977", "Texaco v Libya and LIAMCO v Libya awards"),
        ("1982", "UNCLOS adopted; Aminoil award"),
        ("1994", "Energy Charter Treaty signed (in force 1998)"),
        ("2002", "Extractive Industries Transparency Initiative launched"),
        ("2015", "Paris Agreement adopted"),
        ("2021", "Nigeria's Petroleum Industry Act"),
        ("2023", "COP28: transitioning away from fossil fuels"),
        ("2025", "ICJ Advisory Opinion on climate change obligations"),
    ])


if __name__ == "__main__":
    import sys
    only = sys.argv[1:] or None
    for name, fn in sorted(globals().items()):
        if name.startswith("fig_") and callable(fn):
            if only and not any(name.startswith("fig_" + o) for o in only):
                continue
            fn()
            print("  drew", name)
