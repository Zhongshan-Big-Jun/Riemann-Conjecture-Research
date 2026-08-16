#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
dump_partitions.py — for k=3,4,5 compute the EXACT per-partition J_sigma using the
audited exact box-spline engine (enumerate_moments.shape_integral_exact) and dump a
per-partition JSON that also records the cycle-edge multigraph H_sigma (canonical
edges with multiplicities) so the vanishing rule can be tested graph-theoretically.

Usage: py -3.10 dump_partitions.py  OR  dump_partitions.py <kmax>
Output: perJ_k<k>.json  (k = 3,4,5)
"""
import os, sys, json, time
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enumerate_moments import partitions_of
from boxspline_exact import shape_integral_exact
from dataset import cycle_multigraph, crossing_count, profile, block_of

def canon(blocks):
    return [sorted(b) for b in blocks]

def main(kmax=5):
    for k in range(3, kmax + 1):
        parts = partitions_of(k)
        rows = []
        for blocks in parts:
            J = shape_integral_exact(list(blocks), k)
            Jf = F(J)  # exact engine returns Fraction
            H = cycle_multigraph(k, blocks)
            m = crossing_count(k, blocks)
            rows.append({
                "k": k,
                "blocks": canon(blocks),
                "profile": profile(blocks),
                "b": len(blocks),
                "m_crossing": m,
                "H_edges": sorted(([int(u), int(v)], c) for (u, v), c in H.items()),
                "J_num": Jf.numerator,
                "J_den": Jf.denominator,
                "J_str": str(Jf),
                "nonzero": Jf != 0,
            })
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"perJ_k{k}.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
        tot = F(0)
        for r in rows:
            tot += F(r["J_num"], r["J_den"])
        nz = sum(1 for r in rows if r["nonzero"])
        print(f"k={k}: Bell={len(rows)}, nonzero={nz}, m_k={tot} ({float(tot):.10f})")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
