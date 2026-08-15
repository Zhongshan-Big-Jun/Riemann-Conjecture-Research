# Problem contract — T1c-1 / T1c-2 stability-bridge statements (Stage C)

Run: `runs/rigorous-open-math-research/R-20260816T060000Z-stabridge-a3f1`
Status line: `RIGOROUS_PARTIAL_RESULT` — exact Lean-ready ε-form statements pinned for the
true Δ(M°); T1c-2 sub-lemma decomposition complete; analysis-level proofs + numerical
spot-checks. Lean formalization and the two non-trivial analytic sub-steps (T1c-1 additive
`+Δ`, T1c-2c pinching/+T1c-2d uniformity) are follow-ups (same class as the kernel-limit
precedent).

## 1. Origin and role

The C₉ record chain `lean-proof/Record9/Record9/Chain9.lean` (machine-accepted) states the
bridge hypotheses `stability_eps` (paper step 2) and `stability_averaged_eps` (steps 5–6)
over a placeholder `deltaMT := fun _ => 0`. The two remaining OPEN analytic steps are:

- **T1c-1 (step 2)** — the stability refinement `S ≥ H_MT·N + Δ(M°) − o(N)`.
- **T1c-2 (steps 5–6)** — the averaged block-defect `Δ(M°) ≥ (A₀/m)S − ((m−1)/(500m))N − o(N)`.

This pass = the same pattern as the kernel-limit precedent: **pin the exact ε-form
statements first, then give analysis-level proofs.** Lean formalization is a follow-up.

## 2. Objects (pinned from the snapshot)

- `L = log(T/2π)` (λ=1), MT window φ, zero atoms `v_γ(u)=φ(u)e^{iγu}` (kernel-limit run).
- The retained central simple zeros `γ_1<…<γ_S` (`Defs.lean S1`), `S = N₀ˢ(T,2T)`.
- **Unit-normalized correlation Gram** (all atoms have identical norm
  `‖v_γ‖² = L·F_L(0)`):
  `M°_ab(T) := ⟨v_a,v_b⟩/‖v_a‖‖v_b‖`, diagonal `= 1`, columns `‖·‖ = 1 ≤ 1`.
- `Δ(M°)(T) := tr Ψ(M°(T))`, `Ψ(t) = (t−1)²·1_{t≤2} + (2t−3)·1_{t≥2}` (proof.md §2).

## 3. Exact statements (ε-form; == Chain9 bridge hypotheses for the true Δ)

**T1c-1 (`stability_eps`).**
```
∀ ε>0, ∃ T₀:ℝ, ∀ T≥T₀:
   HD 1 · N(T,2T) + Δ(M°)(T) − ε·N(T,2T) ≤ N₀ˢ(T,2T).
```

**T1c-2 (`stability_averaged_eps`).** with `A₀ = 2499/2500`, `m = 263`,
`A₀/m = 2499/657500`, `(m−1)/(500m) = 262/131500` (exact):
```
∀ ε>0, ∃ T₀:ℝ, ∀ T≥T₀:
   Δ(M°)(T) ≥ (2499/657500)·N₀ˢ(T,2T) − (262/131500)·N(T,2T) − ε·N(T,2T).
```

**Sub-lemmas.**
- **T1c-2a (block energy):** `E_m + (1/500)(y_m−y_1) ≥ f₉(m−8)`, `f₉=392/100000`, `m=263`,
  from `CERTIFIED_F8_GE`.
- **T1c-2b (block defect):** `tr Ψ(G) ≥ min(1, 2Σ_{i<j}|G_ij|²)`; `A₀<1` ⇒ `2Σ`-branch.
- **T1c-2c (pinch/average):** `Δ(M°) ≥ (A₀/m)S − ((m−1)/(500m))·N − o(N)`.
- **T1c-2d (uniformity):** `Σ_{i<j}|(M°)_ij|² = (1/2)E_m + o(1)` uniform, via kernel-limit.

## 4. Completion criteria (this bounded pass)

- [x] Exact Lean-ready statements pinned (T1c-1, T1c-2) for the true Δ(M°) (this file §3).
- [x] Normalization of Δ(M°) resolved / ambiguity precisely reported (§7 of candidate_proof).
- [x] T1c-2 sub-lemma decomposition with exact statements (candidate_proof §3).
- [x] Analysis-level proofs of the finite/structural steps (Lemma 2.1, defect lemma, block
      energy, offset averaging) + kernel-limit reuse.
- [x] Numerical spot-checks (reproducibility/*.py; evidence, not proof).
- [ ] Lean formalization of T1c-1, T1c-2, sub-lemmas + the two non-trivial analytic
      sub-steps (additive `+Δ`, pinching/uniformity): follow-up run.

## 5. Forbidden moves / discipline
- No numerical evidence as proof (all claims either proved or flagged).
- No silent change of quantifier/normalization: the correlation convention is the object,
  the hat-unit alternative is documented as the ambiguity, not silently chosen.
- The `CERTIFIED_F8_GE` input (T2) is assumed for the block-energy sub-lemma, not proved.

## 6. Tool / source constraints
Python `py -3.10` (numpy 2.2.6, mpmath 1.3.0), `PYTHONUTF8=1`. Snapshot read (not assumed):
`Defs.lean`, `ZeroSide/{Mult,RankTraceMult,Final}.lean`, `LinAlg/*`, `ThmD/{AssemblyD,Mult}.lean`;
OpenAI `proof.md`; kernel-limit run `R-…-kernellimit-b9e1`. Version/sha in `repro_manifest.md`,
`SHA256SUMS`.
