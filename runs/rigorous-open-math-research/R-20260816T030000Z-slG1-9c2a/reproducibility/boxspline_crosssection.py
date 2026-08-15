#!/usr/bin/env python
"""Validate the box-spline / Fourier cross-section-volume formulation of D_k on the
known cases D_3=0, D_4=0, and probe D_5.

I_pi = vol_{n-d}( { xi in [-1/2,1/2]^n : V_pi xi = 0 } ),
where n = number of edges (2k: k cycle edges + k permutation edges), d = k-1 (relative
vars, fix x_k=0), and V_pi is the d x n matrix of edge-difference direction vectors.

For k=3: d=2, n=6, cross-section is 4-dim. We compute these 6D-box 4D-cross-section
volumes via monte-carlo-free deterministic polytope volume (Qhull) to check D_3=D_4=0
and get a handle on D_5. This uses the Fourier/indicator (box-spline) representation,
which is the correct infinite-volume (no-truncation) value -- unlike box quadrature.
NOTE: the cross-section volume needs care when the cross-section has empty interior in
the constrained coordinates. We instead compute the volume via the equivalent problem:
since the measure is uniform on the box [-1/2,1/2]^n and we want the (n-d)-area of the
slice V xi = 0, we can compute it as a limit / via a dimension-reduction.

Simpler robust approach for the (n-d)-slice: parametrize the nullspace of V (dim n-d),
so xi = N t with t in R^{n-d}, and the integral becomes int over t of the indicator
{ N t in [-1/2,1/2]^n } * |det(...)| dt. Because N t in a box is a linear preimage, the
volume = |det(restriction)| * vol_{n-d}( { t : N t in box } ). But N t in a box = |(N t)_j|<1/2
for all j, a (n-d)-dim polytope in the t-variables. Its (n-d)-volume times the Gram-factor
gives I_pi. We compute this via scipy.spatial.ConvexHull on the (n-d)-dim polytope.
"""
import numpy as np
import itertools
from fractions import Fraction
from math import pi

def perm_sign(perm):
    n=len(perm); seen=[False]*n; sign=1
    for i in range(n):
        if not seen[i]:
            j=i; c=0
            while not seen[j]:
                seen[j]=True; j=perm[j]; c+=1
            if c%2==0 and c>0: sign*=-1
    return sign

def edge_vectors(k, perm):
    """Return list of n direction vectors in R^{d}, d=k-1, after fixing x_k (index k-1) = 0.
    Coordinates: variables are x_0..x_{k-2} in R^{k-1}; direction for edge (u,v) (meaning
    K(x_u - x_v)) = e_u - e_v with e_i the standard basis in R^{k-1} for i in 0..k-2, e_{k-1}=0.
    cycle edges: (a,a+1) for a=0..k-1 mod k. perm edges: (a, perm[a]).
    Return list of n numpy vectors of length k-1."""
    vs=[]
    for a in range(k):
        u=a; v=(a+1)%k
        vs.append(diff_vec(u,v,k))
    for a in range(k):
        u=a; v=perm[a]
        vs.append(diff_vec(u,v,k))
    return [np.array(w,dtype=float) for w in vs]

def diff_vec(u,v,k):
    # direction x_u - x_v in R^{k-1}; coordinate i corresponds to x_i (i<k-1); x_{k-1}=0
    e=np.zeros(k-1)
    if u < k-1: e[u]+=1
    if v < k-1: e[v]-=1
    return e

def nullspace(M):
    # M: d x n. return orthonormal basis of nullspace (n-dim), shape (n, n-rank)
    u,s,vh=np.linalg.svd(M)
    rank=(s>1e-10).sum()
    N=vh[rank:].T  # columns = nullspace vectors, shape (n, n-rank)
    return N

def cross_section_volume(k, perm):
    """I_pi via polytope: { t : N t in [-1/2,1/2]^n } volume times area factor."""
    vs=edge_vectors(k,perm)
    n=len(vs); d=k-1
    M=np.array(vs).T  # d x n
    N=nullspace(M)    # n x (n-d)
    if N.shape[1]==0:
        return None
    # t in R^{n-d}; constraint N t in box -> for each coord j: -1/2 <= (N t)_j <= 1/2
    row=N.T  # (n-d) x n? N is n x (n-d); rows of N.T are (N t)_j coefficients... N t_j = sum_l N[j,l] t_l
    # Build (n-d)-dim polytope given by halfspaces rows: row[j] = vector of coefficients for constraint (Nt)_j.
    # Use scipy HalfspaceIntersection: needs an interior point. Skip for now; compute via ConvexHull on vertices.
    return N, M, n, d

def main():
    # Validate: for k=3, D_3 should be 0.
    k_list=[3,4]
    for k in k_list:
        perms=list(itertools.permutations(range(k)))
        print(f"=== k={k}, d={k-1}, n={2*k}, cross-dim={2*k-(k-1)} ===")
        # For these small k we print the nullspace dims as sanity
        for p in perms[:3]:
            N,M,n,d=cross_section_volume(k,p)
            print(f"  pi={p} n={n} d={d} null-dim={N.shape[1]}")
        print()

if __name__=="__main__":
    main()
