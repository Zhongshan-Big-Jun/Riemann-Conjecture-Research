"""Numerical (evidence-only) minimization of F_{k-1} over 8/10 variables.

F_{k-1}(g) = 1/(500(k-1)) sum_i g_i
           + sum_{s=1}^{k-1} (2/(k-s)) sum_{i=1}^{k-s} w(g_i+...+g_{i+s-1})
where w(x) = k(x)^2, k = normalized Montgomery-Taylor kernel (sinc form).
Also the pressure-only lower bound and the target thresholds.
This is scope/evidence ONLY for deciding whether a rigorous record is plausible.
"""
import numpy as np
from scipy.optimize import minimize
import math

def kernel_min_k():
    """Small helper: normalized kernel using high-precision target via mpmath-free evaluation.
    We use mpmath for the transcendental, evaluate at high dps."""
    import mpmath as mp
    mp.mp.dps = 50
    sqrt2 = mp.sqrt(2)
    k_zero = sqrt2*mp.sin(1/sqrt2)
    def kk(x):
        freq = mp.pi*x
        zl = mp.pi*x - 1/sqrt2
        zr = mp.pi*x + 1/sqrt2
        val = ((mp.sin(zl))/zl + (mp.sin(zr))/zr)/2
        return val/k_zero
    return kk

def make_F(k):
    kk = kernel_min_k()
    import mpmath as mp
    def F(g):
        # g: array of k-1 gaps
        total = 0.0
        # linear pressure term
        total += sum(g)/(500.0*(k-1))
        L = k-1
        for s in range(1, L+1):
            coef = 2.0/(k-s)
            for i in range(L - s + 1):   # i from 0..L-s
                x = sum(g[i:i+s])
                total += coef*float(kk(x))
        return total
    return F

def minimize_F(k, iters=20):
    F = make_F(k)
    L = k-1
    best = (1e9, None)
    rng = np.random.default_rng(0)
    # kernels vanish near specific zero spacings; init grids
    init_points = []
    # zeros of sinc(pi x - 1/sqrt2): pi x - 1/sqrt2 = n*pi -> x = n + 1/(sqrt2 pi)
    shift = 1.0/(math.sqrt(2)*math.pi)
    for a in range(-2,5):
        for b in range(-2,5):
            if k>=9:
                # 8-var: try putting gaps near shifted integers
                pt = np.full(L, abs(a+b)+0.01)
            init_points.append(np.array([max(1e-3, abs((a*i+b)%11)+0.01) for i in range(L)]))
        for c in range(-2,3):
            init_points.append(np.array([shift+abs(a)+abs(c*i) for i in range(L)]))
    for pt in init_points[:2000]:
        res = minimize(F, pt, method='L-BFGS-B', bounds=[(0,None)]*L,
                       options={'maxiter': 20000, 'ftol': 1e-16, 'gtol': 1e-9})
        if res.fun < best[0]:
            best = (res.fun, res.x)
    return best

for k in (7, 9, 11):
    f, x = minimize_F(k)
    print(f"k={k}: approx min F_{k-1} = {f:.8f}   at g={np.round(x,3)}")
