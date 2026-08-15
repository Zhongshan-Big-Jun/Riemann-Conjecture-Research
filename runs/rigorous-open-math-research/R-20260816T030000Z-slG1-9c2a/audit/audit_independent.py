#!/usr/bin/env python
"""Independent audit of the D_k box-spline computation.
Two independent methods for the cross-section volume, plus an independent
numerical check of the coarea identity via a gaussian-smoothed delta.
"""
import numpy as np, itertools, json, sys
from fractions import Fraction
from scipy.spatial import ConvexHull, HalfspaceIntersection, Delaunay

RUNDIR = r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T030000Z-slG1-9c2a\reproducibility"

# ---------------- build V (both self-loop variants) ----------------
def build_V(pi, k, drop_selfloops):
    d = k-1
    q = [np.eye(d)[a] for a in range(d)] + [np.zeros(d)]
    edges = []
    for a in range(k): edges.append((a,(a+1)%k))
    for a in range(k):
        if (not drop_selfloops) or pi[a]!=a:
            edges.append((a,pi[a]))
    V = np.zeros((d,len(edges)))
    for j,(u,v) in enumerate(edges): V[:,j]=q[u]-q[v]
    return V

def nullspace_orth(M):
    u,s,vh=np.linalg.svd(M); r=(s>1e-9).sum()
    return vh[r:].T, r   # columns = nullspace basis

# ---------------- method A: HalfspaceIntersection + ConvexHull (like Dk_general) ---
def vol_halfspace(N):
    n,dim=N.shape
    if dim==0: return 1.0
    hs=np.hstack([np.vstack([N,-N]),np.full((2*n,1),-0.5)])
    inter=HalfspaceIntersection(hs,np.zeros(dim),qhull_options='Qx')
    verts=inter.intersections
    if dim==1: return verts[:,0].max()-verts[:,0].min()
    return ConvexHull(verts).volume

# ---------------- method B: explicit vertex enumeration (like Dk_boxespline) -------
def vertex_enum(N):
    n,m=N.shape
    if m==0: return 1.0
    verts=[np.zeros(m)]  # origin
    for idxs in itertools.combinations(range(n), m):
        Mt=np.array([N[j] for j in idxs])
        if abs(np.linalg.det(Mt))<1e-9: continue
        for sgn in itertools.product([1,-1],repeat=m):
            rhs=0.5*np.array(sgn)
            try: t=np.linalg.solve(Mt,rhs)
            except np.linalg.LinAlgError: continue
            if np.all(np.abs(N@t)<=0.5+1e-7): verts.append(t)
    pts=np.array(verts)
    if m==1: return pts[:,0].max()-pts[:,0].min()
    pp=np.unique(np.round(pts,8),axis=0)
    return ConvexHull(pp,'QJ').volume

def volume_check(pi,k):
    """Return (volA,volB) using the two independent algorithms, self-loop excluded."""
    V=build_V(pi,k,drop_selfloops=True)
    d=k-1
    coarea=1.0/np.sqrt(abs(np.linalg.det(V@V.T)))
    N,r=nullspace_orth(V); m=N.shape[1]
    if m==0: return 1.0,1.0
    volA=vol_halfspace(N); volB=vertex_enum(N)
    return volA*coarea, volB*coarea

def perm_sign(pi):
    n=len(pi);seen=[False]*n;s=1
    for i in range(n):
        if not seen[i]:
            j=i;c=0
            while not seen[j]:seen[j]=True;j=pi[j];c+=1
            if c%2==0 and c>0:s*=-1
    return s

# ---------------- coarea identity: numeric check with gaussian delta ---------------
def coarea_check():
    """Verify int delta^d(M xi) 1_C d xi = vol(slice C∩ker M)/sqrt(det MM^T) numerically."""
    rng=np.random.default_rng(0)
    for trial in range(6):
        d,n=rng.integers(2,5),rng.integers(5,8)
        M=rng.normal(size=(d,n))
        V=Vt=None
        # level set volume via method A
        N,_=nullspace_orth(M); m=N.shape[1]
        if m==0: continue
        vol=vol_halfspace(N)
        formula=vol/np.sqrt(abs(np.linalg.det(M@M.T)))
        # gaussian-smoothed delta integral: int 1_C prod_d gauss_sigma((M xi)_j) dxi, rescaled
        sigma=0.05
        # int_R^d gauss_sigma(w) dw =1 ; 1/sqrt(det M M^T)
        # Monte Carlo over hull? too hard. Use: measure of {|M xi|<=} ...
        # Instead: int_C (1_C)(xi) prod_j gauss of (M xi)_j / proper norm
        # MC sample xi uniform in [-0.5,0.5]^n
        S=400000
        xs=rng.uniform(-0.5,0.5,size=(S,n))
        w=xs@M.T
        kern=np.prod(np.exp(-w**2/(2*sigma**2)),axis=1)/(np.sqrt(2*np.pi)*sigma)**d
        # as sigma->0, kern -> delta^d(w). int_C kern d xi should -> formula.
        mc=0.0
        for _ in range(3):
            xs=rng.uniform(-0.5,0.5,size=(S,n))
            w=xs@M.T
            kern=np.exp(-0.5*np.sum((w/sigma)**2,axis=1))/(np.sqrt(2*np.pi)*sigma)**d
            mc=kern.mean()   # unit uniform density -> mean
            
        print(f"  trial d={d} n={n} m={m}: formula(slice/sqrtdet)={formula:.5f} "
              f"gaussMC@sigma={sigma}: {mc:.5f} (ratio {mc/formula:.3f})")
    return True

if __name__=="__main__":
    print("=== coarea identity numerical sanity ===")
    try: coarea_check()
    except Exception as e: print("coarea_check err",e)
