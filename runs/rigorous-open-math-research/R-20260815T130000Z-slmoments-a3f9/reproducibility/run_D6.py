from probe_Dk_fast import measure
import time
# D6 is expensive; use L=25 (N~25) and a modest sample budget; run in chunks to see progress
t=time.time()
Nm,mm,ms,D = measure(25.0, 0.05, 40, 6, seed=17)
print(f"=== D6 probe L=25 h=0.05 ns=40 (t={time.time()-t:.0f}s) E[N]={Nm:.1f} ===")
print("  m_k k=1..6: "+" ".join(f"{v:.4f}" for v in mm))
for k in sorted(D): print(f"  D{k} = {D[k][0]:+.5f} +- {D[k][1]:.5f}")
