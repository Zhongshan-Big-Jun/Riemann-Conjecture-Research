# Whiteboard — R-20260816T110000Z-m7exact-ea0a

- **Run ID:** `R-20260816T110000Z-m7exact-ea0a`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5`
- **Project:** `F:\LaTeX\Riemann Conjecture`
- **Last updated:** `2026-08-16T14:00:00Z`

## Run ID / Task packet ID
- Run ID: `R-20260816T110000Z-m7exact-ea0a`
- Task packet ID: `Q-20260814-criticalline-p1-507bb5` (SL exact m₇/m₈ and Λ₄)

## Current plan
Compute exact m₇ (and m₈ if budget permits) for the sine-DPP Gram moment sequence using G2
pruning + exact box-spline engine; then compute Λ₄(0) and test Hankel decay.

## Route history
- Setup and environment check `[SUCCEEDED]`.
- k=7 pruning `[SUCCEEDED]`: Bell(7)=877 → 540 survivors → 18 H-isoclasses.
- k=8 preflight `[SUCCEEDED]`: Bell(8)=4140 → 2683 survivors → 46 isoclasses; full m₈ infeasible in bounded pass; partial b≤2 contribution m₈^(b≤2) = 3724369/181440.
- Exact m₇ b≤3 `[SUCCEEDED]`: all 10 b≤3 isoclasses computed exactly; partial sum m₇^(b≤3) = 1345/72.
- Exact m₇ b=4 `[BLOCKED / OPEN]`: 8 remaining isoclasses are heavy; not completed in budget.

## Ideas to return to
- Complete the 8 b=4 isoclasses with a faster/more optimized engine or more budget; then full m₇ and Λ₄(0).
- If full m₈ remains infeasible, use partial m₈^(b≤2) plus rigorous bounds for b≥3 as evidence.

## Open obligations
- Full exact m₇ (b=4 contribution).
- Λ₄(0) and decay comparison Λ₄ < Λ₃ = 247/2519.
- Full m₈ remains open (b≥3 classes heavy).

## Key artifacts
- `candidate_proof.md`, `research_ledger.md`, `problem_contract.md`, `whiteboard.md`,
  `counterexample_log.md`, `repro_manifest.md`, `SHA256SUMS`.
- `reproducibility/`: `prune_k7.py`, `k7_survivors.json`, `compute_k7_exact.py`,
  `k7_iso_results.json`, `compute_k8_partial.py`, `k8_partial.json`, engines.

## Remaining gaps / honesty
- Exact m₇ is partial (all b≤3; b=4 open).
- Full m₈ computation infeasible in this bounded pass; partial b≤2 contribution only.
