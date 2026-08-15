# reproducibility/ — audit trail for run R-20260816T030000Z-slG1-9c2a

## Authoritative scripts (used for the confirmed results; cite these)
- `Dk_general_qhull.py` — MAIN method: exact box-spline/cross-section volume + rational
  reconstruction; writes D3/D4/D5_exact.json; reproduces D_3=D_4=D_5=0 (sig_num sums).
- `certify_Dk.py` — audits rational reconstruction (max |recon−float|/|I| ≤ 8e-15; signed sums 0).
- `Dk_boxespline_run.py` — INDEPENDENT method (coarea, self-loop exclusion, vertex-enumeration 6-D
  hull); cross-checks D_3≈3e-10, D_4≈−3e-9, D_5=+1.6e-9.
- `crossvalidate_2methods.py` — confirms the two independent methods agree on sampled I_π (~1e-13).
- `exact_D5_boxspline.py` + `D5_BOXSPLINE_REPORT.md` — polished combined method + report.
- `D5_permutation_terms.py`, `D5_cycletype_analysis.py` — box-truncated evidence only (superseded;
  guards against using truncation as proof).

## Supporting / exploration (process audit, not required for the result)
`boxsection_volume.py`, `exact_vertices.py`, `D5_qhull_numeric.py`, `degree2_reduction.py`,
`Ipi_structure.py`, `m5_shapes.py` (flawed multiplicity, counterexample_log item 8), and the
`_*.py` scratch files. Kept to document the derivation and the dead-ends (counterexample_log.md).

## JSON outputs (exact per-π values, reproduced by the authoritative scripts)
`D3_exact.json`, `D4_exact.json`, `D5_exact.json` (per-π: [sign, √det(VVᵀ), rational I_π];
top-level D_k exact total and float total), `D5_qhull_res.json`, `D5_boxspline_report.json`.

## Reproduce
Windows + `py -3.10`, `$env:PYTHONUTF8=1`, numpy 2.2.6 / scipy 1.15.3 / mpmath 1.3.0 / sympy 1.13.1.
E.g. `py -3.10 Dk_general_qhull.py` then `py -3.10 certify_Dk.py`.
