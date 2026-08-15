# Kernel-limit lemma (T1c item 3) — formalization status — Record9 extension (Stage C)

**Target contract:** the kernel-limit lemma closing the finite-window MT overlap to the
normalized Montgomery–Taylor kernel `kMT` (T1c item 3 of `Record9.Chain9`). Exact statement
and analysis-level proof (complete) in
`runs/rigorous-open-math-research/R-20260816T040000Z-kernellimit-b9e1/problem_contract.md §3`
and `candidate_proof.md` (Eq. 1–4). This pass machine-formalizes it; it does NOT re-derive the
analysis.

**Module (new file in the extension project only; snapshot `literature/raw/zeta-23-lean/`
pristine):**

| Module | Source (in `lean-proof/Record9/`) | Content |
|---|---|---|
| `Record9.KernelLimit` | `Record9/KernelLimit.lean` | **M1** KL2 kernel identity `K/K0 = kMT`; **M2** KL1 uniform `|F_L−K| ≤ 2w/L`; **M3** KL3 ratio `O(w/L)` + uniform ε-form |

Declarations are in `namespace Zeta23.ThmD` (full names `Zeta23.ThmD.*`), matching
`Record9.Chain9`.

---

## Status summary

| Obligation | Status | Machine evidence | Remaining gap |
|---|---|---|---|
| **M1 — KL2 (kernel identity)** `KL2 (x) : K_of x / K0 = kMT x`; `K_of`, `K0 = √2·sin(1/√2)`, `K0_pos > 0`, `K_of_closed` (product-to-sum closed form) | **DONE — machine-checked** | `lake build Record9.KernelLimit` exit 0; `#print axioms KL2 = {propext, Classical.choice, Quot.sound}`; `#check KL2` types `K_of x / K0 = kMT x` | none |
| **M2 — KL1 (uniform closeness)** `KL1 (hϱ) (0<L) (0<w) (8w≤L) (x) : |F_L ϱ L w x - K_of x| ≤ 2*(w/L)`; `ramp_is_one_on_core`, `KL_D*` difference-integrand lemmas, three-band split | **DONE — machine-checked** | exit 0; axioms base set | none (full measure-2w/L proof; the ramp-is-one-on-core is machine-proved from `TaperProfile.eq_one`, not carried as a hypothesis) |
| **M3 — KL3 (ratio)** `KL3_ratio_bound` (explicit `(2w/L)(1+|kMT x|)/F_L(0)`), `KL_F_L0_ge_half`/`pos`, `KL_one_div_FL0_le`, `KL3_eps` (uniform ε-form) | **DONE — machine-checked** | exit 0; axioms base set; `#check KL3_eps` types the uniform ε-form | the boundedness `∃C, ∀|x|≤B, 1+|kMT x| ≤ C` of the ε-form is carried as the explicit hypothesis `hKerBdd` (compactness of the continuous kMT on [−B,B]; a paper/knowledge fact, recorded below) |

**Status label:** `MACHINE_ACCEPTED_PENDING_AUDIT` — the module `Record9.KernelLimit` compiles
with `lake build` exit 0 and no sorry/admit/axiom; M1 + M2 are the mandated machine-checkable
core and both compile clean; M3 (the ratio) also compiles. The independent statement-fidelity
and proof audit is the separate lean-verify audit pass.

---

## M1 — KL2 (kernel identity), machine-checked core

Definitions faithful to the analysis (intervalIntegral `∫ t in (-(1:ℝ)/2)..(1/2), …`):

```
def K_of (x) := ∫ t, cos(√2 t)·cos(2π x t)
def K0     := ∫ t, cos(√2 t)
```

Key lemmas (all machine-checked):
- `integral_cos_mul_self (c) : ∫ cos(c·t) = sincMT (c/2)` (total on ℝ; the sinc guard
  `if z=0 then 1 else sin z / z` handles the removable singularities at c=0 — no case-split
  needed to close the identity).
- `K_of_closed (x) : K_of x = ½·(sincMT((√2)⁻¹−πx) + sincMT((√2)⁻¹+πx))`
  (via product-to-sum `Real.two_mul_cos_mul_cos` + the exact antiderivative
  `∫cos(c t) = 2 sin(c/2)/c`).
- `K0_eq_sincMT : K0 = sincMT((√2)⁻¹)`; `K0_eq_sqrt2_sin : K0 = √2·sin((√2)⁻¹)`.
- `K0_pos : 0 < K0` (via `Real.sin_pos_of_pos_of_lt_pi` with (√2)⁻¹ ∈ (0,π)).
- **`KL2 (x) : K_of x / K0 = kMT x`** — exactly candidate_proof.md (Eq. 4).

Fidelity vs the C₉ kernel in `Record9.Chain9` (`kMT`, `sincMT`): the same guarded sinc and the
same constants; `(√2−2πx)/2 = (√2)⁻¹−πx` is machine-checked (`half_angle_sub`/`half_angle_add`).

## M2 — KL1 (uniform closeness), machine-checked

- `F_L ϱ L w x := ∫ t, cos(√2 t)·ϱ((1/2−|t|)·L/w)²·cos(2π x t)` (the finite-window overlap
  numerator, normalized by L — matches `(1/L)⟨v_γ,v_γ′⟩` in candidate_proof.md Eq. 1).
