# Problem contract — Audit of yuhangshi/zeta-simple-zeros-673316977

- **Target**: Yuhang Shi, *A two-certificate trace-energy deduction for simple zeros of the Riemann zeta function*, GitHub `https://github.com/yuhangshi888/zeta-simple-zeros-673316977` v0.1.0, Zenodo DOI 10.5281/zenodo.21926962.
- **Claim**: `liminf N_0^s(T,2T)/N(T,2T) ≥ 0.6733169771424713… > 673316977/10^9`.
- **Completion criteria**:
  1. Run the repository's local verification (`verify_release.py`, unit tests).
  2. Independently audit the finite-dimensional proof (Lemma 1 scaled envelope, Lemma 2 supporting plane, block assembly, global accounting, exact arithmetic).
  3. Verify the Lean formalization boundary: what is machine-proved and what remains hypotheses (`hTrace` spectral case split, imported certificates/interface).
  4. Write an audit report and an analysis report `reports/shi-673316977-analysis.md`.
- **Status discipline**: The result is a research-draft candidate; our audit will either mark it `INDEPENDENTLY_AUDITED_PROOF` (if the local layer is fully verified and imported inputs are accepted) or `RIGOROUS_PARTIAL_RESULT`/`CANDIDATE` with exact gaps.
