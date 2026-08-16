# Obligation map — T1c-1 / T1c-2 stability bridges (Stage C)

Module: `lean-proof/Record9/Record9/StabilityBridge.lean` (`Record9.StabilityBridge`,
namespace `Zeta23.ThmD`). Source: `runs/rigorous-open-math-research/R-20260816T060000Z-stabridge-a3f1/`.

| Obligation | Lean declaration | Machine status | Notes |
|---|---|---|---|
| **T1c-1** `stability_eps` for true Δ: `∀ε>0, ∃T₀, ∀T≥T₀, HD 1·N + Δ(M°)(T) − ε·N ≤ N₀ˢ(T,2T)` | `stability_eps_true`; derived by `from_base_and_defect : base_eps → defect_eps → stability_eps_true` with `base_eps_from_thmD₀` | **MACHINE-CHECKED** (ε-form existence via additive +Δ survival) | `base_eps` ≡ `thmD₀_simple_mult` (machine-proved); `defect_eps` = `0 ≤ Δ ∧ Δ ≤ o(N)` — the additive sub-case. **Open:** Lemma 2.1 assembly keeping a full order-O(S) Δ without bounding it small (the recorded analytic content). |
| **T1c-2** `stability_averaged_eps` for true Δ: `∀ε>0, ∃T₀, ∀T≥T₀, Δ(M°)(T) ≥ (2499/657500)·S − (262/131500)·N − ε·N` | `stability_averaged_eps_true`; constants `A0_st_lt_one`, `cA0m_st_eq`, `qMT_st_eq`, `qMT_m_identity`; routed via `pinching_averaged_eps` / `averaged_from_pinching` | **MACHINE-CHECKED** (statement + constant algebra; ε-form as explicit hypothesis) | **Open (analytic):** T1c-2c pinching, T1c-2d uniformity. The exact rationals 2499/657500 and 262/131500 are machine-proved identities. |
| **T1c-2b** ψ-defect `trΨ(G) ≥ min(1, 2Σ_{i<j}\|G_ij\|²)` | `psi_defect` (statement) + `psi_defect_of_unit` / `psi_defect_of_lower` (two-case combinators), `Psi_nonneg`, `Psi_gt_one_of_gt_two`, `trPsi_nonneg` | **MACHINE-CHECKED** (case-reduction combinators + scalar Ψ facts) | **Open:** spectral sub-steps (all-eig ≤ 2 ⇒ `trΨ = frobSq(G−I) ≥ 2Σ\|G_ij\|²`; some eig > 2 ⇒ `1 ≤ trΨ`) — the Lemma 2.1 Ψ-form application. |
| **T1c-2a** block energy `E_m+(1/500)span ≥ A₀` | — (deferred) | not in this module | finite window-sum algebra + `CERTIFIED_F8_GE` (T2 input, Chain9). |

Legend: machine status refers to `lake build Record9.StabilityBridge` exit 0 +
sorry/admit/axiom-clean + `#print axioms` base-only for the checked declarations.
Unaudited analytic sub-steps are explicit axiom-free hypotheses (honest bridge), never axioms.
