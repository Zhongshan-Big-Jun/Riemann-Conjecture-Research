# Whiteboard — R-20260816T070000Z-g2rule-a1b2

- **Run ID:** `R-20260816T070000Z-g2rule-a1b2`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5`
- **Project:** `F:\LaTeX\Riemann Conjecture`
- **Last updated:** `2026-08-16T15:00:00Z`

## Run ID / Task packet ID
- Run ID: `R-20260816T070000Z-g2rule-a1b2`
- Task packet ID: `Q-20260814-criticalline-p1-507bb5` (SL gap G2: general vanishing rule for J_σ)

## Current plan
Determine the GENERAL vanishing rule for the shape integrals `J_σ` (which partitions σ of
{0,…,k−1} give J_σ=0) from the exact k=5 and k=6 per-partition data, verify against k=3,4,5,6,
and state the refined Lemma P/G2. **STATUS: the vanishing rule is FOUND and 100%-verified on the
exact 275-partition dataset (k=3..6). General-k proof is the open residual identity.** Final
status label: `RIGOROUS_PARTIAL_RESULT` / `FINITE_COMPUTATIONAL_RESULT`.

## Route history
- Assemble exact per-partition dataset `[SUCCEEDED]`: k=6 from m6 CSVs + analytic b=1,2; k=3,4,5
  from the audited exact engine with the 4 documented float-noise k=5 values corrected via the
  isoclass-determinism rule + certified D_5=0. Moments m_2..m_6 reproduced EXACTLY.
- Isoclass-determinism `[SUCCEEDED]`: 38 (b,H-isoclass) classes at k=6, one J per class — J depends
  only on the cycle-crossing multigraph H_σ up to relabeling (`rule_tests.py`).
- Candidate-rule falsification `[SUCCEEDED]`: block-count, isolated-vertex, forest-support,
  m-parity, pure (b,m) threshold all falsified (`counterexample_log.md`).
- **Vanishing rule found `[SUCCEEDED]`**: J_σ≠0 ⟺ H_σ connected AND m ≥ 2b−2; 275/275 exact.
- b=2 closed form `[SUCCEEDED]` (J=c_m−c_{m+2}); b≥3 value formulas `[OPEN]`.

## Ideas to return to
- Prove M1 (disconnected ⇒ J=0 via factorization + lower-order D-type cancellation) and M2
  (connected, m ≤ 2b−3 ⇒ signed box-spline sum telescopes to 0; m ≥ 2b−2 ⇒ a non-cancellable term
  survives). This closes Lemma P for all k.
- Closed c-combination (or Ursell-type) formulas for b≥3 nonzero J values (b=2 is closed).
- Exact m_7,m_8 → Λ_4(0) → SL decay; G3 (Lemma H) matching-sum ⇒ determinacy.

## Open obligations
- General-k proof of the vanishing rule (candidate_proof §7): the exact residual identity.
- b≥3 value (c-combination) formulas.
- SL and Λ_m decay remain open beyond the exact Λ_1,Λ_2,Λ_3.

## Key artifacts
- `reproducibility/allJ.json` — exact per-partition J_σ (k=3..6, 275 rows), the reproducibility datum.
- `reproducibility/final_rule.py` — THE vanishing-rule checker (275/275).
- `reproducibility/build_dataset.py` — dataset assembly + moment anchors.
- `reproducibility/rule_tests.py`, `abstract_k6.py`, `survey_k6.py`, `b2b3_formulas.py` — diagnostics.
- `candidate_proof.md`, `research_ledger.md`, `counterexample_log.md`, `repro_manifest.md`, `SHA256SUMS`.

## Remaining gaps / honesty
- The rule is **verified** (exact computation, 275/275) but **not proven for all k**; the precise
  identity to prove is stated. No numerical evidence is presented as proof.
- b≥3 value formulas (which nonzero fraction each admissible σ gets) are table-driven, not closed-form.
