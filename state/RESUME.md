# Resume this mathematics research program

- **Project:** Riemann Conjecture: Critical-Line Zero Proportion
- **Project ID:** `MRP-20260814-riemann-critical-line-c13b8d`
- **Updated:** 2026-08-15T04:30:00Z

## Current objective

Push liminf N0^s(T,2T)/N(T,2T) (and N0/N, Nd/N) toward 1:
(1) ✅ OpenAI draft constant 0.6730085279277797613 verified (2 independent audits PASS + manager 50-dp check);
(2) ⏳ f9push run: f₉ = 0.00392 certificate (grid-2000, pwsh-4) for a new record 0.6730664726759 > 0.6730536 (running; 0.00395 WITHDRAWN as infeasible — true min ≈ 0.00395005);
(3) ✅ conditional "probability 1" theorem proved (HL* ∀k0 + SL ⇒ 100%; §7.2(f) transcription error m₂=3/4→4/3 resolved; Λ₂(0)=5/36, 13/18 exact) — audit 2bb08828 running; SL moment side COMPLETED 2026-08-15 (random-Gram model reproduces (1,4/3,2,13/4) exactly; SL itself still open as a theorem);
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
| R-…-condp1-698ec7 | RIGOROUS_PARTIAL_RESULT (HL*+SL⇒100%; m₂ 3/4→4/3) | ✅ PASS-CONDITIONAL + F-1 repaired |
| R-…-extpress-2f36ae | RIGOROUS_PARTIAL_RESULT — **NEW RECORD C₉ = 0.673053646** (k=9 certificate F₈≥39/10000) | ✅ PASS with scope limits (manager audit) |
| R-…-f9push-d3b58c | IN_PROGRESS — certify f₉ = 0.00392 → C₉ = 0.6730664726759 (ζ) + 0.8692000910966 (ξ′); grid-2000 8-worker run pwsh-4 (0.00395 WITHDRAWN: infeasible, true min ≈ 0.00395005) | pending |

## Candidate (reports/xi-prime-pressure-method.md, xi-prime-cor22-derivation.md)

ξ′ pressure method with MT window: **C₉^{ξ′} = 0.8691835350528** (exceeds quartic 0.86864).
H_{ξ′}^{MT} = 0.86788886519905193555 (A2 verified two ways); derivation corrected & cross-checked
against OpenAI Cor 2.2 line-for-line; **audits A1–A6 CLOSED at manager level (PASS) —
reports/xi-prime-audit-manager.md**; A1's formalization gap has a complete math blueprint
(reports/admwindow-cos-instance.md: ModFactor A=1, B=2, cMod = cRho+4, all bounds verified
40 dp). Remaining: Lean instance (Stage C, AtOne pattern); f₉=0.00392 certificate.

## Exact next actions

1. Collect the f₉=0.00392 certificate (pwsh-4, grid-2000, 8 workers, launched 2026-08-15
   ~02:10 +08; estimate 20–120k core-s); verify against the precomputed expected values
   (release-checklist.md §1: cutoff 31368, kernel sha 39a209d3…, second-deriv sha 29ca4522…,
   components [[1868,2458];[3511,30823]], initial_boxes 256, depth ≥ 73); if certified →
   new ζ record C₉ = 0.673066472675939665848 and ξ′ linked record
   0.86920009109661916184 (exact forms (657,500·H − 1,310)/655,001, verified dps=130).
   If the 0.00392 run fails: fall back to f₉ = 0.00391
   ((26,300,000·H − 52,400)/26,200,295 → ζ 0.67305992191189169 / ξ′ 0.86919163141999225).
2. Dispatch the independent audit from runs/…/f9push-d3b58c/audit-dispatch-prompt.md
   (manager-level pattern; subagents crash-prone).
3. Update FRONTIER/stage summary; run validate_pipeline; commit + push (per user: sync every result).

## Blockers or missing inputs

None. (Note: GLSS25 primary PDF arXiv:2503.15449 not bundled — quoted via GS Thm 5; verify before relying on it.)

## Budget remaining

unset.

## Validation command

```bash
python C:/Users/HuangZY/.dsh/skills/manage-math-research-program/scripts/validate_project.py "F:\LaTeX\Riemann Conjecture"
python C:/Users/HuangZY/.dsh/skills/math-research-workflow/scripts/validate_pipeline.py --project "F:\LaTeX\Riemann Conjecture" --allow-dirty
```
