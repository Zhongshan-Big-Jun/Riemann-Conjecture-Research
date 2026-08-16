# Final report — T1c-1 / T1c-2 stability-bridge formalization (Stage C)

**Status: MACHINE_ACCEPTED_PENDING_AUDIT**

`lake build Record9.StabilityBridge` exits 0 with the pinned environment (Lean v4.33.0-rc2,
mathlib 51e6992e); the module passes the `lake env lean` check; the comment-aware
sorry/admit/axiom scan is clean; `#print axioms` on every headline theorem is
`{propext, Classical.choice, Quot.sound}` (base-only). The M1 ψ-defect statement plus the
M2/M3 ε-form implications compile clean. Per the task's honest-bridge discipline and the
lean-verify skill's status taxonomy, an independent statement-fidelity/obligation audit has
NOT yet been performed, so the label is `MACHINE_ACCEPTED_PENDING_AUDIT`, not
`FORMALLY_VERIFIED`.

## 1. What is formalized

Module `lean-proof/Record9/Record9/StabilityBridge.lean` (`Record9.StabilityBridge`,
namespace `Zeta23.ThmD`), new module only — Chain9.lean / KernelLimit.lean untouched, no file
under `literature/raw/zeta-23-lean/` source modified.

- **M1 (T1c-2b ψ-defect):** `Psi`, `trPsi` (spectral), `sumSqOffDiag`, `psi_defect` (exact
  statement), plus machine-checked `Psi_nonneg`, `Psi_gt_one_of_gt_two`, `trPsi_nonneg`, and
  the two case combinators `psi_defect_of_unit` / `psi_defect_of_lower`.
- **M2 (T1c-1):** `deltaMT_true`, `stability_eps_true` (exact ε-form with +Δ), `base_eps`,
  `base_eps_from_thmD₀` (machine-proved from `thmD₀_simple_mult`), `defect_eps`, and the
  machine-checked additive +Δ survival `from_base_and_defect : base_eps → defect_eps →
  stability_eps_true`.
- **M3 (T1c-2):** `stability_averaged_eps_true` (exact ε-form), the exact constant identities
  (A₀ < 1, A₀/m = 2499/657500, (m−1)/(500m) = 262/131500, the (m−1)/(500m) closed form at
  m = 263), and `averaged_from_pinching` routing the T1c-2c/2d content through the explicit
  hypothesis `pinching_averaged_eps`.

## 2. Machine evidence table

| Command (workdir = lean-proof/Record9 unless noted) | Exit | Evidence |
|---|---|---|
| `lake build Record9.StabilityBridge` | **0** | "Built Record9.StabilityBridge (36s)"; "Build completed successfully (8839 jobs)"; only a `try 'simp' instead of 'simpa'` linter hint (harmless) |
| `lake env lean Record9/StabilityBridge.lean` | **0** | full type-check; only the same harmless linter hint |
| `#print axioms` (scratch probe, deleted) | **0** | `from_base_and_defect`, `base_eps_from_thmD₀`, `averaged_from_pinching`, `psi_defect_of_unit`, `psi_defect_of_lower`, `Psi_nonneg`, `trPsi_nonneg` → all `[propext, Classical.choice, Quot.sound]` |
| comment-aware sorry/admit/axiom scan | clean | no `sorry`/`admit`/`axiom` outside the header disclaimer |
| snapshot source pristine | yes | no source file under `literature/raw/zeta-23-lean/` modified (only `.lake/build` cache copied to let the single-file `lake env lean` resolve local `Record9.*` imports, per the established pass pattern) |

Toolchain: leanprover/lean4:v4.33.0-rc2, Lake 5.0.0, mathlib @ 51e6992e, packagesDir ->
`literature/raw/zeta-23-lean/.lake/packages`.

## 3. Exact remaining gaps (open analytic obligations)

1. **Lemma 2.1 Ψ-form application (M1 spectral sub-steps).**
   (a) all eigenvalues ≤ 2 ⇒ `tr Ψ(G) = frobSq(G−I)` and `frobSq(G−I) ≥ 2·Σ_{i<j}|G_ij|²`
   (off-diagonal Frobenius of G−I, mirroring the snapshot's `sum_sq_*` machinery);
   (b) some eigenvalue > 2 ⇒ `1 ≤ tr Ψ(G)`. These close `psi_defect_of_lower` /
   `psi_defect_of_unit`; here they are carried as premises.
2. **T1c-1 additive survival, full-O(S) Δ.** The lemma-2.1 assembly keeping an order-O(S)
   Δ additively in `thmD_mult2_abstract`/`N0star_lower_c` without bounding Δ small. This
   module machine-checks only the additive sub-case `0 ≤ Δ ∧ Δ ≤ o(N)` (`defect_eps`); the
   paper-level OpenAI Cor 2.2 content is the recorded open obligation.
3. **T1c-2c pinching** `trΨ(M°) ≥ block-average` and **T1c-2d uniformity**
   `Σ|G_ij|² = (1/2)E_m + o(1)` (kernel-limit reuse). Routed through the explicit hypothesis
   `pinching_averaged_eps` / `averaged_from_pinching`.
4. **T1c-2a block energy** `E_m+(1/500)span ≥ A₀` (with the T2 `CERTIFIED_F8_GE` input) is
   deferred, not in this module.

## 4. Honest-bridge discipline

Every analytic sub-step above is an explicit axiom-free hypothesis (matching the T1/Chain9
`record9Bridge` pattern); no `sorry`/`admit`/`axiom` is introduced, and `#print axioms` on
the checked theorems is base-only. The final integration of the true-Δ bridge
(`stability_eps_true`, `stability_averaged_eps_true`) into `chain9_eps` is a later pass, as
the task specifies.
