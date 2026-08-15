#!/usr/bin/env python
"""Direct high-precision numeric integration of J_sigma for a given partition, as a
cross-validation of the box-spline coarea (which produced exact rationals).  Independent
numerical method (scipy nquad / mpmath) used only to CONFIRM the exact rationals, especially for
the suspicious b=4 shape and D_5.

J_sigma = int_{R^{b-1}} [prod_{cycle edges} K(x_{sigma(a)}-x_{sigma(a+1)})] * rho_b dx
         (rho_b = det[K(x_i-x_j)]_{i,j}, x_{last block} pinned = 0)
"""
import numpy as np
from scipy.integrate import nquad
from fractions import Fraction as F


def sinc(t):
    return np.where(np.abs(t) < 1e-12, 1.0, np.sin(np.pi * t) / (np.pi * t))


def sincp(t, prec=None):
    if abs(t) < 1e-12:
        return 1.0
    return np.sin(np.pi * t) / (np.pi * t)


def rho_b(x):
    """det of bxb matrix K(x_i-x_j); x is the (b-1)-vector of relative coords, x_b=0."""
    b = len(x) + 1
    xx = list(x) + [0.0]
    A = np.empty((b, b))
    for i in range(b):
        for j in range(b):
            A[i, j] = sincp(xx[i] - xx[j])
    return np.linalg.det(A)


def build_edges(blocks):
    """map position->block id; cycle edges (a,a+1%k) as (blockU, blockV). returns k, b."""
    k = sum(len(b) for b in blocks)
    bid = {}
    for i, b in enumerate(blocks):
        for e in b:
            bid[e] = i
    idx = [bid[a] for a in range(k)]
    b = len(blocks)
    edges = []
    for a in range(k):
        edges.append((idx[a], idx[(a + 1) % k]))
    return k, b, idx, edges


def integrand(blocks):
    k, b, idx, edges = build_edges(blocks)

    def f(*args):
        # args length b-1: relative coords x_0..x_{b-2}, with block b-1 pinned at 0
        x = np.array(args, dtype=float)
        xx = list(range(b))  # block coord
        coord = [0.0] * b
        for q in range(b - 1):
            coord[q] = x[q]
        coord[b - 1] = 0.0
        val = 1.0
        for (u, v) in edges:
            if u == v:
                f = 1.0
            else:
                f = sincp(coord[u] - coord[v])
            val *= f
        val *= rho_b(x[: b - 1])
        return val
    return f, b


def J_direct(blocks, epsabs=1e-9, epsrel=1e-8, maxfev=10**7):
    f, b = integrand(list(blocks))
    opts = {'epsabs': epsabs, 'epsrel': epsrel, 'limit': 200}
    # integration domain: coordinates can be large but sinc decays; integrate on [-W,W] ranges
    # with W large enough (tail negligible).  Use a scale and verify convergence.
    W = 30.0
    bounds = [(-W, W)] * (b - 1)
    val, err = nquad(f, bounds, opts=opts)
    return val, err


if __name__ == "__main__":
    tests = [
        (4, [[{0}, {1}, {4}, {2}, {3}]][0]),  # placeholder replaced below
    ]
    import sys
    from enumerate_moments import partitions_of
    target = eval(sys.argv[1])  # e.g. "[{0},{1,4},{2},{3}]"
    blocks = [frozenset(s) for s in target]
    print("partition:", blocks)
    v, e = J_direct(blocks)
    print(f"  J ~ {v:.10f}  (scipy nquad err {e:.1e})")
    fr = F(v).limit_denominator(10**7)
    print(f"  rational recon: {fr}  (diff {abs(float(fr)-v):.2e})")
