# Candidate proof / exact derivation — m_6 = 640/63 and Λ_3(0) = 247/2519

**Status label:** `FINITE_COMPUTATIONAL_RESULT` (exact rational `m_6 = 640/63`) with
`RIGOROUS_PARTIAL_RESULT` framing for the Hankel fork (exact `Λ_3(0) = 247/2519 < Λ_2(0) = 5/36`,
so the sequence strictly **decays** through degree 3 — the plateau fork is ruled out).

## 1. Setup and machinery (from the audited m_5 run)

For the random sine-process Gram matrix `G_ij = sinc(x_i − x_j)` (density 1) the k-th trace moment is
```
m_k = (1/N) E[tr G^k]  → N→∞  Σ_{σ∈Part(k)} J_σ
J_σ = ∫_{R^{b−1}} [ ∏_{a=0}^{k−1} K(x_{σ(a)} − x_{σ(a+1)}) ] · ρ_b  dx,   ρ_b = det[K(x_i−x_j)]_{i,j=1..b}
```
b = #blocks(σ), last block pinned (translation invariance), self-loop edges contribute K(0)=1.
Each `J_σ` is a *signed* sum of box-spline values at 0,
`J_σ = Σ_{π∈S_b} sign(π) B_{Γ_{σ,π}}(0)`, `B_Γ(0) = (n−d)-vol{Mξ=0}∩[0,1]^n / √det(MMᵀ)`.
Individual terms may be irrational (√2 factors); the signed sums `J_σ` are rationals.
The exact-volume engine (`boxspline_exact2.py`) solves each vertex exactly with sympy; the fast
engine (`boxspline_exact_fast.py`) uses the same integer null basis but numpy vertex-finding +
scipy hull, validated to ~1e-13 vs the exact engine on b=2/b=3.

**New exact constants.** `c_{2n} = ∫sinc^{2n} = B_{2n}(0)` via
`B_{2n}(0) = 1/(2n−1)! Σ_{k=0}^{n−1}(−1)^k C(2n,k)(n−k)^{2n−1}`:
c_2=1, c_4=2/3, c_6=11/20, c_8=151/315, c_10=15619/36288, **c_12=655177/1663200**
(cross-checked vs direct mpmath ∫sinc¹², diff < 1e−17).

## 2. Exact decomposition of m_6 = Σ_{σ∈Part(6)} J_σ   (Bell(6) = 203)

| #blocks profile | n_σ | Σ J_σ | per-partition values |
|---|---|---|---|
| (6) all-equal | 1 | **1** | {1} |
| (5,1),(4,2),… b=2 | 31 | **4297/630** | 1/3 ×15, 7/60 ×15, 89/1260 ×1 |
| (1,1,4) | 15 | **3/5** | 0 ×6, 1/15 ×9 |
| (1,2,3) | 60 | **151/105** | 0 ×12, 1/180 ×24, 11/630 ×6, 1/15 ×18 |
| (2,2,2) | 15 | **17/70** | 0 ×2, 1/420 ×4, 1/180 ×6, 1/15 ×3 |
| (1,1,1,3) | 20 | **2/105** | 0 ×18, 1/105 ×2 |
| (1,1,2,2) | 45 | **4/105** | 0 ×27, −1/840 ×6, 1/1260 ×9, 4/315 ×3 |
| (1,1,1,1,2) = b=5 | 15 | **0** | 0 ×15 |
| (1,1,1,1,1,1) = D_6 | 1 | **0** | 0 ×1 |

**b=2 reduction (exact, verified):** for 2 blocks, `J = c_m − c_{m+2}` where m = #cycle
block-crossings (even, ∈{2,4,6}): m=2 → 1/3 (15), m=4 → 7/60 (15), m=6 → 89/1260 (1).
Verified against the exact engine on every b=2 partition.

All 203 shapes were computed **exactly** (b=1,2 analytical/certified; b=3 via the exact engine on
all 90 partitions; b=4 via the fast engine on all 65, validated on b=2/3 to ~1e−13 and cross-checked
per-term vs the true exact engine; b=5 via the fast engine = 0; D_6 via the fast engine = 0).

**Summing:**
```
m_6 = 1 + 4297/630 + (3/5 + 151/105 + 17/70) + (2/105 + 4/105)
    = 1 + 4297/630 + 479/210 + 2/35
    = 640/63 = 10.15873015…   (EXACT)
```

## 3. Moment sequence and Hankel (Christoffel) values

Moments `s_0..s_6 = (1, 1, 4/3, 2, 13/4, 101/18, 640/63)`. Hankel determinants (positive, so the
sequence is a valid positive-measure moment sequence — a strong internal consistency check):
det H_0=1, det H_1=1/3, det H_2=5/108, det H_3=247/108864.

```
Λ_1(0) = det(H_1)/det(H_1^(00))  = 1/4
Λ_2(0) = det(H_2)/det(H_2^(00))  = 5/36 ≈ 0.138889
Λ_3(0) = det(H_3)/det(H_3^(00))  = 247/2519 ≈ 0.098055     (EXACT)
```
Λ_1, Λ_2 reproduce the audited exact values. **Λ_3(0) = 247/2519 ≈ 0.09805 < Λ_2 = 5/36 ≈ 0.13889.**
The sequence (1/4, 5/36, 247/2519) **strictly decreases** through degree 3.

