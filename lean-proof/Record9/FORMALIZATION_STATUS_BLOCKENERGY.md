# Formalization status — T1c-2a block energy (Stage C)

Modules: `lean-proof/Record9/Record9/BlockEnergy.lean` (`Record9.BlockEnergy`),
`lean-proof/Record9/Record9/BlockEnergyLinearReindex.lean`
(`Record9.BlockEnergyLinearReindex`),
`lean-proof/Record9/Record9/BlockEnergyDecomp.lean` (`Record9.BlockEnergyDecomp`), and
`lean-proof/Record9/Record9/BlockEnergyPairBound.lean` (`Record9.BlockEnergyPairBound`),
namespace `Zeta23.ThmD`. Pinned mathlib `51e6992e`, Lean `v4.33.0-rc2`.

Status line: **CLOSED (T1c-2a block energy machine-proved)** —
`lake build Record9.BlockEnergy`, `Record9.BlockEnergyLinearReindex`,
`Record9.BlockEnergyDecomp`, and `Record9.BlockEnergyPairBound` exit 0, no
`sorry`/`admit`/`axiom` outside comments. The full inequality `blockEnergyFromF8` is now a
machine-proved `theorem` (`blockEnergyFromF8_fact`), with `#print axioms` =
`{propext, Classical.choice, Quot.sound}`.

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
- **`f8PairPart_le_blockEnergy_fact`** (in `Record9.BlockEnergyPairBound`) — the pair part is
  bounded by the block energy:
  `(∀ i, 0 ≤ g i) → f8PairPart g ≤ blockEnergy g`.
  Proved by flattening `f8PairPart` into pair-occurrences, bounding each pair's fiber
  multiplicity by `9−s`, and comparing to `blockEnergy`'s `2·wMT` terms.
  `lake build Record9.BlockEnergyPairBound` exit 0; `#print axioms` =
  `{propext, Classical.choice, Quot.sound}`.
- **`blockEnergyFromF8_fact`** (in `Record9.BlockEnergyPairBound`) — **the full T1c-2a
  statement is closed**: `blockEnergyFromF8` is a theorem, obtained by applying
  `blockEnergyFromF8_of_parts` to the two proved finite-counting facts above.

## 3. Remaining open obligations

None. Both finite-counting obligations are machine-proved and the full `blockEnergyFromF8`
is closed as `blockEnergyFromF8_fact`.

## 4. Machine evidence

| Command | Exit | Evidence |
|---|---|---|
| `lake build Record9.BlockEnergy` | **0** | "Build completed successfully (8839 jobs)"; compiler errors only (no sorry/admit/axiom) |
| `lake build Record9.BlockEnergyLinearReindex` | **0** | "Build completed successfully (8840 jobs)"; compiler errors only (no sorry/admit/axiom) |
| `lake build Record9.BlockEnergyDecomp` | **0** | "Build completed successfully (8841 jobs)"; compiler errors only (no sorry/admit/axiom) |
| `lake build Record9.BlockEnergyPairBound` | **0** | "Build completed successfully (8842/8843 jobs)"; compiler errors only (no sorry/admit/axiom) |
| `#print axioms f8WindowSum_eq_linear_add_pair_fact` | clean | `[propext, Classical.choice, Quot.sound]` |
| `#print axioms f8PairPart_le_blockEnergy_fact` | clean | `[propext, Classical.choice, Quot.sound]` |
| `#print axioms blockEnergyFromF8_fact` | clean | `[propext, Classical.choice, Quot.sound]` |
| comment-aware sorry/admit/axiom scan | clean | no `sorry`/`admit`/`axiom` outside the header disclaimer |

## 5. Honest note

The full `blockEnergyFromF8` is now a machine-proved theorem. All T1c-2a components —
linear-part route, certified sum, summed-F₈ decomposition, pair-part bound, and closing
assembly — are verified. This removes the T1c-2a sub-step from the open list; remaining
Stage C analytic sub-steps are T1c-2c pinching, T1c-2d uniformity, full-O(S) Δ survival,
and T2 certificate reflection.
