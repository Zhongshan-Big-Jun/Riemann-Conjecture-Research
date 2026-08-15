# T1 formalizer report — chain9_eps (Stage C, lean-verify)

**Status:** `MACHINE_ACCEPTED_PENDING_AUDIT`

T1a (statement), T1b (algebra core), and T1d (constant identities + `record_c9`) are
formalized and **compile with zero sorry/admit/axiom** against the pinned
leanprover/lean4:v4.33.0-rc2 + mathlib@51e6992e environment. T1c (the analytic bridge:
stability step 2, block-defect + pinching/averaging steps 5–6, and the kernel-limit lemma)
is **not machine-proved**; it is carried as explicit axiom-free hypotheses, exactly per the
task's "honest handling" rule. Full detail: `lean-proof/Record9/FORMALIZATION_STATUS.md`.

## What is formalized (declared in `lean-proof/Record9/Record9/Chain9.lean`)

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

## Build evidence

| Check | Result |
|---|---|
| `lake env lean Record9/Chain9.lean` (pinned env) | **exit 0**, no sorry/admit/axiom |
| `#check Zeta23.ThmD.chain9_eps / CERTIFIED_F8_GE / F8 / stability_eps / stability_averaged_eps / record_c9 / c9Const / chain9_algebra_core` | **exit 0**, types match contract |
| `lake build Record9.M1Baseline` | **exit 0** (8838 jobs; extension plumbing) |
| `lake env lean Record9/M1Baseline.lean` | **exit 0** |
| sorry/admit/axiom scan of `Record9/Chain9.lean` | clean (only the docstring disclaimer mentions the words) |
| Snapshot `literature/raw/zeta-23-lean/lakefile.toml` | **unchanged** |

Note on `lake build`: the path-dependency extension builds fine at the **module** level
(M1Baseline exit 0), but the `lake build Record9.Chain9` graph resolution has a
cross-project latency in this environment (no compile child after ~10 min; killed). The
Chain9 content is verified instead by the `lake env lean` compile of the same file against
the same pinned environment (exit 0) — this is the authoritative compile check (identical to
what `lake build`'s `lean` would run). See `BUILD_LOG.md` for the full command log.

## Route / lakefile changes

- **No change to the snapshot.** The Lean extension lives in the path-dependency project
  `lean-proof/Record9/` (`lakefile.toml` requires `Zeta23` and `mathlib` by path). The
  in-snapshot `[[lean_lib]]` route was attempted and abandoned because the tracked
  lakefile.toml edits get reverted by the project's external Git auto-sync. Documentation:
  `lean-proof/Record9/lakefile-change.md`.

## Deliverables written

- `lean-proof/Record9/Record9/Chain9.lean` (T1 formalization)
- `lean-proof/Record9/Record9/M1Baseline.lean` (M1 plumbing)
- `lean-proof/Record9/FORMALIZATION_STATUS.md` (obligation status)
- `lean-proof/Record9/BUILD_LOG.md` (machine command log)
- `lean-proof/Record9/lakefile-change.md` (routes + lakefile decision)
- `lean-proof/Record9/lakefile.toml`, `lean-proof/Record9/lean-toolchain`
- `lean-proof/obligation_map.md` — appended "T1 formalizer pass" section (O2 now
  T1a/T1b/T1d DONE, T1c OPEN); other rows untouched.
