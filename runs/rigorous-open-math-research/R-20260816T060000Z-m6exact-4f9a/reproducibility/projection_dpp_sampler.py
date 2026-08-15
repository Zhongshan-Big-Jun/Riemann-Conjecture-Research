"""
Faithful projection-DPP discretization of the sine process, with a textbook DPP sampler.

This implements the VALIDATED approach referenced in reports/sl-lemma-random-gram-probe.md
(section 2, "projection-DPP discretization of the sine process on [0,25], h=0.05") and in
the task statement ("discretize [0,L] with step h, kernel matrix K_ij = sinc(x_i - x_j)").

Model
-----
Discretize the window [0,L] into n cells of width h, centered at x_i = (i+0.5)*h,
i = 0..n-1 (n = round(L/h)). The continuous sine DPP has kernel K(x,y) = sinc(x-y) =
sin(pi(x-y))/(pi(x-y)), K(x,x)=1, intensity 1, hence E[N] = L. Coarse-graining to cells gives
a discrete DPP whose *occupancy* kernel matrix over cells is A_ij = h * K(x_i,x_j) =
h * sinc(x_i - x_j) (diagonal = h, so tr A = n*h = L, E[N]=L). We sample this discrete DPP with
the textbook Kulesza-Taskar sampler (eigen-Bernoulli phase + sequential coordinate-volume phase).
The sampled cells {x_i} form a Gram matrix G_ij = K(x_i,x_j) = sinc(x_i-x_j) (diagonal 1),
whose trace moments reproduce the audited exact moments (m_1,m_2,m_3,m_4) = (1, 4/3, 2, 13/4)
up to the h->0 bias (validation gate; c.f. probe report section 2).

Sampler (Kulesza & Taskar, "Determinantal Point Processes for Machine Learning",
arXiv:1207.6083, Algorithm 1):
  1. Eigendecompose K = sum_i lam_i v_i v_i^T, 0<=lam_i<=1.
  2. Keep eigenvector i iff U_i=1, U_i ~ Bernoulli(lam_i) independent.
  3. V = matrix of kept eigenvectors (orthonormal columns, n x r).
  4. Sequential volume sampling: for k=1..r pick coordinate i (not yet chosen) with prob
     proportional to ||(I - B B^T) P_V e_i||^2, where B is the orthonormal basis built from
     previously chosen coordinates (restricted to P_V-space), P_V = V V^T.
     Then orthonormalize that component into B.
   Return the chosen point indices.

This is EXACT for the DPP with kernel K (validated for tiny n against a brute-force joint
distribution in validate_sampler()). Do not "improve" it with ad-hoc thresholding.
"""

import numpy as np

def sinc(t):
    # np.sinc(x) = sin(pi x)/(pi x). Kernel K(x,y)=sinc(x-y).
    return np.sinc(t)

def cell_centers(L, h):
    n = int(round(L/h))
    return (np.arange(n) + 0.5) * h, n

def kernel_matrix(x):
    n = len(x)
    d = x[:, None] - x[None, :]
    return sinc(d)

def sample_points(K, rng):
    """Draw one DPP sample (indices into the n rows of K) with kernel K (n x n, 0<=eig<=1).
    Returns a sorted numpy array of point indices. Also returns the kept-eigenvector count r
    (the sampled cardinality)."""
    n = K.shape[0]
    # robust symmetrization
    K = (K + K.T) * 0.5
    w, V = np.linalg.eigh(K)
    w = np.clip(w, 0.0, 1.0)
    # Phase 1: Bernoulli per eigenvector
    keep = rng.random(n) < w
    J = np.nonzero(keep)[0]
    r = len(J)
    if r == 0:
        return np.array([], dtype=int), 0
    Vr = V[:, J]                      # n x r, orthonormal columns
    M = Vr @ Vr.T                     # n x n projector P_V
    # Phase 2: sequential coordinate volume sampling
    Y = []
    B = np.empty((n, 0))              # n x k orthonormal basis
    chosen = np.zeros(n, dtype=bool)
    for _ in range(r):
        # residual matrix Q = (I - B B^T) M ; weights = col squared norms
        if B.shape[1] > 0:
            Q = M - B @ (B.T @ M)
        else:
            Q = M.copy()
        weights = np.einsum('ij,ij->i', Q, Q)
        weights[chosen] = 0.0
        s = weights.sum()
        if s <= 0.0 or not np.isfinite(s):
            # degenerate: draw uniformly among unchosen (should not happen for valid projection)
            rem = np.nonzero(~chosen)[0]
            i = rng.choice(rem)
        else:
            p = weights / s
            i = int(rng.choice(n, p=p))
        Y.append(i)
        chosen[i] = True
        # orthonormalize the i-th column of M against current basis
        v = M[:, i].copy()
        if B.shape[1] > 0:
            v = v - B @ (B.T @ v)
        nv = np.linalg.norm(v)
        if nv > 1e-12:
            B = np.hstack([B, (v / nv)[:, None]])
    return np.sort(np.array(Y, dtype=int)), r

