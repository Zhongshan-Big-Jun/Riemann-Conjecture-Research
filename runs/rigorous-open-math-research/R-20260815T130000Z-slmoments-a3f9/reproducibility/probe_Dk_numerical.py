"""Numerical probe of the all-distinct terms D_5, D_6 (and sanity D_3, D_4) for the sine-DPP
random Gram, using the VALIDATED projection-DPP discretization (projection_dpp_sampler.run).

Definition (per the probe report / task): D_k is the per-unit-L all-distinct contribution to the
moment m_k = (1/N)E[tr G^k], i.e. the expectation over the DPP of the fully-distinct k-cycle sum
  D_k = lim_L (1/L) E[ SUM_{i1,...,ik pairwise distinct} G_{i1i2} G_{i2i3} ... G_{ik i1} ],
with G the Gram matrix (G_ij = sinc(x_i - x_j)) of the sampled points on [0,L].

Measurement: for each DPP sample, compute
  delta_k(G) = (1/N) * Z_k(G),   Z_k(G) := SUM_{i1..ik pairwise distinct (cyclic)} G[i1,i2]...G[ik,i1]
and average over samples. The all-distinct cyclic sum Z_k is evaluated by direct vectorized
enumeration of ordered fully-distinct k-tuples (k=3..6). We also measure tr(G^k)/N for checks.

EVIDENCE ONLY; the definitive statement is the exact computation (exact_rho_k.py).
"""
import numpy as np
import itertools
from projection_dpp_sampler import run, cell_centers

def cyclic_distinct_sum(G, k, rng=None):
    """Z_k = sum over ordered k-tuples (i1..ik) with pairwise-distinct entries of
    G[i1,i2]G[i2,i3]...G[ik,i1]. Enumerated via nested loops over the first k-1 indices and a
    vectorized product over the last. Returns float."""
    N = G.shape[0]
    if N < k:
        return 0.0
    total = 0.0
    if k == 3:
        for a in range(N):
            for b in range(N):
                if a == b: continue
                # last index c != a,b
                mask = np.ones(N, bool); mask[[a,b]] = False
                cs = np.nonzero(mask)[0]
                t = G[a,b]*G[b,cs]*G[cs,a]
                total += t.sum()
    elif k == 4:
        for a in range(N):
            for b in range(N):
                if a==b: continue
                for c in range(N):
                    if c==a or c==b: continue
                    mask = np.ones(N,bool); mask[[a,b,c]]=False
                    ds = np.nonzero(mask)[0]
                    t = G[a,b]*G[b,c]*G[c,ds]*G[ds,a]
                    total += t.sum()
    elif k == 5:
        for a in range(N):
            ca = G[a]
            for b in range(N):
                if b==a: continue
                for c in range(N):
                    if c==a or c==b: continue
                    for d in range(N):
                        if d==a or d==b or d==c: continue
                        mask = np.ones(N,bool); mask[[a,b,c,d]]=False
                        es = np.nonzero(mask)[0]
                        t = G[a,b]*G[b,c]*G[c,d]*G[d,es]*G[es,a]
                        total += t.sum()
    elif k == 6:
        for a in range(N):
            G_a = G[a]
            for b in range(N):
                if b==a: continue
                Gab = G_a[b]
                for c in range(N):
                    if c in (a,b): continue
                    Gbc = G[b,c]
                    for d in range(N):
                        if d in (a,b,c): continue
                        Gcd = G[c,d]
                        for e in range(N):
                            if e in (a,b,c,d): continue
                            mask = np.ones(N,bool); mask[[a,b,c,d,e]]=False
                            fs = np.nonzero(mask)[0]
                            t = Gab*Gbc*Gcd*G[d,e]*G[e,fs]*G[fs,a]
                            total += t.sum()
    else:
        raise NotImplementedError
    return total

def measure(L, h, nsamples, kmax, seed=1234, sample_subset='dpp'):
    """Measure D_k and m_k from validated DPP samples via the shape route.
    Returns dict with E[N], m_k means/stds and D_k means/stds.
    sample_subset selects which DPP sampling (default the validated projection_dpp_sampler.run
    is NOT reused here because we need the raw point sets, so we re-implement sampling inline).
    """
    from projection_dpp_sampler import sample_points, kernel_matrix, trace_moments, build_gram
    rng = np.random.default_rng(seed)
    xs, n = cell_centers(L, h)
    Kg = kernel_matrix(xs)
    A = h * Kg
    A = (A + A.T) * 0.5
    accD = {k: 0.0 for k in range(3, kmax+1)}
    accD2 = {k: 0.0 for k in range(3, kmax+1)}
    accM = np.zeros(kmax)
    accM2 = np.zeros(kmax)
    Ns = np.zeros(nsamples)
    for s in range(nsamples):
        sel, r = sample_points(A, rng)
        N = len(sel)
        Ns[s] = N
        if N >= kmax:
            G = build_gram(xs[sel], xs)
            m = trace_moments(G, kmax)
            accM += m; accM2 += m*m
            for k in range(3, kmax+1):
                if N >= k:
                    z = cyclic_distinct_sum(G, k)
                    d = z / N
                    accD[k] += d; accD2[k] += d*d
    out = {}
    out['E[N]'] = Ns.mean()
    out['m_mean'] = accM/nsamples
    out['m_std'] = np.sqrt((accM2/nsamples - (accM/nsamples)**2)/nsamples)
    for k in range(3, kmax+1):
        mmean = accD[k]/nsamples
        mvar = (accD2[k]/nsamples) - mmean*mmean
        out[f'D{k}_mean'] = mmean
        out[f'D{k}_std'] = np.sqrt(np.clip(mvar,0,None)/nsamples)
    return out

if __name__ == "__main__":
    import sys
    # small-fast passes first for k=3,4 trust, then k=5,6
    for (L, h, ns, kmax) in [(25.0, 0.05, 120, 4), (30.0, 0.05, 60, 5), (30.0, 0.05, 30, 6)]:
        print(f"=== L={L} h={h} nsamples={ns} kmax={kmax} ===", flush=True)
        res = measure(L, h, ns, kmax)
        print(f"  E[N] = {res['E[N]']:.2f}")
        print("  m_k (k=1..kmax): " + " ".join(f"{v:.4f}" for v in res['m_mean']))
        for k in range(3, kmax+1):
            print(f"  D{k} = {res[f'D{k}_mean']:+.5f} +- {res[f'D{k}_std']:.5f}")
        print(flush=True)
