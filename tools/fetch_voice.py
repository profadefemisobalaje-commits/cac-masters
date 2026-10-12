"""fetch_voice.py — download the Piper voice used for narration.

    python tools/fetch_voice.py

The model is ~63 MB and comes from the `joe-us-piper-voice` wheel on PyPI,
which bundles the ONNX weights for en_US-joe-medium. Nothing else on the
network is reachable from the build sandbox.

Courtesy: Triune Biblical University Global Extension, USA.
"""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "voices", "piper", "joe_us_piper_voice", "data")

WHEEL = ("https://files.pythonhosted.org/packages/b9/10/"
         "b44c7e1ac5d8f3c28473ad9b06e2740a772370a8287909d10c8eb5de4143/"
         "joe_us_piper_voice-1.0.0-py3-none-any.whl")

WANT = ("en_US-joe-medium.onnx", "en_US-joe-medium.onnx.json")
EXPECTED = {"en_US-joe-medium.onnx": 63201294}


def main() -> None:
    os.makedirs(DEST, exist_ok=True)
    have = all(os.path.exists(os.path.join(DEST, n)) for n in WANT)
    if have:
        print(f"voice already present in {DEST}")
        return

    print(f"downloading {WHEEL}")
    tmp = os.path.join(tempfile.gettempdir(), "joe_us_piper_voice.whl")
    with urllib.request.urlopen(WHEEL, timeout=600) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f)

    with zipfile.ZipFile(tmp) as z:
        for n in z.namelist():
            base = os.path.basename(n)
            if base in WANT:
                with z.open(n) as s, open(os.path.join(DEST, base), "wb") as d:
                    shutil.copyfileobj(s, d)
                size = os.path.getsize(os.path.join(DEST, base))
                print(f"  -> {base}  {size:,} bytes")
    os.remove(tmp)

    for name, size in EXPECTED.items():
        got = os.path.getsize(os.path.join(DEST, name))
        if got != size:
            sys.exit(f"size mismatch for {name}: {got} != {size}")
    print("voice ready")


if __name__ == "__main__":
    main()
