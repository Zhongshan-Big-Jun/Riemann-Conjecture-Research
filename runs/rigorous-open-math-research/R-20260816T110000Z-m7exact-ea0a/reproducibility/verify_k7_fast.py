#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify_k7_fast.py — verify the G2 residual identity on NEW k=7 shapes (not in k<=6 275-row set).
Uses the EXACT engine for b=3,4,5 (discriminating: boundary m=2b-2 / m=2b-3) and the FLOAT
engine + rational reconstruction for b=6,7 (low-surplus vanishing; individual values cheap).
Run: py -3.10 verify_k7_fast.py
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxspline_exact import cycle_edges, rho_terms, perm_edges
from boxspline_exact2 import coarea_value_exact
from boxspline2 import coarea_value
from fractions import Fraction as F

def np_array(fl): return np.array([int(round(x)) for x in fl])
def recon(v, exact):
    th = 1e-6 if exact else 1e-4
    if abs(v) < th: return F(0)
    rc = F(v).limit_denominator(500000)
    return rc

def run(blocks, k, use_exact):
    b = len(blocks)
    if b == 1: return F(1)
    cyc = [np_array(e) for e in cycle_edges(list(blocks), k)]
    eng = coarea_value_exact if use_exact else coarea_value
    tot = 0.0
    for sign, perm in rho_terms(b):
        pe = [np_array(e) for e in perm_edges(perm, b)]
        tot += sign * eng(cyc + pe)
    return recon(tot, use_exact)

TARGETS = [
    # (k, blocks, expect_nonzero, label, use_exact)
    (3, [frozenset([0]), frozenset([1,3,5]), frozenset([2,4,6])], True,  "b=3 m=7 nonzero", True),
    (4, [frozenset([0]), frozenset([1]), frozenset([2,4,6]), frozenset([3,5])], True, "b=4 m=7 nonzero", True),
    (5, [frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3,5]), frozenset([4,6])], False, "b=5 m=7 zero", True),
    (6, [frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4,6]), frozenset([5])], False, "b=6 m=7 zero", False),
    (7, [frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5]), frozenset([6])], False, "b=7 m=7 zero", False),
]

def main():
    for k, blocks, expect_nz, label, exact in TARGETS:
        t0 = time.time()
        val = run(blocks, k, exact)
        nz = (val != 0)
        ok = (nz == expect_nz)
        print(f"[{label}] k={k} b={len(blocks)} exact={exact} J={val} nonzero={nz} expect_nz={expect_nz} -> {'PASS' if ok else 'FAIL'} ({time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
