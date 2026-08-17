# Interruption handoff — f9push T2 certificate reflection (counting pass)

- **Run ID**: R-20260814T131528Z-f9push-d3b58c
- **Task packet ID**: Q-20260814-criticalline-p1-507bb5 (obligation O3)
- **Date**: 2026-08-17T01:00Z
- **Interrupt reason**: user requested termination of research and repository handoff; the
  full terminal-box counting pass was still running.
- **Task state**: IN_PROGRESS

## Task state

IN_PROGRESS / BLOCKED (T2 reflection not complete).

## Completed work progress

- The audited certificate file is already released:
  `reproducibility/certificates/nine-point-f8-gt-392over100000-grid2000.txt`
  (nodes 64,748,524, depth 80, components `[[1868,2458];[3511,30823]]`, kernel sha
  `39a209d3…`, second-deriv sha `29ca4522…`).
- The instrumented counting verifier
  `reproducibility/verify_kpoint_parallel_t2count.py` exists and is byte-compatible with
  the audited verifier plus `--emit-boxes`/`--boxes-out`.
- Multiple counting attempts were made:
  - `--workers 8` tangent: killed at ~36k CPU-s (first) and ~40k CPU-s (second) before output.
  - `--no-tangent --workers 4`: killed after ~30k CPU-s before output.
- **Runtime correction (2026-08-17)**: the original certificate report records
  `elapsed_seconds=8765.75` @ 8 workers (~70k core-s), so earlier kills at 36–40k CPU-s were
  premature. A fresh `--workers 8` tangent run (background pwsh-1) was started and was
  killed at user request before completion; no `T2 accepted terminal boxes:` line was printed.

## Completed obligations

- All B0–B6 math checks, independent third-party audit (PASS-WITH-LIMITS), T1 machine checks,
  T3 AtOne facts, and T1c-2a block-energy closure are already committed.

## Open obligations

- O3/T2: terminal accepted-box count and/or Step 1b coarser certified partition.
- Lean T2 checker (`Record9.T2Cert` or equivalent) not yet written; depends on box data.

## Tools and methods tried

- [SUCCEEDED] Original certificate verification (`verify_kpoint_parallel.py`) produced the
  released certificate.
- [PARTIAL] `verify_kpoint_parallel_t2count.py --workers 8` tangent counting: ran to
  ~36–40k CPU-s without completing; interrupted.
- [PARTIAL] `verify_kpoint_parallel_t2count.py --workers 4 --no-tangent`: ran to ~30k CPU-s
  without completing; interrupted.
- [BLOCKED] Full terminal-box count requires ~70k core-s (≈2.4h wall @8 workers); not
  completed before user stop.

## Attempted routes

- [FAILED] Full B&B counting with default tangent: not completed in two attempts.
- [FAILED] Full B&B counting with `--no-tangent`: slower, not completed.
- [PENDING] Step 1b coarser certified partition (not implemented yet).
- [PENDING] Profile `verify_kpoint_parallel_t2count.py` to confirm it matches original
  performance when allowed to run to ~70k core-s.

## Next actions

1. Run `verify_kpoint_parallel_t2count.py 9 392/100000 --grid 2000 --precision 128 --workers 8`
   to completion (allow ~70k core-s / ~2.4h wall) and record `T2 accepted terminal boxes:`.
2. If the count is too large to emit, implement Step 1b coarser certified partition.
3. Generate box JSON (`--emit-boxes --boxes-out`) and build the Lean exact-rational checker.

## Key artifacts

- `reproducibility/verify_kpoint_parallel_t2count.py` (instrumented counting verifier)
- `reproducibility/verify_kpoint_parallel.py` (original audited verifier)
- `reproducibility/certificates/nine-point-f8-gt-392over100000-grid2000.txt` (released cert)
- `reports/t2-reflection-plan.md` (plan + runtime correction)
- `reproducibility/t2count_final_report.txt` / `t2count_final_report2.txt` (not written;
  runs were killed before completion)
