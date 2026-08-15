# Counterexample / failure log — M3-open-A

This pass is a bounded formalization/computation; no adversarial counterexample hunt was
targeted, but several implementation failures were caught and their mechanisms recorded.

## F1 — py-flint ARB vConv closed form was wrong (double-division)
- Symptom: arb Simpson for J1 gave ∫f ≈ 0.0366 instead of the true 0.1063; κ₉ came out ~1.05
  instead of 1.13, and the "certified sandwich" missed the canonical κ₁=1.132.
- Mechanism: `vConvMT` computed `½·[(1−r)cos(√2r) + sin(√2(1−r))/(2·√2)]`, but the correct form
  is `½(1−r)cos(√2r) + sin(√2(1−r))/(2√2)` (the ½ already distributes over the sin term).  The
  extra `/(2√2)` made the sin-term half too small → integrand ~64% of true → wrong J1.
- Fix: derive the closed form again (product-to-sum) → `/(√2)` inside the ½-parens.  Post-fix
  pointwise arb matched mpmath.
- Lesson: every closed form was re-derived and checked against independent quadrature.

## F2 — python-flint `arb(mid, rad)` is (midpoint, radius), NOT (lo, hi)
- Symptom: `J1_int = arb(S.mid−S.rad−rem, S.mid+S.rad+rem)` gave a correct midpoint but radius
  = upper endpoint → κ₉ interval width inflated to 0.25.
- Mechanism: `arb(lo, hi)` treats args as (midpoint, radius); passing an upper endpoint as the
  "radius" silently grossly enlarged the enclosure.
- Fix: explicit `enc(lo, hi) = arb((lo+hi)/2, (hi−lo)/2)`.  Post-fix κ₉ width ~5·10⁻¹⁶.
- Lesson: treat interval construction in python-flint carefully; verify radius magnitudes.

## F3 — naive per-panel |f^{(4)}| interval evaluation blew up (dependency problem)
- First rigorous-integration attempt bounded Simpson remainder via `f4(arb(lo,hi))` over each
  panel; interval arithmetic over a degree-20 polynomial+trig gave huge overestimates (radius ~
  the whole integral).  Replaced with a single global bound `M₄` from the triangle inequality:
  after sympy reduces `f4` to `A+cos(√2r)B+sin(√2r)C` over exact rationals,
  `|f4| ≤ Σ|a_i|+Σ|b_j|+Σ|c_k| = 2601.3…`; Simpson error ≤ M₄·h⁴/180 ≈ 9·10⁻¹⁷ ≪ ε₉.  Rigorous
  and tight.

## F4 — `sp.NegativeOne` doesn't exist in sympy 1.13
- Removed the special-case; `sp.Integer(-1)` already handles negatives in the arb converter.

## F5 — Lean `kappaXi_one_vMT_mem` algebra: `kappaXiOne_MT` not unfolded by nlinarith; `ring`
      vs `le_rfl` on an inequality goal
- Lower bound: had to `unfold kappaXiOne_MT; field_simp` before `nlinarith [hJ.1]`.
- Upper bound: final calc step target is an `≤` that reduces to `le_rfl`, not a `ring`
  (equality) goal.  Fixed final step to `exact le_rfl`.

None of F1–F5 invalidates the mathematics; each was a concrete, reproducible implementation
defect with a precise mechanism and fix, recorded for reproducibility.
