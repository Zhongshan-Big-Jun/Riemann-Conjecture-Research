# Problem Contract — SL gap G2: general vanishing rule for J_σ (Lemma P coefficient structure)

- **Run ID:** `R-20260816T070000Z-g2rule-a1b2`
- **Task packet:** SL gap G2 (bounded combinatorial-analysis pass): determine the GENERAL
  vanishing rule for the shape integrals J_σ (the Lemma P coefficient structure) from the exact
  k=5 and k=6 data.
- **Project root:** `F:\LaTeX\Riemann Conjecture`
- **Skill:** rigorous-open-math-research (solver, bounded pass)

## Normalized statement

Let `Part(k)` be the set-partitions of `{0,…,k−1}`, `b = #blocks(σ)`, `ρ_b = det[K(x_i−x_j)]`
with `K = sinc`, and

```
m_k = Σ_{σ∈Part(k)} J_σ
J_σ = ∫_{R^{b−1}} [∏_{a=0}^{k−1} K(x_{σ(a)}−x_{σ(a+1)})] · ρ_b dx,   x_b pinned (translation)
```

(cycle edges; an edge whose endpoints lie in the same block is a self-loop contributing K(0)=1).
`J_σ = Σ_{π∈S_b} sign(π) B_{Γ_{σ,π}}(0)`, a signed sum of box-spline values at 0 where `Γ_{σ,π}`
is the combined multigraph (cycle edges ∪ permutation edges) on the b blocks.

**Completion criterion (G2):** find a structural characterization, in terms of the partition σ
(equivalently its cycle-crossing multigraph H_σ), of **which σ have J_σ = 0**, that
- reproduces 100% of the exact per-partition data at k=3,4,5,6 (275 partitions total);
- explains the sharp difference between k=5 (b≥4 ⇒ 0) and k=6 (b=4 nonzero, b=5,6 vanish);
- is stated as a precise Lemma P / G2 statement (admissible set + J_σ value structure) and, if
  not provable in this bounded pass, reports the exact remaining combinatorial identity to prove.

## Exact input data (from upstream audited runs)

- k=3: D_3 = 0 (certified G1); m_3 = 2.
- k=4: D_4 = 0 (certified G1); nonzero values {1, 1/3, 7/60, 1/15}; m_4 = 13/4.
- k=5 (run R-20260816T050000Z-m5exact-3f8a): m_5 = 101/18; nonzero multiplicity set
  1(×1), 1/3(×10), 7/60(×5), 1/15(×10), 1/180(×5); 21 zero partitions; D_5 = 0 (certified G1).
- k=6 (run R-20260816T060000Z-m6exact-4f9a): m_6 = 640/63; per-block b:
  b=1: 1; b=2: 4297/630 (J=c_m−c_{m+2}, m even crossings); b=3: 479/210 {0,1/15,1/180,11/630,1/420};
  b=4: 2/35 {0,1/105,−1/840,1/1260,4/315}; b=5: 0; b=6 (D_6): 0.
- c-values: c_2=1, c_4=2/3, c_6=11/20, c_8=151/315, c_10=15619/36288, c_12=655177/1663200.

## Completion status (this pass)

| Requirement | Status |
|---|---|
| General vanishing characterization | **FOUND and 100%-validated on k=3..6 (275 partitions)** |
| Accuracy report on all exact data | 100% (TP=167, TN=108, FP=0, FN=0) |
| General-k proof (all k) | NOT closed in this bounded pass; exact residual identity stated |
| b=2 closed form J=c_m−c_{m+2} | Confirmed (exact, matches all b=2 data) |
