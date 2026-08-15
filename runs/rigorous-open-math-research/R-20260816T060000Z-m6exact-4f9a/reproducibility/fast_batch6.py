#!/usr/bin/env python
"""FAST batched shape-integrals for k=6 b>=4 using the fast exact-engine (numpy vertex enum) driver
boxspline_exact_fast.eq_coarea_value_exact_fast, which matches the sympy exact engine to ~1e-13 on
b=2/3 and runs ~3 orders of magnitude faster. Intended to enumerate b=4,5,6 (81 partitions).
Writes CSV rows per partition (J_float + rational recon)."""
import sys, os, time, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
import numpy as np
from enumerate_moments import partitions_of
from boxspline_exact import cycle_edges, rho_terms, perm_edges
from boxspline_exact_fast import eq_coarea_value_exact_fast as FAST

def np_arr(fl):
    return np.array([int(round(x)) for x in fl])

def shape_fast(blocks, k):
    b = len(blocks)
    if b == 1:
        return 1.0
    cyc = cycle_edges(blocks, k)
    t = 0.0
    for sign, perm in rho_terms(b):
        vs = [np_arr(e) for e in (cyc + perm_edges(perm, b))]
        t += sign * FAST(vs)
    return t

def recon(val, zero_abs=1e-6, maxden=10**7):
    if abs(val) < zero_abs:
        return F(0), "zero"
    fr = F(float(val)).limit_denominator(maxden)
    err = abs(float(fr) - val)
    if err > 1e-4 * max(1.0, abs(val)):
        return None, f"noise({val:+.2e})"
    return fr, "ok"

def main():
    start, end, b, outcsv, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 6
    if os.path.exists(outcsv):
        os.remove(outcsv)
    parts = [list(bl) for bl in partitions_of(k) if len(bl) == b]
    sel = parts[start:end]
    with open(outcsv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["idx","blocks","b","sizes","J_float","J_recon","tag","wall_s"])
        for i, bl in enumerate(sel):
            t0 = time.time()
            v = shape_fast(bl, k)
            fr, tag = recon(v)
            wall = time.time() - t0
            w.writerow([start + i, repr(sorted(sorted(x) for x in bl)), b,
                        repr(sorted(len(x) for x in bl)), repr(v), str(fr), tag, round(wall, 2)])
            f.flush()
            print(f"[{start+i}] b={b} blocks={[sorted(sorted(x) for x in bl)]} J={v:+.7f} recon={fr} tag={tag} wall={wall:.1f}s", flush=True)
    print(f"DONE fast batch [{start},{end}) b={b}: {len(sel)} partitions", flush=True)

main()
