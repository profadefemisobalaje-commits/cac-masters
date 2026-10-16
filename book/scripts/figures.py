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


# ----------------------------------------------------------------- Chapter 5
def fig_05_01():
    f = Fig("fig-05-01", 4.6, 3.1)
    H = f.H
    f.box(30, H - 12, 40, 9, "PETROLEUM ARRANGEMENTS", "teal", size=7.4, bold=True)
    a = f.box(3, H - 30, 40, 10, "Concessionary / licensing systems", "bronze", size=7, bold=True)
    b = f.box(57, H - 30, 40, 10, "Contractual systems", "bronze", size=7, bold=True)
    f.arrow(45, H - 12, 23, H - 20, color=GREY); f.arrow(55, H - 12, 77, H - 20, color=GREY)
    f.box(3, 3, 40, 30, "Investor owns production at wellhead\nState return: bonuses, rentals, royalty, taxes\n\nUK · Norway · US · Australia · Nigeria (PML)", "light", size=6.3)
    c = f.box(50, 3, 23, 30, "Production sharing contract\nState owns petroleum; contractor recovers costs (cost oil) and shares profit oil\nIndonesia · Angola · Nigeria (deep offshore)", "ivory", size=5.9)
    d = f.box(75, 3, 22, 30, "Service contract\nState owns all production; contractor paid a fee (pure or risk service)\nIraq TSCs · Iran", "ivory", size=5.9)
    f.arrow(23, H - 30, 23, 33, color=GREY)
    f.arrow(72, H - 30, 61.5, 33, color=GREY); f.arrow(82, H - 30, 86, 33, color=GREY)
    f.save()


def fig_05_02():
    f = Fig("fig-05-02", 4.6, 2.9)
    H = f.H
    rows = [
        ("Gross production", [(100, TEAL2, "10.0 mmbbl")]),
        ("Royalty (10%)", [(10, BRONZE, "State 1.0"), (90, TEAL_L, "Net 9.0")]),
        ("Cost oil (limit 60% of net)", [(10, "#FFFFFF", ""), (54, TEAL, "Contractor cost recovery 5.4"), (36, TEAL_L, "Profit oil 3.6")]),
        ("Profit oil split (60:40)", [(64, "#FFFFFF", ""), (21.6, BRONZE, "State 2.16"), (14.4, TEAL, "Ctr 1.44")]),
    ]
    top = H - 4
    rh = (H - 16) / len(rows)
    for k, (lab, segs) in enumerate(rows):
        y = top - (k + 1) * rh
        f.text(1, y + rh * 0.45, lab, size=6.4, color=INK, ha="left", bold=True)
        x = 33
        for w, col, t in segs:
            ww = w * 0.65
            if col != "#FFFFFF":
                f.rect(x, y + 1, ww, rh - 3, fc=col, ec="white", lw=0.6)
                f.text(x + ww / 2, y + 1 + (rh - 3) / 2, t, size=5.6,
                       color=WHITE if col in (TEAL, TEAL2, BRONZE) else INK)
            x += ww
    f.rect(3, 2, 3, 3, fc=BRONZE); f.text(7, 3.5, "State", size=6.2, ha="left")
    f.rect(20, 2, 3, 3, fc=TEAL); f.text(24, 3.5, "Contractor", size=6.2, ha="left")
    f.text(97, 3.5, "Before tax: State 3.16 · Contractor 6.84 (of which cost recovery 5.4) — hypothetical", size=5.6, color=GREY, ha="right", italic=True)
    f.save()


