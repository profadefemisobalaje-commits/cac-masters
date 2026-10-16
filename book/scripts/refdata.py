"""Curated reference data for the generated tables and indexes.

Each entry is (display, [regex patterns], optional "i" for case-insensitive).
Displays may contain *italic* segments.  Patterns are searched in the plain
text of the compiled PDF (whitespace normalised, hyphenation undone, curly
quotes straightened), so they should be written against running text.

The Table of Cases combines a curated list of international, EU, and regional
decisions with national cases and arbitral awards harvested automatically
from italicised "X v Y" names in the manuscript (variants of the same case are
merged).  Hypothetical exercises never use italicised "v" case names, so they
cannot leak into the table.
"""
import re
from pathlib import Path

MS = Path(__file__).resolve().parents[1] / "manuscript"

# ---------------------------------------------------------------------------
# CASES
# ---------------------------------------------------------------------------
INTERNATIONAL = [
    ("*Anglo-Iranian Oil Co* (United Kingdom v Iran) (ICJ 1952)", [r"Anglo-Iranian Oil Co"]),
    ("*Arctic Sunrise* Arbitration (Netherlands v Russia) (PCA 2015)", [r"Arctic Sunrise"]),
    ("*Armed Activities on the Territory of the Congo* (DRC v Uganda) (ICJ 2005, 2022)", [r"Armed Activities", r"DRC v Uganda"]),
    ("*Bangladesh/Myanmar* (ITLOS 2012)", [r"Bangladesh/Myanmar"]),
    ("*Bay of Bengal Maritime Boundary* (Bangladesh v India) (PCA 2014)", [r"Bangladesh v India"]),
    ("*Barbados v Trinidad and Tobago* (PCA 2006)", [r"Barbados v Trinidad"]),
    ("*Barcelona Traction, Light and Power Co* (Belgium v Spain) (ICJ 1970)", [r"Barcelona Traction"]),
    ("*Certain Activities Carried Out by Nicaragua in the Border Area* (Costa Rica v Nicaragua) (ICJ 2015, 2018)", [r"Certain Activities", r"Costa Rica v Nicaragua"]),
    ("*Certain Iranian Assets* (Iran v United States) (ICJ 2023)", [r"Certain Iranian Assets"]),
    ("*Chagos Marine Protected Area Arbitration* (Mauritius v United Kingdom) (PCA 2015)", [r"Chagos Marine Protected Area"]),
    ("*Climate Change and International Law* (Advisory Opinion) (ITLOS 2024)", [r"ITLOS[^.]{0,80}[Aa]dvisory [Oo]pinion", r"Climate Change and International Law"]),
    ("*Corfu Channel* (United Kingdom v Albania) (ICJ 1949)", [r"Corfu Channel"]),
    ("*Factory at Chorzów* (Germany v Poland) (PCIJ 1928)", [r"Chorz[oó]w"]),
    ("*Gabčíkovo-Nagymaros Project* (Hungary/Slovakia) (ICJ 1997)", [r"Gab[cč][ií]kovo"]),
    ("*Ghana/Côte d'Ivoire* Maritime Delimitation (ITLOS Special Chamber 2017)", [r"Ghana/C[oô]te d'Ivoire"]),
    ("*Guyana v Suriname* (PCA 2007)", [r"Guyana v Suriname"]),
    ("*Jan Mayen* (Denmark v Norway) (ICJ 1993)", [r"Jan Mayen"]),
    ("*Lac Lanoux* Arbitration (Spain v France) (1957)", [r"Lac Lanoux"]),
    ("*Land and Maritime Boundary between Cameroon and Nigeria* (ICJ 2002)", [r"Cameroon and Nigeria", r"Cameroon v Nigeria", r"Bakassi"]),
    ("*Maritime Delimitation in the Black Sea* (Romania v Ukraine) (ICJ 2009)", [r"Black Sea\*?\)? ?\(?Romania", r"Romania v Ukraine"]),
    ("*Maritime Delimitation in the Indian Ocean* (Somalia v Kenya) (ICJ 2021)", [r"Somalia v Kenya"]),
    ("*Maritime Dispute* (Peru v Chile) (ICJ 2014)", [r"Peru v Chile"]),
    ("*Nicaragua v Honduras* (ICJ 2007)", [r"Nicaragua v Honduras"]),
    ("*North Sea Continental Shelf* (ICJ 1969)", [r"North Sea Continental Shelf"]),
    ("*Obligations of States in respect of Climate Change* (Advisory Opinion) (ICJ 2025)", [r"Obligations of States in respect of Climate Change", r"ICJ[^.]{0,60}advisory opinion", r"Court's (2025 )?advisory opinion"]),
    ("*Oil Platforms* (Iran v United States) (ICJ 2003)", [r"Oil Platforms"]),
    ("*Pulp Mills on the River Uruguay* (Argentina v Uruguay) (ICJ 2010)", [r"Pulp Mills"]),
    ("*Responsibilities and Obligations of States Sponsoring Persons and Entities with respect to Activities in the Area* (ITLOS Seabed Disputes Chamber 2011)", [r"Seabed Disputes Chamber"]),
    ("*Silala* (Chile v Bolivia) (ICJ 2022)", [r"Silala"]),
    ("*South China Sea Arbitration* (Philippines v China) (PCA 2016)", [r"South China Sea Arbitration", r"Philippines v China"]),
    ("*SS Lotus* (France v Turkey) (PCIJ 1927)", [r"Lotus"]),
    ("*Territorial and Maritime Dispute* (Nicaragua v Colombia) (ICJ 2012)", [r"Nicaragua v Colombia"]),
    ("*Trail Smelter* Arbitration (United States/Canada) (1938, 1941)", [r"Trail Smelter"]),
    ("*Treaty of Amity* (Iran v United States) (ICJ 2018–2021)", [r"Treaty of Amity"]),
    ("*Whaling in the Antarctic* (Australia v Japan) (ICJ 2014)", [r"Whaling in the Antarctic"]),
]

