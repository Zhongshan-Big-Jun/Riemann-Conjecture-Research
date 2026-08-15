# Repro Manifest — R-20260815T130000Z-slmoments-a3f9

## Run inputs (accepted project facts, audited upstream)
- SL statement + role: condp1 `R-20260814T041219Z-condp1-698ec7/candidate_proof.md` §5; SL-leg.
- Prior pass `R-20260815T120000Z-sllemma-7b21e4` (problem_contract, candidate_proof, audit_report,
  approach_registry, status_and_literature, repro_manifest, obligation_graph).
- Moment model + exact m_1..m_4 + eliminated models + empirical L=50 moments + validated
  projection-DPP discretization recipe:
  `F:\LaTeX\Riemann Conjecture\reports\sl-lemma-random-gram-probe.md` (read in full).
- Exact low moments (1, 4/3, 2, 13/4): condp1 candidate_proof.md §4.

## Tools / versions
- Python `py -3.10`; numpy 2.2.6, scipy 1.15.3, mpmath 1.3.0, sympy 1.13.1 (only numpy+mpmath used).
- Windows PowerShell; env `$env:PYTHONUTF8=1`.

## Sampler validation (MANDATORY before any D_k evidence)
1. Gate A (exact-joint): `py -3.10 sampler_correctness.py` — PASS (sampler reproduces the exact
   L-ensemble DPP joint distribution on small mixed kernels within sampling error).
2. Gate B (exact moments): `py -3.10 gate_target_moments.py` — PASS:
   E[N]=24.9 (ref 25), m2≈1.313 (ref→4/3), m3≈1.94 (ref→2), m4≈3.09-3.14 (ref→13/4) at L=25 h=0.05.
   (The earlier FAIL was the diag-1 occupancy kernel; corrected to A=h·sinc, E[N]=L. Recorded N1.)

## Artifacts / commands
```
cd "...\R-20260815T130000Z-slmoments-a3f9\reproducibility"
# sampler + gates
py -3.10 -u projection_dpp_sampler.py        # self-test prints moments
py -3.10 -u sampler_correctness.py           # Gate A (exact-joint) PASS
py -3.10 -u gate_target_moments.py           # Gate B (exact moments) PASS
py -3.10 -u check_Ck_fast.py                 # fast all-distinct evaluator vs direct (k=3..6)
# extended moments + Hankel
py -3.10 -u extended_moments_hankel.py       # m_1..m_8 at L=50 + Lambda decay (evidence)
# all-distinct D_k probe (validated sampler)
py -3.10 -u probe_Dk_fast.py                 # D_3,D_4,D_5 (L=25) -- D_6 requires longer run
# exact integrals
py -3.10 -u exact_Dk_integral.py             # D_5,D_6 exact-structure integrals (evidence)
py -3.10 -u exact_moment_decomposition.py    # verifies m_2..m_4 exact from shape constants
```

## Results (definitive numbers from this run)
- Gate A/B: PASS (above).
- L=50 extended moments m_1..m_8: (1.00000, 1.32388, 1.97155, 3.18131, 5.45507, 9.80921,
  18.31936, 35.28210); std’s (…0.003,0.011,0.029,0.069,0.163,0.385,0.910); E[N]=50.08.
  [probe ref (1.0,1.322,1.966,3.171,5.435,9.770,18.245,35.148)]
- Hankel (mpmath 50d): Lambda_1=0.24464, Lambda_2=0.13315, Lambda_3=0.09161.
- D_3 = −0.00093 ± 0.00247 ; D_4 = +0.00002 ± 0.00097 ; D_5 = −0.00008 ± 0.00038 (L=25, ns=120).
- D_6 (MC, L=20, ns=12) = +0.00051 ± 0.00040.
- exact D_5 integral (translation-invariant, x5=0, [-R,R]^4): R=4: −8.2e-5, R=6: −1.0e-4, R=8: −2.0e-4.
- exact D_6 integral ([-R,R]^5): R=3: −4.0e-7, R=4: −1.7e-6, R=5: −1.6e-5.
  Both D_5,D_6 exact integrals at truncation level ≪ m_5,m_6 (≈5.5, 9.8) ⇒ consistent with D_5=D_6=0.

## Hashes
Each artifact/source verified (SHA256 in `SHA256SUMS.md` in the run dir). No fabricated numbers;
every number above is produced by the listed scripts and the two mandatory gates passed.

## Unknowns / restrictions
- The exact-0 of D_k (for general k) is NOT proven; it is supported by the above evidence.
- The matching-sum→Hankel lemma (Lemma H) is OPEN.
- The Christoffel atom theorem (pass 7 T0) is used as a cited theorem, not re-derived.
