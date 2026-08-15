# Christoffel numbers (Hankel ratio) from moment sequences relevant to the sine-Gram SL.
# SL (no atom at 0) <=> Lambda_m(0)->0 <=> det(H_m)/det(minor00) -> 0.
# Test the published/empirical moment lists and the exact partial list (1,4/3,2,13/4).
import numpy as np
from fractions import Fraction

def hankel_det(moms, order):
    H = np.zeros((order+1, order+1))
    for i in range(order+1):
        for j in range(order+1):
            H[i, j] = float(moms[i+j])
    return np.linalg.det(H)

def lambda_m(moms, order):
    # Lambda_m(0) = det(H_m) / det(minor00) ; needs moments up to order 2(m?) ... 
    # H_m is (m+1)x(m+1) uses mom[0..2m]; minor00 is m x m uses mom[2..2m].
    numerator = hankel_det(moms, order)          # det H_m
    denominator = hankel_det(moms[2:], order-1)  # det minor00
    return numerator / denominator

# ---- A) exact partial list (1,4/3,2,13/4) then "unknown" tail as a param probe.
print("=== A) Exact (1,4/3,2,13/4) only: Lambda_m for m=1,2 ===")
ex_list = [Fraction(1), Fraction(4,3), Fraction(2), Fraction(13,4)]
def gl(m):
    # generalized Christoffel using the exact low moments + assume some continuation
    return None
# m=1: uses mom[0..2] = (1,4/3,m2=?)... m=1 needs mom up to 2m=2 -> (m0,m1,m2)=(1,4/3,?).
# We only know m2=4/3; so Lambda_1(0) uses (m0,m1,m2)=(1,1,4/3):
L1 = lambda_m([Fraction(1),Fraction(1),Fraction(4,3)], 1)
# m=2 uses up to mom4=(1,4/3,2,13/4):
L2 = lambda_m([Fraction(1),Fraction(1),Fraction(4,3),Fraction(2),Fraction(13,4)], 2)
print(f"Lambda_1(0) = {float(L1):.6f}  (expect 1 - m1^2/m2 = 1-3/4=0.25? m1=1 -> 1-1/(4/3)=1/4=0.25)")
print(f"Lambda_2(0) = {float(L2):.6f}  (expect probe 0.133, paper 5/36=0.1389)")
print("   m1=1 here makes Lambda_1=1-1/(4/3)=0.25; paper's 5/36=0.1389 is 'Lambda_2' with the (1,4/3,2,13/4) list -> check match.")

# ---- B) empirical sine-Gram moments from probe (L=50): (1, 1.322,1.966,3.171,5.435,9.770,18.245,35.148)
print("\n=== B) Empirical moments (probe L=50), Hankel-ratio Christoffel numbers ===")
emp = [1.0, 1.322, 1.966, 3.171, 5.435, 9.770, 18.245, 35.148]
for m in range(1, 4):  # need up to mom[2m]
    # Lambda_m needs mom[0..2m]; if present
    need = 2*m
    if len(emp) > need:
        lv = lambda_m(emp, m)
        print(f"Lambda_{m}(0) = {lv:.6f}")
print("(probe reported Lambda_1=0.322,Lambda_2=0.133,Lambda_3=0.054? with its own def; "
      "here using Hankel-ratio def)")

# ---- C) Growth-fit: fit m_k ~ a*k^alpha on empirical k=2..8 and extrapolate Lambda_m(0).
print("\n=== C) Moment growth fit (evidence only) ===")
kk = np.arange(2, 8, dtype=float)
mm = np.array([1.322,1.966,3.171,5.435,9.770,18.245])
loga, al = np.polyfit(np.log(kk), np.log(mm), 1)
alpha = float(al); a = float(np.exp(loga))
print(f"m_k ~ a*k^alpha: a={a:.3f} alpha={alpha:.3f}")
# if alpha<2, Carleman sum converges? Carleman needs sum m_{2k}^{-(1/(2k))}=inf.
# For m_k~a k^alpha, m_{2k}^{1/(2k)} -> 1 (bounded) so not conclusive by Carleman tail alone.
# The relevant question: does Lambda_m(0)->0? For a measure on a half-line with all moments
# growing polynomially, the support must be compact (since m_k^(1/k)->1 finite => radius <=1)
# => support in [0,1]. Then 0 in support & no atom control Lambda_m->0.
print("Note: m_k^(1/k) -> 1 => if this held rigorously, support subset [0,1] (compact).")
print("Then whether Lambda_m(0)->0 (no atom at 0) is governed by local mass near 0.")
