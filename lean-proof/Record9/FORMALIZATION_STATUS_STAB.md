# Formalization status — T1c-1 / T1c-2 stability bridges (Stage C)

Run: `runs/rigorous-open-math-research/R-20260816T060000Z-stabridge-a3f1` (source artifacts).
Module: `lean-proof/Record9/Record9/StabilityBridge.lean`, module `Record9.StabilityBridge`,
namespace `Zeta23.ThmD`. Pinned mathlib `51e6992e`, Lean `v4.33.0-rc2`.

Status line: **MACHINE_ACCEPTED_PENDING_AUDIT** — `lake build Record9.StabilityBridge` exits 0,
no `sorry`/`admit`/`axiom` outside comments, `#print axioms` on the headline theorems is
`{propext, Classical.choice, Quot.sound}` (base-only). The machine-checked content is the
Ψ scalar facts, the two-case ψ-defect combinators, the M2 additive `+Δ` survival algebra, and
the M3 constant-identity algebra; the genuinely analytic sub-steps are carried as explicit
hypotheses (honest bridge), exactly as the task permits and the obligation table records.

---

## 1. What is machine-formalized

### M1 — the Ψ-defect lemma (T1c-2b core)
- `Psi (t : ℝ)` — `if t ≤ 2 then (t−1)² else 2t−3` (exact, candidate_proof §0).
- `trPsi G hG` — tr Ψ(G) = Σᵢ Ψ(μᵢ) for Hermitian G (spectral definition via `hG.eigenvalues`).
- `sumSqOffDiag G` — Σ_{i<j} |G_ij|².
- `psi_defect G hG : Prop` — the exact T1c-2b statement `min 1 (2·Σ_{i<j}|G_ij|²) ≤ trΨ(G)`.
- Machine-checked lemmas:
  - `Psi_eq_sq_of_le_two`, `Psi_eq_linear_of_gt_two` (case logic),
  - `Psi_nonneg` (Ψ ≥ 0), `Psi_gt_one_of_gt_two` (the `>1` branch),
  - `trPsi_nonneg` / `deltaMT_nonneg_via_trPsi` (Δ ≥ 0),
  - `psi_defect_of_unit` (if `1 ≤ trΨ(G)` then ψ_defect — the `1`-cap branch),
  - `psi_defect_of_lower` (if `2·Σ_{i<j}|G_ij|² ≤ trΨ(G)` then ψ_defect — the `2Σ` branch).

### M2 — T1c-1 (`stability_eps` for the true Δ)
- `deltaMT_true : ℝ → ℝ` — the true Δ(M°)(T) = tr Ψ(M°(T)) of the unit-normalized
  correlation Gram, carried abstractly (Gram-entry machinery not machine-tied — honest bridge).
- `stability_eps_true : Prop` — the exact ε-form
  `∀ ε>0, ∃ T₀, ∀ T≥T₀, HD 1 · N + Δ(M°)(T) − ε·N ≤ N₀ˢ(T,2T)`.
- `base_eps : Prop` — `S ≥ H_MT·N − o(N)` (the `thmD₀_simple_mult` form).
- `base_eps_from_thmD₀ : base_eps` — machine-proved by `thmD₀_simple_mult`.
- `defect_eps : Prop` — `Δ ≥ 0 ∧ Δ ≤ o(N)` (the honest bounded sub-case).
- `from_base_and_defect : base_eps → defect_eps → stability_eps_true` — the **additive +Δ
  survival**: from the base inequality and the Δ-defect bound, the ε-form with +Δ is derived
  (machine-checked algebra with ε/2, ε/4 split and common T₀ = max T₀₁ T₀₂).

### M3 — T1c-2 (`stability_averaged_eps`)
- `stability_averaged_eps_true : Prop` — the exact ε-form
  `∀ ε>0, ∃ T₀, ∀ T≥T₀, Δ(M°)(T) ≥ (2499/657500)·S − (262/131500)·N − ε·N`.
- Exact constant identities (mirroring Chain9 T1d, all `norm_num`-proved):
  `A0_st_lt_one`, `cA0m_st_eq` (A₀/m = 2499/657500), `qMT_st_eq` ((m−1)/(500m) = 262/131500),
  `qMT_m_identity` (closed form at m = 263), `qMT_closed`.
