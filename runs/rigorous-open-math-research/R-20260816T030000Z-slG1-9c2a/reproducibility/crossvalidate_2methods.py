#!/usr/bin/env python
"""Cross-validate I_pi between two independent box-spline formulations:
(A) subagent's Dk_general_qhull.build_V (full V incl. self-loop zero columns, HalfspaceIntersection)
(B) this run's Dk_boxespline_run coarea (translation-reduced, self-loops dropped, vertex-enum hull).
Compare I_pi for k=3,4,5 and D_k totals.
"""
import numpy as np, sys, itertools
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T030000Z-slG1-9c2a\reproducibility")
import importlib.util

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

A=load(r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T030000Z-slG1-9c2a\reproducibility\Dk_general_qhull.py","Amod")
# B: reproduce coarea I_pi from Dk_boxespline_run.py
B=load(r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T030000Z-slG1-9c2a\reproducibility\Dk_boxespline_run.py","Bmod")

def methodA(k,pi):
    V=A.build_V(list(pi),k)
    vol,nv=A.cross_section_volume(V)
    sdet=float(np.sqrt(np.abs(np.linalg.det(V@V.T))))
    return vol/sdet

for k in [3,4,5]:
    print(f"== k={k} ==")
    np.random.seed(0)
    perms=list(itertools.permutations(range(k)))
    import random; random.seed(1); sample=random.sample(perms,min(8,len(perms)))
    def psi_val(perm):
        n=len(perm);seen=[False]*n;s=1
        for i in range(n):
            if not seen[i]:
                j=i;c=0
                while not seen[j]:seen[j]=True;j=perm[j];c+=1
                if c%2==0 and c>0:s*=-1
        return s
    totA=0;totB=0;bad=0
    for p in itertools.permutations(range(k)):
        if k==5: break  # only sample for k=5 to save time
    for p in sample:
        a=methodA(k,p); b=B.I_pi(k,p)
        totA+=psi_val(p)*a; totB+=psi_val(p)*b
        tag="OK " if (b is not None and abs(a-b)<1e-6*(1+abs(a))) else "MISMATCH"
        if b is None or abs(a-b)>=1e-6*(1+abs(a)): bad+=1
        print(f"  pi={p}  A={a:+.8f}  B={('None' if b is None else '%.8f'%b)}  {tag}")
    print(f"  (sampled A-total over sample={totA:+.6e}, B-total={totB:+.6e}, mismatches={bad})")
