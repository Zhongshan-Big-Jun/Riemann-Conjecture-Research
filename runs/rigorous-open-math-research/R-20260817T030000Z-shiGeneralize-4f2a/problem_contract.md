# Problem contract — absorb Shi 0.673316977 and generalize the two-certificate method

- **Source**: yuhangshi888/zeta-simple-zeros-673316977 v0.1.0 (audited PLAUSIBLE-WITH-GAPS).
- **Task 1 (absorb/validate)**: register the candidate in the project's literature frontier,
  index, and formalization progress as an external candidate with audit status; do NOT mark
  it as an accepted theorem because the imported certificates/interface are not replayed and
  the Lean `hTrace` split is not formalized.
- **Task 2 (generalize)**: explore generalizations of the two-certificate trace-energy
  supporting-plane method to seek a strictly larger lower bound than 0.673316977… using the
  same certified inputs (or the candidate's quarantined extra certificate if it becomes
  usable). Concrete directions:
  1. Reproduce the candidate's closed-form scan and verify `m=219` is best for the
     seven+nine pair.
  2. Generalize the supporting-plane construction to more than two local inequalities
     (multi-certificate supporting plane), and solve the resulting finite-dimensional
     optimization (piecewise-affine/concavity).
  3. Search over the block length `m` and over which subset of certified pressures/targets
     can be combined.
  4. If a new candidate constant is found, pin it with exact rational checks and (if
     possible) a Lean scaffold for the new supporting-plane profile.
- **Completion criteria**:
  - absorption artifacts written (FRONTIER/index/status updates),
  - a generalization report with either a new candidate or an exact obstruction,
  - reproducibility scripts in the run directory.
- **Status discipline**: numerical scans are evidence, not proof; a new candidate is labeled
  `CANDIDATE` until independently audited.
