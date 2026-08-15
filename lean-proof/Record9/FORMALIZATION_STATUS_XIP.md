# ξ′ AdmWindow formalization status — Record9 extension (Stage C, T3)

**Target contract:** instantiate the Lean `AdmWindow` for the Montgomery–Taylor profile
`v_MT(s) = cos(√2·s)` on |s| ≤ 1/2 with ModFactor `f_c(u) = √(cos(√2·u/L))`, parameters
**A = 1, B = 2, c = cRho + 4** (better than the quartic's cRho + 15.75); the zero side
`windowZeroSide_atV` for the MT profile; and the ξ′ record statement `record_c9xip`.

**Source:** `reports/admwindow-cos-instance.md` (§1 profile, §2 ModFactor), the quartic template
(`Zeta23/XiPrime/QuarticWindow/{Quartic,ModWindow,Params,ZeroSide}.lean`,
`Zeta23/XiPrime/Certificate/AtOne.lean`), and the T1 chain
(`Record9.Chain9`).

**Module (new file in the extension project only; snapshot pristine):**

| Module | Source (in `lean-proof/Record9/`) | Content |
|---|---|---|
| `Record9.XiPrimeMT` | `Record9/XiPrimeMT.lean` | **M1** vMT profile + ModFactor A=1,B=2 + admWindow_phiV_MT (c=cRho+4); **M2** aV_range_MT + windowZeroSide_atV_MT; **M3 (stretch)** H_xip, c9ConstXip, xiChain (bridge), record_c9xip |

Declarations are in `namespace Zeta23.XiPrime` (full names `Zeta23.XiPrime.*`), mirroring the
snapshot XiPrime files.

---

## Status summary

| Obligation | Status | Machine evidence | Remaining gap |
|---|---|---|---|
| **M1a — v_MT profile** (`vMT`, `vMT_even`, `vMT_core_ge` ≥ 3/4, `vMT_le_one`, `vMT_contDiff`) | **DONE** | `lake env lean` exit 0 | (four §1 profile L¹-norms are paper constants, NOT AdmWindow fields — see note below) |
| **M1b — ModFactor instance** (`fc`, `hc`, `hc_core_ge/pos`, `fc_antitoneOn`, `fc_contDiffOn`, `abs_deriv_fc_le` ≤ 1/L, `abs_deriv2_fc_le` ≤ 2/L², `modFactor_fc : ModFactor (fc L) L 1 2`) | **DONE** | exit 0 | — |
| **M1c — the AdmWindow witness** (`cMT`, `phiV_MT_eq` (rfl), `admWindow_phiV_MT : AdmWindow (P.phiV vMT T) (P.L T) P.w (cMT P.ϱ)`, `cMT_eq : cMT ϱ = cRho ϱ + 4`) | **DONE** | exit 0 | `cMT P.ϱ = cRho ϱ + 1 + 1² + 2 = **cRho + 4**`, strictly better than quartic's cRho + 15.75 |
| **M2 — zero side** (`atV_MT_a_eq_av`, `phiV_MT_sq_ge`, `aV_range_MT` (1/2 ≤ a ≤ 1), `eventually_aV_range_MT`, `poissonSqV_MT`, `blockInputsV_MT`, `eventually_blockInputsV_MT`, `GzGpV_MT`, `eventually_GzGpV_MT`, `eventually_tailPackageV_MT`, `windowZeroSide_atV_MT : WindowZeroSide Z P (P.atV vMT)`) | **DONE** | exit 0 | — |
| **M3 — ξ′ record statement** (`H_xip`, `c9ConstXip`, `cLHSxip`/`qXip`/identities, `xiChain` bridge, `record_c9xip`) | **DONE (statement + algebra)** | exit 0; c9ConstXip decimal verified mpmath ≥ 40 dp | the AtOne κ₁(1,vMT) certificate (below) and the ξ′ chain `xiChain` are OPEN (carried as hypothesis) |

**Status label:** `MACHINE_ACCEPTED_PENDING_AUDIT` — the module `Record9.XiPrimeMT`
compiles with `lake env lean` exit 0 and no sorry/admit/axiom; M1+M2 (the AdmWindow instance and
the zero side) are fully machine-checked; M3's statement and algebra compile, with the ξ′
analytic/pressure/window-constant content carried as explicit hypotheses.

---

## M1 — the v_MT admissible profile + ModFactor (core of this pass)

- `vMT s := Real.cos (Real.sqrt 2 * s)`.
- **v_MT structure** (even, `vMT_core_ge` ≥ 3/4 on [−1/2,1/2] via
  `Real.one_sub_sq_div_two_le_cos` with |√2s| ≤ 1/√2, `vMT_le_one` via `Real.cos_le_one`,
  `vMT_contDiff`). These are the fields the zero side's `P.atV vMT` and `wV_*` need.
- **ModFactor:** `hc L u := cos(√2·u/L) = vMT(u/L)`, `fc L u := √(max 0 (hc L u))`. On the core
  |u| ≤ L/2 the `max 0` is inert (cos ≥ 3/4 > 0), so `fc` equals the blueprint's `√(cos(√2·u/L))`
  there; the `max 0` matches `P.phiV`'s definition, so `P.phiV vMT T = phiM (fc (P.L T)) …`
  holds **by rfl** (as the quartic). Proven:
  - `fc_even`, `fc_nonneg`, `fc_le_one`, `fc_antitoneOn` (cos antitone on [0,π], arg ≤ 1/√2 < π),
  - `fc_contDiffOn` on `Ioo (-(L/2+L/10)) (L/2+L/10)` (cos > 0 there, √ smooth),
  - **|f_c′| ≤ 1/L** (`abs_deriv_fc_le`): f_c = h_c/(2f_c), |h_c′| ≤ 1/L, 2f_c ≥ √3 ≥ 1.
  - **|f_c″| ≤ 2/L²** (`abs_deriv2_fc_le`): f_c″ = (h_c″ − 2 f_c′²)/(2f_c), with the sharper
    `2f_c′² = h_c′²/(2h_c)` giving |f_c″| ≤ 8/(3√3 L²) < 2/L² (blueprint B = 2).
  - `modFactor_fc : ModFactor (fc L) L 1 2` → **A = 1, B = 2**.
- **AdmWindow witness:** `admWindow_phiM modFactor_fc` gives
  `AdmWindow (P.phiV vMT T) (P.L T) P.w (cMod P.ϱ 1 2)` with
  `cMT ϱ := cMod ϱ 1 2 = Taper.cRho ϱ + 1 + 1² + 2 = cRho ϱ + 4` (proven `cMT_eq`).

### Fidelity note on the four §1 profile L¹-norms

The blueprint §1 rows ‖v′‖₁ ≤ 1/2, ‖(v²)′‖₁ ≤ 38/45, ‖v″‖₁ ≤ 2, ‖(v²)″‖₁ ≤ 4 are **paper
constants** (closed forms 2(1−cos(1/√2)), 1−cos(√2), 2√2·sin(1/√2), 2√2·sin(√2); verified at
40 dp in the math log). They are **NOT structurally required** by the modulated AdmWindow path:
the snapshot's `admWindow_phiM` bounds the window's L¹-derivative norms through the factor's
`A,B` (ModWindow.lean `integral_abs_deriv2_phiM_le`, `integral_abs_deriv2_phiM_sq_le`)
— see `reports/admwindow-cos-instance.md` §1 note and WindowCore.lean:31-43. Hence they are
recorded as **paper-level profile-norm obligations** (not Lean AdmWindow fields), consistent
with the snapshot's own quartic instance (which also does not prove its four §1 norms in Lean).
If a later pass needs them as Lean lemmas, the proofs reduce to evaluating `∫|−√2 sin|`,
`∫|−√2 sin(2√2·)|` on [−1/2,1/2] via the closed forms — OPEN (see open obligations).

---

## M2 — the MT zero side

Mirrors the quartic instance (`ZeroSide.lean §2`):
- `phiV_MT_sq_ge : 3/4·P.phi T u² ≤ P.phiV vMT T u²` (v_MT ≥ 3/4 on core; off support both 0).
- `aV_range_MT : 1/2 ≤ (P.atV vMT T).a T ≤ 1` at 8w ≤ L: av ≥ (3/4)(1 − 2w/L) ≥ (3/4)(3/4) =
  9/16 ≥ 1/2 (profile a_MT = 1/2 + sin(√2)/(2√2) = 0.84922799…, verified).
- `windowZeroSide_atV_MT : WindowZeroSide Z P (P.atV vMT)`
  via `windowZeroSide_atV_of` with `vMT_even` + `admWindow_phiV_MT` + `eventually_aV_range_MT`.

---

## M3 (stretch) — the ξ′ record statement

- `H_xip : ℝ := 2 - kappaXi 1 vMT` (= 0.86788886519905193555…).
- `c9ConstXip : ℝ := (657500 * H_xip - 1310) / 655001` (= 0.86920009109661916184…,
  computed at 40 dp: 0.869200091096619161839638412765782036974, matches the paper value to
  >40 digits).
- Exact algebra identities machine-checked: `record9xip_constant_identity : (H − 131/65750)·657500
  = 657500·H − 1310`, `c9ConstXip_eq : c9ConstXip = (H_xip − qXip)/cLHSxip` with `qXip = 262/131500`,
  `cLHSxip = 655001/657500 > 0`.
- `xiChain : Prop := ∀ε>0 ∃T₀ ∀T≥T₀, (1 − 2499/2500/263)·N₀ˢ_ξ′(T,2T)
  ≥ (H_xip − 262/131500 − ε)·N_ξ′(T,2T)` — the ξ′ chain in ε-form, carried **as an explicit
  axiom-free hypothesis** (mirrors T1's `record9Bridge`; the ξ′ chain's analytic/pressure/
  window-constant content is open and NOT tied here).
- `record_c9xip (b : xiChain) : ∀ε>0 ∃T₀ ∀T≥T₀, (c9ConstXip − ε)·N_ξ′(T,2T) ≤ N₀ˢ_ξ′(T,2T)`
  — the ε-form record corollary, proved by the same cancellation algebra as T1's `record_c9`
  (run the chain at ε·cLHSxip, cancel the positive cLHSxip).
- `Ncount = N_{ξ′}` with multiplicity, `N0simple = N₀ˢ_{ξ′}` simple-on-line (the ξ′ counts of
  `Zeta23/XiPrime/Defs.lean`).

---

## Open obligations (exact statements, not fabricated)

1. **M3-open A — the AtOne certificate content for v_MT.** The sandwich `κ₉ ≤ κ₁(1, vMT) ≤ κ₉ + ε₉`
   together with the exact rational certifices for the v_MT profile. Required concrete inputs
   (math-lvl, verified 40 dp):
   - `∫_{−1/2}^{1/2} vMT s ds = 0.91872536986556843826…`,
   - `∫ vMT² = a_MT = 1/2 + sin(√2)/(2√2) = 0.84922799931830417992…`,
   - `∫ vMT⁴ = b_MT = 3/8 + sin(√2)/(2√2) + sin(2√2)/(16√2) = 0.73784297545060818785…`,
   - `vConv vMT r = ∫ vMT(s)vMT(s+r)` (e.g. r=1/4: 0.6603439026705667…, r=1/2: 0.4197424917352996…),
   - the `D1trunc 9 ≤ D₁ ≤ D1trunc 9 + ε₉` sandwich (`Certificate/D1.lean`), giving `H_xip = 2 − κ₁(1,vMT)`.
   This formalizes `H_xip`'s value in Lean (mirror `AtOne.lean` `kappaXi_one_vQuartic_mem`).
2. **M3-open B — the ξ′ chain `xiChain`.** A Lean proof of the ε-form chain for the ξ′ zeros
   (the pressure method + stability of `reports/xi-prime-pressure-method.md`), mirroring T1's
   `stability_eps`/`stability_averaged_eps` open bridges. `record_c9xip` is conditional on it.
3. **M1-open C — the four §1 profile L¹-norms as Lean lemmas** (paper constants, not AdmWindow
   fields): ‖v′‖₁ = 2(1−cos(1/√2)) ≤ 1/2, ‖(v²)′‖₁ = 1−cos(√2) ≤ 38/45, ‖v″‖₁ = 2√2·sin(1/√2) ≤ 2,
   ‖(v²)″‖₁ = 2√2·sin(√2) ≤ 4. Not required by `admWindow_phiM`/`windowZeroSide_atV_of`.

No sorry/admit/axiom appear in any Record9 file. The snapshot
`literature/raw/zeta-23-lean/` is unchanged (HEAD pristine; only the extension project
`lean-proof/Record9/` was edited). Module `Record9.Chain9` and `Record9.M1Baseline` are untouched.
