# Problem contract — Independent audit of Zenodo 22008814

- **Target**: Hu, C. & Chen, J., *A Hardy-Gauge Contour Method for Density One of Zeta Zeros on the Critical Line*, Zenodo DOI 10.5281/zenodo.22008814 (2026-08-19), 72 pp.
- **Main claim (Theorem 1.1)**: `N0,T/NT = 1 - o(1)` as `T → ∞`, hence `N0(T)/N(T) → 1` (density one of nontrivial zeros of ζ on the critical line).
- **Completion criteria**:
  1. Adversarial audit of the paper's proof structure, in particular the load-bearing sections §10–§15 (rank `o(NT)` stationary edge, relative Hilbert–Schmidt remainder `o(NT)`, finite-dimensional inertia reduction, perturbation/Rouché final step), with each obligation marked PROVEN / PLAUSIBLE / GAP / FAILED.
  2. Lean machine verification of a sample of the early structural lemmas (selected for both importance and feasibility):
     - §2.1/2.2 curvature identity `Z Z'' − Z'² = ½ ∂²_a[Z(s+a)Z(s−a)]|_{a=0}`;
     - §3.1 conjugate-pair residue block `[[0,w],[conj w,0]]` has eigenvalues `±|w|` (exactly one negative) for `w ≠ 0`.
  3. A written audit conclusion and an analysis report `reports/zenodo-22008814-analysis.md` with an explicit credibility assessment vs. our project (0.673066… record) and a recommendation.
- **Status discipline**: `INDEPENDENTLY_AUDITED_PROOF` only if every analytic obligation is independently verified; otherwise the honest label is `RIGOROUS_PARTIAL_RESULT` / `CANDIDATE` depending on findings. Numerical/formal evidence alone is never a completion.
