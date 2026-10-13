#!/usr/bin/env python3
"""Batch-render every subject's 720p lecture video (voice where clips exist)."""
import os, sys, json, glob, traceback
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
sys.path.insert(0, ROOT)
from engine import assemble as AS

def main():
    files = sorted(glob.glob(os.path.join(ROOT, "data", "subjects", "*.json")))
    for f in files:
        try:
            AS.render_course(f)
        except Exception as e:
            print("FAILED", f, e); traceback.print_exc()
    print("ALL VIDEOS DONE")
    os.system(f"{sys.executable} {os.path.join(ROOT, 'bin', 'make_gallery.py')}")

if __name__ == "__main__":
    main()