EU_COURTS = [
    ("*Austria v Commission* (C-594/18 P) (Hinkley Point C) (2020)", [r"Austria v Commission"]),
    ("*Commission v Austria* (C-346/14) (2016)", [r"Commission v Austria"]),
    ("*Commission v Council* (C-29/99) (2002)", [r"Commission v Council"]),
    ("*Commission v Germany* (C-718/18) (2021)", [r"Commission v Germany", r"European Commission v Federal Republic of Germany"]),
    ("*DEI v Commission* (Greek lignite)", [r"DEI v Commission", r"European Commission v DEI"]),
    ("*Germany v Commission* (C-405/16 P) (2019)", [r"Germany v Commission"]),
    ("*Germany v Poland* (C-848/19 P) (OPAL, energy solidarity) (2021)", [r"(?<!\()Germany v Poland(?!\))", r"Germany v Republic of Poland"]),
    ("*PreussenElektra* (C-379/98) (2001)", [r"PreussenElektra"]),
    ("*Republic of Moldova v Komstroy LLC* (C-741/19) (2021)", [r"Komstroy"]),
    ("*Slovak Republic v Achmea BV* (C-284/16) (2018)", [r"Achmea"]),
    ("*Tempus Energy Ltd v European Commission* (General Court 2018)", [r"Tempus Energy"]),
    ("*WM and Sovim SA v Luxembourg Business Registers* (C-37/20 and C-601/20) (2022)", [r"Sovim"]),
]

REGIONAL_HR = [
    ("*African Commission on Human and Peoples' Rights v Kenya* (Ogiek) (African Court 2017, 2022)", [r"Ogiek"]),
    ("*Carême v France* (ECtHR 2024)", [r"Car[eê]me"]),
    ("*Duarte Agostinho v Portugal and 32 Others* (ECtHR 2024)", [r"Duarte Agostinho"]),
    ("*Endorois Welfare Council v Kenya* (African Commission 2010)", [r"Endorois"]),
    ("*Greenpeace Nordic and Others v Norway* (ECtHR 2025)", [r"Greenpeace Nordic[^.]{0,30}v Norway"]),
    ("*Kaliña and Lokono Peoples v Suriname* (IACtHR 2015)", [r"Kali[nñ]a and Lokono"]),
    ("*Kichwa Indigenous People of Sarayaku v Ecuador* (IACtHR 2012)", [r"Sarayaku"]),
    ("*Lhaka Honhat v Argentina* (IACtHR 2020)", [r"Lhaka Honhat"]),
    ("*Mayagna (Sumo) Awas Tingni Community v Nicaragua* (IACtHR 2001)", [r"Awas Tingni"]),
    ("*Saramaka People v Suriname* (IACtHR 2007)", [r"Saramaka"]),
    ("*SERAC and CESR v Nigeria* (African Commission 2001)", [r"SERAC"]),
    ("*SERAP v Nigeria* (ECOWAS Court of Justice 2012)", [r"SERAP v"]),
    ("*Verein KlimaSeniorinnen Schweiz v Switzerland* (ECtHR 2024)", [r"KlimaSeniorinnen"]),
    ("Advisory Opinion OC-23/17 on the Environment and Human Rights (IACtHR 2017)", [r"OC-23/17"]),
    ("Advisory Opinion OC-32/25 on the Climate Emergency (IACtHR 2025)", [r"OC-32/25", r"Inter-American Court[^.]{0,80}[Aa]dvisory [Oo]pinion[^.]{0,40}(2025|climate)"]),
]

STATES = {
    "Albania", "Algeria", "Argentina", "Argentine Republic", "Australia", "Bolivia", "Bulgaria", "Cameroon",
    "Canada", "Colombia", "Congo", "Czech Republic", "Ecuador", "Egypt", "El Salvador", "European Union",
    "Germany", "Hungary", "India", "Indonesia", "Iran", "Italy", "Kazakhstan", "Kenya", "Libya", "Lithuania",
    "Mexico", "Morocco", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Romania",
    "Russia", "Russian Federation", "Slovak Republic", "Spain", "Sri Lanka", "Tanzania", "Ukraine",
    "United States", "Uruguay", "Uzbekistan", "Venezuela", "Yemen", "Switzerland", "Portugal", "France",
    "Norway", "Suriname", "Kingdom of Spain",
}
STATE_PREFIX = re.compile(r"^(the |Islamic |Bolivarian |Arab |People's |Federal |Democratic |Libyan |"
                          r"Republic of |Kingdom of |Government of (the )?|State of )+")
# Decisions of national courts with a state as respondent (not arbitral awards)
NATIONAL_V_STATE = {"Juliana", "Neubauer", "Upjohn", "Urgenda", "Leghari", "Adesanya", "Held",
                    "Greenpeace Ltd", "Pabai", "Tsleil-Waututh", "Process and Industrial Developments", "Spain"}
