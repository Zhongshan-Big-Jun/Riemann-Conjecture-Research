# Formalization status — T1c-2a block energy (Stage C)

Module: `lean-proof/Record9/Record9/BlockEnergy.lean`, module `Record9.BlockEnergy`,
namespace `Zeta23.ThmD`. Pinned mathlib `51e6992e`, Lean `v4.33.0-rc2`.

Status line: **MACHINE_ACCEPTED_PENDING_AUDIT** — `lake build Record9.BlockEnergy` exits 0,
no `sorry`/`admit`/`axiom` outside comments. The exact T1c-2a statement is frozen as
`blockEnergyFromF8`, and the finite bookkeeping sub-lemmas compile; the full inequality
(the `theorem` form of `blockEnergyFromF8`) is the recorded OPEN obligation.

## 1. What is machine-formalized

- `gapAt`, `pointDist`, `blockEnergy`, `blockSpan`, `f8Window`, `f8WindowSum` — exact
  definitions matching the T1c-2a contract.
- `blockEnergyFromF8 : Prop` — the frozen target:
  `∀ g : Fin 262 → ℝ, (∀ i, 0 ≤ g i) → (∀ j : Fin 255, 392/100000 ≤ f8Window g j) →
  2499/2500 ≤ blockEnergy g + (1/500) * blockSpan g`.
- Exact constant identities: `A0_eq_f8_255`, `A0_eq_f8_m_sub_8`.
- Finite bookkeeping:
  - window membership: `windowContainsGap`, `windowContainsPoint`, `windowContainsPair`,
    `windowContainsPair_imp_sep_le_eight`, `windowContainsPair_requires_sep_le_eight`,
    `windowContainsGap_bounds`.
  - linear coefficient: `linearMultiplicity`, `f8LinearPart`, `linear_rate_identity`.
  - pair coefficient: `pairCoeff`, `pairCoeff_of_s0` (with `s0 ≤ 8` hypothesis),
    `pairCoeff_mul_windows`, `pairCoeff_two_over_nine_sub`.

## 2. Machine evidence

| Command | Exit | Evidence |
|---|---|---|
| `lake build Record9.BlockEnergy` | **0** | "Built Record9.BlockEnergy (37s)"; "Build completed successfully (8839 jobs)"; only linter hints |
| comment-aware sorry/admit/axiom scan | clean | no `sorry`/`admit`/`axiom` outside the header disclaimer |

## 3. Open gap

The full inequality `blockEnergyFromF8` is not yet a `theorem`. The missing assembly is the
sum-over-windows decomposition of `f8WindowSum` into:
- a linear part `≤ (1/500)·span` (uses `linearMultiplicity ≤ 8`),
- a pair part `≤ blockEnergy` (uses `pairCoeff`/window-multiplicity counting),
combined with `CERTIFIED_F8_GE` over the 255 windows.

This is the exact T1c-2a obligation remaining; it is finite algebra and Lean-friendly, but
not closed in this bounded pass.
