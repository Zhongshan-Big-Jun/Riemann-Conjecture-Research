#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
explore_signed_sum.py — for a target partition sigma, expand J_sigma = sum_{pi in S_b}
sign(pi) * B_Gamma(0) over the box-spline engine and report per-pi data:
sign, #moved l(pi), active edges n = m + l, surplus delta = n - (b-1), B value.
This exposes the cancellation structure behind M2 (low-surplus telescoping).
Run: py -3.10 explore_signed_sum.py
Edits: PICK_TARGET below selects which (k, blocks) to study.
"""
import os, sys, itertools
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxspline_exact import cycle_edges, rho_terms, perm_edges, rel_weights
from boxspline_exact2 import coarea_value_exact
from enumerate_moments import partitions_of
from dataset import cycle_multigraph, crossing_count

def np_array(fl):
    return np.array([int(round(x)) for x in fl])

PICK_TARGET = [3, 4, 5, 6]  # list of k to dump all partitions' decomposition summaries

def moved(perm):
    return sum(1 for a in range(len(perm)) if perm[a] != a)

def analyze(blocks, k):
    b = len(blocks)
    if b == 1:
        return None
    m = crossing_count(k, blocks)
    cyc = cycle_edges(list(blocks), k)
    rows = []
    js = 0.0
    for sign, perm in rho_terms(b):
        pe = perm_edges(perm, b)
        vs = cyc + pe
        nact = len(vs)
        delta = nact - (b - 1)
        bval = coarea_value_exact([np_array(e) for e in vs])
        js += sign * bval
        rows.append(dict(l=moved(perm), n=nact, delta=delta, sign=sign, B=bval))
    # group by delta
    from collections import defaultdict
    g = defaultdict(lambda: [0, 0.0])
    for r in rows:
        g[r['delta']][0] += 1
        g[r['delta']][1] += r['sign'] * r['B']
    return dict(b=b, m=m, rows=rows, groups=dict(g), J=js)

def canon_blocks(blocks):
    return tuple(tuple(sorted(b2)) for b2 in blocks)

def main():
    for k in PICK_TARGET:
        parts = partitions_of(k)
        print(f"\n########## k={k} (Bell={len(parts)}) ##########")
        shown = 0
        for blocks in parts:
            a = analyze(blocks, k)
            if a is None:
                continue
            b, m = a['b'], a['m']
            # only show a sample: all b<=3, plus one of each (b,m) for b>=4
            key = (b, m)
            if b <= 3 or (shown < 30):
                groups = a['groups']
                gstr = "  ".join(f"d{d}:n{cnt}/sum={val:+.6f}" for d,(cnt,val) in sorted(groups.items()))
                # rational-ish J
                print(f"  prof={sorted((len(x) for x in blocks),reverse=True)} b={b} m={m} J~{a['J']:+.8f} | {gstr}")
                shown += 1
        parts_dup = 0

if __name__ == "__main__":
    main()
