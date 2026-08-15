#!/usr/bin/env python
"""Coarea box-spline value with EXACT polytope volume (Delaunay + exact simplex determinants),
giving ~1e-10 accurate values even for high-dim sections where float qhull hulls were noisy.
This is the AUDIT-grade engine for the m_5 shape integrals."""

import numpy as np, itertools
import scipy.spatial
from exact_volume import hull_volume_exact


def coarea_value_hp(vs, maxcomb=600000):
    """vs: list of float numpy arrays (edge vectors) in R^d. Returns float B(0) accurate ~1e-10."""
    if not vs:
        return 1.0
    n = len(vs)
    M = np.array(vs).astype(float).T
    sv = np.linalg.svd(M, compute_uv=False)
    r = int((sv > 1e-9).sum())
    det_gram = np.linalg.det(M @ M.T)
    coarea = 1.0 / np.sqrt(abs(det_gram))
    m = n - r
    if m == 0:
        return coarea
    vh = np.linalg.svd(M)[2]
    N = vh[r:].T.astype(float)   # n x m orthonormal null basis
    assert np.allclose(N.T @ N, np.eye(m), atol=1e-8), "N not orthonormal"
    # vertices of P={t in R^m : 0 <= N t <= 1}
    rows = np.array([N[j] for j in range(n)])
    constraints = []
    for j in range(n):
        constraints.append((rows[j], 0.0))
        constraints.append((-1.0 * rows[j], -1.0))
    verts = []
    cnt = 0
    for idxs in itertools.combinations(range(2 * n), m):
        cnt += 1
        if cnt > maxcomb:
            raise ValueError(f"too many combos ({cnt})")
        A = np.array([constraints[i][0] for i in idxs])
        b = np.array([constraints[i][1] for i in idxs])
        try:
            t = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            continue
        ev = rows @ t
        if np.all(ev >= -1e-9) and np.all(ev <= 1 + 1e-9):
            verts.append(t)
    if not verts:
        raise ValueError("no vertices")
    pts = np.array(verts)
    # dedup
    if m == 1:
        xs = np.unique(np.round(pts[:, 0], 12))
        vol_t = float(xs[-1] - xs[0])
    else:
        chosen = None
        for ndec in [12, 10, 8, 6]:
            pp = np.unique(np.round(pts, ndec), axis=0)
            if len(pp) >= m + 1:
                chosen = pp
                break
        if chosen is None:
            raise ValueError("too few vertices")
        vol_t = float(hull_volume_exact(chosen))
    return coarea * vol_t
