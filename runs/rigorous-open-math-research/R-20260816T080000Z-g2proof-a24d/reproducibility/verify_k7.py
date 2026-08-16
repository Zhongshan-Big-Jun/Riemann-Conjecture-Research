#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify_k7.py — verify the G2 residual identity on NEW k=7 shapes not present in the
k<=6 dataset (which had 275 partitions / 18 H-isoclasses). Tests the surplus boundary:
   b=3,m=7 -> nonzero (m>=2b-2=4)
   b=4,m=7 -> nonzero (m>=2b-2=6)
   b=5,m=7 -> zero     (m<=2b-3=7)
   b=6,m=7 -> zero     (m<=2b-3=9)
   b=7,m=7 -> zero     (m<=2b-3=11)
Uses the exact box-spline engine (coarea_value_exact) + rational reconstruction, with
threshold 1e-7 for zero (true cancellations are exact; nonzero values are >= ~1/10000).
Run: py -3.10 verify_k7.py
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxspline_exact import cycle_edges, rho_terms, perm_edges
from boxspline_exact2 import coarea_value_exact
from fractions import Fraction as F

def np_array(fl): return np.array([int(round(x)) for x in fl])
def recon(v):
    if abs(v) < 1e-6: return F(0), True   # (value, is_zero)
    rc = F(v).limit_denominator(500000)
    return rc, (rc == 0)

TARGETS = [
    # k, blocks, expected-nonzero (T/F) per rule
    (3, [frozenset([0]), frozenset([1,3,5]), frozenset([2,4,6])], True,  "b=3 m=7 nonzero"),
    (4, [frozenset([0]), frozenset([1]), frozenset([2,4,6]), frozenset([3,5])], True, "b=4 m=7 nonzero"),
    (5, [frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3,5]), frozenset([4,6])], False, "b=5 m=7 zero"),
    (6, [frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4,6]), frozenset([5])], False, "b=6 m=7 zero"),
    (7, [frozenset([0]), frozenset([1]), frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5]), frozenset([6])], False, "b=7 m=7 zero"),
]

def run(blocks, k):
    b = len(blocks)
    if b == 1:
        return F(1), True
    cyc = [np_array(e) for e in cycle_edges(list(blocks), k)]
    tot = 0.0
    for sign, perm in rho_terms(b):
        pe = [np_array(e) for e in perm_edges(perm, b)]
        tot += sign * coarea_value_exact(cyc + pe)
    val, isz = recon(tot)
    return val, (not isz)

def main():
    for k, blocks, expect_nz, label in TARGETS:
        t0 = time.time()
        # only directly compute if k and b are feasible; b=7 has 5040 perms, may be slow
        try:
            val, nz = run(blocks, k)
            ok = (nz == expect_nz)
            print(f"[{label}] k={k} b={len(blocks)} J={val} nonzero={nz} expect_nz={expect_nz} -> {'PASS' if ok else 'FAIL'} ({time.time()-t0:.1f}s)")
        except Exception as e:
            print(f"[{label}] k={k} ERROR: {e}")

if __name__ == "__main__":
    main()
