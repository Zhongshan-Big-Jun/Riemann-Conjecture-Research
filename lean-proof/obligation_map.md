# Obligation map — C₉ = 0.6730665 record (lean-verify Phase 1/2)

Target Lean project: literature/raw/zeta-23-lean (snapshot @3635e748, pinned
leanprover/lean4:v4.33.0-rc2, mathlib4 @ 51e6992e). Verification workspace: lean-proof/.

| Obl | Contract statement | Lean declaration(s) | Fidelity | Status |
|---|---|---|---|---|
| O1 | Baseline: ∀ε>0 ∃T₀ ∀T≥T₀: (H_MT − ε)·N(T,2T) ≤ N₀ˢ(T,2T), H_MT = 3/2 − (1/√2)cot(1/√2) | `Zeta23.ThmD.Mult.thmD₀_simple_mult` (HD 1 − ε form) and `thmD₀_simple_mult'` (constant written out: 3/2 − (√2)⁻¹·cos(1/√2)/sin(1/√2)); cumulative form `thmD₀_simple_mult_cumulative` | **FAITHFUL** (checked line-by-line 2026-08-15: ε-form, dyadic (T,2T], Ncount = N with multiplicity, N0simple = simple-on-line; unconditional via zetaZeroConfig + paperInputs_zeta) | ✅ formalized upstream; **machine build COMPLETE** (`lake build Zeta23` exit 0, 9010 jobs; `#print axioms` on all headline theorems = {propext, Classical.choice, Quot.sound}, lean-proof/axioms-check.log) |
| O2 | Chain: (1 − A₀/m)·N₀ˢ(T,2T) ≥ (H_MT − (m−1)/(500m) − ε)·N(T,2T) given certified F₈ ≥ 392/100000 (m=263, A₀=2499/2500) | `Zeta23.ThmD.chain9_eps` (in extension `Record9.Chain9`, full name `Zeta23.ThmD.chain9_eps`) — **written, compiles**; proven with `hF : CERTIFIED_F8_GE` + bundled bridge `b : record9Bridge` (T1) | **FAITHFUL** (T1a; kernel repaired 2026-08-15 to certificate kernel `kMT` — see "T1 repair round") | 🟨 T1a/T1b/T1d DONE (machine-accepted, re-audit pending); **T1c analytic bridge OPEN** (explicit hypotheses) |
| O3 | Certificate: F₈ ≥ 392/100000 (grid-2000, 128-bit, 64,748,524 nodes; kernel table 31368 entries) | (target: `Zeta23.Pressure.f8_cert`) — NOT yet written | — (B1–B6 computational audit PASS; certificate sha 7F25401A…) | ❌ OPEN (T2, reflection route) |
| O4 | Conclusion: liminf N₀ˢ/N ≥ (657,500·H_MT − 1,310)/655,001 | (target: `Zeta23.ThmD.record_c9`; arithmetic verified dps=130) | — (exact rational identity (657,500/65,750 = 10) verified) | ❌ OPEN (O2+O3) |
| O5 | ξ′ record: liminf N₀ˢ_{ξ′}/N_{ξ′} ≥ (657,500·H_{ξ′} − 1,310)/655,001 | (target: `Zeta23.XiPrime.record_c9xip`; imports `Zeta23.XiPrime.*` + O2) | — (A1–A6 manager PASS; AdmWindow cos blueprint ready) | ❌ OPEN (T3) |
| O6 | Evidence discipline: no numerical evidence labeled as proof | candidate_proof.md honest status; this map | **FAITHFUL** | ✅ |

## Fidelity notes (O1, 2026-08-15)

- `thmD₀_simple_mult` quantifier order: ∀ε>0, ∃T₀, ∀T≥T₀ — matches the informal ε-form.
- `HD 1` is definitionally 2 − 1/c₁* = 3/2 − cot(1/√2)/√2 (HD_one at ThmD/Functional.lean:464
  [corrected 2026-08-15 from the earlier ParamsD.lean note]; `thmD₀_simple_mult'` displays
  the constant explicitly). Decimals are documentation.
- N0simple/Ncount are the multiplicity-counted simple-on-line / total counts — matches the
  record theorem's N₀ˢ / N conventions (N0* = distinct; N0simple = simple). Independent
  audit (lean-proof/lean-audit-report.md, 2026-08-15): O1a–O1f all FAITHFUL, verdict FORMALLY_VERIFIED.
- Boundary: T real, dyadic window (T, 2T]; the cumulative form covers liminf on (0, T].

## T1 formalizer pass (2026-08-16, Stage C) — appended results for O2/O4

**What was formalized** (all in the extension module `Record9.Chain9`, full names
`Zeta23.ThmD.*`; declared in `lean-proof/Record9/Record9/Chain9.lean`).

