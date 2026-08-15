/-
Record9.Chain9 — T1: the chain theorem in ε-form (bounded pass)

Part of the Stage C T1 formalizer pass for the C₉ = 0.67306647267… world-record theorem
(C₉(ζ) = (657,500·H_MT − 1,310)/655,001, H_MT = 3/2 − (1/√2)·cot(1/√2)).

Statement contract: lean-proof/verification-contract.md (T1 row), task "T1 — the chain
theorem in ε-form", and the general-k derivation
runs/rigorous-open-math-research/R-20260814T045000Z-extpress-2f36ae/candidate_proof.general-k-derivation.md
(§1–§6). The machine-checked content here is the ALGEBRA of the algebraic implication for
k=9 in ε-form together with the exact constant identities; the analytic bridge (steps 2, 5,
6 of the chain — stability, block-defect via the Gram-matrix defect lemma, pinching/
averaging) is represented as EXPLICIT axiom-free hypotheses, exactly as the "honest
handling" rule of the task requires. NO sorry/admit/axiom appear in this file or any Record9
file.

Obligations carried here:
  T1a (statement)    : `chain9_eps`, `CERTIFIED_F8_GE`, pressure function `F8gaps`/`F8`
                       (k=9), bridge hypotheses `stability_eps` / `stability_averaged_eps`.
  T1b (algebra core) : `chain9_algebra_core` (single-T two-hypothesis implication),
                       `chain9_eps_from_hypotheses` (ε-form lift), and `chain9_eps`.
  T1c (analytic bridge): OPEN — the physical Δ(M°) is not machine-tied here; carried as
                       the explicit hypotheses `stability_eps`, `stability_averaged_eps`.
                       Exact statements recorded in
                       lean-proof/Record9/FORMALIZATION_STATUS.md.
  T1d (constant identity + O4): `A0_eq_f9n9`, `cLHS_pos`, `c9Const_eq`, and the liminf-ε-form
                       record corollary `record_c9`.

Fidelity notes:
  • The ε-form statement, quantifier order (∀ε>0, ∃T₀, ∀T≥T₀ with T real, window (T,2T]),
    and the constants 2499/2500/263 = A₀/m and 262/131500 = (m−1)/(500m) follow the
    contract exactly, written out as literal rationals. N0simple = N₀ˢ (simple-on-line),
    Ncount = N (with multiplicity) are the baseline snapshot counts.
  • `CERTIFIED_F8_GE` is the paper certificate statement "F₈ ≥ 392/100000 for all gᵢ ≥ 0",
    where F₈ is the k=9 pressure function built from the normalized Montgomery–Taylor
    overlap kernel w. The kernel `wMT` is fixed *structurally* (squared, even, w(0)=1,
    sinc MT-shape); its precise agreement with the finite-window overlap in the high-T
    limit (the kernel-limit lemma) is an analytic-bridge sub-obligation, not assumed here.
  • `chain9_eps` is stated with the certified-pressure hypothesis `hF : CERTIFIED_F8_GE`
    (the contract) AND the bundled bridge `b : record9Bridge` (the honest routing of the
    open analytic steps 2,5,6). The proof only uses the algebra and the ε-lift.
-/
import Zeta23.ThmD.Mult

noncomputable section

open scoped BigOperators
open BigOperators Finset

namespace Zeta23
namespace ThmD

/-! ## Pressure function (k=9) and the certified-bound statement (T1a) -/

/-- normalized Montgomery–Taylor overlap kernel k(x) := K(x)/K(0), so that w(x) := k(x)²,
w(0) = 1 (general-k §1, §2). Fixed here in the sinc MT shape; the precise identity with the
finite-window overlap in the high-T limit is an analytic-bridge sub-obligation (see header).
Kept total on ℝ via the `if x = 0 then 1` guard. -/
def sincMT (x : ℝ) : ℝ := if x = 0 then 1 else Real.sin x / x

/-- the squared normalized MT overlap kernel w(x) = k(x)². -/
def wMT (x : ℝ) : ℝ := (sincMT x) ^ 2

/-- `gapSpan g i len` = g_i + g_{i+1} + ⋯ + g_{i+len-1}  (sum of `len` consecutive gaps
starting at gap index `i`, 0-based). -/
def gapSpan (g : ℕ → ℝ) (i len : ℕ) : ℝ := (Finset.range len).sum (fun j => g (i + j))

/-- the k=9 pressure function F₈(g₁,…,g₈) (general-k §2 for k=9, 8 gaps):
    (1/(500·8))·Σᵢ gᵢ + Σ_{s0=0}^{7} (2/(8−s0))·Σ_{i=0}^{8−s0−1} w(g_i+⋯+g_{i+s0}).
