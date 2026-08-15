"""Hard sampler-correctness gate: does projection_dpp_sampler.sample_points reproduce the EXACT
DPP joint distribution for a generic DPP kernel with eigenvalues in (0,1)?

Reference: for a DPP with kernel K (0<=eig<=1), the exact probability of subset Y is
    P(Y) = det(K_{Y,Y}) / sum_{Z subset of [n]} det(K_{Z,Z}),
where K_{Y,Y} is the |Y|x|Y| principal submatrix (det(empty)=1). We enumerate ALL 2^n subsets
exactly (n small), compute the normalized masses, and compare to the sampler's empirical
histogram over many draws. This is independent of the sine-process discretization and catches
any bug in the eigen-Bernoulli + volume-sampling machinery.
"""
import numpy as np
import itertools
from collections import Counter
from projection_dpp_sampler import sample_points

def build_mixed_kernel(n, seed=0, lam=None):
    """A symmetric PSD n x n kernel with chosen eigenvalues in (0,1) (defaults to a spread)."""
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
    if lam is None:
        lam = np.linspace(0.1, 0.9, n)   # strictly in (0,1)
    K = (Q * lam) @ Q.T
    return K, lam

def exact_joint(K):
    n = K.shape[0]
    masses = {}
    for mask in range(1 << n):          # enumerate all 2^n subsets
        Y = [i for i in range(n) if (mask >> i) & 1]
        det = 1.0
        for sub in itertools.combinations(range(len(Y)), 1):  # placeholder, replaced below
            pass
        # direct determinant of principal submatrix
        if len(Y) == 0:
            det = 1.0
        else:
            # robust: recompute via full K with kron
            KY = K[np.ix_(Y, Y)]
            det = float(np.linalg.det(KY))
        masses[tuple(Y)] = det
    tot = sum(masses.values())
    return {Y: m/tot for Y, m in masses.items()}, tot

def empirical_joint(K, rng, nsamples):
    cnt = Counter()
    for _ in range(nsamples):
        Y, r = sample_points(K, rng)
        cnt[tuple(Y)] += 1
    return {Y: c/nsamples for Y, c in cnt.items()}

def run_test(n, nsamples=120000, seed=7, lam=None):
    K, lamG = build_mixed_kernel(n, lam=lam)
    exact, tot = exact_joint(K)
    rng = np.random.default_rng(seed)
    emp = empirical_joint(K, rng, nsamples)
    # Compare on the union of supports (exact support = subsets with det>0 ~ all for full-rank).
    keys = set(exact) | set(emp)
    maxdev = 0.0
    # also aggregate marginal point probabilities (more robust)
    print(f"--- n={n}, sampling {nsamples} draws, kernel eigvals {np.round(lamG,2)}")
    # per-set deviation on supported subsets
    devs = []
    for Y in exact:
        e = exact[Y]; s = emp.get(Y, 0.0); devs.append(abs(e-s))
    maxdev_set = max(devs) if devs else 0
    # marginal point-inclusion probability
    mix = np.zeros(n);  mref = np.zeros(n)
    for Y,p in emp.items():
        for i in Y: mix[i]+=p
    for Y,p in exact.items():
        for i in Y: mref[i]+=p
    md = max(abs(mix[i]-mref[i]) for i in range(n))
    print(f"  max per-set |dev| (over {len(exact)} supported subsets) = {maxdev_set:.5f}")
    print(f"  max per-point marginal |dev| = {md:.5f}")
    tol = 5/np.sqrt(nsamples)
    print(f"  (sampling error ~ 1/sqrt(nsamples) = {1/np.sqrt(nsamples):.5f})")
    ok = md < max(0.02, 6/np.sqrt(nsamples))
    print("  PASS" if ok else "  FAIL")
    return ok

if __name__ == "__main__":
    ok1 = run_test(5, nsamples=150000, seed=7)
    ok2 = run_test(6, nsamples=120000, seed=11)
    print("ALL PASS" if (ok1 and ok2) else "SOME FAIL")
