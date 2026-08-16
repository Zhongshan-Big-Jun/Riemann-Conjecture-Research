#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
final_rule.py — test the vanishing rule against the full exact dataset (k=3..6).
Rule (Conjectured Lemma P / G2):
   J_sigma != 0   iff   the cycle-edge multigraph H_sigma is CONNECTED
                        AND its surplus  s := m - b = m - #blocks  satisfies  s >= b - 2
                        i.e.  m >= 2b - 2   (all degrees of H are even automatically).
Equivalently  J_sigma = 0  iff  (H disconnected)  or  (m <= 2b - 3 for b>=2).
Special cases: b=1 (m=0,s=-1>= -1) nonzero J=1.

We also test the sub-variants and record which case each partition falls into.
Run: py -3.10 final_rule.py
"""
import os, sys, json
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def components(H, b):
    par = list(range(b))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    deg=[0]*b
    for (u,v) in H:
        ru,rv=f(u),f(v)
        if ru!=rv: par[ru]=rv
        deg[u]+=1; deg[v]+=1
    vs=[i for i in range(b) if deg[i]>0]
    return len({f(i) for i in vs}) if vs else 0

def load_all():
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "allJ.json"), encoding="utf-8") as f:
        raw = json.load(f)
    rows = []
    for r in raw:
        H = {(int(u), int(v)): c for (u, v), c in r["H_edges"]}
        rows.append({
            "k": r["k"], "blocks": r["blocks"], "b": r["b"], "m": r["m"],
            "profile": tuple(r["profile"]), "H": H,
            "J": F(r["J_num"], r["J_den"]),
        })
    return rows

def rule_predict(b, m, H):
    """True -> predicted nonzero."""
    if b == 1:
        return True
    conn = components(H, b) == 1
    if not conn:
        return False
    return m >= 2 * b - 2

def main():
    rows = load_all()
    tp = tn = fp = fn = 0
    mism = []
    # also capability: check connectivity separately
    coord = {}
    for r in rows:
        actual = (r["J"] != F(0))
        pred = rule_predict(r["b"], r["m"], r["H"])
        if pred == actual:
            if actual: tp += 1
            else: tn += 1
        else:
            if actual: fn += 1
            else: fp += 1
            mism.append(r)
        key = (r["b"], r["m"], components(r["H"], r["b"]))
        coord.setdefault(key, [0,0])
        coord[key][1] += 1
        coord[key][0] += 1 if actual else 0
    tot = tp + tn + fp + fn
    print(f"TP={tp} TN={tn} FP={fp} FN={fn}  total={tot}  accuracy={(tp+tn)/tot:.6f}")
    if not mism:
        print("RULE MATCHES ALL DATA (k=3..6) — 100%")
    else:
        for r in mism:
            print("MISMATCH", {k2:r[k2] for k2 in ["k","b","m","profile","J"]})
    print("\n=== (b, m, #comp) -> nonzero/count (all k) ===")
    for key in sorted(coord):
        print(f"  b={key[0]} m={key[1]} comps={key[2]}: nonzero={coord[key][0]}/{coord[key][1]}")

if __name__ == "__main__":
    main()
