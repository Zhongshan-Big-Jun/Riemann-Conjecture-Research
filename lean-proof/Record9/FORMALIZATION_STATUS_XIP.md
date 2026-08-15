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
| `Record9.XiPrimeAtOne` | `Record9/XiPrimeAtOne.lean` | **M3-open-A (stretch)** the AtOne certificate: `IvMT`, `aMT`, `bMT`, `vConvMTcl`, `J1MT`, `kappaXiOne_MT`, and the honest-bridge sandwiches `kappaXi_one_vMT_mem` (κ₉ ≤ κ₁(1,vMT) ≤ κ₉ + ε₉) and `H_xip_vMT_mem` (sharp H range), with the closed-form/Fubini facts carried as explicit axiom-free hypotheses |

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
| **M3 — ξ′ record statement** (`H_xip`, `c9ConstXip`, `cLHSxip`/`qXip`/identities, `xiChain` bridge, `record_c9xip`) | **DONE (statement + algebra)** | exit 0; c9ConstXip decimal verified mpmath ≥ 40 dp | the AtOne κ₁(1,vMT) certificate (next row) and the ξ′ chain `xiChain` are OPEN (carried as hypothesis) |
| **M3-open-A — AtOne certificate** (`Record9.XiPrimeAtOne`: `IvMT`, `aMT`, `bMT`, `vConvMTcl`, `J1MT`, `kappaXiOne_MT`; `kappaXi_one_vMT_mem : kappaXi 1 vMT ∈ Icc κ₉ (κ₉+ε₉)`; `H_xip_vMT_mem`) | **DONE (math sandwich + Lean honest bridge)** | `lake build Record9.XiPrimeAtOne` exit 0; no sorry/admit/axiom; ARB enclosure of κ₉ = 1.132111133800997 ± 2·10⁻¹⁶; `H ∈ [2−(κ₉+ε₉), 2−κ₉]` contains canonical 0.867888865199… (|H−canonical| ≈ 10⁻⁵⁶) | the closed-form/Fubini facts (∫vMT=IvMT, ∫vMT²=aMT, vConv vMT=vConvMTcl, 2∫₀¹vConv vMT=(∫vMT)², 0<IvMT) and the jWin(D1trunc9)=J1MT integral mechanics are **carried as explicit axiom-free hypotheses** (open obligations below); formal Lean proofs of these analystic facts are a later pass |

**Status label:** `MACHINE_ACCEPTED_PENDING_AUDIT` — the modules `Record9.XiPrimeMT` and
`Record9.XiPrimeAtOne` compile with `lake build` exit 0 and no sorry/admit/axiom; M1+M2 (the
AdmWindow instance and the zero side) are fully machine-checked; M3's statement and algebra
compile; **M3-open-A (the AtOne κ₁(1,vMT) certificate) is DONE at the math level (ARB sandwich
κ₉ ≤ κ₁ ≤ κ₉+ε₉, H ∈ [2−(κ₉+ε₉), 2−κ₉] contains the canonical 0.867888865199… to ~10⁻⁵⁶) and its
Lean honest bridge compiles**, with the closed-form/Fubini content carried as explicit
axiom-free hypotheses; the ξ′ analytic/pressure/window-constant content (the `xiChain`) is
carried as an explicit hypothesis.

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

