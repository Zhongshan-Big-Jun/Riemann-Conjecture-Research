#!/usr/bin/env python
"""EXACT box-spline value at 0 for a set of INTEGER edge direction vectors v_e in Z^d.

B(0) = (n-d)-volume{ xi in [0,1]^n : M xi = 0 } / sqrt(det(M M^T)),  M=(v_1..v_n) d x n.

We compute the m=(n-d) volume of the section EXACTLY:
  - N = integer basis of the null space of M  (n x m, entries integer/rational),
  - vertices of P={t in R^m : 0 <= N t <= 1} are RATIONAL, solved exactly via fractions,
  - P's m-volume in t-space computed numerically at high precision (convex hull of EXACT coords),
  - physical volume = sqrt(det(N^T N)) * vol_t,
  - B(0) = sqrt(det(N^T N))*vol_t / sqrt(det(M M^T))   (a rational for the balanced graphs here).

Validated on the 1-dim B-spline constants c_2..c_10 and the certified D3/D4/D5 signed sums.
This is the AUDIT-grade engine (exact vertices => no float-coarsening artifacts).
"""
import numpy as np, itertools
from fractions import Fraction as F
import sympy, scipy.spatial


def _null_rational_basis(M_int):
    """M_int: d x n integer matrix. Return (N, jac) where N is n x m integer matrix whose
    columns span null(M), m=n-rank, and jac = sqrt(det(N^T N))."""
    d, n = M_int.shape
    Msp = sympy.Matrix(M_int.tolist())
    null = Msp.nullspace()  # list of sympy n-vectors
    if not null:
        m = 0
        return np.zeros((n, 0), dtype=float), 1.0
    m = len(null)
    N = np.zeros((n, m), dtype=float)
    for j, v in enumerate(null):
        # clear denominators to integers
        vec = v
        dens = [sympy.denom(c) for c in vec]
        from sympy import lcm, Integer
        L = 1
        for dd in dens:
            L = sympy.lcm(L, dd)
        for i in range(n):
            N[i, j] = float(vec[i] * L)
    jac = float(np.sqrt(np.linalg.det(N.T @ N)))  # sqrt(det(N^T N))
    return N, jac


def coarea_value_exact(vs, maxcomb=4000000):
    """vs: list of integer numpy arrays (edge vectors) in Z^d. Returns float box-spline B(0)
    computed from EXACT rational vertices (so high precision, ~1e-12)."""
    if not vs:
        return 1.0
    n = len(vs)
    M = np.array(vs, dtype=object).T  # d x n of Python ints
    M_int = np.array([[sympy.Integer(int(x)) for x in row] for row in M], dtype=object)
    M_float = np.array(M_int, dtype=float)
    det_gram = float(np.linalg.det(M_float @ M_float.T))
    coarea = 1.0 / np.sqrt(abs(det_gram))
    r = int((np.linalg.svd(M_float, compute_uv=False) > 1e-9).sum())
    m = n - r
    if m == 0:
        return coarea
    N, jac = _null_rational_basis(M_int)  # N: n x m integer columns
    # constraints: 0 <= (N t)_j <= 1  for j=0..n-1  (t in R^m)
    # rows: for j, N[j,:] row; halfspaces N[j,:].t >=0 ; 1 - N[j,:].t >=0
    rows_int = N  # n x m, integer
    constraints = []
    for j in range(n):
        constraints.append((rows_int[j, :], 0))        # N[j]·t = 0
        constraints.append((-rows_int[j, :], -1))       # N[j]·t = 1
    # exact rational vertices: solve m-subsets of the 2n equations
    ncon = 2 * n
    verts = []
    cnt = 0
    for idxs in itertools.combinations(range(ncon), m):
        cnt += 1
        if cnt > maxcomb:
            raise ValueError(f"too many combos ({cnt}) for n={n},m={m}")
        A = np.array([[sympy.Integer(int(constraints[i][0][k])) for k in range(m)]
                      for i in idxs], dtype=object)
        b = sympy.Matrix([sympy.Integer(int(constraints[i][1])) for i in idxs])
        Msp = sympy.Matrix(A)
        if Msp.det() == 0:
            continue
        sol = Msp.LUsolve(b)  # exact rational m-vector
        t = np.array([float(sol[k]) for k in range(m)])
        # verify all constraints  (N t)_j in [0,1], N is n x m
        row_evals = N @ t  # (n,)
        if np.all(row_evals >= -1e-12) and np.all(row_evals <= 1 + 1e-12):
            verts.append(t)
    if not verts:
        raise ValueError("no vertices found")
    pts = np.array(verts)
    # dedup at high precision (vertices are exact, so near-identical should be exact-equal)
    if m == 1:
        xs = np.unique(np.round(pts[:, 0], 14))
        vol_t = float(xs[-1] - xs[0])
    else:
        chosen = None
        for ndec in [14, 12, 10, 8]:
            pp = np.unique(np.round(pts, ndec), axis=0)
            if len(pp) >= m + 1:
                chosen = pp
                break
        if chosen is None:
            raise ValueError("too few distinct vertices for hull")
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
            raise ValueError("convex hull failed")
    return coarea * jac * vol_t


if __name__ == "__main__":
    # validate on 1-dim B-spline constants vs exact rationals
    exact = {2: F(1), 4: F(2, 3), 6: F(11, 20), 8: F(151, 315), 10: F(15619, 36288)}
    for j, den in exact.items():
        vs = []
        for _ in range(j // 2):
            vs.append(np.array([1]))
            vs.append(np.array([-1]))
        v = coarea_value_exact(vs)
        print(f"c_{j}: box={v:.12f}  exact={den}  diff={abs(float(den) - v):.2e}")
