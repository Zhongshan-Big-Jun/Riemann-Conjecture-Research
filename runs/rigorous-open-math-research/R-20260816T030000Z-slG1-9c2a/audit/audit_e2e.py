#!/usr/bin/env python
"""End-to-end independent check for k=3: directly integrate the genuine sinc integral.
Compare to box-spline values. sinc not abs-integrable -> truncation converges
conditionally; we report trend in L to confirm consistency with box-spline value.
Also: verify full signed D5 sum from JSON, and rational reconstruction separation."""
import numpy as np, itertools, json
from scipy.integrate import nquad
from fractions import Fraction

def K(t):
    t=np.asarray(t,float)
    out=np.ones_like(t)
    nz=np.abs(t)>1e-12
    out[nz]=np.sin(np.pi*t[nz])/(np.pi*t[nz])
    return out

def boxspline_Ipi(pi,k):
    # from previous audit module
    import importlib.util
    spec=importlib.util.spec_from_file_location("ar", r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T030000Z-slG1-9c2a\audit\audit_run.py")
    ar=importlib.util.module_from_spec(spec); spec.loader.exec_module(ar)
    pi=tuple(pi)
    V=ar.build_V(pi,k,False); d=k-1
    sdet=float(np.sqrt(abs(np.linalg.det(V@V.T))))
    N,r=ar.nullspace_orth(V); m=N.shape[1]
    vol=ar.vol_halfspace(N) if m>0 else 1.0
    return vol/sdet

def direct_k3(pi, L):
    """I_pi = int_{[-L,L]^2} prod6 sincs dx0 dx1 (x2=0). Returns value."""
    pi=list(pi)
    def f(y0,y1):
        x0=y0; x1=y1; x2=0.0
        c=K(x0-x1)*K(x1-x2)*K(x2-x0)
        p=1.0
        for a in range(3):
            b=pi[a]
            xa=[x0,x1,x2][a]; xb=[x0,x1,x2][b]
            p*=K(xa-xb)
        return float(c*p)
    val,err=nquad(lambda y0,y1: f(y0,y1), [[-L,L],[-L,L]],
                  opts=[{'limit':200},{'limit':200}])
    return val,err

# report box-spline values and their rationals for all k=3 perms
from collections import defaultdict
print("=== k=3: box-spline I_pi & direct-truncation trend (independent route) ===")
for pi in itertools.permutations(range(3)):
    bs=boxspline_Ipi(pi,3)
    rt=Fraction(bs).limit_denominator(1000)
    sg=1 if [0,1,2] in [tuple(range(3))] else None
    print(f"  pi={pi} boxspline={bs:.10f} ~{rt}")

print("\n=== direct sinc quadrature trend (should approach box-spline value) ===")
for pi in [(0,1,2),(1,0,2),(1,2,0)]:
    bs=boxspline_Ipi(pi,3)
    print(f" pi={pi} boxspline={bs:.8f}")
    for L in [6,10,14]:
        v,_=direct_k3(pi,L)
        print(f"   L={L}: direct={v:.8f}")

print("\n=== D5 full signed sum from JSON + separation check ===")
with open(r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T030000Z-slG1-9c2a\reproducibility\D5_exact.json") as f:
    data=json.load(f)
S=Fraction(0); n=0
maxden=1
for pk,(sgfl,sdet,rat) in data["perms"].items():
    pk=tuple(int(x) for x in pk.strip("()").split(",") if x.strip())
    S+=sgfl*Fraction(rat); n+=1
    maxden=max(maxden,Fraction(rat).denominator)
print(f"  {n} perms; signed rational sum = {S} (=0:{S==0}); maxden={maxden}")
# separation: min distance between distinct denom<=180 rationals in the value set
vals=sorted(set(Fraction(v[2]) for v in data['perms'].values()))
gap=min(float(vals[i+1]-vals[i]) for i in range(len(vals)-1))
print(f"  min separation of distinct reconstructed rationals = {gap:.3e}")
print(f"  half-integer-lattice tolerance 1/(2*180^2) = {1/(2*180**2):.3e}")
