#!/usr/bin/env python
"""General D_k via box cross-section volumes (k=3,4,5). 

I_pi = vol_{n-rank}( {xi in [-1/2,1/2]^n : V xi = 0 } ) / sqrt(det(V V^T)),
n=2k edges, V = (k-1) x 2k edge-difference matrix (integer).
D_k = sum_{pi in S_k} sign(pi) I_pi.
Cross-section volume + rational reconstruction.
"""
import numpy as np, json
from itertools import permutations
from collections import defaultdict
from fractions import Fraction
from scipy.spatial import HalfspaceIntersection, ConvexHull

def build_V(pi, k):
    d=k-1
    q=[]
    for a in range(d): q.append(np.eye(d)[a])
    q.append(np.zeros(d)); q=np.array(q)
    edges=[]
    for a in range(k): edges.append((a,(a+1)%k))
    for a in range(k): edges.append((a,pi[a]))
    V=np.zeros((d,len(edges)))
    for j,(u,v) in enumerate(edges): V[:,j]=q[u]-q[v]
    return V

def nullspace_orth(V,tol=1e-8):
    U,S,VT=np.linalg.svd(V); s=S>tol; m=V.shape[1]-sum(s)
    return VT[VT.shape[0]-m:].T

def cross_section_volume(V):
    N=nullspace_orth(V); n,dim=N.shape
    if dim==1:
        # 1D polytope [-1/2,1/2]^n /\ subspace: length = 2*max|...| ... do generically below
        pass
    if dim==0:
        return 1.0,0
    Hs=np.hstack([np.vstack([N,-N]),np.full((2*n,1),-0.5)])
    hs=HalfspaceIntersection(Hs,np.zeros(dim),qhull_options='Qx')
    verts=hs.intersections
    if dim==1:
        return (verts[:,0].max()-verts[:,0].min()), verts.shape[0]
    hull=ConvexHull(verts)
    return hull.volume, verts.shape[0]

def cycle_type(pi):
    n=len(pi);seen=[False]*n;lens=[]
    for i in range(n):
        if not seen[i]:
            j=i;c=0
            while not seen[j]:seen[j]=True;j=pi[j];c+=1
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

def compute(k, denom_max=10**6):
    perms=list(permutations(range(k)))
    per={}
    by=defaultdict(list); bysum=defaultdict(lambda: Fraction(0))
    total=Fraction(0); totalf=0.0
    maxdenom=1
    for pi in perms:
        V=build_V(list(pi),k)
        vol,nv=cross_section_volume(V)
        sdet=float(np.sqrt(np.abs(np.linalg.det(V@V.T))))
        sg=perm_sign(list(pi))
        I=vol/sdet
        rt=Fraction(I).limit_denominator(denom_max)
        maxdenom=max(maxdenom,rt.denominator)
        err=abs(float(rt)-I)
        per[pi]=(sg,vol,sdet,I,rt,nv,err)
        total+=sg*rt; totalf+=sg*I
        ct=cycle_type(list(pi))
        by[ct].append((pi,sg,I,rt)); bysum[ct]+=sg*rt
    return per,by,bysum,total,totalf,maxdenom

def main():
    for k in [3,4,5]:
        denom_max = 10**7 if k==5 else 10**6
        per,by,bysum,total,totalf,maxdenom=compute(k,denom_max)
        print(f"===== D_{k} =====")
        print(f"  total (float) = {totalf:+.10e}")
        print(f"  total (exact rational recon) = {total}, is_zero={total==0}")
        print(f"  max reconstructed denominator = {maxdenom}")
        print(f"  per cycle-type partial sums:")
        nz=0
        for ct in sorted(bysum,key=lambda c:(len(c),c)):
            s=bysum[ct]; cnt=len(by[ct])
            print(f"    type={ct} count={cnt} sum={s}  ~{float(s):+.6f}")
            if s!=0: nz+=1
        print(f"  nonzero cycle-type partial sums: {nz}")
        # validation I_id
        idp=tuple(range(k))
        print(f"  I_{'id'} = {per[idp][4]}  (err {per[idp][6]:.1e})")
        # save
        with open(f"D{k}_exact.json","w") as f:
            json.dump({
                "k":k,"D_float":totalf,"D_exact":str(total),
                "maxdenom":maxdenom,
                "perms":{str(p):[v[0],v[2],str(v[4])] for p,v in per.items()}
            },f)
        print("  saved", f"D{k}_exact.json")
    print("\ndone")

if __name__=="__main__":
    main()
