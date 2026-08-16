#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
explore_focused.py — focused per-pi decomposition of J_sigma for a handful of target
partitions across the surplus boundary, using the fast float box-spline engine.
Each row: pi (as cycle notation summary), sign, l(pi), n_active=m+l, delta=n-(b-1), B.
Grouped by delta with signed subtotal, and total J.
Run: py -3.10 explore_focused.py
"""
import os, sys, itertools
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxspline_exact import cycle_edges, rho_terms, perm_edges
from boxspline2 import coarea_value
from dataset import crossing_count, profile

def np_array(fl):
    return np.array([int(round(x)) for x in fl])

def moved(perm):
    return sum(1 for a in range(len(perm)) if perm[a] != a)

def perm_cycles(perm):
    seen = [False]*len(perm); out=[]
    for i in range(len(perm)):
        if not seen[i]:
            j=i; cyc=[]
            while not seen[j]:
                seen[j]=True; cyc.append(j); j=perm[j]
            if len(cyc)>1: out.append(tuple(cyc))
    return out

def analyze(blocks, k):
    b = len(blocks)
    if b == 1:
        return None
    m = crossing_count(k, blocks)
    cyc = [np_array(e) for e in cycle_edges(list(blocks), k)]
    rows = []
    js = 0.0
    for sign, perm in rho_terms(b):
        pe = [np_array(e) for e in perm_edges(perm, b)]
        vs = cyc + pe
        nact = len(vs)
        delta = nact - (b - 1)
        bval = coarea_value(vs) if nact >= (b-1) else 0.0
        js += sign * bval
        rows.append((sign, moved(perm), nact, delta, bval, perm_cycles(perm)))
    g = {}
    for (sign, l, n, delta, B, pc) in rows:
        g.setdefault(delta, [0, 0.0])
        g[delta][0] += 1
        g[delta][1] += sign * B
    return m, js, rows, g

TARGETS = [
    # k, blocks (as explicit list of frozensets)
    (3, [frozenset([0,1,2])]),                       # b=1 base
    (3, [frozenset([0,1]), frozenset([2])]),         # b=2 m=2 (nonzero 1/3)
    (3, [frozenset([0]), frozenset([1]), frozenset([2])]),  # b=3 m=3 (D3=0)
    (4, [frozenset([0,1]), frozenset([2,3])]),       # b=2 m=4 nonzero
    (4, [frozenset([0,2]), frozenset([1,3])]),       # b=2 m=4 nonzero (crossing)
    (4, [frozenset([0,1,2]), frozenset([3])]),       # b=2 m=2 nonzero
    (4, [frozenset([0]), frozenset([1,2,3])]),       # b=2 m=2
    (4, [frozenset([0,1]), frozenset([2]), frozenset([3])]),  # b=3 m=? 
    (5, [frozenset([0,1]), frozenset([2,3,4])]),     # b=2 m=?
    (5, [frozenset([0,1]), frozenset([2]), frozenset([3,4])]), # b=3 m=?
    (6, [frozenset([0,1]), frozenset([2,3]), frozenset([4,5])]), # b=3 
    # b=3 m=4 nonvanishing (H = two doubled edges sharing a vertex)
    (5, [frozenset([0,1,3]), frozenset([2]), frozenset([4])]),
    # b=3 m=5 nonvanishing 1/180
    (6, [frozenset([0,1,3]), frozenset([2]), frozenset([4,5])]),
    # b=3 m=6 deg-seq variants nonvanishing
    (6, [frozenset([0,1,2]), frozenset([3,4]), frozenset([5])]),
    (6, [frozenset([0,1,2,3]), frozenset([4]), frozenset([5])]),
]

def main():
    for k, blocks in TARGETS:
        # ensure partition covers 0..k-1
        cover = set().union(*blocks)
        if cover != set(range(k)):
            continue
        a = analyze(blocks, k)
        if a is None:
            print(f"k={k} blocks={[sorted(b) for b in blocks]} -> b=1 base J=1"); continue
        m, js, rows, g = a
        b = len(blocks)
        print(f"\nk={k} prof={sorted((len(x) for x in blocks),reverse=True)} b={b} m={m} J~{js:+.10f}  (|J|>1e-4 => {abs(js)>1e-4})")
        for d in sorted(g):
            cnt, subtot = g[d]
            print(f"   delta={d}: n_terms={cnt} signed-subtotal={subtot:+.8f}")
        # show the individual nonzero-delta terms for the smallest partitions only
        if b <= 3:
            print("   per-pi (sign,l,n,delta,B,cycles):")
            for (sign, l, n, d, B, pc) in sorted(rows, key=lambda r:(r[3], r[1])):
                print(f"     sign={sign:+d} l={l} n={n} delta={d} B={B:+.8f} cyc={pc}")

if __name__ == "__main__":
    main()
