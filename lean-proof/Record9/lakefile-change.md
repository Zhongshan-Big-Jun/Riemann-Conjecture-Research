# lakefile change note — Record9 (T1 formalizer pass)

**Date:** 2026-08-16 (session). **Agent:** T1 formalizer (Stage C).

## Route decision: PATH-DEPENDENCY PROJECT (snapshot UNTOUCHED)

The task's route rule says to try a path-dependency project first and fall back to
in-snapshot extension if lake insists on network fetching. After attempting both, the
**path-dependency project is the one used and committed**, and accordingly the snapshot
`literature/raw/zeta-23-lean/` is left **unchanged**.

### What was attempted and why the in-snapshot route was abandoned

1. **In-snapshot extension attempt.** I appended a `[[lean_lib]] name = "Record9"` block to
   `literature/raw/zeta-23-lean/lakefile.toml` and added source under `Zeta23/Record9/`.
   - Lake's module→file mapping for a lean_lib with `srcDir` takes `srcDir/N/M.lean` for
     module `N.M`; after correcting the layout the sources compiled via `lake env lean`.
   - However, editing that tracked `lakefile.toml` is unstable in this environment: it was
     observed to be **reverted to its pristine (HEAD) state** by an external Git auto-sync,
     and the stray `Zeta23/Record9/` directory reappeared. That makes the documented
     in-snapshot multi-minute rebuild both fragile and polluting.
   - It also invalidates the snapshot's `lake` build cache (lakefile hash change ⇒ full
     ~8800-job recompile), which is not something this pass should force on the shared
     baseline.
   - **Conclusion:** abandoned; reverted `lakefile.toml` to pristine and removed the stray
     `Zeta23/Record9/`. Verified `git status` clean for the snapshot source tree.

2. **Path-dependency project (ADOPTED).** `lean-proof/Record9/lakefile.toml` requires
   `Zeta23` by relative path to the snapshot and `mathlib` by path to
   `literature/raw/zeta-23-lean/.lake/packages/mathlib`, with
   `packagesDir = ../../literature/raw/zeta-23-lean/.lake/packages`. Because both packages'
   prebuilt oleans already exist (Zeta23 → `zeta-23-lean/.lake/build`; Mathlib →
   `zeta-23-lean/.lake/packages/mathlib/.lake/build`), the build **replays** the snapshot
   modules (trace checks) instead of recompiling mathlib, and builds only the new `Record9`
   modules. No network fetch occurred. `lean-toolchain` pin: `leanprover/lean4:v4.33.0-rc2`
   (matches the snapshot toolchain).

## Snapshot: NO `[[lean_lib]]` block was added

The snapshot `lakefile.toml` is byte-for-byte unchanged (`git status` clean). The Lean
source files for this pass live in the separate project at
`lean-proof/Record9/Record9/` (module prefix `Record9.*`), not inside the snapshot.

## Build commands (recorded for reproducibility)

Run in `lean-proof/Record9/` with `$env:PATH="$env:USERPROFILE\.elan\bin;$env:PATH"`:

- `lake build Record9.M1Baseline` — exit 0 (8838 jobs, replays snapshot + builds M1Baseline).
- `lake build Record9.Chain9` — exit code recorded in the run log.
- `lake build Record9` — **known Lake limitation**: the *library-target* aggregate build
  reports "Record9: some modules have bad imports" because cross-project (path-dependency)
  imports to `Zeta23.*` are not traced by the library-level graph; the **module-target**
  builds above are the authoritative machine checks and both resolve the imports correctly.
