#!/usr/bin/env python
"""Robust box-spline (Fourier cross-section) volume via explicit vertex enumeration,
for centrally symmetric polytopes P={t in R^m : |(N t)_j|<=1/2 for j=1..n},
N n x m orthonormal columns. For each orbit representative compute volume exactly-ish
(high precision float), then assemble D_k = sum_pi sign(pi) I_pi using the orbit
multiplicities.

Vertex rule: a vertex of P is a point t where m linearly independent halfspaces among
{ (Nt)_j = +1/2 or -1/2 : j=1..n } are active. Enumerate active-index subsets.
"""
import numpy as np, itertools, scipy.spatial
from math import sqrt

def diff_vec(u,v,k):
    e=np.zeros(k-1)
    if u<k-1: e[u]+=1
    if v<k-1: e[v]-=1
    return e

def edge_vectors(k,perm):
    vs=[]
    for a in range(k):
        vs.append(diff_vec(a,(a+1)%k,k))
    for a in range(k):
        if perm[a]!=a:
            vs.append(diff_vec(a,perm[a],k))
    return vs

def nullspace_orth(M):
    u,s,vh=np.linalg.svd(M)
    r=(s>1e-9).sum()
    return vh[r:].T, r   # n x (n-r), rank

def volume_vertices(N):
    """volume of {t: |N t|<=1/2}, N n x m orthonormal columns."""
    n,m=N.shape
    # active constraints: for each j, either (row_j . t) = +1/2 or -1/2, where row = N[j,:]
    # enumerate combinations producing m independent equations
    A_rows=N  # n rows, each length m
    verts=[]
    # choose m distinct indices j and signs
    for idxs in itertools.combinations(range(n), max(1,m)):
        if len(idxs)!=m: continue
        for signs in itertools.product([1,-1],repeat=m):
            Mtx=np.array([A_rows[j] for j in idxs])  # m x m
            if abs(np.linalg.det(Mtx))<1e-10: continue
            rhs=0.5*np.array(signs)
            try:
                t=np.linalg.solve(Mtx,rhs)
            except np.linalg.LinAlgError:
                continue
            # check inside all: |N t| <= 1/2 + tol
            if np.all(np.abs(N@t)<=0.5+1e-9):
                verts.append(t)
    if not verts:
        return None
    # dedupe
    pts=np.unique(np.round(np.array(verts),10),axis=0)
    if m==1:
        xs=sorted(pt[0] for pt in pts)
        if len(xs)<2: return None
        return xs[-1]-xs[0]
    if len(pts)<m+1:
        return 0.0
    hull=scipy.spatial.ConvexHull(pts)
    return hull.volume

def I_pi(k,perm):
    vs=edge_vectors(k,perm); n=len(vs)
    if n==0: return 1.0
    d=k-1
    M=np.array(vs).T
    coarea=1.0/np.sqrt(np.linalg.det(M@M.T))
    N,r=nullspace_orth(M)
    m=N.shape[1]
    if m==0:
        return 1.0*coarea  # 0-dim: value = 1/sqrt(det) ? handle specially
    vol=volume_vertices(N)
    if vol is None:
        return None
    return coarea*vol

def perm_sign(perm):
    n=len(perm);seen=[False]*n;sign=1
    for i in range(n):
        if not seen[i]:
            j=i;c=0
            while not seen[j]:
                seen[j]=True;j=perm[j];c+=1
            if c%2==0 and c>0:sign*=-1
    return sign

def run(k):
    perms=list(itertools.permutations(range(k)))
    tot=0.0;fail=0
    for p in perms:
        v=I_pi(k,p)
        if v is None:
            fail+=1;continue
        tot+=perm_sign(list(p))*v
    print(f"k={k}: D_k={tot:+.10e} fail={fail}")

if __name__=="__main__":
    for k in [3,4]:
        run(k)
