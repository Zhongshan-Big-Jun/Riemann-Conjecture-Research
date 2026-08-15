#!/usr/bin/env python
"""Compute I_pi exactly (as box-spline / Fourier cross-section volumes) for k=3,4,5 and
sum D_k = sum_pi sign(pi) I_pi, to confirm D_3=D_4=0 and resolve D_5.

I_pi = vol_{n-d}( { xi in [-1/2,1/2]^n : V_pi xi = 0 } ), n=2k edges, d=k-1.
Via orthonormal nullspace N (n x (n-d)), I_pi = vol_{n-d}( { t in R^{n-d} : Nt in box } ).
This is a full-dimensional centrally-symmetric polytope in R^{n-d} containing 0 in its
interior; we get its vertices via scipy.spatial.HalfspaceIntersection and volume via
Qhull ConvexHull. All I_pi are exact rationals; we report them as floats and recognize
the exact sum.
"""
import numpy as np
import itertools
import scipy.spatial
from fractions import Fraction

def perm_sign(perm):
    n=len(perm); seen=[False]*n; sign=1
    for i in range(n):
        if not seen[i]:
            j=i; c=0
            while not seen[j]:
                seen[j]=True; j=perm[j]; c+=1
            if c%2==0 and c>0: sign*=-1
    return sign

def diff_vec(u,v,k):
    e=np.zeros(k-1)
    if u < k-1: e[u]+=1
    if v < k-1: e[v]-=1
    return e

def edge_vectors(k, perm):
    """Return edge direction vectors (numpy) plus a weight for self-loops.
    Self-loop edges (u,u) contribute factor K(0)=1 (no integration constraint), so they
    are recorded as the constant 1 and NOT added as a direction vector."""
    vs=[]; weight=1.0
    for a in range(k):
        vs.append(diff_vec(a,(a+1)%k,k))
    for a in range(k):
        if perm[a]==a:
            weight*=1.0  # K(0)=1
        else:
            vs.append(diff_vec(a,perm[a],k))
    return vs, weight

def nullspace(M):
    u,s,vh=np.linalg.svd(M)
    rank=(s>1e-9).sum()
    return vh[rank:].T  # n x (n-rank)

def poly_volume(Nt):
    """vol_{m}( { t in R^m : |(N t)_j| <= 1/2 for all j } ), where Nt is the n x m matrix
    (n = #box inequalities, m = intrinsic dimension)."""
    n,m=Nt.shape
    # constraints: (Nt)_j in [-1/2,1/2] -> two halfspaces per row of Nt (each row length m)
    A=np.vstack([Nt, -Nt])   # (2n) x m
    b=0.5*np.ones(2*n)
    interior=np.zeros(m)
    try:
        hs=scipy.spatial.HalfspaceIntersection(np.column_stack([A,b]), interior)
    except Exception as e:
        return None, str(e)
    pts=hs.intersections
    # dedupe
    if len(pts) < m+1:
        return None, "too few vertices"
    hull=scipy.spatial.ConvexHull(pts)
    vol=hull.volume
    return vol, None

def I_pi(k, perm):
    vs,weight=edge_vectors(k,perm)
    n=len(vs); d=k-1
    if n==0:
        # all self-loops: integrand = 1 (all K(0)), no direction -> value 1
        return weight, None
    M=np.array(vs).T
    # coarea factor for the Dirac: I_pi = (intrinsic slice area)/sqrt(det(MM^T))
    try:
        coarea=1.0/np.sqrt(np.linalg.det(M@M.T))
    except Exception as e:
        return None, f"coarea: {e}"
    N=nullspace(M)      # n x (rank-null)
    if N.shape[1]!=max(0,n-d):
        return None, f"null dim {N.shape[1]} != {n-d}"
    # area factor: N orthonormal (from SVD) so the t-volume equals the xi-slice-volume
    vol,err=poly_volume(N)
    if vol is None:
        return None,err
    return weight*coarea*vol, err

def run(k):
    perms=list(itertools.permutations(range(k)))
    total=0.0; nfail=0; checked={}
    for p in perms:
        vol,err=I_pi(k,p)
        if vol is None:
            nfail+=1; continue
        sg=perm_sign(list(p))
        total+=sg*vol
    # validation: identity should be 1
    v_id,err=I_pi(k,tuple(range(k)))
    print(f"=== k={k} (n-d=2k-(k-1)) total D_k = {total:+.12e}  (nfail={nfail})  I_id={v_id}  err_id={err}", flush=True)
    return total

if __name__=="__main__":
    for k in [3,4,5]:
        run(k)
        print()
