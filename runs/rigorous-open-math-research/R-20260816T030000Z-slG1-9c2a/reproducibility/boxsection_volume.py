#!/usr/bin/env python
"""Compute the 6D central box cross-section volume I_pi via vertex enumeration +
Qhull volume, in the 6D nullspace of V.

P = { y in R^6 : |(N y)_i| <= 1/2, i=1..10 }, N = orthonormal 10x6 nullspace basis.
vol_y(P) = vol (in xi space) = I_pi.
Test: identity permutation should give I=1.
"""
import numpy as np
from itertools import permutations

def build_V(pi, k=5):
    kk=k-1
    q=[]
    for a in range(kk):
        q.append(np.eye(kk)[a])
    q.append(np.zeros(kk))
    q=np.array(q)  # (k, kk)
    edges=[]
    for a in range(k):
        edges.append((a,(a+1)%k))
    for a in range(k):
        edges.append((a,pi[a]))
    n=len(edges)
    d=kk
    V=np.zeros((d,n))
    for j,(u,v) in enumerate(edges):
        V[:,j]=q[u]-q[v]
    return V

def nullspace(V, tol=1e-9):
    U,S,VT=np.linalg.svd(V)
    s=(S>tol)
    m=V.shape[1]-sum(s)
    N=VT[VT.shape[0]-m:].T  # (n, m) orthonormal columns
    return N

def volume_qhull(V):
    """Return volume of {|N y|<=1/2} where N=nullspace(V), via ConvexHull/Delaunay."""
    from scipy.spatial import HalfspaceIntersection, ConvexHull, Delaunay
    N=nullspace(V)
    n,k=N.shape  # (10, 6), N rows are 6-vectors
    # constraint |N_i.y| <= 1/2  <=>  -N_i.y + 0.5 >= 0  and  +N_i.y + 0.5 >= 0
    # scipy halfspace convention: A.x + b >= 0, halfspaces = [A b]
    Hs=np.hstack([np.vstack([-N, N]), np.full((2*n,1),0.5)])  # (20,7)
    # interior point: y=0 is *on* all boundaries (p=0 has |Ny|=0 <= 1/2, but on boundary?)
    # 0 is strictly interior (|N*0|=0 < 1/2), so interior feasible.
    interior=np.zeros(k)
    hs=HalfspaceIntersection(Hs, interior)
    verts=hs.intersections  # (nv,6)
    # volume via ConvexHull (needs enough points for full-dim)
    hull=ConvexHull(verts, incremental=False)
    return hull.volume, verts.shape[0]

def main():
    id_pi=tuple(range(5))
    V=build_V(list(id_pi))
    N=nullspace(V)
    print("id: N shape",N.shape)
    try:
        vol,nv=volume_qhull(V)
        print(f"id: volume={vol} (expect ~1), n_vertices={nv}")
    except Exception as e:
        import traceback; traceback.print_exc()

if __name__=="__main__":
    main()
