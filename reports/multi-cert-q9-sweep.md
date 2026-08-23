# Synthetic q=9 / k=10 operating-point sweep in the multi-certificate LP

Status: **NUMERICAL_EVIDENCE** — all q=9 certificates below are SYNTHETIC and NOT
certified. This scan estimates how strong a future k=10 (q=9) operating point
would need to be to improve the existing two-certificate Shi bound.

Run date: 2026-08-23.

## Results

| scenario | best m | B | tau_q9 |
|---|---:|---:|---:|
| baseline retuned 7+9 | 219 | 0.673316977142471313 | 0 |
| q9 canonical p=1/4500, eps=0.00395 | 219 | 0.673316977142471314 | 0 |
| q9 p=1/4500, eps=0.00400 | 219 | 0.673316977142471314 | 0 |
| q9 p=1/4500, eps=0.00420 | 238 | 0.673318429680808739 | 1.65e-5 |
| **q9 p=1/4500, eps=0.00450** | **377** | **0.673387327683340215** | **4.39e-5** |
| q9 p=1/4000, eps=0.00420 | 219 | 0.673316977142471313 | 0 |
| q9 p=1/3500, eps=0.00420 | 219 | 0.673316977142471313 | 0 |
| q9 p=1/3000, eps=0.00450 | 219 | 0.673316977142471313 | 0 |

## Interpretation

- A **canonical k=10** point (`p=1/4500`, `eps≈0.00395`) is **not useful** in this LP.
- A k=10 operating point with `eps≈0.00420` starts to matter only slightly (`+1.45e-6`).
- A strong k=10 point with `eps≈0.00450` would improve the Shi bound to about
  `0.67338732768334` (about `+7.04e-5`).
- Therefore, a future k=10 certificate is potentially valuable **only if it is
  a retuned/strong operating point**, not the canonical general-k
  `F_9 ≥ f_10` with `f_10 ≈ 0.00395`.

## Reproducibility

- Script: `runs/.../R-20260817T030000Z-shiGeneralize-4f2a/reproducibility/multi_cert_q9_sweep.py`
- Output: `.../multi_cert_q9_sweep.out`
- LP via `scipy.linprog`; all certificate inputs exact `Fraction`s; numerical/evidence only.
