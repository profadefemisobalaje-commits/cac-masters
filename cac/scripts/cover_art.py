"""Series cover art for the CAC Masters Series.

Drawn per edition in the house palette; no stock or generated imagery.
Each artwork keeps the upper third and the lower tenth of the 6 x 9 page
calm: the template places its typographic blocks there.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

IVORY = "#FBF8F1"
TEAL = "#0F4C5C"
TEAL_MID = "#5E8894"
BRONZE = "#9C6B30"
GREY = "#5E6468"

CAC = Path(__file__).resolve().parents[2] / "cac"


def _canvas():
    fig = plt.figure(figsize=(6, 9), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor(IVORY)
    return fig, ax


def _bezier(p0, p1, p2, n=140):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2


def art_confluence(path: Path):
    """Volume 1: four lineages converging on one child."""
    fig, ax = _canvas()
    P = np.array([0.70, 0.40])
    starts = [np.array([0.06, 0.62]), np.array([0.10, 0.50]),
              np.array([0.10, 0.30]), np.array([0.06, 0.18])]
    ctrls = [np.array([0.42, 0.66]), np.array([0.40, 0.52]),
             np.array([0.40, 0.28]), np.array([0.42, 0.14])]
    cols = [TEAL, BRONZE, TEAL_MID, GREY]
    for s, c, col in zip(starts, ctrls, cols):
        pts = _bezier(s, c, P)
        ax.plot(pts[:, 0], pts[:, 1], color=col, lw=1.5, solid_capstyle="round",
                zorder=3)
    for r, a in ((0.10, 0.55), (0.16, 0.35), (0.23, 0.20)):
        ax.add_patch(plt.Circle(P, r, fill=False, edgecolor=BRONZE, lw=0.7,
                                alpha=a, zorder=2))
    ax.add_patch(plt.Circle(P, 0.016, facecolor=TEAL, edgecolor="none", zorder=4))
    ax.add_patch(plt.Circle(P, 0.030, fill=False, edgecolor=BRONZE, lw=1.0, zorder=4))
    fig.savefig(path, facecolor=IVORY)
    plt.close(fig)
    print(f"  cover art -> {path.name}")


def art_rings(path: Path):
    """Volume 2 and default: growth rings, development as accumulation."""
    fig, ax = _canvas()
    C = np.array([0.66, 0.40])
    radii = [0.035, 0.07, 0.105, 0.145, 0.19, 0.24, 0.295]
    cols = [TEAL, BRONZE, TEAL_MID, GREY, TEAL, BRONZE, TEAL_MID]
    alphas = [0.95, 0.85, 0.75, 0.6, 0.5, 0.4, 0.3]
    for r, c, a in zip(radii, cols, alphas):
        ax.add_patch(plt.Circle(C, r, fill=False, edgecolor=c, lw=1.3, alpha=a,
                                zorder=2))
    ax.add_patch(plt.Circle(C, 0.014, facecolor=BRONZE, edgecolor="none", zorder=4))
    # a single open arc: the ring not yet closed, the child still growing
    th = np.linspace(np.pi * 0.15, np.pi * 1.35, 120)
    r = 0.345
    ax.plot(C[0] + r * np.cos(th), C[1] + r * np.sin(th), color=TEAL, lw=1.5,
            alpha=0.85, solid_capstyle="round", zorder=3)
    fig.savefig(path, facecolor=IVORY)
    plt.close(fig)
    print(f"  cover art -> {path.name}")


MOTIFS = {"cac701": art_confluence}


def main(slug: str):
    out = CAC / "books" / slug / "cover"
    out.mkdir(parents=True, exist_ok=True)
    MOTIFS.get(slug, art_rings)(out / "cover-art.png")


if __name__ == "__main__":
    for s in sys.argv[1:] or ["cac701"]:
        main(s)
    print("Done")
