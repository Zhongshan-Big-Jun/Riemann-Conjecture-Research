"""Exact-structure high-precision numerical evaluation of the all-distinct term
D_k = (1/L) int_{[0,L]^k} P_k(x) * rho_k(x) dx,  P_k = prod_{a=1..k} K(x_a,x_{a+1}),
rho_k = det[K(x_p,x_q)] (DPP k-correlation), K = sinc.

Translation invariance: set x_k = 0, integrate the k-1 relative coordinates x_1..x_{k-1} over R^{k-1}
with a vectorized Gauss-Legendre tensor (probe_Dk style). EVIDENCE for D_k ~ 0.

Note: box truncation of the slow-decaying sinc tail causes an O(1e-4..1e-3) residual for the exact
0 case; we report the value and its box dependence.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss

def NCsinc(t):
    t = np.asarray(t, dtype=float)
    out = np.ones_like(t)
    nz = np.abs(t) > 1e-12
    out[nz] = np.sin(np.pi*t[nz])/(np.pi*t[nz])
    return out

def Dk_integral(k, R, nperdim):
    """Evaluate D_k over [-R,R]^k via Gauss-Legendre tensor (vectorized), x_k=0."""
    nodes, w = leggauss(nperdim)
    x = 0.5*R*(nodes+1); wm = 0.5*R*w
    dims = [x]*(k-1)
    g = np.meshgrid(*dims, indexing='ij')
    y = np.stack(g, axis=-1).reshape(-1, k-1)   # (n^(k-1), k-1)
    # X = (x1..x_{k-1}, 0)
    shape = y.shape[:-1]
    X = np.concatenate([y, np.zeros(shape+(1,))], axis=-1)  # (...,k)
    # P_k = prod over cycle edges
    P = np.ones(shape)
    for a in range(k):
        i = a; j = (a+1) % k
        P = P * NCsinc(X[...,i]-X[...,j])
    # rho_k = det[K(xp,xq)]
    K = NCsinc(X[...,:,None]-X[...,None,:])
    rho = np.linalg.det(K)
    val = P*rho
    # weight tensor (n^(k-1))
    W = np.array([1.0])
    for _ in range(k-1):
        W = np.multiply.outer(W, wm)
    Wf = W.reshape(-1)
    return float(np.sum(val*Wf))

if __name__ == "__main__":
    import sys
    for k, Rlist, nper in [(5,[4,6,8],18),(6,[3,4,5],12)]:
        print(f"=== D{k} exact integral ===", flush=True)
        for R in Rlist:
            v = Dk_integral(k, R, nper)
            print(f"  R={R}: D{k} = {v:+.8e}", flush=True)
