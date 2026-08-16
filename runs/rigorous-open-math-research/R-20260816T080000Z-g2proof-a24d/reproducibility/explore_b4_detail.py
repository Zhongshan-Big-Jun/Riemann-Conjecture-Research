#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Detail: individual per-pi B values for b=4 m=4 (H=4-cycle) vanishing case.
Tests whether B is a cycle-length class function / multiplicative. Run: py -3.10 explore_b4_detail.py"""
import os, sys, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxspline_exact import cycle_edges, rho_terms, perm_edges
from boxspline2 import coarea_value

def np_array(fl): return np.array([int(round(x)) for x in fl])
def cyc(perm):
    seen=[False]*len(perm); out=[]
    for i in range(len(perm)):
        if not seen[i]:
            j=i; L=0
            while not seen[j]:
                seen[j]=True; j=perm[j]; L+=1
            out.append(L)
    return tuple(sorted(out, reverse=True))

blocks=[frozenset([0,1]),frozenset([2]),frozenset([3]),frozenset([4])]
k=5
cyc_edges=[np_array(e) for e in cycle_edges(list(blocks),k)]
rows=[]
for sign,perm in rho_terms(4):
    pe=[np_array(e) for e in perm_edges(perm,4)]
    B=coarea_value(cyc_edges+pe)
    rows.append((cyc(perm), sign, B, perm))
# group and show all
from collections import defaultdict
g=defaultdict(list)
for t,s,B,p in rows: g[t].append((s,B,p))
for t in sorted(g):
    print(f"cyc-type {t}: n={len(g[t])}")
    for s,B,p in sorted(g[t]):
        print(f"    sign={s:+d} B={B:+.6f} perm={p}")

print("\nIDs adjacent-preserving vs non-adjacent transpositions (H=4-cycle 0-1,1-2,2-3,3-0):")
for s,B,p in sorted(g[(2,1,1)]):
    print(f"   B={B:+.6f} swap={p}")
