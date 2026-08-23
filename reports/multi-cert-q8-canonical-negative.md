# Multi-certificate LP: adding canonical q=8 certificates does not help

Status: **NUMERICAL_EVIDENCE** — no new proven bound.

Run date: 2026-08-23.

## Question

Can adding our known canonical q=8 (9-point) certificates as extra same-q
inputs improve the existing retuned 7+9 two-certificate LP?

## Result

| certificate set | best m | B |
|---|---:|---|
| baseline retuned 7+9 | 219 | 0.673316977142471313323 |
| baseline + all canonical q=8 points (0.00392, 0.0039, 0.0038) | 219 | 0.673316977142471313900 |

The LP assigns `tau = 0` to all canonical q=8 extras. There is no meaningful
improvement.

## Interpretation

The retuned 9pt-final operating point dominates the canonical q=8 certificates
in this LP. Extra same-q canonical certificates from the general-k family do
not add value; only a **different/stronger retuned operating point** or a new
q=9 operating point can push the multi-certificate bound.

## Reproducibility

- Script: `runs/.../R-20260817T030000Z-shiGeneralize-4f2a/reproducibility/multi_cert_q8_canonical.py`
- Output: `.../multi_cert_q8_canonical.out`
