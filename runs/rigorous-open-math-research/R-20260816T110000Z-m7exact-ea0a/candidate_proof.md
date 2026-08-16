# Candidate proof — SL exact m₇/m₈ (bounded pass)

Run: `R-20260816T110000Z-m7exact-ea0a`
Status line: `RIGOROUS_PARTIAL_RESULT` — all b≤3 exact m₇ contributions are computed and
certified; the b=4 isoclasses (8 remaining) are heavy and were not completed in budget. Full
m₈ is infeasible in this bounded pass; the b≤2 contribution is exact.

## 1. Setup and pruning

- Bell(7) = 877 set partitions enumerated; G2 rule applied.
- Survivors: **540** (1 b=1, 63 b=2, 266 b=3, 210 b=4); 337 pruned by low-surplus.
- H-isoclass collapse: **18 distinct isoclasses** (1 b=1, 3 b=2, 6 b=3, 8 b=4).
- k=8 preflight: Bell(8) = 4140 → **2683 survivors** → **46 isoclasses**
  (1 b=1, 4 b=2, 9 b=3, 19 b=4, 13 b=5). Full exact m₈ requires b=4/5 classes with high
  cost; judged infeasible in this bounded pass.

## 2. Exact m₇ — completed classes

All 10 b≤3 isoclasses are computed exactly, each cross-validated by two engines
(`boxspline_exact2` + `boxspline_exact_fast`) with rational reconstruction:

| b | m | #partitions | J (exact) |
|---|---|---|---|
| 1 | 0 | 1 | 1 |
| 2 | 2 | 21 | 1/3 |
| 2 | 4 | 35 | 7/60 |
| 2 | 6 | 7 | 89/1260 |
| 3 | 4 | 70 | 1/15 |
| 3 | 5 | 105 | 1/180 |
| 3 | 6 | 28 | 1/420 |
| 3 | 6 | 42 | 11/630 |
| 3 | 7 | 7 | 13/2520 |
| 3 | 7 | 14 | 1/840 |

**Partial exact sum (b≤3):**
```
m₇^(b≤3) = 1345/72 ≈ 18.680555555…
```

## 3. Partial m₈ (b≤2)

- `m₈^(b≤2) = 3724369/181440 ≈ 20.526725`
- Full m₈ (b=3,4,5) remains OPEN.

## 4. Open / remaining

- The 8 b=4 isoclasses of m₇ remain uncomputed; each is heavy (24 perms, exact engine).
  Completing them would give the exact full m₇ and then Λ₄(0).
- Full m₈ (b≥3) is infeasible in this bounded pass.

## 5. Honesty

- All reported rationals are exact (dual-engine cross-check, `engine_diff=0.0` where recorded).
- No numerical evidence is presented as proof.
- The run is a partial exact computation, not a proof of SL; it provides strong exact
  moment-route data through b≤3 at k=7.
