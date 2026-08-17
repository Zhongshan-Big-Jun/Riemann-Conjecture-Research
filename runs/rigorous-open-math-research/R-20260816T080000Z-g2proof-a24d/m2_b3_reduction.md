# M2 progress — b=3 family reduction and exact box-spline values

**Label: `RIGOROUS_PARTIAL_RESULT` (paper-level reduction; exact values computer-verified).**

## Summary

The G2 general-k proof attempt has now reduced the entire **b=3 family** of M2 to a
closed determinant expansion, and verified the vanishing/nonvanishing dichotomy on the
small b=3 shapes by exact rational box-spline values.

## Established so far (from earlier passes + this reduction)

- **M1 is closed**: `H_σ` is always connected; the disconnected branch is vacuous.
- **b=2 family is proven**: `ρ₂ = 1 − K²`, so `J = c_m − c_{m+2}` with `c_m = ∫K^m`
  strictly decreasing, hence `J > 0` for all `m ≥ 2`.
- **Killed routes**:
  - multiplicative class-function / EGF route killed by exact counterexample:
    at `b=4,m=4` (4-cycle), `(2,2)`-type `B` values are `{9/20, 11/30, 9/20}`,
    so `B(2,2)=9/20 ≠ (2/3)² = 4/9`.
  - naive degree-2 contraction killed: triangle `b=3,m=3` gives `J=0`, but contracting
    to `b=2,m=2` gives `J=1/3 ≠ 0`.

## b=3 determinant expansion (new reduction)

Expanding the 3×3 determinant

```
ρ₃ = 1 − K₀₁² − K₀₂² − K₁₂² + 2K₀₁K₀₂K₁₂
```

gives the exact closed reduction for the whole b=3 family:

```
J_σ = B_H(0) − Σ_{i<j} B_{H+2·(ij)}(0) + 2·B_{H+triangle}(0)
```

where `H+2(ij)` is `H` plus a doubled edge and `H+triangle` is `H` plus the full triangle.
This identity reproduces both known b=3 cases exactly:

- Triangle `b=3,m=3` (the only b=3 shape with `m ≤ 2b−3 = 3`):
  `J = 1 − 3·(2/3) + 2·(1/2) = 0`.
- Fan `b=3,m=4`:
  `J = 1 − (1/2+2/3+2/3) + 2·(9/20) = 1/15 ≠ 0`.

Certified exact box-spline values involved: `{1, 2/3, 1/2, 9/20}` (denominators ≤ 180;
two independent implementations).

## Recommended next checks / mechanisms

1. Confirm the two discriminating new k=7 shapes:
   - `b=4,m=7` (rule predicts NONZERO),
   - `b=5,m=7` (rule predicts ZERO).
   A background exact-engine verification (`verify_k7_b45.py`) is running.
2. Generalize the determinant-expansion reduction: expand `ρ_b = det[K(x_i−x_j)]` over
   permutations; for low-surplus `H` (`cyclomatic ≤ b−2`), `H ∪ match(π)` stays
   sphere-like and its box-spline should decompose into 1-D constants `c_{2t}` times
   simple rationals. The open core is the non-multiplicative determinant-identity /
   Cauchy–Binet mechanism.

## Status

- M1: DONE.
- b=2: PROVEN.
- b=3: REDUCED + exact small-case verification (vanishing triangle, nonvanishing fan).
- General b ≥ 4 M2: OPEN; k=7 surplus-boundary verification in progress.

This is a partial result, not a full proof of M2.