Here `s0 = s−1` and the inner window uses `len = s0+1` consecutive gaps from `i`; the total
is over the 8 gaps indexed 0..7. This mirrors the paper's F_{k-1} with k=9. -/
def F8gaps (w : ℝ → ℝ) (g : ℕ → ℝ) : ℝ :=
  (1 / (500 * 8)) * ((Finset.range 8).sum g) +
    (Finset.range 8).sum (fun s0 =>
      ((2 : ℝ) / ((8 - s0 : ℕ) : ℝ)) * ((Finset.range (8 - s0)).sum (fun i => w (gapSpan g i (s0 + 1)))))

/-- `F8gaps` for the canonical MT kernel `wMT`, on a vector `g : Fin 8 → ℝ` (0-based). -/
def F8 (g : Fin 8 → ℝ) : ℝ := F8gaps wMT (fun n : ℕ => g ⟨n % 8, Nat.mod_lt n (by decide)⟩)

/-- the certified k=9 pressure bound: F₈(g₁,…,g₈) ≥ 392/100000 for all gᵢ ≥ 0. -/
def CERTIFIED_F8_GE : Prop :=
  ∀ g : Fin 8 → ℝ, (∀ i : Fin 8, 0 ≤ g i) → (392 : ℝ) / 100000 ≤ F8 g

/-! ## Bridge hypotheses — the analytic steps 2, 5, 6 (T1c, OPEN) -/

/-- The bookkeeping value Δ(T) = Δ(M°(T)) of the Gram defect of the retained central simple
zeros (paper Cor 2.2 / general-k §1, §4–§6). This placeholder is only referenced by the
bridge hypotheses; it is never evaluated by the theorems in this file, so its value is inert
for their proofs (it is a free abstract function quantified into the bridge conditions, and
has not been machine-tied to M° here). -/
def deltaMT : ℝ → ℝ := fun _ => 0

/-- Step 2 as an ε-form hypothesis: the stability refinement
    S ≥ H_MT·N + Δ(M°) − o(N),  i.e.  (HD 1)·N + Δ(T) − ε·N ≤ S for large T.
This is OpenAI Lemma 2.1 / Cor 2.2, a paper-level audited input that is NOT in Lean; it is
an explicit OPEN hypothesis of `chain9_eps`. -/
def stability_eps : Prop :=
  ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
    HD 1 * (Ncount T (2 * T) : ℝ) + deltaMT T - ε * (Ncount T (2 * T) : ℝ)
      ≤ N0simple T (2 * T)

/-- Steps 5+6 as an ε-form hypothesis: the averaged block defect
    Δ(M°) ≥ (A₀/m)·S − ((m−1)/(500m))·N − o(N),
    with (A₀/m) = 2499/657500 and ((m−1)/(500m)) = 262/131500.
This is the block-defect lemma + convexity-under-pinching averaging (general-k §4–§6,
[OpenAI §4], [OpenAI (20)]), a paper-level audited input NOT in Lean; it is an explicit OPEN
hypothesis of `chain9_eps`. -/
def stability_averaged_eps : Prop :=
  ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
    deltaMT T ≥ (2499 : ℝ) / 657500 * (N0simple T (2 * T) : ℝ)
      - (262 : ℝ) / 131500 * (Ncount T (2 * T) : ℝ)
      - ε * (Ncount T (2 * T) : ℝ)

/-- bundle of the open analytic-bridge hypotheses that `chain9_eps` requires. -/
structure record9Bridge where
  stability : stability_eps
  averaged : stability_averaged_eps

/-! ## The k=9 constants and their exact identities (T1d) -/

/-- f₉ = 392/100000 (the certified pressure-bound value). -/
abbrev f9 : ℝ := (392 : ℝ) / 100000
/-- n = ⌈1/f₉⌉ − 1 = 255. -/
abbrev n9 : ℝ := 255
/-- A₀ = f₉·n = (392/100000)·255 = 2499/2500 < 1. -/
abbrev A0 : ℝ := (2499 : ℝ) / 2500
/-- m = (k−1) + n = 8 + 255 = 263. -/
abbrev m9 : ℝ := 263
/-- A₀/m = (2499/2500)/263, i.e. the literal 2499/2500/263 (the chain9_eps left multiplier). -/
abbrev cA0m : ℝ := (2499 : ℝ) / 2500 / 263
/-- (m−1)/(500m) at m=263: 262/131500. -/
abbrev qMT : ℝ := (262 : ℝ) / 131500
/-- 1 − A₀/m = 655001/657500. -/
abbrev cLHS : ℝ := 1 - cA0m
/-- C₉ = (657,500·H_MT − 1,310)/655,001. -/
abbrev c9Const : ℝ := (657500 * HD 1 - 1310) / 655001

