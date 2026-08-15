# Obligation graph — R-20260816T060000Z-m6exact-4f9a

## Claims and status
- **C1. m_6 = 640/63 (exact).** Status: ESTABLISHED (this run). Depends on C2,C3,C4,C5. Verified by
  assembly over 203 partitions + positive-definiteness anchor.
- **C2. c_12 = 655177/1663200.** Status: ESTABLISHED (derived exact + mpmath ∫sinc¹²).
- **C3. b=1,2 contributions = 1, 4297/630.** Status: ESTABLISHED (analytic J=c_m−c_{m+2} verified on
  all 31 b=2 partitions).
- **C4. b=3 sum = 479/210.** Status: ESTABLISHED (exact engine on all 90 partitions).
- **C5. b=4 sum = 2/35; b=5 = 0; D_6 = 0.** Status: ESTABLISHED via fast engine (validated per-term
  vs sympy exact); residual audit = full sympy re-verification of 65 b=4 shapes (open, low risk).
- **C6. Moment sequence m_0..m_6 positive definite (det H_0..H_3 > 0).** Status: ESTABLISHED; is the
  anchor that catches gross errors and forces b≥4 ≠ 0.
- **C7. Λ_1=1/4, Λ_2=5/36, Λ_3=247/2519.** Status: ESTABLISHED (from exact moments).
- **C8. Fork = decay, plateau impossible.** Status: ESTABLISHED by the structural argument
  Λ_3(m_6) < 5/36 = Λ_2 for all valid m_6.
- **C9. b≥4 does not all vanish at k=6.** Status: ESTABLISHED (positivity forces b≥4 contribution;
  measured = +2/35 from b=4).
- **C10 (open). General-k Lemma P / G2.** k=5, k=6 instances recorded; general proof open.
- **C11 (open). Exact m_7, m_8 ⇒ Λ_4.** Out of scope this pass.

## Dependencies
C1 ⇐ C2..C5; C7 ⇐ C1 + prior m_1..m_5; C8 ⇐ C7 + positivity; C9 ⇐ C6.
