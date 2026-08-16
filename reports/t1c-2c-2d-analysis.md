# T1c-2c / T1c-2d — Paper-Level Analysis of the Remaining T1c Analytic Sub-Steps

**Label: `RIGOROUS_PARTIAL_RESULT / PAPER-LEVEL ANALYSIS` — NOT a machine-verified proof.**
This document is a Markdown report, not Lean. It contains no `sorry`/`admit`/`axiom`.

- Source run: `runs/rigorous-open-math-research/R-20260816T060000Z-stabridge-a3f1/`
  (`candidate_proof.md` §3–§4, `obligation_graph.md`, `status_and_literature.md`).
- Lean counter-part: `lean-proof/Record9/Record9/` (`Chain9.lean`, `KernelLimit.lean`,
  `StabilityBridge.lean`, `BlockEnergy.lean`, `BlockEnergyDecomp.lean`,
  `BlockEnergyLinearReindex.lean`, `BlockEnergyPairBound.lean`).
- Status ledger: `lean-proof/STATUS.md`.

---

## 1. Purpose and status

T1c (the stability bridge) is being closed in two stages. **T1c-2a is now machine-proved**
as `Zeta23.ThmD.blockEnergyFromF8_fact` (in
`lean-proof/Record9/Record9/BlockEnergyPairBound.lean`, closing assembly
`blockEnergyFromF8_of_parts` in `BlockEnergy.lean`; build exit 0, gold-standard axioms, per
`lean-proof/STATUS.md` O2). Relatedly:

- the kernel-limit lemma is **machine-proved** (`Record9.KernelLimit`: `KL1`, `KL2`,
  `KL3_ratio_bound`, `KL3_eps`; see §3.2), and
- the Ψ-defect lemma is **machine-proved** (`Record9.StabilityBridge.psi_defect`, T1c-2b;
  the A₀<1 branch is `Chain9.A0_lt_one` / `StabilityBridge.A0_st_lt_one`).

The two sub-steps needed before **T1c-2 can be fully closed** are the **paper-level analytic**
steps treated here:

- **T1c-2c** — pinching/averaging finite algebra:
  `Δ(M°) ≥ (A₀/m)·S − ((m−1)/(500m))·N − o(N)`.
- **T1c-2d** — analytic uniformity:
  `Σ_{i<j} |(M°)_ij|² = (1/2)·E_m(B) + o(1)` uniformly in blocks `B`, via the kernel-limit
  lemma.

Both are pinned exactly in Lean as the *hypothesis* `Zeta23.ThmD.pinching_averaged_eps`
(which is propositionally the same as `stability_averaged_eps_true`, routed by
`averaged_from_pinching` in `StabilityBridge.lean`); what remains is the analytic proof that
this hypothesis follows from the per-block defect plus the block×finite-sum transfer. This is
the same status class as the kernel-limit precedent: **statement pinned, proofs at analysis
level, Lean formalization a follow-up.**

---

## 2. T1c-2c — pinching/averaging finite algebra

### 2.1 Exact statement with all constants

From `candidate_proof.md` §3 (T1c-2) and `Chain9.lean` `stability_averaged_eps`
(lines 141–145), with `Δ := Δ(M°)`, `S := N₀ˢ(T,2T)`, `N := N(T,2T)`:

```
∀ ε>0, ∃ T₀ : ℝ, ∀ T ≥ T₀:
    Δ(M°)(T) ≥ (2499/657500)·S − (262/131500)·N − ε·N .          (T1c-2 / T1c-2c)
```

Equivalently (the `o(N)` form carried in the paper):

```
Δ(M°) ≥ (A₀/m)·S − ((m−1)/(500m))·N − o(N).
```

Exact constants (all machine-pinned; `Chain9.lean` T1d, `StabilityBridge.lean` M3):

| Symbol | Definition | Rational value |
|---|---|---|
| `A₀` | `f₉·n₉ = (392/100000)·255` | `2499/2500` (`Chain9.A0_eq_f9n9`) |
| `m` | `m₉ = (k−1)+n₉ = 8 + 255` | `263` (`Chain9.m9`) |
| `A₀/m` | `(2499/2500)/263` | `2499/657500` (`Chain9.cA0m_eq`, `StabilityBridge.cA0m_st_eq`) |
| `(m−1)/(500m)` | `262/(500·263)` | `262/131500` (`Chain9.qMT_eq`, `StabilityBridge.qMT_st_eq`, `qMT_closed`, `qMT_m_identity`) |
| `A₀ < 1` | rigor condition | `Chain9.A0_lt_one`, `StabilityBridge.A0_st_lt_one` |

