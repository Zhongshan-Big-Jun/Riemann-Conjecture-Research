# Status and Literature — R-20260815T130000Z-slmoments-a3f9

Current problem status: **SL = μ_λ({0})=0 for the random sine-process Gram limiting spectral
measure**. This pass contributes a validated numerical/ecological lever toward the exact-moment
(fermionic–Wick) route. No literature change (the exact limiting spectral measure of the random
sine-Gram remains unstated in the literature, cf. pass 7b21e4 §1).

## 1. Literature anchors (unchanged, authoritative)
- Christoffel atom theorem Λ_m(x)→μ({x}): Breuer–Last–Simon (Zbl 1198.42021); Lagomasino–
  Marcellán–Van Assche (CMP 2014). Used in pass 7 as T0 (rigorous).
- Projection nature of the sinc kernel (K∘K=K, symbol 1_{[-1/2,1/2]}): Bonami–Jaming–Karoui
  (hal-00547220v3 / 1012.3881); Slepian DPSS/prolate theory. The idempotence is what collapses
  the graph-integrals and is the structural engine of the D_k cancellation.
- DPP background + Kulesza–Taskar DPP sampling (eigen-Bernoulli + volume sampling):
  arXiv:1207.6083. Used to build the FAITHFUL sampler (Gate A exact-joint + Gate B exact moments).
- Random-Gram / small-eigenvalue (Yaskov Zbl 1381.60024; Shawe-Taylor et al. Gram-vs-operator):
  i.i.d.-column models, not DPP; recorded in pass 7 as not directly applicable.

## 2. New technical content this pass
- The occupancy-kernel discretization correction: A_ij = h·sinc(x_i−x_j) (E[N]=L) reproducing the
  exact moments; the na??ve diag-1 kernel gives E[N]≠L and fails. This concretizes the probe's
  "projection-DPP discretization".
- Two-gate validation of the DPP sampler (exact-joint distribution + exact moments) — the standard
  to which any future D_k evidence must be held.
- D_5 ≈ 0 evidence (MC + exact-integral), consistent with the fermionic conjecture.
- Exact reduction of the all-distinct D_k to a box-spline / translation-invariant integral (and
  the explicit 4-D form for k=5).

## 3. Novelty / gap
The fermionic/Wick identity D_k=0 for the sine-Gram all-distinct terms is NOT in the literature
as a stated theorem (the random sine-Gram spectral measure itself is unstudied). The closest
structural facts (k-particle projection operator; Wick's theorem for Gaussian/free-fermion fields)
motivate but do not prove it. Recorded as the central open sub-conjecture (Lemma M).
