#!/usr/bin/env python
"""Independent validation: compare the FAST engine's per-term box-spline value for one b=4 rho
term against the TRUE exact engine (boxspline_exact2.coarea_value_exact, sympy exact vertices)
for a partition that came out nonzero (idx 12 -> 1/105). If the per-term values agree to ~1e-12
the fast-sum is trustworthy."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from enumerate_moments import partitions_of
from boxspline_exact import cycle_edges, rho_terms, perm_edges
from boxspline_exact_fast import eq_coarea_value_exact_fast as FAST
from boxspline_exact2 import coarea_value_exact as TRUE

def np_arr(fl): return np.array([int(round(x)) for x in fl])

parts = [list(bl) for bl in partitions_of(6) if len(bl) == 4]
bl = parts[12]
print("validating b=4 idx12 partition", [sorted(sorted(x) for x in bl)], flush=True)
cyc = cycle_edges(bl, 6)
# pick a rho term with n>=8 (nontrivial box-spline)
cnt = 0
for sign, perm in rho_terms(4):
    vs = [np_arr(e) for e in (cyc + perm_edges(perm, 4))]
    n = len(vs)
    if n >= 8:
        t0 = time.time()
        f = FAST(vs)
        t1 = time.time()
        t = TRUE(vs)
        print(f"  term n={n} sign={sign:+d} fast={f:+.12f} true={t:+.12f} diff={abs(f-t):.1e} (fast {t1-t0:.1f}s)", flush=True)
        cnt += 1
        if cnt >= 4:
            break
print("done", flush=True)
