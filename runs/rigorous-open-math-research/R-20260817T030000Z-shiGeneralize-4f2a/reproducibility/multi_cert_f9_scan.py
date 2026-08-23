#!/usr/bin/env python3
"""Integration scan: convert general-k pressure certificates into Shi-style
(p_q, eps_q) block inputs and run the existing multi-certificate LP.

This is a numerical/evidence scan. It does NOT prove the supporting-plane
optimum and it imports the upstream analytic interface / certificates as trust
boundaries. All certificate inputs are exact Fractions.
"""

from __future__ import annotations

import sys
from decimal import Decimal, localcontext
from fractions import Fraction as F

# Original multi-certificate scanner (unchanged, read-only import).
ORIG_DIR = (
    "/mnt/f/LaTeX/Riemann Conjecture/runs/rigorous-open-math-research/"
    "R-20260817T030000Z-shiGeneralize-4f2a/reproducibility"
)
sys.path.insert(0, ORIG_DIR)
import multi_cert_scan as mc  # noqa: E402


def make_cert(name: str, q: int, p: F, eps: F) -> dict:
    return {"name": name, "q": q, "p": p, "eps": eps}


# ---------------------------------------------------------------------------
# Certificate sets
# ---------------------------------------------------------------------------
# Existing upstream retuned seven/nine pairs used by multi_cert_scan.py.
SEVEN_RETUNED = make_cert("7pt-retuned", 6, F(1, 2_736), F(891, 200_000))
NINE_RETUNED = make_cert("9pt-final", 8, F(1, 2_500), F(15_211, 2_500_000))
# Direct canonical maps from the general-k pressure certificates:
#   p_q = 1/(500 q), eps_q = f_{q+1}, q = k-1.
SEVEN_CANON = make_cert("7pt-F6>=19/5000", 6, F(1, 3_000), F(19, 5_000))
NINE_F9 = make_cert("9pt-F8>=392/100000", 8, F(1, 4_000), F(392, 100_000))
# Synthetic k=10 / q=9 demonstration certificate. NOT certified.
K10_SYNTH = make_cert("10pt-SYNTHETIC-DEMO-ONLY", 9, F(1, 4_500), F(395, 100_000))

CERT_SETS = [
    ("baseline-retuned", [SEVEN_RETUNED, NINE_RETUNED]),
    ("f9-mapped-retuned7", [SEVEN_RETUNED, NINE_F9]),
    ("f9-mapped-canon7", [SEVEN_CANON, NINE_F9]),
    ("f9-mapped-retuned7-demo-k10", [SEVEN_RETUNED, NINE_F9, K10_SYNTH]),
]


def scan_set(name: str, certs: list, m_range=range(9, 1_001)) -> dict | None:
    certs = mc.sort_certs(certs)
    best = None
    feasible: list[tuple] = []
    for m in m_range:
        sol = mc.solve_lp(m, certs)
        if sol is None:
            continue
        status, tau, r, tax, bound, nodes, rows = sol
        ok, bad = mc.verify_solution(m, tau, r, nodes, certs)
        if not ok:
            print(f"[{name}] m={m}: WARNING LP verification failed: {bad[:1]}")
        feasible.append((bound, m, tau, tax))
        if best is None or bound > best[0]:
            best = (bound, m, tau, tax, r, nodes)
    return {
        "name": name,
        "certs": certs,
        "feasible_count": len(feasible),
        "best": best,
        "feasible": feasible,
    }


def fmt_certs(certs: list) -> str:
    return "; ".join(
        f"{c['name']}: q={c['q']}, p={c['p']} ({float(c['p']):.10g}), "
        f"eps={c['eps']} ({float(c['eps']):.10g})"
        for c in mc.sort_certs(certs)
    )


def main() -> None:
    for name, certs in CERT_SETS:
        print("=" * 100)
        print(f"CERT SET: {name}")
        print(fmt_certs(certs))
        print("scan m=9..1000")
        result = scan_set(name, certs)
        if result is None or result["best"] is None:
            print("no feasible m")
            continue
        bound, m, tau, tax, r, nodes = result["best"]
        print(f"feasible m count: {result['feasible_count']}")
        print(f"best m = {m}")
        print(f"R = Phi_m(A_max) = {r}")
        print(f"tau = {[float(t) for t in tau]}")
        print(f"tax = sum tau_q q (m-q) = {tax}")
        print(f"B = {bound}")
        print("neighbourhood:")
        for mm in range(m - 5, m + 6):
            if mm < 9:
                continue
            sol = mc.solve_lp(mm, certs)
            if sol:
                _, tau_mm, _, _, bound_mm, _, _ = sol
                ok, bad = mc.verify_solution(mm, tau_mm, r, nodes, certs)
                print(f"  m={mm}: B={bound_mm:.30f} tau={[float(t) for t in tau_mm]}")
        ok_best, bad_best = mc.verify_solution(m, tau, r, nodes, certs)
        print(f"best verification ok = {ok_best} (bad {len(bad_best)})")
        if bad_best:
            print("  first bad:", bad_best[:3])

    print("=" * 100)
    print("Illustrative exact A_q(219) for the f9-mapped set (m=219):")
    mapped_certs = mc.sort_certs([SEVEN_RETUNED, NINE_F9])
    for c in mapped_certs:
        a = mc.A(219, mapped_certs.index(c), mapped_certs)
        with localcontext() as ctx:
            ctx.prec = mc.PREC
            a_dec = mc.dec(a)
        print(f"  {c['name']}: q={c['q']}, A_q(219)={a}={a_dec}")


if __name__ == "__main__":
    main()
