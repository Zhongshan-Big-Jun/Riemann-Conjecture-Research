# Audit report — R-20260816T060000Z-m6exact-4f9a

Independent verification performed this pass, and the residual audit items.

## Independent checks that PASS
1. **c_12:** box-spline formula vs direct mpmath ∫sinc¹² — diff < 1e−17; also reproduces c_2..c_10.
2. **b=2:** analytic `J = c_m − c_{m+2}` vs the sympy exact engine on all 31 b=2 partitions — exact
   equality for every one (m=2→1/3, m=4→7/60, m=6→89/1260).
3. **b=3:** all 90 partitions computed with the sympy exact engine (`boxspline_exact2`); values are
   clean small rationals {0, 1/15, 1/180, 11/630, 1/420}; sum 479/210.
4. **b=4 per-term:** the fast engine's per-term box-spline values for a nonzero b=4 partition match
   the sympy exact engine exactly (diff = 0.0) on n=8 and n=9 terms.
5. **Anchors:** engine reproduces m_2=4/3, m_3=2, m_4=13/4 (re-run in the m5 run and verified here);
   Λ_1, Λ_2 reproduce 1/4, 5/36.
6. **Positive-definiteness:** moment sequence m_0..m_6 has det H_0=1, H_1=1/3, H_2=5/108, H_3=
   247/108864 all > 0 — a strong independent consistency check (a wrong b=4 value would very likely
   break this).
7. **Structural fork bound:** Λ_3(m_6) < 5/36 for all valid m_6 (affine-in-m_6, monotonic, asymptote
   = 5/36 from below) — analytic, no numerics.

## Residual audit items (open, honest)
- **Full sympy re-verification of all 65 b=4 shapes.** The fast engine is cross-checked on b=2/3 and
  per-term on one b=4 partition (0.0 diff), and the aggregate is anchored by positive-definiteness;
  a complete sympy pass over b=4 is the remaining rigorous audit (each b=4 partition is ~25+ min with
  the sympy engine, budget-limited this pass).
- **Exact m_7, m_8** (for Λ_4 exact). Sampler m_7,m_8 are finite-L biased; Λ_4 from them is
  unreliable evidence only.

## Unresolved issues
- The plateau/noisy Λ_4 from sampler data (≈0.18 at m_7≈18.3, m_8≈35.2) is inconsistent with the
  exact Λ_3 decay — attributed to finite-L/h-bias on m_7,m_8; resolved by future exact m_7,m_8.
