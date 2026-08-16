#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""survey_k6.py — print the cycle-multigraph H_sigma, profile, crossing count and exact J
for every k=6 partition, grouped by (profile,b), so the vanishing pattern can be read off.
Run: py -3.10 survey_k6.py"""
import os, sys
from fractions import Fraction as F
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dataset import load_m6, cycle_multigraph, crossing_count, profile, partitions_of

def sig(H, b):
    return "".join(f"({u},{v})x{c}" for (u, v), c in sorted(H.items()))

def main():
    k6 = load_m6()
    g = defaultdict(list)
    for blocks, J in k6.items():
        H = cycle_multigraph(6, blocks)
        m = crossing_count(6, blocks)
        b = len(blocks)
        g[(profile(blocks), b)].append((blocks, H, m, J))
    for key in sorted(g, key=lambda x: (-x[1], x[0])):
        prof, b = key
        rows = g[key]
        nz = sum(1 for _, _, _, J in rows if J != F(0))
        print(f"\n===== profile {prof}  b={b}  ({len(rows)} partitions, {nz} nonzero) =====")
        vals = defaultdict(int)
        for blocks, H, m, J in sorted(rows, key=lambda r: (r[2], r[1].keys().__len__(), str(sorted(r[0])))):
            if J != F(0):
                vals[str(J)] += 1
                print(f"   J={J}  m={m}  H={sig(H,b)}  blocks={sorted(sorted(x) for x in blocks)}")
        print(f"   nonzero value mult: {dict(vals)}")

if __name__ == "__main__":
    main()
