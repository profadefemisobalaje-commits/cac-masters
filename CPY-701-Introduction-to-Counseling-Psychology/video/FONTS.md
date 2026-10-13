# Slide typography

The renderer uses two open-license families (SIL Open Font License):

- **Inter** — body, labels, captions (weights 400/500/600/700/800)
- **Poppins** — display, headings, numerals (weights 400/500/600/700)

The sandbox has no fontconfig font directories, so the TTFs are installed to
`~/.fonts` and discovered directly by the rasterizer's font loader.

## One-time setup

```bash
# 1. fetch the webfont packages (woff2) from npm
npm install @fontsource/inter @fontsource/poppins

# 2. decompress woff2 -> ttf into ~/.fonts (needs fonttools + brotli)
pip install fonttools brotli
python - <<'PY'
from fontTools.ttLib import TTFont
import os
out = os.path.expanduser('~/.fonts'); os.makedirs(out, exist_ok=True)
for fam in ('inter', 'poppins'):
    for w in ('400', '500', '600', '700', '800'):
        src = f'node_modules/@fontsource/{fam}/files/{fam}-latin-{w}-normal.woff2'
        if os.path.exists(src):
            f = TTFont(src); f.flavor = None
            f.save(os.path.join(out, f'{fam.capitalize()}-{w}.ttf'))
print('fonts installed')
PY
```

Sources: `@fontsource/inter`, `@fontsource/poppins` (npm registry), which
mirror the upstream releases of Inter (Rasmus Andersson) and Poppins
(Indian Type Foundry).
