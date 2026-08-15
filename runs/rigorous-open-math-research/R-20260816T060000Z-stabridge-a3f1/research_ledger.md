# Research ledger — R-20260816T060000Z-stabridge-a3f1

Run ID: `R-20260816T060000Z-stabridge-a3f1`. Task: pin the T1c-1/T1c-2 bridge statements
(Step C), same pattern as the kernel-limit pass. Timestamps in Z.

## 2026-08-16

- **06:02 — Scope read.** Read authoritative context: `proof.md` (§2 Lemma 2.1 Ψ; §3; §4
  block-defect + averaging), `candidate_proof.general-k-derivation.md` (§1–§6), `Chain9.lean`
  (`stability_eps`, `stability_averaged_eps`, `record9Bridge`, `deltaMT` placeholder),
  `FORMALIZATION_STATUS.md`, snapshot `Defs.lean` (`Gentry`/`Gsummand`/`Gz`, tile/hat scales),
  `ZeroSide/{Mult,RankTraceMult}.lean`, `ThmD/{AssemblyD,Mult}.lean` (`mult_two`,
  `N0star_lower_c`, `thmD_mult2_abstract`), `LinAlg/{RankTrace,HermitianPosPart,PosIndex,
  VonNeumann,Sylvester}.lean`.
- **06:10 — Base flow understood.** Theorem D `S ≥ H_MT·N − o(N)` is the hat-unit `mult_two`
  + trace/fr bounds (`N0star_lower_c`); the `+Δ(M°)` refinement is the OpenAI addition that
  the snapshot's leak-free `rank_trace_mult_k_le` *drops*. So T1c-1 is a genuine (non-mech.)
  new analysis step + a new Lean obligation; not a reuse of the machine-proved ThmD verbatim.
- **06:20 — Normalization crux found.** Computed (numerically) that the raw/hat-unit
  off-diagonal squares relative to `wMT(x)` diverge like `(K(0)/(aL))²` (→0), so the hat-unit
  Gram does NOT give `Σ|G_ij|² = (1/2)E_m`. The **unit-normalized (correlation) Gram** does
  (all atoms share ‖v_γ‖² = L·F_L(0)). Also: hat-unit `tr Ψ(Â) ≈ S` (numerically implied),
  which would break Cor 2.2 (`S ≥ 0.67N+S` impossible). → Resolution: Δ(M°) is the
  correlation-Gram `tr Ψ`, documented as an explicit ambiguity (never silently chosen).
- **06:30 — Lemma 2.1 re-derived.** `min_n[(p−n)²+4n] = 2p−1+Ψ(p)` exact; assembly via
  Q=Q₊−Q₋, ‖Q₊‖²≥4trQ₊−4b, von Neumann, spectra-agreement, trP≤r ⇒ `‖P+Q‖² ≥
  4tr(P+Q)−3r−4b+trΨ(M)` (matches mainpush Entry 3).
- **06:35 — Sub-lemma decomposition locked.** T1c-2a (block energy), T1c-2b (defect lemma +
  A₀<1 → 2Σ branch), T1c-2c (pinch/averaging → defect numbers), T1c-2d (analytic
  uniformity Σ|G_ij|²=(1/2)E_m+o(1) via kernel-limit).
- **06:40 — Numerical checks.** `stabridge_checks.py` (15/15 PASS: Ψ continuity, min_n
  identity, Lemma 2.1 on random (d,r,b), defect lemma, exact constants, window counting,
  correlation energy ratio, branch logic). `stabridge_sublemma.py` (6/6 PASS: block energy,
  offset coefficient, A₀/m). Evidence only.
- **06:45 — Artifacts written.** problem_contract, candidate_proof (§7 ambiguity), whiteboard,
  counterexample_log, repro_manifest, SHA256SUMS, reproducibility/ scripts + run logs.

Decisions not yet needed: Lean formalization deferred (follow-up lean-verify), T2 certificate
out of scope.
