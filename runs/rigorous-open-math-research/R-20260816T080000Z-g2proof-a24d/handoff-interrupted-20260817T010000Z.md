# Interruption handoff — SL G2 general-k proof (M2 continuation)

- **Run ID**: R-20260816T080000Z-g2proof-a24d
- **Task packet ID**: Q-20260814-criticalline-p1-507bb5 (SL gap G2)
- **Date**: 2026-08-17T01:00Z
- **Interrupt reason**: user requested termination of research and repository handoff; an
  exact k=7 b=4/b=5 verification was still running.
- **Task state**: IN_PROGRESS

## Task state

IN_PROGRESS / RIGOROUS_PARTIAL_RESULT (M2 not fully closed).

## Completed work progress

- **M1 is closed**: `H_σ` is always connected; the disconnected branch is vacuous.
- **b=2 family is proven**: `J > 0` for all `m ≥ 2`.
- **b=3 family reduction is recorded** in `m2_b3_reduction.md`:
  - determinant expansion `ρ₃ = 1 − K₀₁² − K₀₂² − K₁₂² + 2K₀₁K₀₂K₁₂` yields
    `J_σ = B_H − Σ B_{H+2(ij)} + 2B_{H+triangle}`.
  - exact values `{1, 2/3, 1/2, 9/20}` reproduce `J=0` (triangle, m=3) and
    `J=1/15` (fan, m=4).
- Killed routes documented in `counterexample_log.md`:
  - multiplicative class-function / EGF route killed by `b=4,m=4` counterexample;
  - naive degree-2 contraction killed by triangle-to-b=2 comparison.

## Completed obligations

- M1, b=2 family, b=3 reduction (paper-level, exact small-case values).

## Open obligations

- M2 for general `b ≥ 4` (the low-surplus signed box-spline telescoping identity).
- Exact verification of the two discriminating new k=7 shapes:
  - `b=4,m=7` (rule predicts NONZERO),
  - `b=5,m=7` (rule predicts ZERO).
  The verification script `verify_k7_b45.py` was started in background and was killed at
  user request before producing output.

## Tools and methods tried

- [SUCCEEDED] Exact box-spline engine / rational reconstruction for b=3 small shapes.
- [PARTIAL] Determinant-expansion reduction for b=3.
- [PARTIAL] `verify_k7_b45.py` exact-engine verification of k=7 b=4/b=5 shapes: started,
  not completed.
- [FAILED] Multiplicative class-function / EGF route (counterexample logged).
- [FAILED] Degree-2 contraction route (counterexample logged).

## Attempted routes

- [SUCCEEDED] M1 connectedness proof.
- [SUCCEEDED] b=2 proof.
- [SUCCEEDED] b=3 determinant reduction + exact small-case values.
- [IN PROGRESS] k=7 b=4/b=5 exact verification (interrupted).
- [OPEN] General b≥4 M2: recommended next mechanism is a non-multiplicative
  determinant-identity / Cauchy–Binet expansion of `ρ_b`.

## Next actions

1. Re-run `reproducibility/verify_k7_b45.py` to completion and record the two exact J values.
2. If b=4,m=7 is nonzero and b=5,m=7 is zero, update `m2_b3_reduction.md` / `candidate_proof.md`
   with the strengthened finite evidence.
3. Attempt the general determinant-expansion reduction for b≥4, focusing on low-surplus
   tree-like `H`.

## Key artifacts

- `m2_b3_reduction.md` (b=3 reduction and exact values)
- `counterexample_log.md` (killed routes)
- `candidate_proof.md` (main partial proof)
- `reproducibility/verify_k7_b45.py` (k=7 b4/b5 exact verification script)
- `reproducibility/boxspline_exact.py`, `boxspline_exact2.py` (exact engine)
