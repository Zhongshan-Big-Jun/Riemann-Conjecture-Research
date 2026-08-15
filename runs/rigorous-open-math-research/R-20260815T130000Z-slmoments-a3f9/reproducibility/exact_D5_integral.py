"""Vectorized high-precision numerical evaluation of D_5 = (1/L) int P * rho_5 (all-distinct term).
Translation-invariant: set x5=0, integrate x1..x4 over R^4 on a large box, Gauss-Legendre tensor.
Vectorized so all nodes are evaluated at once. EVIDENCE that D_5 ~ 0 if the fermionic cancellation
holds. Not a proof.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss

def sinc(t):
    t = np.asarray(t, dtype=float)
    out = np.ones_like(t)
    nz = np.abs(t) > 1e-12
    out[nz] = np.sin(np.pi*t[nz])/(np.pi*t[nz])
    return out

def rho5(X):
    K = sinc(X[:,None]-X[None,:])
    return np.linalg.det(K)

def integrand_vec(y4grid):
    """y4grid: shape (...,4). Returns P*rho5 per point."""
    shape = y4grid.shape[:-1]
    X = np.concatenate([y4grid, np.zeros(shape+(1,))], axis=-1)  # (...,5)
    # P = K(x1,x2)K(x2,x3)K(x3,x4)K(x4,x5)K(x5,x1)
    f = [1,2,3,4, 0]
    s = [0,1,2,3, 4]
    P = np.ones(shape)
    for a in range(5):
        i,j = s[a], f[a]
        P = P * sinc(X[...,i]-X[...,j])
    # rho5 per point: det of 5x5 sinc matrix
    # build per-point 5x5
    # vectorized det via explicit cofactor-free? use np.linalg.det on stacked 5x5
    Kmat = sinc(X[...,:,None]-X[...,None,:])   # (...,5,5)
    rho = np.linalg.det(Kmat)
    return P*rho

def quad4(R, nperdim=22):
    nodes, w = leggauss(nperdim)
    x = 0.5*R*(nodes+1); wm = 0.5*R*w
    g = np.meshgrid(x,x,x,x, indexing='ij')
    y4 = np.stack(g, axis=-1).reshape(-1,4)   # (n^4,4)
    val = integrand_vec(y4)
    # weights tensor
    W = 1.0
    for _ in range(4):
        W = np.multiply.outer(W, wm)
    W4 = W.reshape(-1)
    return float(np.sum(val*W4))

if __name__ == "__main__":
    import time
    for R in [4,6,8]:
        t=time.time(); v=quad4(R,22)
        print(f"R={R}: D5_int={v:+.9e} (t={time.time()-t:.0f}s)", flush=True)
