#!/usr/bin/env python
"""High-precision polytope m-volume from float vertex coordinates (which are accurate to ~1e-12),
by summing EXACT simplex m-volumes from a Delaunay triangulation (fraction determinants)."""

import numpy as np
from fractions import Fraction as F
import scipy.spatial


def simplex_vol_exact(pts_frac, m):
    """pts_frac: (m+1, m) array of Fractions. Returns exact Fraction m-volume = |det|/m!."""
    B = [[F(1)] + list(p) for p in pts_frac]
    A = [[F(v) for v in row] for row in B]
    n = m + 1
    det = F(1)
    for col in range(n):
        piv = None
        for r in range(col, n):
            if A[r][col] != 0:
                piv = r
                break
        if piv is None:
            return F(0)
        if piv != col:
            A[col], A[piv] = A[piv], A[col]
            det = -det
        pv = A[col][col]
        for r in range(col + 1, n):
            if A[r][col] == 0:
                continue
            factor = A[r][col] / pv
            for c in range(col, n):
                A[r][c] = A[r][c] - factor * A[col][c]
        det *= pv
    import math
    return abs(det) / math.factorial(m)


def hull_volume_exact(pts):
    """pts: np.array (P, m) float coordinates (accurate ~1e-12). Returns exact Fraction m-volume
    of their convex hull via Delaunay triangulation + exact simplex volumes."""
    P, m = pts.shape
    if m == 1:
        xs = np.unique(np.round(pts[:, 0], 12))
        return F(float(xs[-1] - xs[0]), 1).limit_denominator(10**9)
    # scipy Delaunay for the triangulation (index-based)
    tri = scipy.spatial.Delaunay(pts, qhull_options="QJ")  # QJ to resolve degeneracy generically
    simplices = tri.simplices  # (T, m+1)
    total = F(0)
    for simp in simplices:
        pts_frac = [[F(repr(float(v))) for v in pts[j]] for j in simp]
        total += simplex_vol_exact(pts_frac, m)
    return total


if __name__ == "__main__":
    import numpy as np
    # test: volume of unit cube [0,1]^2 via hull of 4 corners = 1
    pts = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
    print("unit square volume:", hull_volume_exact(pts), "expect 1")
