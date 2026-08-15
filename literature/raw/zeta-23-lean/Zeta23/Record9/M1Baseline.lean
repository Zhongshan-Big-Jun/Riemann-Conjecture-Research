/-
Record9.M1Baseline — M1 (extension project compiles & imports work)

Part of the Stage C T1 formalizer pass for the C₉ = 0.67306647267… world-record theorem
(C₉(ζ) = (657,500·H_MT − 1,310)/655,001, H_MT = 3/2 − (1/√2)·cot(1/√2)).

This file is the M1 smoke test of the PATH-DEPENDENCY project at lean-proof/Record9/: it
imports the Zeta23 snapshot baseline (including `Zeta23.ThmD.Mult`, which contains the
ε-form baseline theorem `thmD₀_simple_mult`), and establishes that the extension compiles
and links against the baseline. Its only proofs are trivial anchors.

Contract reference: lean-proof/verification-contract.md (O2/T1 row), task "T1 — the chain
theorem in ε-form". No analytic content here; it only proves the plumbing works.

Route decision: PATH-DEPENDENCY PROJECT (lean-proof/Record9/lakefile.toml), requiring the
Zeta23 snapshot by relative path AND mathlib by path to the snapshot's
.lake/packages/mathlib, with packagesDir pointing at the snapshot's .lake/packages so no
network fetch is needed. The snapshot's lakefile.toml is left UNTOUCHED (see the earlier
failed in-snapshot attempt and how an external auto-sync reverted tracked-file edits to the
snapshot — recorded in lean-proof/Record9/lakefile-change.md).
-/
import Zeta23.ThmD.Mult

noncomputable section

namespace Zeta23
namespace Record9

/-- M1 anchor: the baseline ε-form theorem is present and importable in Record9. -/
theorem m1_baseline_imports : True := by
  trivial

/-- M1 anchor (nominal): the baseline HD-rate simple-on-line theorem is reachable. -/
theorem m1_baseline_reachable :
    (∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
      (ThmD.HD 1 - ε) * (Ncount T (2 * T) : ℝ) ≤ N0simple T (2 * T)) := by
  exact ThmD.thmD₀_simple_mult

end Record9
end Zeta23
