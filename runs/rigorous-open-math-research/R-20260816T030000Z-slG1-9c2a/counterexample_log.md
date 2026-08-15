# Counterexample Log — SL gap G1 (D_k = 0), run R-20260816T030000Z-slG1-9c2a

Edge cases, failed lemmas, dead-ends, and attempted disproofs of D_k = 0. Every negative route is
recorded for reuse.

## 1. Fixed-lattice / Toeplitz model (not this DPP) — KNOWN from probe (run 7b21e4)
The fixed-lattice Gram (sinc(i−j))_{i,j} = identity (sin(π·integer)=0) → μ=δ₁, moments all 1.
Eliminated as the wrong model; the random sine-DPP Gram is the correct identification.
(Not re-tested this pass; recorded here for completeness.)

## 2. Per-cycle-type / per-orbit pairing as a proof route — REFUTED (this pass)
Attempted: prove D_k=0 by pairing equal-I_π permutations (dihedral orbits) or by per-cycle-type
cancellation. RESULT: every cycle-type signed partial sum is NONZERO (e.g. k=5: (5)=+61/9,
(1,4)=−34/3, (2,3)=−55/9, (1,1,3)=+10, (1,2,2)=+19/3, (1,1,1,2)=−20/3, id=+1) and only the TOTAL
over all 120 permutations is 0. ⇒ No per-type/per-orbit pairing proof exists; cancellation is global.
Files: D5_cycletype_analysis.py, D5_permutation_terms.py, Dk_general_qhull.py.

## 3. Degree-2 convolution-collapse as full reduction — REFUTED (this pass)
Attempted: integrate out variables by K*K=K (degree-1 and degree-2 vertex collapse) to reduce each
I_π to an empty core. RESULT: the combined (cycle ∪ π) graph is 4-REGULAR (every vertex has 2 cycle
edges + 2 permutation-bit edges), so there is no degree-2 vertex to collapse; no trivial exact
collapse. File: degree2_reduction.py.

## 4. Box-truncated direct quadrature as exact evidence — REJECTED (this pass)
Box-truncated sinc-integral quadrature gives residual ≈ −1e-4 to +5e-4 that oscillates with box size
(R=4,6,8) and does not converge to 0 (it is truncation noise, not the exact 0). Moreover the compute
subagent found box-truncated 4-D quadrature under-converges badly (2/3 → 0.119 for one term). ⇒
Box-truncated numerics are NOT valid evidence; only the truncation-free box-spline route is valid.
Files: D5_permutation_terms.py, D5_BOXSPLINE_REPORT.md §4.

## 5. Attempted rational-obstruction for k=5 (would D_5 fail to be 0?)
Asked whether the signed box-spline sum could fail to vanish for k=5. RESULT: it vanishes exactly
(0). No obstruction found for k=5; the finite pattern D_3=D_4=D_5=0 is confirmed. Whether k≥6 fails
is an OPEN question (no evidence of failure; D_6 ≈ 0 evidence from the earlier validated sampler).
File: candidate_proof.md §7.

## 6. Qhull numerical fragility in 6-D (implementation, not math) — HANDLED
ConvexHull over enumerated 6-D vertices hit QH6271 wide-merge/topology errors; handled by
cascading dedup precision (9→4 decimals) and hull options (Qt/Q12/QJ), with cross-validation against
a second independent construction. RESULT: no spurious values; D_5 robust at +1.6e-9 (noise-level).
File: Dk_boxespline_run.py, crossvalidate_2methods.py.

## 7. False assumption: "quasi-free ⇒ higher DPP cumulants vanish"
Checked against literature: Johansson–Lambert (arXiv:1504.06455) and Brillinger-mixing (Biscio–
Lavancier; Heinrich) show higher cumulants/connected correlations of DPP linear statistics are
generically NONZERO. ⇒ D_k=0 is a genuine special cancellation, not an automatic corollary of the
quasi-free/Gaussian structure. This prevents an overstatement of Prong 1. File:
status_and_literature.md §1 "Critical honesty caveats".

## 8. Quick m_5 multiplicity attempt — FLAWED (quick check, not used)
Quick attempt (m5_shapes.py) to get m_5 = 1 + repeated-index shapes with multiplicity
∏(block-size)! gave m_5 ≈ 474, clearly wrong (validated-sampler m_5 ≈ 5.4). The multiplicity of an
ordered 5-tuple pattern in E[tr(G^5)] is NOT ∏(block-size)!; the correct DPP counting is subtler.
Usable result: D_5=0 (confirmed) contributes nothing; exact m_5 deferred to the shape-decomposition
subagent (adf8ef41) which uses the proper factorial-moment counting. This flawed quick path is
recorded, not used.

## Conclusion of the counterexample search
No counterexample to D_k=0 (k=3,4,5) found; the exact base cases are confirmed 0. The general-k and
Lemma P/H parts remain open, with the precise statements in obligation_graph.md.
