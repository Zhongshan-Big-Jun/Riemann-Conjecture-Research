# Formalization progress — Zenodo 22008814 audit

- Module: `lean-proof/Record9/Record9/ZenodoAudit.lean` (`Record9.ZenodoAudit`), mathlib only.
- Verified lemmas:
  - `curvature_identity` (eq (4) of the preprint) — `lake build` exit 0; axioms gold standard.
  - `conjugate_pair_block_charpoly` — exit 0; axioms gold standard.
  - `conjugate_pair_block_has_negative_eigenvalue` — exit 0; axioms gold standard.
- Not formalized (recommended next targets): Prop 8.1 spectral floor, Lemma 14.1 inertia
  reduction, Lemma 12.3 corrected sign, Prop 11.1 rank bound, Lemma 3.3 Riesz bounds.
