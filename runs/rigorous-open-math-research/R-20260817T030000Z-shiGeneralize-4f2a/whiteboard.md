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
- Generalization run `[COMPLETED]`: reproduced m=219 optimum; wrote
  multi-certificate LP scanner and `GENERALIZATION.md`. No new certified
  constant found because no third certified certificate is pinned.

## Ideas to return to

- Obtain/audit a third certified local certificate with the same `H_cert`
  baseline, then rerun `multi_cert_scan.py` with three or more certificates.
- Formalize the spectral split `hTrace` in Lean to machine-verify the method's core.
- Make the multi-certificate LP exact (rational simplex or formal interval LP).

## Open obligations

- ~~Reproduce candidate's `joint_check.py` results.~~ Done.
- ~~Search for higher candidate constant.~~ Done for the pinned input set.
- ~~Write absorption/generalization report.~~ Done (`GENERALIZATION.md`).

## Key artifacts

- `problem_contract.md`
- `GENERALIZATION.md`
- `reproducibility/` (joint_check.py, exact_check.py, multi_cert_scan.py, explore_R.py, RESULT.json)