# ----------------------------------------------------------------- Chapter 6
def fig_06_01():
    f = Fig("fig-06-01", 4.6, 2.9)
    H = f.H
    stages = ["Upstream\nproduction", "Liquefaction\n(-162 °C)", "Shipping\n(LNG carrier)", "Regasification\n(terminal / FSRU)", "Transmission &\nend-users"]
    n = len(stages); gap = 2.4; w = (100 - 4 - gap * (n - 1)) / n
    yb = H * 0.56; bh = H * 0.26
    xs = []
    for k, st in enumerate(stages):
        x = 2 + k * (w + gap); xs.append(x)
        f.box(x, yb, w, bh, st, "teal" if k % 2 == 0 else "bronze", size=6.6, bold=True)
        if k:
            f.arrow(x - gap + 0.1, yb + bh / 2, x - 0.1, yb + bh / 2, color=INK, lw=1.2)
    contracts = ["Licence / PSC\nfeed-gas supply\nagreement", "Liquefaction or\ntolling agreement;\nEPC contract", "Time / voyage\ncharter;\nSPA (FOB / DES)", "Terminal use\nagreement;\nTPA rules", "Gas sales\nagreements;\nnetwork codes"]
    for x, c in zip(xs, contracts):
        f.box(x, H * 0.10, w, H * 0.34, c, "light", size=5.8)
        f.arrow(x + w / 2, yb - 0.3, x + w / 2, H * 0.44 + 0.3, color=GREY, lw=0.8, style="-")
    f.text(50, H - 3, "Physical chain (top) and principal legal instruments (bottom)", size=6.8, color=GREY, italic=True)
    f.save()


def fig_06_02():
    f = Fig("fig-06-02", 4.6, 2.8)
    H = f.H
    cols = [("Integrated", "Same owners hold upstream reserves and the liquefaction plant; LNG sold jointly", "Qatar · many Australian projects"),
            ("Merchant", "Plant company buys feed gas from producers and sells LNG on its own account", "Nigeria LNG (Bonny)"),
            ("Tolling", "Plant company provides liquefaction service for a fee; gas owners or offtakers keep title", "Freeport LNG (US)")]
    cw = 30; gap = 3
    for k, (h, d, e) in enumerate(cols):
        x = 2 + k * (cw + gap)
        f.box(x, H - 13, cw, 9, h, "teal", size=7.6, bold=True)
        f.box(x, H * 0.36, cw, H - 13 - H * 0.36 - 2, d, "light", size=6.3)
        f.box(x, H * 0.18, cw, H * 0.14, e, "ivory", size=6.0)
    f.text(50, H * 0.08, "Title to gas:  integrated = joint owners · merchant = plant company · tolling = gas owners / offtakers", size=6.0, color=GREY, italic=True)
    f.save()


# ----------------------------------------------------------------- Chapter 7
def fig_07_01():
    f = Fig("fig-07-01", 4.6, 3.0)
    H = f.H
    stages = ["Reconnaissance", "Exploration", "Development\n& construction", "Operation\n(production)", "Closure &\nrehabilitation", "Post-closure\nstewardship"]
    titles = ["Reconnaissance\npermit\n(non-exclusive)", "Exploration\nlicence\n(exclusive; work\nobligations)", "Mining lease;\nEIA approval;\nCDA; land access", "Royalties & tax;\nHSE compliance;\nreporting", "Closure plan;\nfinancial\nassurance", "Closure\ncertificate;\nresidual liability"]
    n = len(stages); gap = 1.6; w = (100 - 4 - gap * (n - 1)) / n
    yb = H * 0.58; bh = H * 0.22
    for k in range(n):
        x = 2 + k * (w + gap)
        f.box(x, yb, w, bh, stages[k], "teal" if k < 4 else "bronze", size=6.0, bold=True)
        if k:
            f.arrow(x - gap + 0.05, yb + bh / 2, x - 0.05, yb + bh / 2, color=INK, lw=1.0)
        f.box(x, H * 0.12, w, H * 0.38, titles[k], "light", size=5.4)
        f.arrow(x + w / 2, yb - 0.3, x + w / 2, H * 0.50 + 0.3, color=GREY, lw=0.8, style="-")
    f.text(50, H - 3.5, "Stages of the mining life cycle (top) and the corresponding legal instruments (bottom)", size=6.6, color=GREY, italic=True)
    f.text(50, H * 0.05, "Security of tenure links exploration to the right to mine; closure obligations are planned and secured from the outset", size=5.8, color=GREY, italic=True)
    f.save()


