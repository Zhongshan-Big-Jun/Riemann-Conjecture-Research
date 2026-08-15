from probe_Dk_numerical import measure
import time

print("=== D3, D4 sanity (validated sampler) ===", flush=True)
t=time.time()
res = measure(25.0, 0.05, 150, 4)
print(f"E[N]={res['E[N]']:.2f}  ({time.time()-t:.1f}s)", flush=True)
print("  m_k: " + " ".join(f"{v:.4f}" for v in res['m_mean']), flush=True)
for k in range(3, 5):
    print(f"  D{k} = {res[f'D{k}_mean']:+.5f} +- {res[f'D{k}_std']:.5f}", flush=True)