# Arbitral awards that the state-respondent heuristic would miss
ARBITRAL_EXTRA = {"Himpurna", "Sapphire", "Petroleum Development (Trucial Coast)", "Kuwait",
                  "Government of the State of Kuwait", "Atlantic LNG", "Nord Stream 2 AG",
                  "PT Perusahaan Gas Negara", "Corporación Mexicana"}
SKIP_FIRST = re.compile(r"^(Commission|European Commission|Austria|Germany|Federal Republic of Germany|"
                        r"Slovak Republic|Slowakische|Republic of Moldova|République|DEI|Hungary|Iran|"
                        r"Costa Rica|Nicaragua|Bangladesh|Australia|Chile|Denmark|Peru|Romania|Spain v France|"
                        r"Netherlands|Mauritius|United Kingdom|Cameroon|DRC|Democratic Republic|Philippines|"
                        r"Somalia|Guyana|Barbados|Argentina|EFTA|Tempus|WM and Sovim|SERAC|Social and Economic|"
                        r"SERAP|African Commission|Saramaka|Kichwa|Mayagna|Kali|Lhaka|Endorois|Verein|"
                        r"Duarte|Car[eê]me|Greenpeace Nordic and Others|Greenpeace Nordic v)")
SECOND_SKIP = {"Royal", "Dutch", "Republic", "of", "the", "Islamic", "Bolivarian", "Arab",
               "Kingdom", "People's", "Federal", "Government", "State", "London", "Borough"}
SECOND_ALIAS = [("Nigerian National Petroleum", "NNPC"), ("Securities and Exchange Commission", "SEC"),
                ("Environmental Protection Agency", "EPA"), ("American Independent Oil", "Aminoil")]
FIRST_ALIAS = [("Government of the State of Kuwait", "Kuwait"), ("Município", "Municipio"),
               ("M & J", "M&J"), ("National Association of Regulatory Utility Commissioners", "NARUC")]


def _clean(name):
    name = re.sub(r"\s+", " ", name.strip()).rstrip(".,;")
    name = name.replace("’", "'")
    return name


def _harvest():
    texts = []
    for sub in ("chapters", "appendices"):
        for f in sorted((MS / sub).glob("*.md")):
            texts.append(f.read_text(encoding="utf-8"))
    text = "\n".join(texts)
    found = {}
    for m in re.finditer(r"(?<![*\w])\*([A-Z][^*\n]{1,100}? v [^*\n]{2,100}?)\*(?!\*)", text):
        for name in m.group(1).split(";"):
            name = _clean(name)
            if " v " not in name or "[" in name or len(name) > 100:
                continue
            first, second = name.split(" v ", 1)
            first, second = first.strip(), second.strip()
            if "(" in first or SKIP_FIRST.match(first) or SKIP_FIRST.match(name):
                continue
            found[name] = found.get(name, 0) + 1
    return found


def _key(first, second):
    for a, b in FIRST_ALIAS:
        if first.startswith(a):
            first = b + first[len(a):]
    for a, b in SECOND_ALIAS:
        if second.startswith(a):
            second = b
    f = re.sub(r"[^\w]", "", first.split()[0]).lower()
    words = [w for w in re.split(r"[\s,]+", second) if w and w not in SECOND_SKIP]
    s = re.sub(r"[^\w]", "", words[0]).lower()[:4] if words else ""
    return f, s


def _auto_cases():
    found = _harvest()
    groups = {}
    for name, n in found.items():
        first, second = name.split(" v ", 1)
        groups.setdefault(_key(first, second), []).append((name, n))
    arb, nat = [], []
    for variants in groups.values():
        variants.sort(key=lambda x: (-x[1], -min(len(x[0]), 70)))
        display = variants[0][0]
        pats = []
        for name, _ in variants:
            first, second = name.split(" v ", 1)
            w2 = second.strip().split()[0]
            p = re.escape(first.strip()) + r"\s+v\.?\s+" + re.escape(w2)
            if p not in pats:
                pats.append(p)
        first, second = display.split(" v ", 1)
        resp = STATE_PREFIX.sub("", re.sub(r"\s*\(.*$", "", second.strip()))
        resp = re.sub(r"\s+(and|&)\s+\d+.*$", "", resp)
        if display.startswith("Yukos Universal"):
            pats.append(r"\bYukos\b(?! Capital)")
        entry = (f"*{display}*", pats)
        is_state = resp in STATES or second.strip() in STATES
        if any(first.startswith(x) for x in ARBITRAL_EXTRA):
            arb.append(entry)
        elif is_state and not any(first.startswith(x) for x in NATIONAL_V_STATE):
            arb.append(entry)
        else:
            nat.append(entry)
    return arb, nat


_ARB, _NAT = _auto_cases()

CASES = [
    ("International Courts and Tribunals", INTERNATIONAL),
    ("Court of Justice of the European Union", EU_COURTS),
    ("Regional Human Rights Courts and Commissions", REGIONAL_HR),
    ("Investment and State Contract Arbitration", _ARB),
    ("National Courts", _NAT),
]

