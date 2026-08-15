# Whiteboard — R-20260816T060000Z-stabridge-a3f1 (T1c-1 / T1c-2 stability bridge)

- **Run ID:** `R-20260816T060000Z-stabridge-a3f1`
- **Task packet ID:** Stage C T1c bridge statements (T1c-1 stability_eps, T1c-2
  stability_averaged_eps); same pattern as kernel-limit precedent.
- **Last updated:** `2026-08-16T06:45:00Z`

## Current plan

PIN + PROVE (analysis level) the two OPEN bridge steps:
- **T1c-1** (step 2): `S ≥ H_MT·N + Δ(M°) − o(N)` → ε-form `stability_eps`.
- **T1c-2** (steps 5–6): `Δ(M°) ≥ (A₀/m)S − ((m−1)/(500m))N − o(N)` → ε-form
  `stability_averaged_eps`, via sub-lemmas T1c-2a (block energy), T1c-2b (defect lemma+A₀<1),
  T1c-2c (pinch/average), T1c-2d (analytic uniformity, kernel-limit).

RUN COMPLETE (statement pass): exact ε-form statements pinned for the true Δ(M°); the
normalization is resolved to the unit-normalized (correlation) Gram; all finite/structural
steps proved + numerically spot-checked. Lean formalization + the two non-trivial analytic
sub-steps are follow-ups.

## Route history

- Normalization `[RESOLVED + AMBIGUITY REPORTED]`: Δ(M°) must be the unit-normalized
  correlation Gram (all zero atoms share ‖v_γ‖² = L·F_L(0)); the hat-unit Gram (`mult_two`)
  would make Δ(Â)≈S and break Cor 2.2. Exact ambiguity documented (candidate_proof §7).
- Lemma 2.1 re-verified `[SUCCEEDED, evidence]`: `min_n` identity + random-matrix inequality.
- Quality block-defect lemma `[SUCCEEDED, evidence]`: `trΨ(G) ≥ min(1,2Σ|G_ij|²)` (C4).
- Constants `[SUCCEEDED, exact]`: A₀/m = 2499/657500, (m−1)/(500m) = 262/131500, cLHS.
- Block energy + window counting `[SUCCEEDED]`: E_m+(1/500)span ≥ A₀ (T1c2a.check).
- Kernel-ratio correlation energy `[SUCCEEDED, evidence]`: 2Σ|G_ij|²/E_m → 1 (C7).
- Offset-averaging coeffs `[SUCCEEDED, exact]`: periodic model (T1c2c).
- **Lean formalization `[BLOCKED — budget]`**: statements + proofs are ready; Lean bridge
  is a follow-up lean-verify run.

## Ideas to return to

- Tight uniformity constant for the o(N) in T1c-2d (block×kernel-limit transfer).
- Lean proof of the pinching `trΨ(M°) ≥ block average` (T1c-2c) and of the additive `+Δ`
  (T1c-1) — the two genuinely new obligations.
- Confirming the hat-unit Δ(Â)≈S rigorously (not just numerically) to seal the ambiguity.

## Open obligations

- Lean formalization of T1c-1 (`stability_eps`), T1c-2 (`stability_averaged_eps`), and the
  four sub-lemmas.
- T1c-2c pinching sub-step + T1c-2d analytic uniformity (the two non-trivial analytic bits).
- T2 (certified F₈≥392/100000) remains OPEN (block-energy input).

## Key artifacts

- `problem_contract.md` — exact statements (T1c-1, T1c-2, sub-lemmas).
- `candidate_proof.md` — full structural proofs + honesty/ambiguity report (§7).
- `research_ledger.md` — chronological decisions.
- `counterexample_log.md` — normalization counter-cases (hat-unit Δ(Â)≈S).
- `reproducibility/{stabridge_checks,stabridge_sublemma}.py` — evidence checks.
- `SHA256SUMS` — hash-bound artifacts.
