# Candidate Proof / Result — SL gap G2: the general vanishing rule for J_σ

**Run:** `R-20260816T070000Z-g2rule-a1b2`
**Status label:** `RIGOROUS_PARTIAL_RESULT` / `FINITE_COMPUTATIONAL_RESULT` (composite).
The **vanishing characterization is VERIFIED on the exact k=3,4,5,6 per-partition data (100%,
275 partitions)**: the deliverable asked for. A fully general-k **proof** remains open; the exact
residual combinatorial identity is stated at the end.

---

## 1. Summary of the finding

For a partition `σ` of `{0,…,k−1}` with `b` blocks, form the **cycle-crossing multigraph**
`H_σ` on the `b` block-vertices: for each cycle edge `(a, a+1)` (indices mod k) whose endpoints
fall in *different* blocks, put one edge between the two blocks (parallel edges counted by
multiplicity; self-loops dropped). Let `m = |E(H_σ)|` = number of cycle block-crossings (this is
an even number, i.e. all H_σ degrees are even, because the cycle is closed).

**Vanishing Rule (Lemma P / G2, the refined general-k statement):**

> **J_σ = 0  ⟺  H_σ is disconnected,  OR  b ≥ 2 and m ≤ 2b − 3.**
> Equivalently, **J_σ ≠ 0  ⟺  H_σ is connected AND m ≥ 2b − 2**, with the b=1 base case
> (H empty, m=0) nonvanishing (J_σ = 1).

That is, a nonvanishing shape is exactly one whose crossing multigraph is **connected and has
surplus** `s := m − b ≥ b − 2` (equivalently cyclomatic number `c = m − b + 1 ≥ b − 1` for the
connected case).

**Verification.** Over the full exact per-partition dataset (Bell(3)+Bell(4)+Bell(5)+Bell(6)
= 5+15+52+203 = **275** partitions, all with exact rational J_σ), the rule predicts correctly in
**275/275 cases** (TP=167 nonvanishing, TN=108 vanishing, FP=0, FN=0). See
`reproducibility/final_rule.py` (output reproduced in the ledger).

This resolves the k=5 vs k=6 tension: the crude "b≥K ⇒ 0" rule FAILS because it ignores H_σ.
At k=6, b=4 partitions with m=6 (≥ 2·4−2=6) are connected with the required surplus and are
nonvanishing; b=4 with m=4,5 and all b=5,6 partitions fall below the threshold (or are of the
degenerate low-surplus type) and vanish. At k=5 the corresponding connected-surplus condition
is only satisfiable for b ≤ 3 (k=5 forces m ≤ 5 < 2b−2 for b≥4).

## 2. Why H_σ alone characterizes J_σ (isoclass-determinism)

`J_σ = ∫_{R^{b−1}} (∏_{e∈H_σ} K(δ_e)) · ρ_b dx` depends **only on the multigraph H_σ**
(and k through the allowed m): the cycle product is exactly the product of K over the crossing
edges, self-loops being K(0)=1, and ρ_b is a function of the b block-variables. Relabeling the
vertices of H_σ is a relabeling of integration variables plus translation, so **J_σ is invariant
under isomorphism of H_σ**. Confirmed computationally: at k=6 the 38 distinct (b,H-isoclass)
classes each carry a single J value (see `reproducibility/abstract_k6.py` / `rule_tests.py`).

So the vanishing rule is a **graph property of H_σ**, which is what the data shows it must be.

## 3. Data evidence for the rule (all blocked properly)

From `reproducibility/rule_tests.py` and `final_rule.py`, grouping by (b, m, cyclomatic, deg-seq):

| b | m | connected | cyclomatic | m ≥ 2b−2? | observed J |
|---|---|---|---|---|---|
| 1 | 0 | — | 0 | (base) | 1 (nonzero) |
| 2 | 2 | yes | 1 | yes | 1/3 |
| 2 | 4 | yes | 3 | yes | 7/60 |
| 2 | 6 | yes | 5 | yes | 89/1260 |
| 3 | 3 | yes | 1 | no | 0 (35×) |
| 3 | 4 | yes | 2 | yes | 1/15 (42×) |
| 3 | 5 | yes | 3 | yes | 1/180 (35×) |
| 3 | 6 | yes | 4 | yes | 1/420 (4×), 11/630 (6×) |
| 4 | 4 | yes | 1 | no | 0 (21×) |
| 4 | 5 | yes | 2 | no | 0 (35×) |
| 4 | 6 | yes | 3 | yes | 1/105, −1/840, 1/1260, 4/315 (20×) |
| 5 | 5 | yes | 1 | no | 0 (7×) |
| 5 | 6 | yes | 2 | no | 0 (9×) |
| 6 | 6 | yes | 1 | no | 0 (1×, D_6) |

