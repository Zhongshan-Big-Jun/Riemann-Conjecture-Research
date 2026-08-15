import numpy as np
from probe_Dk_fast import C3, C4, C5, C6
from cyclic_all_distinct import C_k_direct

rng = np.random.default_rng(5)
N = 7
G = rng.normal(size=(N,N)); G = G@G.T   # symmetric PSD, small
for k, fn in [(3,C3),(4,C4),(5,C5),(6,C6)]:
    mine = fn(G)
    ref = C_k_direct(G, k)
    ok = abs(mine-ref) < 1e-6*max(1,abs(ref))
    print(f"k={k}: fast={mine:.6f} direct={ref:.6f} {'OK' if ok else 'MISMATCH! diff=%.2e'%abs(mine-ref)}")
