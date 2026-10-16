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


# ----------------------------------------------------------------- Chapter 2
def fig_02_01():
    f = Fig("fig-02-01", 4.6, 3.6)
    H = f.H
    f.text(50, H - 3, "FORMAL SOURCES — Article 38(1) ICJ Statute", size=7.2, color=TEAL, bold=True)
    w = 30
    f.box(2, H - 22, w, 15, "Treaties\nUNCLOS · ECT · BITs · WTO · UNFCCC · Paris", "teal", size=6.8)
    f.box(35, H - 22, w, 15, "Custom\nPSNR core · minimum standard · no-harm rule", "teal", size=6.8)
    f.box(68, H - 22, w, 15, "General principles\ngood faith · pacta sunt servanda · reparation", "teal", size=6.8)
    f.box(2, H - 37, 96, 10, "Subsidiary means: judicial decisions (ICJ, ITLOS, WTO, ICSID tribunals) and the teachings of publicists", "light", size=6.8)
    f.text(50, H - 42.5, "NORMATIVE MATERIALS SHAPING INTERPRETATION AND PRACTICE", size=7.2, color=BRONZE, bold=True)
    items = ["Soft law\nRes 1803 · Rio · UNGPs · UNDRIP", "Industry standards\nAPI · ISO · AIEN models · ICMM",
             "Lender standards\nIFC PS · Equator Principles", "State contracts\nconcessions · PSCs · HGAs"]
    for k, t in enumerate(items):
        f.box(2 + k * 24.5, 3, 22.5, 16, t, "bronzel", size=6.4)
    for k in range(4):
        f.arrow(13 + k * 24.5, 19, 13 + k * 24.5, H - 36.8, color=BRONZE, lw=0.8, ls="--")
    f.save()


def fig_02_02():
    f = Fig("fig-02-02", 4.6, 2.6)
    H = f.H
    a = f.box(2, H - 20, 30, 16, "ATTRIBUTION\nArts 4–11: organs, entities exercising governmental authority, direction or control", "teal", size=6.4)
    b = f.box(2, H - 40, 30, 16, "BREACH\nArt 12: conduct not in conformity with an international obligation", "teal", size=6.4)
    c = f.box(38, H - 32, 22, 20, "INTERNATIONALLY WRONGFUL ACT\n(Art 2)", "bronze", size=6.8, bold=True)
    d = f.box(66, H - 16, 32, 13, "Circumstances precluding wrongfulness: consent, self-defence, countermeasures, force majeure, distress, necessity (Arts 20–25)", "ivory", size=5.8)
    e = f.box(66, H - 44, 32, 24, "CONSEQUENCES\ncessation and non-repetition (Art 30); full reparation (Art 31): restitution, compensation, satisfaction (Arts 34–37)", "light", size=6.2)
    f.arrow(32, H - 12, 38, H - 18, color=BRONZE, lw=1.2)
    f.arrow(32, H - 32, 38, H - 26, color=BRONZE, lw=1.2)
    f.arrow(60, H - 22, 66, H - 32, color=BRONZE, lw=1.2)
    f.arrow(66, H - 9.5, 60, H - 15, color=GREY, lw=0.9, ls="--")
    f.text(50, 2.5, "Chorzów Factory (1928): reparation must, as far as possible, wipe out all the consequences of the illegal act", size=6.2, color=GREY, italic=True)
    f.save()


# ----------------------------------------------------------------- Chapter 3
def fig_03_01():
    matrix("fig-03-01", ["Regalian / state ownership", "Accession / landowner", "Claim / free entry"], [
        ["Owner of minerals", "State, nation or people (e.g. Nigeria s 44(3), UK, Mexico art 27)", "Surface owner unless severed (US private land)", "Unowned until located and claimed (US Mining Law 1872)"],
        ["Grant instrument", "Licence, lease, concession, PSC, service contract", "Private lease negotiated with mineral owner", "Location and registration of claim; patent"],
        ["Rent capture", "Royalty, tax, profit oil, state participation", "Bonus and royalty to owner; state taxes", "Limited royalty; taxation"],
        ["Regulator's role", "Owner and regulator: opens acreage, sets terms", "Prevent waste, protect correlative rights", "Record claims, environmental control"],
        ["Typical issues", "Contract stability, transparency, community benefit", "Rule of capture, pooling, unitisation", "Conflicts with indigenous rights, environment"],
    ], w=4.6, h=3.6, size=6.2, first_w=19)


def fig_03_02():
    f = Fig("fig-03-02", 4.6, 3.0)
    H = f.H
    conds = ["Public purpose", "Non-discrimination", "Due process of law", "Payment of compensation"]
    for k, c in enumerate(conds):
        f.box(2 + k * 24.5, H - 15, 22.5, 11, c, "teal", size=6.8, bold=True)
    f.box(2, H - 34, 46, 13, "All conditions met\nLAWFUL EXPROPRIATION", "light", size=7, bold=True)
    f.box(52, H - 34, 46, 13, "Any condition unmet\nUNLAWFUL EXPROPRIATION", "bronze", size=7, bold=True)
    f.box(2, 3, 46, 20, "Treaty standard: fair market value immediately before the taking (or before it became known) + interest — Hull formula 'prompt, adequate and effective'", "ivory", size=6.2)
    f.box(52, 3, 46, 20, "Customary full reparation (Chorzów): may permit valuation at date of award and consequential loss — ADC v Hungary; Yukos; ConocoPhillips v Venezuela", "ivory", size=6.2)
    f.arrow(50, H - 15, 25, H - 21, color=BRONZE)
    f.arrow(50, H - 15, 75, H - 21, color=BRONZE)
    f.arrow(25, H - 34, 25, 23, color=GREY)
    f.arrow(75, H - 34, 75, 23, color=GREY)
    f.save()


# ----------------------------------------------------------------- Chapter 4
def fig_04_01():
    hub("fig-04-01", "GLOBAL ENERGY GOVERNANCE", [
        "Consumer security\nIEA (1974)",
        "Producer coordination\nOPEC · OPEC+ · GECF",
        "Nuclear\nIAEA · NPT safeguards",
        "Renewables\nIRENA · Clean Energy Ministerial",
        "Climate\nUNFCCC · Paris Agreement",
        "Trade & investment\nWTO · ECT · BITs · ICSID",
        "Finance & development\nWorld Bank · IFC · AfDB · JETPs",
        "Regional\nEU/ACER · Energy Community · ECOWAS/WAPP",
        "Dialogue & clubs\nIEF · G7 · G20",
    ], w=4.6, h=3.7, size=6.0, rx=38)


if __name__ == "__main__":
    import sys
    only = sys.argv[1:] or None
    for name, fn in sorted(globals().items()):
        if name.startswith("fig_") and callable(fn):
            if only and not any(name.startswith("fig_" + o) for o in only):
                continue
            fn()
            print("  drew", name)
