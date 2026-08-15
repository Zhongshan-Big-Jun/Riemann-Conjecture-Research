# Probe the sine-DPP Gram moment structure: do the "all-distinct" / non-repeated index
# interaction terms D_k vanish for ALL k (as they do for k=3,4 where D_3=D_4=0)?
# If D_k=0 for all k, the moments come from a cleaner repeated-index combinatorics.
# Evidence only (Monte-Carlo); clearly labeled.
import numpy as np

rng = np.random.default_rng(1234)

# ---- Projection-DPP sampler for the sine kernel on [0,L] (discretization h).
# We sample the sine DPP restricted to a grid {0,h,...,N-1 h} with the discrete projection
# kernel (the discretized sinc, bandwidth ~1/2). We keep points, build their Gram.
def sample_sine_dpp(L, h):
    n = int(round(L/h))
    xs = (np.arange(n)+0.5)*h   # cell centers
    # discrete kernel: sinc(xs_i - xs_j), but for a *projection DPP on the cell basis* the 
    # relevant PSD kernel has eigenvalues in {0,1}. Use the CDF-based trick actually used by
    # Hough et al./standard DPP sampler with the matrix of pairwise sinc -> but to make it a
    # rank-limited projection we diag the Gram of sinc on the grid and threshold.
    K = np.empty((n,n))
    d = xs[:,None]-xs[None,:]
    K = np.sinc(d)  # sin(pi x)/(pi x)
    # Project onto the band-limited subspace: eigen-decompose, keep eigenvalues ~ near 1 (the
    # discretized projection). This reproduces the projection-DPP discretization used in the probe.
    w,V = np.linalg.eigh(K)
    # sine projection: eigenvalues cluster at 0 and 1 in the continuum; in discrete the top
    # ~L*? eigenvalues ~1. Keep all (it's already PSD, a valid DPP kernel if <=1). Clamp to [0,1].
    w = np.clip(w, 0.0, 1.0)
    K = (V*w)@V.T  # PSD with eigenvalues in [0,1] -> valid DPP kernel
    # Determinantal sampling (Hough-Lawler-Karasev / DPP sampler via joint distribution):
    idx = _dpp_sample(K, rng)
    return xs[idx]

def _dpp_sample(K, rng):
    n = K.shape[0]
    w,V = np.linalg.eigh(K)
    # elementary symmetric sampling in the eigenbasis (V-assisted, classic DPP sampler)
    sel=[]
    # project: the DPP chooses a subset; use the projective sampler on eigenbasis
    # Bernoulli-ish on eigenvectors weighted by w in {0,1} end:
    keep = rng.random(n) < w
    E = V[:, keep]  # orthonormal-ish columns
    # now iterative slice sampler over the orthonormal frame
    cols = list(E.T)
    chosen=[]
    for col in cols:
        U = np.array(cols)
        # classic: pick index with prob |col|^2, orthogonalize others
        probs = col**2
        p = probs/probs.sum()
        i = rng.choice(n, p=p)
        chosen.append(i)
        # Gram-Schmidt remove component along col from remaining
        for j in range(len(cols)):
            cols[j] = cols[j] - (cols[j]@col)*col
        # proceed; we'll just gather chosen set
    return np.unique(np.array(chosen))

# ---- Simulate and measure m_k and, via a correlation decomposition, the "fully distinct" part.
def measure(L, h, nsamples, kmax=6):
    m = np.zeros(kmax)
    # To isolate the all-distinct term we can't easily split inside; instead we compare m_k against
    # the value predicted IF only repeated-index shapes contribute (D_k extrapolated). Instead we
    # directly compute E[tr G^k] and separately the "no repeated index" projection is hard.
    # We'll just report raw m_k and the ratio m_k/(m_{k-1}) to see growth.
    acc = np.zeros(kmax)
    for s in range(nsamples):
        xs = sample_sine_dpp(L, h)
        N = len(xs)
        G = np.sinc(xs[:,None]-xs[None,:])
        for k in range(1, kmax+1):
            acc[k-1] += np.trace(np.linalg.matrix_power(G,k))/N
    return acc/nsamples, nsamples

L=50; h=0.1; ns=60
m, ns = measure(L,h,ns,6)
print(f"DPP sim L={L} h={h} ns={ns}: raw E[N] per sample check below")
print("E[m_k] k=1..6:", np.round(m,4))
print("ratios m_k/m_{k-1}:", np.round(m[1:]/np.maximum(m[:-1],1e-9),4))
print("reference exact: m2=1.3333 m3=2.0 m4=3.25")