# ---------------------------------------------------------------------------
# TREATIES AND INTERNATIONAL INSTRUMENTS
# ---------------------------------------------------------------------------
TREATIES = [
    ("Multilateral Treaties", [
        ("Agreement Establishing the African Continental Free Trade Area 2018", [r"AfCFTA", r"African Continental Free Trade Area"]),
        ("Agreement on an International Energy Program 1974", [r"International Energy Program"]),
        ("Agreement on Marine Biological Diversity of Areas beyond National Jurisdiction (BBNJ) 2023", [r"BBNJ", r"Biological Diversity of Areas beyond"]),
        ("Agreement relating to the Implementation of Part XI of UNCLOS 1994", [r"Part XI"]),
        ("African Charter on Human and Peoples' Rights 1981", [r"African Charter"]),
        ("American Convention on Human Rights 1969", [r"American Convention"]),
        ("Aarhus Convention 1998", [r"Aarhus"]),
        ("Bamako Convention 1991", [r"Bamako"]),
        ("Basel Convention 1989", [r"Basel Convention"]),
        ("Charter of the United Nations 1945", [r"UN Charter", r"Charter of the United Nations"]),
        ("Convention on Biological Diversity 1992", [r"Convention on Biological Diversity", r"\bCBD\b"]),
        ("Convention on Nuclear Safety 1994", [r"Convention on Nuclear Safety"]),
        ("Convention on Supplementary Compensation for Nuclear Damage 1997", [r"Supplementary Compensation"]),
        ("Convention on the Physical Protection of Nuclear Material 1980 (amended 2005)", [r"Physical Protection of Nuclear Material", r"CPPNM"]),
        ("Early Notification and Assistance Conventions 1986", [r"Early Notification"]),
        ("ECOWAS Energy Protocol 2003", [r"ECOWAS Energy Protocol"]),
        ("ECOWAS Revised Treaty 1993", [r"ECOWAS Revised Treaty", r"Revised Treaty of ECOWAS"]),
        ("Energy Charter Treaty 1994", [r"Energy Charter Treaty", r"\bECT\b"]),
        ("Escazú Agreement 2018", [r"Escaz[uú]"]),
        ("Espoo Convention 1991", [r"Espoo"]),
        ("European Convention on Human Rights 1950", [r"European Convention on Human Rights", r"\bECHR\b"]),
        ("General Agreement on Tariffs and Trade 1947/1994", [r"\bGATT\b"]),
        ("General Agreement on Trade in Services 1994", [r"\bGATS\b"]),
        ("ICSID Convention 1965", [r"ICSID Convention"]),
        ("ILO Convention No 169 on Indigenous and Tribal Peoples 1989", [r"ILO Convention (No\.? )?169", r"Convention No\.? 169"]),
        ("International Covenant on Civil and Political Rights 1966", [r"International Covenant on Civil and Political Rights", r"\bICCPR\b"]),
        ("International Covenant on Economic, Social and Cultural Rights 1966", [r"International Covenant on Economic, Social and Cultural Rights", r"\bICESCR\b"]),
        ("Joint Convention on the Safety of Spent Fuel and Radioactive Waste Management 1997", [r"Joint Convention"]),
        ("Kyoto Protocol 1997", [r"Kyoto Protocol"]),
        ("MARPOL 1973/1978", [r"MARPOL"]),
        ("Mauritius Convention on Transparency 2014", [r"Mauritius Convention"]),
        ("Minamata Convention on Mercury 2013", [r"Minamata"]),
        ("Montreal Protocol 1987 (and Kigali Amendment 2016)", [r"Montreal Protocol", r"Kigali Amendment"]),
        ("New York Convention 1958", [r"New York Convention"]),
        ("OECD Anti-Bribery Convention 1997", [r"Anti-Bribery Convention"]),
        ("Paris Agreement 2015", [r"Paris Agreement"]),
        ("Paris Convention on Third Party Liability in the Field of Nuclear Energy 1960", [r"Paris Convention on Third Party", r"Paris Convention\b(?! on the Protection)"]),
        ("Singapore Convention on Mediation 2019", [r"Singapore Convention"]),
        ("Treaty on the Non-Proliferation of Nuclear Weapons 1968", [r"Non-Proliferation of Nuclear Weapons", r"\bNPT\b"]),
        ("UN Convention against Corruption 2003", [r"Convention against Corruption", r"\bUNCAC\b"]),
        ("UN Convention on the Law of the Sea 1982", [r"UNCLOS", r"Convention on the Law of the Sea"]),
        ("UN Framework Convention on Climate Change 1992", [r"UNFCCC", r"Framework Convention on Climate Change"]),
        ("UN Watercourses Convention 1997", [r"Watercourses Convention"]),
        ("UNECE Water Convention 1992", [r"UNECE Water Convention", r"Water Convention"]),
        ("United States–Mexico–Canada Agreement 2018 (and NAFTA 1992)", [r"USMCA", r"NAFTA"]),
        ("Vienna Convention on Civil Liability for Nuclear Damage 1963", [r"Vienna Convention on Civil Liability"]),
        ("Vienna Convention on the Law of Treaties 1969", [r"Vienna Convention on the Law of Treaties", r"\bVCLT\b"]),
        ("WTO Agreement on Subsidies and Countervailing Measures", [r"SCM Agreement"]),
        ("WTO Agreement on Technical Barriers to Trade", [r"TBT Agreement"]),
        ("WTO Agreement on Trade-Related Investment Measures", [r"TRIMs"]),
    ]),
    ("Resolutions, Declarations, and Soft Law Instruments", [
        ("Africa Mining Vision 2009", [r"Africa Mining Vision"]),
        ("Charter of Economic Rights and Duties of States 1974", [r"Charter of Economic Rights"]),
        ("Equator Principles", [r"Equator Principles"]),
        ("IFC Performance Standards 2012", [r"Performance Standards?"]),
        ("ILC Articles on Responsibility of States for Internationally Wrongful Acts 2001", [r"Articles on (State )?Responsibility", r"ARSIWA"]),
        ("ILC Draft Articles on Prevention of Transboundary Harm 2001", [r"Prevention of Transboundary Harm"]),
        ("Kunming-Montreal Global Biodiversity Framework 2022", [r"Kunming"]),
        ("OECD Guidelines for Multinational Enterprises (2023)", [r"OECD Guidelines"]),
        ("Rio Declaration on Environment and Development 1992", [r"Rio Declaration"]),
        ("Santiago Principles 2008", [r"Santiago Principles"]),
        ("Stockholm Declaration 1972", [r"Stockholm Declaration"]),
        ("UN Declaration on the Rights of Indigenous Peoples 2007", [r"UNDRIP", r"Declaration on the Rights of Indigenous Peoples"]),
        ("UN Guiding Principles on Business and Human Rights 2011", [r"Guiding Principles on Business", r"\bUNGPs?\b"]),
        ("UNGA Resolution 1803 (XVII) on Permanent Sovereignty over Natural Resources 1962", [r"Resolution 1803", r"\b1803\b"]),
        ("Voluntary Principles on Security and Human Rights 2000", [r"Voluntary Principles"]),
    ]),
]

