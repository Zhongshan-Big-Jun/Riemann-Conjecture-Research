# Repro manifest — R-20260816T080000Z-g2proof-a24d

## Environment

- OS: Windows (PowerShell)
- Python: `py -3.10` (numpy, scipy, sympy, mpmath; no networkx required)
- `$env:PYTHONUTF8=1`
- Project root: `F:\LaTeX\Riemann Conjecture`

## Inputs

- Upstream G2 rule run: `R-20260816T070000Z-g2rule-a1b2`
  - `reproducibility/allJ.json` (exact per-partition J, k=3..6, 275 rows)
  - `candidate_proof.md` §7 residual identity
- Upstream G1 run: `R-20260816T030000Z-slG1-9c2a`
  - box-spline/coarea exact engine and D_k=0 machinery

## Commands / checks

- Exact per-π decomposition (small cases): see `reproducibility/exact_contribs.py`,
  `explore_b4.py`, `explore_b4_detail.py`, `explore_signed_sum.py`.
- Rule/data checks: `reproducibility/rule_tests.py`, `final_rule.py`, `build_dataset.py`,
  `dataset.py`, `allJ.json`, `perJ_k{3,4,5}.json`.
- Killed-route checks: `reproducibility/degree2_reduction.py` (K2),
  `reproducibility/explore_signed_sum.py` / `b2b3_formulas.py` (K1).
- k=7 new-isoclass verification: `reproducibility/verify_k7.py`,
  `reproducibility/verify_k7_fast.py` (started, not completed in budget).

## Reproducibility note

The exact box-spline values quoted in `candidate_proof.md` §3.1 were re-derived with the
exact engine and are consistent with `allJ.json`. The k=7 verification scripts are included
for reproducibility but were not run to completion; this is recorded as `[PARTIAL]`.
