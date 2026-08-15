#!/usr/bin/env python
"""Compute D_5 exactly via box-spline vertex enumeration, using dihedral-orbit reduction
to avoid recomputing equivalent I_pi. Also compute D_3, D_4 for cross-check.
"""
import numpy as np, itertools, scipy.spatial

def diff_vec(u,v,k):
    e=np.zeros(k-1)
    if u<k-1:e[u]+=1
    if v<k-1:e[v]-=1
    return e

def edge_vectors(k,perm):
    vs=[]
    for a in range(k): vs.append(diff_vec(a,(a+1)%k,k))
    for a in range(k):
        if perm[a]!=a: vs.append(diff_vec(a,perm[a],k))
    return vs

def nullspace_orth(M):
    u,s,vh=np.linalg.svd(M); r=(s>1e-9).sum()
    return vh[r:].T, r

def volume_vertices(N):
    n,m=N.shape
    A_rows=N; verts=[]
    if m==0:
        return 1.0
    for idxs in itertools.combinations(range(n), m):
        for signs in itertools.product([1,-1],repeat=m):
            Mtx=np.array([A_rows[j] for j in idxs])
            if abs(np.linalg.det(Mtx))<1e-10: continue
            rhs=0.5*np.array(signs)
            try: t=np.linalg.solve(Mtx,rhs)
            except np.linalg.LinAlgError: continue
            if np.all(np.abs(N@t)<=0.5+1e-9):
                verts.append(t)
    if not verts: return None
    pts=np.unique(np.round(np.array(verts),7),axis=0)
    if m==1:
        xs=sorted(p[0] for p in pts)
        return xs[-1]-xs[0]
    if len(pts)<m+1: return 0.0
    try:
        hull=scipy.spatial.ConvexHull(pts, qhull_options="QJ Qz")
        vol=hull.volume
        if vol<0 or not np.isfinite(vol) or vol>10: 
            return None
        return vol
    except Exception as e:
        return None

def I_pi(k,perm):
    vs=edge_vectors(k,perm); n=len(vs)
    if n==0: return 1.0
    d=k-1; M=np.array(vs).T
    coarea=1.0/np.sqrt(np.linalg.det(M@M.T))
    N,r=nullspace_orth(M); m=N.shape[1]
    vol=volume_vertices(N)
    if vol is None: return None
    return coarea*vol

def compose(f,g):
    return tuple(g[f[i]] for i in range(len(f)))

def dihedral_orbits(k, perms):
    # dihedral group of the labeled k-cycle: rotation r: a->a+1, reflection s: a->-a (both mod k)
    rot=tuple((i+1)%k for i in range(k))   # as permutation on labels
    ref=tuple((-i)%k for i in range(k))
    def conj(g,pi):
        # g pi g^{-1} : (i) -> g(pi(g^{-1}(i)))
        ginv=tuple(g.index(j) for j in range(k))
        return tuple(g[pi[ginv[i]]] for i in range(k))
    def orbit(pi):
        seen=set([pi]); frontier=[pi]
        while frontier:
            x=frontier.pop()
            for g in [rot,ref]:
                y=conj(g,x)
                if y not in seen:
                    seen.add(y); frontier.append(y)
        return seen
    seen=set(); reps=[]
    for p in perms:
        if p in seen: continue
        orb=orbit(p)
        seen|=orb
        reps.append((sorted(orb)[0], len(orb)))
    return reps

def run(k):
    perms=list(itertools.permutations(range(k)))
    reps=dihedral_orbits(k,perms)
    total=0.0; repdetail=[]
    for rep,mul in reps:
        sg=perm_sign_val(rep)
        val=I_pi(k,rep)
        if val is None:
            repdetail.append((rep,mul,'FAIL')); continue
        total+=mul*sg*val
        repdetail.append((rep,mul,val))
    print(f"k={k}: D_k={total:+.10e}  ({len(reps)} orbit reps)")
    return total,repdetail

def perm_sign_val(perm):
    n=len(perm);seen=[False]*n;sign=1
    for i in range(n):
        if not seen[i]:
            j=i;c=0
            while not seen[j]:
                seen[j]=True;j=perm[j];c+=1
            if c%2==0 and c>0:sign*=-1
    return sign

if __name__=="__main__":
    for k in [3,4,5]:
        t,d=run(k); print()
