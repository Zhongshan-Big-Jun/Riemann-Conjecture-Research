#!/usr/bin/env python
"""Step 2: exact Hankel-ratio Christoffel numbers Lambda_m(0) from the EXACT moments.

Definition (matches extended_moments_hankel.py / probe): with moment sequence
moments s_0..s_N = [m_0, m_1, m_2, ...] with m_0 = 1,
  Lambda_m(0) = det(H_m)/det(H_m^(00)), where
    H_m     = (s_{i+j})_{i,j=0..m}          (m+1)x(m+1)
    H_m^(00)= (s_{2+i+j})_{i,j=0..m-1}      (m-matrix)
Using exact Fractions -> rational Lambda_m(0)."""
from fractions import Fraction as F

def hankel_det(s, order, shift, use_fractions=True):
    import numpy as np
    n = order + 1
    M = [[s[shift + i + j] for j in range(n)] for i in range(n)]
    if use_fractions:
        M = [[F(v) for v in row] for row in M]
        # exact fraction determinant by fraction elimination
        A = [row[:] for row in M]
        NN = len(A)
        det = F(1)
        for col in range(NN):
            piv = None
            for r in range(col, NN):
                if A[r][col] != 0:
                    piv = r; break
            if piv is None:
                return F(0)
            if piv != col:
                A[col], A[piv] = A[piv], A[col]; det = -det
            pv = A[col][col]
            for r in range(col + 1, NN):
                if A[r][col] == 0: continue
                factor = A[r][col] / pv
                for c in range(col, NN):
                    A[r][c] = A[r][c] - factor * A[col][c]
            det *= pv
        return det
    else:
        return np.linalg.det(np.array(M, dtype=float))

if __name__ == "__main__":
    import mpmath as mp
    mp.mp.dps = 50
    # exact moments s_k = m_k (m0=1); m1..m5 exact, m6..m8 from sampler (L=50,h=0.05) as evidence
    mexact = [F(1), F(1), F(4, 3), F(2), F(13, 4), F(101, 18)]
    sampler = [5.45506723, 9.80921161, 18.31935527, 35.28209683]  # m5..m8 (m5 replaced below
    # use exact m1..m5; m6,m7,m8 from sampler
    s6s = [float(F(101,18)), 9.80921161, 18.31935527, 35.28209683]
    s = [F(1), F(1), F(4, 3), F(2), F(13, 4), F(101, 18),
         F(9.80921161).limit_denominator(10**9), F(18.31935527).limit_denominator(10**9),
         F(35.28209683).limit_denominator(10**9)]
    print("moments s0..s8 (exact thru s5; s6..s8 sampler rat approx)")
    for m in range(1, 5):
        H = hankel_det(s, m, 0)
        H00 = hankel_det(s, m - 1, 2)
        lam = H / H00
        tag = "EXACT" if m <= 2 else "sampler s6.. for H terms"
        print(f"Lambda_{m}(0) = {lam} = {float(lam):.10f}   [{tag}]  (detH00={H00})")
    # also compute Lambda_3,4 in pure mpmath high precision from exact+sampler floats (stable det)
    smp = [mp.mpf('1.0'), mp.mpf('1.0'), mp.mpf('4')/3, mp.mpf('2'), mp.mpf('13')/4,
           mp.mpf('101')/18, mp.mpf('9.80921161'), mp.mpf('18.31935527'), mp.mpf('35.28209683')]
    def lam_mp(m):
        H = mp.matrix([[smp[i+j] for j in range(m+1)] for i in range(m+1)])
        H00 = mp.matrix([[smp[2+i+j] for j in range(m)] for i in range(m)])
        return mp.det(H)/mp.det(H00)
    for m in [1,2,3,4]:
        print(f"  [mpmath] Lambda_{m}(0) = {mp.nstr(lam_mp(m),14)}")
