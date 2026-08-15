# Whiteboard — R-20260815T130000Z-slmoments-a3f9 (SL moment route)

- **Run ID:** `R-20260815T130000Z-slmoments-a3f9`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5`
- **Last updated:** `2026-08-16T01:45:00Z`

## Current plan

RUN COMPLETE (2026-08-16): NUMERICAL_EVIDENCE / RIGOROUS_PARTIAL_RESULT (composite). The
moment/fermionic route toward SL is strongly supported but not closed. Standing rigorous
reduction (pass 7b21e4, audited): SL ⟺ μ_λ({0}) = 0 ⟺ Λ_m(0) = det(H_m)/det(H_m⁽⁰⁰⁾) → 0.
This pass: (1) validated a faithful projection-DPP sampler on two gates; (2) produced first
trustworthy D₃–D₆ ≈ 0 evidence (fermionic/Wick through k=6); (3) Hankel decay evidence;
(4) formulated the closing-lemma framework M → P → H → SL with gaps G1/G2/G3. Next steps
(not part of this run): G1 exact D_k=0 proof (quasi-free fermion literature angle);
G3 (Lemma H) is the hard step.

## Route history

- Sampler reconstruction + validation `[SUCCEEDED]`: occupancy kernel A = h·sinc(x_i−x_j)
  (E[N]=L) is the correct discretization; the naive diag-1 kernel FAILS (E[N]=27.5). Gate A
  (exact-joint, L-ensemble law vs Kulesza–Taskar sampler within sampling error) PASS; Gate B
  (exact moments m₂→4/3, m₃→2, m₄→13/4 within h-bias) PASS. (Independent manager rerun of
  Gate A: per-set deviations 0.0017/0.0015 at 150k/120k draws — PASS.)
- D_k measurement (MC, validated sampler) `[SUCCEEDED]`: D₃=−0.0009±0.0025,
  D₄=+0.0000±0.0010, D₅=−0.00008±0.00038 (L=25), D₆=+0.0005±0.0004 (L=20) — all consistent
  with 0.
- Exact-structure integrals `[SUCCEEDED]`: translation-invariant Gauss box
  integrals give D₅ ≈ −1e-4, D₆ ≈ −1e-5…−1.6e-5 — ~4 orders below m₅≈5.5, m₆≈9.8.
- Extended-moment Hankel decay `[SUCCEEDED]`: Λ₁=0.245, Λ₂=0.133, Λ₃=0.092
  (L=50 moments, mpmath 50d) — decaying, consistent with Λ_m(0)→0.
- Exact-0 rational proof of D₅ `[BLOCKED]`: the 4-D all-distinct integrand reduces
  to a computable Gauss box integral (≈ −1e-4) but a rigorous exact-0 rational proof was not
  achieved in budget; recorded as the natural next exact target.
- Literature angle (quasi-free fermion / fermion point process) [PARTIAL]: identified as a potential existing proof of D_k=0; not yet searched in this pass.
  quasi-free fermion states may already prove D_k=0 ("quasi-free fermion point process
  truncated correlations").

## Ideas to return to

- Exact-0 rational proof of D_5 via the computable translation-invariant Gauss box integral
  (value ≈ −1e-4, truncation-level).
- Quasi-free fermion / fermion-point-process literature for a possible existing D_k=0 proof.
- Larger windows (L=100+) to test Λ_m(0) decay at higher m (evidence only; conditioning
  caveat at large m — stable determinant algorithms).
- The occupancy-kernel discretization lesson (A = h·sinc vs diag-1) for future DPP
  simulations in this project.

## Open obligations

- G1 (Lemma M): prove D_k = 0 exactly for all k ≥ 3 (D_3, D_4 exact; D_5, D_6 evidence only).
- G2 (Lemma P): prove the only surviving m_k shapes are the size-≤2 matched blocks.
- G3 (Lemma H): prove the matching-sum moment sequence has Λ_m(0) → 0 (determinacy +
  Hankel asymptotic / Szegő–Widom) — the hard step; closes SL via T0/T1.
- SL itself and the unconditional liminf N₀ˢ/N → 1 remain OPEN.

## Key artifacts

- `runs/.../slmoments-a3f9/problem_contract.md` — pass contract (SL via exact moments).
- `runs/.../slmoments-a3f9/candidate_proof.md` — composite status; Lemma M/P/H framework;
  sha256 DD12111D...
- `runs/.../slmoments-a3f9/research_ledger.md` — chronological steps incl. sampler
  reconstruction; sha256 FC76C13C...
- `runs/.../slmoments-a3f9/reproducibility/projection_dpp_sampler.py` — validated sampler;
  sha256 B33E0DC9...
- `runs/.../slmoments-a3f9/reproducibility/sampler_correctness.py` + `gate_target_moments.py`
  — Gates A/B.
- `runs/.../slmoments-a3f9/reproducibility/probe_Dk_fast.py` + `check_Ck_fast.py` — D_k MC.
- `runs/.../slmoments-a3f9/reproducibility/exact_Dk_integral.py` + `exact_D5_integral.py` —
  exact-structure Gauss integrals.
- `runs/.../slmoments-a3f9/reproducibility/extended_moments_hankel.py` — Hankel decay.
- Full hash list: `runs/.../slmoments-a3f9/SHA256SUMS`.
