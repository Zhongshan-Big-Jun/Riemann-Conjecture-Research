# Run report — R-20260816T040000Z-xipAtOne-3078

## Output-protocol status label
**`FINITE_COMPUTATIONAL_RESULT`** (math-level certificate), with the Lean honest-bridge module
**`MACHINE_ACCEPTED_PENDING_AUDIT`**.

Concretely:
- The **certified AtOne sandwich** for v_MT is established:
  `κ₉ ≤ κ₁(1, vMT) ≤ κ₉ + ε₉`,
  `κ₉ = (aMT + J1MT)/(IvMT)² = 1.132111133800997 ± 2·10⁻¹⁶`,
  `ε₉ = 1024/2990212875 = 3.424505…×10⁻⁷` (formally-verified D₁ tail).
- The canonical `κ₁(1,vMT) = 1.132111134800948064449685289579659686777429502383…` and
  `H_{ξ′} = 0.8678888651990519355503147104203403132225704976166306446…` lie **inside** the
  certified sandwich (contain-checks True); independent mpmath recomputation agrees to ~10⁻⁵⁶.
- Lean `Record9.XiPrimeAtOne` compiles (`lake build` exit 0); `#print axioms` = base only
  [propext, Classical.choice, Quot.sound]; no sorry/admit/axiom.

## What was delivered
- `reproducibility/atone_xip_mt.py` — the rigorous ARB certificate (exact closed forms +
  composite-Simpson with rigorous global M₄ bound; all bounds are ARB intervals = rigorous).
- `reproducibility/audit_kappa.py` — independent mpmath cross-check (EVIDENCE) confirming the
  sandwich contains the canonical values to ~56 digits.
- `machine_check.log` — recorded commands + exit codes.
- Standard artifact set (problem_contract, research_ledger, candidate_proof, repro_manifest,
  status_and_literature, obligation_graph, counterexample_log, whiteboard, audit_report,
  approach_registry, SHA256SUMS).
- Lean module `lean-proof/Record9/Record9/XiPrimeAtOne.lean`.
- `lean-proof/Record9/FORMALIZATION_STATUS_XIP.md` M3-open-A row updated.

## Exact remaining gaps (not closed, honest)
1. **M3-open-A formal (Lean):** promote to real lemmas the analytic facts currently carried as
   hypotheses — (a) `∫vMT = IvMT`, `∫vMT² = aMT`, (b) `vConv vMT = vConvMTcl` on [0,1],
   (c) Fubini `2∫₀¹ vConv vMT = (∫vMT)²`, (d) `0 < IvMT` (⟺ vConv vMT ≥ 0 on [0,1]),
   (e) `jWin(D1trunc 9,1,vMT) = J1MT` + the D₁-certificate jWin sandwich integral mechanics.
   All are elementary/known; math-verified this pass, formalized as hypotheses.
2. **M3-open-B:** the ξ′ chain `xiChain` (pressure method) — unchanged, open.
3. **M1-open-C:** the four §1 profile L¹-norms as Lean lemmas — unchanged, open.
4. Independent/adversarial review of the closed-form derivation (product-to-sum + Fubini) against
   [XF′ Thm 8.1] recommended for a formal audit of O5–O8.

## Anti-hiding
- κ₉ is NOT an exact rational for v_MT (∫vMT, aMT, vConv contain sin/cos of √2); it is a real
  number enclosed to ~10⁻¹⁶ (≪ ε₉).  This honest fact is stated explicitly (candidate_proof,
  whiteboard, problem_contract), not presented as an exact Rational.
- Quadrature = EVIDENCE; only the ARB interval enclosures are rigorous bounds.  Both labelled.
- Five reproducible implementation failures (F1–F5) are recorded with mechanisms and fixes.