# ----------------------------------------------------------------- Chapter 8
def fig_08_01():
    f = Fig("fig-08-01", 4.6, 3.1)
    H = f.H
    stages = ["Extraction\n(mining / brine)", "Processing &\nrefining", "Components\n(cathodes, magnets)", "End products\n(batteries, EVs,\nturbines)", "Collection &\nrecycling"]
    law = ["Mining codes; state\nownership; export\nbans (Art XI GATT)", "Export controls;\ninvestment screening;\nindustrial policy", "Subsidies; local\ncontent; trade\nremedies", "Due diligence;\nforced-labour bans;\nbattery passport", "Recycled content;\nEPR; Basel\nConvention"]
    n = len(stages); gap = 2.2; w = (100 - 4 - gap * (n - 1)) / n
    yb = H * 0.50; bh = H * 0.24
    for k in range(n):
        x = 2 + k * (w + gap)
        f.box(x, yb, w, bh, stages[k], "teal" if k != 4 else "bronze", size=6.0, bold=True)
        if k:
            f.arrow(x - gap + 0.05, yb + bh / 2, x - 0.05, yb + bh / 2, color=INK, lw=1.0)
        f.box(x, H * 0.10, w, H * 0.30, law[k], "light", size=5.4)
        f.arrow(x + w / 2, yb - 0.3, x + w / 2, H * 0.40 + 0.3, color=GREY, lw=0.8, style="-")
    # recycling loop back to processing
    xr = 2 + 4 * (w + gap) + w / 2; xp = 2 + 1 * (w + gap) + w / 2
    f.arrow(xr, yb + bh + 0.3, xp, yb + bh + 0.3, color=BRONZE, lw=1.2, rad=0.25)
    f.text(50, H - 2.5, "Secondary supply (circular economy)", size=6.0, color=BRONZE, italic=True)
    f.text(50, H * 0.035, "Supply-chain stage (top) and principal legal levers (bottom); processing is the most concentrated stage", size=5.8, color=GREY, italic=True)
    f.save()


# ----------------------------------------------------------------- Chapter 9
def fig_09_01():
    matrix("fig-09-01",
           ["Competition in generation", "Wholesale buyer choice", "Retail choice", "Typical examples"],
           [["1. Vertically integrated monopoly", "No", "No", "No", "Many developing states; SE United States"],
            ["2. Single buyer", "Yes — for new PPAs", "No", "No", "1990s Asian & African IPP models"],
            ["3. Wholesale competition", "Yes", "Yes", "No", "Transitional systems; Nigeria (in law)"],
            ["4. Retail competition", "Yes", "Yes", "Yes", "EU; Great Britain; Texas; Australia"]],
           h=3.0, size=6.6, first_w=24)


# ----------------------------------------------------------------- Chapter 10
def fig_10_01():
    matrix("fig-10-01",
           ["What the state fixes", "Who bears price risk", "Typical instruments / examples"],
           [["Feed-in tariff", "Price per MWh", "Consumers / state", "German EEG 2000; Nigeria FiT Regs 2015"],
            ["Feed-in premium", "Premium over market", "Shared", "EU schemes after 2014 State aid guidelines"],
            ["Quota + certificates", "Quantity (obligation)", "Generator", "US RPS; UK Renewables Obligation"],
            ["Auction + PPA / CfD", "Quantity; price by bid", "Shared (two-way CfD)", "South Africa REIPPPP; UK CfD"],
            ["Fiscal incentives", "Tax credit or relief", "Taxpayers", "US ITC/PTC; 45Y/48E; duty waivers"]],
           h=3.3, size=6.6, first_w=22)


