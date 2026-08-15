# Whiteboard — R-20260816T060000Z-m6exact-4f9a

- **Run ID:** `R-20260816T060000Z-m6exact-4f9a`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5`
- **Last updated:** `2026-08-16T07:30:00Z`

## Current plan

RUN COMPLETE (2026-08-16): FINITE_COMPUTATIONAL_RESULT (exact m_6) / RIGOROUS_PARTIAL_RESULT
(Hankel fork). Deliverable: m_6 = 640/63 exact (all 203 set partitions) + Λ_3(0) = 247/2519
exact; the Hankel decay-vs-plateau fork is DECIDED = DECAY (Λ_3 < Λ_2 = 5/36; the plateau
estimate 0.149 is mathematically impossible by positivity). Next steps (not part of this
run): exact m_7, m_8 for Λ_4; the general-k vanishing/coefficient structure (Lemma P/G2);
then G3 (Lemma H) toward SL.

## Route history

- c_12 = 655177/1663200 exact (box-convolution formula + mpmath cross-check, diff < 1e-17)
  `[SUCCEEDED]`.
- b=2 analytic reduction J = c_m − c_{m+2} (m ∈ {2,4,6}: 1/3, 7/60, 89/1260), verified on all
  31 b=2 partitions `[SUCCEEDED]`.
- b=3: all 90 partitions via the sympy exact engine; values {0, 1/15, 1/180, 11/630, 1/420}
  `[SUCCEEDED]`.
- b=4: all 65 via the fast-exact engine (numpy vertex-finding on exact integer null basis +
  scipy hull, ~10^3× faster), validated per-term vs the sympy engine on a nonzero b=4
  partition and ~1e-13 on b=2/3; values {0, 1/105, −1/840, 1/1260, 4/315} `[SUCCEEDED]`.
- b=5 (all 15) = 0; D_6 (all-distinct) = 0 `[SUCCEEDED]` (consistent with certified D_3..D_5 = 0).
- m_6 = 640/63 assembly + positivity anchor (det H_0..H_3 > 0) `[SUCCEEDED]`.
- Hankel fork: Λ_1 = 1/4, Λ_2 = 5/36, Λ_3 = 247/2519 exact; structural proof
  Λ_3(m_6) < 5/36 for every valid m_6 ⇒ **DECAY** `[SUCCEEDED]`.
- k=5 rule "b ≥ 4 ⇒ 0" tested at k=6 `[FAILED → corrected]`: b=4 contributes +2/35
  (required for positivity); the vanishing rule is partition-structure-dependent.
- Λ_4 with sampler m_7, m_8 `[PARTIAL]`: ≈0.18 but unreliable (finite-L/h-bias); exact
  m_7, m_8 needed.

## Ideas to return to

- Bell(7)=877 / Bell(8)=4140 partitions for exact m_7, m_8 (heavy but the fast-exact engine
  makes it feasible) → exact Λ_4 and the decay curve.
- The refined vanishing conjecture: which partition structures vanish at each k (b=5,6
  vanish at k=6; b=4 nonzero) — seek a structural rule (crossing structure / block sizes).
- The Λ_3(m_6) monotonicity trick (affine in m_6) may generalize: Λ_m as a function of the
  top moment — a positivity-based bound route toward Λ_m → 0.

## Open obligations

- Exact m_7, m_8 (⇒ exact Λ_4 and the decay curve).
- General-k coefficient/vanishing structure (Lemma P/G2): k=6 shows b=4 nonzero — the
  conjecture is refined, not closed.
- Full sympy re-verification of all 65 b=4 shapes (residual audit item; fast-engine
  cross-check already =0.0 diff on a nonzero b=4 partition and exact on b=2/3).
- G3 (Lemma H: Λ_m(0) → 0) + SL itself + the unconditional liminf → 1 remain OPEN.

## Key artifacts

- `runs/.../m6exact-4f9a/candidate_proof.md` — full decomposition table + Λ_3 structural proof.
- `runs/.../m6exact-4f9a/lemmaP_k6.md` — Lemma P (k=6) coefficient structure.
- `runs/.../m6exact-4f9a/reproducibility/` — boxspline_exact2.py (sympy exact),
  boxspline_exact_fast.py (fast exact), batch_exact6.py/fast_batch6.py (parallel),
  reduce_b2.py (b=2 analytic), assemble_b3.py (assembly), validate_b4_fast.py
  (fast-vs-true-exact), b3_batch*.csv, b4_fast_c*.csv, b5_fast.csv, b6_fast.csv,
  master_summary6.py (reproduce m_6 = 640/63, Λ_3 = 247/2519).
- `runs/.../m6exact-4f9a/SHA256SUMS` (42 entries).
