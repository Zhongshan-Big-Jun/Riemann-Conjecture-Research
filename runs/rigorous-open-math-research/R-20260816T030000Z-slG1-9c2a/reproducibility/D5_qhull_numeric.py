#!/usr/bin/env python
"""Compute D_5 numerically from the box cross-section volumes:

  I_pi = vol_6({ t in [-1/2,1/2]^10 : V t = 0 }) / sqrt(det(V V^T)),   V = 4x10 integer.

where I_pi = integral of the two K-cycles (product of 10 sinc factors) over the 4 free
relative variables. D_5 = sum_{pi in S5} sign(pi) I_pi.

Cross-section volume via Qhull: enumerate vertices of the 6D polytope |N y|<=1/2 in the
nullspace of V (N has orthonormal columns), then ConvexHull volume.
"""
import numpy as np
from itertools import permutations
from collections import defaultdict
from scipy.spatial import HalfspaceIntersection, ConvexHull

def build_V(pi, k=5):
    kk=k-1; q=[]
    for a in range(kk): q.append(np.eye(kk)[a])
    q.append(np.zeros(kk)); q=np.array(q)
    edges=[]
    for a in range(k): edges.append((a,(a+1)%k))
    for a in range(k): edges.append((a,pi[a]))
    V=np.zeros((kk,len(edges)))
    for j,(u,v) in enumerate(edges): V[:,j]=q[u]-q[v]
    return V

def nullspace_orth(V,tol=1e-8):
    U,S,VT=np.linalg.svd(V); s=S>tol; m=V.shape[1]-sum(s)
    return VT[VT.shape[0]-m:].T  # (n,m) orthonormal cols

def cross_section_volume(V):
    N=nullspace_orth(V)
    n,k=N.shape
    Hs=np.hstack([np.vstack([N,-N]),np.full((2*n,1),-0.5)])  # A x + b <= 0
    hs=HalfspaceIntersection(Hs,np.zeros(k),qhull_options='Qx')
    verts=hs.intersections
    hull=ConvexHull(verts)
    return hull.volume, verts.shape[0]

def cycle_type(pi):
    n=len(pi); seen=[False]*n; lens=[]
    for i in range(n):
        if not seen[i]:
            j=i;c=0
            while not seen[j]: seen[j]=True;j=pi[j];c+=1
            lens.append(c)
    return tuple(sorted(lens))
def perm_sign(pi):
    n=len(pi);seen=[False]*n;s=1
    for i in range(n):
        if not seen[i]:
            j=i;c=0
            while not seen[j]:seen[j]=True;j=pi[j];c+=1
            if c%2==0 and c>0:s*=-1
    return s

def main():
    perms=list(permutations(range(5)))
    res={}
    total=0.0
    for pi in perms:
        V=build_V(list(pi))
        vol,nv=cross_section_volume(V)
        detg=abs(np.linalg.det(V@V.T))
        sg=perm_sign(list(pi))
        I=vol/np.sqrt(detg)
        res[pi]=(sg,vol,np.sqrt(detg),I,nv)
        total+=sg*I
    print(f"total D5 = {total:+.10e}\n")
    bytype=defaultdict(list)
    for pi,(sg,vol,sdet,I,nv) in res.items():
        bytype[cycle_type(list(pi))].append((pi,sg,vol,sdet,I,nv))
    print("== per cycle type: count, sum(sign*I), list of (I, sqrtdet, nverts) ==")
    for ct in sorted(bytype,key=lambda c:(len(c),c)):
        items=bytype[ct]
        s=sum(sg*I for _,sg,_,_,I,_ in items)
        print(f" type={ct} count={len(items)} sum_sgn_I={s:+.8f}")
        for pi,sg,vol,sdet,I,nv in sorted(items,key=lambda t:t[4]):
            print(f"   pi={pi} sign={sg:+d} I={I:+.10f} sqrtdet={sdet:.5f} nverts={nv}")
    # save
    import json
    out={str(pi):[sg,vol,sdet,I,nv] for pi,(sg,vol,sdet,I,nv) in res.items()}
    with open("D5_qhull_res.json","w") as f: json.dump({"D5":total,"perms":out},f)
    print("\nsaved D5_qhull_res.json, D5=",total)

if __name__=="__main__":
    main()
