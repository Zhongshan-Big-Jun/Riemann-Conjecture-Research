# T1 formalization status — Record9 extension (Stage C, lean-verify)

**Declaration targets (contract):** `Zeta23.ThmD.chain9_eps` (T1), plus auxiliaries
`CERTIFIED_F8_GE`, `F8`/`F8gaps`/`wMT`, bridge hypotheses, `record_c9` (O4), and the
constant identities (T1d).

**Files (Lean source, in the path-dependency extension project `lean-proof/Record9/`):**

| File | Module | Content |
|---|---|---|
| `Record9/M1Baseline.lean` | `Record9.M1Baseline` | M1 smoke test: baseline `thmD₀_simple_mult` importable. |
| `Record9/Chain9.lean` | `Record9.Chain9` | T1 (chain9_eps), pressure function + certificate statement, bridge hypotheses, algebra core, record_c9, constants. |

The declarations live in the `Zeta23.ThmD` and `Zeta23.Remainder` namespaces via the module
`Record9.Chain9`; full names are `Zeta23.ThmD.chain9_eps` etc. (see #check evidence).

---

## Status summary

| Obligation | Status | Machine evidence | Remaining gap |
|---|---|---|---|
| **T1a — statement** (`chain9_eps`, `CERTIFIED_F8_GE`, pressure `F8`, bridge hypotheses) | **DONE** | `lake env lean Record9/Chain9.lean` exit 0; `#check Zeta23.ThmD.chain9_eps` types the conclusion `(1 − (2499:ℝ)/2500/263)·N₀ˢ ≥ (HD 1 − 262/131500 − ε)·N`; `CERTIFIED_F8_GE : Prop` | none (statement faithful; see Fidelity notes) |
| **T1b — algebra core** (`chain9_algebra_core`, `chain9_eps_from_hypotheses`, `chain9_eps`) | **DONE** | Same build exit 0; `chain9_algebra_core` proves the ε-form implication from the two bridge hypotheses | none |
| **T1c — analytic bridge** (stability step 2; block-defect + pinching/averaging steps 5–6) | **OPEN** (explicit hypotheses) | represented as `stability_eps` and `stability_averaged_eps`, bundled in `record9Bridge`; not faked, not machine-proved | exact statements below |
| **T1d — constant identity + O4** (`A0_eq_f9n9`, `cLHS_pos`, `c9Const_eq`, `record9_constant_identity`, `record_c9`) | **DONE** | Same build exit 0; `record_c9` states liminf N₀ˢ/N ≥ C₉ = (657,500·H_MT − 1,310)/655,001 in ε-form | none (conditional on T1b closure + bridge) |
| **T2 certificate** (`F8 ≥ 392/100000`) | **OPEN** (separate target) | `CERTIFIED_F8_GE` declared, value `392/100000`; not proved (T2 scope) | reflection route |

---

## T1a — statement fidelity

The ε-form statement, written out with the contract's literal rationals, is:

```lean
theorem chain9_eps (hF : CERTIFIED_F8_GE) (b : record9Bridge) :
    ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
      (1 - (2499 : ℝ) / 2500 / 263) * (N0simple T (2*T) : ℝ)
        ≥ (HD 1 - (262 : ℝ) / 131500 - ε) * (Ncount T (2*T) : ℝ)
```

Fidelity vs the contract:
- `(1 − (2499:ℝ)/2500/263) = 1 − A₀/m` with `A₀/m = 2499/657500` ✓ (cA0m_eq).
- `(262:ℝ)/131500 = (m−1)/(500m)` for m=263 ✓ (qMT_eq: = 131/65750).
- `HD 1 = H_MT` via baseline `Zeta23.ThmD.HD_one` ✓ (imported baseline).
- Quantifier order `∀ε>0, ∃T₀, ∀T≥T₀`, T real, dyadic window (T,2T], `N0simple`/`Ncount`
  are the baseline multiplicity/simple-on-line counts ✓.
- `chain9_eps` is stated with `hF : CERTIFIED_F8_GE` (the paper certificate) **and** the
  bundled `b : record9Bridge` — the honest routing of the open analytic steps 2,5,6 as
  explicit axiom-free hypotheses (task "honest handling" rule). It is not possible to
  derive the conclusion from `hF` alone without those steps, so they are threaded through
  as hypotheses.

`CERTIFIED_F8_GE` (what it means):
```lean
CERTIFIED_F8_GE : Prop := ∀ g : Fin 8 → ℝ, (∀ i : Fin 8, 0 ≤ g i) → (392:ℝ)/100000 ≤ F8 g
```
where `F8` is the k=9 pressure value `F8gaps wMT` (see below).

## T1a — pressure function F₈ and the kernel w

`F8gaps (w : ℝ → ℝ) (g : ℕ → ℝ) : ℝ` implements, for k=9 (8 gaps), exactly the general-k §2
expression (s0 = s−1 ∈ 0..7):
```
F₈ = (1/(500·8))·Σ_{i<8} g_i  +  Σ_{s0=0}^{7} (2/(8−s0))·Σ_{i<8−s0} w(gapsum(g,i,s0+1))
```
`gapSpan g i len = Σ_{j<len} g(i+j)` is the consecutive-gap window sum; the inder windows
cover the 8 gaps 0..7 with the paper's `2/(k−s)` weighing. `F8 : Fin 8 → ℝ → ℝ` adapts the
0-based vector.

The kernel `wMT x = (sincMT x)²`, `sincMT x = if x = 0 then 1 else sin x / x`, is the
**normalized Montgomery–Taylor overlap kernel fixed structurally** (even, w(0)=1, nonneg,
sinc-shaped) per the paper. Its precise identity with the finite-window overlap autocorrelation
in the high-T limit (the *kernel-limit lemma*) is **not assumed and not machine-tied here**; it
is an analytic-bridge sub-obligation (bounded handling of M4). `CERTIFIED_F8_GE` is therefore a
statement about the intended (structurally-fixed) kernel; the numerical certificate asserting it
is T2.

## T1c — analytic bridge (OPEN), exact statements

These are the paper-level, audited-but-not-in-Lean steps. They are declared verbatim as
hypotheses; the machine content is only that they *imply* the ε-form chain.

1. `stability_eps` (step 2; OpenAI Lemma 2.1/Cor 2.2):
   ```
   ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
     HD 1 * N(T,2T) + Δ(T) − ε·N(T,2T) ≤ N₀ˢ(T,2T)
   ```
   where `Δ(T) = Δ(M°(T))` is the Gram-defect value (placeholder `deltaMT`; not machine-tied).
   This says `S ≥ H_MT·N + Δ(M°) − o(N)`.

2. `stability_averaged_eps` (steps 5–6: block-defect lemma + convexity-under-pinching
   averaging, general-k §4–§6 / [OpenAI §4], [OpenAI (20)]):
   ```
   ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
     Δ(T) ≥ (2499/657500)·N₀ˢ(T,2T) − (262/131500)·N(T,2T) − ε·N(T,2T)
   ```
   i.e. `Δ(M°) ≥ (A₀/m)·S − ((m−1)/(500m))·N − o(N)`.

3. The **kernel-limit lemma** linking `wMT` with the finite-window MT overlap (needed to reach
   the block-defect from the energy bound) is likewise an open analytic sub-obligation.

No `axiom` is used: these are plain theorem hypotheses (`Prop` fields of `record9Bridge`).
Closing T1c = supplying correct Lean proofs of `stability_eps` and `stability_averaged_eps`
for the true `Δ(M°)`; that is the remaining gap.

## T1b — the machine-checked algebra (what the build actually proves)

`chain9_algebra_core`, proved by `norm_num`+`ring_nf`+`set`+`linarith`:
> from `HD 1·N + D − e₁·N ≤ S` and `(2499/657500)·S − (262/131500)·N − e₂·N ≤ D`
> derive `(1 − (2499:ℝ)/2500/263)·S ≥ (HD 1 − 262/131500)·N − (e₁+e₂)·N`.

`chain9_eps_from_hypotheses` lifts this to the ε-form over T with the ε/2 splitting;
`chain9_eps` is its literal re-statement with the contract's rationals.

## T1d — exact constant identities (machine-checked)

- `A0_eq_f9n9 : A₀ = f₉·n₉ = 2499/2500` (f₉ = 392/100000, n₉ = 255).
- `cLHS_eq : cLHS = 655001/657500`, `cLHS_pos : 0 < cLHS`.
- `qMT_eq : 262/131500 = 131/65750`.
- `record9_constant_identity : (H − 131/65750)·657500 = 657500·H − 1310` (the 657500/65750=10
  engine).
- `c9Const_eq : c9Const = (H_MT − q)/cLHS` with `c9Const = (657500·H_MT − 1310)/655001`.

`record_c9` (O4 form):
> `∀ε>0, ∃T₀, ∀T ≥ T₀, (c9Const − ε)·N(T,2T) ≤ N₀ˢ(T,2T)`
is proved as a corollary of `chain9_eps` (run at rescaled slack ε·cLHS, cancel the positive
cLHS), giving the liminf N₀ˢ/N ≥ C₉ = 0.673066472675939665848…

## Machine evidence summary

- `lake env lean Record9/Chain9.lean` (from the snapshot working dir, pinned
  v4.33.0-rc2): **exit 0**, no sorry/admit/axiom.
- `lake env lean` probe appending `#check Zeta23.ThmD.chain9_eps / CERTIFIED_F8_GE / F8 /
  stability_eps / stability_averaged_eps / record_c9 / c9Const / chain9_algebra_core`:
  **exit 0**; printed types match the contract (see the check transcript in
  `lean-proof/Record9/` build log).
- `lake build Record9.M1Baseline`: **exit 0** (8838 jobs; replays snapshot + builds the
  plumbing).
- Snapshot `literature/raw/zeta-23-lean/lakefile.toml`: **unchanged** (see lakefile-change.md).

## Status label for this pass

**MACHINE_ACCEPTED_PENDING_AUDIT** — the algebra and statement chain (T1a/T1b/T1d) compile
with zero sorry/axiom; the analytic bridge (T1c) is carried as explicit hypotheses and the
certificate (T2) is separate. Fidelity is recorded but the final independent audit is
pending (see the lean-verify workflow's separate audit pass).
