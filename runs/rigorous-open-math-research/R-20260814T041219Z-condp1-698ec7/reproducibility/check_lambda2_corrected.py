"""Independent check: with the corrected moment list (1,4/3,2,13/4), Lambda_2(0)=5/36,
and 13/18 = 2*(1-Lam)-1.  Exact rational arithmetic."""
from fractions import Fraction as Fr

def det(A):
    n = len(A)
    if n == 1: return A[0][0]
    return sum((-1) ** j * A[0][j] * det([r[:j] + r[j+1:] for r in A[1:]]) for j in range(n))

def Lam2(ms):  # ms[0..4], Christoffel 1/(M^{-1})_00, M=(m_{i+j})_{i,j=0..2}
    M = [[ms[i+j] for j in range(3)] for i in range(3)]
    d = det(M)
    cof = det([[M[1][1], M[1][2]], [M[2][1], M[2][2]]])  # minor M_{00}
    return d / cof   # M^{-1}_00 = cof/d ; Lam = 1/(M^{-1}_00) = d/cof

corr = [Fr(1), Fr(1), Fr(4, 3), Fr(2), Fr(13, 4)]
p    = [Fr(1), Fr(1), Fr(3, 4), Fr(2), Fr(13, 4)]

Lam_c = Lam2(corr)
Lam_p = Lam2(p)
print("corrected (1,4/3,2,13/4):  Lambda_2(0) =", Lam_c, "=", float(Lam_c))
print("  1 - Lambda_2(0)          =", 1 - Lam_c, "=", float(1 - Lam_c))
print("  -> matches paper's 5/36?", Lam_c == Fr(5, 36))
print("paper    (1,3/4,2,13/4):  Lambda_2(0) =", Lam_p, "=", float(Lam_p))

lam = Fr(5, 36)
print("\n13/18 = 2*(1-5/36)-1 ?", (2 * (1 - lam) - 1) == Fr(13, 18),
      "  value 2*(1-5/36)-1 =", 2 * (1 - lam) - 1, "=", float(2 * (1 - lam) - 1))

# validity of corrected list
print("\nCorrected list validity: m_2-m_1^2 =", Fr(4, 3) - Fr(1) * Fr(1), ">=0 yes;")
print("leading 3x3 Hankel det:", end=" ")
M3 = [[corr[i+j] for j in range(3)] for i in range(3)]
print(det(M3))
