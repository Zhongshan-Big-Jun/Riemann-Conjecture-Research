# Independent exact-rational check: Lambda_2(0) = 5/36 from exact sine-Gram moments.
#
# CONVENTION (trace-normalized — matches condp1 candidate_proof.md + the probe):
#   m0 = total mass = 1
#   m1 = (1/N) tr G_L  = 1
#   m2 = 4/3, m3 = 2, m4 = 13/4
#   The audited list "(1, 4/3, 2, 13/4)" is (m1,m2,m3,m4). m0 is the separate total-mass moment.
# This exact-rational check reproduces Lambda_2(0)=5/36 and confirms monotonicity + Cauchy-Schwarz,
# rebutting a mis-indexed reading of the list.
from fractions import Fraction

# moments: m0 (total mass)=1, m1=1, m2=4/3, m3=2, m4=13/4
m0,m1,m2,m3,m4 = Fraction(1),Fraction(1),Fraction(4,3),Fraction(2),Fraction(13,4)

def det2(A):
    return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def det3(A):
    return (A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])
          - A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])
          + A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))

# H_2 = 3x3 Hankel of (m0..m4)
H2=[[m0,m1,m2],[m1,m2,m3],[m2,m3,m4]]
# minor00 = delete row0,col0 -> 2x2 Hankel of (m2,m3,m4)
MIN=[[m2,m3],[m3,m4]]

num=det3(H2)
den=det2(MIN)
L = Fraction(num,den)
print("det(H_2)  =", num)
print("det(minor)= ", den)
print("Lambda_2(0) = det(H_2)/det(minor) =", L, "=", float(L))
print("paper value 5/36 = 0.138888... ; match:", L == Fraction(5,36))

# Lambda_1(0) has (m0,m1,m2)=(1,1,4/3): det[[1,1],[1,4/3]] / (4/3) = (1/3)/(4/3) = 1/4.
L1 = Fraction(m0*m2 - m1*m1, m2)
print("Lambda_1(0) =", L1, "=", float(L1), "(m0=1,m1=1,m2=4/3)")

# --- Explicit consistency / validity checks (rebuts mis-indexed reading) ---
print("\nConsistency checks under the correct convention (m0=1,m1=1,m2=4/3,m3=2,m4=13/4):")
print("  monotonicity Lam_2 <= Lam_1 ?", L <= L1, f"  ({float(L):.4f} <= {float(L1):.4f})")
print("  Cauchy-Schwarz  m3^2 <= m2*m4 ?", m3*m3 <= m2*m4, f"  ({float(m3*m3):.3f} <= {float(m2*m4):.3f})")
print("  full 3x3 Hankel det > 0 (PSD moment seq) ?", (m0,m1,m2,m3,m4) is not None and True if det3(H2) > 0 else False, f"  det={det3(H2)}")
assert L <= L1, "monotonicity violated"
assert m3*m3 <= m2*m4, "CS violated"
assert det3(H2) > 0, "moment seq not PSD"
print("\nAll consistency checks PASS. The exact list (m1,m2,m3,m4)=(1,4/3,2,13/4) with m0=1 is a valid "
      "probability-moment sequence and gives Lambda_2(0)=5/36 exactly.")
