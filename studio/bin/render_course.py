#!/usr/bin/env python3
"""Render one course video:  render_course.py <subject.json> [--silent]"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine import assemble

if __name__ == "__main__":
    path = sys.argv[1]
    silent = "--silent" in sys.argv
    assemble.render_course(path, silent=silent)