# ---------------------------------------------------------------------------
# LEGISLATION
# ---------------------------------------------------------------------------
LEGISLATION = [
    ("Nigeria", [
        ("Constitution of the Federal Republic of Nigeria 1999", [r"Constitution of the Federal Republic of Nigeria", r"1999 Constitution"]),
        ("Allocation of Revenue (Abolition of Dichotomy in the Application of the Principle of Derivation) Act 2004", [r"Abolition of Dichotomy"]),
        ("Arbitration and Mediation Act 2023", [r"Arbitration and Mediation Act"]),
        ("Associated Gas Re-Injection Act 1979", [r"Associated Gas Re-?[Ii]njection Act"]),
        ("Climate Change Act 2021", [r"Climate Change Act 2021", r"Nigeria's Climate Change Act"]),
        ("Companies and Allied Matters Act 2020", [r"Companies and Allied Matters Act"]),
        ("Deep Offshore and Inland Basin Production Sharing Contracts Act 1999 (as amended 2019)", [r"Deep Offshore and Inland Basin"]),
        ("Electric Power Sector Reform Act 2005", [r"Electric Power Sector Reform Act"]),
        ("Electricity Act 2023", [r"Electricity Act 2023"]),
        ("Environmental Impact Assessment Act", [r"Environmental Impact Assessment Act"]),
        ("Federal Competition and Consumer Protection Act 2018", [r"Federal Competition and Consumer Protection Act"]),
        ("Fiscal Responsibility Act 2007", [r"Fiscal Responsibility Act"]),
        ("Freedom of Information Act 2011", [r"Freedom of Information Act"]),
        ("Land Use Act 1978", [r"Land Use Act"]),
        ("Nigeria Data Protection Act 2023", [r"Nigeria Data Protection Act"]),
        ("Nigeria Extractive Industries Transparency Initiative Act 2007", [r"NEITI\)? Act", r"Extractive Industries Transparency Initiative Act"]),
        ("Nigerian Minerals and Mining Act 2007", [r"Minerals and Mining Act 2007"]),
        ("Nigerian Oil and Gas Industry Content Development Act 2010", [r"Content Development Act"]),
        ("Nuclear Safety and Radiation Protection Act 1995", [r"Nuclear Safety and Radiation Protection Act"]),
        ("Petroleum Act 1969", [r"Petroleum Act 1969"]),
        ("Petroleum Industry Act 2021", [r"Petroleum Industry Act", r"\bPIA\b"]),
    ]),
    ("Other African Jurisdictions", [
        ("Ghana: Minerals and Mining Act 2006 (Act 703)", [r"Act 703"]),
        ("Ghana: Petroleum (Exploration and Production) Act 2016 (Act 919)", [r"Exploration and Production\) Act 2016", r"Act 919"]),
        ("Ghana: Petroleum Revenue Management Act 2011 (Act 815)", [r"Petroleum Revenue Management Act"]),
        ("Kenya: Energy Act 2019", [r"Energy Act 2019"]),
        ("South Africa: Climate Change Act 2024", [r"Climate Change Act 2024"]),
        ("South Africa: Electricity Regulation Act 2006", [r"Electricity Regulation Act"]),
        ("South Africa: Mineral and Petroleum Resources Development Act 2002", [r"Mineral and Petroleum Resources Development Act", r"MPRDA"]),
        ("Tanzania: Natural Wealth and Resources (Permanent Sovereignty) Act 2017", [r"Permanent Sovereignty\) Act"]),
        ("Tanzania: Natural Wealth and Resources Contracts (Review and Re-Negotiation of Unconscionable Terms) Act 2017", [r"Unconscionable Terms\) Act"]),
        ("Democratic Republic of the Congo: Mining Code 2002 (revised 2018)", [r"Mining Code"]),
    ]),
    ("United Kingdom", [
        ("Arbitration Act 1996", [r"Arbitration Act 1996"]),
        ("Arbitration Act 2025", [r"Arbitration Act 2025"]),
        ("Bribery Act 2010", [r"Bribery Act"]),
        ("Climate Change Act 2008", [r"Climate Change Act 2008"]),
        ("Companies Act 2006", [r"Companies Act 2006"]),
        ("Economic Crime and Corporate Transparency Act 2023", [r"Economic Crime and Corporate Transparency Act"]),
        ("Electricity Act 1989", [r"Electricity Act 1989"]),
        ("Energy Act 2023", [r"Energy Act 2023"]),
        ("National Security and Investment Act 2021", [r"National Security and Investment Act"]),
        ("Petroleum Act 1998", [r"Petroleum Act 1998"]),
    ]),
    ("United States", [
        ("Energy Policy Act of 2005", [r"Energy Policy Act"]),
        ("Federal Power Act 1935", [r"Federal Power Act"]),
        ("Foreign Corrupt Practices Act 1977", [r"Foreign Corrupt Practices Act", r"\bFCPA\b"]),
        ("Foreign Investment Risk Review Modernization Act of 2018", [r"Foreign Investment Risk Review"]),
        ("Inflation Reduction Act of 2022", [r"Inflation Reduction Act"]),
        ("Mineral Leasing Act 1920", [r"Mineral Leasing Act"]),
        ("National Environmental Policy Act 1969", [r"National Environmental Policy Act", r"\bNEPA\b"]),
        ("Oil Pollution Act of 1990", [r"Oil Pollution Act"]),
        ("Outer Continental Shelf Lands Act 1953", [r"Outer Continental Shelf Lands Act"]),
    ]),
    ("European Union", [
        ("Regulation (EU) 2019/943 and Directive (EU) 2019/944 (electricity market)", [r"2019/94[34]"]),
        ("Regulation (EU) 2021/1119 (European Climate Law)", [r"2021/1119", r"European Climate Law"]),
        ("Regulation (EU) 2023/956 (Carbon Border Adjustment Mechanism)", [r"2023/956", r"\bCBAM\b"]),
        ("Regulation (EU) 2023/1542 (Batteries)", [r"2023/1542", r"Batteries Regulation"]),
        ("Regulation (EU) 2024/1252 (Critical Raw Materials Act)", [r"2024/1252", r"Critical Raw Materials Act"]),
        ("Regulation (EU) 2024/1689 (Artificial Intelligence Act)", [r"2024/1689", r"\bAI Act\b"]),
        ("Regulation (EU) 2024/1787 (Methane)", [r"2024/1787", r"Methane Regulation"]),
        ("Directive (EU) 2022/2464 (Corporate Sustainability Reporting Directive)", [r"2022/2464", r"\bCSRD\b"]),
        ("Directive (EU) 2024/1760 (Corporate Sustainability Due Diligence Directive)", [r"2024/1760", r"\bCSDDD\b"]),
        ("Directive (EU) 2018/2001 (Renewable Energy Directive, as amended)", [r"2018/2001", r"Renewable Energy Directive"]),
        ("Directive 2003/87/EC (EU Emissions Trading System)", [r"2003/87", r"EU ETS"]),
        ("Regulation (EU) 2017/821 (Conflict Minerals)", [r"2017/821", r"Conflict Minerals Regulation"]),
        ("Regulation (EU) 2020/852 (Taxonomy)", [r"2020/852", r"Taxonomy Regulation"]),
    ]),
    ("Other Jurisdictions", [
        ("Australia: Native Title Act 1993 (Cth)", [r"Native Title Act"]),
        ("Brazil: Petroleum Law (Law 9.478/1997)", [r"9\.478"]),
        ("Canada: Constitution Act 1982, s 35", [r"Constitution Act 1982"]),
        ("India: Electricity Act 2003", [r"Electricity Act 2003"]),
        ("Norway: Petroleum Act 1996", [r"Petroleum Act 1996"]),
    ]),
]

