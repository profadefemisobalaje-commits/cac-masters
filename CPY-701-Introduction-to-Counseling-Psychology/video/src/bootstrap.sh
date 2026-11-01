#!/usr/bin/env bash
# CPY 701 video studio bootstrap: restores every ephemeral dependency.
# Safe to re-run each session (node_modules, venvs and ~/.fonts do not persist).
set -e
cd "$(dirname "$0")/.."

echo "== node deps (slide rasterizer)"
[ -d node_modules/@resvg/resvg-js ] || npm install --silent --no-audit --no-fund

echo "== python venv (ffmpeg + pptx)"
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  .venv/bin/pip install --quiet imageio-ffmpeg python-pptx
fi

echo "== fonts (vendored TTFs -> ~/.fonts for the rasterizer's font loader)"
mkdir -p "$HOME/.fonts"
cp -f fonts/*.ttf "$HOME/.fonts/" 2>/dev/null || true

echo "== ready"
.venv/bin/python -c "import imageio_ffmpeg as f; print('ffmpeg:', f.get_ffmpeg_exe())"
