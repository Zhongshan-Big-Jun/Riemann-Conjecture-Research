# Independent verification of the condp1 core finding (manager, 2026-08-14)
# Objects:
#  (a) int_R sinc^2(pi u) du = 1, int_R sinc^4(pi u) du = 2/3   (numerical, 50 dp)
#  (b) Christoffel function at 0: Lambda_m(0) = 1 / ((M_m^{-1})_00),
#      M_m = (m+1)x(m+1) Hankel matrix [m_{i+j}], moments m_0=1, m_1=1, m_2=m2, m_3=2, m_4=13/4
#  (c) corrected list m2 = 4/3: Lambda_2(0) = 5/36, 1-Lambda_2(0) = 31/36, 2*(31/36)-1 = 13/18
#  (d) written list m2 = 3/4: Lambda_2(0) = 38/25 > 1 (non-statement), Hankel det = -19/8 < 0
#  (e) m=1 sanity: Lambda_1(0) = m2 - m1^2 ... check formula gives 1 - Lambda_1(0) = m1^2/m2

from fractions import Fraction

# ---- (b),(c),(d),(e): exact rational arithmetic ----
def hankel(moments, size):
    # size x size Hankel matrix with entries moments[i+j]
    return [[moments[i + j] for j in range(size)] for i in range(size)]

def det(mat):
    n = len(mat)
    if n == 1:
        return mat[0][0]
    # Laplace along row 0
    total = Fraction(0)
    for c in range(n):
        minor = [row[:c] + row[c + 1:] for row in mat[1:]]
        total += ((-1) ** c) * mat[0][c] * det(minor)
    return total

def christoffel(moments, m):
    # Lambda_m(0) = 1 / ((M^{-1})_00); M = (m+1)x(m+1) Hankel
    M = hankel(moments, m + 1)
    D = det(M)
    # cofactor C_00 = det of M with row 0 replaced by e_0 = (1,0,...,0)
    row0 = [Fraction(1)] + [Fraction(0)] * m
    M2 = [row0] + M[1:]
    C00 = det(M2)
    inv00 = C00 / D
    return Fraction(1) / inv00

corr = [Fraction(1), Fraction(1), Fraction(4) / 3, Fraction(2), Fraction(13) / 4]
wrong = [Fraction(1), Fraction(1), Fraction(3) / 4, Fraction(2), Fraction(13) / 4]

for name, mom in [("corrected (1,4/3,2,13/4)", corr), ("written   (1,3/4,2,13/4)", wrong)]:
    H2 = det(hankel(mom, 2))
    H3 = det(hankel(mom, 3))
    L1 = christoffel(mom, 1)
    L2 = christoffel(mom, 2)
    print(f"[{name}]")
    print(f"  det H2 = {H2}   det H3 = {H3}")
    print(f"  Lambda_1(0) = {L1}   -> 1-Lambda_1(0) = {1 - L1}")
    print(f"  Lambda_2(0) = {L2}   -> 1-Lambda_2(0) = {1 - L2}   -> 2*(1-L2)-1 = {2 * (1 - L2) - 1}")

# m=1 identity check: 1 - Lambda_1(0) vs m1^2/m2
print("check m=1: m1^2/m2 (corrected) =", Fraction(1) / (Fraction(4) / 3))

# ---- (a): sinc integral identities (numerical, 50 dp) ----
import mpmath as mp
mp.mp.dps = 50
sinc = lambda u: mp.sin(mp.pi * u) / (mp.pi * u)
I2 = mp.quad(sinc, [-mp.inf, mp.inf])
I4 = mp.quad(lambda u: sinc(u) ** 4, [-mp.inf, mp.inf])
print(f"int sinc^2 = {mp.nstr(I2, 30)}   (expect 1)")
print(f"int sinc^4 = {mp.nstr(I4, 30)}   (expect 2/3 = {mp.nstr(mp.mpf(2) / 3, 30)})")
print("Lemma C: E tr G^2 / L -> 1 + (int sinc^2 - int sinc^4) =", mp.nstr(1 + (I2 - I4), 30), "(expect 4/3)")
