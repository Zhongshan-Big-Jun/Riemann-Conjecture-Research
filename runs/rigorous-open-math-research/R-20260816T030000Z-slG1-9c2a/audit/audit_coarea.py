#!/usr/bin/env python
"""Numerical verification of the coarea identity underlying I_pi:
    int_{C=[-1/2,1/2]^n} delta^d(M xi) dxi  =  vol_{n-d}{ C cap ker M } / sqrt(det(MM^T))
for full row-rank M, by smoothing delta with a Gaussian that is a genuine approximant.
We do a change of variable: xi = M^T(MM^T)^{-1} w + N y, so
  int_C g(xi) prod_j d(w_j) dxi = int g(...) 1_{...} /sqrt(det MM^T) (1/w-part)
Actually we verify the *formula* by numerical quadrature of a smoothed case
where C is replaced by a Gaussian envelope so no domain cutoff issues, and compare
both sides EXACTLY in closed form as a function of sigma.
Better: directly check  vol(slice)/sqrt(det) by MC of delta^d smoothing.
"""
import numpy as np, itertools
from scipy.spatial import ConvexHull, HalfspaceIntersection

def nullspace_orth(M):
    u,s,vh=np.linalg.svd(M); r=int((s>1e-10).sum()); return vh[r:].T, r

def vol_slice(M):
    N,_=nullspace_orth(M); n,dim=N.shape
    if dim in (0,): return 1.0
    if dim==1:
        # length of {y:|N y|<=1/2} = max |(1/N_coord)|... for 1-d N is n-vector
        # polytope { y in R : -1/2 <= N_j y <= 1/2 } -> |y|<=1/(2 max|N_j|)
        return float(1.0/np.max(np.abs(N[:,0])))
    hs=np.hstack([np.vstack([N,-N]),np.full((2*n,1),-0.5)])
    inter=HalfspaceIntersection(hs,np.zeros(dim),'Qx'); v=inter.intersections
    return float(ConvexHull(v).volume)

def gauss_delta_MC(M, nSamp, sigma):
    """int_C prod_j gauss_{sigma}((M xi)_j) dxi  (approximates delta^d when sigma small,
    times normalisation so that as sigma->0 it -> int_C delta^d). 
    Note prod_j gauss_sigma(w_j) as a function of w in R^d integrates to 1 over R^d, so
    limit is int_C delta^d(M xi) dxi."""
    n=M.shape[1]
    pdf=lambda w: np.prod(np.exp(-(w/sigma)**2/2)/(np.sqrt(2*np.pi)*sigma),axis=1)
    rng=np.random.default_rng(1)
    val=0.0
    for _ in range(4):
        xs=rng.uniform(-0.5,0.5,size=(nSamp,n))
        w=xs@M.T
        val+= pdf(w).mean()
    return val/4

rng=np.random.default_rng(0)
print("d  n  sigma     MC(delta-smth)     formula(slice/sqrtdet)   ratio")
for trial in range(8):
    d=int(rng.integers(2,4)); n=int(rng.integers(d+1,6))
    M=rng.normal(size=(d,n))
    slice_vol=vol_slice(M)
    formula=slice_vol/np.sqrt(abs(np.linalg.det(M@M.T)))
    for sigma in [0.01]:
        mc=gauss_delta_MC(M,250000,sigma)
        print(f"{d} {n} {sigma:5g}   {mc:.6f}           {formula:.6f}   {mc/formula:.4f}")
