# Whiteboard — R-20260816T050000Z-m5exact-3f8a

- **Run ID:** `R-20260816T050000Z-m5exact-3f8a`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5` (SL moment route)
- **Project:** `F:\LaTeX\Riemann Conjecture`
- **Last updated:** `2026-08-16T07:10:00Z`

## Run ID / Task packet ID
- Run ID: `R-20260816T050000Z-m5exact-3f8a`
- Task packet ID: `Q-20260814-criticalline-p1-507bb5`

## Current plan
Compute the 5th trace moment of the random sine-process Gram matrix **exactly**:
m_5 = (1/N) E[tr G^5], G_ij = sinc(x_i−x_j), via the DPP factorial-moment / set-partition
shape decomposition, with D_5 = 0 (certified) so the all-distinct term vanishes. Then test the
Hankel (Christoffel) decay Λ_m(0) → 0 (the SL criterion) with m_5. Status: **the exact
m_5 = 101/18 = 5.6111… is obtained and validated. RUN COMPLETE (RIGOROUS_PARTIAL_RESULT /
FINITE_COMPUTATIONAL_RESULT).**

## Route history
- Correct shape-integral formula `[SUCCEEDED]`: m_k = Σ_{σ∈Part(k)} J_σ, with
  J_σ = ∫_{R^{b−1}} [Π cycle edges K(x_{σ(a)}−x_{σ(a+1)})]·ρ_b, b = #blocks, ρ_b = det[K].
  (The scaffold `m5_shapes.py` in the G1 run was WRONG: it omitted the ρ_b factor and miscounted.)
  This formula reproduces m_2=4/3, m_3=2, m_4=13/4 EXACTLY (anchor).
- Exact box-spline (coarea) engine `[SUCCEEDED]`: B(0) computed by vertex enumeration of the
  section polytope {Mξ=0}∩[0,1]^n, validated on c_2..c_10 and the certified D3/D4/D5 values.
  A float hull bug (over-coarse dedup → ±1e-3 noise) was found and fixed; an independent
  high-precision engine (`exact_volume.py` Delaunay + exact fraction simplex volumes) cross-
  validates every distinct shape value.
- c_{2n} exact `[SUCCEEDED]`: c_2=1, c_4=2/3, c_6=11/20, c_8=151/315, c_10=15619/36288.
- m_5 exact decomposition `[SUCCEEDED]`: over the 52 partitions, only the b≤3-block profiles
  contribute; m_5 = 1 + 5/3 + 9/4 + 1/3 + 13/36 = **101/18**.
- Vanishing shapes `[SUCCEEDED]/(PARTIAL proof)`: the (1,1,1,2) [b=4] and (1,1,1,1,1) [D_5]
  profiles = 0. (1,1,1,2) verified ≈0 by the hp engine and reduces to D_4-type cancellation;
  D_5=0 is certified from the G1 run. A closed "b≥4 ⇒ J_σ=0" proof for general k is the open
  part of Lemma P/G2.
- Numerical validation `[PARTIAL]`: L=50 DPP simulation gives m_5 ≈ 5.45–5.49 (h=0.02–0.05,
  ±0.08); the task's L=50 h=0.05 reference was 5.4551 with h-bias −0.13±0.08 (⇒ exact ≈ 5.59).
  The exact 101/18=5.6111 is ~1.5–2σ above the raw L=50 small-h measurement; the gap is
  attributed to finite-L (L=50 underestimates) + h-bias corrections. The simulation is
  consistent-with (not conclusively confirming) 5.6111.
- Hankel test `[SUCCEEDED] exact Λ1,Λ2; Λ3,Λ4 unresolved`: Λ_1(0)=1/4, Λ_2(0)=5/36 exactly
  (needs only m_1..m_4). Λ_3,Λ_4 need m_6,m_7,m_8 which are not exact; sampler evidence gives a
  plateau (~0.149, ~0.148) pending higher moments — the SL-relevant decay is NOT yet pinned.
- Lemma P (k=5) coefficient structure `[SUCCEEDED]`: nonzero values and multiplicities recorded
  (see Key artifacts / master_summary.py).

## Ideas to return to
- Compute m_6 EXACTLY (Bell(6)=203 partitions) to pin Λ_3(0) and decide whether Λ_m decays or
  plateaus — the decisive SL test. The engine here generalizes; needs more robust high-precision
  volume for m=7..9 sections (or the exact null-basis volume path fixed/speed-ups).
- Closed proof of "J_σ=0 whenever b ≥ 4" (generalizes D_k=0): the box-spline signed-sum
  identity (Lemma M) extended to the b-block reductions.
- Larger L (L=100+) high-statistics m_5..m_8 to separate finite-L from h-bias.
- The task's "surviving shapes = blocks size ≤ 2" framing is INCORRECT: blocks of size 3 and 4
  do contribute; the vanishing is by #blocks (b ≥ 4), not block size.

## Open obligations
- G2 (Lemma P) general-k proof: the exact coefficient structure of m_k (which partition profiles
  vanish) — closed for k=5 (validated), open in general.
- Decisive SL test needs exact m_6,m_7,m_8 → Λ_3,Λ_4 (decay vs plateau).
- G3 (Lemma H): matching-sum moment sequence ⇒ Λ_m(0)→0 (Szegő–Widom / determinacy) — open.
- SL and the unconditional liminf → 1 remain OPEN.

## Key artifacts
- `reproducibility/m5_final.py` — the exact decomposition table, m_5 = 101/18.
- `reproducibility/master_summary.py` — all deliverable numbers in one script.
- `reproducibility/enumerate_moments.py` — the exact set-partition enumeration (anchored m_2..m_4).
- `reproducibility/boxspline2.py`, `boxspline_exact.py`, `boxspline_exact2.py`, `exact_volume.py`,
  `boxspline_hp.py`, `hp_one.py`, `hp_batch.py` — the exact/high-precision box-spline engines.
- `reproducibility/hankel_exact.py` — Λ_1,Λ_2 exact + Λ_3,Λ_4 sampler evidence.
- `reproducibility/simulate_m5_bias.py`, simulation outputs — L=25/L=50 DPP runs.
- Full hashes: `SHA256SUMS`.

## Remaining gaps / honesty
- The exact m_5 = 101/18 is a computer-verified exact identity (rational), validated by two
  independent engines and anchored on m_2,m_3,m_4. It is NOT yet a closed-form general-k theorem.
- DPP numerics are consistent-with (within ~2σ) but do not independently PIN m_5=101/18 due to
  finite-L and h-bias; no nUmerical evidence is treated as proof.
- SL-relevant Λ_m decay is unresolved beyond Λ_2; explicit, honest: the plateau vs decay of Λ_3,Λ_4
  is UNKNOWN without exact higher moments.
