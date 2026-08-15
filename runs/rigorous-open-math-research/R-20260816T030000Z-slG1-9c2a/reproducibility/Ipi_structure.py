#!/usr/bin/env python
"""Structural analysis of exact I_pi for k=5: test whether the box-spline value factors over
the connected components of the combined (cycle union pi-edges) graph, i.e. whether
I_pi = prod over components C of boxvalue(C), giving a closed form and a route to the
general cancellation. Uses exact rationals from D5_exact.json (subagent) + reclassification."""
import json, itertools
from fractions import Fraction
from collections import defaultdict

D=json.load(open(r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T030000Z-slG1-9c2a\reproducibility\D5_exact.json","r"))
# perms map: str(pi) -> [sign, vol(sqrtdet factor), rational-I]
perms=D["perms"]
print("max denominator asserted:", D["maxdenom"])

K=5
def build_graph(pi):
    # vertices 0..4, edges: cycle (a,a+1 mod5) and (a,pi[a]) ; self-loop = loop at a
    edges=[]
    for a in range(K):
        edges.append(tuple(sorted([a,(a+1)%K])))
    for a in range(K):
        edges.append(tuple(sorted([a,pi[a]])))
    # connected components (undirected, self-loops ignored for connectivity)
    adj={v:set() for v in range(K)}
    for (u,v) in edges:
        if u!=v:
            adj[u].add(v); adj[v].add(u)
    seen=set(); comps=[]
    for v in range(K):
        if v in seen: continue
        stack=[v]; comp=set()
        while stack:
            x=stack.pop()
            if x in comp: continue
            comp.add(x)
            for y in adj[x]:
                stack.append(y)
        comps.append(frozenset(comp)); seen|=comp
    # count self-loops per vertex
    loops=[edges.count((a,a)) for a in range(K)]
    return edges,comps,loops

# Tabulate I_pi per (cycle-type, signature of components aggregated)
bycomp={}
for ps,val in perms.items():
    pi=tuple(int(c) for c in ps.strip('()').split(','))
    Ir=Fraction(val[2])
    edges,comps,loops=build_graph(pi)
    comp_sizes=tuple(sorted(len(c) for c in comps))
    # multiplicity of edges contributed per pair-type -> count non-loop edges per comp
    comp_key=[]
    for c in comps:
        in_c=[e for e in edges if e[0] in c and e[1] in c]
        comp_key.append((len(c),len(in_c)))
    comp_key=tuple(sorted((len(c),len([e for e in edges if e[0] in c and e[1] in c])) for c in comps))
    bycomp.setdefault(comp_key,set()).add((Ir,tuple(edges)))

print("\n== group by (component-size, edge-count-in-comp) signature ==")
for sig,vals in sorted(bycomp.items(), key=lambda kv:(kv[0][0][0],kv[0])):
    print(f"  sig={sig}: distinct I values: {sorted({(num,den) for num,den in [(v.numerator,v.denominator) for v in set(v[0] for v in vals)]})}")
