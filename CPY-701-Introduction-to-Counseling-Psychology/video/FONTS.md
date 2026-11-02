# Slide typography

Two open-licence families (SIL Open Font License) are **vendored in this
folder** so the pipeline is reproducible in any sandbox:

- **Inter** — body, labels, captions (weights 400/500/600/700/800)
- **Poppins** — display, headings, numerals (weights 400/500/600/700)

`src/bootstrap.sh` copies `fonts/*.ttf` into `~/.fonts`, where the SVG
rasterizer's font loader discovers them (the render sandbox has no
fontconfig font directories of its own).

Provenance: converted from the npm webfont packages `@fontsource/inter` and
`@fontsource/poppins` (woff2 → ttf via `fontTools`), which mirror the upstream
releases of Inter (Rasmus Andersson) and Poppins (Indian Type Foundry).
To re-vendor:

```bash
npm install @fontsource/inter @fontsource/poppins
pip install fonttools brotli
python - <<'PY'
from fontTools.ttLib import TTFont
import os
for fam in ('inter', 'poppins'):
    for w in ('400', '500', '600', '700', '800'):
        src = f'node_modules/@fontsource/{fam}/files/{fam}-latin-{w}-normal.woff2'
        if os.path.exists(src):
            f = TTFont(src); f.flavor = None
            f.save(f'fonts/{fam.capitalize()}-{w}.ttf')
PY
```
