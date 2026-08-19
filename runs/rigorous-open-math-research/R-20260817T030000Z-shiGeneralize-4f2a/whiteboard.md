# Whiteboard — R-20260817T030000Z-shiGeneralize-4f2a (Shi two-certificate generalization)

- **Run ID:** `R-20260817T030000Z-shiGeneralize-4f2a`
- **Task packet ID:** Q-20260814-criticalline-p1-507bb5 (external candidate absorption + generalization)
- **Last updated:** `2026-08-17T03:00:00Z`

## Current plan

1. Absorb the Shi 0.673316977 candidate into project records (FRONTIER/index/status).
2. Reproduce and generalize the two-certificate supporting-plane method.
3. Search for a higher candidate constant (multi-certificate / other m).
4. Produce exact-rational scripts and a generalization report.

## Route history

- Audit of Shi candidate `[SUCCEEDED]`: PLAUSIBLE-WITH-GAPS (see shiAudit run).
- Generalization run `[IN PROGRESS]`.

## Ideas to return to

- Multi-certificate supporting plane (three or more local inequalities).
- Formalize the spectral split `hTrace` in Lean to machine-verify the method's core.
- Explore other block lengths and pairings.

## Open obligations

- Reproduce candidate's `joint_check.py` results.
- Search for higher candidate constant.
- Write absorption/generalization report.

## Key artifacts

- `problem_contract.md`
- `reproducibility/` (joint_check.py, exact_check.py, RESULT.json)
- (to be added) generalization scripts/report
