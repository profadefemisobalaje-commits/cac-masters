// ===========================================================================
//  BECOMING A DOCTOR OF INTERNATIONAL ENERGY AND NATURAL RESOURCES LAW
//  Book design template — 6 x 9 in academic trim
//  Typeset with Typst. Body: EB Garamond. Display: Source Sans 3.
// ===========================================================================

#let teal = rgb("#0F4C5C")
#let teal-light = rgb("#E3EEF0")
#let bronze = rgb("#9C6B30")
#let bronze-light = rgb("#F4EADB")
#let ivory = rgb("#FBF8F1")
#let ink = rgb("#1B1B1B")
#let grey = rgb("#5E6468")

#let serif = ("EB Garamond", "Libertinus Serif")
#let sans = ("Source Sans 3", "DejaVu Sans")

#let book-title = "Becoming a Doctor of International Energy and Natural Resources Law"
#let book-title-upper = "BECOMING A DOCTOR OF INTERNATIONAL ENERGY AND NATURAL RESOURCES LAW"
#let book-author = "TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA"
#let running-verso = "International Energy and Natural Resources Law"

// --------------------------------------------------------------------------
// State used for running heads and chapter-relative numbering
// --------------------------------------------------------------------------
#let chap-num = state("chap-num", "0")
#let matter = state("matter", "front")

#let opening-pages() = {
  // pages on which a part, chapter, front/back heading begins: no running head
  query(<opening>).map(m => m.location().page())
}

