"""Differential-evolution scoping minimizer for F_{k-1} (evidence only)."""
import numpy as np
from scipy.optimize import differential_evolution, minimize
import math

sqrt2 = math.sqrt(2.0)
k_zero = sqrt2*math.sin(1.0/sqrt2)
def kk(x):
    x = np.asarray(x, float)
    with np.errstate(divide='ignore', invalid='ignore'):
        zl = np.pi*x - 1.0/sqrt2; zr = np.pi*x + 1.0/sqrt2
        sl = np.where(np.abs(zl)<1e-14,1.0,np.sin(zl)/zl)
        sr = np.where(np.abs(zr)<1e-14,1.0,np.sin(zr)/zr)
    return (sl+sr)/2.0/k_zero

def make_F(k):
    L=k-1
    def F(g):
        total=0.0
        for span in range(1,k):
            coef=2.0/(k-span)
            G=np.asarray(g,float)
            for i in range(k-span):
                total+=coef*float(kk(np.sum(G[i:i+span]))**2)
        return total
    return F

def scope(k, base=None):
    L=k-1
    F=make_F(k)
    bounds=[(0.0,16.0)]*L
    result=differential_evolution(F,bounds,seed=11,maxiter=700,popsize=24,tol=1e-10,
                                  polish=True,workers=1)
    best=result.fun
    # many local polishes from DE population
    for pt in result.population[:]:
        r=minimize(F,pt,method='L-BFGS-B',bounds=[(0,None)]*L,
                   options={'maxiter':2000,'ftol':1e-14,'gtol':1e-8})
        if r.fun<best: best=r.fun
    # also multi-seed
    for s in (3,7,19):
        r2=differential_evolution(F,bounds,seed=s,maxiter=400,popsize=20,tol=1e-9,polish=True)
        best=min(best,r2.fun)
    return best

for k in (7,9,11):
    best=scope(k)
    print(f"k={k}: DE min F_{k-1} ~ {best:.10f}   (f_7=0.0038, record-threshold k=9: 0.0038296)")
