import numpy as np, sys
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T050000Z-m5exact-3f8a\reproducibility")
from fractions import Fraction as F
from boxspline_hp import coarea_value_hp
from enumerate_moments import partitions_of, blocksizes
from boxspline_exact import cycle_edges, rho_terms, perm_edges, reconstruct_rational
from collections import defaultdict

def J_hp(blocks, k):
    b = len(blocks)
    if b == 1:
        return F(1)
    cyc = cycle_edges(blocks, k)
    tot = 0.0
    for sign, perm in rho_terms(b):
        vs = cyc + perm_edges(perm, b)
        tot += sign * coarea_value_hp(vs)
    return F(tot).limit_denominator(10**6) if abs(tot) > 1e-6 else F(0)

def run(k):
    parts = partitions_of(k)
    rows = []
    byprof = defaultdict(lambda: F(0))
    tot = F(0)
    for blocks in parts:
        J = J_hp(list(blocks), k)
        rows.append((sorted(sorted(x) for x in blocks), blocksizes(blocks), J))
        byprof[tuple(blocksizes(blocks))] += J
        tot += J
    print(f"k={k}: TOTAL = {tot} = {float(tot):.10f}")
    for prof in sorted(byprof, key=len):
        print(f"   {prof}: {byprof[prof]} = {float(byprof[prof]):+.8f}")
    return tot, rows

if __name__ == "__main__":
    for k in [2,3,4,5]:
        run(k)