#let page-header = context {
  let p = here().page()
  if p in opening-pages() { return }
  if matter.get() == "cover" { return }
  let heads = query(selector(<runhead>).before(here()))
  let right-text = if heads.len() > 0 { heads.last().value } else { "" }
  set text(font: sans, size: 7.6pt, fill: grey, tracking: 0.04em)
  if calc.even(p) {
    grid(columns: (auto, 1fr), column-gutter: 10pt,
      text(fill: teal, weight: "semibold")[#counter(page).display()],
      align(left, upper(running-verso)))
  } else {
    grid(columns: (1fr, auto), column-gutter: 10pt,
      align(right, upper(right-text)),
      text(fill: teal, weight: "semibold")[#counter(page).display()])
  }
  v(-4pt)
  line(length: 100%, stroke: 0.4pt + bronze)
}

#let page-footer = context {
  let p = here().page()
  if matter.get() == "cover" { return }
  if p in opening-pages() {
    align(center, text(font: sans, size: 8pt, fill: grey)[#counter(page).display()])
  }
}

// --------------------------------------------------------------------------
// Global document set-up
// --------------------------------------------------------------------------
#let setup(body) = {
  set document(title: book-title, author: book-author,
    keywords: ("energy law", "natural resources law", "international law", "doctoral studies"))
  set page(
    width: 6in, height: 9in,
    margin: (inside: 0.85in, outside: 0.68in, top: 0.86in, bottom: 0.8in),
    binding: left,
    header: page-header, header-ascent: 38%,
    footer: page-footer, footer-descent: 40%,
  )
  set text(font: serif, size: 10.6pt, fill: ink, lang: "en", region: "gb",
    hyphenate: true, number-type: "old-style")
  set par(justify: true, leading: 0.6em, first-line-indent: (amount: 1.15em, all: false),
    spacing: 0.62em)
  show heading: set text(font: sans, fill: ink, hyphenate: false)
  show heading: set par(justify: false)

  // Section (md ##) -> level 3
  show heading.where(level: 3): it => {
    v(1.25em, weak: true)
    block(sticky: true, below: 0.75em, {
      set text(size: 12.2pt, weight: "semibold", fill: teal)
      it.body
    })
  }
  // Sub-section (md ###) -> level 4
  show heading.where(level: 4): it => {
    v(1.0em, weak: true)
    block(sticky: true, below: 0.6em, {
      set text(size: 10.6pt, weight: "bold", fill: ink)
      it.body
    })
  }
  // Sub-sub-section (md ####) -> level 5
  show heading.where(level: 5): it => {
    v(0.8em, weak: true)
    block(sticky: true, below: 0.5em, {
      set text(font: serif, size: 10.6pt, weight: "regular", style: "italic", fill: bronze)
      it.body
    })
  }

  // Footnotes
  set footnote.entry(separator: line(length: 28%, stroke: 0.4pt + bronze), gap: 0.45em, indent: 0.8em)
  show footnote.entry: set text(size: 8.3pt)
  show footnote.entry: set par(leading: 0.5em, first-line-indent: 0pt)

  // Quotations
  show quote.where(block: true): it => {
    pad(left: 1.4em, right: 1.0em, top: 0.2em, bottom: 0.2em,
      text(size: 9.8pt, it.body))
  }

  // Lists
  set list(indent: 0.6em, body-indent: 0.55em, marker: (text(fill: bronze)[▪], text(fill: teal)[–]))
  set enum(indent: 0.6em, body-indent: 0.55em)

  // Tables
  set table(stroke: none, inset: (x: 5pt, y: 4.2pt),
    fill: (_, y) => if y == 0 { teal } else if calc.even(y) { teal-light } else { white })
  show table.cell: set text(font: sans, size: 8.2pt, number-type: "lining")
  show table.cell: set par(justify: false, leading: 0.48em, first-line-indent: 0pt)
  show table.cell.where(y: 0): set text(fill: white, weight: "semibold")
  show table: it => block(stroke: (top: 0.8pt + teal, bottom: 0.8pt + teal), it)

  // Figures & captions — chapter-relative numbering
  set figure(numbering: (..n) => context [#chap-num.get().#n.pos().first()], gap: 0.7em)
  set figure.caption(separator: [ #h(0.3em)])
  show figure.caption: it => {
    set text(font: sans, size: 8.2pt, fill: grey)
    set par(justify: false, leading: 0.5em, first-line-indent: 0pt)
    block(width: 100%, inset: (x: 4pt), [
      #text(fill: teal, weight: "bold")[#it.supplement #context it.counter.display(it.numbering)] #h(0.4em) #it.body
    ])
  }
  show figure.where(kind: table): set figure.caption(position: top)
  show figure: set block(above: 1.3em, below: 1.3em)
  show figure.where(kind: image): set block(breakable: false)
  show figure.where(kind: table): set block(breakable: true)
  show figure.where(kind: table): set figure(placement: none)

  show link: set text(fill: teal)
  body
}

// --------------------------------------------------------------------------
// Structural components
// --------------------------------------------------------------------------
#let opening-marker = [#metadata("open") <opening>]

#let front-heading(title, outlined: true, runhead: none) = {
  pagebreak(to: "odd", weak: true)
  opening-marker
  [#metadata(if runhead == none { title } else { runhead }) <runhead>]
  v(0.9in)
  block(width: 100%, {
    set par(justify: false, first-line-indent: 0pt)
    line(length: 2.2em, stroke: 2pt + bronze)
    v(0.35em)
    show heading: set text(font: sans, size: 19pt, weight: "semibold", fill: teal)
    heading(level: 1, supplement: [front], outlined: outlined, title)
  })
  v(1.6em)
}

#let roman(n) = numbering("I", n)

#let part-page(num: "I", title: [], img: none, summary: []) = {
  pagebreak(to: "odd", weak: true)
  opening-marker
  [#metadata("Part " + num) <runhead>]
  page(header: none, footer: none, margin: 0pt, fill: ivory, {
    if img != none {
      block(width: 100%, height: 52%, clip: true, image(img, width: 100%, height: 100%, fit: "cover"))
    } else {
      block(width: 100%, height: 52%, fill: teal)
    }
    block(width: 100%, height: 0.12in, fill: bronze)
    pad(x: 0.75in, top: 0.42in, {
      set par(justify: false, first-line-indent: 0pt)
      text(font: sans, size: 10pt, weight: "semibold", tracking: 0.32em, fill: bronze)[PART #num]
      v(0.2em)
      show heading: set text(font: sans, size: 21pt, weight: "semibold", fill: teal)
      heading(level: 1, supplement: [#num], outlined: true, title)
      v(0.7em)
      line(length: 3em, stroke: 1.2pt + bronze)
      v(0.6em)
      text(font: serif, size: 10.2pt, style: "italic", fill: grey, summary)
    })
  })
}

#let chapter-open(num: "1", title: [], short: none) = {
  pagebreak(to: "odd", weak: true)
  matter.update("main")
  chap-num.update(num)
  counter(footnote).update(0)
  counter(figure.where(kind: image)).update(0)
  counter(figure.where(kind: table)).update(0)
  opening-marker
  [#metadata("Chapter " + num + " · " + (if short == none { "" } else { short })) <runhead>]
  v(0.55in)
  block(width: 100%, {
    set par(justify: false, first-line-indent: 0pt)
    grid(columns: (auto, 1fr), column-gutter: 14pt, align: (left + bottom, left + bottom),
      text(font: sans, size: 52pt, weight: "light", fill: bronze, number-type: "lining", num),
      block(inset: (bottom: 8pt), text(font: sans, size: 9pt, weight: "semibold", tracking: 0.36em, fill: grey)[CHAPTER]))
    v(0.1em)
    line(length: 100%, stroke: 0.9pt + teal)
    v(0.55em)
    show heading: set text(font: sans, size: 18.5pt, weight: "semibold", fill: teal)
    heading(level: 2, supplement: [#num], outlined: true, title)
  })
  v(1.3em)
}

#let appendix-open(letter: "A", title: []) = {
  pagebreak(to: "odd", weak: true)
  matter.update("back")
  chap-num.update(letter)
  counter(footnote).update(0)
  counter(figure.where(kind: image)).update(0)
  counter(figure.where(kind: table)).update(0)
  opening-marker
  [#metadata("Appendix " + letter) <runhead>]
  v(0.55in)
  block(width: 100%, {
    set par(justify: false, first-line-indent: 0pt)
    text(font: sans, size: 9pt, weight: "semibold", tracking: 0.36em, fill: bronze)[APPENDIX #letter]
    v(0.2em)
    line(length: 100%, stroke: 0.9pt + teal)
    v(0.45em)
    show heading: set text(font: sans, size: 17pt, weight: "semibold", fill: teal)
    heading(level: 2, supplement: [#letter], outlined: true, title)
  })
  v(1.2em)
}

// --------------------------------------------------------------------------
// Callout boxes
// --------------------------------------------------------------------------
#let callout-styles = (
  objectives: (label: "Learning Objectives", fill: teal-light, accent: teal),
  casebox: (label: "Leading Authority", fill: bronze-light, accent: bronze),
  keypoint: (label: "Key Doctrinal Point", fill: teal-light, accent: teal),
  comparative: (label: "Comparative Perspective", fill: ivory, accent: bronze),
  exercise: (label: "Practical Exercise — Hypothetical Scenario", fill: ivory, accent: teal),
  research: (label: "Doctoral Research Questions", fill: teal-light, accent: teal),
  summary: (label: "Chapter Summary", fill: bronze-light, accent: bronze),
  reading: (label: "Further Reading", fill: ivory, accent: grey),
  instrument: (label: "Primary Instrument", fill: ivory, accent: bronze),
  practice: (label: "Practice Note", fill: ivory, accent: teal),
  illustration: (label: "Illustration Placement Note", fill: ivory, accent: grey),
)

#let callout(kind: "keypoint", title: none, body) = {
  let s = callout-styles.at(kind, default: callout-styles.keypoint)
  let label = if title == none { s.label } else { title }
  block(width: 100%, breakable: true, above: 1.1em, below: 1.1em,
    fill: s.fill, stroke: (left: 2.6pt + s.accent), inset: (left: 11pt, right: 10pt, top: 8pt, bottom: 9pt),
    radius: (right: 2pt), {
      set par(first-line-indent: 0pt, spacing: 0.55em)
      set text(size: 9.6pt)
      block(sticky: true, below: 0.55em,
        text(font: sans, size: 7.8pt, weight: "bold", tracking: 0.14em, fill: s.accent, upper(label)))
      body
    })
}

// --------------------------------------------------------------------------
// Table of contents
// --------------------------------------------------------------------------
#let dots = box(width: 1fr, inset: (x: 3pt), repeat(gap: 2.2pt, text(fill: rgb("#9a9a9a"), size: 7pt)[.]))

#let book-toc() = {
  front-heading("Contents", outlined: false)
  show outline.entry: it => {
    let el = it.element
    let pg = it.page()
    set par(first-line-indent: 0pt, justify: false)
    set text(hyphenate: false)
    if it.level == 1 {
      if el.supplement != [front] {
        v(1.0em, weak: true)
        block(sticky: true, link(el.location(), text(font: sans, size: 9.4pt, weight: "bold", fill: teal)[
          #upper[Part #el.supplement]#h(0.6em)#el.body #h(1fr) #pg]))
      } else {
        v(0.55em, weak: true)
        link(el.location(), text(font: sans, size: 9pt, weight: "semibold")[#el.body #dots #pg])
      }
    } else if it.level == 2 {
      v(0.55em, weak: true)
      link(el.location(), grid(columns: (2.6em, 1fr, auto), column-gutter: 0pt,
        text(font: sans, size: 9pt, weight: "bold", fill: bronze)[#el.supplement],
        text(font: sans, size: 9pt, weight: "semibold")[#el.body #dots],
        text(font: sans, size: 9pt, weight: "semibold")[#pg]))
    } else {
      v(0.18em, weak: true)
      link(el.location(), pad(left: 2.6em, grid(columns: (1fr, auto),
        text(size: 8.8pt)[#el.body #dots], text(size: 8.8pt)[#pg])))
    }
  }
  outline(title: none, depth: 3, indent: 0pt)
}

#let lof-mode = state("lof-mode", false)
#let figsrc(body) = context if lof-mode.get() { none } else { body }

#let list-of(kind, title) = {
  front-heading(title)
  show outline.entry: it => {
    set par(first-line-indent: 0pt, justify: false)
    let el = it.element
    v(0.3em, weak: true)
    link(el.location(), grid(columns: (3.4em, 1fr, auto),
      text(font: sans, size: 8.4pt, weight: "bold", fill: teal, hyphenate: false)[#chap-num.at(el.location()).#counter(figure.where(kind: kind)).at(el.location()).first()],
      text(size: 9pt)[#el.caption.body #dots], text(size: 9pt)[#it.page()]))
  }
  lof-mode.update(true)
  outline(title: none, target: figure.where(kind: kind))
  lof-mode.update(false)
}
