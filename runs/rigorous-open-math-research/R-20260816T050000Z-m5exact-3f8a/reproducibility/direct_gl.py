#!/usr/bin/env python
"""High-precision multi-dim integration of J_sigma using tensor-product Gauss-Legendre on a
cluster grid over several W values (Romberg-like convergence in W), used as an INDEPENDENT
validation of the box-spline coarea exact rationals.

J_sigma = int_{R^{b-1}} prod_edges K(x_u-x_v) * rho_b(rel) dx.
Because K decays, we integrate over [-W,W]^(b-1) with large N for mesh, extrapolating W.
"""
import numpy as np
import scipy.special as sp

def sincp(t):
    t = np.asarray(t, dtype=float)
    return np.where(np.abs(t) < 1e-12, 1.0, np.sin(np.pi * t) / (np.pi * t))

def rho_b(xarr):
    # xarr: (b-1,)-vector rel coords; returns bxb det value
    b = len(xarr) + 1
    xx = np.concatenate([xarr, [0.0]])
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
    return k, b, idx, edges

def integrand_f(blocks):
    k, b, idx, edges = build_edges(blocks)
    def f(x):
        coord = np.append(x, 0.0)  # block b-1 pinned
        val = np.ones(x.shape[0])
        for (u, v) in edges:
            if u != v:
                val = val * sincp(coord[u] - coord[v])
        rho = np.empty(x.shape[0])
        for i in range(x.shape[0]):
            rho[i] = rho_b(x[i])
        return val * rho
    return f, b

def gl_grid(W, N):
    x, w = np.polynomial.legendre.leggauss(N)
    # map [-1,1] to [-W,W]
    xg = W * x
    wg = W * w
    return xg, wg

def J_gl(blocks, W=20, N=100):
    f, b = integrand_f(list(blocks))
    dim = b - 1
    grids = [gl_grid(W, N) for _ in range(dim)]
    # tensor product eval
    ax = [np.newaxis] * (2 * dim)
    def place(g, d):
        axes = [None] * (2 * dim)
        axes[d] = slice(None)
        return g[tuple(axes)]
    # iterative
    total = 0.0
    # vectorize via meshgrid
    ms = np.meshgrid(*[g[0] for g in grids], indexing='ij')
    ws = np.meshgrid(*[g[1] for g in grids], indexing='ij')
    pts = np.stack([m.ravel() for m in ms], axis=1)  # (P, dim)
    ww = np.ones(pts.shape[0])
    for wg in ws:
        ww = ww * wg.ravel()
    vals = f(pts)
    return np.sum(ww * vals)

if __name__ == "__main__":
    import sys
    target = eval(sys.argv[1])
    blocks = [frozenset(s) for s in target]
    print("partition:", blocks)
    for W in [10, 14, 18, 22]:
        v = J_gl(blocks, W=W, N=120)
        print(f"  W={W}: J={v:+.10f}")
