# Lemma P (k=6) coefficient structure — run R-20260816T060000Z-m6exact-4f9a

For the shape decomposition `m_k = Σ_{σ∈Part(k)} J_σ`, the k=6 per-partition values J_σ (exact):

## Nonzero J_σ values and multiplicities (by #blocks / block-size profile)

| #blocks b | block-size profile | #partitions | per-partition values (value × count) | profile sum |
|---|---|---|---|---|
| 1 | (6) | 1 | 1 × 1 | 1 |
| 2 | various | 31 | 1/3 × 15, 7/60 × 15, 89/1260 × 1 | 4297/630 |
| 3 | (1,1,4) | 15 | 0 × 6, 1/15 × 9 | 3/5 |
| 3 | (1,2,3) | 60 | 0 × 12, 1/180 × 24, 11/630 × 6, 1/15 × 18 | 151/105 |
| 3 | (2,2,2) | 15 | 0 × 2, 1/420 × 4, 1/180 × 6, 1/15 × 3 | 17/70 |
| 4 | (1,1,1,3) | 20 | 0 × 18, 1/105 × 2 | 2/105 |
| 4 | (1,1,2,2) | 45 | 0 × 27, −1/840 × 6, 1/1260 × 9, 4/315 × 3 | 4/105 |
| 5 | (1,1,1,1,2) | 15 | 0 × 15 | 0 |
| 6 | (1,1,1,1,1,1) | 1 | 0 × 1 (D_6) | 0 |

m_6 = Σ = 640/63. Distinct nonzero rationals: 1, 1/3, 7/60, 89/1260, 1/15, 1/180, 11/630, 1/420,
1/105, −1/840, 1/1260, 4/315.

## Which shapes vanish
- b=5 (all 15, profile (1,1,1,1,2)) and b=6 (D_6) vanish entirely.
- b=4: 45 of 65 vanish; the nonzero ones are the block-size-3 (1,1,1,3) with value 1/105 (2 of 20)
  and (1,1,2,2) values −1/840, 1/1260, 4/315.
- b=3: 20 of 90 vanish (so even at b=3 not every shape contributes).

## Refined general-k conjecture (from k=5 and k=6 data)
- For k=5, only b≤3 contributed (b≥4 vanished); for k=6, b=4 also contributes (b=5,b=6 vanish).
  So the crude "b≥K ⇒ vanish" is a *per-k* threshold, not a universal one. For k=6 it is b≥5 ⇒ 0
  (the order given by the m_5 reduction-to-D_k mechanism continues: small blocks/large-#blocks
  arrangements that contract to lower-order D-type cyclic integrals vanish, while the "first
  non-vanishing" nontrivial b block sizes contribute).
- Structure: J_σ vanishes when the partition's cycle reduces (by fusing the singleton/2-blocks) to a
  D-type integral of lower degree that vanishes. The nonzero J_σ are small rationals whose
  denominators factor into small primes and 7 (e.g. 1/420, 1/1260, 11/630, 89/1260).
- Precise general statement is OPEN (Lemma P / G2): a conjectured rule is that the contributing
  shapes are exactly those with #blocks ≤ (k − the largest block size), with values expressible as
  differences of c-constants and small-rational box-spline values; k=6 data is the evidence.
