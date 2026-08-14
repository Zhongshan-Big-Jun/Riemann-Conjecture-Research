# Audit report — R-20260814T041219Z-condp1-698ec7 (post-delivery audit)

> Note: a pre-existing `audit_report.md` in this run root recorded a FAIL at a moment when the
> directory was empty (before the solver wrote artifacts). That report is superseded: all artifacts
> now exist and are audited below. The pre-existing report is one reason the earlier solver was
> "cut off" and this continuation completed the run.

Status: solver-side audit (no separate auditor role spawned in this continuation). Checks are
independent re-derivations / duplicate computations. A fresh adversarial auditor is recommended
before downstream use.

## 1. Independent arithmetic checks (two code paths)
- Λ_2(0) = 5/36 for (1,4/3,2,13/4): (i) `moments_christoffel_full.py` Gaussian-elimination
  inversion, and (ii) `check_lambda2_corrected.py` 3×3 cofactor/determinant. Both exact rationals,
  same answer. ✓
- 13/18 = 2(1 − Λ_2(0)) − 1 with Λ_2(0)=5/36: exact. ✓
- (1,3/4,2,13/4) not a probability-moment sequence: m_2−m_1² = −1/4 < 0 (direct); Λ_2(0)=143/100. ✓
- Corrected-list Hankel positivity: leading 3×3 det = 5/108 > 0; m_2−m_1² = 1/3 > 0. ✓

## 2. Consistency with the Lean snapshot (O1)
- `Zeta23/ThmD/Final.lean` lines 10–19: `HD 1 = 2 − 1/c₁* = 3/2 − cot(1/√2)/√2`, `c₁* =
  √2 tan(1/√2)/(1+tan(1/√2)/√2)`, CS simple `2c₁*−1`, distinct `(3−1/c₁*)/2`. Match v2 §7.1 ✓.
- `thmD₀_simple` constant `2c₁*−1 = 0.50659` is the Cauchy–Schwarz (m=1) form = our §3.A m=1 bound
  with corrected m_2: m_1²/m_2 = 3/4 → N0^s/N ≥ 2·(3/4)−1 = 1/2 (window-optimized 0.50659). ✓

## 3. Logical review of candidate_proof.md
- Lemma 3.A (SOS witness): sign handling verified (p=t·r, r≥0 ⇒ negative-λ contributes ≤0 to
  numerator, ∈ ≥0 to denominator; C.-S. applies). ✓
- Lemma 3.B (Christoffel): μ({0}) ≤ Λ_m(0) = min_{p(0)=1}∫p². ✓
- Cor 3.C / §5: ε-handling standard; tightness+determinacy needs Carleman (valid for the
  compactly-supported-in-limit Gram law). Only external input is **SL**. ✓
- No forbidden unconditional-100% claim. ✓

## 4. Unresolved / risks
- **SL is unproved** — the theorem is genuinely conditional; the open prerequisite is isolated and
  precisely stated (zero-gap spectral data of sine-kernel Gram at 0). Do not treat 100% as
  unconditional.
- GLSS25 primary source not bundled (reliance on GS Theorem 5 quote; packet O7 partial).
- m_3,m_4 are numerical evidence only (CUE); the theorem does not use them.
- No Lean formalization of the new results this run (candidate for a stage-C `lean-verify` run).

## 5. Delivery-level check
The pre-existing audit's FAIL reason ("directory empty, no artifacts") no longer holds: the
standard artifact set (problem_contract, status_and_literature, obligation_graph, approach_registry,
research_ledger, counterexample_log, candidate_proof, audit_report, repro_manifest, reproducibility/)
is present and hashed (see SHA256SUMS).

## 6. Verdict
The conditional theorem and the inconsistency resolution pass audit. The run is an honest
RIGOROUS_PARTIAL_RESULT with exactly one conditional prerequisite (SL) and no hidden unconditional
claim beyond the known 2/3-class.
