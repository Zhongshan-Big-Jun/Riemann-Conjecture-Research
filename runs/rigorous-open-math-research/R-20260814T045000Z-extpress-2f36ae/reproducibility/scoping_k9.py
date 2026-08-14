"""Fast scoping for k=9 minimum f_9 (evidence only).

Approach: exploit structure. The minimum of F lives where inter-point distances
sit near zeros of w. Use basinhopping + local polish with many structured + RANDOM
starts in a bounded box (sum of gaps limited by pressure bound). Kept lightweight.
"""
import numpy as np
from scipy.optimize import minimize
import math, sys

sqrt2 = math.sqrt(2.0)
k_zero = sqrt2*math.sin(1.0/sqrt2)
def kk(x):
    x=np.asarray(x,float)
    with np.errstate(divide='ignore',invalid='ignore'):
        zl=np.pi*x-1.0/sqrt2; zr=np.pi*x+1.0/sqrt2
        sl=np.where(np.abs(zl)<1e-14,1.0,np.sin(zl)/zl)
        sr=np.where(np.abs(zr)<1e-14,1.0,np.sin(zr)/zr)
    return (sl+sr)/2.0/k_zero

def make_F(k):
    L=k-1
    def F(g):
        g=np.asarray(g,float)
        t=float(np.sum(g))/(500.0*L)
        for span in range(1,k):
            c=2.0/(k-span)
            for i in range(k-span):
                q=float(kk(np.sum(g[i:i+span])))
                t+=c*q*q
        return t
    return F

def scope(k, n_rand, out):
    L=k-1; F=make_F(k)
    rng=np.random.default_rng(2024)
    best=(1e18,None)
    def try_pt(pt):
        nonlocal best
        r=minimize(F,pt,method='L-BFGS-B',bounds=[(0,None)]*L,
                   options={'maxiter':3000,'ftol':1e-15,'gtol':1e-9})
        if r.fun<best[0]:
            best=(r.fun,r.x)
    # structured starts
    structures=[]
    for rep in range(1,L+1):
        # put `rep` tiny gaps and rest larger
        for pos in range(0,L-rep+1):
            for big in np.array([0.9,1.0,1.2,1.5,2.0]):
                g=np.full(L,big); g[pos:pos+rep]=0.001
                structures.append(g)
    # kernel first few zeros for w are near 0.9,1.9,...; try all-equal bands
    for a in np.linspace(0.2,4.0,40):
        structures.append(np.full(L,a))
    for idx,pt in enumerate(structures):
        try_pt(pt)
    # random starts
    for _ in range(n_rand):
        u=np.where(rng.uniform(0,1,L)<0.15, 0.003, rng.uniform(0.3,4.0,L))
        try_pt(u)
    sys.stdout.write(f"{out} k={k}: min ~ {best[0]:.10f}\n"); sys.stdout.flush()
    np.save(f'k{k}_opt.npy', best[1])
    return best

if __name__ == '__main__':
    # k=7 sanity (should give ~0.0038)
    scope(7, 800, "scoping")
    # k=9 critical
    scope(9, 3000, "scoping")
    print("done")