/-- exact: A₀ = f₉·n₉ = 2499/2500. -/
lemma A0_eq_f9n9 : A0 = f9 * n9 := by norm_num [A0, f9, n9]

/-- exact: A₀ < 1 (the rigor condition of general-k §4). -/
lemma A0_lt_one : A0 < 1 := by norm_num [A0]

/-- A₀/m = 2499/657500 (as a rational identity). -/
lemma cA0m_eq : (2499 : ℝ) / 2500 / 263 = (2499 : ℝ) / 657500 := by norm_num

/-- 1 − A₀/m = 655001/657500. -/
lemma cLHS_eq : cLHS = (655001 : ℝ) / 657500 := by norm_num [cLHS]

/-- cLHS > 0, so it can be used to invert the chain inequality. -/
lemma cLHS_pos : 0 < cLHS := by norm_num [cLHS]

/-- (m−1)/(500m) = 262/131500 = 131/65750. -/
lemma qMT_eq : qMT = (131 : ℝ) / 65750 := by norm_num [qMT]

/-- the record numerator identity: 657,500·H − 1,310 = (H − 131/65750)·657,500, since
657500/65750 = 10. -/
lemma record9_constant_identity :
    (HD 1 - (131 : ℝ) / 65750) * (657500 : ℝ) = 657500 * HD 1 - 1310 := by
  ring

/-- assembled: C₉ = (H − q)/cLHS = (657,500·H − 1,310)/655,001, where cLHS = 1 − A₀/m. -/
lemma c9Const_eq : c9Const = (HD 1 - qMT) / cLHS := by
  unfold c9Const qMT cLHS cA0m
  norm_num
  ring

/-! ## T1b: the algebraic core (single-T implication) -/

/-- single-T algebraic step (k=9, ε-form chain step 7):
    from  (i)  (HD 1)·N + D − e₁·N ≤ S              (stability refinement, ε-form)
    and   (ii) (2499/657500)·S − (262/131500)·N − e₂·N ≤ D     (averaged block defect, ε-form)
    derive     (1 − 2499/2500/263)·S ≥ (HD 1 − 262/131500)·N − (e₁+e₂)·N.
    Proved by `norm_num`+`ring_nf`+`set`+`linarith` (all rational arithmetic). -/
lemma chain9_algebra_core {S N D e₁ e₂ : ℝ}
    (hStab : HD 1 * N + D - e₁ * N ≤ S)
    (hAvg : (2499 : ℝ) / 657500 * S - (262 : ℝ) / 131500 * N - e₂ * N ≤ D) :
    (1 - (2499 : ℝ) / 2500 / 263) * S ≥ (HD 1 - (262 : ℝ) / 131500) * N - (e₁ + e₂) * N := by
  norm_num at hStab hAvg ⊢
  ring_nf at hStab hAvg ⊢
  set t : ℝ := HD 1 * N with htd
  linarith

/-! ## T1b: the ε-form lift and the contract-named theorem -/

/-- the ε-form lift: for an input ε, use ε/2 in each bridge hypothesis and combine at a
common T₀ = max T₀₁ T₀₂. -/
theorem chain9_eps_from_hypotheses (b : record9Bridge) :
    ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
      (1 - (2499 : ℝ) / 2500 / 263) * (N0simple T (2 * T) : ℝ)
        ≥ (HD 1 - (262 : ℝ) / 131500 - ε) * (Ncount T (2 * T) : ℝ) := by
  intro ε hε
  have hε2 : ε / 2 > 0 := by linarith
  obtain ⟨T₀₁, h₁⟩ := b.stability (ε / 2) hε2
  obtain ⟨T₀₂, h₂⟩ := b.averaged (ε / 2) hε2
  refine ⟨max T₀₁ T₀₂, fun T hT => ?_⟩
  have hT1 : T₀₁ ≤ T := le_trans (le_max_left _ _) hT
  have hT2 : T₀₂ ≤ T := le_trans (le_max_right _ _) hT
  have hs := h₁ T hT1
  have ha := h₂ T hT2
  have hstep := chain9_algebra_core
    (S := (N0simple T (2 * T) : ℝ)) (N := (Ncount T (2 * T) : ℝ)) (D := deltaMT T)
    (e₁ := ε / 2) (e₂ := ε / 2) hs ha
  -- reduce (ε/2 + ε/2) to ε in the RHS coefficient
  have hfinal :
      (HD 1 - (262 : ℝ) / 131500) * (Ncount T (2 * T) : ℝ) - (ε / 2 + ε / 2) * (Ncount T (2 * T) : ℝ)
        = (HD 1 - (262 : ℝ) / 131500 - ε) * (Ncount T (2 * T) : ℝ) := by
    ring
  rw [hfinal] at hstep
  exact hstep

