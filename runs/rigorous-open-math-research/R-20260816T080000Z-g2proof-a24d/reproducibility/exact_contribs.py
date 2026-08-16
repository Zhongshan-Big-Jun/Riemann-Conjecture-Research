#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
exact_contribs.py — exact (rational-reconstructed) per-pi box-spline values for select
partitions, using the SLOW exact engine (coarea_value_exact). Small b only.
Run: py -3.10 exact_contribs.py
"""
import os, sys, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxspline_exact import cycle_edges, rho_terms, perm_edges
from boxspline_exact2 import coarea_value_exact
from fractions import Fraction as F

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
def recon(v):
    if abs(v)<1e-7: return F(0)
    rc=F(v).limit_denominator(200000)
    if abs(float(rc)-v) > 1e-6: return F("approx_%s"%v)
    return rc

def run(blocks,k):
    b=len(blocks)
    cyc_edges=[np_array(e) for e in cycle_edges(list(blocks),k)]
    from collections import defaultdict
    g=defaultdict(list)
    js=0.0
    for sign,perm in rho_terms(b):
        pe=[np_array(e) for e in perm_edges(perm,b)]
        B=coarea_value_exact(cyc_edges+pe)
        js+=sign*B
        g[cyc(perm)].append((sign,recon(B),perm))
    print(f"  b={b} J~{js:+.10f} recon-sum-total:")
    for t in sorted(g):
        line=", ".join(f"{'+' if s>0 else '-'}{str(v)}" for s,v,p in g[t])
        print(f"    cyc {t}: {line}")

TARGETS=[
    (3,[frozenset([0]),frozenset([1]),frozenset([2])]),
    (4,[frozenset([0,2]),frozenset([1]),frozenset([3])]),
    (5,[frozenset([0,1]),frozenset([2]),frozenset([3]),frozenset([4])]),
]
for k,blocks in TARGETS:
    print(f"\n== k={k} blocks={[sorted(x) for x in blocks]} ==")
    run(blocks,k)