# ----------------------------------------------------------------- Chapter 11
def fig_11_01():
    matrix("fig-11-01",
           ["Objective", "Principal instruments", "Institutions / review"],
           [["Safety", "Protect people & environment from radiation; prevent accidents", "CNS 1994; Joint Convention 1997; IAEA Safety Standards", "National regulator; CNS peer review; IRRS"],
            ["Security", "Prevent theft, sabotage & malicious acts", "CPPNM & 2005 Amendment; ICSANT; UNSCR 1540", "Competent authority; IPPAS"],
            ["Safeguards", "Verify non-diversion to weapons", "NPT Art III; INFCIRC/153; Additional Protocol", "IAEA Board; UN Security Council"],
            ["Liability", "Compensate victims of nuclear damage", "Paris/Brussels; Vienna; Joint Protocol; CSC", "Courts of installation state"],
            ["Waste & decommissioning", "Avoid undue burdens on future generations", "Joint Convention; Euratom Dir. 2011/70", "Waste agencies; segregated funds"]],
           h=3.7, size=6.3, first_w=18)


# ----------------------------------------------------------------- Chapter 12
def fig_12_01():
    vflow("fig-12-01",
          ["Production\nelectrolysis (renewable / nuclear) or gas reforming + CCS",
           "Conversion & storage\nammonia, methanol, LOHC, salt caverns",
           "Transport\npipelines, ships, trucks",
           "Trade & import\ncertification, customs, CBAM",
           "End use\nsteel, fertiliser, shipping, aviation, power"],
          side=["Classification; permits; water & land rights; RFNBO / carbon-intensity rules",
                "Seveso & safety law; storage permits; pore space",
                "Network unbundling; third-party access; IGC Code; transit",
                "GoO vs mass balance; ISO 19870; TBT & SCM; H2Global",
                "Demand mandates; support schemes (CfDs, auctions); claims"],
          h=4.5, size=7.4)


# ----------------------------------------------------------------- Chapter 13
def fig_13_01():
    vflow("fig-13-01",
          ["Measure found inconsistent with a GATT obligation\n(e.g. Art I, III or XI)",
           "Tier 1 — Provisional justification\nDoes the measure fall within a paragraph of Art XX?",
           "Tier 2 — The chapeau\nNo arbitrary or unjustifiable discrimination; no disguised restriction",
           "Measure justified"],
          side=["Burden on complainant to establish violation",
                "(b) 'necessary' — weighing & balancing, alternatives; (g) 'relating to' + even-handedness",
                "Flexibility for different conditions; good-faith negotiation (US — Shrimp; US — Gasoline)",
                "Burden on respondent throughout Art XX"],
          h=3.9, size=7.4)


# ----------------------------------------------------------------- Chapter 14
def fig_14_01():
    matrix("fig-14-01",
           ["Core content", "Leading authorities"],
           [["Fair and equitable treatment", "Legitimate expectations; non-arbitrariness; due process; transparency; denial of justice", "Tecmed; Saluka; Parkerings; Waste Management II; Chevron v Ecuador II"],
            ["Full protection & security", "Due diligence against physical harm, incl. by third parties", "AAPL v Sri Lanka; Wena Hotels v Egypt"],
            ["National treatment / MFN", "No less favourable treatment in like circumstances", "SD Myers; Occidental I; Methanex; Maffezini; Plama"],
            ["Expropriation", "Public purpose, non-discrimination, due process, compensation (FMV)", "Metalclad; Methanex; Philip Morris v Uruguay; Yukos"],
            ["Umbrella clause", "Observance of obligations entered into with the investor", "SGS v Pakistan; SGS v Philippines; ECT Art 10(1)"]],
           h=3.7, size=6.5, first_w=20)


def fig_14_02():
    chain("fig-14-02",
          ["Dispute|& notice", "Cooling-off|negotiation", "Constitution|of tribunal", "Jurisdiction|& merits", "Award", "Annulment|or set-aside", "Enforce-|ment"],
          h=1.9, size=6.6,
          note="ICSID: annulment (Art 52), enforcement (Art 54). Others: set-aside at seat; New York Convention.")


