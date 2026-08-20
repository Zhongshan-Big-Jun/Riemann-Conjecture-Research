# Interruption handoff — hTrace spectral-split Lean formalization

- **Run ID**: R-20260817T040000Z-shiSpectralLean-6d3a
- **Task packet ID**: Q-20260814-criticalline-p1-507bb5 (Shi candidate Lean gap)
- **Date**: 2026-08-17T04:30:00Z
- **Interrupt reason**: user requested full handoff; also to stop repeated mathlib fetch/build
  that was saturating network/CPU.
- **Task state**: IN_PROGRESS

## Completed work progress

- Attempted `Record9.TwoCertificateSpectral` in eigenvalue-list formulation.
- Machine-proved (in scaffold):
  - `traceEnergyIdentity` (D = E + 2X − q − Q)
  - `phi_le_self` (Φ_m(E) ≤ E)
  - `R_lt_two`
- The partial scaffold is preserved at
  `reproducibility/TwoCertificateSpectral.scaffold.lean` (marked `SCAFFOLD`).
- Independent reproduction of the Shi 0.673316977… candidate itself is complete
  (`verify_release.py` PASSED, exact/joint/multi-cert scans reproduce m=219 optimum).

## Completed obligations

- None of the target `hTrace` alternative is fully proved in Lean.
- The scalar identities above are the beginning of the proof.

## Open obligations

- `traceD_gt_two_of_two_large` (q ≥ 2 case) — currently `sorry`.
- q = 1 case `D ≥ Φ_m(E)`.
- Assemble `R ≤ D ∨ phi219 E ≤ D`.
- Optionally bridge from the matrix spectral theorem to the eigenvalue-list formulation.

## Tools and methods tried

- [SUCCEEDED] eigenvalue-list definitions and simple identities in Lean (traceEnergyIdentity,
  phi_le_self, R_lt_two).
- [PARTIAL] q≥2 / q=1 case proofs — not completed.
- [BLOCKED] full spectral theorem route — not attempted due to resource/time; mathlib fetch
  caused network/CPU saturation and was stopped.

## Attempted routes

- [PARTIAL] Eigenvalue-list formulation of the spectral split.
- [NOT STARTED] Full mathlib spectral theorem for Hermitian matrices.
- [NOT STARTED] Small-dimension direct proof (m=3/4).

## Next actions

1. Complete q≥2 and q=1 inequalities in the eigenvalue-list scaffold.
2. Then either accept an eigenvalue-list hypothesis as the bridge to the matrix statement or
   formalize the matrix spectral theorem.
3. Re-run `lake build` only with the existing local mathlib cache (do not repeatedly fetch
   mathlib).

## Key artifacts

- `reproducibility/TwoCertificateSpectral.scaffold.lean`
- `formalization_progress.md`
- `problem_contract.md`
- `whiteboard.md`
