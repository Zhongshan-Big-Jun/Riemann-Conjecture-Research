"""Fast targeted (evidence-only) minimization of F_{k-1} over k-1 variables.

For scoping only. Uses numpy float64 kernel via sinc form. Starts from the
k-1 prior optimum (found for smaller k) and copies of it, plus a handful of
structured and random starts. Prints min and both the value and where it sits
relative to the 7-point certificate and the record-threshold.
"""
import numpy as np
from scipy.optimize import minimize
import math

sqrt2 = math.sqrt(2.0)
k_zero = sqrt2*math.sin(1.0/sqrt2)

def kk(x):
    x = np.asarray(x, dtype=np.float64)
    with np.errstate(divide='ignore', invalid='ignore'):
        zl = np.pi*x - 1.0/sqrt2
        zr = np.pi*x + 1.0/sqrt2
        sinc_l = np.where(np.abs(zl)<1e-14, 1.0, np.sin(zl)/zl)
        sinc_r = np.where(np.abs(zr)<1e-14, 1.0, np.sin(zr)/zr)
    return (sinc_l + sinc_r)/2.0/k_zero

def make_grad_F(k):
    """Return (F, grad) where F/grad use float64."""

    def F(g):
        g = np.asarray(g, float)
        total = float(g.sum())/(500.0*(k-1))
        for span in range(1, k):
            coef = 2.0/(k-span)
            for i in range(k-span):
                total += coef*float(kk(g[i:i+span].sum()))
        return total
    return F

def minimize_F(k, base, n_random=400):
    L = k-1
    F = make_grad_F(k)
    rng = np.random.default_rng(777)
    inits = []
    # start from a base optimum extended by a new gap near 0
    for rep in range(1, min(8, L+1)):
        for j in range(L-rep+1):
            v = list(base)
            # insert `rep` small gaps at position j
            cand = np.array(v[:j] + [0.001]*rep + v[j:][:L-j-rep] + [0.001]*(L-len(v)) )[:L]
            if len(cand) == L:
                inits.append(cand)
    # equal small gaps
    inits.append(np.zeros(L))
    for mult in np.arange(0.2, 8.0, 0.4):
        inits.append(np.full(L, mult))
    # two-tone patterns
    for A in np.arange(0.2,3.0,0.3):
        for B in np.arange(0.2,3.0,0.3):
            inits.append(np.array([(A if i%2==0 else B)+ (math.sin(i*1.3)*0.05) for i in range(L)]))
    for _ in range(n_random):
        inits.append(rng.uniform(0.0, 12.0, L))
    best = (1e18, None)
    for pt in inits:
        try:
            res = minimize(F, pt, method='L-BFGS-B', bounds=[(0,None)]*L,
                           options={'maxiter': 1500, 'ftol':1e-14, 'gtol':1e-7})
        except Exception:
            continue
        if res.fun < best[0]:
            best = (res.fun, res.x)
    return best

# base optimum for k=7 from prior runs ~ (some config). We search k=7 from scratch too.
b7 = minimize_F(7, [], n_random=600)

# for k=9 use base = b7 extended; for k=11 use b9.
print(f"k=7:  min ~ {b7[0]:.9f}  g={np.round(b7[1],3)}")

b9 = minimize_F(9, b7[1], n_random=800)
print(f"k=9:  min ~ {b9[0]:.9f}  g={np.round(b9[1],3)}")

b11 = minimize_F(11, b9[1], n_random=1000)
print(f"k=11: min ~ {b11[0]:.9f}  g={np.round(b11[1],3)}")

print("\nrecord threshold (f needed to beat 0.673008528) ~ 0.0038296")
print("class-limit threshold ~ 0.0037263")
