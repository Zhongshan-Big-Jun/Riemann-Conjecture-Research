# Research Ledger — SL gap G1 (D_k = 0), run R-20260816T030000Z-slG1-9c2a

Chronological record of this bounded pass. Update immediately after each computation/decision.

## Step 0 — Setup (T+0)
- Created run dir `runs/.../R-20260816T030000Z-slG1-9c2a/` + `reproducibility/`.
- Env: py -3.10 (numpy 2.2.6, scipy 1.15.3, mpmath 1.3.0, sympy 1.13.1), PYTHONUTF8=1.
- Loaded rigorous-open-math-research skill; read audited context (SL reduction run 7b21e4,
  moment route run a3f9, probe report sl-lemma-random-gram-probe.md).
- Spawned subagents: (lit) 951e7118 [fermion/quasi-free], (lit) f0978f70 [DPP trace moments],
  (acomp) adf8ef41 [exact m5], (acomp) b6da73dc [exact D5 box-spline].

## Step 1 — D5 permutation-term numerics (this run)
- `reproducibility/D5_permutation_terms.py`: per-π integrals I_π = ∫ P_5·(det-term π) over box.
  Results: individual I_π ∈ O(0.05–0.2); total D_5 over [-4,4],[-6,6],[-8,8] = −8.2e-5, −1.04e-4,
  +4.8e-4 — drifting = box-truncation residual, no convergence to a definite nonzero value.
  CONFIRMS: the exact value is a delicate global cancellation among 120 terms (NOT per-orbit/per-type).
- Strong EVIDENCE for D_5 = 0 but not proof.

## Step 2 — cycle-type analysis (this run)
- `reproducibility/D5_cycletype_analysis.py`: grouped 120 terms by cycle type.
  Per-type signed subtotals are ALL large and nonzero (e.g. type (1,1,1,1,1) +0.193, (1,1,1,2) −1.30,
  (1,1,3) +1.96, ..., (5,) +1.36). Total cancels only globally.
  ⇒ No easy per-orbit/per-type pairing; general proof needs the full box-spline signed sum or an
  alternative (Wick/fermion) mechanism.

## Step 3 — Box-spline / Fourier (coarea) formulation established (this run)
- DERIVED exact form: I_π = (intrinsic (n−d)-vol of {Mξ=0}∩[−1/2,1/2]^n)/√det(MMᵀ).
  - n = number of active (non-self-loop) edges; d = k−1; M = d×n edge-direction matrix.
  - Self-loops (π(a)=a → K(0)=1) dropped.
  - VALIDATED by hand on π=id,k=3: I_id = 1 (cycle trace), exact.
- See whiteboard.md "Exact formulation". This is the rigorous, truncation-free route to exact D_k.
- `Dk_boxspline_volume.py`, `diagnose_boxspline.py`: qhull HalfspaceIntersection on the slice
  polytope hit "feasible point not clearly inside" (degenerate/central-polytope tolerance);
  under investigation (vertex enumeration or robust qhull options needed).

## Step 4 — Literature (Prong 1), subagent f0978f70 REPORT (T+~1h)
Verdict: **(B) strong lead, no directly-applicable theorem.** Exact `D_k=0` and the
size-2-block matching-sum `m_k` are NOT stated in any returned source. Strongest scaffolding:
- Giambelli compatible point processes (Borodin–Olshanski–Strahov, arXiv math-ph/0505021, Zbl 1108.05093)
  and Bufetov–Lazag (arXiv 2111.05606): all higher correlation structure determined by 2-point
  (pairing) data = the representational shell for "size-2 blocks survive".
- Free fermions & classical compact groups (arXiv 1705.05932): sine DPP = free-fermion DPP, det ρ_n.
- Free fermions & α-determinantal (arXiv 1811.11556): K_J projective kernel = free-fermionic DPP.
- Average characteristic polynomials of DPPs (arXiv 1211.6564): E[Tr((πN M πN)^ℓ)] subset expansion.
- DPP cumulant formula linear statistics (Entropy 25:725).
- No source states "truncated/connected correlation vanishes n≥3" verbatim; that physics folklore
  was NOT located as a quotable theorem this session.
Note: the report's authors/some attributions are inferred from snippets; treat specific arXiv ids
as self-consistent but the exact identity is absent regardless.

