# Whiteboard — R-20260816T080000Z-g2proof-a24d

- **Run ID:** `R-20260816T080000Z-g2proof-a24d`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5`
- **Project:** `F:\LaTeX\Riemann Conjecture`
- **Last updated:** `2026-08-16T09:30:00Z`

## Run ID / Task packet ID
- Run ID: `R-20260816T080000Z-g2proof-a24d`
- Task packet ID: `Q-20260814-criticalline-p1-507bb5` (SL gap G2: general-k proof of the residual identity M1/M2)

## Current plan
Prove the G2 residual identity: `Σ_{π∈S_b} sign(π)·B_{Γ_{σ,π}}(0) = 0 ⟺ H_σ disconnected OR m ≤ 2b−3`.
M1 is closed (H_σ is always connected for b≥2, so the disconnected branch is vacuous). The remaining
content is M2: the low-surplus signed box-spline sum telescopes to 0; surplus survives ⇒ nonzero.
Final status label will be updated by the solver on completion (expected `RIGOROUS_PARTIAL_RESULT` or
`REPAIRABLE_GAP`).

## Route history
- Setup and upstream data loading `[SUCCEEDED]`.
- M1 connectivity lemma `[SUCCEEDED]`: H_σ always connected for b≥2; disconnected branch vacuous.
- Per-π box-spline decomposition `[SUCCEEDED]`: exact certified B values for b=3,4 low cases.
- Route 1 (cycle-class-function / multiplicative EGF) `[FAILED]`: B is not a multiplicative class function.
- Naive degree-2 contraction `[FAILED]`: not closed under the determinant ρ_b.
- b=2 family `[SUCCEEDED]`: J = c_m − c_{m+2} > 0 always.
- k=7 new-isoclass verification `[IN PROGRESS]`: extends the 275-row dataset to new H-isoclasses.

## Ideas to return to
- Grassmann/Wick (fermionic Gaussian) interpretation of the signed box-spline sum.
- Laplacian-determinant / cofactor formulation of the surplus condition m ≥ 2b−2.
- Induction on b or k with the determinant contraction tracked.

## Open obligations
- M2 general-k proof: `Σ sign(π) B_{H∪π}(0) = 0 ⟺ m ≤ 2b−3`.
- Full run artifacts (candidate_proof.md, repro_manifest.md, SHA256SUMS, counterexample_log.md) being finalized.
- G3 (Lemma H) + SL itself remain open.

## Key artifacts
- `problem_contract.md`, `research_ledger.md` (live).
- `reproducibility/` — exact box-spline engines and per-J datasets.
- Final `candidate_proof.md`, `repro_manifest.md`, `SHA256SUMS` expected on completion.

## Remaining gaps / honesty
- The general-k proof is not yet closed; finite checks through k=7 strengthen but do not prove M2.
- No numerical evidence is claimed as proof; the target is a rigorous combinatorial/analytic identity.