1. **M3-open A — the AtOne certificate content for v_MT.** ✅ **sandwich proven (math) and the
   Lean honest bridge compiled** (`Record9.XiPrimeAtOne`): the constants
   - `∫_{−1/2}^{1/2} vMT s ds = IvMT = √2·sin(1/√2) = 0.91872536986556843778…`
     (⚠ older `FORMALIZATION_STATUS_XIP.md` text had `…843826` — a **transcription typo**; the
     true value `…437784` is confirmed by closed form, quadrature, and machine_check.log's
     `K(0) = √2·sin(1/√2)`),
   - `∫ vMT² = a_MT = 1/2 + sin(√2)/(2√2) = 0.84922799931830417992…` (blueprint `a`),
   - `∫ vMT⁴ = b_MT = 3/8 + sin(√2)/(2√2) + sin(2√2)/(16√2) = 0.73784297545060818785…` (blueprint `b`;
     **b is ∫v⁴**, re-confirmed by closed form + quadrature),
   - `vConv vMT r = ½(1−r)cos(√2r) + sin(√2(1−r))/(2√2)` (closed form; agrees with quadrature at
     r ∈ {0.1,0.2,0.25,0.5,0.75} to 40 dp; r=1/4: 0.6603439026705667…, r=1/2: 0.4197424917352996…),
   - **J1 = 2∫₀¹ D1trunc9·vConv vMT = 0.10633754139274846 ± 2·10⁻¹⁶** (ARB),
   - **κ₉ = (aMT+J1)/(IvMT)² = 1.132111133800997 ± 2·10⁻¹⁶**, and the certified sandwich
     `κ₉ ≤ κ₁(1,vMT) ≤ κ₉ + ε₉` with `ε₉ = 1024/2990212875` (from `Certificate/D1.lean`) —
     giving `H_xip = 2 − κ₁(1,vMT) ∈ [2−(κ₉+ε₉), 2−κ₉]`, which **contains** the canonical
     `0.8678888651990519355503147104203403132225704976166306446…` (cross-check |H−canonical| ≈ 10⁻⁵⁶).
   - **Lean:** `Record9.XiPrimeAtOne` declares `IvMT/aMT/bMT/vConvMTcl/J1MT/kappaXiOne_MT`,
     `kappaXi_one_vMT_mem` and `H_xip_vMT_mem` (honest bridge), `lake build Record9.XiPrimeAtOne`
     exit 0, no sorry/admit/axiom.
   - **REMAINING OPEN (formal Lean proofs of the analytic facts, currently carried as explicit
     axiom-free hypotheses `vConvMT_closed`, `two_integral_vConv_vMT`, `integral_vMT_forms`,
     `IvMT_pos`, `jWin_D1_one_vMT_sandwich`):**
     (a) `∫vMT = IvMT`, `∫vMT² = aMT` (trig integral evaluations);
     (b) `vConv vMT = vConvMTcl` on [0,1] (product-to-sum closed form);
     (c) `2∫₀¹ vConv vMT = (∫vMT)²` (Fubini);
     (d) `0 < IvMT` (⟺ `vConv vMT ≥ 0` on [0,1], sandwich sign);
     (e) `jWin(D1trunc 9, 1, vMT) = J1MT` and the D₁-certificate jWin sandwich (integral mechanics).
     A later pass may promote these to real lemmas (they are all elementary/known results).
2. **M3-open B — the ξ′ chain `xiChain`.** A Lean proof of the ε-form chain for the ξ′ zeros
   (the pressure method + stability of `reports/xi-prime-pressure-method.md`), mirroring T1's
   `stability_eps`/`stability_averaged_eps` open bridges. `record_c9xip` is conditional on it.
3. **M1-open C — the four §1 profile L¹-norms as Lean lemmas** (paper constants, not AdmWindow
   fields): ‖v′‖₁ = 2(1−cos(1/√2)) ≤ 1/2, ‖(v²)′‖₁ = 1−cos(√2) ≤ 38/45, ‖v″‖₁ = 2√2·sin(1/√2) ≤ 2,
   ‖(v²)″‖₁ = 2√2·sin(√2) ≤ 4. Not required by `admWindow_phiM`/`windowZeroSide_atV_of`.

No sorry/admit/axiom appear in any Record9 file (all `kappaXi_one_vMT_mem`, `H_xip_vMT_mem`,
`J1MT`, `kappaXiOne_MT` depend only on the base axioms [propext, Classical.choice, Quot.sound]
— verified by `#print axioms`). The snapshot `literature/raw/zeta-23-lean/` is unchanged (HEAD
pristine; only the extension project `lean-proof/Record9/` was edited). Modules
`Record9.Chain9`, `Record9.M1Baseline`, and `Record9.XiPrimeMT` are untouched; the new
`Record9.XiPrimeAtOne` adds the M3-open-A certificate (math + honest Lean bridge).