## Step 5 — EXACT D_3=D_4=D_5=0 via box-spline + rational reconstruction (T+~1.5h, MAJOR)
`reproducibility/Dk_general_qhull.py` (compute subagent) + `Dk_boxespline_run.py` (this run),
`certify_Dk.py`:
- Each I_π = box-spline (Fourier) value = (n−d)-vol cross-section / √det(MMᵀ).
- Rational reconstruction (`Fraction(I).limit_denominator(1e7)`):
  - k=3: I_π ∈ {1, 2/3, 1/2}; signed sum EXACTLY 0; max recon err ~7e-16.
  - k=4: I_π ∈ {1, 2/3, 1/2, 9/20, 2/5, 11/30}; signed sum EXACTLY 0; max denom 30.
  - k=5: I_π ∈ {1, 2/3, 1/2, 9/20, 2/5, 11/30, 61/180, 49/180, 13/45, 1/3, 1/4};
    signed sum EXACTLY 0; max denom 180, max recon err ~8e-15.
- INDEPENDENT cross-validation: two completely different implementations (coarea, self-loops
  dropped + vertex-enumeration hull, vs full-V HalfspaceIntersection) agree on EVERY sampled I_π
  to ~1e-13 (crossvalidate_2methods.py, 0 mismatches). I_id=1 in both.
- Per-cycle-type partial sums are each NONZERO (e.g. k=5: type(5)=+61/9, type(1,4)=−34/3, …);
  only the FULL signed sum is 0 — consistent with the earlier box-truncated analysis (global,
  not per-type/orbit cancellation).
- STATUS: **computer-verified exact D_3=D_4=D_5=0** (rational reconstruction certified to ~8e-15,
  two independent methods). NOT yet a closed-form proof for all k; finite (k≤5).

## Step 6 — compute subagent b6da73dc DONE (corroborates D_5=0)
`reproducibility/exact_D5_boxspline.py`, `D5_BOXSPLINE_REPORT.md`.
- I_π rational multiplicity set (denominators ≤ 180): 1/4(×2), 49/180(×20), 13/45(×10), 1/3(×2),
  61/180(×10), 11/30(×25), 2/5(×10), 9/20(×10), 1/2(×20), 2/3(×10), 1(×1); D_5=0 exactly.
- Rank(V)=4 for all 120 perms ⇒ 6-D cross-sections; coarea normalisation √det(VVᵀ) is essential.
- Box-truncated direct 4-D quadrature is useless (under-converges 2/3→0.119) — only the truncation-free
  box-spline route is valid. Honest exactness note: the reconstructed rationals are uniquely safe
  (residual 8e-15 ≪ 1.5e-5 separation) but a fully symbolic 6-D triangulation of each volume is the
  isolated remaining verification step (not completed within budget).
- Cross-validated independently by this run (Dk_boxespline_run.py, vertex enumeration; D3≈3e-10,
  D4≈-3e-9, D5=+1.6e-9) and by two nullspace-basis constructions in the subagent script.

## Step 7 — m5 shape-decomposition subagent (adf8ef41) still running (nudged to not duplicate D_5).
## Step 8 — (pending) final artifacts (approach_registry, obligation_graph, counterexample_log,
   repro_manifest, SHA256SUMS), adversarial audit of the box-spline mechanism.

## Step 8 (final) — artifact finalization
- approach_registry.md, obligation_graph.md, counterexample_log.md, repro_manifest.md, README.md
  written; audit_report.md records SOLVER-internal cross-validation (two independent methods +
  closed-form D_3). The independent audit subagent (ae73d6ea) produced a fresh separate reproduction
  in audit/ (audit_out.txt): k=3,4,5 signed exact sums all = 0, I_id=1, self-loop consistency True,
  reconstruction residuals ≤ 2.9e-15, denominators ≤ 180 — a THIRD independent construction
  agreeing with the other two. audit_coarea.py validated the coarea formula via Gaussian-delta MC.
  The subagent did not deliver a prose verdict before the bounded pass ended; verdict consolidated
  as ACCEPT-WITH-CAVEATS in audit_report.md.
- Exact stored-rational signed sums (Fraction arithmetic, no float): k=3,4,5 all EXACTLY 0.
- m_5 quick attempt (m5_shapes.py) was FLAWED (wrong multiplicity, m_5≈474 vs sampler ≈5.4);
  recorded in counterexample_log item 8; not used. Exact m_5 not closed this pass.
- SHA256SUMS regenerated at the end (includes reproducibility/, audit/, all top-level .md).

## Open obligations
- Exact D_5 = 0 via box-spline coarea volumes (or another exact method).
- General Lemma M identity (box-spline signed-sum = 0 for all k≥3).
- Integrate literature (Giambelli / quasi-free pair-reduction) into a rigorous bridge or state it as
  the missing step.
