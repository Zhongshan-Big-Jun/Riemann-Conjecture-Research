# Audit Report — R-20260815T130000Z-slmoments-a3f9

Independent review of this pass's claims (validated sampler; D_5,D_6≈0 evidence; Hankel decay).
This is a research-pass audit; heavy claims are labeled evidence, not proof.

## A1. Sampler trustworthiness (the critical gate) — VERIFIED
- **Gate B (exact moments)**: the occupancy-kernel discretization A=h·sinc (E[N]=L) reproduces
  m_2≈1.313→4/3, m_3≈1.94→2, m_4≈3.09–3.14→13/4 and E[N]=24.9 (ref 25) at L=25 h=0.05. Confirms the
  probe's validated recipe. The initial diag-1 kernel FAILED (E[N]=27.5); the correction is recorded
  (N1) so it is not reused.
- **Gate A (exact-joint)**: the Kulesza–Taskar sampler reproduces the exact L-ensemble DPP joint
  distribution on small mixed kernels (eigvals in (0,1)) within sampling error (n=5,6). So the
  sampler is distributively correct, not just moment-matched.
- VERDICT: the sampler is trustworthy; D_k/Hankel evidence from it is admissible (unlike the
  defective 7b21e4 sampler).

## A2. D_5, D_6 ≈ 0 (evidence) — CORROBORATED by two independent methods
- MC (validated sampler): D_3=−0.00093±0.0025, D_4=+0.00002±0.0010, D_5=−0.00008±0.00038
  (L=25, ns=120); D_6=+0.00051±0.00040 (L=20, ns=12). All consistent with 0.
- Exact-structure integral (translation-invariant Gauss-Legendre): D_5≈−1e-4…−1.3e-4 over boxes
  R=4..8; D_6≈−4e-7…−1.6e-5 over R=3..5. Both at truncation level ≪ the moments m_5≈5.5,m_6≈9.8.
- VERDICT: **consistent with D_5=D_6=0**, but the exact-0 (box-spline identity / fermionic proof)
  is NOT established — this is the honest residual (Gap 1). No numerical evidence is proof.

## A3. Hankel decay (evidence) — consistent with Λ_m(0)→0
mpmath 50-digit: Λ_1=0.2446, Λ_2=0.1332, Λ_3=0.0916 from the validated sampler's moments. Decaying;
not a float artifact (50-digit recomputation). Still a finite prefix; does not decide the limit.

## A4. Reductions / framework
- exact_moment_decomposition.py reproduces m_2=4/3, m_3=2, m_4=13/4 from the shape constants
  (c_2=1,c_4=2/3,c_6=11/20,S_3=1/15) — the exact framework is consistent with the probe.
- Möbius power-trace grouping (cyclic_all_distinct.py) FAILED direct-enumeration for revisiting
  walks and was discarded (N2); the validated fast evaluator (probe_Dk_fast.py) matches direct
  enumeration exactly for k=3..6 (check_Ck_fast.py).

## Verdict
The new claims are ADDITIVE, adequately validated, and honestly labeled as evidence. The
fermionic conjecture is supported (D_3..D_6 ≈ 0) but not proven; Lemma H (matching-sum→Λ→0)
remains OPEN. No claim of closing SL is made. Status label: **NUMERICAL_EVIDENCE / RIGOROUS_PARTIAL_RESULT** (composite; the reduction is rigorous, the moment progress is evidence).
