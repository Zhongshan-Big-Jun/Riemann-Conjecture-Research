#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""abstract_k6.py — group k=6 partitions by the ISOMORPHISM class (vertex relabeling) of the
cycle-edge multigraph H_sigma, and print J per class. Since J depends only on the abstract
multigraph, all partitions in a class share the same J. This is the clean way to read the rule.
Run: py -3.10 abstract_k6.py"""
import os, sys
from fractions import Fraction as F
from itertools import permutations
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dataset import load_m6, cycle_multigraph, crossing_count, profile, C, c_2n

def canonical_form(H, b, m):
    """Canonical integer string for (weighted) multigraph H on b vertices up to relabeling."""
    best = None
    for perm in permutations(range(b)):
        s = []
        for (u, v), c in sorted(H.items()):
            su, sv = perm[u], perm[v]
            a, z = (su, sv) if su < sv else (sv, su)
            s.append(f"{a}{z}x{c}")
        key = "|".join(s)
        if best is None or key < best:
            best = key
    return best

def degree_seq(H, b):
    d = [0]*b
    for (u, v), c in H.items():
        d[u] += c; d[v] += c
    return tuple(sorted(d, reverse=True))

def main():
    k6 = load_m6()
    bycanon = defaultdict(list)
    for blocks, J in k6.items():
        H = cycle_multigraph(6, blocks)
        m = crossing_count(6, blocks)
        b = len(blocks)
        c = canonical_form(H, b, m)
        bycanon[(b, c)].append((J, profile(blocks), m, blocks, degree_seq(H,b)))
    print(f"# distinct (b, H-isoclass): {len(bycanon)}")
    print(f"\n=== Nonzero J values and their H-isomorphism classes (all b) ===")
    for (b, c) in sorted(bycanon):
        entries = bycanon[(b, c)]
        js = {e[0] for e in entries}
        bl = entries[0]
        n = len(entries)
        nz = sum(1 for e in entries if e[0] != F(0))
        only = js.pop() if len(js) == 1 else None
        ds = bl[4]
        print(f" b={b} m={bl[2]} degs={ds} H[{c}]  count={n} nonzero={nz} J={list(js)}{'' if only else ''}")
        for e in sorted(entries, key=lambda e: str(e[0])):
            if e[0] != F(0):
                print(f"      J={e[0]}  prof={e[1]}  blocks={sorted(sorted(x) for x in e[3])}")

if __name__ == "__main__":
    main()
