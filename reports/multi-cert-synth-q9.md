# Multi-certificate LP: synthetic q=9 / k=10 exploration

Status: **NUMERICAL_EVIDENCE** — synthetic certificates are NOT certified. This scan
explores whether a future k=10 (q=9) certificate could improve the existing
two-certificate supporting-plane bound.

Run date: 2026-08-23. Uses the original `multi_cert_scan.py` read-only.

## Results

| certificate set | best m | B (LP bound) | tau_6 | tau_8 | tau_9 |
|---|---:|---:|---:|---:|---:|
| baseline retuned 7+9 | 219 | 0.673316977142471313323 | 1.8576e-5 | 3.7967e-4 | — |
| baseline + synthetic canonical q=9 (p=1/4500, eps=0.00395) | 219 | 0.673316977142471313641 | 1.8576e-5 | 3.7967e-4 | 0.0 |
| baseline + synthetic strong q=9 (p=1/4500, eps=0.0042) | 238 | 0.673318429680808739328 | 0.0 | 3.7023e-4 | 1.6541e-5 |

## Interpretation

- A **canonical** k=10 certificate modelled as `(q=9, p=1/4500, eps=0.00395)` gives **no improvement**:
  the LP sets `tau_9 = 0` and keeps the existing two-certificate optimum.
- A **stronger** synthetic q=9 operating point `(eps=0.0042)` gives only a tiny
  improvement: `+1.45e-6` over the baseline (`0.6733184296808` vs `0.6733169771424`).
- Therefore, to beat the current Shi two-certificate value through the multi-certificate
  LP, a new k=10 certificate would need to be a **retuned/stronger operating point**,
  not merely the canonical `f_10 ≈ 0.00395` from the general-k family.

## Reproducibility

- Script: `C:\Users\HuangZY\AppData\Local\Temp\multi_cert_synth.py`
- Output: `/tmp/synth.out`
- Uses exact `Fraction` inputs; LP solved by `scipy.linprog`; numerical/evidence only.
