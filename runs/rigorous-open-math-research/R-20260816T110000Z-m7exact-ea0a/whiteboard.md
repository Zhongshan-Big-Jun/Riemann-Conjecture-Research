# Whiteboard — R-20260816T110000Z-m7exact-ea0a

```text
- **Run ID:** `R-20260816T110000Z-m7exact-ea0a`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5` (SL exact m₇/m₈ and Λ₄)
- **Project:** `F:\LaTeX\Riemann Conjecture`
- **Last updated:** `2026-08-16T12:10:00Z`
```

## Run ID / Task packet ID
- Run ID: `R-20260816T110000Z-m7exact-ea0a`
- Task packet ID: `Q-20260814-criticalline-p1-507bb5` (SL exact m₇/m₈ and Λ₄)

## Current plan
Bounded exact pass on SL moments. Active: **exact m₇** — G2-prune 877→540 survivors → 18
H-isoclasses → exact per-isoclass J (b=1,2 closed form; b=3,4 box-spline exact+fast cross-check)
→ sum m₇ → Hankel/Λ₄ test → validation. Then record m₈ status (full OPEN; exact b≤2 partial
done). Immediate next: wait for `compute_k7_exact.py` BG job (pwsh-11) to finish all 18
isoclasses, then assemble m₇, Λ tests, and artifacts.

## Route history
- `setup-env` `[SUCCEEDED]`: py -3.10, numpy/scipy/sympy/mpmath/flint OK; engines copied byte-identical.
- `k7-prune` `[SUCCEEDED]`: Bell(7)=877 → 540 survivors (1 b=1, 63 b=2, 266 b=3, 210 b=4); 337 pruned (all low-surplus; disconnected prong vacuous for real k=7 partitions).
- `k7-isoclass` `[SUCCEEDED]`: 540 survivors → 18 isoclasses (1 b=1, 3 b=2, 6 b=3, 8 b=4); J depends only on (b,H).
- `k7-exact` `[IN PROGRESS]`: 7/18 done; b=1,2 closed-form exact; b=3 values 1/15, 1/180, 1/420, 11/630, each engine_diff=0.0. Script `compute_k7_exact.py`.
- `k8-preflight` `[SUCCEEDED]`: Bell(8)=4140 → 2683 survivors → 46 isoclasses; b=4 ~387s/iso, b=5 over cap ⇒ **full m₈ OPEN** (budget).
- `k8-partial` `[SUCCEEDED]`: exact b≤2 m₈^(b≤2) = 3724369/181440 ≈ 20.526725.
- `hankel` `[PENDING]`: needs m₀..m₇ (and m₈ if Λ₄ determinant requires it).

## Ideas to return to
- Promote the (b,H_canonical)→J isoclass table as a reusable tool (m6 note cited 18 isoclasses; reproduced here).
- Future full-m₈ pass: need faster b=4/b=5 box-spline path (float engine + per-isoclass exact cross-check, or the g2proof degree-2 reduction).

## Open obligations
- **Exact m₇ sum + Λ₄ Hankel test** — in progress (blocked on compute job finishing).
- **Λ₄(0) < Λ₃ = 247/2519 ?** — pending; if Λ₄ needs m₈, report exact gap.
- **Full m₈ (b=3,4,5)** — OPEN (budget-limited); only b≤2 exact partial claimed.

## Key artifacts
- `reproducibility/prune_k7.py`, `k7_survivors.json`, `compute_k7_exact.py`, `k7_iso_results.json`, `k7_allJ.json`.
- `reproducibility/prune_k8.py`, `k8_survivors.json`, `compute_k8_partial.py`, `k8_partial.json`.
- `reproducibility/*.py` upstream engines; `problem_contract.md`, `repro_manifest.md`, `research_ledger.md`, `counterexample_log.md`.
(sha256 for each in `SHA256SUMS` when finalized.)

## Remaining gaps / honesty
- Exact m₇ not yet complete; all recorded partial J values are exact rationals.
- Full m₈ infeasible in this bounded pass; only exact b≤2 partial claimed.
- G2 rule used as upstream-verified, not re-proved here.