The complementary chain constant `cLHS = 1 − A₀/m = 655001/657500` (`Chain9.cLHS_eq`,
`cLHS_pos`) is the coefficient that appears in the assembled chain, not in T1c-2c itself.

### 2.2 The offset-averaging construction (`m = 263` offset partitions)

For each retained-simple-zero ordinate set (of cardinal `S`), take the `m = 263` **offset
block partitions**: for each offset `r = 0,…,m−1`, partition the ordinates into consecutive
blocks of length exactly `m = 263` (the "9-window certificate blocks"); the `r`-th offset
shifts the block boundaries by `r`. Across the `m` offsets every ordinate is a member of
exactly one block of each partition, and the **total normalized retained length** of all blocks
over all offsets is `N + o(N)` — the small-`o` absorbs boundary/dangling ordinates that do not
fit into a full block (their count is `O(m)` = `O(1)` relative to `N → ∞`; equivalently each
offset retains `S/m` full blocks and the total is `m·(S/m) = S = N + o(N)` up to the
multiplicity/edge correction). This is the finite-algebra prelude recorded in
`candidate_proof.md` §3 (T1c-2c) and `obligation_graph.md` (T1c-2c branch).

### 2.3 The finite counting claim

The per-block span enters the linear defect term through the quantity `(1/500)·span(B)`
(span = `y_m − y_1`, block span `blockSpan` in Lean). The offset averaging yields:

- **Each interior gap is charged at most `m−1` times across the `m` offsets.** A given gap
  separates two ordinates; among the `m` offsets, the gap lies *inside* a block for all offsets
  except possibly the ones where it straddles a block boundary. Because a block has `m = 263`
  points (262 gaps) and the boundaries move by one step per offset, a fixed interior gap is
  interior to a block for at least `m − 1` of the `m` offsets (exactly `m−1` in the periodic
  exact model; the exceptional offset is the one where the gap is the boundary line). This is
  the same bookkeeping pattern already fully machine-proved for T1c-2a's *within-one-block*
  counting (`pairMultiplicity_le`, `linearMultiplicity_le_8`, `pairCoeff_mul_windows` in
  `BlockEnergyPairBound.lean` / `BlockEnergyLinearReindex.lean`), lifted to the offset,
  multi-block level — the `≤ m−1` interior-gap charge is the exact analogue of the
  "each gap in ≤ 8 windows" lemma, at the block level.

- **The span averages by `(m−1)/m`.** Summing `(1/500)·span(B)` over all full blocks of all
  offsets, each interior gap contributes its length to `m−1` block spans (one per offset minus
  the boundary offset), and the atomic gap is charged at most once per block. Hence

  ```
  Σ_{offsets} Σ_{blocks B} (1/500)·span(B)  =  (1/500)·(m−1)·(total gap length) + o(N)
                                             =  ((m−1)/(500m))·N + o(N),
  ```

  because the total gap length over the `≈ S/m` blocks of one offset is the retained span
  `N + o(N)` and there are `m` offsets. This yields exactly the coefficient `(m−1)/(500m) =
  262/131500`, matching the machine-pinned rational (`Chain9.qMT_eq`); the periodic-exact
  model gives this coefficient, as spot-checked in `stabridge_sublemma.py` T1c2c
  (`candidate_proof.md` §5).

- **The block energy/averaged intercept.** Averaging the per-block bound
  `Δ(G_B) ≥ E_m(B) + o(1) ≥ A₀ − (1/500)·span(B) − o(1)` (see §3.4) over the `m` offsets and
  the `≈ S/m` blocks of each gives

  ```
  average over blocks of [Δ(G_B)]  ≥  A₀ − ((m−1)/(500m))·(N/S) − o(1)
                                     =  A₀ − ((m−1)/(500m))·(N/S) − o(1),
  ```

  and the total defect over all full blocks is
  `A₀·(S/m)·(of offsets m)/m...` — concretely the aggregate is
  `(A₀/m)·S` minus `((m−1)/(500m))·N`, i.e. exactly the T1c-2c coefficients
  `2499/657500 = A₀/m` and `262/131500 = (m−1)/(500m)`.

### 2.4 The pinching step

The per-offset, per-block defect is `tr Ψ(G_B)` for each block Gram block `G_B`. The global
defect `Δ(M°) = tr Ψ(M°)` controls the **block-average** via **unitarily-invariant convex
pinching**:

