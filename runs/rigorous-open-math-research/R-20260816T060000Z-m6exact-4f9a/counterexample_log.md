# Counterexample log — R-20260816T060000Z-m6exact-4f9a

## Falsified / corrected claims
- **Float coarea engine unreliable at k=6** (even b=3): returned −303/6302 for a b=3 shape whose
  true J=0. Root cause: float cancellation in signed box-spline sums (irrational √2 terms). The
  exact and fast-exact engines are authoritative.
- **"b ≥ 4 ⇒ J_σ = 0" FAILS at k=6.** The k=5 rule does not extend: b=4 contributes +2/35. This is
  forced by positivity (m_6(b≤3)=3182/315 gives det H_3 < 0 ⇒ invalid moment sequence) and
  confirmed by direct exact computation (b=4 sum 2/35; b=5, b=6 vanish).
- **"Only b≤3 shapes contribute" FAILS at k=6** (b=4 contributes).
- **Some b=3 shapes vanish** (20 of 90) — so even within b≤4 the contributing set is nontrivial.

## Edge cases tested
- b=1 (all-equal)=1; b=2 analytic J=c_m−c_{m+2} verified on all 31 (no counterexample).
- b=3: all 90 exact; values {0,1/15,1/180,11/630,1/420}.
- b=4: all 65; some vanish, some give {1/105,−1/840,1/1260,4/315}.
- b=5: all 15 = 0. b=6 (D_6): 0 (consistent with D_3,D_4,D_5=0).
- c_12 cross-check vs mpmath ∫sinc¹² (diff < 1e-17).
- Positivity: m_0..m_6 moment sequence positive definite (det H>0) — no violation.

## Obstructions
- Exact m_7, m_8 (for Λ_4): not computed (box-spline enumeration scales up; sampler m_7,m_8 are
  finite-L biased). This is the precise obstruction to the exact full decay curve.
- Full sympy re-verification of all 65 b=4 shapes: budget-limited (each ~25 min with sympy); the
  fast engine is cross-checked per-term (=0.0 diff) and the aggregate anchored by positivity.
