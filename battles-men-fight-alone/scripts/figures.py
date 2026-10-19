#!/usr/bin/env python3
"""Render every registered figure for Battles Men Fight Alone.

Figure definitions live in figs_partN.py (one module per Part).  Each module
exposes FIGS: a dict {figure-name: callable}.  Run:

    ~/.venv/bin/python scripts/figures.py                 # all parts present
    ~/.venv/bin/python scripts/figures.py fig-01-01 ...   # selected figures
"""
import importlib
import sys
import traceback
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK / "scripts"))


def load():
    figs = {}
    for i in range(1, 25):
        try:
            m = importlib.import_module(f"figs_part{i}")
        except ModuleNotFoundError:
            continue
        except Exception:
            print(f"!! figs_part{i} failed to import")
            traceback.print_exc()
            continue
        figs.update(getattr(m, "FIGS", {}))
    return figs


def main():
    figs = load()
    wanted = [a for a in sys.argv[1:] if not a.startswith("-")]
    names = wanted or sorted(figs)
    done, failed = 0, []
    for name in names:
        fn = figs.get(name)
        if fn is None:
            print(f"?? no definition for {name}")
            continue
        try:
            fn()
            done += 1
        except Exception:
            failed.append(name)
            print(f"!! {name} failed")
            traceback.print_exc()
    print(f"rendered {done}/{len(names)} figures" + (f"; FAILED: {', '.join(failed)}" if failed else ""))


if __name__ == "__main__":
    main()
