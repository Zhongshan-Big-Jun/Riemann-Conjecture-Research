# T1 formalizer report — chain9_eps (Stage C, lean-verify)

**Status:** `MACHINE_ACCEPTED_PENDING_AUDIT`

T1a (statement), T1b (algebra core), and T1d (constant identities + `record_c9`) are
formalized and **compile with zero sorry/admit/axiom** against the pinned
leanprover/lean4:v4.33.0-rc2 + mathlib@51e6992e environment. T1c (the analytic bridge:
stability step 2, block-defect + pinching/averaging steps 5–6, and the kernel-limit lemma)
is **not machine-proved**; it is carried as explicit axiom-free hypotheses, exactly per the
task's "honest handling" rule. Full detail: `lean-proof/Record9/FORMALIZATION_STATUS.md`.

## Canonical sources (ONLY location — the snapshot is pristine and untouched)

The T1 Lean sources live **only** in the path-dependency project `lean-proof/Record9/`:

- `lean-proof/Record9/Record9/M1Baseline.lean` — module `Record9.M1Baseline`
- `lean-proof/Record9/Record9/Chain9.lean`     — module `Record9.Chain9`

The `chain9_eps` and `record_c9` declarations are opened in the `Zeta23.ThmD` namespace, so
their full names are `Zeta23.ThmD.chain9_eps`, `Zeta23.ThmD.record_c9`,
`Zeta23.ThmD.CERTIFIED_F8_GE`, etc., matching the obligation map. The snapshot
`literature/raw/zeta-23-lean/` contains **no** Record9 files (verified clean, HEAD 706d71e); I
created NO files under it in the final state.

## What is formalized (module `Record9.Chain9`)

- **`Zeta23.ThmD.chain9_eps (hF : CERTIFIED_F8_GE) (b : record9Bridge)`** — the ε-form chain
  theorem (T1):
  ```
  ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
    (1 − (2499:ℝ)/2500/263)·N₀ˢ(T,2T) ≥ (HD 1 − (262:ℝ)/131500 − ε)·N(T,2T)
  ```
  written with the contract's literal rationals (`A₀/m = 2499/657500`, `(m−1)/(500m) = 262/131500`).
- **`CERTIFIED_F8_GE : Prop`** — `∀ g : Fin 8 → ℝ, (∀ i, 0 ≤ g i) → 392/100000 ≤ F8 g`, the
  k=9 pressure certificate statement (value 392/100000). `F8 g = F8gaps wMT g` implements the
  general-k §2 pressure function; `wMT x = (sinc x)²` is the structurally-fixed MT kernel
  (kernel-limit identity = open sub-obligation).
- **Bridge hypotheses** `stability_eps` (step 2) and `stability_averaged_eps` (steps 5–6),
  bundled in `record9Bridge` — the exact open analytic statements, no `axiom`.
- **`chain9_algebra_core`** (T1b), **`chain9_eps_from_hypotheses`** (ε-lift), and the exact
  constant identities + **`record_c9`** (O4): `∀ε>0, ∃T₀, ∀T≥T₀, (c9Const − ε)·N ≤ N₀ˢ`
  with `c9Const = (657500·H_MT − 1310)/655001 = 0.673066472675939665848…`.

## What remains (exact statements)

**T1c — analytic bridge (OPEN).** Provide Lean proofs of:
1. `stability_eps`: `∀ε>0, ∃T₀, ∀T≥T₀: HD 1·N + Δ(T) − ε·N ≤ N₀ˢ` (OpenAI Lemma 2.1/Cor 2.2).
2. `stability_averaged_eps`: `∀ε>0, ∃T₀, ∀T≥T₀: Δ(T) ≥ (2499/657500)·N₀ˢ − (262/131500)·N − ε·N`
   (block-defect lemma + convexity-under-pinching, general-k §4–§6).
3. the **kernel-limit lemma** tying `wMT` to the finite-window MT overlap autocorrelation.
These are paper-level audited inputs; the true `Δ(T) = Δ(M°(T))` is not yet machine-tied.