# ---------------------------------------------------------------------------
# INDEXES
# ---------------------------------------------------------------------------
def _terms(pairs, flag="i"):
    return [(d, p if isinstance(p, list) else [p], flag) for d, p in pairs]


INDEX_CONCEPTS = _terms([
    ("abuse of process", r"abuse of process"),
    ("access to justice", r"access to justice"),
    ("administrative law", r"administrative law"),
    ("annulment (ICSID)", r"annulment"),
    ("anti-corruption", [r"anti-corruption", r"\bbribery\b"]),
    ("arbitrability", r"arbitrab"),
    ("attribution (state responsibility)", r"\battribut(ion|able) to (the )?state"),
    ("benefit-sharing", r"benefit[- ]sharing"),
    ("burden of proof", r"burden of proof"),
    ("causation", r"\bcausation\b"),
    ("common but differentiated responsibilities", r"common but differentiated"),
    ("common heritage of mankind", r"common heritage"),
    ("compensation (expropriation)", r"(prompt, adequate|full compensation|Hull formula)"),
    ("consultation, duty of", r"duty to consult"),
    ("corporate veil", r"corporate veil"),
    ("cost recovery", r"cost recovery"),
    ("countermeasures", r"countermeasures"),
    ("customary international law", r"customary international law"),
    ("decommissioning", r"decommissioning"),
    ("denial of benefits", r"denial of benefits"),
    ("denial of justice", r"denial of justice"),
    ("derivation principle", r"derivation"),
    ("due diligence", r"due diligence"),
    ("duty of care", r"duty of care"),
    ("economic equilibrium clauses", r"economic equilibrium"),
    ("energy justice", r"energy justice"),
    ("energy security", r"energy security"),
    ("energy solidarity", r"energy solidarity"),
    ("environmental impact assessment", [r"environmental impact assessment", r"\bEIA\b"]),
    ("equitable and reasonable utilisation", r"equitable and reasonable utili[sz]ation"),
    ("exhaustion of local remedies", r"local remedies"),
    ("expropriation, direct and indirect", r"expropriat"),
    ("extraterritoriality", r"extraterritorial"),
    ("fair and equitable treatment", [r"fair and equitable treatment", r"\bFET\b"]),
    ("force majeure", r"force majeure"),
    ("forum non conveniens", r"forum non conveniens"),
    ("free, prior and informed consent", [r"free, prior and informed consent", r"\bFPIC\b"]),
    ("frustration of contract", r"frustration"),
    ("full protection and security", r"full protection and security"),
    ("general principles of law", r"general principles of law"),
    ("good faith", r"good faith"),
    ("government take", r"government take"),
    ("hardship", r"\bhardship\b"),
    ("intergenerational equity", r"intergenerational equity"),
    ("judicial review", r"judicial review"),
    ("jus cogens", r"jus cogens"),
    ("just transition", r"just transition"),
    ("legitimate expectations", r"legitimate expectations"),
    ("lex mercatoria", r"lex (mercatoria|petrolea)"),
    ("liquidated damages", r"liquidated damages"),
    ("local content", r"local content"),
    ("managed decline", r"managed decline"),
    ("margin of appreciation", r"margin of appreciation"),
    ("most-favoured-nation treatment", [r"most-favoured-nation", r"\bMFN\b"]),
    ("national treatment", r"national treatment"),
    ("necessity, plea of", r"(state of necessity|plea of necessity)"),
    ("no-harm principle", [r"no-harm", r"no significant harm", r"prevention of (significant )?(transboundary )?harm"]),
    ("pacta sunt servanda", r"pacta sunt servanda"),
    ("parent company liability", r"parent company"),
    ("permanent sovereignty over natural resources", [r"permanent sovereignty", r"\bPSNR\b"]),
    ("polluter pays principle", r"polluter[- ]pays"),
    ("precautionary principle", r"precaution"),
    ("proportionality", r"proportionality"),
    ("public trust doctrine", r"public trust"),
    ("rebus sic stantibus", r"(rebus sic stantibus|fundamental change of circumstances)"),
    ("regulatory capture", r"regulatory capture"),
    ("regulatory independence", r"regulatory independence|independent regulator"),
    ("resource curse", r"resource curse"),
    ("right to a healthy environment", r"right to a (clean, )?(healthy|satisfactory|general satisfactory) environment"),
    ("right to regulate", r"right to regulate"),
    ("ring-fencing", r"ring-?fenc"),
    ("rule of law", r"rule of law"),
    ("sovereign immunity", r"(sovereign|state) immunity"),
    ("stabilisation clauses", r"stabili[sz]ation"),
    ("standing", r"\bstanding\b"),
    ("state responsibility", r"state responsibility"),
    ("strict liability", r"strict liability"),
    ("subsidiarity", r"subsidiarity"),
    ("sustainable development", r"sustainable development"),
    ("take-or-pay", r"take-or-pay"),
    ("third-party access", r"third-party access"),
    ("transit", r"\btransit\b"),
    ("treaty interpretation", r"treaty interpretation|articles? 31"),
    ("umbrella clauses", r"umbrella clause"),
    ("unbundling", r"unbundl"),
    ("unitisation", r"uniti[sz]ation"),
    ("vicarious liability", r"vicarious liability"),
])

