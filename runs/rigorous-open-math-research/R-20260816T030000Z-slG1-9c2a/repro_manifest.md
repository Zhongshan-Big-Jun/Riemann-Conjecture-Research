# Repro Manifest — R-20260816T030000Z-slG1-9c2a (SL gap G1)

## 1. Environment
- Python: `py -3.10` (Python 3.10.11), `$env:PYTHONUTF8=1` on Windows.
- numpy 2.2.6, scipy 1.15.3, mpmath 1.3.0, sympy 1.13.1.
- All scripts run with `py -3.10 <script>`.

## 2. Authoritative inputs (inherited, audited)
- SL reduction run `R-20260815T120000Z-sllemma-7b21e4` (candidate_proof, status_and_literature,
  problem_contract): SL ⟺ μ_λ({0})=0 ⟺ Λ_m(0)=det(H_m)/det(H_m^{(00)})→0. T0/T1 rigorous.
- Moment route run `R-20260815T130000Z-slmoments-a3f9` (validated projection-DPP sampler, Gates A/B
  PASS; D_3..D_6 evidence; Lemma M/P/H framework; Gap G1 = D_k=0).
- Probe report `reports/sl-lemma-random-gram-probe.md`: exact m_1..m_4 = (1,1,4/3,2,13/4), D_3=D_4=0.

## 3. Key objects
- K(x) = sinc(x) = sin(πx)/(πx), orthogonal projection (symbol 1_{[-1/2,1/2]}), K*K=K.
- ρ_k(x_1..x_k) = det[K(x_a,x_b)].  P_k = ∏_{a=0}^{k-1}K(x_a−x_{a+1}), x_k=x_0.
- D_k = Σ_{π∈S_k} sign(π) I_π,  I_π = ∫_{R^{k-1}}(∏_cycle K)(∏_a K(x_a−x_{π(a)})) dx_0..dx_{k-2}
  (x_{k-1}=0 pinned by translation invariance).

## 4. Reproducible scripts (all in reproducibility/, run from that dir or by absolute path)
- `D5_permutation_terms.py` — box-truncated per-π I_π for k=5 (evidence only; superseded).
- `D5_cycletype_analysis.py` — groups 120 terms by cycle type (evidence; global-cancellation).
- `Dk_general_qhull.py` — MAIN exact method: box-spline cross-section volume + rational
  reconstruction; writes D3/D4/D5_exact.json. Reproduces D_3=D_4=D_5=0.
- `certify_Dk.py` — audits the rational reconstruction (max |recon−float|/|I| ≤ 8e-15; signed
  rational sums = 0 for k=3,4,5).
- `Dk_boxespline_run.py` — INDEPENDENT method (coarea, self-loops dropped, vertex-enumeration 6-D
  hull), cross-check. D_3≈3e-10, D_4≈-3e-9, D_5=+1.6e-9 (noise-level 0).
- `crossvalidate_2methods.py` — verifies the two independent methods agree on sampled I_π to ~1e-13.
- `exact_D5_boxspline.py`, `D5_BOXSPLINE_REPORT.md` — compute subagent's polished method + report.
- `degree2_reduction.py`, `boxsection_volume.py`, `exact_vertices.py`, `D5_qhull_numeric.py` —
  supporting explorations.
- JSON outputs: `D3_exact.json`, `D4_exact.json`, `D5_exact.json` (per-π sign, √det, rational I_π,
  exact totals D_k=0), `D5_qhull_res.json`, `D5_boxspline_report.json`.

## 5. Literature locators (all from actual web_search returns; NOT fabricated)
- A. Soshnikov, "Gaussian limit for determinantal random point fields", Ann. Probab. 30 (2002)
  171–187; arXiv:math/0006037; Zbl 1033.60063. Lemma 1 eq.(14): cumulant of a DPP linear statistic
  = signed sum over block decompositions of cyclic kernel integrals.
- Soshnikov & Wu, "A Note on Cumulant Technique in Random Matrix Theory", Entropy 25(5):725 (2023),
  DOI:10.3390/e25050725; PMC10217726.
- Dappiaggi, Lechner, Morfa-Morales, arXiv:1006.3548 (quasi-free/CAR matching: odd vanish, even =
  products of two-point).
- Olshanskii, "DPPs and fermion quasi-free states", arXiv:2002.10723.
- Borodin–Olshanski–Strahov, "Giambelli compatible point processes", arXiv:math-ph/0505021,
  Zbl 1108.05093; Bufetov–Lazag, arXiv:2111.05606.
- Cunden–Majumdar–O'Connell, "Free fermions and α-determinantal processes", arXiv:1811.11556.
- Johansson–Lambert, arXiv:1504.06455 (Ann. Probab. 46 (2018)): higher DPP cumulants generally
  nonzero (honesty caveat).
- Biscio–Lavancier, arXiv:1507.06506; Heinrich, Kybernetika 52 (2016), Zbl 1488.60126
  (Brillinger-mixing: factorial cumulants decay, not vanish).
- Historical anchors checked (recorded, not re-verified full-text): Shirai–Takahashi
  (Zbl 1051.60052/3), Lyons–Steif (arXiv:math/0204325, Zbl 1068.82010), Hardy et al.
  (arXiv:1211.6564), Balslev–Verbeure (CMP 7 (1968)).

## 6. Unknowns / caveats
- The exactness of each individual reconstructed I_π rational rests on high-precision 6-D polytope
  volume + safe rational reconstruction (residual ≤8e-15, denominator separation ≥1.5e-5). A fully
  symbolic proof (exact/interval 6-D volume) of each rational is the isolated remaining verification
  step. Not claimed as a closed-form theorem.
- The general k≥6 identity (Lemma M) is NOT proven; D_6=0 is only numerical evidence (earlier pass).
- No fabricated run data; all subagent reports content-verified against the files/citations they cite.