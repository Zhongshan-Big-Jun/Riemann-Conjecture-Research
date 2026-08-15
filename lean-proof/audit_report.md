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
