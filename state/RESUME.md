# Resume this mathematics research program

- **Project:** Riemann Conjecture: Critical-Line Zero Proportion
- **Project ID:** `MRP-20260814-riemann-critical-line-c13b8d`
- **Updated:** 2026-08-14T04:25:00Z

## Current objective

Push liminf N0^s(T,2T)/N(T,2T) (and N0/N, Nd/N) toward 1:
(1) independently verify the OpenAI/GPT-5.6 draft constant 0.6730085279277...;
(2) attempt unconditional improvements (gap-structure certificates, >7-point, better windows);
(3) prove conditional "probability 1" (HL*(all k0) ⇒ 100%, PCC full support ⇒ 100% [GLSS25]);
(4) report exact obstructions to unconditional probability 1.

## Read these files first

1. `literature/maps/FRONTIER.md` (B0 audit trail, exact known results, barriers)
2. `agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md` (contract, obligations O1–O8, sources+hashes)
3. `state/current.json` and `project.json`
4. Latest handoff under `runs/` (if any stage was interrupted)

## Key sources (all local, hashed)

- Claude/Anthropic paper v2 (preferred): `literature/raw/claude-paper-main-v2-20260813.pdf`
- Lean snapshot: `literature/raw/zeta-23-lean/` (commit 3635e748; Lean v4.33.0-rc2)
- OpenAI draft: `literature/raw/zeta-simple-zeros/` (commit 040c5e8; paper/riemann.pdf; src/ verifier)

## Last completed action

Stage A complete: project initialized, preflight OK (0 problems), B0 novelty preflight done,
7 papers registered, packet Q-20260814-criticalline-p1-507bb5 dispatched to three solver runs
(R-20260814T041219Z-{mainpush-3cdc81, oaidraft-7c3e73, condp1-698ec7}).

## Active tasks and runs

| Run | Task |
|---|---|
| R-…-mainpush-3cdc81 | verify OpenAI draft + improve constants + probability-1 attack + numerics |
| R-…-oaidraft-7c3e73 | focused independent audit of OpenAI draft (O2, O7) |
| R-…-condp1-698ec7 | conditional probability-1 theorems (O5, O4-cond) |

## Exact next action

Collect run outputs (job ids in session log), ingest status labels verbatim into
`index/runs.json` + `index/artifacts.json`, run adversarial audits, then decide Stage C
(Lean formalization of any qualified result) — gate: only `CANDIDATE_COMPLETE_PROOF`/`已证`.

## Blockers or missing inputs

None. (arXiv API rate-limited 429/503 on 2026-08-14; use abs-page fetches with backoff.)

## Budget remaining

unset.

## Validation command

```bash
python C:/Users/HuangZY/.dsh/skills/manage-math-research-program/scripts/validate_project.py "F:\LaTeX\Riemann Conjecture"
python C:/Users/HuangZY/.dsh/skills/math-research-workflow/scripts/validate_pipeline.py --project "F:\LaTeX\Riemann Conjecture" --allow-dirty
```
