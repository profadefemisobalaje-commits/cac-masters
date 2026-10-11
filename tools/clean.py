#!/usr/bin/env python3
"""Housekeeping: report and reclaim disk used by the lecture build.

    python3 tools/clean.py            # report only
    python3 tools/clean.py --work     # delete per-segment intermediates
    python3 tools/clean.py --work --all   # also delete superseded videos

Keeps: slides/, audio/ (source voice), *.pptx, *.txt, *.vtt, *.json
"""
from __future__ import annotations
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.course import ROOT, MEDIA

OUT = MEDIA
WORKDIRS = ("work", "work_preview", "work_interim")
SUPERSEDED = ("PREVIEW-", "INTERIM-")


def size(path: str) -> int:
    if os.path.isfile(path):
        return os.path.getsize(path)
    return sum(os.path.getsize(os.path.join(r, f))
               for r, _, fs in os.walk(path) for f in fs)


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def main():
    rm_work = "--work" in sys.argv
    rm_all = "--all" in sys.argv
    freed = 0
    print(f"{'path':<52} {'size':>9}")
    print("-" * 63)
    for entry in sorted(os.listdir(OUT)):
        base = os.path.join(OUT, entry)
        if not os.path.isdir(base):
            continue
        for sub in sorted(os.listdir(base)):
            p = os.path.join(base, sub)
            tag = ""
            if sub in WORKDIRS:
                tag = "[intermediate]" if not rm_work else "[DELETING]"
            elif any(sub.startswith(s) for s in SUPERSEDED):
                tag = "[superseded]" if not (rm_work and rm_all) else "[DELETING]"
            if tag:
                print(f"{os.path.relpath(p, ROOT):<52} {human(size(p)):>9}  {tag}")
                if "DELETING" in tag:
                    freed += size(p)
                    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        print(f"{entry + '/':<52} {human(size(base)):>9}  total")
    if rm_work:
        print(f"\nreclaimed {human(freed)}")
    else:
        print("\nrun again with --work to delete intermediates "
              "(add --all to also drop superseded previews)")


if __name__ == "__main__":
    main()
