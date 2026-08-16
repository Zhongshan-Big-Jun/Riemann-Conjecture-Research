#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scan_disconnected.py — M1 exploration: find partitions sigma (k=3..7) whose cycle-crossing
multigraph H_sigma is DISCONNECTED, and compute J_sigma via the exact box-spline engine to
test the "disconnected => J=0" claim (M1) on concrete instances not present in k<=6 data.
Run: py -3.10 scan_disconnected.py
"""
import os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enumerate_moments import partitions_of
from boxspline_exact import shape_integral_exact
from dataset import cycle_multigraph, crossing_count, profile, block_of

def components(H, b):
    par = list(range(b))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    deg = [0]*b
    for (u, v) in H:
        ru, rv = f(u), f(v)
        if ru != rv:
            par[ru] = rv
        deg[u] += 1; deg[v] += 1
    vs = [i for i in range(b) if deg[i] > 0]
    return len({f(i) for i in vs}) if vs else 0

def main():
    for k in range(3, 8):
        parts = partitions_of(k)
        disc = []
        conn = 0
        for blocks in parts:
            H = cycle_multigraph(k, blocks)
            m = crossing_count(k, blocks)
            b = len(blocks)
            c = components(H, b)
            if c > 1:
                # disconnected (proper components, ignoring isolated vertices)
                disc.append((blocks, b, m, c, H))
            else:
                conn += 1
        print(f"k={k}: total={len(parts)} connected={conn} disconnected={len(disc)}")
        for blocks, b, m, c, H in disc[:12]:
            # J via exact engine; may be slow for large b, guard with try
            try:
                J = shape_integral_exact(list(blocks), k)
                Jf = F(J)
            except Exception as e:
                Jf = f"ERR:{e}"
            print(f"  b={b} m={m} comps={c} profile={profile(blocks)} H={dict(sorted(H.items()))} J={Jf}")

if __name__ == "__main__":
    main()
