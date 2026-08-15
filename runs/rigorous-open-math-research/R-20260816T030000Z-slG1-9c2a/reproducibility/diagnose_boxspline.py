#!/usr/bin/env python
"""Diagnose which permutations' box-spline slice polytopes cause HalfspaceIntersection
trouble, and for a few compute the vertex set by enumeration to get the exact volume.
Helps decide the robust strategy for D_5 exact computation."""
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
    return [np.array(w,float) for w in vs]

def nullspace(M):
    u,s,vh=np.linalg.svd(M)
    r=(s>1e-9).sum()
    return vh[r:].T,r

def try_half(k,perm):
    vs=edge_vectors(k,perm); n=len(vs); d=k-1
    if n==0:
        return 1.0,"all-selfloop"
    M=np.array(vs).T
    coarea=1.0/np.sqrt(np.linalg.det(M@M.T))
    N,r=nullspace(M)
    m=N.shape[1]
    # qhull interior
    try:
        A=np.vstack([N,-N]); b=0.5*np.ones(2*n)
        hs=scipy.spatial.HalfspaceIntersection(np.column_stack([A,b]), np.zeros(m), qhull_options="QJ")
        pts=hs.intersections
        if len(pts)<m+1:
            return None,f"few verts {len(pts)}<{m+1}"
        vol=scipy.spatial.ConvexHull(pts).volume
        return coarea*vol,"ok(QJ)"
    except Exception as e:
        return None,f"half fail: {str(e)[:120]}"

if __name__=="__main__":
    for k in [3]:
        for p in itertools.permutations(range(k)):
            v,e=try_half(k,p)
            print(f"k={k} pi={p} I={('None' if v is None else ('%.6f'%v))} [{e}]")
