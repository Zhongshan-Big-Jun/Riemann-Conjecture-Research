"""Gate B: reproduce audited exact moments (m_1,m_2,m_3,m_4)=(1,4/3,2,13/4) on the
projection-DPP discretization of the sine process on [0,25], h=0.05, within the h->0 bias
quoted in reports/sl-lemma-random-gram-probe.md section 2:
  E[N]=25.0; m2~1.3134->4/3; m3~1.94->2; m4~3.1056->13/4.
EVIDENCE GATE: if these do NOT match within a reasonable h-bias, the sampler is defective and
must be reported; no D_k evidence may be produced from it.
"""
import numpy as np
from projection_dpp_sampler import run

def main():
    L, h = 25.0, 0.05
    for ns in [150, 300]:
        mean, std, meanN, Ns = run(L, h, ns, 5, seed=1234)
        print(f"[L={L} h={h} ns={ns}] E[N]={meanN:.3f} (ref 25.0), N in [{Ns.min()},{Ns.max()}]")
        print(f"   m1..m5 = " + " ".join(f"{v:.4f}" for v in mean))
        print(f"   std    = " + " ".join(f"{v:.4f}" for v in std))
        ok = abs(meanN-25.0)<1.5 and abs(mean[1]-4/3)<0.15 and abs(mean[2]-2.0)<0.25 and abs(mean[3]-3.25)<0.4
        print(f"   gate m2~4/3,m3~2,m4~13/4,E[N]~25 -> {'OK' if ok else 'FAIL'}")
        # print flushed
        print(flush=True)

if __name__ == "__main__":
    main()
