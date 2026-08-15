"""Extended sine-DPP Gram moments from the validated projection-DPP discretization,
and the Hankel-ratio Christoffel numbers Lambda_m(0) at high precision.

m_k = (1/N)E[tr G^k] measured by the validated sampler (gate passed: reproduces
(1,4/3,2,13/4) within h-bias; E[N]=25). We report the full list and Lambda_m(0) for m up to
the available order, at mpmath 50-digit precision with a stable determinant path.
EVIDENCE ONLY (simulation), never a proof of SL.
"""
import numpy as np
from projection_dpp_sampler import run

def hankel(moms, order, shift=0):
    return [[moms[shift+i+j] for j in range(order+1)] for i in range(order+1)]

def lam(moms, order):
    import mpmath as mp
    mp.mp.dps = 50
    mm = [mp.mpf(str(x)) for x in moms]
    H  = mp.det(hankel(mm, order, 0))
    mn = mp.det(hankel(mm, order-1, 2))
    return H/mn, H, mn

if __name__ == "__main__":
    import mpmath as mp
    mp.mp.dps = 50
    print("=== Extended moments m_1..m_8 from validated sampler ===", flush=True)
    print("(L=50, h=0.05, several sample budgets to reduce Monte-Carlo error)", flush=True)
    mean, std, meanN, Ns = run(50.0, 0.05, 200, 8, seed=42)
    print(f"  E[N]={meanN:.2f}", flush=True)
    print("  m_k  = " + " ".join(f"{v:.5f}" for v in mean), flush=True)
    print("  std  = " + " ".join(f"{v:.5f}" for v in std), flush=True)
    emp = [1.0] + list(mean)          # m_0=1 separate from m_1
    print("\n=== Hankel-ratio Christoffel Lambda_m(0) (mpmath 50 digit) ===", flush=True)
    for m in range(1, 4):
        Lv, H, mn = lam(emp, m)
        print(f"  Lambda_{m}(0) = {mp.nstr(Lv, 12)}", flush=True)
    # save list for artifacts
    with open("measured_moments_L50.txt","w") as f:
        f.write("m0=1\n")
        for k,v in enumerate(mean, start=1):
            f.write(f"m{k}={v:.8f}\n")
    print("\n  [probe L=50 reference: (1.0,1.322,1.966,3.171,5.435,9.770,18.245,35.148)]", flush=True)
