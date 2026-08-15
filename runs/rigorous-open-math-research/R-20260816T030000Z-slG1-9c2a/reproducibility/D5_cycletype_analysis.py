#!/usr/bin/env python
"""Analyze D_5: group the 120 permutation terms by cycle type of pi and by value,
to identify the cancellation structure. Uses the operator-moment framework: recompute
I_pi to high precision for a chosen box, then group.

We also attempt exact rational recognition of individual I_pi (they are box-spline
values, conjecturally rational) to test whether the signed sum is exactly 0.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
import itertools
from fractions import Fraction

def sinc(t):
    t = np.asarray(t, dtype=float)
    out = np.ones_like(t)
    nz = np.abs(t) > 1e-12
    out[nz] = np.sin(np.pi*t[nz])/(np.pi*t[nz])
    return out

def perm_sign(perm):
    n = len(perm); seen=[False]*n; sign=1
    for i in range(n):
        if not seen[i]:
            j=i; c=0
            while not seen[j]:
                seen[j]=True; j=perm[j]; c+=1
            if c%2==0 and c>0: sign*=-1
    return sign

def cycle_type(perm):
    # returns tuple of sorted cycle lengths
    n=len(perm); seen=[False]*n; lens=[]
    for i in range(n):
        if not seen[i]:
            j=i; c=0
            while not seen[j]:
                seen[j]=True; j=perm[j]; c+=1
            lens.append(c)
    return tuple(sorted(lens))

def I_call(k, perm, X):
    shape = X.shape[:-1]
    P = np.ones(shape)
    for a in range(k):
        b=(a+1)%k; P = P*sinc(X[...,a]-X[...,b])
    for a in range(k):
        P = P*sinc(X[...,a]-X[...,perm[a]])
    return P

def compute(k, R, nperdim):
    perms = list(itertools.permutations(range(k)))
    nodes,w = leggauss(nperdim); x=0.5*R*(nodes+1); wm=0.5*R*w
    g=np.meshgrid(x,x,x,x,indexing='ij'); y4=np.stack(g,axis=-1).reshape(-1,k-1)
    X=np.concatenate([y4,np.zeros(y4.shape[:-1]+(1,))],axis=-1)
    W=np.array([1.0])
    for _ in range(k-1): W=np.multiply.outer(W,wm)
    Wf=W.reshape(-1)
    res={}
    for perm in perms:
        sg=perm_sign(list(perm)); v=float(np.sum(I_call(k,list(perm),X)*Wf))
        res[perm]=(sg,v)
    return res

def main():
    k=5; R=6; n=24
    res=compute(k,R,n)
    total=sum(sg*v for sg,v in res.values())
    print(f"D5 total (R={R}, n={n}) = {total:+.6e}")
    # group by cycle type
    from collections import defaultdict
    bytype=defaultdict(list)
    for p,(sg,v) in res.items():
        bytype[cycle_type(list(p))].append((p,sg,v))
    print("\n== per cycle type: sum of contrib, count, avg I ==")
    for ct,items in sorted(bytype.items()):
        s=sum(sg*v for _,sg,v in items)
        avg=sum(v for _,_,v in items)/len(items)
        print(f"  type={ct} count={len(items)} contrib_sum={s:+.6e} avg_I={avg:+.6e}")
    # rational recognition of a few representative I values
    print("\n== try to recognize representative I as rational (R=6 n=24) ==")
    seen=set()
    for p,(sg,v) in res.items():
        # only examine one per dihedral-orbit via dedup by rounded value
        key=round(v,4)
        if key in seen: continue
        seen.add(key)
        # try continued fraction
        cf=Fraction(v).limit_denominator(200000)
        if abs(float(cf)-v)<1e-6:
            print(f"  pi={p} I={v:+.8f} ~ {cf.numerator}/{cf.denominator} = {float(cf):+.8f} (err {abs(float(cf)-v):.1e})")
        else:
            print(f"  pi={p} I={v:+.8f} (no <1e-6 rational found)")
    print(f"\n total sum = {total:+.8e}")

if __name__=="__main__":
    main()