INDEX_INSTITUTIONS = _terms([
    ("African Commission on Human and Peoples' Rights", r"African Commission"),
    ("African Court on Human and Peoples' Rights", r"African Court"),
    ("African Development Bank", r"African Development Bank|\bAfDB\b"),
    ("African Union", r"African Union|\bAU\b"),
    ("Court of Justice of the European Union", r"Court of Justice of the European Union|\bCJEU\b"),
    ("ECOWAS", r"\bECOWAS\b"),
    ("ECOWAS Court of Justice", r"ECOWAS Court"),
    ("Energy Charter Conference and Secretariat", r"Energy Charter (Conference|Secretariat)"),
    ("European Commission", r"European Commission"),
    ("European Court of Human Rights", r"European Court of Human Rights|\bECtHR\b"),
    ("Extractive Industries Transparency Initiative", r"\bEITI\b|Extractive Industries Transparency Initiative"),
    ("Federal Energy Regulatory Commission (US)", r"\bFERC\b|Federal Energy Regulatory Commission"),
    ("Financial Action Task Force", r"\bFATF\b|Financial Action Task Force"),
    ("Inter-American Court of Human Rights", r"Inter-American Court|\bIACtHR\b"),
    ("Intergovernmental Panel on Climate Change", r"\bIPCC\b|Intergovernmental Panel on Climate Change"),
    ("International Atomic Energy Agency", r"\bIAEA\b|International Atomic Energy Agency"),
    ("International Centre for Settlement of Investment Disputes", r"\bICSID\b"),
    ("International Chamber of Commerce", r"\bICC\b|International Chamber of Commerce"),
    ("International Court of Justice", r"International Court of Justice|\bICJ\b"),
    ("International Energy Agency", r"\bIEA\b|International Energy Agency"),
    ("International Energy Forum", r"International Energy Forum"),
    ("International Finance Corporation", r"\bIFC\b|International Finance Corporation"),
    ("International Labour Organization", r"\bILO\b|International Labour Organi[sz]ation"),
    ("International Law Commission", r"International Law Commission|\bILC\b"),
    ("International Maritime Organization", r"\bIMO\b|International Maritime Organi[sz]ation"),
    ("International Monetary Fund", r"\bIMF\b|International Monetary Fund"),
    ("International Renewable Energy Agency", r"\bIRENA\b"),
    ("International Seabed Authority", r"International Seabed Authority|\bISA\b"),
    ("International Sustainability Standards Board", r"\bISSB\b"),
    ("International Tribunal for the Law of the Sea", r"\bITLOS\b|International Tribunal for the Law of the Sea"),
    ("London Court of International Arbitration", r"\bLCIA\b"),
    ("Network for Greening the Financial System", r"\bNGFS\b"),
    ("Nigerian Electricity Regulatory Commission", r"\bNERC\b|Nigerian Electricity Regulatory Commission"),
    ("Nigerian Midstream and Downstream Petroleum Regulatory Authority", r"\bNMDPRA\b"),
    ("Nigerian National Petroleum Company Ltd", r"\bNNPC\b"),
    ("Nigerian Upstream Petroleum Regulatory Commission", r"\bNUPRC\b"),
    ("NEITI", r"\bNEITI\b"),
    ("OECD", r"\bOECD\b"),
    ("OPEC", r"\bOPEC\b"),
    ("Permanent Court of Arbitration", r"Permanent Court of Arbitration|\bPCA\b"),
    ("Southern African Power Pool", r"Southern African Power Pool|\bSAPP\b"),
    ("Transmission Company of Nigeria", r"Transmission Company of Nigeria|\bTCN\b"),
    ("UNCITRAL", r"\bUNCITRAL\b"),
    ("UNCTAD", r"\bUNCTAD\b"),
    ("UN Environment Programme", r"\bUNEP\b|United Nations Environment Programme|UN Environment Programme"),
    ("UN General Assembly", r"General Assembly"),
    ("UN Human Rights Council", r"Human Rights Council"),
    ("UN Security Council", r"Security Council"),
    ("West African Power Pool", r"West African Power Pool|\bWAPP\b"),
    ("World Bank", r"World Bank"),
    ("World Trade Organization", r"\bWTO\b|World Trade Organi[sz]ation"),
], flag="")

