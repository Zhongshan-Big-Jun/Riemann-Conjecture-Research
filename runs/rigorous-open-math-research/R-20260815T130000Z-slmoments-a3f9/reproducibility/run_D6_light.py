from probe_Dk_fast import measure
import time
# lightweight D6 (smaller N, fewer samples) to also get a numerical figure; exact integral is primary
t=time.time()
Nm,mm,ms,D = measure(20.0, 0.05, 12, 6, seed=99)
print(f"D6 MC L=20 h=0.05 ns=12 (t={time.time()-t:.0f}s) E[N]={Nm:.1f}")
print("  m_k: "+" ".join(f"{v:.4f}" for v in mm))
for k in sorted(D): print(f"  D{k} = {D[k][0]:+.5f} +- {D[k][1]:.5f}")
