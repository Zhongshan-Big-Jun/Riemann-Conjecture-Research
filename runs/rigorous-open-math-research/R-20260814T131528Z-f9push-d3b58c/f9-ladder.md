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
