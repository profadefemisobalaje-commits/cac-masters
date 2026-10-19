"""Generate the two full-bleed backgrounds used across the collection.

Both are deliberately quiet: a warm paper with a soft edge-vignette, and a
midnight ground with a bronze glow.  They are JPEGs so that reusing the same
image on every slide adds a single small part to each PPTX package.
"""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageFilter

from . import theme

SIZE = (1800, 1013)   # 2x the 900x506 pt area at 2 dpi-per-pt; plenty for print


def _vignette(w, h, strength=0.10, power=2.4):
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w / 2, h / 2
    r = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2) / np.sqrt(2)
    return 1.0 - strength * (r ** power)


def _blur_noise(w, h, scale=2.0, amount=1.6, seed=7):
    rng = np.random.default_rng(seed)
    small = rng.normal(0, amount, (max(2, h // 8), max(2, w // 8)))
    rng_span = float(np.ptp(small)) + 1e-9
    img = Image.fromarray(((small - small.min()) / rng_span * 255).astype(np.uint8))
    img = img.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale * 2.4))
    a = np.asarray(img, dtype=np.float32)
    return (a - a.mean()) / (a.std() + 1e-6)


def _compose(base_hex, glow_hex, glow_strength, vig_strength, out, grain):
    w, h = SIZE
    base = np.array(theme.hex_rgb(base_hex), dtype=np.float32)
    glow = np.array(theme.hex_rgb(glow_hex), dtype=np.float32)

    yy, xx = np.mgrid[0:h, 0:w]
    # elliptical glow centred high and to the right
    d = np.sqrt(((xx - w * 0.78) / (w * 0.62)) ** 2 + ((yy - h * 0.18) / (h * 0.55)) ** 2)
    g = np.clip(1.0 - d, 0, 1)[..., None] ** 1.7 * glow_strength
    img = base[None, None, :] * (1 - g) + glow[None, None, :] * g

    v = _vignette(w, h, vig_strength)[..., None]
    img = img * v

    n = _blur_noise(w, h, amount=grain * 255)[..., None]
    img = img + n * grain

    img = np.clip(img, 0, 255).astype(np.uint8)
    Image.fromarray(img).save(out, quality=94, subsampling=0, optimize=True)


def main():
    theme.ASSETS.mkdir(parents=True, exist_ok=True)
    _compose(theme.PAPER, "#FFFDF6", 0.55, 0.065,
             theme.ASSETS / "paper.jpg", grain=0.42)
    _compose(theme.DARK, "#3A2A16", 0.30, 0.22,
             theme.ASSETS / "dark.jpg", grain=0.42)
    print("textures ->", theme.ASSETS)


if __name__ == "__main__":
    main()
