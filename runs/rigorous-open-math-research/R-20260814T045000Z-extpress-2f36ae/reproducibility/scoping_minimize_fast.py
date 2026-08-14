"""Fast vectorized (evidence-only) minimization of F_{k-1} over k-1 variables.

For scoping only. Uses numpy float64 kernel evaluation via the sinc form.
"""
import numpy as np
from scipy.optimize import minimize
import math

sqrt2 = math.sqrt(2.0)
k_zero = sqrt2*math.sin(1.0/sqrt2)

def kk(x):
    x = np.asarray(x, dtype=np.float64)
    zl = np.pi*x - 1.0/sqrt2
    zr = np.pi*x + 1.0/sqrt2
    sinc_l = np.where(zl==0, 1.0, np.sin(zl)/zl)
    sinc_r = np.where(zr==0, 1.0, np.sin(zr)/zr)
    return (sinc_l + sinc_r)/2.0/k_zero

def make_F(k):
    L = k-1
    def F(g):
        total = float(sum(g))/(500.0*L)
        for span in range(1, L+1):
            coef = 2.0/(k-span)
            for i in range(L-span+1):
                x = float(np.sum(g[i:i+span]))
                total += coef*kk(x)
        return total
    return F

def minimize_F(k, n_init=1200):
    F = make_F(k)
    L = k-1
    rng = np.random.default_rng(12345)
    best = (1e18, None, 0)
    shift = 1.0/(sqrt2*np.pi)   # first kernel zero location ~0.225
    # candidate initial guesses: shift + integer combinations
    inits = []
    for _ in range(n_init):
        # random gaps in [0, 12]
        inits.append(rng.uniform(0.0, 12.0, L))
    # structured: around multiples of ~1 (kernels vanish every ~1)
    for mult in np.arange(0.5, 12.0, 0.5):
        inits.append(np.full(L, mult))
    for a in range(6):
        inits.append(np.linspace(0.2, 1.0+a*0.3, L))
    for b in range(0, 30, 3):
        inits.append(np.array([abs(math.sin(b*0.7+i))+0.05 for i in range(L)]))
    for idx, pt in enumerate(inits):
        res = minimize(F, pt, method='L-BFGS-B', bounds=[(0,None)]*L,
                       options={'maxiter': 4000, 'ftol':1e-15, 'gtol':1e-8})
        if res.fun < best[0]:
            best = (res.fun, res.x, idx)
    return best

for k in (7, 9, 11):
    f, x, idx = minimize_F(k)
    print(f"k={k}: min F_{k-1} ~ {f:.9f}  at g={np.round(x,3)} (init idx {idx})")
