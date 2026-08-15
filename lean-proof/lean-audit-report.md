# Lean 4 Independent Audit Report — O1 (baseline) statement fidelity

**Verdict: FORMALLY_VERIFIED (O1 fidelity + independence pass)**
**Role:** INDEPENDENT VERIFIER (adversarial auditor; no shared chain of thought with formalizer)
**Obligation under audit:** O1 — `Zeta23.ThmD.thmD₀_simple_mult` (+ `'`, `_cumulative`) faithful-ness of the Lemma-D baseline: ∀ε>0 ∃T₀ ∀T≥T₀: (H_MT − ε)·N(T,2T) ≤ N₀ˢ(T,2T), H_MT = 3/2 − (1/√2)·cot(1/√2).
**Snapshot:** `F:\LaTeX\Riemann Conjecture\literature\raw\zeta-23-lean`; toolchain `leanprover/lean4:v4.33.0-rc2`; lake-manifest sha256 `491590487526a398…`.
**Audit date:** this session.

---

## 0. Environment / reproducibility pins (Phase 0)

- `lean --version` (project cwd, elan): **Lean 4.33.0-rc2**, commit `d8b18978322de05a8f3dba51ef03cf5461676c17` — matches `machine_check.log` and `run-manifest.json` recorded environment. (Default elan toolchain is 4.31.0, but the project `lean-toolchain` correctly pin 4.33.0-rc2, and `lake env lean` from the project cwd resolves to it.)
- `lake env lean` on the audit scratch probe resolved the pinned toolchain correctly.
- **Git commit discrepancy (documented, non-fatal):** the obligation map / machine_check.log / verification.json / run-manifest record snapshot commit `@3635e748`. That object does **not** exist in the current repo; the actual HEAD is `49691a5` ("Stage C housekeeping: O1 baseline machine evidence complete (lake build Zeta23 exit 0, 9010 jobs; #print axioms gold standard clean)"). The `3635e748` identifier appears to be a stale / pre-rebase identifier for the same content. **Binding evidence that the audited files ARE the machine-built files:** the sha256 of every file I read matches byte-for-byte the hash recorded in `lean-proof/run-manifest.json` for that path (Mult.lean `35ACEA86…`, Statement.lean `C9FC4B6F…`, Functional.lean `B8E084C…`, Limit.lean `1D05E40E…`, Defs/Counting.lean `A244E8A4…`, Statement/SeamClosed.lean `3B379EC9…`, Main.lean `9AB521E4…`, Final.lean `D92D44CC…` all match). So the substance is bound even though the documented commit token is stale.

**Files read (recorded):**
1. `lean-proof/verification-contract.md`
2. `lean-proof/obligation_map.md`
3. `lean-proof/machine_check.log`
4. `lean-proof/run-manifest.json`
5. `lean-proof/verification.json`
6. `literature/raw/zeta-23-lean/lean-toolchain`
7. `literature/raw/zeta-23-lean/Zeta23/ThmD/Mult.lean`
8. `literature/raw/zeta-23-lean/Zeta23/ThmD/Functional.lean`
9. `literature/raw/zeta-23-lean/Zeta23/ThmD/Limit.lean`
10. `literature/raw/zeta-23-lean/Zeta23/Defs/Counting.lean`
11. `literature/raw/zeta-23-lean/Zeta23/Statement.lean`
12. `literature/raw/zeta-23-lean/Zeta23/Statement/SeamClosed.lean`
13. `literature/raw/zeta-23-lean/Zeta23/Main.lean`
14. `literature/raw/zeta-23-lean/Zeta23/Final.lean`
15. Scratch probe `Zeta23/VerifyAudit.lean` (created for `#print axioms`, deleted after use)

Environment checks run: `lake env lean --version`, `elan show`, `git rev-parse HEAD`, `git cat-file -t 3635e748` (absent), sha256 file binding, and a fresh `lake env lean` `#check` + `#print axioms` probe.

---

## Per-obligation results

### O1a — Definitions (N0simple = simple-on-line; Ncount with multiplicity) — **FAITHFUL**

