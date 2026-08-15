# Status & literature — T1c-1 / T1c-2 stability-bridge (Stage C)

Run: `R-20260816T060000Z-stabridge-a3f1`. Status line: `RIGOROUS_PARTIAL_RESULT`.

## Current status
- The exact ε-form bridge statements T1c-1 (`stability_eps`) and T1c-2
  (`stability_averaged_eps`) are pinned for the true Δ(M°) (unit-normalized Gram's `tr Ψ`).
- All finite/structural steps proved at analysis level; numeric spot-checks pass.
- Two non-trivial analytic sub-steps are stated precisely but are the follow-up formalization
  obligations: (i) the additive survival of `+Δ(M°)` in the Thm-D assembly (T1c-1),
  (ii) the pinching `tr Ψ(M°) ≥ block average` + the block×kernel-limit `o(1)` uniformity
  (T1c-2c/T1c-2d).

## Exact known theorems used / cited
- Theorem D (Lean-verified): `S ≥ H_MT·N − o(N)`, `H_MT = 3/2 − (1/√2)cot(1/√2)`;
  `ThmD/Mult.lean thmD₀_simple_mult`, `ThmD/Functional.lean HD_one`.
- Kernel-limit lemma (machine-proved, kernellimit run): `⟨v_a,v_b⟩/‖v‖² = kMT(x)+O(w/L)`
  uniform, λ=1, `kMT = K_1/K_1(0)` equals Chain9's kernel/certificate kernel.
- OpenAI `proof.md` §2 Lemma 2.1 (Ψ rank-inertia) and Cor 2.2 (S ≥ H·N + Δ(M°)); general-k
  run §2–§6 (block energy, defect, pinching/averaging). Both are paper-level audited inputs
  that are NOT yet in Lean; this pass makes their statements exact and fits them to the
  snapshot.

## Novelty / ambiguity risks
- The normalization of Δ(M°) is the main novelty/fidelity risk; reported (see
  counterexample_log §1, candidate_proof §7). No silent convention adopted.
- The `A₀<1` → `2Σ|G_ij|²`-branch, the block-energy window summation, and the
  offset-averaging defect numbers are the finite-algebra core (Lean-friendly).

## Provenance
Inputs and hashes: `repro_manifest.md`. Ledger: `research_ledger.md`.