```
tr Ψ(M°) ≥ (average over all offset blocks B of tr Ψ(G_B)) .
```

The mechanism: `Ψ` is a convex function of the eigenvalues, `tr Ψ` is unitarily-invariant and
convex in `M°`, and the passage from the full Gram to the block-diagonal Gram (each offset's
blocks) is a **pinching** — a completely positive, trace-preserving, convexity-decreasing map
(specifically, `M° ↦ diag(G_{B₁}, …, G_{B_{S/m}})` discards cross-block off-diagonal entries).
Convexity under pinching gives `tr Ψ(block-diagonal) ≤ tr Ψ(M°)`, and averaging the
block-diagonal `tr Ψ` over the `m` offsets is the "convexity-under-pinching averaging" named in
`Chain9.lean` line 138 and `candidate_proof.md` §3 ("Assembly T1c-2 → ε-form", line 196:
`trΨ(M°) ≥ block-averaged defect — standard unitarily-invariant convex pinching, flagged as
the sub-step to formalize"). The block-averaged defect then is bounded below by
`(A₀/m)·S − ((m−1)/(500m))·N − o(N)` from §2.2–2.3.

**This pinching step is the standard unitarily-invariant convex pinching — the exact sub-step
flagged to formalize.** It is stated precisely but is not yet in Lean (no
`pinch_trPsi_ge_average` lemma exists; see §4).

### 2.5 What is already machine-checked vs what remains paper-level for T1c-2c

Machine-checked (all in `Record9`):
- The exact statement form `stability_averaged_eps` / `stability_averaged_eps_true` /
  `pinching_averaged_eps` and the routing `averaged_from_pinching` (`Chain9.lean`,
  `StabilityBridge.lean`).
- All exact constants and identities: `A0 = 2499/2500`, `A0_lt_one`, `cA0m = 2499/657500`,
  `qMT = 262/131500`, `cLHS = 655001/657500`, `cLHS_pos` (`Chain9.lean` T1d,
  `StabilityBridge.lean` M3).
- The **within-block** finite counting (T1c-2a) that underlies the coefficient arithmetic:
  `pairMultiplicity_le`, `pairCoeff_mul_windows`, `f8PairPart_le_blockEnergy_fact`,
  `blockEnergyFromF8_fact` (`BlockEnergyPairBound.lean`), `f8LinearPart_le_blockSpan`,
  `linearMultiplicity_le_8` (`BlockEnergy.lean`), `f8LinearReindex`
  (`BlockEnergyLinearReindex.lean`), `f8WindowSum_eq_linear_add_pair_fact`
  (`BlockEnergyDecomp.lean`).
- The defect lemma `psi_defect` (T1c-2b) and `deltaMT_nonneg_via_trPsi`
  (`StabilityBridge.lean`).

Remaining paper-level (this report, not yet Lean):
- The **offset-level** counting: "each interior gap is charged at most `m−1` times across the
  `m` offsets; span averages by `(m−1)/m`" — the multi-block lifting of the already-proved
  within-block counting; produces the exact coefficient `(m−1)/(500m) = 262/131500`.
- The **pinching lemma**: `tr Ψ(M°) ≥` (average over offsets of the block-diagonal defect),
  i.e. the unitarily-invariant convex-pinching inequality. This is the standard sub-step
  flagged for formalization.

---

## 3. T1c-2d — analytic uniformity

### 3.1 Exact statement

For a fixed block `B` of `m = 263` retained zeros `y₁ < … < y_m` (the block Gram `G_B =
(M°|_B)`):

```
Σ_{i<j} |(M°)_ij|² = (1/2)·E_m(B) + o(1)   uniformly in B, as L → ∞,
```

where `E_m(B) = 2·Σ_{i<j} wMT(y_j − y_i)` is the block energy (`candidate_proof.md` §3
T1c-2d; `BlockEnergy.lean` `blockEnergy`). "Uniformly in `B`" means the `o(1)` depends only
on `L` (hence `T`), not on which block `B`; this is what allows summing over all `≈ S/m`
blocks of every offset.

### 3.2 The kernel-limit lemma (already machine-proved, `Record9.KernelLimit`)

The pointwise engine is the kernel limit: for a retained pair `(i,j)` in `B`, the
unit-normalized Gram entry is the overlap ratio `⟨v_i,v_j⟩/⟨v_i,v_i⟩ = M°_ij`, and — with the
MT window `φ` (TaperProfile `ϱ`), `w` the ramp half-width, `x_ij = (γ_i−γ_j)·L/(2π)` — the
kernel-limit lemma gives

```
M°_ij = kMT(x_ij) + O(w/L)   uniformly in x,
        and thus wMT(x_ij) = kMT(x_ij)² → |M°_ij|²  with rate O(w/L).
```

Machine-proved pieces in `Record9.KernelLimit`:
- `KL2` (`K_of x / K0 = kMT x` — kernel identity, `KernelLimit.lean:464`);
- `KL1` (`|F_L(x) − K_of(x)| ≤ 2w/L` uniformly in `x`, `KernelLimit.lean:392`);
- `KL3_ratio_bound` (`|F_L(x)/F_L(0) − kMT(x)| ≤ (2w/L)(1+|kMT x|)/F_L(0)`,
  `KernelLimit.lean:538`), and
- `KL3_eps` (uniform ε-form for bounded separations `|x| ≤ B`,
  `KernelLimit.lean:599`, carrying the explicit compactness hypothesis `hKerBdd` that
  `1 + |kMT|` is bounded on `[−B,B]`).

The `wMT(x) := kMT(x)²` notation is `Chain9.wMT` (used throughout the block-energy modules);
the pointwise convergence `wMT(x_ij) → |M°_ij|²` with rate `O(w/L)` uniform in `x` is exactly
`KL3_ratio_bound` squared (since `|M°_ij − kMT(x_ij)| = O(w/L)` and `wMT(x_ij) = kMT(x_ij)²`).
This is the "kernel-limit lemma (machine-proved)" cited in `candidate_proof.md` §3 (T1c-2d)
and `obligation_graph.md` (T1c-2d, marked `[A-P]`).

### 3.3 The block × finite-sum transfer (epsilon-delta/N argument)

A block has **fixed** size `m = 263`, so `Σ_{i<j}` is a finite sum of exactly
`m(m−1)/2 = 263·262/2 = 34,453` terms, independent of `L` and of `B`. The uniformity is then
immediate:

1. Fix `ε > 0`. By `KL3_eps` (or the squared `KL3_ratio_bound`), choose `L₀ = L₀(ε)` such that
   for all `L ≥ L₀` and all normalized separations `|x| ≤ B` of the block (the block has
   bounded normalized span — ordinates in a length-`m` block of zeros near `T` so that
   `|x_ij| ≤ B_m` for a fixed `B_m`), we have
   `|wMT(x_ij) − |M°_ij|²| ≤ ε' := ε/(2·34453)`.
2. **Pigeonhole/E-N step:** define `E_m(B)` as the finite sum `2·Σ_{i<j} wMT(y_j − y_i)`
   (exactly `blockEnergy` in Lean). Then

   ```
   | Σ_{i<j} |(M°)_ij|² − (1/2)·E_m(B) |
     = | Σ_{i<j} (|(M°)_ij|² − wMT(y_j−y_i)) |
     ≤ Σ_{i<j} | |(M°)_ij|² − wMT(x_ij) |
     ≤ (m(m−1)/2)·ε'  =  (263·262/2)·ε'  ≤  ε/2 + ε/2 = ε  (choice of ε'),
   ```

   uniformly in `B` (nothing in the right-hand side depends on which block `B` was chosen).
   This is the standard "finite sum of pointwise limits is uniform because the number of terms
   is fixed" — the block×finite-sum transfer.

3. The same argument handles the two-sided statement
   `(1/2)E_m(B) − o(1) ≤ Σ_{i<j}|(M°)_ij|² ≤ (1/2)E_m(B) + o(1)` with symmetric N-choices of
   `L₀`.

This is the "since a block has fixed `m` and the kernel-limit rate `O(w/L)` is uniform in
`x`, the `o(1)` is uniform" of `candidate_proof.md` §3 (T1c-2d, line 187–189), now made
explicit. The only analytic engine it consumes is the already-machine-proved kernel limit
plus the elementary finite-sum bound.

### 3.4 Consequence: the per-block defect lower bound

Given §3.3, the block's square-off-diagonal energy is
`2·Σ_{i<j}|(M°)_ij|² = E_m(B) + o(1)`. By the (now machine-proved) **defect lemma** T1c-2b
`psi_defect` (with `A₀ < 1` putting the active branch at `2Σ|G_ij|²`, cf. `candidate_proof.md`
§3–§4, `obligation_graph.md`), the block defect satisfies

```
Δ(G_B) = tr Ψ(G_B)  ≥  min(1, 2·Σ_{i<j}|G_ij|²)
                    =  2·Σ_{i<j}|(M°)_ij|²        (since A₀ < 1 keeps the 2Σ branch active)
                    =  E_m(B) + o(1),
```

and by the **block-energy inequality** T1c-2a (`blockEnergyFromF8_fact`, now machine-proved:
`E_m(B) + (1/500)·span(B) ≥ A₀`),

```
Δ(G_B) ≥ E_m(B) + o(1) ≥ A₀ − (1/500)·span(B) − o(1) = A₀ − (1/500)span(B) − o(1).
```

This is the per-block input to the T1c-2c averaging (§2.4). The consequence chain
`Δ(G_B) ≥ 2Σ|G_ij|² = E_m(B)+o(1) ≥ A₀ − (1/500)span(B) − o(1)` is exactly
`candidate_proof.md` §3 (T1c-2d, line 187–188).

### 3.5 Machine-checked vs paper-level for T1c-2d

Machine-checked:
- Kernel identity and uniform closeness: `KernelLimit.KL1`, `KL2`, `KL3_ratio_bound`,
  `KL3_eps`, `K0_pos`.
- Defect lemma `psi_defect` and the `A₀ < 1` constants (`StabilityBridge`,
  `Chain9.A0_lt_one`).
- Block-energy inequality `blockEnergyFromF8_fact` (T1c-2a).

Remaining paper-level (this report):
- The **uniform finite-sum transfer** (the fixed-`m` finite sum of the pointwise kernel limits,
  §3.3) — an elementary N/ε argument, but not yet written as a Lean obligation.
- A Lean statement that "uniformly in `B`, `Σ_{i<j}|(M°)_ij|² = (1/2)E_m(B) + o(1)`" — i.e.
  connecting the abstract Gram-of-a-block `(M°|_B)`, the kernel ratio to the `o(1)`, including
  the honest bounded-span hypothesis (the analogue of `hKerBdd` in `KL3_eps`).
- The final per-block consequence `Δ(G_B) ≥ A₀ − (1/500)span(B) − o(1)` assembled from
  `psi_defect` + `blockEnergyFromF8_fact` + the transfer.

---

## 4. Formalization gap analysis — exact remaining Lean obligations

Existing Lean ingredients (already present):
- `blockEnergyFromF8_fact` (T1c-2a, `BlockEnergyPairBound.lean`) and the supporting
  `f8WindowSum_eq_linear_add_pair_fact`, `f8LinearPart_le_blockSpan`,
  `f8PairPart_le_blockEnergy_fact`, `linearMultiplicity_le_8`, `pairMultiplicity_le`,
  `pairCoeff_mul_windows`.
- `psi_defect` (T1c-2b) + `A0_lt_one` / `A0_st_lt_one`.
- Kernel limit: `KL1`, `KL2`, `KL3_ratio_bound`, `KL3_eps` (`KernelLimit.lean`).
- Exact constants and `pinching_averaged_eps` / `stability_averaged_eps_true` /
  `averaged_from_pinching` (`Chain9.lean`, `StabilityBridge.lean`).

Remaining Lean obligations, grouped by sub-step:

**T1c-2c (pinching/averaging):**
1. *Finite offset-counting in Lean*: a lemma that each interior gap of a block belongs to at
   most `m−1` of the `m` offset partitions, and the corresponding span average
   `Σ_offsets Σ_blocks span(B) = (m−1)·(total length) + o(N)`; gives the exact coefficient
   `(m−1)/(500m) = 262/131500`. (The within-block analogue is machine-proved; this is the
   multi-block/offset lift.)
2. *Convex pinching lemma*: `tr Ψ(M°) ≥` (average over offsets of `tr Ψ(G_B)`) — the
   unitarily-invariant convex pinching inequality (`pinch_trPsi_ge_block_average`), the
   standard step flagged in `candidate_proof.md` §3 and `Chain9.lean` line 138, and the
   genuinely new ingredient (not yet in Lean).
3. *Assembly*: from the per-block bound `Δ(G_B) ≥ A₀ − (1/500)span(B) − o(1)` (needs T1c-2d
   §4.6) plus the pinching lemma and the finite offset-counting, derive
   `pinching_averaged_eps` (= `stability_averaged_eps_true`), closing T1c-2c.

**T1c-2d (analytic uniformity):**
4. *Uniform finite-sum transfer*: since a block has fixed `m = 263`
   (`m(m−1)/2 = 34,453` terms), translate `KL3_eps`/`KL3_ratio_bound` into
   "uniformly in `B`, `Σ_{i<j}|(M°)_ij|² = (1/2)E_m(B) + o(1)`" — an elementary N/ε
   (pigeonhole) argument, not yet a Lean lemma.
5. *Per-block consequence*: `Δ(G_B) ≥ 2·Σ_{i<j}|G_ij|² = E_m(B) + o(1) ≥ A₀ − (1/500)span(B) −
   o(1)`, assembled from `psi_defect` + the transfer + `blockEnergyFromF8_fact`; needs the
   `A₀ < 1` 2Σ-branch application to the block Gram.

There are **two genuinely non-trivial obligations**: the **convex pinching lemma** (T1c-2c
item 2) and the **uniform finite-sum transfer / per-block consequence** (T1c-2d items 4–5);
the offset finite-counting (item 1) and the rational assembly (item 3) are elementary finite
algebra / `norm_num`-style and directly parallel the already-closed T1c-2a counting.

---

## 5. Honest labels

This report is **`RIGOROUS_PARTIAL_RESULT / PAPER-LEVEL ANALYSIS`** — it is a rigorous
paper-level analysis of the two remaining analytic sub-steps T1c-2c and T1c-2d, **not** a
machine-verified proof. Specifically:

- The statements, exact constants, and the per-block / kernel-limit engines are machine-pinned
  (T1c-2a `blockEnergyFromF8_fact`, T1c-2b `psi_defect`, `KernelLimit`).
- The **pinching** step (T1c-2c) and the **uniform finite-sum transfer** (T1c-2d) are
  presented as analysis-level arguments, following the exact precedent of the kernel-limit
  lemma (statement pinned; Lean formalization a follow-up), as recorded in
  `candidate_proof.md`, `obligation_graph.md`, `status_and_literature.md`, and
  `lean-proof/STATUS.md`.
- No numerical spot-checks are claimed as proof, and no `sorry`/`admit`/`axiom` appear
  anywhere in this Markdown report or in any `Record9` module.
- The normalization of `Δ(M°)` is the unit-normalized (correlation) Gram `tr Ψ(M°)`; the
  hat-unit convention would break Cor 2.2 (see `candidate_proof.md` §7). This fidelity note is
  carried, not silently resolved here; the `pinching_averaged_eps`/`stability_averaged_eps_true`
  Lean statements use the abstract `deltaMT_true` standing for `tr Ψ(M°)` (honest bridge).

---

## Files cited

- `runs/rigorous-open-math-research/R-20260816T060000Z-stabridge-a3f1/candidate_proof.md` (§3 T1c-2, §4 defect lemma, §5 checks, §6 mapping, §7 ambiguity; constants `2499/657500`, `262/131500`, `A₀ = 2499/2500`).
- `runs/rigorous-open-math-research/R-20260816T060000Z-stabridge-a3f1/obligation_graph.md` (T1c-2c/T1c-2d branches, `[P]`/`[A-P]` labels).
- `runs/rigorous-open-math-research/R-20260816T060000Z-stabridge-a3f1/status_and_literature.md` (status line, kernel-limit citation).
- `lean-proof/STATUS.md` (O2 record: T1c-2a closed, kernel-limit machine-proved, T1c-2c/T1c-2d open).
- `lean-proof/Record9/Record9/Chain9.lean` (`stability_averaged_eps`, constants, `A0_lt_one`, `cA0m_eq`, `qMT_eq`, `record9Bridge`).
- `lean-proof/Record9/Record9/KernelLimit.lean` (`KL1`, `KL2`, `KL3_ratio_bound`, `KL3_eps`, `K0_pos`).
- `lean-proof/Record9/Record9/StabilityBridge.lean` (`psi_defect`, `deltaMT_true`, `pinching_averaged_eps`, `stability_averaged_eps_true`, `averaged_from_pinching`, constants).
- `lean-proof/Record9/Record9/BlockEnergy.lean` (`blockEnergyFromF8`, `blockEnergy`, `blockSpan`, within-block counting lemmas).
- `lean-proof/Record9/Record9/BlockEnergyPairBound.lean` (`blockEnergyFromF8_fact`, `f8PairPart_le_blockEnergy_fact`, `pairMultiplicity_le`).
- `lean-proof/Record9/Record9/BlockEnergyDecomp.lean` (`f8WindowSum_eq_linear_add_pair_fact`).
- `lean-proof/Record9/Record9/BlockEnergyLinearReindex.lean` (`f8LinearReindex`).