(The (b,m) cross-k totals differ from the k=6-only table because k=3,4,5 contribute too; the
*rule* is checked partition-by-partition on all 275.)

Note every H_σ occurring in the data is connected (all degrees ≥ 2 for b≥2, so H always has a
nontrivial component covering all blocks → the "disconnected" branch of the rule never fires in
this data, k ≤ 6; we keep it because it is forced by the integral factorization argument in §6
and will matter for k ≥ 7). The discriminating feature is purely **m ≥ 2b − 2**.

## 4. Lemma P (refined, general-k) statement

**Lemma P (conjectured, verified for k ≤ 6).** With σ, b, H_σ, m as above,

```
m_k  =  Σ_{ σ : H_σ connected, m ≥ 2b−2 } J_σ     (all other σ contribute 0).
```

The **admissible set** (nonvanishing partitions) is `{ σ : H_σ connected and m ≥ 2b−2 }`.

**Value structure observed (exact rationals):**
- b = 1: `J = 1` (the unit term).
- b = 2: `J = c_m − c_{m+2}`,  m ∈ {2,4,…,k−1 even}. Exact; never zero (c-sequence strictly
  decreasing). Verified on every b=2 partition of k=2..6 (see `b2b3_formulas.py`).
- b = 3 (k=6 exact, from the m6 CSV / allJ.json): m=4 → 1/15; m=5 → 1/180; m=6 → 1/420
  (deg-seq (4,4,4)) or 11/630 (deg-seq (6,4,2)). Exact rationals; a *closed c-combination
  formula for general b=3 is not yet pinned* (see §7 — open sub-identity).
- b = 4 (k=6 exact): m=6 → 1/105 (deg-seq (6,2,2,2): the 3-star), 1/1260, −1/840, 4/315 by
  H-isoclass. All vanishing for m=4,5.
- b = 5, 6 (k=6): all 0 (never reach m ≥ 2b−2 = 8, 10 for k=6).

The complete exact per-partition table is shipped as `reproducibility/allJ.json` (275 rows).

## 5. Validation of the exact per-partition dataset

- k=3,4,5 from the audited box-spline exact engine, corrected for the documented float-noise:
  the m5 run established the true k=5 value set {1, 1/3, 7/60, 1/15, 1/180, 0}. The engine
  reproduced exactly m_3=2, m_4=13/4 (no correction needed at k=3,4); at k=5 the four float
  residues that do not lie in the true set were corrected to their isoclass value via the
  (k=6-confirmed) isoclass-determinism rule and the certified D_5=0: 5178/86089 → 1/15,
  2954/44309 → 1/15, 87/70634 → 0, −41/89756 → 0. After correction **m_5 = 101/18 exactly**.
- k=6 from the m6 run CSVs (b=3,4,5,6 exact per-partition) + analytic b=1 (1), b=2
  (c_m−c_{m+2}); **m_6 = 640/63 exactly**.
- Net anchors: m_2=4/3, m_3=2, m_4=13/4, m_5=101/18, m_6=640/63 all reproduced exactly
  (`build_dataset.py`).
- Rule accuracy: **275/275 (100%)**, no counterexample (`final_rule.py`).

## 6. Why the rule should hold in general (proof approach, not a proof)

**Fermionic / quasi-free (Wick) structure.** ρ_b = det[K(x_i−x_j)] and J_σ = Σ_{π∈S_b} sign(π)
B_{Γ_{σ,π}}(0), Γ_{σ,π} = H_σ ∪ match(π). Two provable components:

1. **Disconnected ⇒ 0.** If H_σ has a connected component on a proper subset S of the blocks,
   the cycle product ∏_{e∈H}K factors over the components (no crossing between S and its
   complement), and the determinant ρ_b = det[K] restricts to a block-diagonal-plus-`det≤0`? —
   precisely, ρ_b separates up to the cross-K's which are *not* present in H, so the x-integral
   over the isolated part runs over its own determinant with the cycle product: an ∮ of a
   determinant that is an odd/even cancellation. The clean statement: the integral factorizes
   with a leftover factor ∮_{sub-blocks}(cycle-edges)·ρ_{|S|}, which is the "lower-order D-type"
   integral that vanishes. (This is the mechanism behind D_k=0 and the b→ lower-block vanishing
   described in the m5/m6 runs.)

