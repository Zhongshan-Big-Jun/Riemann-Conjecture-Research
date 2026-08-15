"""T1 re-audit: comment-aware sorry/admit/axiom scan of repaired Chain9.lean."""
import re, sys

FILES = [
    r"F:\LaTeX\Riemann Conjecture\lean-proof\Record9\Record9\Chain9.lean",
]

def scan(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    lines = src.split("\n")
    # Strip block comments and line comments, tracking original line numbers.
    stripped = []   # (line_idx, text_after_comment_strip)
    in_block = False
    for ln, raw in enumerate(lines):
        t = raw
        if in_block:
            # we are inside a block comment; find closing -/
            idx = t.find("-/")
            if idx == -1:
                continue  # whole line commented-out
            t = t[idx+2:]
            in_block = False
        # strip line comments (--) that occur outside strings (approx; Lean files only use -- for comments)
        # and nested block comments
        while True:
            bc = t.find("/-")
            lc = t.find("--")
            if lc != -1 and (bc == -1 or lc < bc):
                t = t[:lc]
                break
            if bc != -1:
                cls = t.find("-/", bc+2)
                if cls == -1:
                    # open block to end of line
                    t = t[:bc]
                    in_block = True
                    break
                t = t[:bc] + t[cls+2:]
                continue
            break
        stripped.append((ln+1, t))
    hits = []
    for ln, t in stripped:
        for m in re.finditer(r"\b(sorry|admit|axiom)\b", t):
            hits.append((ln, m.group(1), t.strip()))
    return hits

for f in FILES:
    hits = scan(f)
    print(f"\n=== scan: {f} ===")
    if not hits:
        print("  NO sorry/admit/axiom declaration hits.")
    else:
        for ln, kw, line in hits:
            print(f"  line {ln}: {kw} :: {line}")