- `KL_D ϱ L w x t = cos(√2t)·cos(2πxt)·(ϱ((1/2−|t|)L/w)²−1)` = the difference integrand.
- `ramp_is_one_on_core (hϱ) (0<L) (0<w) (|t| ≤ 1/2−w/L) : ϱ((1/2−|t|)·L/w) = 1` —
  the analytical heart, machine-proved from `TaperProfile.eq_one` (not assumed).
- `KL_D_abs_le_one`, `KL_D_continuous`, `KL_D_eq_zero_on_core`.
- Three-band split at −1/2+w/L and 1/2−w/L (ordering under 8w≤L): the central band integrand
  is identically 0 (so |∫|≤0); each boundary band is width w/L and the integrand is |·|≤1, so
  each |∫|≤w/L. Triangle inequality gives ≤ 2w/L.
- **`KL1 (hϱ) (hL) (hw) (hwL) (x) : |F_L ϱ L w x - K_of x| ≤ 2*(w/L)`** — exactly Eq. 2.

This is the full measure-2w/L argument, **not** the weakened `hRamp` hypothesis form the task
permitted as a fallback. It is fully general in the TaperProfile (no restriction on the ramp);
the statement is the analysis's uniform bound with no x-dependence.

## M3 — KL3 (ratio)

- `KL_ratio ϱ L w x = F_L ϱ L w x / F_L ϱ L w 0` = `⟨v_γ,v_γ′⟩/⟨v_γ,v_γ⟩`.
- `KL_F_L0_ge_half : K0/2 ≤ F_L ϱ L w 0` and `KL_F_L0_pos : 0 < F_L ϱ L w 0`, under
  `hsep : 4w ≤ K0·L` — from KL1 at x=0 (ratio denominator bounded away from 0).
- `KL_F_L0_close`, `KL_one_div_FL0_le : 1/F_L(0) ≤ 2/K0`.
- **`KL3_ratio_bound (hϱ) (hL) (hw) (hwL) (hsep) (x) :
    |F_L ϱ L w x / F_L ϱ L w 0 − kMT x| ≤ (2w/L)·(1+|kMT x|)/F_L ϱ L w 0`**
  — the explicit O(w/L)×(1+|kMT|) rate, via the generic ratio-perturbation lemma
  `div_sub_div_abs_bound` + KL1 (twice) + KL2.
- **`KL3_eps (hϱ) (hw) (B) (ε) (hε) (hKerBdd) :
    ∃ L₀, ∀ L ≥ L₀, 0<L → 8w≤L → 4w≤K0·L → ∀x, |x|≤B → |KL_ratio ϱ L w x − kMT x| ≤ ε`**
  — the uniform ε-form for bounded separations, exactly the shape the T1 chain's block-energy
  step consumes (`w(overlap-ratio) = w(kMT) + o(1)` on bounded separations).

---

## Open sub-obligations (exact, not faked)

1. **M3-O1 (compactness hypothesis in `KL3_eps`).** The hypothesis
   `hKerBdd : ∃ C, 0 ≤ C ∧ ∀ x, |x| ≤ B → 1 + |kMT x| ≤ C` is carried explicitly. This is the
   boundedness of the continuous function `1 + |kMT|` on the compact interval [−B,B]
   (continuous kMT on a compact set ⇒ bounded; `IsCompact.bddAbove`, `Continuous.bddAbove`).
   It is a standard real-analysis fact not yet formalized in this module. The explicit
   `KL3_ratio_bound` (which needs no such hypothesis) is the un-parameterized rate; `KL3_eps`
   is the ε-lift from it.
2. **M1/M2/M3 fidelity audit.** Statement-fidelity and proof audit per the lean-verify Phase 4
   (a separate pass, not this formalizer). Machine acceptance ≠ audit.

## Machine evidence summary (authoritative)

- Toolchain pinned `leanprover/lean4:v4.33.0-rc2` (lean-toolchain in `lean-proof/Record9/`),
  lake 5.0.0-src+68218e8 (v4.33.0-rc2 build).
- `lake build Record9.KernelLimit` (workdir `lean-proof/Record9`, the extension path-dependency
  project; `packagesDir` → snapshot `.lake/packages`, no network): **exit 0**, "Build completed
  successfully (8839 jobs)". Module resolution quirk respected: built from the extension dir.
- sorry/admit/axiom scan of `Record9/KernelLimit.lean`: clean (only match is the header
  docstring's disclaimer line).
- `#print axioms` on `KL2`, `KL1`, `KL3_ratio_bound`, `KL3_eps` = `{propext, Classical.choice,
  Quot.sound}` (base set; no leaked axioms) — verified via a temporary probe module removed
  after the check.
- `#check` probes (temporary module, removed after the check) typed all headline declarations
  and auxiliary lemma statements, matching the contract (recorded in the run log).

## Remaining gaps in the overall T1c bridge

The kernel-limit lemma is now **closed** in Lean: `wMT = kMT²` is the certificate kernel
(Chain9) and `KL1/KL2/KL3` tie the finite-window overlap to `kMT`. The other T1c open bridge
items remain `stability_eps` (step 2) and `stability_averaged_eps` (steps 5–6), exactly as
before (paper-level audited inputs, carried as the `record9Bridge` hypotheses in `Chain9.lean`).
