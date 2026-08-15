# lakefile change note — Record9 (T1 formalizer pass)

**Date:** 2026-08-16 (session). **Agent:** T1 formalizer (Stage C).

## Final state (canonical): NO change to the snapshot; path-dependency project only

The T1 Lean sources live **only** in the path-dependency project `lean-proof/Record9/`
(modules `Record9.M1Baseline` and `Record9.Chain9`). The snapshot
`literature/raw/zeta-23-lean/` is **pristine** (HEAD 706d71e, no Record9 files under it) and
its `lakefile.toml` is **unchanged** (no `[[lean_lib]]` block was added).

- `lean-proof/Record9/lakefile.toml`:
  - `packagesDir = ../../literature/raw/zeta-23-lean/.lake/packages` (reuse snapshot packages).
  - `[[require]] name = "Zeta23" path = ../../literature/raw/zeta-23-lean`
  - `[[require]] name = "mathlib" path = ../../literature/raw/zeta-23-lean/.lake/packages/mathlib`
  - `[[lean_lib]] name = "Record9"`
  - `lean-toolchain` pin: `leanprover/lean4:v4.33.0-rc2` (matches the snapshot).
- Lean source:
  - `lean-proof/Record9/Record9/M1Baseline.lean` → module `Record9.M1Baseline`
  - `lean-proof/Record9/Record9/Chain9.lean` → module `Record9.Chain9`
    (declarations opened in `Zeta23.ThmD`, so full names are `Zeta23.ThmD.chain9_eps`,
    `Zeta23.ThmD.record_c9`, `Zeta23.ThmD.CERTIFIED_F8_GE`, etc.)

## History / alternatives tried (none is in the final state)

1. **In-snapshot `[[lean_lib]] name = "Record9"` block (rejected).** Appending it to the
   snapshot's lakefile causes `lake build Record9` to fail with "some modules have bad imports"
   (module-ownership conflict: the main `Zeta23` lib's root scan also claims `Record9/*.lean`),
   even though `lake build Record9.M1Baseline` and `lake env lean` work (manager finding).
   Editing the tracked file is also unstable here (an external Git auto-sync reverts it) and
   invalidates the snapshot build cache.
2. **In-snapshot modules under `Zeta23/Record9/` (tried, unstable, removed).** Copying the
   modules into `Zeta23/Record9/` (folded into the existing `Zeta23` lean_lib) built via
   `lake build Zeta23.Record9.{M1Baseline,Chain9}` exit 0, but the external Git auto-sync
   intermittently deletes untracked files under `Zeta23/` during long builds. The manager
   removed those copies and restored the snapshot to pristine (commit 706d71e). **Not part of
   the final state.**
3. **Path-dependency project `lean-proof/Record9/` (FINAL).** Canonical and stable, outside the
   snapshot. `lake build Record9.M1Baseline` → exit 0; `Record9.Chain9` compiles via `lake env
   lean` exit 0 (the path-dep `lake build Record9.Chain9` has graph-resolution latency on this
   machine, exceeding the formalizer's 10-min budget; the independent verifier re-runs it with
   a long timeout).

## Build commands (final state)

Run in `lean-proof/Record9/` with `$env:PATH="$env:USERPROFILE\.elan\bin;$env:PATH";`:

- `lake build Record9.M1Baseline` — **exit 0** ("Build completed successfully (8838 jobs)").
- `lake build Record9.Chain9` — **re-run by the verifier (long timeout)**; formalizer observed
  only `lake env lean Record9/Chain9.lean` exit 0 (identical source) this pass.
- `lake env lean <file>` from the snapshot dir — quick typecheck (used to iterate on proofs).
- `lake build Zeta23` (O1 baseline) — exit 0, manager-recorded (9010 jobs).

## Auto-sync / environment note

This project has an external Git auto-sync that intermittently deletes untracked files under
`literature/raw/zeta-23-lean/Zeta23/` during long builds, which is why the canonical sources
are kept in `lean-proof/Record9/` (outside the snapshot) rather than in-snapshot. The snapshot
is intentionally left pristine.
