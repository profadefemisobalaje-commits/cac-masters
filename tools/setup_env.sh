#!/usr/bin/env bash
# Rebuild the production environment. Safe to re-run at the start of any session.
set -e
cd "$(dirname "$0")/.."

echo "==> Python deps (PyPI)"
pip3 install --quiet --break-system-packages \
  Pillow numpy python-pptx imageio-ffmpeg 2>&1 | tail -3

echo "==> ffmpeg"
python3 - <<'PY'
import imageio_ffmpeg, os, shutil, subprocess
exe = imageio_ffmpeg.get_ffmpeg_exe()
os.makedirs("tools/bin", exist_ok=True)
shutil.copy2(exe, "tools/bin/ffmpeg")
os.chmod("tools/bin/ffmpeg", 0o755)
print(subprocess.run(["tools/bin/ffmpeg","-version"],capture_output=True,text=True).stdout.splitlines()[0])
PY
ln -sf ffmpeg tools/bin/ffprobe 2>/dev/null || true

echo "==> Fonts"
python3 - <<'PY'
import matplotlib, os, glob, shutil
src = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
os.makedirs("assets/fonts", exist_ok=True)
n = 0
for f in glob.glob(os.path.join(src, "*.ttf")):
    shutil.copy2(f, "assets/fonts/"); n += 1
print(f"installed {n} TTF fonts from matplotlib")
PY

echo "==> Optional: nicer display fonts via npm"
( npm pack roboto-fontface --silent >/dev/null 2>&1 && \
  tar xzf roboto-fontface-*.tgz -C /tmp && \
  find /tmp/package -name "*.ttf" -exec cp {} assets/fonts/ \; && \
  rm -f roboto-fontface-*.tgz && echo "roboto TTF installed" ) || echo "npm font fetch skipped - DejaVu will be used"

echo "==> Done"
ls assets/fonts | head -20
