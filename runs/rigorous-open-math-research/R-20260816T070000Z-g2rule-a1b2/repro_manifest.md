# Reproducibility Manifest — R-20260816T070000Z-g2rule-a1b2

## Environment
- Python 3.10 (`py -3.10`), `PYTHONUTF8=1`, Windows host. stdlib only for the analysis
  (fractions, itertools, collections, math, csv, json, re); **networkx is NOT installed** — graph
  checks (components, isoclass canonicalization, degree sequences) implemented manually.
- Upstream box-spline engine uses numpy/scipy/sympy (present in the environment); reused verbatim
  from the m6 run.

## Inputs (hash-bound upstream artifacts, audited)
- `R-20260816T050000Z-m5exact-3f8a`: m_5=101/18; k=5 true value set {1,1/3,7/60,1/15,1/180,0};
  D_5=0 certified (G1); profile aggregates.
- `R-20260816T030000Z-slG1-9c2a`: D_3=D_4=D_5=0 exact; box-spline value sets; c-values.
- `R-20260816T060000Z-m6exact-4f9a`: exact per-partition k=6 CSVs (b3_clean_table.tsv,
  b4_fast_c0..4.csv, b5_fast.csv, b6_fast.csv); analytic b=2 (c_m−c_{m+2}); m_6=640/63;
  c_2..c_12; engines (boxspline_exact*.py, shape_exact2.py, enumerate_moments.py).

## New files (this run)
- `dataset.py` — partition enumeration, cycle-multigraph H_σ, c-values, k=6 loader (CSV + analytic).
- `dump_partitions.py` — exact per-partition J for k=3,4,5 via the audited engine → perJ_k3/4/5.json.
- `build_dataset.py` — canonical `allJ.json` (275 rows), corrects the 4 documented float-noise
  k=5 values via isoclass-determinism + certified D_5=0; verifies m_2..m_6.
- `survey_k6.py`, `abstract_k6.py`, `rule_tests.py` — k=6 grouping by (b,m,cyclomatic,deg-seq),
  isoclass determinism check.
- `final_rule.py` — the vanishing-rule checker over all 275 partitions (THE result: 100%).
- `b2b3_formulas.py` — b=2 closed form verification; b=3 value probe.
- `allJ.json` — the exact per-partition dataset (k=3..6), the reproducibility datum.
- Copied m6 CSVs + engines into `reproducibility/` (path-patched, run-relative).

## Reproducible commands
```
cd runs/rigorous-open-math-research/R-20260816T070000Z-g2rule-a1b2/reproducibility
py -3.10 dump_partitions.py 5      # exact per-partition J for k=3,4,5 (engine; expect float noise at k=5)
py -3.10 build_dataset.py          # canonical allJ.json + moment anchors m_2..m_6
py -3.10 final_rule.py             # vanishing-rule accuracy (expect 275/275, TP=167 TN=108)
py -3.10 rule_tests.py             # (b,m,cyclomatic,degseq) table + isoclass determinism
py -3.10 b2b3_formulas.py          # b=2 closed form + b=3 probe
py -3.10 survey_k6.py / abstract_k6.py   # diagnostics
```

## Deliverable claims (exact / verified)
- **Vanishing rule (G2):** J_σ=0 ⟺ H_σ disconnected or m ≤ 2b−3; nonzero ⟺ connected & m ≥ 2b−2.
  Verified 100% (275/275; TP=167, TN=108, FP=0, FN=0) on exact k=3,4,5,6 data.
- Moments reproduced exactly: m_2=4/3, m_3=2, m_4=13/4, m_5=101/18, m_6=640/63.
- b=2 closed form J=c_m−c_{m+2} confirmed on all b=2 partitions (m=2,4,6).

## Known unknowns / honest limits
- General-k PROOF of the rule is NOT complete (this bounded pass); exact residual identity is
  stated in candidate_proof §7 (M1 disconnected-factorization, M2 low-surplus telescoping).
- Closed c-combination formulas for b≥3 nonzero J values are not pinned (values are exact and
  table-driven in allJ.json).
- k=5 per-partition exact values rely on the audited m5 value set + isoclass-determinism; the 4
  corrected values are documented in build_dataset.py and the ledger (none alters m_5=101/18).
- No numerical evidence is used as proof; all rule claims are exact-rational checks.
