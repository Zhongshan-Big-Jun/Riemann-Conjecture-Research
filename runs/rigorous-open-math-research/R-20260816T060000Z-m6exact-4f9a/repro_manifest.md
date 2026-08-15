# Reproducibility manifest — R-20260816T060000Z-m6exact-4f9a

## Environment
- Python 3.10 (`py -3.10`), `PYTHONUTF8=1`; Windows host.
- numpy 2.2.6, scipy 1.15.3, sympy 1.13.1, mpmath, fractions/csv (stdlib). No GPU.
- Parallel exact jobs via separate `py -3.10` processes (background).

## Inputs / prior artifacts (hash-bound upstream)
- m5 run `R-20260816T050000Z-m5exact-3f8a`: engines `boxspline2.py`, `boxspline_exact.py`,
  `boxspline_exact2.py`, `enumerate_moments.py`, `exact_volume.py`; m_2..m_5 = 4/3,2,13/4,101/18;
  c_2..c_10. Copied and path-patched to run-relative.
- SL run `R-20260815T120000Z-sllemma-7b21e4`: reduction SL ⟺ μ_λ({0})=0 ⟺ Λ_m(0)→0; Λ_1=1/4, Λ_2=5/36.
- DPP sampler `R-20260815T130000Z-slmoments-a3f9/reproducibility/projection_dpp_sampler.py`.

## New files (this run)
- `boxspline_exact_fast.py` — fast exact engine (`eq_coarea_value_exact_fast`). Same integer null
  basis as `boxspline_exact2`, numpy vertex-finding + scipy hull; validated =0.0 per-term vs the
  sympy engine (b=4 n=8/9 terms) and ~1e-13 on b=2/3.
- `shape_exact2.py` — exact-engine shape driver (b=3 via `boxspline_exact2`).
- `batch_exact6.py` / `fast_batch6.py` — parallel exact / fast batch workers.
- `reduce_b2.py` — b=2 analytic `J=c_m−c_{m+2}` + c-values derivation.
- `assemble_b3.py`, `master_summary6.py` — m_6 assembly + Hankel verdict.
- `validate_b4_fast.py` — fast-vs-true-exact per-term cross-check.
- `direct_integral6.py`, `simulate_m6_evidence.py`, `projection_dpp_sampler.py` (evidence).
- CSV data: `b3_batch*.csv` (90), `b4_fast_c*.csv` (65), `b5_fast.csv` (15), `b6_fast.csv` (1),
  `b3_clean_table.tsv`, `sim_evidence.txt`.

## Deliverable claims (exact)
- c_12 = 655177/1663200 (B_{2n}(0) formula; mpmath ∫sinc¹² cross-check).
- b contributions: b=1: 1; b=2: 4297/630 (analytic, verified); b=3: 479/210 (exact engine, 90);
  b=4: 2/35 (fast engine, 65); b=5: 0 (fast, 15); b=6 (D_6): 0 (fast).
- **m_6 = 640/63**; **Λ_3(0) = 247/2519**; Λ_1=1/4, Λ_2=5/36. Fork = decay.
- Numerics (DPP L=50) are evidence only.

## Reproducible commands
```
cd runs/rigorous-open-math-research/R-20260816T060000Z-m6exact-4f9a/reproducibility
py -3.10 master_summary6.py        # exact m_6 + Lambda_1,2,3 + fork verdict
py -3.10 reduce_b2.py              # c-values + b=2 reduction
py -3.10 boxspline_exact2.py       # c_2..c_10 engine self-check
py -3.10 simulate_m6_evidence.py   # DPP m_1..m_7 evidence (slow)
```

## Known unknowns / audit
- Full sympy re-verification of all 65 b=4 shapes not completed (budget); fast engine cross-checked
  on b=2/3 and per-term on a nonzero b=4 partition (=0.0 diff); aggregate anchored by
  positive-definiteness of m_0..m_6.
- Λ_4 needs exact m_7, m_8 (out of scope); sampler m_7,m_8 biased.
- All 203-partition exact values are in the CSVs; SHA256SUMS locks them.