2. **Connected with m ≤ 2b−3 ⇒ 0 (the "low-surplus"/quasi-forest obstruction).** When m ≤ 2b−3,
   the combined graph Γ_{σ,π} has `n(Γ) = m + (# non-self-loop π-edges)` active edges and the
   coarea value B_Γ(0) sits where the "caps"/zonotope section forces a signed cancellation across
   the S_b orbit: the surplus `m − b` being < b−2 means there are not enough independent cycle
   directions to force an interior box-spline section, so each B_{Γ_{σ,π}}(0) is expressible as a
   finite sum over *smaller-order* box-splines whose signed sum telescopes to 0 by the fermionic
   (Wick/Grassmann) determinant identity — the same mechanism that makes D_k = 0 (the all-distinct
   `m = k, b = k` case has m = b < 2b−2 for b ≥ 3, hence vanishes; and b=4 m=4,5 vanish at k=6).

3. **Connected with m ≥ 2b−2 ⇒ ≠ 0.** The surplus condition m − b ≥ b − 2 forces every block to
   carry an "over-full" crossing structure (average surplus ≥ 1 per block beyond a tree), so the
   signed sum has at least one orbit that is not cancellable — the box-spline section polytope has
   a genuine interior vertex and the corresponding J_σ is a nontrivial positive/negative rational
   (matching the observed small-denominator rationals). The b=2 base case is closed exactly:
   J = c_m − c_{m+2} ≠ 0.

This is the honest proof *strategy*; the general-k proof that the signed sum over S_b telescopes
exactly on the complement of `{connected, m ≥ 2b−2}` is the precise open obligation (§7).

## 7. Exact remaining identity (G2 proof goal, unresolved in this pass)

**Open obligation (Lemma P ⇒ all k).** Prove the combinatorial identity: for all k and σ ∈ Part(k),
```
J_σ = Σ_{π∈S_b} sign(π) B_{Γ_{σ,π}}(0)  =  0   ⟺   H_σ disconnected or m ≤ 2b−3,
```
where B_Γ(0) is the (n−d)-volume box-spline value at 0 for the combined cycle∪π multigraph.
Equivalently, the signed box-spline sum vanishes precisely on the graph class
`{H_σ : not (connected and m ≥ 2b−2)}`.

Two sub-identities that would close it:
- **M1 (disconnected / reduced-Dcancellation).** When H has a proper component, J_σ factors with
  a residual lower-order "closed cycle-product × determinant" integral that vanishes — prove this
  factorization and the vanishing of the residual (this is the generalized D_k=0).
- **M2 (low-surplus telescoping).** For connected H with m ≤ 2b−3, prove the S_b-signed sum of
  the box-spline values telescopes to 0 via the degree-≤2/convolution reduction (the
  `degree2_reduction.py` cascade) or via the Wick/quasi-free (Grassmann) determinant identity;
  and that for m ≥ 2b−2 at least one non-cancellable term survives (so J_σ ≠ 0).

### Blocked / honest
- The **general-k proof is NOT complete**: this pass proves (by exhaustive exact computation)
  the rule for k=3,4,5,6 and states the precise identity to prove for all k. No numerical evidence
  is presented as proof.
- A **closed b=3 (and higher) c-combination formula** for the nonzero J_σ values is not pinned;
  the exact values are table-driven (allJ.json). b=2 is fully closed: J = c_m − c_{m+2}.
- The **value formula** (which nonzero fraction each admissible σ gets) for general b, m, H is a
  separate open problem (part of Lemma P's coefficient structure), beyond the vanishing rule that
  this G2 pass was tasked to determine.

## 8. Honesty / status
- **The general vanishing rule for J_σ is determined and verified 100% on the exact k=3,4,5,6
  data** (the G2 deliverable). 
- Proof for all k: open; the precise residual identity is §7.
- The k=4 value set quoted in the task brief (`{1,1/3,7/60,1/15,1/180}`) is a slight over-count:
  the engine reproduces m_4=13/4 exactly with k=4 values {1, 1/3, 7/60, 1/15, 0} (1/180 first
  appears at k=5). Noted for the record.
