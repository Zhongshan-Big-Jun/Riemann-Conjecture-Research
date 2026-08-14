# Whiteboard — extpress-2f36ae

- **Run ID:** R-20260814T045000Z-extpress-2f36ae
- **Task packet ID:** Q-20260814-criticalline-p1-507bb5

## Current plan

k-point pressure method: certify F₈ ≥ f₈ for the largest certified f₈ and push the C₉ record.

## Route history

- k=9 pressure chain derivation (block-energy, block-defect, pinching/averaging) [SUCCEEDED]
- 22-worker spawn stall diagnosed; fixed with 8 workers [SUCCEEDED]
- k=9 certificate F₈ ≥ 39/10000 certified (53,137,290 nodes, kernel hash 7029ac0f…) [SUCCEEDED]
- NEW RECORD C₉ = 0.67305364595258992520 (closed form (6875·H_MT − 1315/96)/6849) [SUCCEEDED]
- Manager audit PASS-with-limits (numerical-evidence discipline enforced) [SUCCEEDED]

## Ideas to return to

- f₉ ladder: 0.00395 in certification (f9push-d3b58c); 0.00398 = infeasible (equality at
  true minimum F₈ ≈ 0.0039818).
- k=11 infeasible in this environment (10-var B&B, 8-worker limit; cost model recorded).

## Open obligations

- Independent audit of the 0.0039 certificate + record theorem (extpress precedent).

## Key artifacts

- runs/…/extpress-2f36ae/reproducibility/verify_kpoint_parallel.py (deterministic, --out)
- reports/linked-ladder.md, k11-feasibility.md
