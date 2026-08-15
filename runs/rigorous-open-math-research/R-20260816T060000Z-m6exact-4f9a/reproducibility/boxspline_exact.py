#!/usr/bin/env python
"""Exact box-spline (coarea) value for a general edge multigraph, rational reconstruction.

Given a set of directed edge vectors v_e in R^d (from the combined cycle x permutation
multigraph), the integral I = int_{[0,1]^d sym window} prod K(v_e·x)  (after fixing one
integration variable by translation) equals the (n-d)-volume of {M xi=0}∩[-1/2,1/2]^n divided
by sqrt(det(M M^T)), where the columns of M are the edge vectors.  This is a rational box-spline
value at 0.  We compute it in float via vertex enumeration of the polytope, then reconstruct the
exact rational with Fraction(x).limit_denominator() (validated: denominators bounded, spacing
~1/den >> float error).

Validated by reproducing the certified D3/D4/D5 I_pi values and signed sums = 0.
"""
import numpy as np, itertools, scipy.spatial
from fractions import Fraction as F
from boxspline2 import coarea_value


def reconstruct_rational(val, maxden=100000):
    """Reconstruct the exact Fraction of a known-rational box-spline signed-sum from float.
    A signed sum that should vanish (D_k cancellations) comes out as a tiny float residue;
    treat |val| < 1e-4 as exactly 0 (genuine nonzero shape integrals are >= 1/180 ~= 0.0056)."""
    if abs(val) < 1e-4:
        return F(0)
    fr = F(val)
    rc = fr.limit_denominator(maxden)
    err = abs(float(rc) - val)
    if err > max(1e-6 * max(1.0, abs(val)), 1e-8):
        raise ValueError(f"no rational recon for val={val} (rc={rc}, err={err})")
    return rc


def rel_weights(blocks, k):
    """Assign each position a{0..k-1} its block index; blocks list of frozensets.
    Return idx[a] = block index (0..b-1)."""
    bid = {}
    for i, b in enumerate(blocks):
        for e in b:
            bid[e] = i
    return [bid[a] for a in range(k)]


def cycle_edges(blocks, k):
    """edge direction vectors for the k cycle edges between block indices (b-1 dim), pinning last block 0."""
    b = len(blocks)
    if b == 1:
        return []
    idx = rel_weights(blocks, k)
    vs = []
    for a in range(k):
        u = idx[a]
        v = idx[(a + 1) % k]
        e = np.zeros(b - 1)
        if u < b - 1:
            e[u] += 1
        if v < b - 1:
            e[v] -= 1
        vs.append(e)
    return vs


def rho_terms(b):
    """Yield (sign, perm) for S_b terms of the determinant det[K(x_a-x_b)]."""
    for perm in itertools.permutations(range(b)):
        # sign of perm
        p = list(perm)
        seen = [False] * b
        sign = 1
        for i in range(b):
            if not seen[i]:
                j = i
                cnt = 0
                while not seen[j]:
                    seen[j] = True
                    j = p[j]
                    cnt += 1
                if cnt % 2 == 0 and cnt > 0:
                    sign *= -1
        yield sign, perm


def perm_edges(perm, b):
    """edges for permutation (self loops dropped): x_a - x_{perm(a)}, dim (b-1), last block pinned 0."""
    vs = []
    for a in range(b):
        if perm[a] != a:
            e = np.zeros(b - 1)
            if a < b - 1:
                e[a] += 1
            if perm[a] < b - 1:
                e[perm[a]] -= 1
            vs.append(e)
    return vs


def shape_integral_exact(blocks, k):
    """J_sigma = int [prod cycle K(x_{sigma(a)}-x_{sigma(a+1)})] * rho_b, over R^{b-1} rel coords.
    Returns exact Fraction.  rho_b = det[K(x_a-x_b)] = sum_{perm} sign prod K(x_a-x_{perm(a)}).
    Individual coarea terms may be irrational (sqrt); the signed sum J_sigma is rational."""
    b = len(blocks)
    if b == 1:
        return F(1)  # all edges self-loop => K(0)=1 each, rho_1=1
    cyc = cycle_edges(blocks, k)
    total = 0.0
    for sign, perm in rho_terms(b):
        pe = perm_edges(perm, b)
        vs = cyc + pe
        total += sign * coarea_value(vs)
    return reconstruct_rational(total)
