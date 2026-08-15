# f_9 step ladder — certified-target planning (manager, 2026-08-14)

Computed with mpmath (25+ digits), general-k chain C_9(f) = (H_MT − (m−1)/(500m)) / (1 − f·n/m),
m = 8 + n, n = ⌈1/f⌉ − 1, H_MT = 0.67250070367941164573….

| Certified f_9 | n | m | A_0 = f·n | C_9 (new record) | Gain vs 0.0039 |
|---|---|---|---|---|---|
| 0.00390 (done) | 256 | 264 | 0.9984 | 0.673053645952589925 | — |
| 0.00391 | 255 | 263 | 0.99705 | 0.67305992191189169 | +6.3e-6 |
| 0.00392 | 255 | 263 | 0.9996 | 0.673066472675939666 | +1.3e-5 |
| 0.00393 | 254 | 262 | 0.99822 | 0.673072744423451255 | +1.9e-5 |
| 0.00394 | 253 | 261 | 0.99682 | 0.673079012573332524 | +2.5e-5 |
| 0.00395 | 253 | 261 | 0.99935 | 0.673085562133504049 | +3.2e-5 |
| 0.00396 | 252 | 260 | 0.99792 | 0.673091825967756815 | +3.8e-5 |
| 0.00397 | 251 | 259 | 0.99647 | 0.673098086111331951 | +4.4e-5 |
| 0.00398 | 251 | 259 | 0.99898 | 0.673104634442792576 | +5.1e-5 |

All rows satisfy the rigor condition A_0 < 1. Strategy: attempt 0.00395 (grid 4000) after the
baseline re-run; if the branch-and-bound does not close within a generous budget, step down
(0.00394, 0.00393, …) — every certified step is a new world record. Numerically indicated true
minimum of F_8: ≈ 0.00398 (evidence only; extpress scoping).

## Cost gradient vs true minimum (manager, 2026-08-14, second pass)

| f_9 | n | m | A_0 | margin to true min (0.0039818) | note |
|---|---|---|---|---|---|
| 0.00395 | 253 | 261 | 0.99935 | 3.18e-5 | practical ceiling (in progress) |
| 0.00396 | 252 | 260 | 0.99792 | 2.18e-5 | likely 5–10× B&B cost |
| 0.00397 | 251 | 259 | 0.99647 | 1.18e-5 | likely ≫10× cost |
| 0.00398 | 251 | 259 | 0.99898 | 1.82e-6 | infeasible (equality case at the min) |

B&B cost grows steeply as the margin shrinks; 0.00395 is the realistic ceiling, with
0.00393–0.00394 as fallback steps if the 0.00395 runs cannot close.

## True-minimum verification (manager, 2026-08-14)

Recomputed F_8 at the scoping optimum (k9_opt.npy,
[1.0471, 1.9927, 2.0018, 2.0024, 2.0024, 2.0018, 1.9927, 1.0471]) using the scoping kernel
kk(x) = (sinc(πx−1/√2) + sinc(πx+1/√2))/(2√2·sin(1/√2)): **F_8 = 0.0039818181719** ≈ 0.00398 ✓
(extpress claim confirmed). Reference points: all-2.0 → 0.00436; all-1.99 → 0.00495.
Consequence: a certificate at the true minimum (0.00398) would require equality handling and
is effectively infeasible; **f_9 = 0.00395 (margin 3.2e-5) is the realistic ceiling**, with
0.00393–0.00394 as fallback steps.

## True-minimum re-verification with the CERTIFICATE kernel (manager, 2026-08-15)

The scoping kernel kk(x) and the certificate kernel k(x) (kernel.py, normalized_kernel:
k(x) = [sinc(1/√2 − πx) + sinc(1/√2 + πx)]/2 / (√2·sin(1/√2))) are algebraically IDENTICAL
(sinc evenness + k_zero = √2 sin(1/√2)). Re-evaluated F_8(g) = (1/4000)Σg_i +
Σ_{s=1..8} (2/(9−s))Σ_i k(span)² with arb enclosures (256-bit) at the same points:

| point | F_8 (certificate kernel, arb) | ladder claim |
|---|---|---|
| k9_opt | 0.003981819776026 ± 6e-16 | 0.0039818181719 ✓ (1.6e-9 diff = rounded point coords) |
| all 2.0 | 0.004355474104594 ± 5e-16 | 0.00436 ✓ |
| all 1.99 | 0.004947869925822 ± 2e-16 | 0.00495 ✓ |

Conclusion: true min ≈ 0.0039818 confirmed with the actual certificate kernel; the 0.00395
target margin ≈ 3.2e-5 stands. (Note: F_8 must use w = k², not k — the kernel itself is
sign-indefinite; the squared form is the pressure weight from the general-k derivation.)

## CORRECTION — 0.00395 CERTIFICATION FAILED; true min ≈ 0.00395005 (manager, 2026-08-15)

**Both 0.00395 certification runs (pwsh-1 grid-4000, pwsh-2 grid-2000, 8 workers, prec 128)
FAILED** with exit code 2 (loud fail): the branch-and-bound reached width-0 leaf boxes whose
rigorous lower bound is below the target:

- grid-2000 leaf cells (2095, 3992, 3999, 3999, 3972, 2090, 3954, 2090) → physical
  [1.0475, 1.996, 1.9995, 1.9995, 1.986, 1.045, 1.977, 1.045]; bound 0x1.0195c3373fb78p-8
  ≈ 0.0039314.
- grid-4000 leaf cells (4186, 7984, 7998, 7998, 7946, 4181, 7903, 4181) → physical
  [1.0465, 1.996, 1.9995, 1.9995, 1.9865, 1.04525, 1.97575, 1.04525]; bound
  0x1.02367203313ebp-8 ≈ 0.00394017.

**Exact-kernel evaluation** (mpmath, dps=50; k = normalized Montgomery–Taylor kernel):
F_8 at the g2000 lower corner = 0.003950153311868921, at the g4000 lower corner =
0.003950049001339790, at the g4000 midpoint = 0.003950746112768043. L-BFGS-B box
minimization over the g4000 leaf box from two starts converges to the lower corner
(0.003950049001339789) — the box minimum is AT THE CORNER. k9_opt still evaluates to
0.003981819776025529 (a DIFFERENT, higher local minimum).

**Consequences:**
1. The earlier "true min ≈ 0.0039818" was only a local-minimum claim; the scoping
   optimization that produced k9_opt missed the lower basin near
   (1.0465, 1.996, 1.9995, 1.9995, 1.9865, 1.04525, 1.97575, 1.04525). The true global
   minimum satisfies 0.0039 ≤ m* ≤ 0.003950049 (lower bound from the PASSED 0.0039
   certificate; upper bound from this configuration). Plausibly m* ≈ 0.003950049.
2. Target 0.00395 has true margin ≈ 4.9e-8, while the verifier's box bound at the critical
   leaf loses ≈ 1e-5 (range-min table over span cells). Even a perfect S→∞ leaf refinement
   retains the intrinsic quadratic-dip loss ≈ 3.5e-6 (Σ_r (2/(9−r))·½k″·(r·w)² ≈ 224·½·0.5·w²,
   w = 2.5e-4). Certifying 0.00395 would need grid ≳ 34000 — **0.00395 is infeasible;
   abandoned** (NOT a machinery bug: all bounds are down-rounded rigor; the gap is
   bound-loss > true margin).
3. **New release target: f_9 = 0.00392, grid-2000** (launched pwsh-4, 8 workers,
   2026-08-15). Margins: 1.14e-5 above the g2000 critical-leaf bound, ≈ 3.0e-5 above the
   presumed true min. Expected certificate values precomputed: cutoff 31368, kernel sha256
   39a209d3e4a897d982023ab49db27a206401824c769980572433dc4c47387297, components
   [[1868,2458];[3511,30823]], initial_boxes 256, second-deriv sha256
   29ca4522e12a991b7ab48943838a174fb2350b328ecc2155d9ecba4cb429f32c (second_start 1900).
   C_9(ζ, 0.00392) = (657500·H_MT − 1310)/655001 = 0.673066472675939665848…
   C_9(ξ′, 0.00392) = (657500·H_ξ′ − 1310)/655001 = 0.86920009109661916183995…
   Fallback if the 0.00392 run cannot close: 0.00391 (C_9(ζ) = 0.67305992191189169,
   margin ≈ 4.0e-5 vs presumed true min).

## 0.00393 / 0.00394 premium assessment (manager, 2026-08-15, after the 0.00392 release)

Post-release re-assessment of the next ladder steps (0.00392 certified 2026-08-15):

| f_9 | n | m | A_0 | exact rational C_9(ζ) | C_9(ζ) (mpmath 50d, re-verified) | gain vs 0.00392 | feasibility |
|---|---|---|---|---|---|---|---|
| 0.00393 | 254 | 262 | 0.99822 | (13,100,000·H_MT − 26,100)/13,050,089 | 0.673072744423451254556223736062 | +6.3e-6 | BORDERLINE: margin vs g4000 leaf bound = 1.017e-5, vs presumed true min ≈ 2.0e-5; verifier bound loss at the critical leaf ≈ 1e-5. Same order as the SUCCESSFUL 0.00392 grid-2000 run (margin 1.14e-5) but on grid-4000 (4× cells/dim; est. 1–2 days @ 8 workers; initial_boxes 4^8 = 65536) |
| 0.00394 | 253 | 261 | 0.99682 | — | 0.673079012573332524 | +1.25e-5 | RISKY: margin ≈ 1.7e-6 vs leaf bound (g4000) — below bound loss; likely infeasible with this machinery |

Recommendation: 0.00393 grid-4000 is the only remaining k=9 premium step worth attempting, and it is
borderline (margin ≈ bound loss). Cost 1–2 days of compute for +6.3e-6. NOT launched 2026-08-15:
(i) the k=10 scoping (reproducibility/scoping_k10.py, running) may indicate a better cost/benefit
elsewhere; (ii) the Stage C formalization + SL threads are the priority. Revisit after those settle;
if attempted, launch grid-4000 @ 8 workers with the validated verifier (--out atomic write) and
precomputed expected values (cutoff = floor((393/100000)*4000*4000)+8 = 62888; kernel table grid 4000).
