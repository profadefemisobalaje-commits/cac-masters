#import "/templates/book.typ": *
#pagebreak(to: "odd", weak: true)
#page(header: none, footer: none)[
  #opening-marker
  #v(2.4in)
  #align(center, block(width: 75%, {
    set par(justify: false, first-line-indent: 0pt, leading: 0.6em)
    text(font: sans, size: 8pt, weight: "semibold", tracking: 0.3em, fill: bronze)[DEDICATION]
    v(1.2em)
    text(size: 11.5pt, style: "italic", fill: teal)[To the researchers who test what practitioners believe, and to the practitioners who test what researchers propose —]
    v(0.6em)
    text(size: 11.5pt, style: "italic", fill: teal)[and to the families whose difficulties have taught this discipline almost everything it knows.]
  }))
]
