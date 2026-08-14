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
| R-…-condp1-698ec7 | RIGOROUS_PARTIAL_RESULT (HL*+SL⇒100%; m₂ 3/4→4/3) | ✅ PASS-CONDITIONAL + F-1 repaired |
| R-…-extpress-2f36ae | RIGOROUS_PARTIAL_RESULT — **NEW RECORD C₉ = 0.673053646** (k=9 certificate F₈≥39/10000) | ✅ PASS with scope limits (manager audit) |
| R-…-f9push-d3b58c | IN_PROGRESS — certify f₉ = 0.00395 → C₉ = 0.6730856 (ζ) + 0.8692247 (ξ′); grid-2000/grid-4000 8-worker runs | pending |

## Candidate (reports/xi-prime-pressure-method.md, xi-prime-cor22-derivation.md)

ξ′ pressure method with MT window: **C₉^{ξ′} = 0.8691835350528** (exceeds quartic 0.86864).
H_{ξ′}^{MT} = 0.86788886519905193555 (A2 verified two ways); derivation corrected & cross-checked
against OpenAI Cor 2.2 line-for-line; audits A1–A6 packet ready (reports/xi-prime-audit-request.md).

## Exact next actions

1. Collect f₉=0.00395 certification results (pwsh-43 grid-2000, pwsh-44 grid-4000); verify
   certificates; if certified → new ζ record C₉ = 0.6730855621335 and ξ′ linked record
   0.8692247262342 (ladder in reports/linked-ladder.md).
2. Run the A1–A6 independent audit of the ξ′ candidate (audit request packet prepared).
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
