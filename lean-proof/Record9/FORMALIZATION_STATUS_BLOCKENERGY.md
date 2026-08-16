# Formalization status — T1c-2a block energy (Stage C)

Modules: `lean-proof/Record9/Record9/BlockEnergy.lean` (`Record9.BlockEnergy`),
`lean-proof/Record9/Record9/BlockEnergyLinearReindex.lean`
(`Record9.BlockEnergyLinearReindex`), and
`lean-proof/Record9/Record9/BlockEnergyDecomp.lean` (`Record9.BlockEnergyDecomp`),
namespace `Zeta23.ThmD`. Pinned mathlib `51e6992e`, Lean `v4.33.0-rc2`.

Status line: **REPAIRABLE_GAP (one of two finite-counting obligations now closed)** —
`lake build Record9.BlockEnergy`, `Record9.BlockEnergyLinearReindex`, and
`Record9.BlockEnergyDecomp` exit 0, no `sorry`/`admit`/`axiom` outside comments. The summed-F₈
decomposition `f8WindowSum = f8LinearPart + f8PairPart` is machine-proved; the full
inequality `blockEnergyFromF8` is now reduced to exactly one finite-counting obligation
(`f8PairPart_le_blockEnergy`), still open in this bounded pass.

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
    `pairCoeff_mul_windows`.

## 2. Proven this pass (machine-checked, sorry-free)

- **`linearMultiplicity_le_8`** — every gap `r` lies in at most 8 of the 255 windows. The
  injective witness maps a containing window `j` to the offset `r − j ∈ Fin 8`.
- **`f8LinearPart_le_blockSpan`** — for nonnegative `g`, the linear part of the summed F₈ is
  `≤ (1/500)·blockSpan g`. Uses `linearMultiplicity ≤ 8` and `linear_rate_identity`.
- **`f8WindowSum_ge_certified`** — (route step 1) if every 9-window satisfies
  `392/100000 ≤ f8Window g j`, then `2499/2500 ≤ f8WindowSum g` (via `A0_eq_f8_255`).
- **`wMT_nonneg`** — the MT kernel is a square, hence pointwise `≥ 0` (the slack source for
  the dropped separation-≥9 pairs).
- **`blockEnergyFromF8_of_parts`** — the closing assembly lemma: given
  (i) `f8WindowSum g = f8LinearPart g + f8PairPart g` and
  (ii) `f8PairPart g ≤ blockEnergy g`,
  together with the two proven bounds above, the full T1c-2a statement follows.
- **`f8PairPart`** — the exact aggregate pair part of `f8WindowSum` (the `wMT`/quadratic
  terms of `F8gaps`, summed over all 255 windows), defined without any `sorry`.
- **`f8LinearReindex`** (in `Record9.BlockEnergyLinearReindex`) — the linear counting
  identity
  `Σ_j Σ_{n<8} g⟨j+n⟩ = Σ_r (linearMultiplicity r)·g r`,
  i.e. summing each window's 8 gaps equals summing over all gaps weighted by window
  multiplicity. This is the key reindexing step needed for `f8WindowSum_eq_linear_add_pair`.
- **`f8WindowSum_eq_linear_add_pair_fact`** (in `Record9.BlockEnergyDecomp`) — the summed F₈
  decomposes into its linear part plus the pair part:
  `f8WindowSum g = f8LinearPart g + f8PairPart g`.
  Uses `f8LinearReindex` for the linear side and a pointwise `gapSpan`/`gapAt` mod-identity
  for the pair side. `lake build Record9.BlockEnergyDecomp` exit 0; `#print axioms` =
  `{propext, Classical.choice, Quot.sound}`.

## 3. Remaining open obligation (precisely pinned, no sorry)

The full theorem is reduced by `blockEnergyFromF8_of_parts` to one remaining finite-counting
identity, stated as a `def` Prop (compile-only):

1. **`f8PairPart_le_blockEnergy g`** — the pair part is bounded by the block energy:
   each `s`-separated point pair (`1 ≤ s ≤ 8`) is counted `≤ 9−s` times with coefficient
   `2/(9−s)`, contributing `≤ 2·wMT(distance)` (one `blockEnergy` summand); separation-`≥9`
   pairs never appear (their `wMT ≥ 0` contribution is dropped). This is the finite
   `Finset.sum_bij` reindexing / counting identity.

This is finite algebra, Lean-friendly per the contract, but not closed in this bounded pass.

## 4. Machine evidence

| Command | Exit | Evidence |
|---|---|---|
| `lake build Record9.BlockEnergy` | **0** | "Build completed successfully (8839 jobs)"; compiler errors only (no sorry/admit/axiom) |
| `lake build Record9.BlockEnergyLinearReindex` | **0** | "Build completed successfully (8840 jobs)"; compiler errors only (no sorry/admit/axiom) |
| `lake build Record9.BlockEnergyDecomp` | **0** | "Build completed successfully (8841 jobs)"; compiler errors only (no sorry/admit/axiom) |
| `#print axioms f8WindowSum_eq_linear_add_pair_fact` | clean | `[propext, Classical.choice, Quot.sound]` |
| comment-aware sorry/admit/axiom scan | clean | no `sorry`/`admit`/`axiom` outside the header disclaimer |

## 5. Honest note

The full `blockEnergyFromF8` is not yet a `theorem`. The linear-part route (multiplicity ≤ 8,
span bound), route step 1 (certified sum = A₀), the summed-F₈ decomposition, and the closing
assembly are machine-proved; the remaining obligation is the pair-part bound
`f8PairPart_le_blockEnergy`. A future pass should close that final counting identity and
then apply `blockEnergyFromF8_of_parts`.
