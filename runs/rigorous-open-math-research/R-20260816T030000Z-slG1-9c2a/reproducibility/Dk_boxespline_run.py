#!/usr/bin/env python
"""Run D_k via box-spline vertex enumeration with the robust hull method (Qt, no QJ,
aggressive dedup). Validate on k=3,4 then k=5. If a rep fails, report it instead of skipping.
"""
import numpy as np, itertools, scipy.spatial, sys

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
    if m==0: return 1.0
    A_rows=N; verts=[]
    for idxs in itertools.combinations(range(n), m):
        Mtx=np.array([A_rows[j] for j in idxs])
        if abs(np.linalg.det(Mtx))<1e-8: continue
        for signs in itertools.product([1,-1],repeat=m):
            rhs=0.5*np.array(signs)
            try: t=np.linalg.solve(Mtx,rhs)
            except np.linalg.LinAlgError: continue
            if np.all(np.abs(N@t)<=0.5+1e-7):
                verts.append(t)
    if not verts: return None
    pts=np.array(verts)
    if m==1:
        xs=sorted(p[0] for p in pts)
        return xs[-1]-xs[0]
    # try progressively coarser dedup to stabilize the hull
    for ndec in [9,7,5,4]:
        pp=np.unique(np.round(pts,ndec),axis=0)
        if len(pp)<m+1: continue
        for opts in [["Qt"],["Qt","Q12"],["Qt","QJ"]]:
            try:
                h=scipy.spatial.ConvexHull(pp, qhull_options=" ".join(opts))
                v=h.volume
                if np.isfinite(v) and 0<=v<1e3:
                    return v
            except Exception:
                continue
        # if all hull opts fail at this dedup, try coarser
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

def perm_sign_val(perm):
    n=len(perm);seen=[False]*n;sign=1
    for i in range(n):
        if not seen[i]:
            j=i;c=0
            while not seen[j]:
                seen[j]=True;j=perm[j];c+=1
            if c%2==0 and c>0:sign*=-1
    return sign

def dihedral_orbits(k, perms):
    rot=tuple((i+1)%k for i in range(k)); ref=tuple((-i)%k for i in range(k))
    def conj(g,pi):
        ginv=tuple(g.index(j) for j in range(k)); return tuple(g[pi[ginv[i]]] for i in range(k))
    def orbit(pi):
        seen=set([pi]); frontier=[pi]
        while frontier:
            x=frontier.pop()
            for g in [rot,ref]:
                y=conj(g,x)
                if y not in seen: seen.add(y); frontier.append(y)
        return seen
    seen=set(); reps=[]
    for p in perms:
        if p in seen: continue
        orb=orbit(p); seen|=orb; reps.append((sorted(orb)[0],len(orb)))
    return reps

def run(k):
    perms=list(itertools.permutations(range(k)))
    reps=dihedral_orbits(k,perms)
    total=0.0; fails=[]; detail=[]
    for rep,mul in reps:
        sg=perm_sign_val(rep); val=I_pi(k,rep)
        if val is None:
            fails.append((rep,mul)); continue
        total+=mul*sg*val
        detail.append((rep,mul,val))
    print(f"k={k}: D_k={total:+.10e}  reps={len(reps)} fails={len(fails)}", flush=True)
    if fails:
        for f in fails[:40]: print("   FAIL", f, flush=True)
        # report distinct m-dim among fails
    return total,detail

if __name__=="__main__":
    which=[int(a) for a in sys.argv[1:]] or [3,4,5]
    for k in which:
        run(k); print()
