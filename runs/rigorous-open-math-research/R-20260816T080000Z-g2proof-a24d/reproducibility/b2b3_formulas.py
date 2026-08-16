#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""b2b3_formulas.py — search for c-combination / box-spline-difference formulas for the
b=2 and b=3 J values against the exact dataset. Records the found formulas (observation,
not proof) for the Lemma P statement."""
import os, sys, json
from fractions import Fraction as F
from math import comb, factorial
from itertools import product
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def c_2n(n):
    m = 2*n; s = 0
    for k in range(n):
        s += (-1)**k * comb(m, k) * (n-k)**(m-1)
    return F(s, factorial(m-1))

C = {2: c_2n(1), 4: c_2n(2), 6: c_2n(3), 8: c_2n(4), 10: c_2n(5), 12: c_2n(6)}

def load():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "allJ.json"), encoding="utf-8") as f:
        raw = json.load(f)
    out = []
    for r in raw:
        H = {(int(u), int(v)): c for (u, v), c in r["H_edges"]}
        out.append({"k": r["k"], "b": r["b"], "m": r["m"], "profile": tuple(r["profile"]),
                    "H": H, "J": F(r["J_num"], r["J_den"])})
    return out

def main():
    rows = load()
    print("=== b=2 (J = c_m - c_{m+2}) — verify ===")
    for m in [2, 4, 6]:
        js = {r["J"] for r in rows if r["b"] == 2 and r["m"] == m}
        formula = C[m] - C[m+2]
        ok = js == {formula}
        print(f"  m={m}: data={sorted(map(str,js))}  c_{m}-c_{m+2}={formula}  match={ok}")

    print("\n=== b=3 values vs c-box-spline differences — search ===")
    # targets by (m, deg-seq)
    targets = {}
    for r in rows:
        if r["b"] != 3 or r["J"] == 0:
            continue
        ds = tuple(sorted((sum(v for (u,ww),v in r['H'].items() if u==i or ww==i) for i in range(3)), reverse=True))
        targets[(r["m"], ds)] = r["J"]
    print("  collected b=3 nonzero targets:")
    for k in sorted(targets, key=lambda x:x[0]):
        print("    ", k, targets[k])

    # Print candidate c-combinations near target values
    print("\n  candidate combos (c_w - c_x*c_y and similar):")
    cset = {2,4,6,8,10}
    combos = {}
    for a in cset:
        for b in cset:
            if b >= a: continue
            v = C[a] - C[a+2]               # pure
            combos[f"c{a}-c{a+2}"] = v
            for d in cset:
                combos[f"c{d}*(c{a}-c{a+2})"] = C[d]*(C[a]-C[a+2])
    seen=set()
    for name,v in combos.items():
        if v in seen: continue
        seen.add(v)
        print(f"    {name} = {v}")

if __name__ == "__main__":
    main()
