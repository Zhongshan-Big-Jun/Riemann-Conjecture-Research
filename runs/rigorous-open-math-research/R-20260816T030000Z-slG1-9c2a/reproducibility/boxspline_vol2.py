#!/usr/bin/env python
"""Compute I_pi (box-spline value at 0) via HalfspaceIntersection with a strictly-interior
non-symmetric starting point (small all-ones) to dodge qhull's 'feasible point not clearly
inside' fragility. Validate on k=3 (expect D_3=0) then D_4 (expect 0), D_5 (expect 0)."""
import numpy as np, itertools, scipy.spatial

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

def nullspace(M):
    u,s,vh=np.linalg.svd(M)
    r=(s>1e-9).sum()
    return vh[r:].T  # n x (n-r)

def I_pi(k,perm):
    vs=edge_vectors(k,perm); n=len(vs)
    if n==0: return 1.0
    d=k-1
    M=np.array(vs).T
    coarea=1.0/np.sqrt(np.linalg.det(M@M.T))
    N=nullspace(M); m=N.shape[1]
    A=np.vstack([N,-N]); b=0.5*np.ones(2*n)
    interior=1e-7*np.ones(m)
    try:
        hs=scipy.spatial.HalfspaceIntersection(np.column_stack([A,b]), interior, qhull_options="QJ Qz")
        pts=hs.intersections
        # dedupe points
        pts=np.unique(np.round(pts,12),axis=0)
        if len(pts)<m+1: return None, f"few verts {len(pts)}<{m+1}"
        vol=scipy.spatial.ConvexHull(pts).volume
        return coarea*vol, None
    except Exception as e:
        return None, str(e)[:150]

def perm_sign(perm):
    n=len(perm); seen=[False]*n; sign=1
    for i in range(n):
        if not seen[i]:
            j=i;c=0
            while not seen[j]:
                seen[j]=True;j=perm[j];c+=1
            if c%2==0 and c>0: sign*=-1
    return sign

def run(k):
    perms=list(itertools.permutations(range(k)))
    tot=0.0; nfail=0; vals=[]
    for p in perms:
        v,e=I_pi(k,p)
        if v is None:
            nfail+=1; continue
        sg=perm_sign(list(p)); tot+=sg*v
    print(f"k={k}: D_k={tot:+.10e}  (nfail={nfail})")
    # identity check
    v_id=per[0] if False else I_pi(k,tuple(range(k)))[0]
    print(f"   I_id(k={k}) = {v_id}")

for k in [3,4]:
    run(k)
