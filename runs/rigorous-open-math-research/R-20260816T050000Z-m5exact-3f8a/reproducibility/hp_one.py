import numpy as np, sys, time
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T050000Z-m5exact-3f8a\reproducibility")
from fractions import Fraction as F
from boxspline_hp import coarea_value_hp
from boxspline_exact import cycle_edges, rho_terms, perm_edges
from exact_volume import hull_volume_exact

def J_hp_one(blocks, k, maxcomb):
    b = len(blocks)
    cyc = cycle_edges(blocks, k)
    tot = 0.0
    t0=time.time()
    for i,(sign, perm) in enumerate(rho_terms(b)):
        vs = cyc + perm_edges(perm, b)
        t1=time.time()
        v = coarea_value_hp(vs, maxcomb=maxcomb)
        tot += sign * v
        #print(f"  perm{i} sign{sign} v={v:.6f} ({time.time()-t1:.1f}s) edges={len(vs)}")
    return tot, time.time()-t0

if __name__=="__main__":
    import sys as s2
    target=eval(s2.argv[1]); blocks=[frozenset(x) for x in target]
    k=5
    mc=int(s2.argv[2]) if len(s2.argv)>2 else 200000
    t0=time.time()
    tot,wall=J_hp_one(blocks,k,mc)
    print("partition",blocks,"result",tot,"=%.8f"%tot,"wall",wall)
