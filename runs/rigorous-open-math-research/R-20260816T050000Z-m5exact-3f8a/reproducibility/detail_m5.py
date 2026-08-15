#!/usr/bin/env python
"""Dump per-partition J_sigma for k=5 with float residue, to identify which block-size profiles
contribute and isolate the small (cancellation) residues b=4, b=5.
"""
import sys, itertools, json
from fractions import Fraction as F
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T050000Z-m5exact-3f8a\reproducibility")
from boxspline_exact import shape_integral_exact
from enumerate_moments import partitions_of, blocksizes


def run(k):
    allparts = partitions_of(k)
    rows = []
    for blocks in allparts:
        J = shape_integral_exact(list(blocks), k)
        sz = blocksizes(blocks)
        b = len(blocks)
        rows.append({"blocks": sorted(sorted(x) for x in blocks), "b": b, "sizes": sz,
                     "J": str(J), "Jf": float(J)})
    # group by size profile
    from collections import defaultdict
    byprof = defaultdict(list)
    for r in rows:
        byprof[tuple(r["sizes"])].append(r)
    tot = F(0)
    print("=== per size-profile totals for k=%d ===" % k)
    for prof, rs in sorted(byprof.items(), key=lambda kv: len(kv[0])):
        s = F("0") if False else sum(F(r["J"]) for r in rs)
        tot += s
        print(f"profile {prof}: count={len(rs)}  sum={s} = {float(s):+.8f}")
    print(f"total m_k = {tot} = {float(tot):.10f}")
    # print the nonzero-by-float but reconstructed-small ones
    print("\n=== partitions with |J| < 0.05 ===")
    for r in rows:
        if abs(r["Jf"]) < 0.05:
            print(f"  {r['blocks']} b={r['b']} sizes={r['sizes']} J={r['J']} = {r['Jf']:+.8e}")
    return rows


if __name__ == "__main__":
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
