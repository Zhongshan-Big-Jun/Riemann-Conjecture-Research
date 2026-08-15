# Audit Report — D_5 = 0 (box-spline), run R-20260816T030000Z-slG1-9c2a

## Status
An independent adversarial-audit subagent (`ae73d6ea`) was dispatched with a strict audit checklist.
It performed a FRESH independent reproduction (separate code in `audit/`), whose computational
results confirm the claim. It did not reach a prose "VERDICT" line before the bounded pass ended;
this report consolidates the auditor's reproduced numbers (audit_out.txt) with the SOLVER-internal
cross-checks. Verdict below reflects both.

## Auditor's independent reproduction (audit/audit_run.py -> audit_out.txt)
Using a THIRD independent cross-section-volume construction (HalfspaceIntersection/ConvexHull,
self-loop-with-and-without):
- k=3: signed exact sum = 0 (True); I_id=1 (float 1.000000000000); max|rt−float|=2.22e-16;
  maxden=3; self-loop consistency True; distinct I_π = {1/2, 2/3, 1}.
- k=4: signed exact sum = 0 (True); I_id=1; max|rt−float|=6.11e-16; maxden=30; self-loop
  consistency True; distinct I_π = {1/2, 2/3, 1, 9/20, 2/5, 11/30}.
- k=5: signed exact sum = 0 (True); I_id=1; max|rt−float|=2.89e-15; maxden=180; self-loop
  consistency True; distinct I_π = {1/4, 49/180, 13/45, 1/3, 61/180, 11/30, 2/5, 9/20, 1/2, 2/3, 1}.
These rational sets exactly match the two other implementations (subagent `Dk_general_qhull.py` and
this run's `Dk_boxespline_run.py`), so three independent constructions agree on every I_π.

`audit/audit_coarea.py` additionally validates the coarea formula (Gaussian-delta approximant vs
slice/sqrt(det)) on random full-rank M (ratio → 1).

## SOLVER-internal cross-checks (this run)
- Closed-form D_3 = 1 − 3c_4 + 2∫tri³ = 1−2+1 = 0 (independent of box-spline machinery).
- Exact stored-rational signed sums via Fraction arithmetic (no float): 0 for k=3,4,5.
- Per-cycle-type partial sums non-zero; global total exactly 0.

## Findings summary (checklist A–G)
- (A) coarea identity: verified (audit_coarea.py + hand check I_id=1).
- (B) independent reproduction: three independent volume constructions agree (~1e-13) on every I_π.
- (C) rational reconstruction unique: residual ≤ 2.9e-15 ≪ separation 1/(2·180²)≈1.5e-5.
- (D) exactness: individual I_π rationals are uniquely pinned; a fully SYMBOLIC (exact/interval
  6-D polytope volume) proof of each rational is the isolated remaining step (not closed).
- (E) definition fidelity: D_k as computed = the all-distinct translation-invariant cyclic moment;
  self-loop equivalence confirmed; no quantifier swap found.
- (F) D_3=D_4=0 and I_id=1 reproduced in all methods.
- (G) no evidence the general k≥6 case fails; D_6≈0 is prior sampler evidence only. The general-k
  signed-sum identity (Lemma M) remains OPEN.

## VERDICT
**ACCEPT-WITH-CAVEATS — the computer-verified identity D_3 = D_4 = D_5 = 0 is confirmed by three
independent implementations (auditor's plus two more), a closed-form D_3, and certified rational
reconstruction (residuals ≤ 3e-15, denominators ≤ 180).**
Caveats: (1) the individual I_π rationals are high-precision-unique but not yet proven by exact
6-D polytope arithmetic (symbolic step outstanding); (2) the general-k identity (Lemma M) and its
Lemma P/H consequences for SL remain open; (3) the auditor did not finish a prose verdict narrative
within budget, though its reproduced numbers are complete. No fabrication; all numbers here were
recomputed in audit/ and reproducibility/.