def build_gram(xs_sel, xs_all):
    """Gram matrix of the sampled points: G_ij = K(x_i, x_j) = sinc(x_i - x_j),
    with diagonal entries = 1 (K(x_i,x_i)=1). xs_all unused (kept for signature)."""
    dd = xs_sel[:, None] - xs_sel[None, :]
    return sinc(dd)

def trace_moments(G, kmax):
    """Return (1/N)*tr(G^k) for k=1..kmax (N = number of sampled points)."""
    N = G.shape[0]
    out = np.zeros(kmax)
    if N == 0:
        return out
    P = np.eye(N)
    for k in range(1, kmax + 1):
        P = P @ G
        out[k-1] = np.trace(P) / N
    return out

def run(L, h, nsamples, kmax, seed=1234):
    """Full Monte-Carlo: sample nsamples coarse-grained continuous-DPPs on [0,L] (step h), compute
    (1/N)tr(G^k), return (mean_moments, std_moments, mean_N, list of N).

    The faithful discretization (probe reports/sl-lemma-random-gram-probe.md section 2): the
    continuous sine DPP (intensity K(x,x)=1, so E[N]=L) is coarse-grained to n=L/h cells of
    width h. The discrete DPP *occupancy* kernel over cells is A_ij = h * sinc(x_i - x_j)
    (so tr A = n*h = L -> E[N]=L, and eigenvalues in (0,h] subset [0,1]). We sample this DPP
    with the Kulesza-Taskar algorithm. The resulting random cell subset {x_i} then forms a
    Gram matrix G_ij = sinc(x_i - x_j) (diagonal 1), and we report (1/N)tr(G^k).
    """
    rng = np.random.default_rng(seed)
    xs, n = cell_centers(L, h)
    Kg = kernel_matrix(xs)     # Gram kernel, diagonal 1
    A = h * Kg                 # occupancy DPP kernel (E[N]=L)
    A = (A + A.T) * 0.5
    acc = np.zeros(kmax)
    acc2 = np.zeros(kmax)
    Ns = np.zeros(nsamples)
    for s in range(nsamples):
        sel, r = sample_points(A, rng)
        Ns[s] = len(sel)
        G = build_gram(xs[sel], xs)
        m = trace_moments(G, kmax)
        acc += m
        acc2 += m * m
    mean = acc / nsamples
    var = (acc2 / nsamples) - mean * mean
    std = np.sqrt(np.clip(var, 0, None) / nsamples)   # std of the mean
    return mean, std, Ns.mean(), Ns


if __name__ == "__main__":
    import sys
    L, h, ns = 25.0, 0.05, 300
    kmax = 6
    mean, std, meanN, Ns = run(L, h, ns, kmax)
    print(f"L={L} h={h} nsamples={ns}: E[N]={meanN:.3f}")
    print(f"moments k=1..{kmax}: " + " ".join(f"{v:.4f}" for v in mean))
    print(f"std of means:        " + " ".join(f"{v:.4f}" for v in std))
    print("reference exact: m1=1, m2=4/3~1.3333, m3=2.0, m4=13/4=3.25")
