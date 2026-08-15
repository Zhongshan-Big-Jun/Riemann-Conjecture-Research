import numpy as np, sys, time
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260815T130000Z-slmoments-a3f9\reproducibility")
from projection_dpp_sampler import run

if __name__ == "__main__":
    L = 25.0
    for h in [0.1, 0.05, 0.025]:
        ns = 60 if h >= 0.05 else 80
        t0 = time.time()
        mean, std, meanN, Ns = run(L, h, ns, 5, seed=20260816)
        print(f"L={L} h={h} ns={ns} E[N]={meanN:.3f} wall={time.time()-t0:.0f}s")
        print("  m1..m5:", " ".join(f"{v:.5f}" for v in mean))
        print("  std:    ", " ".join(f"{v:.5f}" for v in std))
        sys.stdout.flush()
