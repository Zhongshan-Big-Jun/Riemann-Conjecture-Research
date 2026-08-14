# Resume this mathematics research program

- **Project:** Riemann Conjecture: Critical-Line Zero Proportion
- **Project ID:** `MRP-20260814-riemann-critical-line-c13b8d`
- **Updated:** 2026-08-14T05:40:00Z

## Current objective

Push liminf N0^s(T,2T)/N(T,2T) (and N0/N, Nd/N) toward 1:
(1) ✅ OpenAI draft constant 0.6730085279277797613 verified (2 independent audits PASS + manager 50-dp check);
(2) ⏳ extpress run: 9/11-point pressure certificates for a new record > 0.6730085 (running);
(3) ✅ conditional "probability 1" theorem proved (HL* ∀k0 + SL ⇒ 100%; §7.2(f) transcription error m₂=3/4→4/3 resolved; Λ₂(0)=5/36, 13/18 exact) — audit 2bb08828 running;
(4) ✅ exact obstruction report (bandwidth-one 0.6818; class ceiling 0.6730583; k=1 moment barrier; ghost configuration; PCC/HL* routes).

## Read these files first

1. `literature/maps/FRONTIER.md` (B0 audit trail, exact known results, barriers)
2. `agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md`
3. `state/current.json` and `project.json`
4. Latest handoff under `runs/` (if any stage was interrupted)

## Key sources (all local, hashed)

- Claude/Anthropic paper v2: `literature/raw/claude-paper-main-v2-20260813.pdf`
- Lean snapshot: `literature/raw/zeta-23-lean/` (commit 3635e748; Lean v4.33.0-rc2; local lake 4.31.0 — use elan to pin)
- OpenAI draft: `literature/raw/zeta-simple-zeros/` (commit 040c5e8)

## Run status matrix

| Run | Status | Audit |
|---|---|---|
| R-…-mainpush-3cdc81 | RIGOROUS_PARTIAL_RESULT (R1 verified, R2 PCC⇒100%, R3 ceiling 0.6730583) | ✅ PASS (5F0EDEAA…) |
| R-…-oaidraft-7c3e73 | INDEPENDENTLY_AUDITED_PROOF (draft 0.673008528 verified) | ✅ PASS (3F554804…) |
| R-…-condp1-698ec7 | RIGOROUS_PARTIAL_RESULT (HL*+SL⇒100%; m₂ 3/4→4/3) | ⏳ audit 2bb08828 running |
| R-…-extpress-2f36ae | IN_PROGRESS (9/11-pt pressure) | pending |

## Exact next actions

1. Collect condp1 audit verdict (2bb08828) + extpress result (f4d9e0c3); verify hashes.
2. If extpress certifies a new constant > 0.673008528: reconstruct full proof chain, dispatch audit.
3. Ingest all verdicts; write stage summary (assets/stage-summary.template.md → state/stage-summaries/); update FRONTIER; run validate_pipeline; commit + push.
4. Report to user: honest final state (achieved conditionally / reduced / blocked unconditionally).

## Blockers or missing inputs

None. (Note: GLSS25 primary PDF arXiv:2503.15449 not bundled — quoted via GS Thm 5; verify before relying on it.)

## Budget remaining

unset.

## Validation command

```bash
python C:/Users/HuangZY/.dsh/skills/manage-math-research-program/scripts/validate_project.py "F:\LaTeX\Riemann Conjecture"
python C:/Users/HuangZY/.dsh/skills/math-research-workflow/scripts/validate_pipeline.py --project "F:\LaTeX\Riemann Conjecture" --allow-dirty
```
