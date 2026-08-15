# Whiteboard — SL lemma (sine-process Gram spectral measure)

- **Run ID:** `R-20260815T120000Z-sllemma-7b21e4`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5`
- **Last updated:** `2026-08-15T22:55:00Z`

## Current plan

RUN COMPLETE (2026-08-15): RIGOROUS_PARTIAL_RESULT, external adversarial audit
PASS-CONDITIONAL. Deliverable: rigorous reduction of SL (the single open ingredient of the
conditional 100% theorem, condp1 run) to a pure moment-sequence statement. Next run steps
(not part of this run): (1) prove det(H_m)/det(H_m^(00)) -> 0 for the sine-Gram moment
sequence — closure route = fermionic/Wick conjecture D_k = 0 for all k >= 3 giving exact
high moments; (2) formalize the Christoffel-atom theorem + compact-support determinacy in
Lean; (3) high-precision/stable methods for large-order Christoffel values.

## Route history

- Literature pass 7 (10 queries) `[SUCCEEDED]`: no theorem states the random sine-Gram
  limiting spectral measure; new anchors Yaskov (least eig, i.i.d. only), Shawe-Taylor
  (Gram-vs-operator, i.i.d. only), Bonami-Karoui (sinc operator = projection, spectrum
  {0,1}), Johansson-Lambert (DPP linear statistics). status_and_literature.md.
- Reduction (T0) `[SUCCEEDED]`: SL (Christoffel form Lambda_m(0)->0) <=> mu_lambda({0})=0
  (Christoffel atom theorem, anchors Breuer-Last-Simon / Lagomasino-Marcellan-Van Assche);
  load-bearing-clause analysis: 0-in-supp NOT needed by the condp1 theorem — sharpening.
  candidate_proof.md section 1.
- Hankel criterion (T1) `[SUCCEEDED]`: Lambda_m(0) = det(H_m)/det(H_m^(00)); validated
  EXACTLY: Lambda_1(0)=1/4, Lambda_2(0)=5/36 from (1,4/3,2,13/4); model measures confirm
  Lambda_m->mu({0}). reproducibility/ scripts.
- Higher-moment probe (Step 4-6) `[FAILED]`: hand-rolled projection-DPP sampler does NOT
  reproduce the audited exact moments (m_2=1.798 vs 4/3) — sampler defective; result
  DISCARDED as evidence (discipline: no bad evidence). Trustworthy source = the probe's
  validated L=50 moments (reports/sl-lemma-random-gram-probe.md).
- External adversarial audit `[SUCCEEDED]` (fresh subagent 52d8d44d, no shared chain of
  thought): T1 HOLDS; T0a HOLDS-CONDITIONALLY (moment-determinacy, satisfied via compact
  support); m0-vs-m1 indexing objection rebutted with exact rational arithmetic (CS
  4 <= 13/3, Hankel det > 0, monotonicity 5/36 < 1/4). audit_report.md.

## Ideas to return to

- Exact m_5..m_8 shape decomposition via full rho_5/rho_6 determinants (52 set partitions
  for rho_5 — error-prone by hand; needs a computer-algebra pass) — would test D_k = 0.
- Shawe-Taylor transfer needs a DPP-vs-i.i.d. gap lemma — likely hard; not pursued.
- Operator-spectrum route: sinc kernel operator is a projection (spectrum {0,1}); the
  random-Gram measure is NOT the operator spectrum — indirect link only, recorded.

## Open obligations

- SL itself: prove lim_m det(H_m)/det(H_m^(00)) = 0 for the sine-Gram moment sequence
  (equivalently mu_lambda({0}) = 0) — the minimal missing ingredient (candidate_proof.md
  section 3, T2). Route: D_k = 0 for all k >= 3 (fermionic/Wick) -> exact moments -> Hankel
  ratio.
- Formalize Christoffel-atom theorem + compact-support determinacy (Lean, T4 optional).
- The condp1 100% theorem remains conditional on SL; unconditional liminf -> 1 OPEN.

## Key artifacts

- `runs/.../sllemma-7b21e4/problem_contract.md` -- SL contract rebuilt (object, lambda role, ambiguities); sha256 FB4A13E9...
- `runs/.../sllemma-7b21e4/status_and_literature.md` -- pass-7 search log + anchors + sharpening; sha256 3B182DAF...
- `runs/.../sllemma-7b21e4/candidate_proof.md` -- RIGOROUS_PARTIAL_RESULT: T0 reduction + T1 criterion + T2 open gap; sha256 DFCADCD2...
- `runs/.../sllemma-7b21e4/audit_report.md` -- adversarial audit verdict + rebuttal; sha256 D55A22A4...
- `runs/.../sllemma-7b21e4/research_ledger.md` -- chronological steps 0-8 incl. failed sampler; sha256 3E5D1680...
- `runs/.../sllemma-7b21e4/obligation_graph.md` -- T0/T1/T2/T3 graph; sha256 29658802...
- `runs/.../sllemma-7b21e4/approach_registry.md` -- routes A-F with states; sha256 8BB89D0F...
- `runs/.../sllemma-7b21e4/counterexample_log.md` -- tested edge cases + broken sampler record; sha256 ABC7B7D8...
- `runs/.../sllemma-7b21e4/repro_manifest.md` -- inputs/versions; sha256 CA9A59E6...
- `runs/.../sllemma-7b21e4/reproducibility/` -- 6 scripts (criterion checks, exact 5/36, decay fits, high-prec); see SHA256SUMS.
