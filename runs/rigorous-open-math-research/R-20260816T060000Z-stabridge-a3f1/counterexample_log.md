# Counterexample / failure log — R-20260816T060000Z-stabridge-a3f1

Run: `R-20260816T060000Z-stabridge-a3f1`. Failures, edge cases, and the ambiguity's
counter-candidate.

## 1. Normalization counter-candidate (hat-unit Δ)

**Candidate rejected:** defining `Δ(M°)(T) = tr Ψ(Â(T))` with `Â = Az/(aL²)` (the hat-unit
Gram that `ZeroSide/Mult.lean mult_two` / `Defs.lean hat` actually use).

**Why it fails.** Numerically (C7 + raw-overlap check): for the hat-unit Gram the
off-diagonal squares satisfy `|Â_ab|²/wMT(x_ab) = (K(0)/(aL))² → 0`, so
`2Σ|G_ij|² → 0` relative to `E_m`. Meanwhile the hat-unit diagonal
`Â_aa = ‖v_γ‖²/(aL²) = F_L(0)/(aL) → 0`, so every eigenvalue of `Â` → 0 and
`tr Ψ(Â) = ΣΨ(μ_i) → Σ 1 = S`. Hence `Δ(Â) ≈ S`.

**The defect.** Plugging `Δ(Â)≈S` into Cor 2.2 `S ≥ H_MT·N + Δ(M°) − o(N)` would give
`S ≥ 0.6725·N + S − o(N)`, i.e. `0 ≥ 0.6725·N − o(N)`, false since `S ≈ 0.67N ≪ N`.
So the hat-unit object is **not** the Δ of the bridge — it both breaks T1c-2's target
(`Δ ≥ (A₀/m)S` is trivially true but for the wrong reason) and makes T1c-1 impossible.

**Resolution used:** the unit-normalized (correlation) Gram, `M°_ab = ⟨v_a,v_b⟩/‖v‖²`,
diagonal `=1`, off-diagonal `→ kMT(x)` (kernel-limit), `Σ|G_ij|² = (1/2)E_m + o(1)`,
`Δ(M°) ≈ E_m` (order `O(S)`), consistent with both T1c-1 and T1c-2.

## 2. `min(1, 2Σ|G_ij|²)` branch — not an error but a caveat
For a block whose `2Σ|G_ij|² ≥ 1` the defect lemma caps at `1` (still ≥ A₀ because A₀<1);
the `2Σ|G_ij|²` branch is used where `2Σ|G_ij|²` (i.e. `E_m`) is `≲ A₀<1`. Both directions
hold; no counterexample.

## 3. Offset-averaging finite model — boundary caveat
Naive finite non-periodic tiling of the offset-averaging span gave `(1/m)Σ span ≈ (m−1)P/m`
with a boundary residue; the clean identity `(m−1)/(500m)` is exact on the periodic model
(no boundary). Boundary effects are `o(N)` in the actual chain (tail zeros excluded), so the
`−o(N)` absorbs them; not a defect of the target but a finite-check artifact (recorded; the
exact rational coefficients are what matter, verified via `A0/m` and `(m−1)/(500m)`).

## 4. No counterexample found
- Lemma 2.1: no violation over random Hermitian Q / PSD P (C3).
- Defect lemma `trΨ(G) ≥ min(1,2Σ|G_ij|²)`: no violation over random PSD (C4).
- All 21 checks pass; none is a proof.

## Search code
`reproducibility/stabridge_checks.py`, `stabridge_sublemma.py` (seeded, deterministic);
see run logs `check_run.log`, `sublemma_run.log`.
