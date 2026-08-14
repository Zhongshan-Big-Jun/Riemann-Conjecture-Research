# Approach registry — R-20260814T041219Z-condp1-698ec7

Route families considered for `lim N0^s/N → 1`, states, and exact gaps.

## R1 — Baseline rank–trace (Prop 4.4(ii)) — exhausted unconditionally
- Owner: §7.1/Thm D. State: **done (unconditional 2/3-class)**. Gap: uses only tr, HS-norm, block
  structure; Prop 7.4 caps at ≤ λ₁N on-line points ⇒ ceiling 2−1/λ₁ → 1 only at λ→1, but m_2
  there would need higher moments; unconditional content is 2/3 (0.67250).

## R2 — Cauchy–Schwarz / n₊ (Prop 4.5, Lemma 3.3) — m=1 exhausted
- Owner: §1.4/§7.5(b). State: **done (m=1)**. n₊(R)/d ≥ m_1²/m_2 = 3/4 (corrected m_2=4/3),
  giving liminf N0^s/N ≥ 1/2 (window-optimal 2c₁*−1 = 0.50659). Gap: cannot improve without
  higher-moment/spectral data.

## R3 — Higher-moment / Christoffel route (this run's HL* route) — CONDITIONAL THEOREM
- Owner: §7.2(f) made rigorous. State: **done as a conditional theorem** (RIGOROUS_PARTIAL_RESULT).
  - Lemma 3.A SOS-witness n₊-bound from moments up to 2m (new, rigorous, unconditional in linalg).
  - Lemma 3.B → 1−Λ_m(0); corrected moments ⇒ Λ_2(0)=5/36 ⇒ N0^s/N ≥ 2(31/36)−1 = 13/18.
  - All-k0 ⇒ 1, conditional on **SL**.
  - Gaps: (a) SL (spectral density of sine-kernel Gram at 0) not in literature — the exact open
    requirement; (b) m_3,m_4 exact closed forms (unnecessary for the theorem, open).

## R4 — PCC full-support route (GLSS25) — complementary, not pursued here
- State: external theorem (GS Thm 5): PCC full support ⇒ 100% simple on line. Gap: PCC is
  conjectural; different hypothesis from HL*. Recorded for reconciliation only (O5-D6).

## R5 — Unconditional 100% — BLOCKED (structural, honest)
- State: **blocked by the known structural ceiling and the absence of unconditional higher-moment
  data** in the relevant band (RS96 kλ<2; Prop 7.4 makes λ≤1/2 vacuous). The user's unconditional
  goal is not reached by any route in this run; only the conditional HL*+SL route reaches 1.

## Failure modes / decision log
- The paper's literal §7.2(d) "1−Λ_m(0)" reading fails for the printed moments (Λ_2=143/100>1);
  fixed by m_2: 3/4→4/3 (see counterexample_log delta_-1).
- Odd moments (m_3) cannot improve the m=1 bound (they don't enter Λ_1); higher moments only help
  via even-order Christoffel/Λ_m, which requires valid (even) moments — corroborating §7.2(e).
