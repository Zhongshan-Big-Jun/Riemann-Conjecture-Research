#!/usr/bin/env python3
"""Multi-certificate trace-energy scan.

This is a generalization of the two-certificate supporting-plane method in
Yuhang Shi's ``main.tex``.  It accepts an arbitrary number of local
certificates
    E + p_q L_q >= A_q(m),   A_q(m) = eps_q (m - q),
where q is the number of gaps in the local window minus one (so the
(q+1)-point window has q gaps).  The span normalization comparison is
    L_a / q_a >= L_b / q_b   for q_a < q_b,
which is the exact coefficientwise statement used for the seven/nine-point
certificates in the candidate.

The block supporting plane is
    D + sum_q tau_q L_q >= R,   R = Phi_m(A_max),
and the averaged global bound is
    B = (m H_cert - sum_q tau_q q (m-q)) / (m - R).
The pressure taxes tau_q are found by a finite linear program: for every
breakpoint E of the piecewise-linear minimal-pressure function F(E), we
require F(E) >= R - Phi_m(E).  Because F is linear between these
breakpoints and Phi_m is concave, checking the breakpoints proves the
supporting plane on the whole interval [0, A_max].

All certificate inputs are exact Fractions; the LP uses floating point to
scan, and the best candidate is then verified in high-precision Decimal.
"""

from __future__ import annotations

import sys
from decimal import Decimal, localcontext
from fractions import Fraction as F
from typing import List, Optional, Sequence, Tuple

try:
    from scipy.optimize import linprog
    HAVE_SCIPY = True
except Exception:  # pragma: no cover
    HAVE_SCIPY = False


# ---------------------------------------------------------------------------
# Pinned inputs
# ---------------------------------------------------------------------------
H = F(3_362_285_207, 5_000_000_000)
H_DEC = Decimal(H.numerator) / Decimal(H.denominator)

# q = number of gaps in the local window minus one.
# The two certified Shi inputs are the retuned seven-point and nine-point
# certificates.  The script is generic: append more exact certificates to
# the list to scan a multi-certificate supporting plane.
CERTIFICATES: List[dict] = [
    {
        "name": "7pt-retuned",
        "q": 6,
        "p": F(1, 2_736),
        "eps": F(891, 200_000),
    },
    {
        "name": "9pt-final",
        "q": 8,
        "p": F(1, 2_500),
        "eps": F(15_211, 2_500_000),
    },
]

PREC = 80


def dec(x: F) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = PREC
        return Decimal(x.numerator) / Decimal(x.denominator)


def phi(m: int, e: Decimal) -> Decimal:
    """The finite-dimensional concave envelope Phi_m(E)."""
    with localcontext() as ctx:
        ctx.prec = PREC
        threshold = Decimal(m) / Decimal(m - 1)
        if e <= threshold:
            return e
        return (
            2 * ((Decimal(m - 1) / Decimal(m)) * e).sqrt()
            - 1
            + e / Decimal(m)
        )


def sort_certs(certs: Sequence[dict]) -> List[dict]:
    """Return certificates sorted by q (ascending), as the LP assumes."""
    return sorted(certs, key=lambda c: c["q"])


def A(m: int, i: int, certs: Sequence[dict]) -> F:
    return certs[i]["eps"] * (m - certs[i]["q"])


def normalized_cert_slope(certs: Sequence[dict], i: int) -> F:
    """Coefficient of -E in c_i(E)=(A_i-E)/(p_i q_i)."""
    return F(1, certs[i]["p"] * certs[i]["q"])


def l_value(m: int, i: int, e_dec: Decimal, certs: Sequence[dict]) -> Decimal:
    """Minimal feasible normalized pressure l_i(E)=max_{j>=i} c_j(E).

    Indices are sorted by q, and l_1 >= l_2 >= ... >= l_k.  The minimal
    monotone sequence dominating c_i is l_i = max_{j>=i} c_j.
    """
    with localcontext() as ctx:
        ctx.prec = PREC
        best = Decimal(0)
        for j in range(i, len(certs)):
            a_dec = dec(A(m, j, certs))
            cj = max(Decimal(0), (a_dec - e_dec) / (dec(certs[j]["p"]) * certs[j]["q"]))
            if cj > best:
                best = cj
        return best


def breakpoints(m: int, certs: Sequence[dict]) -> List[Decimal]:
    """All E where the argmax in l_i(E) can change, plus 0 and A_max.

    These are the nodes at which the LP constraints are imposed.
    """
    certs = sort_certs(certs)
    with localcontext() as ctx:
        ctx.prec = PREC
        nodes = {Decimal(0)}
        k = len(certs)
        # The relevant interval ends at the largest A.
        amax = max(A(m, i, certs) for i in range(k))
        amax_dec = dec(amax)
        for i in range(k):
            a_dec = dec(A(m, i, certs))
            if Decimal(0) <= a_dec <= amax_dec:
                nodes.add(a_dec)
            # c_i(E)=0 at E=A_i, already added.
            for j in range(i + 1, k):
                # Solve (A_i-E)/(p_i q_i) = (A_j-E)/(p_j q_j), i.e.
                # (s_j - s_i) E = s_j A_j - s_i A_i, s_i = 1/(p_i q_i).
                si = normalized_cert_slope(certs, i)
                sj = normalized_cert_slope(certs, j)
                den = sj - si
                if den == 0:
                    continue
                num = A(m, j, certs) * sj - A(m, i, certs) * si
                e_frac = num / den
                e_dec = dec(e_frac)
                if Decimal(0) <= e_dec <= amax_dec:
                    nodes.add(e_dec)
        return sorted(nodes)


