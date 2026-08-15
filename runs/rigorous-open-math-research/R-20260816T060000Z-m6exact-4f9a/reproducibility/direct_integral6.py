#!/usr/bin/env python
"""Drive direct numeric integration of J_sigma over R^{b-1} for k=6 shapes, as an INDEPENDENT
(audit-grade) method for the box-spline coarea. For low b (1..3) the smooth, localized integrand
is cheap and accurate, letting us reconstruct exact rationals. For b>=4 3-D/4-D/5-D integrals are
harder; used mainly to test vanishing vs small-nonzero.
"""
import sys, os, time, itertools
from fractions import Fraction as F
import numpy as np
from scipy.integrate import nquad
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enumerate_moments import partitions_of, blocksizes


def sincp(t):
    if abs(t) < 1e-12:
        return 1.0
    return np.sin(np.pi * t) / (np.pi * t)


def rho_b(x):
    """bxb det of K(x_i-x_j); x is (b-1)-vector of relative coords, last block pinned 0."""
    b = len(x) + 1
    xx = list(x) + [0.0]
    A = np.empty((b, b))
    for i in range(b):
        for j in range(b):
            A[i, j] = sincp(xx[i] - xx[j])
    return np.linalg.det(A)


def build_edges(blocks):
    k = sum(len(b) for b in blocks)
    bid = {}
    for i, b in enumerate(blocks):
        for e in b:
            bid[e] = i
    idx = [bid[a] for a in range(k)]
    b = len(blocks)
    edges = [(idx[a], idx[(a + 1) % k]) for a in range(k)]
    return b, edges


def integrand_fn(blocks):
    b, edges = build_edges(blocks)
    def f(*args):
        x = np.array(args, dtype=float)
        coord = [0.0] * b
        for q in range(b - 1):
            coord[q] = x[q]
        coord[b - 1] = 0.0
        val = 1.0
        for (u, v) in edges:
            if u == v:
                continue
            val *= sincp(coord[u] - coord[v])
        val *= rho_b(x[: b - 1])
        return val
    return f, b


def J_direct(blocks, W=25.0, epsabs=1e-9, epsrel=1e-7, maxfev=5*10**6, limit=300):
    f, b = integrand_fn(list(blocks))
    if b == 1:
        return 1.0, 0.0
    opts = {"epsabs": epsabs, "epsrel": epsrel, "limit": limit}
    val, err = nquad(f, [(-W, W)] * (b - 1), opts=opts)
    return val, err


def reconstruct(val, tol=2e-6, maxden=2*10**6, zero_abs=2e-5):
    if abs(val) < zero_abs:
        return F(0), "zero"
    fr = F(float(val)).limit_denominator(maxden)
    err = abs(float(fr) - val)
    if err > tol * max(1.0, abs(val)):
        return None, f"noise: reconst {fr} diff {err:.1e}"
    return fr, "ok"


if __name__ == "__main__":
    parts = partitions_of(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
    if len(sys.argv) >= 3:
        # specific blocks given as python literal list of sets
        import ast
        target = ast.literal_eval(sys.argv[2])
        blocks = [frozenset(s) for s in target]
        t0 = time.time()
        v, e = J_direct(blocks)
        fr, tag = reconstruct(v)
        print(f"blocks={sorted(sorted(x) for x in blocks)} b={len(blocks)} J={v:+.10f} err={e:.1e} tags={tag} -> {fr} wall={time.time()-t0:.1f}s")
    else:
        t0=time.time()
        for b_target in sorted(set(len(bl) for bl in parts)):
            cnt=0; s=0.0; wall0=time.time()
            for blocks in parts:
                if len(blocks)!=b_target: continue
                cnt+=1
                v, e = J_direct(blocks)
                fr, tag = reconstruct(v)
                s += float(fr)
            print(f"b={b_target}: n={cnt} sum={s:+.8f} wall={time.time()-wall0:.1f}s", flush=True)
        print(f"total wall={time.time()-t0:.1f}s")