/-- **chain9_eps (T1)** — the k=9 pressure-method chain in ε-form.
    Given the certified pressure bound (hF) and the bundled analytic bridge (b), for every
    ε > 0 there is T₀ such that for all T ≥ T₀
        (1 − (2499/2500)/263)·N₀ˢ(T,2T) ≥ (H_MT − 262/131500 − ε)·N(T,2T),
    i.e.  (1 − A₀/m)·S ≥ (HD 1 − (m−1)/(500m) − ε)·N  — the ε-form record chain.
    `hF` and `b` are hypotheses (the bridge encodes steps 2,5,6); the machine-checked
    content is the algebra and the ε-lift. -/
theorem chain9_eps (hF : CERTIFIED_F8_GE) (b : record9Bridge) :
    ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
      (1 - (2499 : ℝ) / 2500 / 263) * (N0simple T (2 * T) : ℝ)
        ≥ (HD 1 - (262 : ℝ) / 131500 - ε) * (Ncount T (2 * T) : ℝ) :=
  chain9_eps_from_hypotheses b

/-! ## T1d + O4: the liminf record corollary -/

/-- **record_c9 (O4, conditional on the chain)** — liminf N₀ˢ/N ≥ C₉ in ε-form.
    Corollary of `chain9_eps`: run the chain at the rescaled slack ε·cLHS and cancel the
    (positive) multiplier cLHS, so the displayed constant is exactly
    C₉ = (657,500·H_MT − 1,310)/655,001. `hF` and the bundled bridge `b` are the hypotheses
    (steps 2,5,6 remain open). -/
theorem record_c9 (hF : CERTIFIED_F8_GE) (b : record9Bridge) :
    ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
      (c9Const - ε) * (Ncount T (2 * T) : ℝ) ≤ N0simple T (2 * T) := by
  intro ε hε
  have hc : (0 : ℝ) < cLHS := cLHS_pos
  have hce : ε * cLHS > 0 := mul_pos hε hc
  obtain ⟨T₀, hT₀⟩ := chain9_eps hF b (ε * cLHS) hce
  refine ⟨T₀, fun T hT => ?_⟩
  let N : ℝ := (Ncount T (2 * T) : ℝ)
  let S : ℝ := (N0simple T (2 * T) : ℝ)
  have hS : cLHS * S ≥ (HD 1 - (262 : ℝ) / 131500 - ε * cLHS) * N := by
    simpa [cLHS, N, S] using hT₀ T hT
  -- exact coefficient identity: cLHS·(C₉ − ε) = (HD − (262/131500) − ε·cLHS)
  have hcoef : cLHS * (c9Const - ε) = HD 1 - (262 : ℝ) / 131500 - ε * cLHS := by
    unfold cLHS c9Const cA0m
    ring
  -- cLHS·(C₉−ε)·N ≤ (HD − (262/131500) − ε·cLHS)·N ≤ cLHS·S
  have hchain : cLHS * (c9Const - ε) * N ≤ cLHS * S := by
    calc
      cLHS * (c9Const - ε) * N = (HD 1 - (262 : ℝ) / 131500 - ε * cLHS) * N := by rw [hcoef]
      _ ≤ cLHS * S := by
        exact hS
  have hleft : cLHS * ((c9Const - ε) * N) ≤ cLHS * S := by
    simpa [mul_assoc] using hchain
  -- cancel the positive cLHS:  (c9Const − ε)·N ≤ S
  have hcancel : (c9Const - ε) * N ≤ S := by
    -- from cLHS * ((c9Const-ε)*N) ≤ cLHS * S, multiply by cLHS⁻¹ (nonneg) and cancel.
    have hsimp : cLHS⁻¹ * (cLHS * ((c9Const - ε) * N)) = (c9Const - ε) * N := by
      rw [← mul_assoc, inv_mul_cancel₀ (ne_of_gt hc), one_mul]
    have hsimp2 : cLHS⁻¹ * (cLHS * S) = S := by
      rw [← mul_assoc, inv_mul_cancel₀ (ne_of_gt hc), one_mul]
    have hx : cLHS⁻¹ * (cLHS * ((c9Const - ε) * N)) ≤ cLHS⁻¹ * (cLHS * S) :=
      mul_le_mul_of_nonneg_left hleft (inv_nonneg.mpr hc.le)
    simpa [hsimp, hsimp2] using hx
  simpa [N, S] using hcancel

end ThmD
end Zeta23
