# Approach registry — R-20260816T060000Z-m6exact-4f9a

## Route families tried / states
| Route | State | Result / why |
|---|---|---|
| Direct float box-spline shape sum (`shape_integral_exact`) | FAILED (as driver) | Unreliable at k=6: gave −303/6302 for a b=3 shape with true J=0 (float cancellation + hull noise). Used only for per-term sanity. |
| Exact sympy box-spline (`boxspline_exact2`) | OK (b=2,3); budget-limited (b=4..6) | Correct but O(C(2n,m)) sympy per subset; b=4 partition ~25+ min. Used for all 90 b=3 shapes and per-term audit. |
| Fast exact engine (`boxspline_exact_fast`) | OK (b=4,5,6) | Same integer null basis, numpy vertex-finding + scipy hull; ~10^3× faster, =0.0 per-term diff vs sympy on b=4 (n=8/9), exact on b=2/3. Drove b=4 (65), b=5 (15), D_6. |
| b=2 analytical reduction `J = c_m − c_{m+2}` | OK | Verified vs exact engine on all 31 b=2 partitions; sums to 4297/630. |
| c-value derivation `B_{2n}(0)` formula | OK | c_12 = 655177/1663200; mpmath cross-check. |
| Direct numeric integration (scipy/mpmath) | FAILED (evidence only) | Tail-heavy `∫sinc²` gives ~1e−4 errors near ∞; cannot resolve ~1e−3 shape values reliably. |
| DPP simulation (L=50) | KILLED early (evidence) | Freed CPU for exact b=3; earlier m5-run L=50 evidence + task sampler m_6≈9.5–10 consistent with exact 10.16 under finite-L/h-bias. |

## Owners
Solver (this pass) ran all routes; validation of the fast engine vs sympy exact and the
positive-definite anchor are the two independent checks.

## Exact gaps
- Full sympy re-verification of all 65 b=4 shapes (fast-engine sanity + per-term cross-check done).
- Exact m_7, m_8 (⇒ Λ_4 exact) — future.
