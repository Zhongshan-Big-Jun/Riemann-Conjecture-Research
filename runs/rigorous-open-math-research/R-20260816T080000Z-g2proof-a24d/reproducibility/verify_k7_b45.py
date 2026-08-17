#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""verify_k7_b45.py — exact-engine verification of the two most discriminating NEW k=7 shapes:
   b=4,m=7 (must be NONZERO, m>=2b-2=6) and b=5,m=7 (must be ZERO, m<=2b-3=7).
   Uses the exact box-spline engine + rational reconstruction. Run: py -3.10 verify_k7_b45.py"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxspline_exact import cycle_edges, rho_terms, perm_edges
from boxspline_exact2 import coarea_value_exact
from fractions import Fraction as F

def np_array(fl): return np.array([int(round(x)) for x in fl])
def recon(v):
    if abs(v) < 1e-6: return F(0)
    return F(v).limit_denominator(500000)

def run(blocks, k):
    b = len(blocks)
    cyc = [np_array(e) for e in cycle_edges(list(blocks), k)]
    tot = 0.0
    for sign, perm in rho_terms(b):
        pe = [np_array(e) for e in perm_edges(perm, b)]
        tot += sign * coarea_value_exact(cyc + pe)
    return recon(tot)

def main():
    TARGETS = [
        (4, [frozenset([0]), frozenset([1]), frozenset([2,4,6]), frozenset([3,5])], True,  "b=4 m=7 (expect NONZERO)"),
        (5, [frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3,5]), frozenset([4,6])], False, "b=5 m=7 (expect ZERO)"),
    ]
    for b, blocks, expect_nz, label in TARGETS:
        t0 = time.time()
        val = run(blocks, 7)
        nz = (val != 0)
        ok = (nz == expect_nz)
        print(f"[{label}] b={b} J={val} nonzero={nz} expect_nz={expect_nz} -> {'PASS' if ok else 'FAIL'} ({time.time()-t0:.1f}s)", flush=True)

if __name__ == "__main__":
    main()