**T2 — the certificate** `F₈ ≥ 392/100000` (reflection route; `CERTIFIED_F8_GE` is declared
with value 392/100000 but not proved) — separate target.

## Build evidence (exact final state)

The verifier re-runs machine checks independently; what the formalizer itself observed in this
pass, on the canonical sources in `lean-proof/Record9/Record9/`:

| Check | Result | How observed |
|---|---|---|
| O1 baseline: `lake build Zeta23` + `#print axioms` | exit 0 (9010 jobs); headline axioms = `{propext, Classical.choice, Quot.sound}` | manager-recorded (lean-proof/axioms-check.log) |
| `lake build Record9.M1Baseline` (path-dep project) | **exit 0** ("Build completed successfully (8838 jobs)") | this pass |
| `lake env lean` compile of `Record9/Chain9.lean` | **exit 0** (multiple iterations; no sorry/admit/axiom) | this pass |
| `lake env lean` probe with `#check` of chain9_eps / CERTIFIED_F8_GE / F8 / stability_eps / stability_averaged_eps / record_c9 / c9Const / chain9_algebra_core | **exit 0**, types match contract | this pass |
| `lake build Record9.Chain9` (path-dep project) | **not completed by the formalizer** — the path-dep graph resolution exceeded a 10-min budget (killed); the source is identical to the `lake env lean` exit-0 compile and to `Record9.M1Baseline`'s successful `lake build`, so any failure would be environmental, not the code. The verifier re-runs it with a long timeout. | this pass |
| sorry/admit/axiom scan of `Record9/{Chain9,M1Baseline}.lean` | clean (matches only in header docstring disclaimer) | this pass |

Note: earlier in this session an in-snapshot experiment built `Zeta23.Record9.{M1Baseline,Chain9}`
exit 0; those copies were transient (an external Git auto-sync deletes untracked snapshot
files), were removed by the manager (HEAD 706d71e), and are **not** part of the final state.
The authoritative, canonical sources are solely `lean-proof/Record9/Record9/`.

## Route / lakefile changes

- **Snapshot `literature/raw/zeta-23-lean/lakefile.toml` is unchanged** (no `[[lean_lib]]`
  block); the snapshot source tree is pristine (HEAD 706d71e, no Record9 files under it).
- **Canonical project:** path-dependency `lean-proof/Record9/lakefile.toml` (requires `Zeta23`
  and `mathlib` by path; `packagesDir` → snapshot's `.lake/packages`, no network). Modules
  `Record9.M1Baseline` / `Record9.Chain9`.
- A `[[lean_lib]] name = "Record9"` block inside the snapshot was **not** used: the manager
  empirically showed it breaks `lake build Record9` with a bad-imports module-ownership
  conflict. Folding a copy into `Zeta23/` was tried but is unstable here (external auto-sync
  deletes untracked snapshot files) and was reverted. Neither is part of the final state.
- Documentation: `lean-proof/Record9/lakefile-change.md`.

## Deliverables written

- `lean-proof/Record9/Record9/Chain9.lean` (T1 formalization — canonical)
- `lean-proof/Record9/Record9/M1Baseline.lean` (M1 plumbing — canonical)
- `lean-proof/Record9/lakefile.toml`, `lean-proof/Record9/lean-toolchain` (path-dep project)
- `lean-proof/Record9/FORMALIZATION_STATUS.md` (obligation status)
- `lean-proof/Record9/BUILD_LOG.md` (machine command log)
- `lean-proof/Record9/lakefile-change.md` (routes + lakefile decision)
- `lean-proof/Record9/REPORT.md` (this report)
- `lean-proof/obligation_map.md` — appended "T1 formalizer pass" section (O2 now
  T1a/T1b/T1d DONE, T1c OPEN; O1 row carries the completed build/axioms evidence); other rows
  untouched.

No file under `literature/raw/zeta-23-lean/` was created, edited, or left behind in the final
state.
