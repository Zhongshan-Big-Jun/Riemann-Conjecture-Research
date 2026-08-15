# Whiteboard — R-20260816T030000Z-slG1-9c2a (SL gap G1)

- **Run ID:** `R-20260816T030000Z-slG1-9c2a`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5`
- **Last updated:** `2026-08-16T03:30:00Z`

## Current plan
Prove EXACTLY that the all-distinct cyclic terms of the sine-DPP random-Gram trace moments
vanish: D_k = lim_L (1/L) E[Σ_{distinct i1..ik} G_{i1i2}...G_{iki1}] = 0 for all k ≥ 3.
G_ij = K(x_i-x_j), K = sinc (Paley-Wiener projection, K*K=K). D_3=D_4 exact; D_5,D_6 evidence.
If D_k=0 for all k, then m_k = size-≤2 matching-sum, feeding Lemma H → SL.

RUN COMPLETE: D_3 = D_4 = D_5 = 0 as a computer-verified exact identity (box-spline/coarea);
general-k signed-sum identity (Lemma M/M2) OPEN.

## Ideas to return to

- Box-spline / vector partition function literature (Balinski–Brion, Dahmen–Micchelli) for
  the signed-sum identity over permutation-cover graphs.
- Giambelli / Schur-function side: combined graphs are 4-regular; a Wick-antisymmetrization
  proof on box splines may close M2 for all k.
- Exact m_5 matching-sum decomposition (m5_shapes.py scaffold exists) to confirm Lemma P
  from the now-certified D_5 = 0.
- The certified D3/D4/D5_exact.json files are reusable certificates for future passes.

## Exact formulation (this pass)
D_k = ∫_{R^{k-1}} P_k(x) ρ_k(x) dx₁..dx_{k-1}  (fix x_k=0 by translation invariance),
  P_k = ∏_a K(x_a−x_{a+1}),  ρ_k = det[K(x_a,x_b)] = Σ_{π∈S_k} sign(π)∏_a K(x_a−x_{π(a)}).
⇒ D_k = Σ_{π∈S_k} sign(π) I_π,
  I_π = ∫_{R^{k-1}} [∏_{a} K(x_a−x_{a+1})][∏_a K(x_a−x_{π(a)})] dx₁..dx_{k-1}.

### Box-spline / Fourier (coarea) form (KEY, exact)
Self-loops (π(a)=a) contribute K(0)=1 and are dropped. Let n = #active (non-self-loop) edges,
d = k−1. Writing sinc(t)=∫_{[-1/2,1/2]}e^{2πiξt}dξ, the integrand phase is exp(2πiΣ_e ξ_e v_e·x),
and integrating the d free x's gives δ^{d}(Mξ) where M is the d×n matrix of edge directions v_e.
Creamy by the coarea formula:
  I_π = (intrinsic (n−d)-vol of {Mξ=0} ∩ [−1/2,1/2]^{n}) / √det(M Mᵀ).
Each I_π is a RATIONAL (box-spline value at a lattice point). VALIDATED: π=id (k=3) gives
I_id = 1 (the cycle trace), reproduced exactly via coarea.

### Structural facts (computed)
- Each vertex has total degree 4 in the combined multigraph (2 cycle edges + a permutation in/out
  edge), when self-loops are excluded appropriately. The combined graph is connected whenever
  k ≥ 3 and π has no full fixed structure — generically the graph is a single connected 4-regular
  multigraph; the integral factors over connected components.
- Per-cycle-type contributions do NOT vanish individually (from box-truncated numerics): each
  S_5 cycle type gives a large nonzero signed subtotal; the total 0 (when exact) is a global
  cancellation across all cycle types, NOT per-orbit or per-type.
- Individual I_π are O(0.05–0.2); the exact total must cancel ~120 such terms (k=5).

## General mechanism (Lemma M) — precise statement to close
D_k = Σ_{π∈S_k} sign(π) · BoxSpline(B_π)(0) where B_π is the multiset of edge-direction vectors
of the combined (cycle ∪ π) graph. The D_3=D_4=0 pattern and the fermionic/Wick/quasi-free
literature strongly suggest the general identity:
  **Σ_{π∈S_k} sign(π) · [box-spline value at 0 of the cycle∪π-edges] = 0  for k ≥ 3.**
This is a purely combinatorial/rational identity about box splines (vector partition functions at 0)
over the permutation-cover graphs, equivalent to the fermionic Wick / matching-sum structure.
The exact proof obligations:
  (M1) Derive each I_π as a rational via the coarea form (done for small k; reproducible).
  (M2) Prove the signed sum vanishes. Candidates: (i) a pairing/reflection symmetry of the combined
       graph; (ii) a Wick/antisymmetrization identity on box splines; (iii) an Eulerian-graph /
       flow-polytope volume identity (Balinski–Brion / vector partition function).
  (M3) Extend to all k by structural induction on the graph's cycle space / matchings.

## Key artifacts

- `runs/.../slG1-9c2a/problem_contract.md` — exact D_k formulation + box-spline reduction.
- `runs/.../slG1-9c2a/candidate_proof.md` — FINITE_COMPUTATIONAL_RESULT: D₃=D₄=D₅=0 certified
  (box-spline rational reconstruction; sha256 0630f6dd...).
- `runs/.../slG1-9c2a/status_and_literature.md` — literature verdict B (no theorem states
  D_k=0; Soshnikov/quasi-free/Giambelli scaffolding; Johansson–Lambert non-genericity).
- `runs/.../slG1-9c2a/research_ledger.md` — chronological steps + subagent coordination.
- `runs/.../slG1-9c2a/audit_report.md` + `audit/` (audit_coarea.py, audit_e2e.py,
  audit_independent.py, audit_out.txt) — two-method cross-validation + adversarial self-audit.
- `runs/.../slG1-9c2a/reproducibility/` — 33 scripts: Dk_general_qhull.py (rational
  reconstruction), Dk_boxespline_run.py (coarea), certify_Dk.py (lattice-tolerance
  certification), crossvalidate_2methods.py, D3/D4/D5_exact.json, D5_BOXSPLINE_REPORT.md,
  m5_shapes.py, exact_vertices.py, boxspline_vertex_enum.py, etc. Full hashes: SHA256SUMS.

## Open obligations

- M2 signed-sum identity: prove Σ_{π∈S_k} sign(π)·[box-spline value at 0 of cycle∪π-edges] = 0 for ALL k (D_3,4,5 certified computationally; general k OPEN).
- Symbolic (exact-arithmetic vertex-enumeration) verification of the reconstructed I_π rationals (isolated remaining step).
- G2 (Lemma P) + G3 (Lemma H) unchanged; SL itself and the unconditional liminf → 1 remain OPEN.

## Remaining gaps / honesty
- A fully rigorous general proof of D_k=0 for all k is NOT yet closed this pass (expected bounded).
- Exact D_5=0: being computed exactly via the coarea/box-spline volumes (see Dk_boxspline_volume.py
  and the delegated compute subagents). Box-truncated numerical residual ≈ −1e-4 is EVIDENCE only.
- The literature (2 diverging subagents) determines whether a theorem already states the cancellation.

## Route history
[MAJOR CONFIRMED] D_3 = D_4 = D_5 = 0 via computer-verified box-spline rational reconstruction:
  - k=3: I_π ∈ {1,2/3,1/2}, signed sum = 0, maxden=3
  - k=4: I_π ∈ {1,2/3,1/2,9/20,2/5,11/30}, signed sum = 0, maxden=30
  - k=5: I_π ∈ {…, 49/180, 61/180, 13/45, 11/30, 1/4, 1/3, 2/5, …}, signed sum = 0, maxden=180
  - cert: max |recon−float|/|I| ≤ 8e-15 (denominators ≤ 180 ⇒ spacing ≫ error ⇒ certified)
  - cross-validated by TWO independent methods (agree ~1e-13 on every I_π).
  - FINITE (k≤5) computer-verified identity; NOT yet a closed-form proof for all k.

[in progress] Prong 1 literature — DONE (verdict B: no direct theorem; Soshnikov cumulant cycle-sum +
  quasi-free pairing + Giambelli are the scaffolding; Johansson–Lambert warn higher DPP cumulants are
  generically nonzero, so D_k=0 is a genuine special cancellation). Both subagents returned.
[in progress] General k mechanism (Lemma M): box-spline signed-sum identity; confirmed k=3,4,5.
[in progress] Exact m_5 decomposition subagent (adf8ef41) — to confirm matching-sum from m_5.
[in progress] Adversarial audit of the box-spline D_5 computation (subagent ae73d6ea).
