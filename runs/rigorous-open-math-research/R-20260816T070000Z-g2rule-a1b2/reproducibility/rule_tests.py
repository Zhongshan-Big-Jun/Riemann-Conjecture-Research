#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
rule_tests.py — definitive checks against k=6 exact per-partition data:
  1. isoclass-determinism: same abstract multigraph H (up to relabel) => same J.
  2. tabulate J vs (b, m, degree-seq, cyclomatic-number c = m - b + #conncomp)
  3. test candidate vanishing predicates.
Run: py -3.10 rule_tests.py
"""
import os, sys
from fractions import Fraction as F
from itertools import permutations
from collections import defaultdict, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dataset import load_m6, cycle_multigraph, crossing_count

def canonical_form(H, b):
    best = None
    for perm in permutations(range(b)):
        s = []
        for (u, v), c in sorted(H.items()):
            su, sv = perm[u], perm[v]
            a, z = (su, sv) if su < sv else (sv, su)
            s.append(f"{a}{z}x{c}")
        key = "|".join(s)
        if best is None or key < best:
            best = key
    return best

def degree_seq(H, b):
    d = [0]*b
    for (u, v), c in H.items():
        d[u] += c; d[v] += c
    return tuple(sorted(d, reverse=True))

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
    if not vs: return 0 if b==0 else (b if False else 1)
    return len({f(i) for i in vs})

def main():
    k6 = load_m6()
    # 1) isoclass determinism
    byiso = defaultdict(set)
    for blocks,J in k6.items():
        H = cycle_multigraph(6, blocks)
        byiso[(len(blocks), canonical_form(H,len(blocks)))].add(J)
    bad = {k for k,v in byiso.items() if len(v)>1}
    print(f"isoclasses: {len(byiso)}, classes with >1 J value: {len(bad)}")
    if bad:
        for k in list(bad)[:5]:
            print("   bad",k, sorted(map(str,byiso[k])))
    print()

    # 2) tabulate nonzero vs (b, m, deg-seq, cyclomatic)
    tab = defaultdict(lambda: [set(), 0, 0])
    for blocks,J in k6.items():
        H = cycle_multigraph(6, blocks)
        m = crossing_count(6, blocks)
        b = len(blocks)
        c = m - b + components(H,b)
        key=(b,m,c,degree_seq(H,b))
        tab[key][0].add(J)
        tab[key][1]+= (J!=F(0))
        tab[key][2]+=1
    print("=== (b, m, cyclomatic, degseq) -> nonzero/count ===")
    for key in sorted(tab, key=lambda x:(x[0],x[1])):
        vals,nz,cnt = tab[key]
        print(f"  b={key[0]} m={key[1]} cyc={key[2]:+d} degs={key[3]}  nonzero={nz}/{cnt}  J={sorted(map(str,vals))}")

if __name__=="__main__":
    main()
