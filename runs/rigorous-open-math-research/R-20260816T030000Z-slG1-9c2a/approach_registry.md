# Approach Registry — SL gap G1 (D_k = 0), run R-20260816T030000Z-slG1-9c2a

Routes explored this bounded pass, with owners, states, and exact gaps.

| Route | Owner | State | Exact gap / result |
|---|---|---|---|
| R1 Literature (quasi-free/fermion/CAR) | subagent 951e7118 | DONE | No direct theorem; quasi-free/CAR matching verified (Dappiaggi et al.), Giambelli; D_k=0 NOT stated. Verdict B. |
| R2 Literature (DPP trace moments/matching) | subagent f0978f70 | DONE | Soshnikov cumulant cycle-sum (Lemma 1 eq.14 / Entropy 25:725) gives the cyclic-block structure; no D_k=0 statement; Johansson–Lambert warn higher DPP cumulants nonzero ⇒ D_k special. Verdict B. |
| R3 Box-spline/coarea exact D_5 | this run + subagent b6da73dc | DONE | D_3=D_4=D_5=0 as computer-verified rational sum (two independent methods, certified to ~8e-15). Finite k≤5. |
| R4 Box-truncated per-permutation numerics | this run | SUPERSEDED | Individual I_π ≈ 0.1–0.2; global cancellation only; box-truncation residual not a proof. |
| R5 Vertex-enumeration polytope volume | this run | DONE (cross-check) | Confirmed D_5≈0 (+1.6e-9 noise); used to cross-validate R3. Qhull 6-D fragility handled by cascading dedup/options. |
| R6 General k Lemma M (box-spline signed-sum identity) | this run | OPEN | Σ_{π∈S_k} sign(π)·[box-spline of cycle∪π] = 0 for all k. Proven for k=3,4,5; general proof (exact (M1) done, signed-sum (M2) unproven). |
| R7 Exact m_5 via shape decomposition | subagent adf8ef41 | IN PROGRESS | To confirm m_5 = size-≤2 matching-sum given D_5=0. |
| R8 Degree-2 convolution reduction | subagent b6da73dc | EXPLORED | Convolution-collapse (K*K=K) reduces degree-2 vertices; combined graph is 4-regular (no degree-2), so no trivial collapse; recorded as dead-end for the signed sum. |
| R9 Matching-sum / Giambelli bridge for Lemma P | OPEN | — | Need: prove m_k = Σ_{size-≤2 blocks} ∏c_{2t} from D_k=0 + the full repeated-index algebra. Not closed this pass. |

## Open obligations (from R6/R9)
- Prove Σ_{π∈S_k} sign(π)·[box-spline value] = 0 for ALL k (Lemma M general proof).
- Prove each reconstructed I_π rational is the exact box-spline value (exact/interval 6-D polytope
  volume) — the isolated remaining verification step for the finite k≤5 result.
- Match D_3..D_5 exact to the size-≤2 matching-sum for m_3..m_5 (Lemma P) and its Hankel decay (Lemma H).
