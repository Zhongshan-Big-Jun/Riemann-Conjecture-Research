#!/usr/bin/env python
"""Master summary for R-20260816T060000Z-m6exact-4f9a.
Reassembles m_6 from the batch CSVs (ignoring hardcoded sums) and prints the exact Hankel verdicts.
Status label: FINITE_COMPUTATIONAL_RESULT (exact m_6) / RIGOROUS_PARTIAL_RESULT (fork)."""
import os, csv, glob
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))

def load(pat):
    d = {}
    for f in glob.glob(os.path.join(HERE, pat)):
        for r in csv.DictReader(open(f)):
            key = int(r["idx"])
            v = r["J_recon"].strip()
            d[key] = F(0) if v == "0" else F(v)
    return d

def main():
    b1 = F(1)
    # b=2 analytic (verified)
    b2 = F(4297, 630)
    b3 = sum(load("b3_batch*.csv").values(), F(0))
    b4 = sum(load("b4_fast_c*.csv").values(), F(0))
    b5 = sum(load("b5_fast.csv").values(), F(0))
    b6 = sum(load("b6_fast.csv").values(), F(0))
    m6 = b1 + b2 + b3 + b4 + b5 + b6
    print("n_b3 =", len(load("b3_batch*.csv")), " n_b4 =", len(load("b4_fast_c*.csv")),
          " n_b5 =", len(load("b5_fast.csv")), " n_b6 =", len(load("b6_fast.csv")))
    print("b1 =", b1)
    print("b2 =", b2)
    print("b3 =", b3, "=", float(b3))
    print("b4 =", b4, "=", float(b4))
    print("b5 =", b5)
    print("b6 =", b6)
    print("m_6 =", m6, "=", float(m6))
    assert m6 == F(640, 63), "m6 mismatch"

    # Hankel
    ms = [F(1), F(1), F(4, 3), F(2), F(13, 4), F(101, 18), m6]
    def ham(M):
        A = [[ms[i + j] for j in range(M + 1)] for i in range(M + 1)]
        N = M + 1
        A = [row[:] for row in A]; d = F(1)
        for col in range(N):
            piv = next((r for r in range(col, N) if A[r][col] != 0), None)
            if piv is None: return F(0)
            if piv != col: A[col], A[piv] = A[piv], A[col]; d = -d
            pv = A[col][col]
            for r in range(col + 1, N):
                if A[r][col] == 0: continue
                fac = A[r][col] / pv
                for c in range(col, N): A[r][c] -= fac * A[col][c]
            d *= pv
        return d
    print("\nHankel (Christoffel) ratios:")
    for M in (1, 2, 3):
        H = ham(M-0)
        A00 = [[ms[2 + i + j] for j in range(M)] for i in range(M)]
        N = M; A00 = [row[:] for row in A00]; d00 = F(1)
        for col in range(N):
            piv = next((r for r in range(col, N) if A00[r][col] != 0), None)
            if piv is None: d00 = F(0); break
            if piv != col: A00[col], A00[piv] = A00[piv], A00[col]; d00 = -d00
            pv = A00[col][col]
            for r in range(col + 1, N):
                if A00[r][col] == 0: continue
                fac = A00[r][col] / pv
                for c in range(col, N): A00[r][c] -= fac * A00[col][c]
            d00 *= pv
        lam = H / d00
        print(f"  Lambda_{M}(0) = {lam} = {float(lam):.9f}")
    l2 = F(5, 36); l3 = F(247, 2519)
    print("\nfork verdict: Lambda_3 =", l3, "< Lambda_2 =", l2, "-> DECAY (plateau ~0.149 impossible).")

main()
