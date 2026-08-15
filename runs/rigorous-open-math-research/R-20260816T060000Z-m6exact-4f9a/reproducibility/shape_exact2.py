#!/usr/bin/env python
"""Shape integral J_sigma computed with the EXACT-volume box-spline engine
(boxspline_exact2.coarea_value_exact). This is the AUDIT-grade driver for the
k=6 (and cross-check k=5) shape decomposition, immune to the float hull noise
that afflicted the float coarea engine on large-b cancellation terms.

J_sigma = int_R^(b-1) [prod cycle K] * rho_b ; b=#blocks, last block pinned (translation).
rho_b = det[K(x_a - x_b)] = sum_{perm in S_b} sign(perm) prod_a K(x_a - x_perm(a)).
Each integrand is a product of sincs = a box-spline value at 0 (K^ = window).  We sum the
sign-weighted box-spline values; the individual values come from exact rational vertices.
"""
import os, sys, itertools
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxspline_exact import cycle_edges, rho_terms, perm_edges
from boxspline_exact2 import coarea_value_exact


def shape_integral_exact2(blocks, k, maxcomb=4000000):
    """Returns float J_sigma computed via the exact engine (values ~1e-12 accurate)."""
    b = len(blocks)
    if b == 1:
        return 1.0
    cyc = cycle_edges(blocks, k)
    total = 0.0
    for sign, perm in rho_terms(b):
        pe = perm_edges(perm, b)
        vs = [np_array(e) for e in (cyc + pe)]
        total += sign * coarea_value_exact(vs, maxcomb=maxcomb)
    return total


def np_array(fl):
    import numpy as np
    return np.array([int(round(x)) for x in fl])


def reconstruct(val, threshold=1e-6, maxden=200000):
    """Reconstruct exact Fraction from the exact-engine float; treat values below threshold
    as exactly 0 (genuine nonzero shape integrals for k<=6 are >= ~1e-3 apart from zeros;
    cancellation shapes return ~1e-11 residues)."""
    if abs(val) < threshold:
        return F(0)
    fr = F(val)
    rc = fr.limit_denominator(maxden)
    err = abs(float(rc) - val)
    if err > max(1e-7 * max(1.0, abs(val)), 1e-9):
        # try with larger denominator, else leave as fraction (caller decides)
        raise ValueError(f"no clean rational for val={val:.12f} (rc={rc}, err={err:.1e})")
    return rc


if __name__ == "__main__":
    from enumerate_moments import partitions_of, blocksizes
    from collections import defaultdict
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    for k in range(2, kmax + 1):
        parts = partitions_of(k)
        byprof = defaultdict(lambda: F(0))
        byprof_cnt = defaultdict(int)
        tot = F(0)
        small = []
        for blocks in parts:
            val = shape_integral_exact2(list(blocks), k)
            if abs(float(val)) < 0.05:
                small.append((sorted(sorted(x) for x in blocks), len(blocks), float(val)))
            J = reconstruct(val)
            prof = tuple(blocksizes(blocks))
            byprof[prof] += J
            byprof_cnt[prof] += 1
            tot += J
        print(f"===== k={k}: Bell={len(parts)} partitions =====")
        for prof in sorted(byprof, key=len):
            print(f"  profile {prof}: cnt={byprof_cnt[prof]} sum={byprof[prof]} = {float(byprof[prof]):+.9f}")
        print(f"  TOTAL m_{k} = {tot} = {float(tot):.12f}")
        print(f"  small-residue partitions ({len(small)}):")
        for bl, b, v in small:
            print(f"     b={b} {bl} J={v:+.3e}")
    want = {2: F(4, 3), 3: F(2), 4: F(13, 4), 5: F(101, 18)}
    print("\nanchors (recompute to confirm exact engine):")
    for k in want:
        parts = partitions_of(k)
        tot = F(0)
        for blocks in parts:
            tot += reconstruct(shape_integral_exact2(list(blocks), k))
        print(f"  k={k}: {tot}  expect {want[k]}  -> {'PASS' if tot == want[k] else 'FAIL'}")
