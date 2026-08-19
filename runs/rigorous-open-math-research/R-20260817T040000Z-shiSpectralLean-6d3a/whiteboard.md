# Whiteboard — R-20260817T040000Z-shiSpectralLean-6d3a (hTrace Lean formalization)

- **Run ID:** `R-20260817T040000Z-shiSpectralLean-6d3a`
- **Task packet ID:** Q-20260814-criticalline-p1-507bb5 (Shi candidate Lean gap)
- **Last updated:** `2026-08-17T04:00:00Z`

## Current plan

1. Formalize the spectral case split `R ≤ D ∨ phi219(E) ≤ D` for PSD unit-diagonal Gram
   matrices (Lemma 1 in Shi's manuscript).
2. Build and check axioms in our Lean project.
3. If full spectral theorem is too heavy, produce a reduced version + exact gap report.

## Route history

- Lean subagent `[PARTIAL]`: eigenvalue-list scaffold produced; q≥2 and q=1 cases remain
  with `sorry`. Subagent interrupted to stop repeated mathlib fetch/build.
- Scaffold moved to `reproducibility/TwoCertificateSpectral.scaffold.lean`.

## Ideas to return to

- Use mathlib's spectral theorem for Hermitian matrices if available.
- Prove q≥2 and q=1 cases in the eigenvalue-list formulation first, then bridge to matrices.

## Open obligations

- Prove `traceD_gt_two_of_two_large` (q≥2 case).
- Prove q=1 case `D ≥ Φ_m(E)`.
- Assemble `R ≤ D ∨ phi219 E ≤ D`.

## Key artifacts

- `problem_contract.md`
- `formalization_progress.md`
- `reproducibility/TwoCertificateSpectral.scaffold.lean`