- `Zeta23.ThmD.chain9_eps (hF : CERTIFIED_F8_GE) (b : record9Bridge) :
    ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
      (1 − (2499:ℝ)/2500/263)·N₀ˢ(T,2T) ≥ (HD 1 − (262:ℝ)/131500 − ε)·N(T,2T)`
  — **the T1 statement**, written with the contract's literal rationals.
- `Zeta23.ThmD.CERTIFIED_F8_GE : Prop` :=
  `∀ g : Fin 8 → ℝ, (∀ i, 0 ≤ g i) → (392:ℝ)/100000 ≤ F8 g`, where `F8 g = F8gaps wMT g`
  is the k=9 pressure function (general-k §2) over the structurally-fixed MT kernel
  `wMT x = (sinc x)²`.
- Bridge hypotheses (open analytic steps, carried axiom-free as `record9Bridge` fields):
  `stability_eps` (step 2) and `stability_averaged_eps` (steps 5–6) — exact statements in
  `lean-proof/Record9/FORMALIZATION_STATUS.md`.
- `Zeta23.ThmD.chain9_algebra_core` (T1b algebra), `chain9_eps_from_hypotheses` (ε-lift),
  constants + identities (T1d), and `record_c9` (O4 form):
  `∀ε>0, ∃T₀, ∀T≥T₀, (c9Const − ε)·N(T,2T) ≤ N₀ˢ(T,2T)`, `c9Const = (657500·H_MT − 1310)/655001`.

**Machine evidence (pinned v4.33.0-rc2):**
- `lake env lean Record9/Chain9.lean` → exit 0 (no sorry/admit/axiom; sorry/axiom scan clean).
- `#check Zeta23.ThmD.chain9_eps` etc. → exit 0; the printed types match the contract
  (statement-fidelity probe preserved in the run log).
- `lake build Record9.M1Baseline` → exit 0 (extension plumbing). The library-level `lake
  build` of the path-dependency project has a cross-project graph-resolution latency; the
  authoritative module compile is the `lake env lean` exit 0 above (same lake env as build).
- Snapshot `literature/raw/zeta-23-lean/lakefile.toml`: unchanged (route = path-dependency
  extension; see `lean-proof/Record9/lakefile-change.md`).

**Remaining gaps (exact statements, not faked):**
- **T1c** — the analytic bridge: provide Lean proofs of `stability_eps` and
  `stability_averaged_eps` for the true `Δ(M°)`, and of the kernel-limit lemma tying `wMT`
  to the finite-window MT overlap. These are paper-level audited inputs (OpenAI Lemma 2.1/Cor
  2.2; general-k §4–§6) and are the open analytic obligations.
- **T2** — the certificate `F₈ ≥ 392/100000` (reflection route; `CERTIFIED_F8_GE` declared but
  not proved).
- Fidelity of `chain9_eps`: it is stated with `hF` **and** the bundled bridge `b`; the
  bridge is required because steps 2,5,6 are not machine-proved. Full record: see
  `lean-proof/Record9/FORMALIZATION_STATUS.md`.

**T1 pass verdict:** `MACHINE_ACCEPTED_PENDING_AUDIT` (T1a/T1b/T1d compile with zero
sorry/axiom; T1c open as explicit hypotheses).

## T1 repair round (2026-08-15) — O2/T1a kernel fidelity

The independent verifier's finding #1 (statement-layer defect) is **repaired**. `wMT` was a
plain `sinc²` placeholder; it is now the certificate's **true normalized Montgomery–Taylor
overlap kernel**:

- `sincMT z = if z = 0 then 1 else sin z / z` (guarded sinc, unchanged).
- `kMT x = [sincMT((√2)⁻¹ − πx) + sincMT((√2)⁻¹ + πx)] / 2 / (√2·sin((√2)⁻¹))` — matches
  `zeta_simple_zeros/kernel.py` `normalized_kernel` (openai, zeta-simple-zeros:43-54;
  `k_zero = √2·sin((√2)⁻¹)`, lines 32-40).
- `wMT x = (kMT x)²`; added `kMT_den_pos : 0 < √2·sin((√2)⁻¹)`.

`CERTIFIED_F8_GE` now states exactly what the Arb certificate
`nine-point-f8-gt-392over100000-grid2000.txt` certifies. **Statement freeze honored**: the
ε-form statement, quantifiers, constants and bridge hypotheses of `chain9_eps` / `record_c9`
are unchanged (verified by `#check` in this round). Kernel-limit lemma (finite-window
`Cfun` → `kMT`) remains an **open analytic bridge** (T1c item 3); T2, T3 unchanged.

**Status:** `MACHINE_ACCEPTED_PENDING_AUDIT` — repaired file compiles clean
(`lake env lean` exit 0; `lake build Record9.Chain9` exit 0, 8838 jobs), no
sorry/admit/axiom, statement shape unchanged. **Re-audit pending** (fidelity of the repaired
kernel statement).
