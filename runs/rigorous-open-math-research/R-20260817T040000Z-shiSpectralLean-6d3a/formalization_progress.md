# Formalization progress — hTrace spectral split (SCAFFOLD)

- Attempted module: `Record9.TwoCertificateSpectral` (eigenvalue-list formulation).
- Completed lemmas (no sorry in these):
  - `traceEnergyIdentity` : `D = E + 2X − q − Q`
  - `phi_le_self` : `Φ_m(E) ≤ E`
  - `R_lt_two`
- Unfinished / blocked:
  - `traceD_gt_two_of_two_large` : q ≥ 2 ⇒ D > 2 (placeholder `sorry`)
  - the q = 1 case `D ≥ Φ_m(E)`
  - the final `R ≤ D ∨ phi219 E ≤ D` alternative
- The full matrix spectral bridge (PSD symmetric matrix → eigenvalue list) is not formalized.
- Status: **SCAFFOLD** (partial, not verified). The scaffold is stored in
  `reproducibility/TwoCertificateSpectral.scaffold.lean`; it was moved out of
  `lean-proof/Record9/Record9/` to avoid presenting a `sorry` as verified.
- Next steps:
  1. Prove q≥2 and q=1 cases in the eigenvalue-list formulation.
  2. Then either accept an eigenvalue-list hypothesis as a bridge or formalize the spectral theorem.
