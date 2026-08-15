#!/usr/bin/env python
"""Dump every partition's J for k in 2..5 with float value + conservative rational recon,
flagging any non-reconstructable (float-noisy) entries. Independent of the sum logic.
"""
import sys, json
from fractions import Fraction as F
from collections import defaultdict
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T050000Z-m5exact-3f8a\reproducibility")
from boxspline_exact import shape_integral_exact
from enumerate_moments import partitions_of, blocksizes


def run(k):
    parts = partitions_of(k)
    rows = []
    noisy = []
    for blocks in parts:
        # recompute raw float total without reconstruction
        from boxspline2 import coarea_value
        from boxspline_exact import cycle_edges, rho_terms, perm_edges
        b = len(blocks)
        if b == 1:
            Jf = 1.0
        else:
            cyc = cycle_edges(blocks, k)
            tot = 0.0
            for sign, perm in rho_terms(b):
                vs = cyc + perm_edges(perm, b)
                tot += sign * coarea_value(vs)
            Jf = tot
        J = shape_integral_exact(list(blocks), k)  # rational
        rows.append({"blocks": sorted(sorted(x) for x in blocks), "b": b,
                     "sizes": blocksizes(blocks), "J": str(J),
                     "Jf_float": Jf, "Jf": float(J)})
        if abs(Jf - float(J)) > 1e-5:
            noisy.append((sorted(sorted(x) for x in blocks), b, Jf, float(J), abs(Jf - float(J))))
    return rows, noisy


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    for k in range(2, kmax + 1):
        rows, noisy = run(k)
        print(f"===== k={k} ({len(rows)} partitions), noisy entries: {len(noisy)} =====")
        if noisy:
            for bl, b, Jf, Jr, d in noisy:
                print(f"   NOISY {bl} b={b} float={Jf:+.8e} recon={Jr:+.8e} diff={d:.1e}")
        # per-profile sums (rational), and float check
        byprof = defaultdict(lambda: F(0))
        byprof_cnt = defaultdict(int)
        tot = F(0)
        for r in rows:
            prof = tuple(r["sizes"])
            byprof[prof] += F(r["J"])
            byprof_cnt[prof] += 1
            tot += F(r["J"])
        for prof in sorted(byprof, key=len):
            print(f"   profile {prof}: count={byprof_cnt[prof]} sum={byprof[prof]} = {float(byprof[prof]):+.8f}")
        print(f"   TOTAL m_{k} = {tot} = {float(tot):.10f}")