- `pinching_averaged_eps` (explicit hypothesis routing the T1c-2c/2d steps) and the
  definitional `averaged_from_pinching : pinching_averaged_eps → stability_averaged_eps_true`.

## 2. Machine evidence table

| Command (workdir = lean-proof/Record9 unless noted) | Exit | Evidence |
|---|---|---|
| `lake build Record9.StabilityBridge` | **0** | "Built Record9.StabilityBridge (36s)"; "Build completed successfully (8839 jobs)"; only a `try 'simp' instead of 'simpa'` linter hint (harmless) |
| `lake env lean Record9/StabilityBridge.lean` | **0** | full type-check; only the same harmless linter hint |
| `lake env lean Record9/Probe_axioms_stab.lean` (scratch, deleted) | **0** | `#print axioms` of all headline theorems = `[propext, Classical.choice, Quot.sound]` (base-only) |
| sorry/admit/axiom scan of `Record9/StabilityBridge.lean` | clean | comment-aware scan: no `sorry`/`admit`/`axiom` outside the header disclaimer |
| Snapshot source pristine | yes | no file under `literature/raw/zeta-23-lean/` source modified (only `.lake/build` cache copied for the `lake env lean` import path, per the established pass pattern) |

Toolchain: leanprover/lean4:v4.33.0-rc2, Lake 5.0.0, mathlib @ 51e6992e.

## 3. Obligation table and exact open gaps

| Obligation | Machine status | Exact gap |
|---|---|---|
| **M1 ψ-defect lemma `psi_defect`** | statement frozen + two-case combinators machine-checked | **Open:** the two spectral sub-steps that close the branch premises — (S1) all eigenvalues ≤ 2 ⇒ `tr Ψ(G) = frobSq(G−I)` and `frobSq(G−I) ≥ 2·Σ_{i<j}\|G_ij\|²` (off-diagonal Frobenius of G−I via `sum_sq_*` mirror); (S2) some eigenvalue > 2 ⇒ `1 ≤ tr Ψ(G)`. These are the recorded "Lemma 2.1 Ψ-form application" analytic obligation. |
| **M2 T1c-1 ± ε-form** | `stability_eps_true`, `base_eps`, `from_base_and_defect` machine-checked | **Open (analytic):** the Lemma 2.1 assembly keeping a full order-O(S) Δ additively in `thmD_mult2_abstract`/`N0star_lower_c` without bounding Δ small; this module machine-checks only the additive sub-case where `0 ≤ Δ ∧ Δ ≤ o(N)` (`defect_eps`). The full-O(S) Δ survival is the OpenAI Cor 2.2 audited step. |
| **M3 T1c-2 ε-form** | `stability_averaged_eps_true` + constant algebra machine-checked | **Open (analytic):** T1c-2c pinching `trΨ(M°) ≥ block-average` and T1c-2d uniformity `Σ\|G_ij\|² = (1/2)E_m + o(1)` (kernel-limit reuse). Routed via `pinching_averaged_eps` / `averaged_from_pinching` as explicit hypotheses. |
| **T1c-2a block energy** `E_m+(1/500)span ≥ A₀` (T2 `CERTIFIED_F8_GE` input) | not in this module | finite window-sum algebra + the certified `F₈ ≥ 392/100000`; deferred (T2-scope input, Chain9's `CERTIFIED_F8_GE`). |

## 4. Fidelity notes
- Statements are frozen vs `problem_contract.md` §3 and `candidate_proof.md`; the ε-form
  quantifier order (∀ε>0, ∃T₀:ℝ, ∀T≥T₀, window (T,2T]) and the literal constants
  2499/657500 = A₀/m and 262/131500 = (m−1)/(500m) match `Chain9.stability_eps` /
  `stability_averaged_eps` with `deltaMT` replaced by `deltaMT_true`.
- The unit-normalized (≡ correlation) Gram convention is the one consistent with Cor 2.2 and
  T1c-2 (stabridge `counterexample_log.md` §1); `deltaMT_true` is that Δ, carried abstractly.
- Honest-bridge discipline: the analytic sub-steps are explicit axiom-free hypotheses, never
  assumed as axioms; no `sorry`/`admit`/`axiom` are introduced.
