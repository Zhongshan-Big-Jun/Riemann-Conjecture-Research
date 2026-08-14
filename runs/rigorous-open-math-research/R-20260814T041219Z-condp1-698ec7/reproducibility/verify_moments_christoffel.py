"""Verify: m_k(1), Lambda_2(0)=5/36, 1-Lam=31/36, and the Christoffel one-sided bound numerically."""
import numpy as np
from fractions import Fraction as Fr

def rat_mat(M):
    return [[Fr(str(x)) for x in row] for row in M]

def rat_inv(Mmat):
    n=len(Mmat); M=[row[:] for row in Mmat]
    aug=[row[:]+[Fr(1) if i==j else Fr(0) for j in range(n)] for i,row in enumerate(M)]
    for col in range(n):
        piv=None
        for r in range(col,n):
            if aug[r][col]!=0: piv=r; break
        assert piv is not None, "singular"
        aug[col],aug[piv]=aug[piv],aug[col]
        pv=aug[col][col]
        aug[col]=[x/pv for x in aug[col]]
        for r in range(n):
            if r!=col and aug[r][col]!=0:
                f=aug[r][col]; aug[r]=[a-f*b for a,b in zip(aug[r],aug[col])]
    return [row[n:] for row in aug]

# Christoffel function Lambda_m(0) for moment sequence with m_0=1, m_1..m_{2m}
def chris(ms, m):
    # moments m_0..m_{2m}; ms[0]=m_0=1, ms[k]=m_k for k<=2m
    n=m+1
    G=[[ms[i+j] for j in range(n)] for i in range(n)]
    Ginv=rat_inv(G)
    Lam= 1/Ginv[0][0]
    return Lam

print("=== Lambda_2(0) for m=(1,3/4,2,13/4) (m_0=1) ===")
ms=[Fr(1),Fr(1),Fr(3,4),Fr(2),Fr(13,4)]  # m_0..m_4
Lam2=chris(ms,2)
print("m_1..m_4 =", [str(x) for x in ms[1:]])
print("Lambda_2(0) =", Lam2, "=", float(Lam2))
print("1 - Lambda_2(0) =", 1-Lam2, "=", float(1-Lam2))
print("expected Lambda_2(0)=5/36, 1-Lam=31/36 :", Lam2==Fr(5,36), (1-Lam2)==Fr(31,36))

print("\n=== Lambda_1(0) (should be 1 - m_1^2/m_2) ===")
Lam1=chris(ms[:3],1)  # m_0,m_1,m_2
print("Lambda_1(0) =", Lam1, " =?", 1-Fr(ms[1]**2*ms[0]//1,ms[2] if False else ms[2]))

# one-sided: what is the maximum possible mu((-inf,0]) over measures with moments, at m=1?
# = s_2 Var/(Var+s1^2) = 1 - s1^2/s2 for s1>0 (Cantelli). This equals Lambda_1(0). Check.
print("\n=== m=1 Cantelli check ===")
s1,s2=Fr(1),Fr(3,4)
print("Cantelli mu((-inf,0]) <= sigma^2/(sigma^2+s1^2) = ", (s2-s1*s1)/s2 if s1>0 else None)
print("Lambda_1(0) =", chris([Fr(1),s1,s2],1))

print("\n=== Verify Christoffel bound numerically: 1-mu((0,inf)) <= Lambda_m(0)? ===")
# Build candidate measures with moments matching m_k, s1>0, maximize negative-index fraction.
# We'll do a simple LP over discrete support points (grid) with numpy/scipy later.