def solve_lp(
    m: int, certs: Sequence[dict] = CERTIFICATES
) -> Optional[Tuple[float, List[float], Decimal, Decimal, Decimal, List[Decimal], List[dict]]]:
    """Solve the supporting-plane LP at block length m.

    Returns (status, tau, R, tax, B, nodes, row_info) or None if not
    applicable (A_max not on the concave branch or R >= 2).
    """
    certs = sort_certs(certs)
    k = len(certs)
    amax = max(A(m, i, certs) for i in range(k))
    amax_dec = dec(amax)
    threshold = Decimal(m) / Decimal(m - 1)
    if amax_dec <= threshold:
        return None
    r = phi(m, amax_dec)
    if r >= 2:
        return None

    nodes = breakpoints(m, certs)
    if not HAVE_SCIPY:
        raise RuntimeError("scipy is required for the LP scan")

    A_ub = []
    b_ub = []
    rows = []
    for e in nodes:
        if e > amax_dec + Decimal("1e-40"):
            continue
        rhs = r - phi(m, e)
        if rhs <= 0:
            continue
        coeffs = []
        for i in range(k):
            coeffs.append(float(certs[i]["q"] * l_value(m, i, e, certs)))
        A_ub.append([-c for c in coeffs])
        b_ub.append(-float(rhs))
        rows.append({"E": e, "coeffs": coeffs, "rhs": float(rhs)})

    c_obj = [float(certs[i]["q"] * (m - certs[i]["q"])) for i in range(k)]
    bounds = [(0, None)] * k
    res = linprog(c_obj, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not res.success:
        # Infeasible supporting plane at this m.
        return None
    tau = list(res.x)
    tax = sum(tau[i] * float(certs[i]["q"] * (m - certs[i]["q"])) for i in range(k))
    with localcontext() as ctx:
        ctx.prec = PREC
        tax_dec = Decimal(0)
        for i in range(k):
            tax_dec += Decimal(str(tau[i])) * Decimal(certs[i]["q"] * (m - certs[i]["q"]))
        bound = (Decimal(m) * H_DEC - tax_dec) / (Decimal(m) - r)
    return (0, tau, r, tax_dec, bound, nodes, rows)


def verify_solution(
    m: int,
    tau: Sequence[float],
    r: Decimal,
    nodes: Sequence[Decimal],
    certs: Sequence[dict] = CERTIFICATES,
    tol: str = "1e-12",
) -> Tuple[bool, List[dict]]:
    """High-precision verification of the LP solution at all breakpoints."""
    certs = sort_certs(certs)
    with localcontext() as ctx:
        ctx.prec = PREC
        tol_dec = Decimal(tol)
        bad = []
        for e in nodes:
            rhs = r - phi(m, e)
            if rhs <= 0:
                continue
            lhs = Decimal(0)
            for i in range(len(certs)):
                lval = l_value(m, i, e, certs)
                lhs += Decimal(str(tau[i])) * certs[i]["q"] * lval
            margin = lhs - rhs
            if margin < -tol_dec:
                bad.append({"E": e, "lhs": lhs, "rhs": rhs, "margin": margin})
        return (not bad), bad


def format_bound(bound: Decimal) -> str:
    return f"{bound:.30f}"


DEMO_CERT = {
    "name": "8pt-SYNTHETIC-DEMO-ONLY",
    "q": 7,
    "p": F(1, 2_600),
    "eps": F(6_000, 1_000_000),
}


def main() -> None:
    args = sys.argv[1:]
    demo_three = "--demo-three" in args
    m_arg = None
    for a in args:
        if a != "--demo-three":
            try:
                m_arg = int(a)
                break
            except ValueError:
                pass

    certs = list(CERTIFICATES)
    if demo_three:
        certs.append(dict(DEMO_CERT))
        print("*** DEMO MODE: the third certificate is SYNTHETIC and NOT certified. ***")
    certs = sort_certs(certs)

    if m_arg is not None:
        m_range: Sequence[int] = [m_arg]
    else:
        m_range = range(9, 1_001)

    print("multi-certificate scan")
    print(f"certificates: {[(c['name'], c['q']) for c in certs]}")
    print(f"scan range: {m_range.start if hasattr(m_range,'start') else m_range}.."
          f"{m_range.stop-1 if hasattr(m_range,'stop') else m_range[0]}")
    best = None
    feasible = []
    for m in m_range:
        sol = solve_lp(m, certs)
        if sol is None:
            continue
        status, tau, r, tax, bound, nodes, rows = sol
        ok, bad = verify_solution(m, tau, r, nodes, certs)
        if not ok:
            print(f"m={m}: WARNING LP solution failed verification: {bad[:1]}")
        feasible.append((bound, m, tau, tax))
        if best is None or bound > best[0]:
            best = (bound, m, tau, tax, r, nodes)

    print(f"feasible m count: {len(feasible)}")
    if best is None:
        print("no feasible m in range")
        return

    bound, m, tau, tax, r, nodes = best
    print("\nBEST")
    print(f"m = {m}")
    print(f"R = {r}")
    print(f"tau = {[float(t) for t in tau]}")
    print(f"tax = {tax}")
    print(f"B = {bound:.50f}")
    print("\nneighbourhood")
    for mm in range(m - 4, m + 5):
        if mm < 9:
            continue
        sol = solve_lp(mm, certs)
        if sol is not None:
            _, tau_mm, _, _, bound_mm, _, _ = sol
            print(f"m={mm}: B={bound_mm:.30f} tau={[float(t) for t in tau_mm]}")
    print("\nverification of best:")
    ok, bad = verify_solution(m, tau, r, nodes, certs)
    print(f"ok = {ok}")
    if bad:
        print(bad[:3])


if __name__ == "__main__":
    main()