def fig_15_01():
    hub("fig-15-01", "PROJECT\nCOMPANY", [
        "Host government\n(licence / PSC /\nconcession)",
        "JOA / shareholders'\nagreement",
        "EPC contract\n(construction)",
        "O&M agreement\n(operation)",
        "Fuel / gas supply\nagreement",
        "Offtake / PPA\n(buyer, utility)",
        "Loan & security\ndocuments (lenders)",
        "Insurance\n(property, liability,\npolitical risk)",
    ], size=7.0)


def fig_16_01():
    vflow("fig-16-01", [
        "Project revenues\n(PPA / offtake receipts into proceeds account)",
        "Operating & maintenance costs",
        "Taxes, royalties & regulatory charges",
        "Senior debt service\n(fees, interest, principal)",
        "Debt service reserve account top-up",
        "Maintenance & other reserve accounts",
        "Subordinated / mezzanine debt service",
        "Distribution lock-up test (DSCR, no default)",
        "Equity distributions to sponsors",
    ], side=[
        "Lender-controlled accounts",
        "Per O&M agreement and budget",
        "Fiscal regime (s 16.4–16.5)",
        "Senior lenders, ECAs, DFIs",
        "Typically 6 months' debt service",
        "Scheduled major overhauls",
        "Ranks behind senior debt",
        "Cash trapped if test fails",
        "Residual, first-loss capital",
    ], h=5.6, size=7.0)


def fig_16_02():
    matrix("fig-16-02",
           ["Concession (tax & royalty)", "Production sharing contract", "Service contract"],
           [["Ownership of production", "Investor at wellhead", "State; contractor takes cost & profit oil", "State; contractor paid a fee"],
            ["Main state instruments", "Bonus, royalty, income tax, resource rent tax", "Royalty, profit-oil split, income tax, state participation", "Retention of all production; fee set by contract"],
            ["Cost recovery", "Through tax deductions", "Cost oil, subject to a recovery limit", "Reimbursed with fee (risk or pure service)"],
            ["Risk bearer", "Investor bears most risk", "Contractor bears exploration risk", "State bears most market risk"],
            ["Examples", "UK, Norway, USA, Australia", "Indonesia, Angola, Nigeria (deep offshore)", "Iran, Iraq (TSCs), pre-2013 Mexico"]],
           h=3.6, size=6.4, first_w=19)


def fig_17_01():
    vflow("fig-17-01", [
        "Project proposal\n(oil field, mine, dam, power plant)",
        "Screening",
        "Scoping",
        "Impact statement / ESIA report",
        "Public participation & consultation",
        "Review by competent authority",
        "Decision & permit conditions",
        "Monitoring, follow-up & enforcement",
    ], side=[
        "Proponent prepares project description",
        "Is EIA required? Transboundary risk?",
        "Issues, alternatives, baseline, cumulative effects",
        "Direct & indirect effects, incl. downstream emissions (Finch)",
        "Affected communities; notification of other states (Espoo)",
        "Independent panel; expert advice",
        "Approval, refusal or conditions; reasons published",
        "Continuous monitoring over project life (Pulp Mills)",
    ], h=5.2, size=7.0)


def fig_18_01():
    chain("fig-18-01",
          ["NDC|every five years, Art\u00a04", "Domestic|measures, Art\u00a04(2)", "Transparency|reports, Art\u00a013", "Global|stocktake, Art\u00a014", "Enhanced NDC|progression, Art\u00a04(3)"],
          h=2.0, size=6.8,
          note="Stocktakes 2023, 2028 ... each informs the next round of NDCs; compliance committee (Art 15).")


def fig_19_01():
    matrix("fig-19-01",
           ["Core content", "Sources and authorities"],
           [["Equitable & reasonable utilisation", "Each state entitled to an equitable share; all factors weighed; vital human needs", "UNWC Arts 5, 6, 10; Gabčíkovo-Nagymaros; Helsinki Rules"],
            ["No significant harm", "Due diligence to prevent harm; mitigation; compensation where appropriate", "UNWC Art 7; Trail Smelter; Pulp Mills"],
            ["Notification & consultation", "Prior notice of planned measures; six-month reply; good-faith negotiation", "UNWC Arts 11–19; Lac Lanoux; Silala"],
            ["Cooperation & data exchange", "Joint bodies; regular exchange of hydrological data; flood warning", "UNWC Arts 8–9; Water Convention; OMVS; NBA"],
            ["Ecosystem protection", "Environmental flows; pollution control; emergencies", "UNWC Arts 20–28; Kishenganga awards"]],
           h=3.7, size=6.5, first_w=20)


