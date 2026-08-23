# Off-line Pair Bridge — Investigation Report

**Status:** `NUMERICAL_EVIDENCE` / `BLOCKED_REDUCTION`  
**Date:** 2026-08-23  
**Scope:** Focused investigation of the off-line pair bridge for simple zeros of the Riemann zeta function.

No new proof is claimed. The central open lemma is still open. The report records what is
already known from the upstream `trmdy/zeta-simple-zeros-673137` campaign, the new small
numerical probes performed in this session, and the exact remaining gap.

---

## 1. Sources read

- `literature/raw/zeta-simple-zeros-673137/docs/campaign-2.md`
- `literature/raw/zeta-simple-zeros-673137/docs/nine-point.md`
- `literature/raw/zeta-simple-zeros-673137/docs/retuned-record.md`
- `literature/raw/zeta-simple-zeros-673137/docs/proof.md`
- `literature/raw/zeta-simple-zeros-673137/paper/main.tex`
- `literature/raw/zeta-simple-zeros-673137/src/zeta_ext/` (window, kernel, verifier)
- `literature/raw/zeta-zeros-npip/` (Lean bridge/block-matrix/compact-Gram files)
- `literature/raw/zeta-23-lean/Zeta23/ZeroSide.lean` and `PairCeiling/` (off-line pair
  algebra, `p₂₅₆` law)
- `reports/offline-pair-bridge-plan.md`
- `reports/upstream-673137-analysis.md`
- Project status/roadmap reports in `reports/`

---

## 2. Current landscape (for context)

| Quantity | Value | Label |
|---|---|---|
| Certified record in this project (k=9, `f₉=392/100000`) | `0.673066472675939665848…` | VERIFIED from repo record files |
| Best public candidate (retuned 7+9 supporting-plane LP) | `0.673316977142471313480…` | EVIDENCE (candidate, not a proof) |
| Upstream nine-point certified candidate | `0.673312742272245998143…` | EVIDENCE (source report) |
| Horizon ceiling for transfer-operator class | ≈ `0.67331–0.67340` | EVIDENCE (source report) |
| Pure pair-energy class ceiling | ≈ `0.674826` | EVIDENCE (source report) |
| Bandwidth-1 law ceiling `p₂₅₆` | ≈ `0.68182868746…` | VERIFIED exact rational from Lean source; Lean-certified law |
| Mark-2 (off-line/multiple) mass in `p₂₅₆` law | ≈ `31.817%` | VERIFIED as `1 − p₀ = 0.318171312536…` |
| Break-even per-pair residual quoted by campaign-2 | `κ ≈ 0.00122` | EVIDENCE |
| Required average per-pair contribution for 0.675 | ≈ `0.0117/pair` | EVIDENCE |

The key structural fact is that the extremal law at the bandwidth-one ceiling is a
**marked configuration law**: each point carries mark 1 (simple on-line zero) or mark 2
(off-line pair / multiple zero), and the law has only `p₀ ≈ 68.18%` mark-1 mass.  The
current proof machinery prices only the mark-1 mass through the simple-zero Gram defect.
The off-line pair bridge is the missing theorem that would let the remaining `≈31.8%`
mark-2 mass be charged.

---

## 3. The open lemma / target theorem

### 3.1 What is known, in the existing framework

For an admissible window profile `v`, the stability-refined trace method gives

```
S ≥ H(v)·N + tr Ψ(M) − o(N),
```

where

- `S` = number of simple on-line zeros in `(T,2T]`,
- `N` = number of all nontrivial zeros with multiplicity,
- `M` = the unit-normalized Gram matrix of the simple-zero atoms,
- `Ψ(t) = (t−1)²` for `0 ≤ t ≤ 2` and `Ψ(t) = 2t−3` for `t ≥ 2`,
- `H(v)` is the Montgomery–Taylor window constant.

The zero-side matrix `Â` splits into a positive-semidefinite on-line part and
signature-`(1,1)` blocks from off-line hyperbolic pairs.  In the current proofs the
off-line pair contribution is only used to bound the positive index of the indentation
remainder (`n₊(Q) ≤ p`); it is then thrown away.  The bridge seeks to keep or price the
off-line pair blocks instead of discarding them.

### 3.2 The target theorem (as best reconstructable from the available sources)

