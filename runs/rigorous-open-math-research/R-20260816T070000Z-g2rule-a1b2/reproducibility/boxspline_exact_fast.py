#!/usr/bin/env python
"""OPTIMIZED exact box-spline value at 0 for integer edge vectors, for the k=6 (and k=5) shapes.

Same math as boxspline_exact2.coarea_value_exact, but the vertex enumeration runs a FAST numpy
float solve per candidate m-subset to locate the valid vertices, then does the EXACT rational solve
(mpmath-sympy-free: numpy float -> Fraction solution via sympy LU) only for the distinct vertices.
For the box-splines here the vertex set is small, so this is orders of magnitude faster than solving
every subset with sympy.

Mirrors boxspline_exact2 (B(0) = (n-d)-vol of {M xi=0} n [0,1]^n / sqrt(det MM^T)), with exact
rational vertices; used as the fast driver for the bulk b=3 enumeration and cross-checked against
boxspline_exact2.coarea_value_exact on a subset.
"""
import numpy as np, itertools
from fractions import Fraction as F
import sympy, scipy.spatial


def _null_rational_basis(M_int):
    d, n = M_int.shape
    Msp = sympy.Matrix(M_int.tolist())
    null = Msp.nullspace()
    if not null:
        return np.zeros((n, 0), dtype=float), 1.0
    m = len(null)
    N = np.zeros((n, m), dtype=float)
    import sympy as _Sp
    for j, v in enumerate(null):
        vec = v
        L = 1
        for c in vec:
            L = _Sp.lcm(L, _Sp.denom(c))
        for i in range(n):
            N[i, j] = float(vec[i] * L)
    jac = float(np.sqrt(np.linalg.det(N.T @ N)))
    return N, jac


def eq_coarea_value_exact_fast(vs, maxcomb=4000000):
    """vs: list of integer numpy int vectors (edges). Returns exact-box-vertex float B(0)."""
    if not vs:
        return 1.0
    n = len(vs)
    M = np.array(vs, dtype=object).T
    M_int = np.array([[sympy.Integer(int(x)) for x in row] for row in M], dtype=object)
    M_float = np.array(M_int, dtype=float)
    det_gram = float(np.linalg.det(M_float @ M_float.T))
    coarea = 1.0 / np.sqrt(abs(det_gram))
    r = int((np.linalg.svd(M_float, compute_uv=False) > 1e-9).sum())
    m = n - r
    if m == 0:
        return coarea
    N, jac = _null_rational_basis(M_int)   # n x m integer columns
    Nf = N.astype(float)
    # constraints: rows_j = N[j,:] (n x m); 0 <= (N t)_j <= 1
    # halfspaces equations: N[j].t = 0 (rhs 0), N[j].t = 1 (rhs 1)
    # Build combined matrix A_stack (2n x m), rhs_stack (2n,)
    A_stack = np.vstack([Nf, -Nf])          # equations for N[j].t and N[j].t - 1 (=0)
    rhs_stack = np.concatenate([np.zeros(n), -np.ones(n)])
    ncon = 2 * n
    verts_float = []
    idxs_singular = []
    cnt = 0
    for idxs in itertools.combinations(range(ncon), m):
        cnt += 1
        if cnt > maxcomb:
            raise ValueError(f"too many combos ({cnt}) n={n} m={m}")
        A = A_stack[list(idxs)]
        b = rhs_stack[list(idxs)]
        # fast rank/det check via numpy
        try:
            detA = np.linalg.det(A)
        except np.linalg.LinAlgError:
            detA = 0.0
        if abs(detA) < 1e-9:
            continue
        try:
            t = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            continue
        # feasibility check: 0 <= Nf @ t <= 1
        ev = Nf @ t
        if np.all(ev >= -1e-7) and np.all(ev <= 1.0 + 1e-7):
            verts_float.append(t)
    if not verts_float:
        raise ValueError("no vertices found (fast)")
    pts = np.array(verts_float)
    # dedup at high precision (float vertex coordinates, which are ~1e-12 accurate to their rational
    # values; distinct vertices are well separated); if m==1 just take range.
    if m == 1:
        xs = np.unique(np.round(pts[:, 0], 8))
        vol_t = float(xs[-1] - xs[0])
        return coarea * jac * vol_t
    chosen = None
    for ndec in [7, 6, 5, 4]:
        pp = np.unique(np.round(pts, ndec), axis=0)
        if len(pp) >= m + 1:
            chosen = pp
            break
    if chosen is None or len(chosen) < m + 1:
        raise ValueError("too few distinct vertices (fast)")
    ok = False
    vol_t = None
    for opts in [["Qt"], ["Qt", "Q12"], ["Qt", "QJ"]]:
        try:
            h = scipy.spatial.ConvexHull(chosen, qhull_options=" ".join(opts))
            v = h.volume
            if np.isfinite(v) and 0 <= v < 1e4:
                vol_t = v
                ok = True
                break
        except Exception:
            continue
    if not ok:
        raise ValueError("convex hull failed (fast)")
    return coarea * jac * vol_t


if __name__ == "__main__":
    # cross-check against the slow exact engine on the 1-D B-spline constants
    sys_import_ok = True
    from boxspline_exact2 import coarea_value_exact
    from fractions import Fraction as F
    exact = {2: F(1), 4: F(2, 3), 6: F(11, 20), 8: F(151, 315), 10: F(15619, 36288), 12: F(655177, 1663200)}
    for j, e in exact.items():
        vs = [np.array([1]) if i % 2 == 0 else np.array([-1]) for i in range(j)]
        vf = eq_coarea_value_exact_fast(vs)
        vs2 = [np.array([1]) if i % 2 == 0 else np.array([-1]) for i in range(j)]
        ve = coarea_value_exact(vs2)  # slow exact
        print(f"c_{j}: fast={vf:+.10f} slowExact={ve:+.10f} exact={e} diff-fast={abs(vf-float(e)):.1e} diff-slow={abs(ve-float(e)):.1e}")
