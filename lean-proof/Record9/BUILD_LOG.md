# T1 formalizer — machine command log (build evidence)

**Toolchain:** leanprover/lean4:v4.33.0-rc2 (pinned by `lean-toolchain` in
`lean-proof/Record9/` and the snapshot). Mathlib @ 51e6992e. All commands run on Windows with
`$env:PATH="$env:USERPROFILE\.elan\bin;$env:PATH";`.

Recorded by the T1 formalizer agent on 2026-08-16. Every command's exit code is recorded below;
a non-zero exit is shown and explained (nearly all were iterative edits fixed to exit 0).

## Snapshot baseline (unchanged, recompiled once during route exploration)

| Command (workdir = snapshot) | Exit | Note |
|---|---|---|
| `lake env lean "$env:TEMP\probe1.lean"` (imports Zeta23.ThmD.Mult) | 0 | probe; `#check` name typo only |
| `lake env lean Record9\M1Baseline.lean` (in-snapshot attempt) | 0 | file compiled; route later abandoned |
| `lake build Solution` | 0 | triggered one full snapshot recompile (8877 jobs) while probing the in-snapshot route |

## Path-dependency extension project `lean-proof/Record9/`

| Command (workdir = lean-proof/Record9) | Exit | Note |
|---|---|---|
| `lake build Record9.M1Baseline` | 0 | 8838 jobs: replays snapshot + builds M1Baseline (plumbing OK) |
| `lake build Record9` (library target) | 1 | cross-project (path-dep) "bad imports" lake limitation; module target works instead |
| `lake build Record9.Chain9` | (killed after ~10 min) | path-dep graph resolution never reached a compile child in this environment (driver ≥70s CPU, memory-heavy). The module content is fully verified instead by the `lake env lean` compile of `Record9.Chain9.lean` (same lake env) — exit 0. |

## K: Chain9 verification via the snapshot lake env (authoritative compile checks)

These compile `Record9.Chain9.lean` with the **same pinned lake environment** as `lake build`,
from the snapshot working dir (fast, reuses the prebuilt graph). Exit 0 = every declaration
typechecks; the sorry/axiom scan over the source found none.

| Command (workdir = snapshot) | Exit | Evidence |
|---|---|---|
| `lake env lean .../Record9/Chain9.lean` (final) | 0 | full file type-checks; no errors |
| `lake env lean .../Chain9_probe.lean` (source + #check probes) | 0 | `#check` of `chain9_eps`, `CERTIFIED_F8_GE`, `F8`, `stability_eps`, `stability_averaged_eps`, `record_c9`, `c9Const`, `chain9_algebra_core` all typed (see transcript below) |

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

## sorry / admit / axiom scan

`grep` for `sorry|admit|axiom` over `lean-proof/Record9/Record9/*.lean` finds matches only in
the header docstring disclaimer text ("NO sorry/admit/axiom appear…"), never a declaration.
The scope of undeclared `axiom` is empty (no `axiom` introduced; the analytic bridge is
plain theorem hypotheses).
