#import "/templates/book.typ": *
#pagebreak(to: "odd", weak: true)
#page(header: none, footer: none)[
  #opening-marker
  #v(2.4in)
  #align(center, block(width: 75%, {
    set par(justify: false, first-line-indent: 0pt, leading: 0.6em)
    text(font: sans, size: 8pt, weight: "semibold", tracking: 0.3em, fill: bronze)[DEDICATION]
    v(1.2em)
    text(size: 11.5pt, style: "italic", fill: teal)[To the scholars, regulators, negotiators, advocates, and arbitrators whose rigorous work turns the world’s energy and natural resources into lawful, accountable, and equitable development —]
    v(0.6em)
    text(size: 11.5pt, style: "italic", fill: teal)[and to the communities whose lands, waters, and futures that work must always serve.]
  }))
]
