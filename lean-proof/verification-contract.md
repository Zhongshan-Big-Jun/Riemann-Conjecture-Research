# Verification problem contract — C₉ = 0.6730665 record (lean-verify Phase 1)

## Informal theorem contract (from runs/…/f9push-d3b58c/candidate_proof.md)

**T(ζ)**: With the certified k=9 pressure bound F₈ ≥ 392/100000 for all gᵢ ≥ 0, one has
unconditionally, in ε-form:

    ∀ ε > 0, ∃ T₀, ∀ T ≥ T₀: (1 − A₀/m)·N₀ˢ(T,2T) ≥ (H_MT − (m−1)/(500m) − ε)·N(T,2T)

with n = ⌈1/f⌉−1 = 255, m = 8+n = 263, A₀ = f·n = 2499/2500 < 1,
H_MT = 3/2 − (1/√2)·cot(1/√2) = 2 − 1/c₁* (Lean-verified baseline, ε-form: thmD₀_simple_mult).
Equivalently liminf N₀ˢ(T,2T)/N(T,2T) ≥ (657,500·H_MT − 1,310)/655,001 = 0.673066472675939665848…

**T(ξ′)**: the same chain with H_{ξ′} = 2 − κ₁(1, v_MT) = 0.86788886519905193555… gives
liminf N₀ˢ_{ξ′}/N_{ξ′} ≥ (657,500·H_{ξ′} − 1,310)/655,001 = 0.86920009109661916184…

Boundary cases: gᵢ ≥ 0 (pressure variables); T real, dyadic window (T, 2T]; ε > 0.
Completion criteria: (i) machine build of the snapshot baseline; (ii) obligation map with
fidelity results; (iii) independent audit; (iv) structured verdict.

## Contract audit note

The informal chain (steps 1–7) was audited at the paper level (B1–B6 manager PASS,
2026-08-15; extpress precedent PASS-with-limits). The Lean verification scope for this
run: O1 (baseline — snapshot machine build) is the machine-checkable part; O2–O5
(chain + certificate) are OPEN formalization obligations (Stage C contract,
reports/lean-formalization-contract.md). Numerical evidence (certificate computation,
constant digits) is recorded separately and never presented as proof.
