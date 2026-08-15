#!/usr/bin/env python
"""Robust box-spline value at 0 for a set of edge direction vectors v_e in R^d.

B(0) = (n-d)-volume{ xi in [0,1]^n : M xi = 0 } / sqrt(det(M M^T)),  M = (v_1 ... v_n) (d x n).

Implementation: xi in Null(M), let N be an ORTHONORMAL n x m basis of Null(M) (m=n-d).
P = { t in R^m : 0 <= N t <= 1 }  (componentwise).  Its m-volume (isometry since N orthonormal)
is computed by enumerating vertices: solve subsets of m active constraints (rows of N at
boundary, rhs in {0,1}) and taking the m-volume convex hull (scipy).  Polyhedra here are
bounded for the connected graphs we use.

Validated: B(0) for edge multiset {+e1,-e1} x j  (1-dim) recovers c_{2j}=int sinc^{2j}:
j=1->c2=1, j=2->c4=2/3, j=3->c6=11/20, j=4->c8, j=5->c10.
"""
import numpy as np, itertools
import scipy.spatial

def coarea_value(vs, maxcomb=None):
    if not vs:
        return 1.0
    n = len(vs)
    M = np.array(vs).astype(float).T  # d x n
    sv = np.linalg.svd(M, compute_uv=False)
    r = int((sv > 1e-9).sum())
    det_gram = np.linalg.det(M @ M.T)
    coarea = 1.0 / np.sqrt(abs(det_gram))
    m = n - r
    if m == 0:
        return coarea  # square; box-spline = 1/sqrt(det MM^T) (density of a square box)
    vh = np.linalg.svd(M)[2]          # n x n
    N = vh[r:].T.astype(float)        # n x m, columns orthonormal (right singular vectors)
    # N already orthonormal (rows of Vh are orthonormal), N^T N = I
    assert np.allclose(N.T @ N, np.eye(m), atol=1e-9), "N not orthonormal"

    rows = np.array([N[j] for j in range(n)])  # constraints (N t)_j in [0,1] -> rows_j
    verts = []
    # enumerate m-subsets of the 2n halfspaces with active rhs in {0,1}
    # halfspaces: rows_j t >= 0  and  1 - rows_j t >= 0
    constraints = []
    for j in range(n):
        constraints.append((rows[j], 0.0))      # N_j . t = 0
        constraints.append((-1.0 * rows[j], -1.0))  # N_j . t = 1  -> N_j.t -1 =0
    ncon = n * 2
    if maxcomb is None:
        maxcomb = 2000000
    cnt = 0
    for idxs in itertools.combinations(range(ncon), m):
        cnt += 1
        if cnt > maxcomb:
            raise ValueError(f"too many combos ({cnt})")
        A = np.array([constraints[i][0] for i in idxs])  # m x m
        b = np.array([constraints[i][1] for i in idxs])
        try:
            t = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            continue
        # verify all constraints satisfied (in t-space)
        lo = rows @ t
        if np.all(lo >= -1e-6) and np.all(lo <= 1.0 + 1e-6):
            verts.append(t)
    if not verts:
        raise ValueError("no vertices found")
    pts = np.array(verts)
    # dedup: keep the FINEST distinct vertex set that still has >= m+1 points.
    if m == 1:
        xs = np.unique(np.round(pts[:, 0], 12))
        vol = float(xs[-1] - xs[0])
    else:
        chosen = None
        for ndec in [12, 10, 9, 8, 7, 6, 5, 4]:
            pp = np.unique(np.round(pts, ndec), axis=0)
            if len(pp) >= m + 1:
                chosen = pp
                break
        if chosen is None:
            raise ValueError(f"too few distinct vertices: {len(pts)} for m={m}")
        ok = False
        vol = None
        for opts in [["Qt"], ["Qt", "Q12"], ["Qt", "QJ"]]:
            try:
                h = scipy.spatial.ConvexHull(chosen, qhull_options=" ".join(opts))
                v = h.volume
                if np.isfinite(v) and 0 <= v < 1e4:
                    vol = v
                    ok = True
                    break
            except Exception:
                continue
        if not ok:
            raise ValueError("convex hull failed")
    return coarea * vol


if __name__ == "__main__":
    import mpmath as mp
    def s(t):
        return mp.sin(mp.pi*t)/(mp.pi*t)
    for j in [1, 2, 3, 4, 5]:
        vs = []
        import numpy as _np
        for _ in range(j):
            vs.append(_np.array([1.0]))
            vs.append(_np.array([-1.0]))
        box = coarea_value(vs)
        # direct high-precision reference
        mp.mp.dps = 30
        ref = mp.quad(lambda t: s(t)**(2*j), [-mp.inf, mp.inf])
        print(f"c_{2*j}: box={box:.10f}  direct={mp.nstr(ref,15)}  diff={abs(box-float(ref)):.2e}")
