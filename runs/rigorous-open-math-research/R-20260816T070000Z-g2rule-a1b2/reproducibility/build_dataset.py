#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_dataset.py — canonical exact per-partition J_sigma dataset for k=3..6 + verification.

Exact values sourced from:
  * k=3,4,5: the box-spline exact engine dump (perJ_k*.json). For k=3,4 all values already
    lie in the audited value sets (m_3=2, m_4=13/4 reproduced). For k=5 the engine is reliable
    on b<=3; the four b>=3/4 residues ('noise', documented in the m5 run) are corrected from the
    audited m5 profile aggregates + the isoclass-determinism rule (confirmed at k=6:
    J depends only on the isoclass of the cycle-multigraph H_sigma).
  * k=6: exact per-partition values from the m6 run CSVs (b=3,4,5,6) + analytic b=1,2
    (J=1 ; J=c_m-c_{m+2}).

Outputs: allJ.json (canonical), and prints the m_2..m_6 anchors for verification.
"""
import os, sys, json
from fractions import Fraction as F
from itertools import permutations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dataset import load_m6, cycle_multigraph, crossing_count, C, partitions_of

KNOWN5 = {F(1), F(1,3), F(7,60), F(1,15), F(1,180), F(0)}

def canon(H, b):
    best = None
    for perm in permutations(range(b)):
        s = []
        for (u, v), c in sorted(H.items()):
            a, z = (perm[u], perm[v]) if perm[u] < perm[v] else (perm[v], perm[u])
            s.append(f"{a}{z}x{c}")
        k = "|".join(s)
        if best is None or k < best:
            best = k
    return best

def find_k6_iso_J(k6, H, b, m):
    cH = canon(H, b)
    for b6, J6 in k6.items():
        if len(b6) != b:
            continue
        if crossing_count(6, b6) != m:
            continue
        if canon(cycle_multigraph(6, b6), b) == cH:
            return J6
    return None

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    k6 = load_m6()

    # ---- k=3,4,5 from dump (correct k=5 spurious) ----
    D = {}
    for k in [3, 4, 5]:
        with open(os.path.join(base, f"perJ_k{k}.json"), encoding="utf-8") as f:
            for r in json.load(f):
                blocks = tuple(frozenset(b) for b in r["blocks"])
                J = F(r["J_num"], r["J_den"])
                key = (k, blocks)
                if J in KNOWN5:
                    D[key] = J
                else:
                    # spurious float residue -> correct via isoclass (k6) or certified D5
                    H = cycle_multigraph(k, blocks)
                    b = len(blocks); m = r["m_crossing"]
                    if (k, b, m) == (5, 5, 5):        # all-distinct D5 = 0 (certified, G1)
                        D[key] = F(0)
                    else:
                        Jc = find_k6_iso_J(k6, H, b, m)
                        if Jc is None:
                            raise RuntimeError(f"no k6 isoclass for k={k} blocks={blocks} "
                                               f"iso={canon(H,b)} spurious={J}")
                        D[key] = Jc
                        print(f"  corrected k={k} b={b} m={m} iso={canon(H,b)}: spurious {J} -> {Jc}")

    # ---- k=6 from k6 dict ----
    for blocks, J in k6.items():
        D[(6, blocks)] = J

    # ---- verify moments ----
    for k in [2, 3, 4, 5, 6]:
        tot = F(0)
        for blocks in partitions_of(k):
            b = len(blocks)
            if b == 1:
                J = F(1)
            elif k == 6 and b == 2:
                J = C[crossing_count(6, blocks)] - C[crossing_count(6, blocks) + 2]
            elif k == 2 and b == 2:
                J = C[crossing_count(2, blocks)] - C[crossing_count(2, blocks) + 2]
            else:
                J = D[(k, blocks)]
            tot += J
        print(f"m_{k} = {tot}  (float {float(tot):.12f})")

    # ---- write canonical json ----
    out = []
    for (k, blocks), J in sorted(D.items(), key=lambda kv: kv[0][0]):
        out.append({
            "k": k,
            "blocks": sorted(sorted(x) for x in blocks),
            "b": len(blocks),
            "m": crossing_count(k, blocks),
            "profile": tuple(sorted((len(x) for x in blocks), reverse=True)),
            "J_num": J.numerator, "J_den": J.denominator, "J": str(J),
            "H_edges": sorted(([int(u), int(v)], c) for (u, v), c in cycle_multigraph(k, blocks).items()),
        })
    with open(os.path.join(base, "allJ.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=0)
    print(f"wrote allJ.json: {len(out)} rows")

if __name__ == "__main__":
    main()
