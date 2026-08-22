#!/usr/bin/env python3
"""Antigravity Environment Preflight Diagnostic for math-research-workflow."""
import os, sys, pathlib

# Defer to top-level doctor.py if available or run directly
top_doc = pathlib.Path(__file__).resolve().parents[3] / "scripts" / "doctor.py"
if top_doc.is_file():
    exec(top_doc.read_text(encoding="utf-8"), globals())
else:
    print("Preflight: math-research-workflow plugin is active in Antigravity.")