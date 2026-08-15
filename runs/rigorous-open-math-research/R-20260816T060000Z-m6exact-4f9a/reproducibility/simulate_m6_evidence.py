#!/usr/bin/env python
"""Step-2 evidence: DPP simulation of m_1..m_7 at L=50 over several h, measuring the h-bias so the
h->0 limit can be extrapolated and compared with the EXACT m_6 (evidence only, never proof).
The finite-h occupancy-DPP sampler underestimates higher moments (the established bias model from
the m_5 run)."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from projection_dpp_sampler import run

def main():
    L = 50.0
    print(f"# L={L} DPP simulation of m_1..m_7 (evidence only)", flush=True)
    print("# h   ns   E[N]   m1       m2       m3       m4       m5       m6       m7")
    for h in [0.05, 0.03333333, 0.025, 0.02]:
        ns = 200 if h >= 0.033 else 250
        t0 = time.time()
        mean, std, meanN, Ns = run(L, h, ns, 7, seed=20260816)
        print(f"{h:.5f} {ns} {meanN:.1f} " + " ".join(f"{v:8.5f}" for v in mean) +
              f"   [wall {time.time()-t0:.0f}s]", flush=True)
        print(f"  (std)      " + "          " + " ".join(f"{v:8.5f}" for v in std), flush=True)

main()
