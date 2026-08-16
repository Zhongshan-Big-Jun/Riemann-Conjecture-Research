#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
explore_b4.py — per-pi box-spline values for b=4 vanishing (m=4 cycle / m=5) and one
nonvanishing (m=6) partition, to test whether B_Gamma(0) is a cycle-length class function
in the vanishing (low-surplus) regime and how it breaks in the surplus regime.
Uses the float engine for individual B; prints grouped-by-cycle-type subtotals.
Run: py -3.10 explore_b4.py
"""
import os, sys, itertools
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxspline_exact import cycle_edges, rho_terms, perm_edges
from boxspline2 import coarea_value

def np_array(fl):
    return np.array([int(round(x)) for x in fl])

def moved(perm):
    return sum(1 for a in range(len(perm)) if perm[a] != a)

def cycle_type(perm):
    seen=[False]*len(perm); lens=[]
    for i in range(len(perm)):
        if not seen[i]:
            j=i; L=0
            while not seen[j]:
                seen[j]=True; j=perm[j]; L+=1
            lens.append(L)
    return tuple(sorted(lens, reverse=True))

def run(blocks, k):
    b=len(blocks)
    cyc=[np_array(e) for e in cycle_edges(list(blocks), k)]
    from collections import defaultdict
    bytype=defaultdict(lambda:[0,0.0,0.0])  # type -> [count, signed B sum, abs-sum]
    js=0.0
    vals=[]
    for sign,perm in rho_terms(b):
        pe=[np_array(e) for e in perm_edges(perm,b)]
        vs=cyc+pe
        B=coarea_value(vs)
        t=cycle_type(perm)
        bytype[t][0]+=1; bytype[t][1]+=sign*B; 
        js+=sign*B
        vals.append((sign,t,B,perm))
    print(f"  b={b}  J~{js:+.10f}  (nonzero>{1e-4}: {abs(js)>1e-4})")
    for t in sorted(bytype):
        cnt,sB,ab=bytype[t]
        print(f"     cyc-type {t}: count={cnt} signed-cum={sB:+.8f}")
    return js, vals

def main():
    targets = [
        # k, blocks, label
        (5, [frozenset([0,1]),frozenset([2]),frozenset([3]),frozenset([4])], "b=4 m=4 (cycle H) vanish"),
        (5, [frozenset([0,2]),frozenset([1]),frozenset([3]),frozenset([4])], "b=4 m=5 vanish"),
        (6, [frozenset([0,1,2]),frozenset([3]),frozenset([4]),frozenset([5])], "b=4 m=4 vanish"),
    ]
    for k,blocks,label in targets:
        print(f"\n== {label} ==")
        run(blocks, k)

if __name__=="__main__":
    main()
