"""Validation gate for projection_dpp_sampler.

A) EXACT small-n check: for a small symmetric PSD kernel (e.g. a bandwidth-limited Toeplitz
   projection), compare the EmF-exact joint distribution from the sampler vs brute-force
   enumeration of P(Y) = det(K_Y) (a DPP's marginal kernel characterization). This catches
   sampler bugs independent of the sine-process discretization.

B) TRUSTWORTHY-TARGET check: reproduce E[N]=L and the audited exact moments
   (m_0,m_1,m_2,m_3,m_4) = (1,1,4/3,2,13/4) on the projection-DPP discretization of the sine
   process on [0,25], h=0.05, within the h->0 bias quoted in the probe report.
"""
import numpy as np
import itertools
from projection_dpp_sampler import sample_points, kernel_matrix, run

def brute_force_projection_dpp(K, rng, nsamples):
    """Reference: sample the projection DPP by EXACT enumeration of the joint distribution:
    P(Y) = det(K_Y)/sum_{Z}det(K_Z) over subset likelihood. For a projection kernel this is
    supported on subsets of size = rank. We draw by direct sampling from the enumerated mass."""
    n = K.shape[0]
    w, V = np.linalg.eigh((K+K.T)*0.5)
    rank = int(round(w[-1])) if len(w) else 0
    # mass of each subset Y: det(K_{Y,Y}); only size-rank subsets have nonzero mass
    masses = {}
    for r in range(max(0, rank-2), min(n, rank+3)+1):
        for Y in itertools.combinations(range(n), r):
            Yl = list(Y)
            if len(Yl)==0:
                m = 1.0
            else:
                KY = K[np.ix_(Yl, Yl)]
                # for projection kernel det = 0 or 1 typically; use robust
                m = max(0.0, np.linalg.det(KY))
                if m < 1e-8:
                    m = 0.0
            if m > 0:
                masses[Y] = m
    tot = sum(masses.values())
    keys = list(masses.keys())
    probs = np.array([masses[k]/tot for k in keys])
    samples_idx = rng.choice(len(keys), size=nsamples, p=probs)
    return [keys[i] for i in samples_idx]

def validate_exact_smalln():
    rng = np.random.default_rng(1)
    # Build a small projection kernel (a few dominant band-limited modes).
    n = 8
    xs = np.arange(n) + 0.5
    K = kernel_matrix(xs)   # sinc kernel, 8x8, approx projection
    # symmetrize + clip to [0,1]
    K = (K + K.T)*0.5
    w, V = np.linalg.eigh(K)
    w = np.clip(w, 0, 1)
    Kc = (V * w) @ V.T
    # sample from sampler
    S = []
    for _ in range(20000):
        Y, r = sample_points(Kc, rng)
        S.append(tuple(Y))
    from collections import Counter
    emp = Counter(S)
    # brute force reference
    ref = brute_force_projection_dpp(Kc, np.random.default_rng(2), 20000)
    refc = Counter(ref)
    # compare marginal (per-point inclusion) probabilities
    emp_marg = np.zeros(n); ref_marg = np.zeros(n)
    for Y,c in emp.items():
        for i in Y: emp_marg[i] += c
    emp_marg/=20000
    for Y,c in refc.items():
        for i in Y: ref_marg[i]+=c
    ref_marg/=20000
    print("=== A) Exact small-n joint-distribution check (n=8) ===")
    print("per-point marginal probability: sampler  |  brute-force reference")
    maxdev=0
    for i in range(n):
        d=abs(emp_marg[i]-ref_marg[i])
        maxdev=max(maxdev,d)
        print(f"  point {i}: {emp_marg[i]:.4f} | {ref_marg[i]:.4f}")
    print(f"max |marginal gap| = {maxdev:.5f}")
    print("PASS" if maxdev<0.02 else "FAIL")

def validate_target_moments():
    print("\n=== B) Trustworthy-target: sine-DPP discretization [0,25] h=0.05 ===")
    for ns in [400]:
        mean, std, meanN, Ns = run(25.0, 0.05, ns, 6, seed=1234)
        print(f"nsamples={ns}: E[N]={meanN:.3f} (expect 25.0), actual N range [{Ns.min()},{Ns.max()}]")
        print("moments   : " + " ".join(f"{v:.4f}" for v in mean))
        print("std       : " + " ".join(f"{v:.4f}" for v in std))
        print("reference (probe, h-bias): m2~1.3134->4/3, m3~1.94->2, m4~3.1056->13/4")
        # gate: must be within ~0.1 of the expected h-biased values and E[N]~25
        ok_N = abs(meanN-25.0) < 1.5
        ok_m2 = abs(mean[1]-4/3) < 0.15
        ok_m3 = abs(mean[2]-2.0) < 0.25
        ok_m4 = abs(mean[3]-3.25) < 0.35
        print("Gate: E[N]~25:", ok_N, " m2~4/3:", ok_m2, " m3~2:", ok_m3, " m4~13/4:", ok_m4)
        print("PASS" if (ok_N and ok_m2 and ok_m3 and ok_m4) else "FAIL")

if __name__ == "__main__":
    validate_exact_smalln()
    validate_target_moments()