**Open Lemma (multi-pair composition / off-line pair bridge).**
For the positive-definite band-limited overlap kernel `k_v` arising from an admissible
window, prove a lower bound of the shape

```
Δ_actual  ≥  Δ_fully-virtualized  +  Σ_{off-line pairs} ε_pair
```

(or a kink-regularized / taxed-defect variant of the same inequality), where

- `Δ_actual = tr Ψ(M_actual)` for the Gram-type matrix that includes the off-line pair
  interaction,
- `Δ_fully-virtualized` is the defect obtained by treating each off-line hyperbolic pair
  as a virtual on-line double (retaining the Gram-defect interaction),
- `ε_pair` is a per-pair scalar residual.

If the lemma is proved with the constants already measured in the upstream campaign, the
assembled unconditional bound is expected to land in `0.674–0.675`.  The required average
per-pair residual is approximately `0.0117/pair` in the infinite pair-chain extreme; the
best measured residual in the `~10⁵` adversarial search is `0.00686` for a single pair
(worst case), which is still `5.6×` the break-even `κ=0.00122` for the assembled bound.

**Honesty note.** The exact formal statement of the open lemma is not present in the copied
sources.  `docs/campaign-2.md` gives the summary above, not a complete Lean/theorem
statement with all constants.  The following statement is therefore a **reconstruction**
(EVIDENCE), not a verified formal statement.

---

## 4. Known proved local bridge results

These are reported as proved in `docs/campaign-2.md`; I did **not** independently replay
the certification in this session.  Label: **EVIDENCE (source claim, not independently
re-derived here).**

- **Exact complex Gram formulas for pair blocks.**  With normalization
  `D = L(β−1/2)/(2π)`, the two-member off-line pair blocks have exact complex Gram
  formulas.  This was certified by an `82,751`-box complex-interval (`acb`) proof.
- **Raw local bridge:** `δ ≥ d₁₂ + π`.
- **Robust local bridge:** `B ≥ d₁₂` and `B ≥ T²−1`.
- **One-pair positive-environment theorem:** `Δ ≥ D₂ + (T−1)²`.
- **Safe global regrouping:** there exists a `D₊` regrouping preserving the entire
  simple-zero defect.

These local results are the building blocks for the open composition lemma.  The missing
step is not a single-pair statement; it is the **multi-pair composition** of those local
bounds.

---

## 5. Refuted counterexamples and exact obstructions

Again, these are reported as refuted in `docs/campaign-2.md` and are not independently
re-verified here.  Label: **EVIDENCE (source claim).**

- **Additive local pricing fails.**  An actual-kernel two-pair configuration has
  `δ₂ − 2π = −22.14` (certified), so one cannot simply add the local pair contributions.
- **Stacking local `B` on the full simple defect fails.**  A Schur-deficit witness
  (≈ `0.1249`) shows the local bridge cannot be stacked naively on the full simple-zero
  defect.
- **Shifted-kernel-zero escape.**  The naive safe assembly is evaded by a configuration
  with `θ = π = 0`.
- **Abstract PSD composition is false.**  For two arbitrary positive-semidefinite Gram
  matrices, the two-pair envelope is negative: spectral crowding at the `k₂` kink
  (eigenvalue `2`) can destroy the defect.  This means the global claim is **not**
  provable from positivity alone.

I also verified the algebraic core of the last bullet with a simple deterministic example;
see §7.1.

---

## 6. Candidate proof strategies

The strategies listed in `offline-pair-bridge-plan.md` / `campaign-2.md` are:

