"""Fast scoping for k=10 minimum f_10 (evidence only).

Same machinery as scoping_k9.py (extpress run, validated against the k=9
certified minimum basin). k=10 -> 9 pressure variables, F_9.

Evidence-only label: minimization, NOT a certificate. Historical lesson
(2026-08-15): the k=9 scoping found a LOCAL minimum 0.0039818; the true
minimum (0.003950049001339790) was found later by box minimization during
the failed 0.00395 certification. So treat the value as an UPPER bound on
the true minimum, i.e. inf F_9 <= scoped value; certification is the only
rigorous path.
"""
import numpy as np
from scipy.optimize import minimize
import math, sys

sqrt2 = math.sqrt(2.0)
k_zero = sqrt2 * math.sin(1.0 / sqrt2)

def kk(x):
    x = np.asarray(x, float)
    with np.errstate(divide='ignore', invalid='ignore'):
        zl = np.pi * x - 1.0 / sqrt2
        zr = np.pi * x + 1.0 / sqrt2
        sl = np.where(np.abs(zl) < 1e-14, 1.0, np.sin(zl) / zl)
        sr = np.where(np.abs(zr) < 1e-14, 1.0, np.sin(zr) / zr)
    return (sl + sr) / 2.0 / k_zero

def make_F(k):
    L = k - 1
    def F(g):
        g = np.asarray(g, float)
        t = float(np.sum(g)) / (500.0 * L)
        for span in range(1, k):
            c = 2.0 / (k - span)
            for i in range(k - span):
                q = float(kk(np.sum(g[i:i + span])))
                t += c * q * q
        return t
    return F

def scope(k, n_rand, out, seeds, progress_every=200):
    L = k - 1
    F = make_F(k)
    rng = np.random.default_rng(20260815)
    best = (1e18, None)
    n_evals = 0
    def try_pt(pt):
        nonlocal best, n_evals
        r = minimize(F, pt, method='L-BFGS-B', bounds=[(0, None)] * L,
                     options={'maxiter': 2000, 'ftol': 1e-14, 'gtol': 1e-9})
        n_evals += r.nfev
        if r.fun < best[0]:
            best = (r.fun, r.x)
    starts = []
    for pt in seeds:
        starts.append(np.asarray(pt, float))
    # structured starts
    for rep in range(1, L + 1):
        for pos in range(0, L - rep + 1):
            for big in np.array([0.9, 1.0, 1.2, 1.5, 2.0]):
                g = np.full(L, big); g[pos:pos + rep] = 0.001
                starts.append(g)
    for a in np.linspace(0.2, 4.0, 40):
        starts.append(np.full(L, a))
    for idx, pt in enumerate(starts):
        try_pt(pt)
        if (idx + 1) % progress_every == 0:
            sys.stdout.write(f"  [{idx+1}/{len(starts)} structured] best {best[0]:.12f}\n")
            sys.stdout.flush()
    for i in range(n_rand):
        u = np.where(rng.uniform(0, 1, L) < 0.15, 0.003, rng.uniform(0.3, 4.0, L))
        try_pt(u)
        if (i + 1) % progress_every == 0:
            sys.stdout.write(f"  [rand {i+1}/{n_rand}] best {best[0]:.12f}\n")
            sys.stdout.flush()
    sys.stdout.write(f"{out} k={k}: scoped inf F <= {best[0]:.12f} (nfev total {n_evals})\n")
    sys.stdout.flush()
    np.save(f'k{k}_opt.npy', best[1])
    return best

if __name__ == '__main__':
    # Seeds: k=9 certified-minimum basin (lower corner of the grid-4000
    # critical leaf) and the k=9 scoped (local) minimum, extended to 9 gaps.
    k9_true_min_cfg = [1.0465, 1.996, 1.9995, 1.9995, 1.9865, 1.04525, 1.97575, 1.04525]
    try:
        k9_opt = np.load(r'F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260814T045000Z-extpress-2f36ae\reproducibility\k9_opt.npy')
        seeds = []
        for pos in range(9):
            g = [float(x) for x in k9_opt]
            g.insert(pos, 0.003)
            seeds.append(g[:9])
    except Exception:
        seeds = []
    for pos in range(9):
        g = list(k9_true_min_cfg)
        g.insert(pos, 0.003)
        seeds.append(g[:9])
    # k=7 scoped config as a further seed family
    try:
        k7_opt = np.load(r'F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260814T045000Z-extpress-2f36ae\reproducibility\k7_opt.npy')
        for pos in range(9):
            g = list(k7_opt)
            while len(g) < 9:
                g.insert(pos, 0.003)
            seeds.append(g[:9])
    except Exception:
        pass
    print("seeds:", len(seeds))
    scope(10, 1500, "scoping", seeds)
    print("done")
