#!/usr/bin/env python
"""compute_k8_partial.py — exact b<=2 (closed-form) contribution to m_8.

Full m_8 needs b=3,4,5 box-spline signed sums; those are out of budget in this pass with
the available engines (b=4 ~6+ min/isoclass, b=5 relies on S_5=120 perms + high null dim).
This script certifies the b<=2 part EXACTLY: b=1 -> J=1, b=2 -> J = c_m - c_{m+2},
m = #cycle crossings, m even in {2,4,6,8}. Result is a rigorous LOWER (b<=2) partial m_8.
Run: py -3.10 compute_k8_partial.py
"""
import os, sys, json
from fractions import Fraction as F
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dataset import partitions_of, crossing_count
from compute_k7_exact import cval

K = 8

def main():
    parts = partitions_of(K)
    assert len(parts) == 4140
    byb = defaultdict(list)
    for p in parts:
        byb[len(p)].append(p)
    b1 = F(1)
    b2_total = F(0)
    bym = defaultdict(lambda: [0, F(0)])
    for p in byb[2]:
        m = crossing_count(K, p)
        J = cval(m) - cval(m + 2)
        bym[m][0] += 1
        bym[m][1] += J
        b2_total += J
    m8_b2 = b1 + b2_total
    out = {
        "k": K, "method": "closed_form_b<=2",
        "b1": str(b1), "b2_total": str(b2_total),
        "m_8_b_le_2": str(m8_b2),
        "m_8_b_le_2_num": m8_b2.numerator, "m_8_b_le_2_den": m8_b2.denominator,
        "b2_by_m": {str(m): {"count": bym[m][0], "J_per": str(cval(m) - cval(m + 2)),
                             "sum": str(bym[m][1])} for m in sorted(bym)},
        "note": "full m_8 needs b=3,4,5 (open in this pass); b<=2 part is exact.",
    }
    print("k=8 b<=2 exact partial m_8:")
    print("  b=1 :", b1)
    for m in sorted(bym):
        print(f"  b=2 m={m}: n={bym[m][0]} J_per={cval(m)-cval(m+2)} sum={bym[m][1]}")
    print("  b<=2 total m_8^(b<=2) =", m8_b2, "=", float(m8_b2))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "k8_partial.json"),
              "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("wrote k8_partial.json")

if __name__ == "__main__":
    main()
