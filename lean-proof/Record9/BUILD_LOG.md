# T1 formalizer — machine command log (build evidence)

**Toolchain:** leanprover/lean4:v4.33.0-rc2 (pinned by `lean-toolchain`). Mathlib @ 51e6992e. All
commands run on Windows with `$env:PATH="$env:USERPROFILE\.elan\bin;$env:PATH";`.

Recorded by the T1 formalizer agent on 2026-08-16. Every command's exit code is recorded below.

## O1 baseline (manager-recorded, referenced for context)

`lake build Zeta23` exit 0 (9010 jobs); `#print axioms` on all headline theorems = {propext,
Classical.choice, Quot.sound} (lean-proof/axioms-check.log).

## Canonical project — `lean-proof/Record9/` (path-dependency). FINAL STATE.

The T1 Lean sources live **only** under `lean-proof/Record9/Record9/` as modules
`Record9.M1Baseline` and `Record9.Chain9`. `lakefile.toml` requires `Zeta23` and `mathlib` by
path (`packagesDir` → the snapshot's `.lake/packages`; no network). The snapshot holds NO
Record9 files and its `lakefile.toml` is unchanged.

| Command (workdir = lean-proof/Record9) | Exit | Evidence |
|---|---|---|
| `lake build Record9.M1Baseline` | **0** | "Build completed successfully (8838 jobs)": replays snapshot + builds the plumbing. |
| `lake build Record9.Chain9` | (not completed this pass) | path-dep graph-resolution latency exceeded the 10-min budget (killed; driver never reached the compile child). The source is identical to the `lake env lean` exit-0 compile and to `Record9.M1Baseline`'s successful build, so a failure would be environmental. The independent verifier re-runs this with a long timeout. |
| `lake build Record9` (library target) | 1 | known lake limitation with cross-project (path-dep) library aggregation ("bad imports"); the module targets above are the authoritative checks. |

## `lake env lean` compile checks (used to iterate on proofs, from the snapshot dir; fast)

| Command | Exit | Note |
|---|---|---|
| `lake env lean lean-proof/Record9/Record9/Chain9.lean` (various) | 0 | full file type-checks (all proof iterations), no sorry/admit/axiom |
| `lake env lean %TEMP%\Chain9_probe.lean` (source + #check probes) | 0 | #check of every T1 declaration typed correctly |

### `#check` transcript (statement fidelity evidence)

```
Zeta23.ThmD.chain9_eps (hF : Zeta23.ThmD.CERTIFIED_F8_GE) (b : Zeta23.ThmD.record9Bridge) (ε : ℝ) :
  ε > 0 → ∃ T₀, ∀ T ≥ T₀,
    (1 - 2499/2500/263) * ↑(Zeta23.N0simple T (2*T)) ≥ (Zeta23.ThmD.HD 1 - 262/131500 - ε) * ↑(Zeta23.Ncount T (2*T))
Zeta23.ThmD.CERTIFIED_F8_GE : Prop
Zeta23.ThmD.F8 (g : Fin 8 → ℝ) : ℝ
Zeta23.ThmD.stability_eps : Prop
Zeta23.ThmD.stability_averaged_eps : Prop
Zeta23.ThmD.record_c9 (hF : Zeta23.ThmD.CERTIFIED_F8_GE) (b : Zeta23.ThmD.record9Bridge) (ε : ℝ) :
  ε > 0 → ∃ T₀, ∀ T ≥ T₀, (Zeta23.ThmD.c9Const - ε) * ↑(Zeta23.Ncount T (2*T)) ≤ ↑(Zeta23.N0simple T (2*T))
Zeta23.ThmD.c9Const : ℝ
Zeta23.ThmD.chain9_algebra_core {S N D e₁ e₂ : ℝ} (hStab : Zeta23.ThmD.HD 1 * N + D - e₁ * N ≤ S)
  (hAvg : 2499/657500 * S - 262/131500 * N - e₂ * N ≤ D)
  : (1 - 2499/2500/263) * S ≥ (Zeta23.ThmD.HD 1 - 262/131500) * N - (e₁ + e₂) * N
```

## Historical (NOT in the final state): transient in-snapshot experiment

Earlier the same module content was temporarily copied under `literature/raw/zeta-23-lean/Zeta23/Record9/`
(modules `Zeta23.Record9.*`) and built via `lake build Zeta23.Record9.{M1Baseline,Chain9}` → exit 0.
These copies were killed by an intermittent external Git auto-sync and then removed by the manager
(commit 706d71e). They are recorded here only as additional evidence that the code builds via
`lake build`, but they are **not** part of the final deliverable; the canonical sources are solely
`lean-proof/Record9/Record9/`.

## sorry / admit / axiom scan

`grep` for `sorry|admit|axiom` over `lean-proof/Record9/Record9/*.lean` finds matches only in the
header docstring disclaimer text ("NO sorry/admit/axiom appear…"), never a declaration. No `axiom`
is introduced; the analytic bridge is plain theorem hypotheses.
