# Research ledger — R-20260814T041219Z-condp1-698ec7

Chronological log of derivations, computations, and decisions.

## Step 1 — Contract & source ingest
- Loaded `rigorous-open-math-research` skill; read existing `problem_contract.md`, `repro_manifest.md`,
  task packet Q-20260814-criticalline-p1-507bb5, and the stub `verify_moments_christoffel.py`.
- Read v2 §7.2(b)–(f) (lines 1602–1658), Lemma 3.2/3.3 (513–556), Prop 4.1/4.4/4.5 (579–804),
  units (4.4) (590–600), Theorem 5.8 (1180–1230), Theorem D (1395–1427), §7.5 (1591–1627).

## Step 2 — Baseline (O1) constants cross-check
- Reconciled paper vs Lean: c₁* = 0.75329 = √2 tan(1/√2)/(1+tan(1/√2)/√2); H_MT = 3/2 − cot(1/√2)/√2;
  distinct (3−1/c₁*)/2 = 0.83625; CS-simple 2c₁*−1 = 0.50659. Noted Lean `thmD₀_simple` uses the
  weaker CS form (2c₁*−1) while the paper's §7.1 headline simple-on-line 0.67250 is the rank–trace
  form in `Mult.lean`. Baseline chain confirmed ✓.
- Decision: the moment/Christoffel route must use Prop 4.5 (n₊ count) not Prop 4.4(ii), so the
  13/18 structure is `2(1−Λ_m(0))−1`.

## Step 3 — Moment-consistency discovery (the key insight)
- Derived (exact): m_2(1) = 4/3 for the sine-kernel Gram (Lemma C), ≠ paper's 3/4.
- Computed (exact, script v1 `verify_moments_christoffel.py`): naive Christoffel for paper list
  gives Λ_2(0) = 143/100, NOT 5/36; 1−Λ_2(0)<0 → the list is internally inconsistent
  (m_2 − m_1² = −1/4 < 0; 2×2 Hankel det −1/4 < 0).
- Predicted the corrected list restores the paper's numbers.

## Step 4 — Verification (multiple independent exact computations)
- `moments_christoffel_full.py` (+ rewrite of D): corrected list (1,4/3,2,13/4) ⇒ Λ_2(0)=5/36 exact,
  1−Λ_2(0)=31/36, 13/18 exact. m=1 bound n₊/d ≥ m_1²/m_2 = 3/4 → liminf N0^s/N ≥ 1/2 (matches Lean CS).
- `check_lambda2_corrected.py`: independent 3×3 cofactor computation confirms Λ_2(0)=5/36 and
  13/18 = 2(1−5/36)−1 with exact rationals.
- CUE Monte-Carlo (evidence only): m_1≈1, m_2≈1.3355, m_3≈2.006, m_4≈3.264 corroborate the
  corrected list.

## Step 5 — Proof construction
- Wrote the SOS-witness Lemma 3.A (new, generalizes Lemma 3.3), Christoffel Lemma 3.B, Cor 3.C
  (Prop 4.5 route), and the convergence theorem §5 conditional on SL.
- Identified **SL** (0 in the support of the sine-kernel Gram spectral measure) as the single
  missing-in-literature ingredient; made the 100% theorem explicitly conditional on it.

## Step 6 — Reconciliation
- O5-D6: GLSS25/GS Thm 5 (PCC full support ⇒ 100%) is a complementary route (no contradiction);
  k=1 barrier (§7.2(e)) upheld: RS96 range kλ<2, odd moments don't lower Λ_1(0), λ≤1/2 vacuous.

## Step 7 — Artifacts
- Wrote problem_contract (final), status_and_literature, obligation_graph, approach_registry,
  candidate_proof, research_ledger, counterexample_log, audit_report, SHA256SUMS; hashed inputs/outputs.
