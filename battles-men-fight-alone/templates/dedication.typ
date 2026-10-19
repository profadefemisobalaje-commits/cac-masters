#import "/templates/book.typ": *
#pagebreak(to: "odd", weak: true)
#page(header: none, footer: none)[
  #opening-marker
  #v(2.2in)
  #align(center, block(width: 78%, {
    set par(justify: false, first-line-indent: 0pt, leading: 0.6em)
    text(font: sans, size: 8pt, weight: "semibold", tracking: 0.3em, fill: bronze)[DEDICATION]
    v(1.4em)
    text(size: 12pt, style: "italic", fill: teal)[To every man who has carried a weight he could not describe to anyone — and who kept going anyway.]
    v(0.9em)
    text(size: 12pt, style: "italic", fill: teal)[And to the families, friends, and professionals who learn to notice the quiet ones.]
  }))
]
