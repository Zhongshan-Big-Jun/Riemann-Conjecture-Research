#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
graph_rule.py — test candidate vanishing rules for J_sigma against the exact per-partition
data (k=3..6). For each partition we have the cycle-edge multigraph H_sigma (b vertices,
m crossing edges; every degree even since the cycle is closed) and the exact J.

Predicates tested (return True i.e. "predicted vanish"):
  (a) block-count threshold: b >= T   [known to fail, kept for the record]
  (b) H has an isolated vertex (degree-0 block among cycle edges)
  (b') H has a cut/isolated connected component
  (c) H has a bridge / is a forest
  (d) all-degrees-even (always true; controL)
  (e) m_crossing satisfies some parity
We then intersect with the data: report how many true-J=0/1 match before/after.
Run: py -3.10 graph_rule.py  (uses perJ_k*.json for k=3..5 and m6 CSVs for k=6)
"""
import os, sys, json
from fractions import Fraction as F
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dataset import load_m6, partitions_of, cycle_multigraph, crossing_count, profile

def canonkey(blocks):
    return tuple(tuple(sorted(b)) for b in blocks)

def degree_of_H(H, b):
    deg = [0]*b
    for (u, v), c in H.items():
        deg[u] += c
        deg[v] += c
    return deg

def empty():
    return {"tp": 0, "tn": 0, "fp": 0, "fn": 0}

def acc(r, p, actual):
    if p == actual:
        if actual == 0:
            r["tn"] += 1
        else:
            r["tp"] += 1
    else:
        if actual == 0:
            r["fp"] += 1
        else:
            r["fn"] += 1

def pred_b_geq_T(H, b, m, T):
    return b >= T

def pred_isolated(H, b, m):
    deg = degree_of_H(H, b)
    return 0 in deg

def pred_isolated_component(H, b, m):
    # count vertices with degree 0; also disconnected (ignores isolated only)
    deg = degree_of_H(H, b)
    return any(d == 0 for d in deg)

def pred_forest(H, b, m):
    # cycle-edge graph is a forest (no multi-cycle): i.e. as simple support, acyclic
    # simple edges = set of support
    supp = set(H)
    # count independent edges in simple support
    n_edges_supp = len(supp)
    verts = {v for e in supp for v in e}
    nverts = len(verts)
    return n_edges_supp <= nverts - 1  # acyclic (forest) on its vertices

def pred_all_even(H, b, m):
    deg = degree_of_H(H, b)
    return all(d % 2 == 0 for d in deg)

def pred_m_parity(H, b, m, want=2):
    return (m % 4) == want

def pred_disconnected(H, b, m):
    # component count > number of nonzero-deg vertices groups
    parent = list(range(b))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for (u, v) in H:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
    deg = degree_of_H(H, b)
    verts = [i for i in range(b) if deg[i] > 0]
    if not verts:
        return True
    roots = {find(i) for i in verts}
    return len(roots) > 1

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    # gather (k, blocks, H, b, m, J, nonzero)
    rows = []
    for k in [3, 4, 5]:
        fp = os.path.join(base, f"perJ_k{k}.json")
        with open(fp, encoding="utf-8") as f:
            for r in json.load(f):
                blocks = tuple(frozenset(b) for b in r["blocks"])
                H = {(int(u), int(v)): c for (u, v), c in r["H_edges"]}
                rows.append((k, blocks, H, r["b"], r["m_crossing"],
                             F(r["J_num"], r["J_den"]), r["nonzero"]))
    # k=6 from CSVs
    k6 = load_m6()
    for blocks, J in k6.items():
        H = cycle_multigraph(6, blocks)
        m = crossing_count(6, blocks)
        b = len(blocks)
        rows.append((6, blocks, H, b, m, J, J != 0))

    print(f"total partitions used: {len(rows)} (k=3..6)")
    for k in [3, 4, 5, 6]:
        sub = [r for r in rows if r[0] == k]
        nz = sum(1 for r in sub if r[6])
        print(f"  k={k}: n={len(sub)}, nonzero J = {nz}")

    tests = {
        "(a) b>=4": lambda H,b,m: pred_b_geq_T(H,b,m,4),
        "(a') b>=5": lambda H,b,m: pred_b_geq_T(H,b,m,5),
        "(b) isolated block (deg 0 in H)": pred_isolated,
        "(b') disconnected/isolated comp": lambda H,b,m: pred_isolated_component(H,b,m) or pred_disconnected(H,b,m),
        "(c) H simple support is a forest": pred_forest,
        "(d) all degrees even [control]": pred_all_even,
        "(e) m % 4 == 2": lambda H,b,m: pred_m_parity(H,b,m,2),
        "(e') m % 4 == 0": lambda H,b,m: pred_m_parity(H,b,m,0),
    }
    for name, fn in tests.items():
        r = empty()
        for (k, blocks, H, b, m, J, nz) in rows:
            p = fn(H, b, m)
            acc(r, p, (J == F(0)))
        tot = r["tp"]+r["tn"]+r["fp"]+r["fn"]
        accr = (r["tp"]+r["tn"])/tot if tot else 1
        print(f"\n--- {name} ---")
        print(f"  TP={r['tp']} TN={r['tn']} FP={r['fp']} FN={r['fn']}  accuracy={accr:.3f}")
        if r["fp"] == 0 and r["fn"] == 0:
            print("  PERFECT match on k=3..6 data")

if __name__ == "__main__":
    main()