Evidence:
- `N0simple T₁ T₂ = (zerosIn T₁ T₂ ∩ {ρ | ρ.re = 1/2} ∩ {ρ | zeroMult ρ = 1}).ncard` — `Zeta23/Statement.lean:62`.
  - `zerosIn T₁ T₂ = {ρ | IsNontrivialZero ρ ∧ T₁ < ρ.im ∧ ρ.im ≤ T₂}` (`Statement.lean:46`) — the half-open ordinate window `(T₁, T₂]`, matching the dyadic `(T,2T]` convention.
  - `{ρ | ρ.re = 1/2}` = the critical line Re s = ½. `{ρ | zeroMult ρ = 1}` = simple (multiplicity exactly 1; `zeroMult` = analytic order of ζ at ρ, `Statement.lean:43`).
  - `.ncard` counts **distinct** simple-on-line zeros. Because each counted point has `zeroMult = 1`, the distinct count equals the with-multiplicity count for this subset (each simple zero contributes exactly 1). No multiplicity is dropped: the simple condition `zeroMult = 1` is applied, so N₀ˢ is exactly the paper's "number of simple zeros on the critical line."
- `Ncount T₁ T₂ = ∑ᶠ ρ ∈ zerosIn T₁ T₂, zeroMult ρ` (`Statement.lean:49`) — a finsum over multiplicities: counts **all** nontrivial zeros **with multiplicity**, matching the paper's N.
- The abstract-seam bridge is faithful: `zetaZeros_N0s : (zetaZeros hs).N0s T₁ T₂ = N0simple T₁ T₂` (`Statement.lean:115`) and `zetaZeros_N : … = Ncount` (`Statement.lean:107`) — the abstract `ZeroConfig` simple-on-line count is definitionally the concrete `N0simple`. `SeamClosed.lean:35-38` gives the same for `zetaZeroConfig`.
- Window positivity: `IsNontrivialZero ρ := riemannZeta ρ = 0 ∧ 0 < ρ.re ∧ ρ.re < 1` (`Statement.lean:38`) = nontrivial zeros in the open critical strip, with positive ordinate (via `zerosIn` requiring `T₁ < ρ.im`; the paper's N counts the upper-half zeros). No sign/|| symmetry mismatch: the paper's N(T,2T) indeed counts positive-ordinate zeros on (T,2T].
- **No mismatch found.** N0simple is simple-on-line with-multiplicity-coinciding count; Ncount is with multiplicity. Conventions match the O1 contract.

### O1b — Quantifier / shape — **FAITHFUL**

Evidence: `Mathlib`-printed statement of `thmD₀_simple_mult` (from the audit probe `#check`):
```
(ε : ℝ) : ε > 0 → ∃ T₀, ∀ T ≥ T₀, (ThmD.HD 1 - ε) * ↑(Ncount T (2 * T)) ≤ ↑(N0simple T (2 * T))
```
- ∀ε>0, ∃T₀:ℝ, ∀T≥T₀ (T real, `Ncount T (2*T)` is ℕ cast to ℝ) — matches the contract's ε-form exactly.
- Window is `(T, 2*T]` (via `zerosIn T (2*T)`), NOT `(0,T]`; no switch.
- No hidden change of quantifier domain: T is ℝ (the comparison `T ≥ T₀` is over reals; `Ncount`/`N0simple` take real bounds).

### O1c — Constant (HD 1 = 3/2 − cot(1/√2)/√2) — **FAITHFUL**

Evidence:
- `thmD₀_simple_mult'` (Mult.lean:441-445) states the constant **written out** as
  `3 / 2 - (Real.sqrt 2)⁻¹ * (Real.cos (Real.sqrt 2)⁻¹ / Real.sin (Real.sqrt 2)⁻¹)`.
  Literal reading: `(√2)⁻¹` = 1/√2 appears as the argument of both cos and sin; `cos(θ)/sin(θ)` = cot θ; whole term = `(1/√2)·cot(1/√2)`. So `3/2 − (1/√2)·cot(1/√2)`. Sign (−), division (1/√2 outside, cot inside), and argument ((√2)⁻¹ = 1/√2) all match the paper's H_MT. ✓
- Proof is `rw [← HD_one]; exact thmD₀_simple_mult` (`Mult.lean:445`), so `'` is definitionally the same real number as the `HD 1` form.
- `HD_one : HD 1 = 3/2 - (√2)⁻¹ * (cos (√2)⁻¹ / sin (√2)⁻¹)` — `Zeta23/ThmD/Functional.lean:464-465`. This ties `HD 1` (= `2 - 1/cStar 1`, `Functional.lean:53`; `cStar 1 = √2·sin(1/√2)/(cos(1/√2)+(1/√2)·sin(1/√2))`, `Functional.lean:35-36`) to the cot form. Numeral consistency with the paper's `2 − 1/c₁* = 3/2 − cot(1/√2)/√2` is asserted and machine-checked.
- **Location note (documentation nit, not a fidelity issue):** the obligation map claimed `HD_one` lives in `ParamsD.lean`; it is actually in `Functional.lean:464`. `ParamsD.lean` contains the window-realizing parameter family (atD), not `HD_one`. The map's substance (HD 1 identity) is correct; only the file pointer is off.

### O1d — Unconditionality — **FAITHFUL**

Evidence:
- `thmD₀_simple_mult` has **no explicit hypotheses**; the only argument is `ε` (confirmed by `#check`).
- It instantiates `paperInputs_zeta` (`Final.lean:291`: `PaperInputs zetaZeroConfig := PaperInputs.of_EF zetaEF` — constructed, not assumed) and `zetaSeam` (`SeamClosed.lean:22`: `theorem zetaSeam : ZetaSeam := ZetaSeam.of_reflect zeta_reflect_zero zeta_mult_reflect` — a **theorem** with no hypotheses; the file header states the four `ZetaSeam` fields are all discharged Mathlib theorems: `one_le_mult`, `finite_window` from Seam.lean, `reflect_zero`, `mult_reflect` from ZetaReflect.lean).
- `zetaZeroConfig := zetaZeros zetaSeam` (`SeamClosed.lean:26`) is therefore a hypothesis-free object.
- No assumption on RH, no `paperInputs`-as-assumption, no conjecture. Unconditional.

### O1e — Cumulative form — **FAITHFUL**

Evidence:
- `thmD₀_simple_mult_cumulative : ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀, (HD 1 - ε) * (Ncount 0 T : ℝ) ≤ N0simple 0 T` (`Mult.lean:468-471`), printed by `#check` as `(HD 1 - ε) * ↑(Ncount 0 T) ≤ ↑(N0simple 0 T)`.
- This is the liminf-over-(0,T] form. Correct seam: derived via `cumulative_of_dyadic zetaSeam paperInputs_zeta.RvM (fun _ _ _ => N0simple_add' zetaSeam)` (`Mult.lean:470`). `cumulative_of_dyadic` (`Main.lean:51-63`) converts the dyadic ε-form into the cumulative ε-form using interval additivity of `f` and the Riemann–von Mangoldt asymptotic `(tendsto_Ncount_zero_atTop hs hR)` — it needs `paperInputs_zeta.RvM` (a RiemannVonMangoldt instance), which is part of the (constructed, unconditional) `PaperInputs`. Seam convention consistent with the dyadic-based liminf claim.
- `N0simple_add'` (`Main.lean:69-71`) gives the interval additivity of `N0simple`; consistent.

### O1f — Non-circularity / axiom set — **FAITHFUL**

Evidence:
- Mult.lean imports are `Zeta23.ThmD.Final`, `Zeta23.Assembly.SeamMult`, `Zeta23.FinalMult` (Mult.lean:16-18). None is in the `PairCeiling` layer; `Final.lean` (imported transitively) does not pull assumption-bound results into the headline axiom set.
- **Independent `#print axioms` probe** (fresh scratch `Zeta23/VerifyAudit.lean`; `lake env lean`, toolchain v4.33.0-rc2, HEAD `49691a5`; run by this auditor, then scratch deleted):
  - `Zeta23.ThmD.thmD₀_simple_mult` → `[propext, Classical.choice, Quot.sound]`
  - `Zeta23.ThmD.thmD₀_simple_mult'` → `[propext, Classical.choice, Quot.sound]`
  - `Zeta23.ThmD.thmD₀_simple_mult_cumulative` → `[propext, Classical.choice, Quot.sound]`
  - `Zeta23.ThmD.HD_one` → `[propext, Classical.choice, Quot.sound]`
- This **independently confirms** the gold standard recorded in machine_check.log / verification.json, and confirms that the tactic-test axioms `qc`/`hqc` (AdditiveCombination.lean:183-184) — while present in a source file reachable by import — appear in **no** headline theorem's axiom set. Non-circularity: the baseline uses no conjecture and no record theorem.

---

## Critical errors / gaps

- **None for O1.** All six sub-obligations are FAITHFUL, with the axiom-set gate independently re-closed at the exact pinned toolchain.
- **Documentation/reproducibility nits (non-fatal, worth correcting):**
  1. Stale snapshot commit token `@3635e748` in `obligation_map.md`, `machine_check.log`, `verification.json`, `run-manifest.json`; the real HEAD is `49691a5` and `3635e748` is not a valid git object. Content binding to the machine build is nevertheless established via byte-identical file hashes against `run-manifest.json`.
  2. `HD_one` is located in `Zeta23/ThmD/Functional.lean:464`, not `ParamsD.lean` as the obligation map states.
  3. The `#print axioms` probe I ran is independent evidence; the scratch file I used was deleted after the run (no artifact pollution).

## Repair hints

- (Reproducibility only, no proof change needed.) Re-tag the snapshot with the actual commit `49691a5` (or record it in the run manifest) and re-point the `HD_one` reference to `Functional.lean:464`. Optionally note that the default elan toolchain is 4.31.0 while the project build uses 4.33.0-rc2 — the project `lean-toolchain` already pins this, so a rebuilt `lake build` resolves correctly from the project cwd.
- No Lean file was modified during this audit.

## Statement-fidelity summary table

| Obl | Contract statement | Verdict | Evidence |
|---|---|---|---|
| O1a | N₀ˢ = simple-on-line count; Ncount = with multiplicity; (T,2T] | **FAITHFUL** | Statement.lean:46,49,62; SeamClosed.lean:35 |
| O1b | ∀ε>0 ∃T₀ ∀T≥T₀ (T real), dyadic window | **FAITHFUL** | Mult.lean:435-436; #check |
| O1c | HD 1 = 3/2 − (1/√2)cot(1/√2) | **FAITHFUL** | Functional.lean:464-465; Mult.lean:441-445 |
| O1d | Unconditional | **FAITHFUL** | SeamClosed.lean:22,26; Final.lean:291 |
| O1e | Cumulative (0,T] form, seam consistent | **FAITHFUL** | Mult.lean:468-471; Main.lean:51-63,69 |
| O1f | Non-circular; axioms = {propext, choice, Quot.sound} | **FAITHFUL** | #print axioms probe; Mult.lean:16-18 |

---

# T1 verifier pass (independent) — chain9_eps / record_c9 (Stage C, lean-verify)

**Role:** INDEPENDENT VERIFIER (fresh agent; no shared chain of thought with the T1 formalizer).
**Obligations audited:** T1a (statement), T1b (algebra core + ε-lift), T1c (bridge honesty),
T1d (constant identities + record_c9), O2 (chain), O4 (liminf record). O1 (baseline) is already
FORMALLY_VERIFIED and NOT re-audited here. T2 (certificate `F₈ ≥ 392/100000`) is out of scope.
**Machine evidence:** `lean-proof/machine_check.log` → "T1 ... INDEPENDENT verifier pass".
**Audit date:** this session (2026-08-16). **Sources audited:** `lean-proof/Record9/Record9/Chain9.lean`
(sha256 `45F22025535A7D81DA244E47EAC29BCF669E15A54CCAC73F8A18D440EE24635E`), `M1Baseline.lean`
(sha256 `F82345EEFA01B3C56CE9B75F7AD63AC1D4B1D71E9FAE023DBB7171C3AC7A645C`), both unchanged during audit.
Chain source for the pressure function / steps: `runs/…/R-20260814T045000Z-extpress-2f36ae/candidate_proof.general-k-derivation.md`.

## Machine evidence (exact commands + exit codes)

| Check | Result |
|---|---|
| `lean --version` (Record9 cwd, pinned v4.33.0-rc2) | **4.33.0-rc2** (d8b18978322de05a8f3dba51ef03cf5461676c17) |
| `lake build Record9.Chain9` | **exit 0** (8838 jobs; formalizer's BUILD_LOG claimed "killed after ~10 min" — here it completed in ~47s, so the module target builds cleanly) |
| `lake build Record9.M1Baseline` | **exit 0** (8838 jobs, 46s) |
| `lake env lean Record9/Chain9.lean` (authoritative module compile) | **exit 0** (only unused-`hF` linter warning) |
| scratch `#check`/`#print axioms` probe | **exit 0**; types match contract verbatim; all axioms = {propext, Classical.choice, Quot.sound} |
| sorry/admit/axiom scan, both .lean files | **0 real hits** (only header-comment word "axiom"; no declarations) |
| snapshot `git status --porcelain` | **empty at final check**; `lakefile.toml` byte-identical to HEAD (git diff exit 0) |

## Per-obligation fidelity results

### T1a — statement (`chain9_eps`, `CERTIFIED_F8_GE`, bridge hypotheses) — **FAITHFUL** (with one flagged kernel caveat, see 2)

1. **Quantifier order / shape.** `chain9_eps (hF : CERTIFIED_F8_GE) (b : record9Bridge) (ε : ℝ) :
   ε > 0 → ∃ T₀, ∀ T ≥ T₀, (1 − 2499/2500/263)·N₀ˢ(T,2T) ≥ (HD 1 − 262/131500 − ε)·N(T,2T)`.
   Matches the contract: `∀ε>0 ∃T₀ (T real) ∀T≥T₀`, dyadic window `(T, 2T]`, `N0simple`/`Ncount`
   are the baseline multiplicity/simple-on-line counts (verified in O1). **FAITHFUL.**
2. **Constants.** `1 − 2499/2500/263 = 1 − A₀/m` (by `cA0m_eq`, Chain9.lean:145); `262/131500 =
   (m−1)/(500m)` at m=263 (by `qMT_eq`, :154); `HD 1 = H_MT` (baseline `HD_one`, Functional.lean:464).
   `A₀ = 2499/2500 = (392/100000)·255 < 1` (rigor condition §4; `A0_lt_one` :142). **FAITHFUL.**
3. **Pressure-function structure `F8gaps` vs general-k §2 — re-derived.** Paper (k=9, 8 gaps,
   1-based) `F₈ = (1/[500·8])Σgᵢ + Σ_{s=1}^{8} (2/(9−s))Σ_{i=1}^{9−s} w(gᵢ+…+g_{i+s−1})`. Lean
   `F8gaps` (Chain9.lean:72-75) uses `s0 = s−1 ∈ 0..7`, coefficient `2/(8−s0) = 2/(9−s)`, inner
   window `Finset.range (8−s0) = 9−s` terms, `gapSpan g i (s0+1)` = `s` consecutive gaps from `i`
   (0-based) = paper's `gᵢ+…+g_{i+s−1}`. Linear term `1/(500·8)`. Total pair count
   `Σ_{s0=0}^7(8−s0) = 36 = C(9,2) = Σ_{s=1}^8 (9−s)` ✓. Sampled s0=0 (coeff 2/8, 8 windows w(gᵢ))
   and s0=7 (coeff 2/1, 1 window w(g₀+…+g₇)) both match. **No off-by-one. FAITHFUL** for the
   function skeleton.
4. **Kernel `wMT` — STRUCTURAL PLACEHOLDER (fidelity caveat, honestly declared).**
   `sincMT x = if x=0 then 1 else sin x/x`, `wMT x = (sincMT x)^2`. The paper's normalized MT
   overlap kernel is the baseline autocorrelation `Cfun lam L y = (L−y)/2·cos(ωy) + sin(ω(L−y))/(2ω)`,
   `ω = √2λ/L` (Window.lean:1211-1213, from `vStar = cos(√2λs)`, `theta λ = λ/√2`), NOT a plain
   squared sinc. `wMT` lacks the `√2λ/L` frequency scaling, the `cos(ω(L−y))` term, the `(L−y)/2`
   factor and the `1/√2`-structure. So `CERTIFIED_F8_GE` (`F8gaps wMT ≥ 392/100000`) is currently a
   statement about the placeholder kernel, not yet the paper's `F₈` for the true MT kernel. The
   formalizer is **explicit and honest** about this (Chain9.lean:55-57, 68-71 header; FORTALIZATION_
   STATUS "not assumed and not machine-tied … kernel-limit lemma … open analytic-bridge
   sub-obligation") — it is NOT presented as a proved fact. Classification: the pressure-function
   structure is FAITHFUL; the concrete kernel identity is an open analytic bridge (kernel-limit
   lemma). This is a **MINOR_PARAPHRASE / open-bridge** on the certificate content, not a silent
   misstatement. Error layer: **boundary-convention / dependency (open analytic input).**

### T1b — algebra core (`chain9_algebra_core`, ε-lift, `chain9_eps`) — **FAITHFUL**

Independently re-derived. From `S ≥ H·N + Δ − e₁·N` and `Δ ≥ (A₀/m)S − q·N − e₂·N` (A₀/m =
2499/657500, q = 262/131500) the add/collect gives `(1−A₀/m)S ≥ (H−q)N − (e₁+e₂)N`, i.e. the Lean
conclusion `(1 − 2499/2500/263)S ≥ (HD 1 − 262/131500)N − (e₁+e₂)N`. Chain9.lean:175-182 proves this
with `norm_num`+`ring_nf`+`set`+`linarith` (pure rational arithmetic — machine-checked). The ε-lift
`chain9_eps_from_hypotheses` (:188-210) splits ε = ε/2 + ε/2 across the two bridge hypotheses and
combines at `T₀ = max T₀₁ T₀₂`; `chain9_eps` (:219-223) is literally `chain9_eps_from_hypotheses b`.
No hidden assumption: the algebra and `record_c9` hold for arbitrary real S,N,D (`N ≥ 0` is not
required by any step; the `cLHS > 0` cancellation uses only nonnegativity of the multiplier).
**FAITHFUL.**

### T1c — bridge honesty (`stability_eps`, `stability_averaged_eps`, `deltaMT`) — **FAITHFUL (honest, non-circular, no weakening)**

1. `stability_eps` (:97-100) = `∀ε>0 ∃T₀ ∀T≥T₀, HD 1·N + deltaMT T − ε·N ≤ N0simple`, i.e. the
   paper step-2 / Cor 2.2 `S ≥ H_MT·N + Δ(M°) − o(N)` in ε-form (general-k §1). **Matches
   OpenAI Cor 2.2 form.**
2. `stability_averaged_eps` (:108-112) = `∀ε>0 ∃T₀ ∀T≥T₀, deltaMT T ≥ (2499/657500)·N0simple −
   (262/131500)·N − ε·N`, i.e. `Δ(M°) ≥ (A₀/m)·S − ((m−1)/(500m))·N − o(N)` — the block-defect +
   convexity-under-pinching averaging step (general-k §5-6 / [OpenAI (20)]). **Matches AV_k form
   exactly.**
3. **Non-circular / no trivially-implies-conclusion:** `deltaMT` is a free abstract placeholder
   `fun _ => 0` (:91) only quantified into the bridge conditions and never evaluated by the proofs.
   Neither bridge hypothesis alone nor their conjunction implies the conclusion without the
   (machine-proved) `chain9_algebra_core` step; `stability_averaged_eps` is a lower bound on Δ that
   the conclusion genuinely requires. **No silent weakening** (e.g., it does not directly assert
   `chain9_eps`). No `axiom` — the bridge is two `def : Prop` fields of `record9Bridge`.
4. **Non-circularity of the chain:** `chain9_eps` does NOT use `record_c9`; `record_c9` uses
   `chain9_eps` (intended corollary direction). Neither is used in the bridge statements (they have
   no proofs). **No circularity.**
5. **Honest scope:** the true physical Δ(M°(T)) is NOT machine-tied here; the bridge is declared
   over `deltaMT`. Formalizer's REPORT/FORMALIZATION_STATUS state this plainly. The task's
   "honest handling" rule (carry open analytic steps as explicit axiom-free hypotheses) is complied
   with. **FAITHFUL (a declared open bridge, not a hidden assumption).** Error layer:
   **dependency / open analytic input.**

### T1d + O4 — constant identities and `record_c9` — **FAITHFUL**

- `A0_eq_f9n9` (:139): (392/100000)·255 = 99960/100000 = 2499/2500 ✓.
- `cLHS_eq` (:148): 1 − 2499/657500 = 655001/657500 ✓; `cLHS_pos` ✓ (655001/657500 > 0).
- `qMT_eq` (:154): 262/131500 = 131/65750 ✓; matches `(m−1)/(500m)` with m=263.
- `record9_constant_identity` (:158-160): (H − 131/65750)·657500 = 657500·H − 1310 ✓ (since
  657500/65750 = 10), i.e. 657,500·H − 1,310.
- `c9Const_eq` (:163-166): c9Const = (657500·H − 1310)/655001 and c9Const = (H − qMT)/cLHS;
  checked: (H − 262/131500)·(657500/655001) = (657500·H − 262·5)/655001 = (657500·H − 1310)/655001 ✓
  (since 657500/131500 = 5, 657500/65750 = 10).
- `record_c9` (:232-266): uses `chain9_eps` at rescaled slack `ε·cLHS` (positive since cLHS>0),
  derives `cLHS·S ≥ (H − q − ε·cLHS)·N`, applies the exact coefficient identity
  `cLHS·(c9Const−ε) = H − q − ε·cLHS` (:245, ring), then cancels the positive cLHS
  (`mul_le_mul_of_nonneg_left`, `inv_mul_cancel₀`) to get `(c9Const − ε)·N ≤ S`. The O4 ε-form
  `∀ε>0 ∃T₀ ∀T≥T₀ (c9Const − ε)·N ≤ N₀ˢ` with `c9Const = (657500·H_MT − 1310)/655001 =
  0.673066472675939665848…` matches the contract's O4. **FAITHFUL.**
- Boundary rigor condition: `A0_lt_one` (:142) establishes A₀ = 2499/2500 < 1, the §4 rigor
  condition; the ε-form (not liminf-form) is used as the contract prescribes. **FAITHFUL.**

## Critical errors / gaps (exact locations)

1. **`Chain9.lean:59,62` — `wMT` is a structural placeholder for the true MT overlap kernel.**
   Not a proof error (it compiles and carries no false *claim* — the formalizer treats it as a
   fixed structural shape and flags the kernel-limit identity as open). But `CERTIFIED_F8_GE`
   (`F8gaps wMT`, :81-82) is therefore currently a statement about the squared-sinc kernel, not
   the baseline's `Cfun` MT overlap autocorrelation (Window.lean:1211). **Until the kernel-limit
   lemma ties `wMT` to the true kernel (with `√2λ/L` scaling and the `1/√2`-shift structure), the
   T2 certificate, when it lands, will be a certificate of a DIFFERENT pressure function than the
   paper's.** Fidelity caveat; error layer **boundary-convention / dependency (open analytic).**
2. **`Chain9.lean:91` — `deltaMT := fun _ => 0` is a placeholder.** `stability_eps` /
   `stability_averaged_eps` are stated over this abstract function, not the true physical
   Δ(M°(T)). This is honest (declared open), but it means T1c is open: the bridge is an unresolved
   analytic obligation, not a completed proof. Error layer **dependency (open analytic).**
3. **Snapshot-cleanliness transient (observed; now resolved).** At session start,
   `literature/raw/zeta-23-lean/Zeta23/Record9/` (stale byte-identical copies of Chain9.lean /
   M1Baseline.lean) was untracked in the snapshot — a leftover of the abandoned in-snapshot route
   that `lakefile-change.md` claims was removed. It was auto-removed during the session by the
   external Git auto-sync (the phenomena the formalizer documented). **Final snapshot state is
   clean and `lakefile.toml` is byte-identical to HEAD**, but the formalizer's "removed" claim was
   not true at session start. Error layer **boundary-convention (reproducibility / bookkeeping).**
4. **Formalizer's BUILD_LOG "lake build Record9.Chain9 killed after ~10 min" is inaccurate for
   this environment** — the verifier observed the identical command complete in ~47s with exit 0.
   This strengthens (does not weaken) the machine-acceptance evidence; the "killed" note is a
   recording discrepancy, not a failure. (Not an error layer; a report-hygiene nit.)
5. **Unused-hypothesis lint** `Chain9.lean:219` `hF` is unused by `chain9_eps` (the theorem is
   literally `chain9_eps_from_hypotheses b`, so `hF` plays no role). This is deliberate and correct
   (the certificate is not needed for the algebra), but the linter warning is worth silencing
   (`_hF` or omit) to keep the artifact warning-clean. Error layer: none (style).

## Non-circularity (closed)

- `chain9_eps` is not used in `stability_eps`/`stability_averaged_eps` (they have no proofs) and
  not used in `record_c9`'s construction path that would be circular; `chart` direction is
  `chain9_eps → record_c9` (the intended corollary). No obligation is discharged by a statement
  equivalent in strength to the target without a new proof.

## Per-obligation table

| Obl | Contract statement | Lean decl | Fidelity | Status (this pass) |
|---|---|---|---|---|
| T1a | statement / quantifiers / constants | `chain9_eps`, `CERTIFIED_F8_GE`, `F8gaps`/`F8`, `stability_*` | **FAITHFUL** (kernel `wMT` = open-bridge caveat) | Machine-accepted; statement faithful |
| T1b | algebra core + ε-lift | `chain9_algebra_core`, `chain9_eps_from_hypotheses`, `chain9_eps` | **FAITHFUL** | Machine-checked (pure rational algebra) |
| T1c | stability / block-defect / averaging (open analytic) | `stability_eps`, `stability_averaged_eps` (hypotheses) | **FAITHFUL (honest bridge, non-circular)** | OPEN as explicit axiom-free hypotheses |
| T1d | constant identities + O4 record | `A0_eq_f9n9`, `cLHS_eq/_pos`, `qMT_eq`, `c9Const_eq`, `record_c9` | **FAITHFUL** | Machine-checked |

## Verdict (this T1 pass)

**MACHINE_ACCEPTED_PENDING_AUDIT** — T1a/T1b/T1d compile with exit 0 and zero sorry/admit/axiom,
the statement matches the contract verbatim, the axiom set is exactly the baseline gold standard,
and the independent audit finds the prose/statement and the machine-checked algebra **faithful and
non-circular**. The analytic bridge (T1c: stability, averaged block-defect and the kernel-limit
lemma) is **open** — carried honestly as explicit axiom-free hypotheses over the placeholder
`deltaMT` and the structural kernel `wMT`; closing it is a real, unresolved analytic obligation,
exactly as the formalizer reports. One fidelity caveat to carry forward: `CERTIFIED_F8_GE` is only
as faithful to the paper as the kernel-limit lemma makes `wMT` equal to the true MT overlap kernel.