def fig_20_01():
    f = Fig("fig-20-01", 4.6, 3.4)
    H = f.H
    sea = 30
    f.rect(10, 4, 90, sea - 4, fc="#DCEBEF")
    f.poly([(0, 4), (0, sea + 3), (10, sea + 3), (10.5, sea), (10, 4)], fc=BRONZE_L, ec=BRONZE)
    f.text(5, sea + 6, "LAND", size=6.5, color=BRONZE, bold=True)
    bed = [(10, sea - 2), (34, sea - 6), (44, sea - 8), (56, 12), (70, 8), (100, 6.5), (100, 0), (10, 0)]
    f.poly(bed, fc="#C9B48F", ec=BRONZE, lw=0.8)
    f.text(24, sea - 7.5, "shelf", size=5.6, color=INK, italic=True)
    f.text(46, 18, "slope", size=5.6, color=INK, italic=True)
    f.text(63, 6.5, "rise", size=5.6, color=INK, italic=True)
    f.text(86, 3, "abyssal plain", size=5.6, color=WHITE, italic=True)
    f.line([10.5, 10.5], [4, H - 5], color=TEAL, lw=1.0, ls="--")
    f.text(10.5, H - 3, "baseline", size=5.8, color=TEAL, bold=True)
    y1 = sea + 3
    water = [(10.5, 23, "Territorial sea 12 nm: sovereignty", "teal"),
             (23, 34, "Contiguous zone 24 nm", "teal2"),
             (34, 70, "EEZ 200 nm: sovereign rights over resources and energy from water, currents and winds (Art 56)", "light"),
             (70, 100, "High seas: freedoms incl. laying cables and pipelines (Art 87)", "ivory")]
    for (a_, b_, lab, st) in water:
        f.box(a_ + 0.3, y1, b_ - a_ - 0.6, 15, lab, st, size=5.5)
    y2 = y1 + 17
    seabed = [(10.5, 80, "Continental shelf (Arts 76-77): 200 nm or outer edge of the margin, max 350 nm or 2,500 m isobath + 100 nm", "bronzel"),
              (80, 100, "The Area (Part XI): common heritage; ISA", "bronze")]
    for (a_, b_, lab, st) in seabed:
        f.box(a_ + 0.3, y2, b_ - a_ - 0.6, 11, lab, st, size=5.5)
    f.text(99, H - 3, "Water column (lower row) and seabed (upper row); not to scale", size=5.2, color=GREY, ha="right", italic=True)
    f.save()


def fig_21_01():
    matrix("fig-21-01",
           ["What it requires", "Common failures in practice"],
           [["Free", "No coercion, intimidation, manipulation or undue pressure; community sets the process", "Security presence; selective payments; dividing communities"],
            ["Prior", "Sought before concessions are granted and before activities begin", "Consultation after licensing or construction"],
            ["Informed", "Full, accessible information on scope, risks, impacts and benefits; independent advice", "Technical documents only; no local language; no time to deliberate"],
            ["Consent", "Collective decision through the people's own institutions; may be given, conditioned or withheld", "Hand-picked representatives; treating consultation as consent"],
            ["Ongoing agreement", "Benefit-sharing, mitigation, monitoring and grievance redress over the project life", "One-off sign-off; no follow-up on changes"]],
           h=3.7, size=6.5, first_w=17)


if __name__ == "__main__":
    import sys
    only = sys.argv[1:] or None
    for name, fn in sorted(globals().items()):
        if name.startswith("fig_") and callable(fn):
            if only and not any(name.startswith("fig_" + o) for o in only):
                continue
            fn()
            print("  drew", name)