1. **Positive-type / band-limited Bochner strategy.**  Use the fact that the overlap
   kernel is positive definite (Bochner's theorem) and band-limited.  One would try to prove
   a Szegő-type **anti-crowding** bound controlling eigenvalues of Gram matrices of
   translates of such a kernel near the `k₂` kink at eigenvalue `2`.
2. **Szegő-type anti-crowding near the k₂ kink.**  The kink is where `Ψ` changes from
   quadratic `(t−1)²` to linear `2t−3`.  An anti-crowding bound would say that for an
   actual kernel Gram matrix one cannot have too many eigenvalues pinned at `2` in the
   way that arbitrary PSD matrices can.
3. **Kink-regularized / taxed defect variant.**  Modify the defect function (for example,
   add a tax on eigenvalues crossing the kink) so that the multi-pair composition becomes
   tractable, then account for the tax in the assembly.

All three strategies are **SPECULATION** until a proof exists.  They are not supported by
a completed argument in any source read for this report.

---

## 7. New observations and small verified numerical experiments

All computations below were run in the repository with Python/NumPy in this session.  They
are small-dial probes, not proofs.

### 7.1 Concrete failure of abstract PSD composition (VERIFIED)

Take the two unit-diagonal PSD matrices

```
A = [[1, 1], [1, 1]],    B = [[1, −1], [−1, 1]].
```

Then

- `spec(A) = {0, 2}` and `spec(B) = {0, 2}`,
- `Ψ(0) = 1`, `Ψ(2) = 1`, so `Δ(A) = Δ(B) = 2`,
- `A + B = 2I`, so `spec(A+B) = {2, 2}` and `Δ(A+B) = 2`,
- `Δ(A+B) − Δ(A) − Δ(B) = −2 < 0`.

Thus the defect is **not superadditive** over arbitrary PSD blocks.  This is exactly the
mechanism described in the upstream refutation: the two individual blocks each have an
eigenvalue at the kink `2`, and summing the blocks crowds both eigenvalues at `2`,
losing defect.  **VERIFIED** by exact algebra; the numeric output is deterministic.

### 7.2 Positive-type kernel probes: no observed violation for actual translates (EVIDENCE)

The previous example uses arbitrary PSD matrices.  To test whether the **positive-type /
band-limited** structure is the right extra hypothesis, I probed actual Gram matrices of
translates of the Montgomery–Taylor kernel

```
k(x) = K(x)/K(0),   K(x) = ∫_{-1/2}^{1/2} cos(√2 t) cos(2π x t) dt.
```

For random point configurations split into two blocks, I searched for

```
Δ(G_full) − Δ(G_block1) − Δ(G_block2) < 0,
```

with `G_ij = k(|x_i − x_j|)` and `G_block` the corresponding sub-blocks.

- Sizes `(2+2), (2+3), (3+3), (4+4)`; `200,000` random configurations per size.
- **No negative value was found.**  The minimum observed difference in every batch was
  `0.0` (to numerical precision), while positive superadditive differences were common.
- For comparison, arbitrary unit-diagonal PSD matrices of the same sizes produced
  strongly negative differences in the same probes.

This is only **EVIDENCE**, not a proof.  It is a small numerical hint that the actual
kernel Gram matrices may satisfy the superadditivity property that arbitrary PSD matrices
do not.  It does not address off-line pair blocks directly, and it does not prove the
multi-pair composition lemma.

### 7.3 Positive-definiteness alone does not prevent spectral crowding (VERIFIED)

For the same Montgomery–Taylor kernel, three points placed at `x = 0, 0.01, 0.02` produce
a Gram matrix with maximum eigenvalue `≈ 2.9994`.  Coincident or near-coincident points
therefore give Gram matrices with eigenvalues well above the kink `2`.

Consequence: a naive “positive-definite kernels cannot crowd eigenvalues above 2” statement
is **false**.  A Szegő-type anti-crowding bound, if it exists, must use more than
positive-definiteness of the kernel alone (for example, the actual arithmetic/analytic
structure of the zeros, or a different spectral dual).  This is a **caveat** on the
positive-type/Bochner candidate strategy.

### 7.4 Balanced-word pair-energy check (EVIDENCE)

I implemented the balanced word from `campaign-2.md`

```
g_i = 1 + ⌊(i+1)·327/673⌋ − ⌊i·327/673⌋,  i = 1,…,673,
```

which sums to `1000` (so `P = 673` points on normalized length `L = 1000`).

For the Montgomery–Taylor kernel-square `w = (K/K(0))²`, the raw sum over unordered pairs
is

```
Σ_{i<j} w(y_j−y_i) ≈ 1.07060   (MT kernel),
Σ_{i<j} w(y_j−y_i) ≈ 1.07155   (optimized seven-term window).
```

These numbers do **not** match the campaign's quoted `e_full < 0.003523506664` with the
normalization I guessed.  I did not have the campaign's exact scaling convention, so I am
**not** claiming a reproduction or contradiction.  This check is recorded as a minor
reproduction caveat: the exact definition of `e_full` and the normalization used for the
`0.674826` ceiling are not fully pinned in the copied sources.

---

## 8. Reduction and exact gap

### 8.1 A useful reduction (candidate, EVIDENCE)

Let `G` be an actual Gram matrix of translates of the normalized band-limited kernel `k`,
and let `G₁, G₂` be principal sub-blocks corresponding to two disjoint groups.  If the
superadditivity

```
Δ(G) ≥ Δ(G₁) + Δ(G₂)          (∗)
```

held for all such actual kernel Gram matrices, then the multi-pair composition lemma
would reduce to:

1. Prove a local one-pair bridge (already reported as done),
2. apply (∗) to all off-line pair blocks in a block-wise decomposition,
3. add the per-pair residuals.

The refuted abstract PSD version shows (∗) is **not** a consequence of positivity alone.
The only new evidence here is that I could not find a counterexample to (∗) for actual
Kernel Gram matrices in small random probes.  **This is not a proof.**

### 8.2 The exact gap

The remaining mathematical obligation can be stated as:

> Prove or refute the superadditivity / multi-pair composition statement for Gram
> matrices of translates of a positive-definite band-limited overlap kernel, with the
> measured local bridge constants, at the level of the full zero-side matrix including
> signature-`(1,1)` off-line pair blocks.

No source read in this session contains a proof of that statement.  The strongest available
evidence remains:

- `~10⁵` adversarial configurations survived the virtualized claim (EVIDENCE),
- exact infinite pair-chain limits sustain `0.0101–0.0271` per pair at all depths
  (EVIDENCE),
- no transition dead zone and multiplicity `≥ 3` dodges self-destruct (EVIDENCE),
- abstract PSD composition is refuted (EVIDENCE), but actual-kernel positive-type
  composition is not refuted by the small probes in this session (EVIDENCE).

---

## 9. Explicit next steps

1. **Pin the exact formal statement.**  Obtain the full campaign-2 notes or upstream
   workspace `numerics2/`, `numerics3/` (the copied sources only contain the summary).
   Write a definitional statement of `D_2`, the fully virtualized defect, the pair block
   formulas, and the `ε_pair` constants.  Until then, any formalization is guessing at the
   contract.
2. **Target the superadditivity question** for actual band-limited kernel Gram matrices.
   The concrete PSD counterexample in §7.1 shows the proof must use the kernel's
   positive-type/band-limited structure; the probes in §7.2 are a cheap sanity check.
3. **Try a Szegő-type anti-crowding theorem** with the correct hypotheses.  The probe in
   §7.3 warns that this cannot be merely “positive definiteness prevents crowding”; it
   must use additional structure.
4. **Try the kink-regularized/taxed-defect variant** in a small Linear Programming or
   interval-arithmetic setting.  A certified finite certificate for a two-pair envelope
   would be a major step, even before a general theorem.
5. **Run a rigorous search for counterexamples to actual-kernel superadditivity.**
   Use interval arithmetic (via `python-flint`/Arb) on a parameterized family of
   configurations, rather than random floating point, to convert the evidence in §7.2 into
   a certified finite result (or to find a counterexample).
6. **If the local composition lemma is proved, assemble the global bound** using the
   existing `tr Ψ(M)` framework and the measured constants, then consider a Lean
   formalization in the style of `zeta-zeros-npip/lean/Zeta23Ext/`.

---

## 10. Summary / verdict

- **Plausible path?**  Yes, but unproven.  The off-line pair bridge is the right
  high-payoff direction: the bandwidth-one extremal law has `≈31.8%` mark-2 mass, and the
  current methods price none of it.
- **Blocker:**  The single open lemma (multi-pair composition for off-line pair blocks)
  is not proved.  The only known attempt at a general proof (abstract PSD composition) is
  **refuted** by exact counterexamples.  A candidate route remains available through the
  kernel's positive-type/band-limited structure, but this session found no proof and no
  refutation of that route.
- **New contribution:** a concrete deterministic demonstration of the PSD composition
  failure (§7.1), a small numerical sanity check that actual kernel Gram matrices may not
  suffer the same failure (§7.2), and a warning that positive-definiteness alone does not
  prevent spectral crowding above the kink (§7.3).
- **No new bound is claimed.**
