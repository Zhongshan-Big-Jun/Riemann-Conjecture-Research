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