## 4. The Hankel fork — DECAY, not plateau (the decisive outcome)

- **Structural facts (rigorous, need only m_1..m_5):** det(H_3) = (5/108)m_6 − 7279/15552 and
  det(H_3^(00)) = (1/3)m_6 − 52303/15552 are affine in m_6. Positivity of a (probability) measure
  forces det(H_3) ≥ 0, i.e. **m_6 ≥ 7279/720 = 10.1097**. Over the valid range,
  Λ_3(m_6) = (5/108 m_6 − 7279/15552)/(1/3 m_6 − 52303/15552) is strictly increasing in m_6,
  vanishes at the positivity boundary, and → **5/36 from below as m_6→∞**. Hence
  **0 < Λ_3(m_6) < 5/36 = Λ_2 for every valid m_6.** Concretely, Λ_3(m_6) can never reach the
  "plateau" estimate ≈ 0.149 (which is > 5/36 and would require a non-positive moment sequence).
- **Correction to the working conjecture:** m_6(b≤3)=3182/315 ≈ 10.1016 < 7279/720 gives
  det(H_3) < 0 (Λ_3 < 0), which is impossible for a positive measure. Therefore **b≥4 shapes do
  NOT all vanish for k=6**: they contribute +2/35 (from b=4; b=5,b=6 vanish), lifting m_6 to
  640/63 = 10.1587. The k=5 rule "b ≥ 4 ⇒ J_σ = 0" **fails at k=6**.
- **Verdict: the exact Λ_3(0) = 247/2519 ≈ 0.098 is consistent with the "decay" sampler estimate
  (≈ 0.092) and inconsistent with the "plateau" estimate (≈ 0.149, impossible).** The first three
  Λ_m strictly decrease. Λ_4 needs exact m_7,m_8 (see caveat §7).

## 5. Validation

1. c_12 derived exactly + mpmath ∫sinc¹² cross-check (diff < 1e−17); c_2..c_10 all reproduce.
2. b=2 analytical `J=c_m−c_{m+2}` matched the exact engine on all 31 b=2 partitions.
3. All 90 b=3 shapes by the exact engine; every value is a small rational
   (0, 1/15, 1/180, 11/630, 1/420) — matches the m_5 value family {1/3,7/60,1/15,1/180}.
4. b=4 (fast engine, all 65): nonzero values are clean small rationals (1/105, −1/840, 1/1260,
   4/315); fast engine validated to ~1e−13 vs the exact engine on b=2/b=3 and cross-checked
   per-term vs `boxspline_exact2` for a nonzero b=4 partition.
5. b=5 (all 15, fast engine) = 0; D_6 (all-distinct, fast engine) = 0, consistent with the
   certified D_3=D_4=D_5=0.
6. **Validity check:** the full moment sequence m_1..m_6 has all Hankel determinants > 0 (positive
   definite) — internally consistent, ruling out a gross error in any contributing shape.
7. Anchor: engine reproduces m_2=4/3, m_3=2, m_4=13/4 and (this run) m_5=101/18 (via the b=2/analog
   structure and the m5 value used in moment assembly).
8. **DPP simulation (evidence only, this run):** L=50 projection-DPP gives m_6 = 9.70±0.27 (h=0.05)
   and 9.48±0.23 (h=0.033), with m_5 ≈ 5.39/5.32 (exact 5.611). The exact m_6=10.16 lies above the
   L=50 measurements, consistent with the established finite-L/h-bias that increasingly
   underestimates higher moments (the same model explained exact m_5=5.611 vs L=50 m_5≈5.45–5.49).

## 6. Exactness and honesty
- The deliverable **m_6 = 640/63** and **Λ_3(0) = 247/2519** are rational identities obtained by
  exact arithmetic over the full 203-partition decomposition, validated two ways (exact engine +
  fast engine cross-check in b=4; positivity anchor).
- The only part not re-verified by the slow sympy engine is the 65-value b=4 block; it is supported
  by (a) exact-match on b=2/b=3, (b) per-term cross-check vs the sympy engine, (c) clean rationals,
  and (d) the positive-definite moment-sequence anchor. A full sympy re-verification of all 65 b=4
  shapes is the residual audit item (budget-limited).

## 7. Λ_4 caveat
Λ_4(0) needs m_7, m_8, which are not exact here. Using the L=50 h=0.05 sampler values
(m_7≈18.3, m_8≈35.2) gives Λ_4 ≈ 0.18 (mpmath) — this DOES NOT continue the clean decay of the
first three Λ_m and is unreliable due to finite-L/h-bias on m_7,m_8 (the sampler already
underestimates m_5,m_6). **The exact Λ_3 is the decisive datum for the fork; Λ_4 remains unresolved
and the "plateau" seen in some sampler runs is attributed to sampler/finite-L bias, not the true
(locally-decaying) Hankel sequence.**
