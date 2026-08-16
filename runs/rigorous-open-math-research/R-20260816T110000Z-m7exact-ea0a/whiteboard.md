# Whiteboard — R-20260816T110000Z-m7exact-ea0a

- **Run ID:** `R-20260816T110000Z-m7exact-ea0a`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5`
- **Project:** `F:\LaTeX\Riemann Conjecture`
- **Last updated:** `2026-08-16T12:30:00Z`

## Run ID / Task packet ID
- Run ID: `R-20260816T110000Z-m7exact-ea0a`
- Task packet ID: `Q-20260814-criticalline-p1-507bb5` (SL exact m₇/m₈ and Λ₄)

## Current plan
Compute exact m₇ (and m₈ if budget permits) for the sine-DPP Gram moment sequence using G2
pruning + the fast-exact box-spline engine; then compute Λ₄(0) and test Hankel decay.

## Route history
- Setup and environment check `[SUCCEEDED]`.
- k=7 pruning `[SUCCEEDED]`: Bell(7)=877 → 540 survivors (1 b=1, 63 b=2, 266 b=3, 210 b=4); 337 pruned.
- H-isoclass collapse `[SUCCEEDED]`: 540 survivors → 18 isoclasses (1 b=1, 3 b=2, 6 b=3, 8 b=4).
- k=8 preflight `[SUCCEEDED]`: Bell(8)=4140 → 2683 survivors → 46 isoclasses; full m₈ judged NOT feasible in budget; partial b≤2 contribution m₈^(b≤2) = 3724369/181440 computed.
- Exact m₇ computation `[IN PROGRESS]`: 7/18 isoclasses completed (b=1, b=2 all, b=3 m=4,5,6); b=3 m=7 and b=4 pending.

## Ideas to return to
- Finish b=3 m=7 and b=4 isoclasses; sum to exact m₇.
- Compute Λ₄(0) from m₀..m₇ (or m₈ if needed).
- If m₈ full is infeasible, use the partial m₈^(b≤2) plus rigorous bounds for b≥3 as evidence.

## Open obligations
- Exact m₇ completion.
- Λ₄(0) and decay comparison Λ₄ < Λ₃ = 247/2519.
- Full m₈ remains open (b≥3 classes heavy).

## Key artifacts
- `reproducibility/prune_k7.py`, `k7_survivors.json`, `compute_k7_exact.py`, `k7_iso_results.json`, `compute_k8_partial.py`, engines.
- `problem_contract.md`, `research_ledger.md`, `repro_manifest.md`.

## Remaining gaps / honesty
- Exact m₇ not yet complete; partial results are exact where recorded.
- m₈ full computation is infeasible in this bounded pass; partial b≤2 contribution only.
