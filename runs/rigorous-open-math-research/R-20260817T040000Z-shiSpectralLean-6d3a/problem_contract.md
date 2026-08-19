# Problem contract — Lean formalization of the spectral split (hTrace)

- **Source**: Yuhang Shi, two-certificate trace-energy deduction; the candidate's Lean
  `TwoCertificate.SupportingPlane` leaves `hTrace : R ≤ D ∨ phi E ≤ D` as an assumption.
- **Goal**: formalize the missing spectral case split from Lemma 1 of the manuscript:
  for a positive-semidefinite unit-diagonal real symmetric `m × m` matrix `G` with
  `E = Σ(λ_i−1)²`, `D = tr Ψ(G)`, `R = Φ_m(A_max)`, prove
  `R ≤ D ∨ Φ_m(E) ≤ D`.
- **Target module**: `lean-proof/Record9/Record9/TwoCertificateSpectral.lean` (mathlib only,
  or importing the candidate-style definitions if convenient).
- **Completion criteria**:
  - `lake build` exit 0, no `sorry`/`admit`/`axiom`;
  - `#print axioms` = `{propext, Classical.choice, Quot.sound}`;
  - statement is an honest formalization of the intended `hTrace`.
- **Fallback**: if the full spectral theorem route is too heavy, produce a rigorous
  reduced formalization (e.g., for a 2×2/3×3 case or via a stated finite-dimensional
  Hermitian spectral theorem) and report the exact remaining obstacle.
