"""Compute D_5 = sum_{pi in S5} sign(pi) * I_pi, where I_pi = int P_5(x) * [pi-term of det rho_5] dx,
P_5 = K(x1-x2)K(x2-x3)K(x3-x4)K(x4-x5)K(x5-x1), rho_5 = det[K(x_a,x_b)], K=sinc.

For each permutation pi (as 0-indexed list of images), the integrand is
  sign(pi) * prod_{a=0..4} K(x_a - x_{a+1}) * prod_{a=0..4} K(x_a - x_{pi(a)}).
We fix x_5 = 0 (translation invariance) and integrate x_1..x_4 over [-R,R]^4 with a
vectorized Gauss-Legendre tensor. This reveals per-permutation terms and the signed sum.

EVIDENCE ONLY (quadrature + box truncation). Not a proof.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
import itertools, sys

def sinc(t):
    t = np.asarray(t, dtype=float)
    out = np.ones_like(t)
    nz = np.abs(t) > 1e-12
    out[nz] = np.sin(np.pi*t[nz])/(np.pi*t[nz])
    return out

def perm_sign(perm):
    # perm: list of images 0..k-1
    n = len(perm)
    seen = [False]*n
    sign = 1
    for i in range(n):
        if not seen[i]:
            # cycle length
            cyc = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                cyc += 1
            if cyc % 2 == 0 and cyc > 0:
                sign *= -1
    return sign

def I_call(k, perm, X):
    """X: (...,k) points. Returns prod_edges K(x_a-x_b) for the graph = cycle + perm edges.
    cycle edges: (a,a+1 mod k). perm edges: (a, perm(a))."""
    shape = X.shape[:-1]
    P = np.ones(shape)
    for a in range(k):
        b = (a+1) % k
        P = P * sinc(X[...,a]-X[...,b])
    for a in range(k):
        b = perm[a]
        P = P * sinc(X[...,a]-X[...,b])
    return P

def compute(k, R, nperdim):
    perms = list(itertools.permutations(range(k)))
    nodes, w = leggauss(nperdim)
    x = 0.5*R*(nodes+1); wm = 0.5*R*w
    g = np.meshgrid(x,x,x,x, indexing='ij')   # k-1=4 dims for k=5
    y4 = np.stack(g, axis=-1).reshape(-1, k-1)
    shape = (k-1,)
    # X = (x0..x_{k-2}, 0): align so vertex labels 0..k-2 are the free vars, vertex k-1 pinned
    X = np.concatenate([y4, np.zeros(y4.shape[:-1]+(1,))], axis=-1)
    W = np.array([1.0])
    for _ in range(k-1):
        W = np.multiply.outer(W, wm)
    Wf = W.reshape(-1)
    results = {}
    total = 0.0
    for perm in perms:
        sg = perm_sign(list(perm))
        val = np.sum(I_call(k, list(perm), X)*Wf)
        results[perm] = (sg, val)
        total += sg*val
    return results, total

if __name__ == "__main__":
    k = 5
    for R, n in [(4,18),(6,18),(8,16)]:
        results, total = compute(k, R, n)
        print(f"=== k={k} R={R} n={n} ===", flush=True)
        nz = [(p,(sg,v)) for p,(sg,v) in results.items() if abs(v) > 1e-8]
        nz.sort(key=lambda t: -abs(t[1][1]))
        print(f" total D5 = {total:+.6e}", flush=True)
        print(f" nonzero-magnitude terms count = {len(nz)}")
        for p,(sg,v) in nz[:20]:
            print(f"   pi={p} sign={sg:+d} I={v:+.6e} contrib={sg*v:+.6e}", flush=True)
        print(flush=True)
