#!/usr/bin/env bash
# Restore the whole production environment and rebuild lecture videos.
#
#   bash tools/bootstrap.sh                 # environment only
#   bash tools/bootstrap.sh w04             # environment + Week 4 video and tiers
#   bash tools/bootstrap.sh w04 w02 w03     # several weeks, in order
#
# A sandbox recreation resets the working tree to the base commit, wipes
# everything gitignored, and starts a fresh clone state. The narration audio is
# tracked in git and always survives; the static ffmpeg, the display fonts,
# rendered slides and MP4s do not. This script puts all of it back, so a
# recreation costs one command instead of a debugging session.
set -e
cd "$(dirname "$0")/.."
BRANCH=arena/27f30ef9-cac-masters

echo "==> 1. restore tracked work"
git fetch -q origin "$BRANCH"
git reset --hard "origin/$BRANCH" >/dev/null
echo "    HEAD $(git log --oneline -1)"

echo "==> 2. python deps"
pip3 install --quiet --break-system-packages \
  Pillow numpy python-pptx imageio-ffmpeg matplotlib fonttools brotli 2>&1 | tail -2

echo "==> 3. ffmpeg"
python3 - <<'PY'
import imageio_ffmpeg, os, shutil, subprocess
exe = imageio_ffmpeg.get_ffmpeg_exe()
os.makedirs("tools/bin", exist_ok=True)
shutil.copy2(exe, "tools/bin/ffmpeg")
os.chmod("tools/bin/ffmpeg", 0o755)
print("   ", subprocess.run(["tools/bin/ffmpeg","-version"],capture_output=True,
                           text=True).stdout.splitlines()[0])
PY

echo "==> 4. fonts"
python3 - <<'PY'
# matplotlib ships plenty of TTFs, which is enough for a fallback, but the
# design system is built on Roboto. setup_env.sh tries `npm pack roboto-fontface`
# and reports success while installing nothing, because that package now ships
# woff2 rather than TTF - so the slides then fail with "cannot open resource".
# Convert the woff2 to TTF instead, which fontTools does losslessly.
import os, glob, shutil, subprocess, tarfile, matplotlib
from fontTools.ttLib import TTFont

src = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
os.makedirs("assets/fonts", exist_ok=True)
for f in glob.glob(os.path.join(src, "*.ttf")):
    shutil.copy2(f, "assets/fonts")

weights = {
    "Roboto-Light.woff2": "Roboto-Light.ttf",
    "Roboto-Regular.woff2": "Roboto-Regular.ttf",
    "Roboto-RegularItalic.woff2": "Roboto-Italic.ttf",
    "Roboto-Medium.woff2": "Roboto-Medium.ttf",
    "Roboto-Bold.woff2": "Roboto-Bold.ttf",
    "Roboto-BoldItalic.woff2": "Roboto-BoldItalic.ttf",
}
need = [t for t in weights.values() if not os.path.exists(os.path.join("assets/fonts", t))]
if need:
    pkg = "/tmp/roboto/package/fonts/roboto"
    if not os.path.isdir(pkg):
        os.makedirs("/tmp/roboto", exist_ok=True)
        subprocess.run(["npm", "pack", "roboto-fontface", "--silent"],
                       cwd="/tmp/roboto", check=True, capture_output=True)
        tarfile.open(glob.glob("/tmp/roboto/*.tgz")[0]).extractall("/tmp/roboto")
    for woff, ttf in weights.items():
        if ttf in need:
            f = TTFont(os.path.join(pkg, woff)); f.flavor = None
            f.save(os.path.join("assets/fonts", ttf))
print(f"    {len(os.listdir('assets/fonts'))} fonts, roboto present:",
      all(os.path.exists(os.path.join("assets/fonts", t)) for t in weights.values()))
PY

if [ "$#" -eq 0 ]; then
  echo "==> done (environment only - pass week ids to rebuild videos)"
  exit 0
fi

echo "==> 5. rebuild videos: $*"
for w in "$@"; do
  slug="cpy-701-$w"
  echo "--- $slug: slides"
  python3 tools/build_lecture.py slides "content/cpy-701/week-${w#w}.json" | tail -2
  echo "--- $slug: merge audio"
  python3 tools/narrate.py merge "content/cpy-701/week-${w#w}.json" | tail -1
  echo "--- $slug: assemble"
  python3 tools/build_lecture.py assemble "content/cpy-701/week-${w#w}.json" \
    | grep -E '"duration_hms"|"tempo"|"output"'
  echo "--- $slug: tiers"
  tools/bin/ffmpeg -y -v error -i "media/$slug/$slug.mp4" -vf scale=960:540 \
    -c:v libx264 -crf 30 -preset medium -c:a aac -b:a 64k -ac 1 \
    -movflags +faststart "media/$slug/$slug-COMPACT.mp4"
  tools/bin/ffmpeg -y -v error -t 90 -i "media/$slug/$slug.mp4" -vf scale=960:540 \
    -c:v libx264 -crf 32 -preset medium -c:a aac -b:a 64k -ac 1 \
    -movflags +faststart "media/$slug/$slug-PREVIEW-90s.mp4"
  rm -rf "media/$slug/work"
  ls -la "media/$slug"/*.mp4 | awk '{printf "    %-52s %6.1f MB\n", $9, $5/1048576}'
done
echo "==> done"
