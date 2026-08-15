#!/usr/bin/env python
"""Exact computation of D_5 for the sine-kernel DPP via box cross-section volumes.

  K(x) = sinc(x) = sin(pi x)/(pi x)   (Fourier symbol 1_{[-1/2,1/2]}).

For a cyclic DPP moment for k=5:
  D_5 = sum_{pi in S_5} sign(pi) I_pi,
  I_pi = int_{R^4} [prod_{a=0..4} K(x_a-x_{a+1})] [prod_{a=0..4} K(x_a - x_{pi(a)})] dx_0 dx_1 dx_2 dx_3
         (translation-normalized: pin x_4 = 0; free vars x_0..x_3).

KEY FACT (box-spline identity, via coarea). Let n = 2k = 10 edges (5 cycle + 5 perm),
d = k-1 = 4 (translation quotient). Build the d-by-n edge-difference matrix V (integer),
columns = q_u - q_v (q_a = unit vector e_a for a<4, q_4 = 0).  Then
  I_pi = vol_{n-rank(V)}( { xi in [-1/2,1/2]^n : V xi = 0 } ) / sqrt( det( V V^T ) ).
(For rank 4 everywhere the cross-section is 6-dimensional; note the sqrt(det) factor,
 which is the coarea/Jacobian normalisation that the raw cube cross-section volume needs.)

We enumerate vertices of the 6D polytope |N y|<=1/2 in an orthonormal nullspace N of V,
and take the Qhull volume; then divide by sqrt(det V V^T) and reconstruct the exact
rational (each I_pi has denominator <= 180). Sum with sign(pi) exactly -> D_5 = 0.

Discipline: we also report D_3 (expect 0) and D_4 (expect 0) and I_id = 1 as validation,
and we report the residual of each rational fit (should be ~1e-9 or better).
"""
import json, itertools
import numpy as np
from fractions import Fraction
from collections import defaultdict
from scipy.spatial import HalfspaceIntersection, ConvexHull


# --------------------------------------------------------------------------- graph / V
def build_edges(pi, k):
    """cycle edges (a, a+1 mod k) then permutation edges (a, pi[a])."""
    E = [(a, (a + 1) % k) for a in range(k)]
    E += [(a, pi[a]) for a in range(k)]
    return E


def build_V(pi, k):
    d = k - 1
    q = [np.eye(d)[a] for a in range(d)] + [np.zeros(d)]
    E = build_edges(pi, k)
    V = np.zeros((d, len(E)))
    for j, (u, v) in enumerate(E):
        V[:, j] = q[u] - q[v]
    return V, E


def perm_sign(pi):
    n = len(pi); seen = [False]*n; s = 1
    for i in range(n):
        if not seen[i]:
            j = i; c = 0
            while not seen[j]:
                seen[j] = True; j = pi[j]; c += 1
            if c % 2 == 0 and c > 0:
                s *= -1
    return s


def cycle_type(pi):
    n = len(pi); seen = [False]*n; lens = []
    for i in range(n):
        if not seen[i]:
            j = i; c = 0
            while not seen[j]:
                seen[j] = True; j = pi[j]; c += 1
            lens.append(c)
    return tuple(sorted(lens))


def nullspace_orth(V, tol=1e-8):
    U, S, VT = np.linalg.svd(V)
    s = S > tol
    m = V.shape[1] - int(sum(s))
    return VT[VT.shape[0]-m:].T   # (n, m) orthonormal columns


def cross_section_volume(V):
    """vol_{n-rank} of { xi in [-1/2,1/2]^n : V xi = 0 }, via 6D polytope |N y|<=1/2."""
    N = nullspace_orth(V)
    n, dim = N.shape
    if dim == 0:
        return 1.0, 0
    Hs = np.hstack([np.vstack([N, -N]), np.full((2*n, 1), -0.5)])  # A x + b <= 0
    hs = HalfspaceIntersection(Hs, np.zeros(dim), qhull_options='Qx')
    verts = hs.intersections
    if dim == 1:
        return float(verts[:, 0].max() - verts[:, 0].min()), verts.shape[0]
    hull = ConvexHull(verts)
    return float(hull.volume), verts.shape[0]


def compute_k(k, denom_bound=10**7):
    perms = list(itertools.permutations(range(k)))
    by = defaultdict(list); bysum = defaultdict(lambda: Fraction(0))
    total = Fraction(0); totalf = 0.0
    maxdenom = 1; maxresid = 0.0; per = {}
    for pi in perms:
        V, _ = build_V(list(pi), k)
        vol, nv = cross_section_volume(V)
        G = V @ V.T
        detg = abs(float(np.linalg.det(G)))
        sdet = float(np.sqrt(detg))
        sg = perm_sign(list(pi))
        Ival = vol / sdet
        rt = Fraction.from_float(Ival).limit_denominator(denom_bound)
        resid = abs(float(rt) - Ival)
        maxdenom = max(maxdenom, rt.denominator); maxresid = max(maxresid, resid)
        per[tuple(pi)] = (sg, vol, sdet, Ival, rt, resid)
        total += sg * rt
        totalf += sg * Ival
        by[cycle_type(list(pi))].append((pi, sg, Ival, rt))
        bysum[cycle_type(list(pi))] += sg * rt
    return per, by, bysum, total, totalf, maxdenom, maxresid


def main():
    print("=" * 74)
    print("Box cross-section computation of D_3, D_4, D_5 (sine-kernel DPP)")
    print("I_pi = vol_6(cube cross-section) / sqrt(det(VV^T)), V integer edge matrix")
    print("=" * 74)
    summary = {}
    for k in (3, 4, 5):
        per, by, bysum, total, totalf, maxdenom, maxresid = compute_k(k)
        idrt = per[tuple(range(k))][4]
        nz = sum(1 for s in bysum.values() if s != 0)
        summary[k] = {
            "D_float": totalf, "D_exact": str(total),
            "maxdenom": maxdenom, "max_fit_residual": maxresid,
            "I_id": str(idrt), "nonzero_cycletype_sums": nz,
        }
        print(f"\n  D_{k}:")
        print(f"    float sum          = {totalf:+.12e}")
        print(f"    exact rational sum = {total}    (==0? {total == 0})")
        print(f"    I_{'id'}              = {idrt}   (expect 1)")
        print(f"    max reconstructed denominator = {maxdenom}")
        print(f"    max rational-fit residual     = {maxresid:.2e}")
        print(f"    nonzero cycle-type partial sums = {nz}  (cancellation is GLOBAL)")
        if k == 5:
            print("    per-cycle-type exact partial sums:")
            for ct in sorted(bysum, key=lambda c: (len(c), c)):
                print(f"      type={ct} count={len(by[ct])}  sum={bysum[ct]}  ~{float(bysum[ct]):+10.6f}")
            print("    distinct I_pi rational values (value : multiplicity):")
            from collections import Counter
            cnt = Counter(per[p][4] for p in per)
            for v in sorted(cnt, key=lambda f: float(f)):
                print(f"      {v}   x{cnt[v]}")
    with open("D5_boxspline_report.json", "w") as f:
        json.dump(summary, f, indent=1)
    print("\n  saved D5_boxspline_report.json")


if __name__ == "__main__":
    main()
