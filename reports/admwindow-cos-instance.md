# AdmWindow / ModFactor blueprint for v_MT = cos(√2s) (formalization-ready, 2026-08-15)

Purpose: close, at the math level, the A1 open item of reports/xi-prime-audit-manager.md —
the Lean `admWindow_phiV` instance for the Montgomery–Taylor profile v_MT(s) = cos(√2 s),
which `windowZeroSide_atV_of` (Zeta23/XiPrime/QuarticWindow/ZeroSide.lean:110) needs to
instantiate `WindowZeroSide` for the ξ′ zeros with the MT profile. Every bound below is
elementary (sin x ≤ x, cos x ≥ 1 − x²/2, alternating-series bounds), with exact closed
forms confirmed at mpmath 40 digits.

## 1. Profile-level norms (v = v_MT on [−1/2, 1/2])

Closed forms (exact; quadrature on |sin| integrands is unreliable at the u = 0 kink, so the
closed forms are authoritative — they agree with quadrature to 5-6 digits only):

| Quantity | Closed form | Value (40 dp) | Simple bound |
|---|---|---|---|
| ‖v′‖₁ | 2(1 − cos(1/√2)) | 0.47951080584873969749… | ≤ 1/2  (cos x ≥ 1 − x²/2 at x = 1/√2) |
| ‖(v²)′‖₁ | 1 − cos(√2) | 0.84405630523462552655… | ≤ 38/45  (cos(√2) ≥ 7/45 via alternating series: 1 − 1 + 1/6 − 1/90) |
| ‖v″‖₁ | 2√2·sin(1/√2) | 1.8374507397311368756… | ≤ 2  (sin x ≤ x) |
| ‖(v²)″‖₁ | 2√2·sin(√2) | 2.7938239945464334394… | ≤ 4  (sin x ≤ x) |
| a = L⁻¹∫v² (L=1) | 1/2 + sin(√2)/(2√2) | 0.84922799931830417992… | ∈ [1/2, 1]  (0 ≤ sin(√2) ≤ 1) |
| b = L⁻¹∫v⁴ (L=1) | 3/8 + sin(√2)/(2√2) + sin(2√2)/(16√2) | 0.73784297545060818785… | ≤ 3/8 + 1/(2√2) + 1/(16√2) < 1 |

All four norm bounds are ≤ 2 resp. ≤ c/w with c = 4, w = 1 — the AdmWindow thresholds
(WindowCore.lean:31-43). Structure fields: even ✓ (cos), nonneg ✓ (cos ≥ cos(1/√2) =
0.76024459707563… ≥ 3/4 > 0), le_one ✓ (cos ≤ 1), ContDiff ℝ 2 ✓ (analytic), support:
supplied by the taper in the modulated construction (phiM_eq_zero, ModWindow.lean:59) — the
profile need not vanish.

## 2. ModFactor instance for f_c(u) = √(cos(√2·u/L))

Template: `ModFactor f_Q L (3/2) 12` (Quartic.lean:257) with f_Q = √(max 0 vQuartic(·/L)),
f_Q ≥ 4/5, |f_Q′| ≤ (29/20)/L, |f_Q″| ≤ 12/L². For cos the factor is strictly simpler
(no max needed: cos ≥ 3/4 > 0 on |u| ≤ L/2):

- even ✓, nonneg ✓, le_one ✓, **antitone on [0, L/2] ✓** (cos decreasing on [0, 1/√2·L/2]…:
  argument √2·u/L ≤ 1/√2 < π/2, cos decreasing there; √ increasing ⇒ f_c decreasing).
- smooth: C^∞ on (−(L/2+δ), L/2+δ) for small δ (cos ≥ 3/4 > 0 on that neighborhood).
- |f_c′|: f_c′(u) = −√2·sin(√2u/L)/(2L·√(cos(√2u/L))); with |sin(√2u/L)| ≤ √2|u|/L ≤ 1/√2 and
  √cos ≥ √3/2:
  |f_c′| ≤ √2·(1/√2)/(2·√3/2)/L = **1/√3·L⁻¹ < 1/L** → **A = 1**.
- |f_c″|: f_c″(u) = F″(u/L)/L², F(t) = √(cos(√2t)), F″(t) = −[√(cos(√2t)) + sin²(√2t)/(2cos^{3/2}(√2t))];
  |F″| ≤ 1 + 1/(2·(3/4)^{3/2}) = 1 + 1/(2·(3√3/8)) = 1 + 4/(3√3) ≈ 1.7698 < 2 → **B = 2**.
- Core lower bound: f_c ≥ √(3/4) = √3/2 ≈ 0.8660 (better than quartic's 4/5).

## 3. Consequence

`admWindow_phiM` (ModWindow.lean:485) builds the AdmWindow for φ_f = f_c·φ₀ with window
constant c = cMod = Taper.cRho + A + A² + B = **cRho + 4** (quartic: cRho + 15.75; cos is
strictly better). With `windowZeroSide_atV_of` (which needs only an even admissible v and an
admWindow proof), the ξ′ zeros (xiDerivZeros) get `WindowZeroSide (xiDerivZeros …) P (P.atV v_MT)`
— the A1 zero-side bundle for the MT profile — and the whole ξ′ chain
(reports/xi-prime-cor22-derivation.md) is instantiated. Profile-side a = 0.8492 ∈ [1/2, 1]
feeds the a_half proof (same template as quartic's a_Q).

## 4. Verification log

2026-08-15: all closed forms and bounds checked at mpmath 40 digits (script inline in the
session; numbers above transcribed from the run output). Quadrature kink caveat recorded:
mp.quad on |−√2 sin(√2u)| and |−√2 sin(2√2u)| has ~1e-6 error at u = 0; closed forms exact.

Status: A1 math-level gap CLOSED; remaining work is Lean code following the quartic
template (Stage C formalization, AtOne pattern) — out of scope for this session.
