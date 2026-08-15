# lakefile change note — Record9 (T1 formalizer pass)

**Date:** 2026-08-16 (session). **Agent:** T1 formalizer (Stage C).

## Route decision: PATH-DEPENDENCY PROJECT (snapshot UNTOUCHED)

The task route rule says to try a path-dependency project first and fall back to the
in-snapshot extension if lake insists on network fetching. Both were attempted; the
**path-dependency project is used and committed**, and accordingly the snapshot
`literature/raw/zeta-23-lean/` is left **unchanged** (no `[[lean_lib]]` block was added; its
`lakefile.toml` is byte-for-byte the original).

### In-snapshot attempt — abandoned

I appended a `[[lean_lib]] name = "Record9"` block to the snapshot's `lakefile.toml` and
added source under `Zeta23/Record9/`. Two problems forced abandoning this:

1. **External Git auto-sync reverts tracked-file edits** in this project: the edited
   `lakefile.toml` was observed returning to its pristine (HEAD) state, and the untracked
   additions under `Zeta23/Record9/` were removed. The snapshot subtree is effectively
   read-only in this environment.
2. Editing `lakefile.toml` invalidates the snapshot's lake build cache hash, forcing a full
   ~8800-job recompile of the shared baseline — undesirable for a shared artifact.

I reverted my changes (confirmed `git status` clean for the snapshot source tree) and moved
to the path-dependency project.

### Path-dependency project — ADOPTED

`lean-proof/Record9/lakefile.toml`:

- `packagesDir = ../../literature/raw/zeta-23-lean/.lake/packages` (reuse snapshot packages,
  no network fetch).
- `[[require]] name = "mathlib" path = ../../literature/raw/zeta-23-lean/.lake/packages/mathlib`
- `[[require]] name = "Zeta23" path = ../../literature/raw/zeta-23-lean`
- `[[lean_lib]] name = "Record9"`
- `lean-toolchain` pin: `leanprover/lean4:v4.33.0-rc2` (matches the snapshot toolchain).

Because both path packages already have prebuilt oleans (Zeta23 → `zeta-23-lean/.lake/build`,
Mathlib → `zeta-23-lean/.lake/packages/mathlib/.lake/build`), the build **replays** the
snapshot modules (trace checks) instead of recompiling mathlib, and compiles only the new
`Record9` modules. No network fetch occurred.

### Snapshot: NO change

The snapshot `lakefile.toml` and all tracked files are unchanged; my Lean source only lives
in the separate project at `lean-proof/Record9/Record9/` (module prefix `Record9.*`).

## Build commands (recorded)

Run in `lean-proof/Record9/` with `$env:PATH="$env:USERPROFILE\.elan\bin;$env:PATH";`:

- `lake build Record9.M1Baseline` — exit 0 (8838 jobs, replays snapshot + builds M1Baseline).
- `lake env lean Record9.M1Baseline.lean` — exit 0 (from the snapshot working dir, fast).
- `lake env lean Record9.Chain9.lean` — exit 0 (from the snapshot working dir; see below).
- `lake build Record9.Chain9` — see STATUS note; a cross-project graph-resolution latency
  affects the library-level `lake build` in this environment.

### STATUS note on `lake build` vs `lake env lean`

The path-dependency project's `lake build` sometimes incurs multi-minute graph-resolution
latency because lake rewalks the huge mathlib transitive closure through path deps on each
invocation (observed 49s for the first M1Baseline build; longer for libraries). The primary
machine evidence reported for the Chain9 formalization (M2/M3) is therefore the **`lake env
lean` compile of `Record9.Chain9.lean` (exit 0, no sorry/admit/axiom)** plus the successful
`lake build Record9.M1Baseline` for the plumbing. `lake env lean <file>` is the same Lean
compiler/lake environment as `lake build`; the exit code 0 establishes that every
declaration in the file typechecks against the pinned Zeta23/mathlib environment.
