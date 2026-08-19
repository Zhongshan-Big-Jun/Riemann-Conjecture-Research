#!/usr/bin/env python3
"""Exploratory scan over the supporting-plane target R (not a proof artifact)."""

import sys
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260817T030000Z-shiGeneralize-4f2a\reproducibility")
from decimal import Decimal, localcontext
from fractions import Fraction as F
from scipy.optimize import linprog
import multi_cert_scan as mc


def eroot(m: int, R: Decimal) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = mc.PREC
        lo = Decimal(m) / Decimal(m - 1)
        hi = Decimal(1000)
        for _ in range(200):
            mid = (lo + hi) / 2
            if mc.phi(m, mid) < R:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2


def solve_R(m: int, R: Decimal):
    certs = mc.CERTIFICATES
    k = len(certs)
    nodes = mc.breakpoints(m, certs)
    e_r = eroot(m, R)
    nodes = [e for e in nodes if e <= e_r + Decimal("1e-40")]
    nodes.append(e_r)
    nodes = sorted(set(nodes))
    A_ub = []
    b_ub = []
    for e in nodes:
        rhs = R - mc.phi(m, e)
        if rhs <= 0:
            continue
        coeffs = [float(certs[i]["q"] * mc.l_value(m, i, e, certs)) for i in range(k)]
        A_ub.append([-c for c in coeffs])
        b_ub.append(-float(rhs))
    cobj = [float(certs[i]["q"] * (m - certs[i]["q"])) for i in range(k)]
    res = linprog(cobj, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)] * k, method="highs")
    if not res.success:
        return None
    tau = list(res.x)
    tax = sum(tau[i] * float(certs[i]["q"] * (m - certs[i]["q"])) for i in range(k))
    with localcontext() as ctx:
        ctx.prec = mc.PREC
        taxd = Decimal(0)
        for i in range(k):
            taxd += Decimal(str(tau[i])) * Decimal(certs[i]["q"] * (m - certs[i]["q"]))
        B = (Decimal(m) * mc.H_DEC - taxd) / (Decimal(m) - R)
    return B, tau, taxd, R, e_r


def main() -> None:
    m = 219
    certs = mc.CERTIFICATES
    amax = max(mc.A(m, i, certs) for i in range(len(certs)))
    with localcontext() as ctx:
        ctx.prec = mc.PREC
        rmax = mc.phi(m, mc.dec(amax))
        print("Rmax", rmax)
        best = None
        for n in range(1, 1001):
            R = rmax * Decimal(n) / Decimal(1000)
            sol = solve_R(m, R)
            if sol and (best is None or sol[0] > best[0]):
                best = sol
        print("best", best)
        for R in [Decimal("1.26"), Decimal("1.265"), Decimal("1.266"),
                  Decimal("1.2665"), Decimal("1.2667"), Decimal("1.26675"), rmax]:
            sol = solve_R(m, R)
            print(R, sol[0] if sol else None,
                  sol[1] if sol else None,
                  sol[3] if sol else None)


if __name__ == "__main__":
    main()
