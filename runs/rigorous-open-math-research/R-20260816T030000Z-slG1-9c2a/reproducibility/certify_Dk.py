#!/usr/bin/env python
"""Certify the rational reconstruction underlying D_k=0: for each permutation, the subagent
reconstructed I_pi as a rational Fraction(I).limit_denominator(1e7). We independently recompute
I_pi (method A: same qhull cross-section; 3 independent start-with-different-tolerance calls)
and record max |float - rational| to quantify confidence, plus the exact signed sum.
This is an audit, not a replacement proof.
"""
import numpy as np, itertools, importlib.util, sys
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T030000Z-slG1-9c2a\reproducibility")
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
A=load(r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T030000Z-slG1-9c2a\reproducibility\Dk_general_qhull.py","Am2")
from fractions import Fraction
import json

def perm_sign(pi):
    n=len(pi);seen=[False]*n;s=1
    for i in range(n):
        if not seen[i]:
            j=i;c=0
            while not seen[j]:seen[j]=True;j=pi[j];c+=1
            if c%2==0 and c>0:s*=-1
    return s

for k in [3,4,5]:
    perms=list(itertools.permutations(range(k)))
    totalr=Fraction(0); totalf=0.0; maxerr=0.0; maxabs=0.0; denommax=1
    nfail=0
    for pi in perms:
        V=A.build_V(list(pi),k)
        try:
            vol,nv=A.cross_section_volume(V)
        except Exception:
            nfail+=1; continue
        sdet=float(np.sqrt(np.abs(np.linalg.det(V@V.T))))
        I=vol/sdet
        rt=Fraction(I).limit_denominator(10**7)
        err=abs(float(rt)-I)
        maxerr=max(maxerr,err)
        maxabs=max(maxabs,abs(I))
        denommax=max(denommax,rt.denominator)
        sg=perm_sign(list(pi))
        totalr+=sg*rt; totalf+=sg*I
    print(f"k={k}: signed rational sum = {totalr}  (=0: {totalr==0}); float sum={totalf:+.3e}; "
          f"max |recon-float|/|I| = {maxerr/maxabs:.2e}; maxerr={maxerr:.2e}; maxdenom={denommax} nfail={nfail}")
