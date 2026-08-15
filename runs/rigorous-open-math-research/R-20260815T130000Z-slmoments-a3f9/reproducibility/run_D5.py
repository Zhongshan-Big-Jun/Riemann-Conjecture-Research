from probe_Dk_numerical import measure
import time, sys

# k=5: needs moderate N; use L=30 h=0.05 (N~30), limited samples for runtime
print("=== D5 (validated sampler, L=30 h=0.05) ===", flush=True)
t=time.time()
res = measure(30.0, 0.05, 40, 5, seed=2026)
print(f"E[N]={res['E[N]']:.2f}  ({time.time()-t:.1f}s)", flush=True)
print("  m_k k=1..5: " + " ".join(f"{v:.4f}" for v in res['m_mean']), flush=True)
print(f"  D3={res['D3_mean']:+.5f} +- {res['D3_std']:.5f}", flush=True)
print(f"  D4={res['D4_mean']:+.5f} +- {res['D4_std']:.5f}", flush=True)
print(f"  D5={res['D5_mean']:+.5f} +- {res['D5_std']:.5f}", flush=True)