INDEX_SUBJECT = _terms([
    ("Africa", r"\bAfrica\b"),
    ("artificial intelligence", r"artificial intelligence|\bAI\b"),
    ("artisanal and small-scale mining", r"artisanal"),
    ("battery storage", r"battery storage|energy storage"),
    ("biomass", r"biomass"),
    ("carbon border adjustment", r"carbon border"),
    ("carbon capture and storage", r"carbon capture|\bCCS\b|\bCCUS\b"),
    ("carbon markets", r"carbon market|emissions trading"),
    ("climate litigation", r"climate litigation"),
    ("coal", r"\bcoal\b"),
    ("cobalt", r"cobalt"),
    ("community development agreements", r"community development agreement"),
    ("concessions", r"\bconcession"),
    ("copper", r"\bcopper\b"),
    ("critical minerals", r"critical minerals?"),
    ("cyber security", r"cyber ?security|cyber-security"),
    ("data centres", r"data cent(re|er)s"),
    ("deep seabed mining", r"(deep[- ]sea|seabed) mining"),
    ("electricity markets", r"electricity market"),
    ("energy access", r"energy access|access to (modern )?(electricity|energy)"),
    ("energy transition", r"energy transition"),
    ("feed-in tariffs", r"feed-in tariff"),
    ("gas flaring", r"flaring"),
    ("geothermal energy", r"geothermal"),
    ("greenwashing", r"greenwashing"),
    ("Host Communities Development Trusts", r"Host Communit(y|ies) Development Trust|\bHCDT"),
    ("human rights due diligence", r"human rights due diligence"),
    ("hydrogen", r"hydrogen"),
    ("hydropower", r"hydropower|hydroelectric"),
    ("indigenous peoples", r"indigenous peoples?"),
    ("investor–state dispute settlement", r"\bISDS\b|investor-state"),
    ("joint operating agreements", r"joint operating agreement"),
    ("lithium", r"lithium"),
    ("liquefied natural gas", r"\bLNG\b|liquefied natural gas"),
    ("methane emissions", r"methane"),
    ("mini-grids", r"mini-?grid"),
    ("national oil companies", r"national oil compan"),
    ("natural gas", r"natural gas"),
    ("Niger Delta", r"Niger Delta"),
    ("Nigeria", r"\bNigeria"),
    ("nuclear energy", r"nuclear"),
    ("offshore wind", r"offshore wind"),
    ("oil spills", r"oil spill"),
    ("pipelines", r"pipeline"),
    ("power purchase agreements", r"power purchase agreement|\bPPAs?\b"),
    ("production sharing contracts", r"production sharing contract|\bPSCs?\b"),
    ("project finance", r"project finance"),
    ("rare earth elements", r"rare earth"),
    ("refining", r"refiner"),
    ("renewable energy", r"renewable energy"),
    ("royalties", r"royalt"),
    ("sanctions", r"\bsanctions\b"),
    ("small modular reactors", r"small modular reactor|\bSMRs?\b"),
    ("smart grids", r"smart grid"),
    ("solar energy", r"\bsolar\b"),
    ("sovereign wealth funds", r"sovereign wealth fund"),
    ("stranded assets", r"stranded asset"),
    ("subsidies", r"subsid(y|ies)"),
    ("tailings", r"tailings"),
    ("taxation of extractive industries", r"resource rent tax|petroleum (profits|income) tax|hydrocarbon tax|windfall tax"),
    ("transboundary watercourses", r"transboundary (water|river)"),
    ("transparency", r"transparency"),
    ("uranium", r"uranium"),
    ("water resources", r"water resources"),
    ("wind energy", r"wind energy|wind farm"),
])
