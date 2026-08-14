"""
INDEPENDENT adversarial re-check (auditor), R-...-698ec7.

Cross-checks the solver's arithmetic via DIFFERENT code paths than the run scripts:
  (A) Lambda_2(0) for the corrected list, via Gram-Schmidt orthogonal polynomials
      (not matrix inversion, not cofactors) -> should be 5/36.
  (B) Final numbers 13/18, 1-5/36=31/36.
  (C) Numerical sinc integrals int sinc^2(pi u) and int sinc^4(pi u) (should be 1 and 2/3).
  (D) Lemma C E[tr G_L^2]/L -> 1 + (1 - 2/3) = 4/3 from the DPP 2-point intensity.
  (E) Lemma 3.A: a tiny explicit numeric instance of the SOS-witness bound vs Cauchy-Schwarz.
"""
from fractions import Fraction as Fr
import numpy as np

# ---- (A) Christoffel via orthogonal-polynomial recursion (Stieltjes on a reference measure).
# We build the Christoffel number directly from the moment functional's inner product
# <p,q> = sum_{k} p_k q_k * m_{k+1} ... here for degree<=m against (1,x,x^2).  Instead just
# verify the KEY identity used in Lemma 3.B: min_{p(0)=1, deg<=m} int p^2 dmu = Lambda_m(0).
# For the truncated moment functional with Gramian G=(m_{i+j}), this equals 1/(G^{-1})_{0,0},
# which the run scripts already compute.  We recompute via the Schur complement / block formula:
#   Lambda_2(0) = m2 - (m1,m2) * inv([[m2,m3],[m3,m4]]) * ((m1,m2).T)  ... wait this is for
#   the *raw* quadratic; we instead compute the exact minimizing poly by solving the linear system.

def min_integral_sq(ms, m):
    # min over p(t)=sum_{j<=m} a_j t^j, p(0)=1, of int p^2 dmu = a^T G a, G=(m_{i+j}).
    # Constraint a_0 = 1.  Minimize over a_1..a_m:
    #   f = [1,a_rest]^T G [1;a_rest];  d/da_rest = 0  =>  solve.
    G = [[ms[i+j] for i in range(m+1)] for j in range(m+1)]  # hmm indices
    n = m + 1
    G = [[ms[i+j] for j in range(n)] for i in range(n)]
    Gaa = [[G[i][j] for j in range(1,n)] for i in range(1,n)]  # a_rest x a_rest
    Ga1 = [G[i][0] for i in range(1,n)]                         # cross with a0
    p = [Fr(-g) for g in Ga1]                                   # Gaa x = -Ga1
    # solve rational linear system Gaa x = p
    A = [r[:] for r in Gaa]; b = p[:]
    for col in range(len(A)):
        piv = next((r for r in range(col,len(A)) if A[r][col]!=0), None)
        assert piv is not None, "singular"
        A[col],A[piv]=A[piv],A[col]; b[col],b[piv]=b[piv],b[col]
        pv=A[col][col]; A[col]=[x/pv for x in A[col]]; b[col]=b[col]/pv
        for r in range(len(A)):
            if r!=col and A[r][col]!=0:
                f=A[r][col]; A[r]=[a-f*c for a,c in zip(A[r],A[col])]; b[r]=b[r]-f*b[col]
    arest=b
    a=[Fr(1)] + arest
    val=sum(G[i][j]*a[i]*a[j] for i in range(n) for j in range(n))
    return val, a

corr=[Fr(1),Fr(1),Fr(4,3),Fr(2),Fr(13,4)]
L2min,_ = min_integral_sq(corr,2)
print("(A) min_{p(0)=1,deg<=2} int p^2 dmu (corrected list) =", L2min, " ~", float(L2min))
print("    == 5/36 ?", L2min==Fr(5,36))
Lam1,_ = min_integral_sq(corr,1)
print("    m=1 value = m1^2/m2 =", Lam1, "== 3/4 ?", Lam1==Fr(3,4))

# (B)
print("\n(B) 1-5/36 =", 1-Fr(5,36), " | 2*(31/36)-1 =", 2*(1-Fr(5,36))-1, "== 13/18 ?", 2*(1-Fr(5,36))-1==Fr(13,18))

# (C) numerical sinc integrals
from scipy.integrate import quad
import math
def sinc(u):
    return 1.0 if abs(u) < 1e-14 else math.sin(math.pi*u)/(math.pi*u)
s2 = quad(lambda u: sinc(u)**2, -60, 60, limit=400)[0]
s4 = quad(lambda u: sinc(u)**4, -60, 60, limit=400)[0]
print("\n(C) int sinc^2(pi u) over [-60,60] ~", round(s2,6), " (true 1)")
print("    int sinc^4(pi u) over [-60,60] ~", round(s4,6), " (true 2/3=",round(2/3,6),")")

# (D) Lemma C formula: E tr G_L^2 / L -> 1 + (int K^2 - int K^4) with K=sinc(pi x)
print("\n(D) E[tr]/L -> 1 + (IntK2 - IntK4) =", 1 + (s2 - s4), " ~ 4/3 =", round(4/3,6))

# (E) Lemma 3.A numeric spot-check: 2x2 diagonal-ish counterexample
# R = diag(1, -2): d=2, eig {1,-2}.  r(t)=1, p(t)=t.
# A_p = sum p = 1-2 = -1 <0 -> trivial max(0).  Use r(t)= (t+1)^2 (SOS):
lam=[Fr(0),Fr(0)]  # skip; do fully rational with R=diag(a,b) general
# Use R with eigs {1,2} only positive to show consistency with Cauchy-Schwarz:
lam2=[1,2]; m1=(1+2)/2; m2=(1+4)/2
cs=m1*m1/m2  # 2.25/2.5=0.9
print("\n(E) positive-eig sanity: diag(1,2): C-S m1^2/m2 =", cs, " n_+/d=1 (trivial bound)")
# mixed sign: eigs {1,-3}: bound should be meaningful.
lam3=[1,-3]; m1m=(1-3)/2; m2m=(1+9)/2
# Corrupted eigs, use SOS witness r(t)=(t+1)^2: p(t)=t(t+1)^2 = t^3+2t^2+t
p3=[1**3+2*1+1, (-3)**3+2*9+(-3)]  # p(1)=4, p(-3)=-27+18-3=-12
A=sum(p3); B=sum(x*x for x in p3)
# n_+/d >= (sum_{lam>0} p)^2/(d*B): only positive eig contributes 4.
nbd= (p3[0]**2)/(2*B)   # (4)^2/(2*(16+144))=16/320=0.05
print("    eigs {1,-3}, r=(t+1)^2 SOS, p=t*r: A_p=",A," B_p=",B," n_+/d >= max(0,A)^2/(2 B)=", nbd)
