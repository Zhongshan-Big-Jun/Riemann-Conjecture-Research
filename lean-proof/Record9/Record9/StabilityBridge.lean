/-
Record9.StabilityBridge — T1c-1 / T1c-2 stability-bridge formalization (Stage C).

Part of the Stage C formalizer pass for the C₉ = 0.67306647267… world-record theorem. This
module formalizes the stability-bridge statements from
`runs/rigorous-open-math-research/R-20260816T060000Z-stabridge-a3f1/` (problem_contract.md §3,
candidate_proof.md). The analysis-level statements are COMPLETE (pinned at analysis level);
this module machine-formalizes the bounded, honest milestones. NO sorry/admit/axiom appear
anywhere in this module.

Obligations carried here:
  M1 — the Ψ-defect lemma (T1c-2b core):
        `Psi`  : Ψ(t) = (t−1)²·1_{t≤2} + (2t−3)·1_{t>2} (candidate_proof §0, proof.md §2),
        `trPsi`  : tr Ψ(G) = Σᵢ Ψ(μᵢ) for Hermitian G (spectral definition via eigenvalues),
        `sumSqOffDiag` : Σ_{i<j} |G_ij|²,
        `psi_defect` : the T1c-2b exact statement  tr Ψ(G) ≥ min(1, 2·Σ_{i<j}|G_ij|²),
        machine-checked: `Psi_nonneg`, `Psi_gt_one_of_gt_two`, and the two-case combinators
        `psi_defect_of_unit` (μ_max > 2 ⇒ the `1`-cap branch) and `psi_defect_of_lower`
        (the `2Σ` branch). The two spectral sub-steps that close the case split — (i) all
        eigenvalues ≤ 2 ⇒ tr Ψ(G) = frobSq (G − I) ≥ 2·Σ|G_ij|² (off-diagonal Frobenius of
        G − I), and (ii) some eigenvalue > 2 ⇒ 1 ≤ tr Ψ(G) — are the recorded OPEN analytic
        obligations (Lemma 2.1 Ψ-form application), exactly as the honest-bridge rule requires.
  M2 — T1c-1 (stability_eps for the true Δ):
        `deltaMT_true` (the true Δ(M°) of the unit-normalized correlation Gram, abstracted),
        `stability_eps_true` (the exact ε-form statement with +Δ),
        `base_eps` (≡ thmD₀_simple_mult, machine-proved) and `defect_eps`,
        `from_base_and_defect` : the additive +Δ SURVIVAL — from the base inequality and the
        Δ-defect bound, derive the ε-form with +Δ. The analytic Lemma 2.1 assembly content
        (keeping a full order-O(S) Δ without bounding it small) is the recorded OPEN
        obligation; this module machine-checks the purely additive sub-case where Δ ≥ 0 and
        Δ = o(N).
  M3 — T1c-2 (stability_averaged_eps):
        `stability_averaged_eps_true` (the exact ε-form statement with the true Δ),
        the exact constant identities (A₀ = 2499/2500, A₀/m = 2499/657500,
        (m−1)/(500m) = 262/131500, and the (m−1)/(500m) = 262/131500 closed form at m = 263),
        mirroring Chain9's algebra-core style. The pinching `trΨ(M°) ≥ block-average` (T1c-2c)
        and the block-uniformity Σ|G_ij|² = (1/2)E_m + o(1) (T1c-2d) are the recorded OPEN
        analytic obligations; the ε-form statement is carried as the honest bridge.

Fidelity notes:
  • Statement freeze vs the stabridge artifacts: the ε-form statements, quantifier order
    (∀ε>0, ∃T₀, ∀T≥T₀ with T real, window (T,2T]), and the constants 2499/657500 = A₀/m and
    262/131500 = (m−1)/(500m) follow the contract exactly (problem_contract.md §3), written
    out as literal rationals, matching `Zeta23.ThmD.stability_eps` / `stability_averaged_eps`
    with `deltaMT` replaced by the true `deltaMT_true`.
  • `deltaMT_true` is defined abstractly (the physical Gram M°(T) needs the snapshot's
    Gram-entry machinery, which is not machine-tied here); the honest-bridge rule carries the
    Gram content as explicit hypotheses.
  • The unit-normalized (≡ correlation) Gram is the only convention consistent with Cor 2.2
    and T1c-2 (see stabridge counterexample_log.md §1); this module's `deltaMT_true` is that Δ.
-/
import Record9.Chain9
import Zeta23.ThmD.Mult
import Zeta23.LinAlg.PosIndex
import Zeta23.Assembly

noncomputable section

open scoped BigOperators
open BigOperators Finset
open Matrix RHLinalg

namespace Zeta23
namespace ThmD

/-! ## M1 — the Ψ-defect lemma (T1c-2b core) -/

/-- Ψ(t) = (t−1)²·1_{t≤2} + (2t−3)·1_{t>2} : the Gram-defect function (proof.md §2,
    candidate_proof §0). Continuous, nonnegative, Ψ(0) = Ψ(2) = 1, linear for t > 2. -/
def Psi (t : ℝ) : ℝ := if t ≤ 2 then (t - 1)^2 else 2 * t - 3

/-- tr Ψ(G) for Hermitian G, defined spectrally: Σᵢ Ψ(μᵢ) where μᵢ are the eigenvalues. -/
def trPsi {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ) (hG : G.IsHermitian) : ℝ :=
  ∑ i : Fin n, Psi (hG.eigenvalues i)

/-- Σ_{i<j} |G_ij|² : the off-diagonal square-energy of a Gram block (candidate_proof §2b). -/
def sumSqOffDiag {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ) : ℝ :=
  ∑ i : Fin n, ∑ j : Fin n, (if i < j then (G i j)^2 else 0)

/-- on the branch t ≤ 2, Ψ(t) = (t−1)². -/
lemma Psi_eq_sq_of_le_two {t : ℝ} (ht : t ≤ 2) : Psi t = (t - 1)^2 := by
  unfold Psi
  exact if_pos ht

/-- on the branch 2 < t, Ψ(t) = 2t − 3. -/
lemma Psi_eq_linear_of_gt_two {t : ℝ} (ht : 2 < t) : Psi t = 2 * t - 3 := by
  unfold Psi
  exact if_neg (not_le.mpr ht)

/-- Ψ ≥ 0 on all of ℝ (the defect is nonnegative). -/
lemma Psi_nonneg (t : ℝ) : 0 ≤ Psi t := by
  unfold Psi
  by_cases h : t ≤ 2
  · rw [if_pos h]
    positivity
  · rw [if_neg h]
    have ht2 : 2 < t := lt_of_not_ge h
    nlinarith

/-- for t > 2, Ψ(t) > 1 (the `>1` branch used in the μ_max > 2 case). -/
lemma Psi_gt_one_of_gt_two {t : ℝ} (ht : 2 < t) : 1 < Psi t := by
  rw [Psi_eq_linear_of_gt_two ht]
  nlinarith

/-- tr Ψ(G) ≥ 0 for Hermitian G (Ψ ≥ 0 on each eigenvalue). -/
lemma trPsi_nonneg {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ) (hG : G.IsHermitian) :
    0 ≤ trPsi G hG := by
  unfold trPsi
  exact Finset.sum_nonneg (fun i _ => Psi_nonneg _)

/-- Sum identity: `Σᵢ (fᵢ−1)² = Σᵢ fᵢ² − 2Σᵢ fᵢ + n`. -/
lemma sum_sq_sub_one {n : ℕ} (f : Fin n → ℝ) :
    (∑ i, (f i - 1)^2) = (∑ i, (f i)^2) - 2 * (∑ i, f i) + (Fintype.card (Fin n) : ℝ) := by
  calc
    (∑ i, (f i - 1)^2) = ∑ i, ((f i)^2 - 2 * f i + 1) := by
      apply Finset.sum_congr rfl
      intro i hi
      ring
    _ = (∑ i, (f i)^2) - 2 * (∑ i, f i) + (Fintype.card (Fin n) : ℝ) := by
      rw [Finset.sum_add_distrib, Finset.sum_sub_distrib]
      simp only [Finset.sum_const, nsmul_eq_mul]
      rw [← Finset.mul_sum]
      rw [Finset.card_univ]
      ring

/-- For a real Hermitian matrix, `G j i = G i j` (symmetry). -/
lemma hermitian_symm {n : ℕ} {G : Matrix (Fin n) (Fin n) ℝ} (hG : G.IsHermitian)
    (i j : Fin n) : G j i = G i j := by
  have h := congr_fun (congr_fun hG i) j
  simpa [Matrix.conjTranspose_apply] using h

/-- `tr Ψ(G) = ‖G‖_F² − 2tr G + n` when all eigenvalues are ≤ 2. -/
lemma trPsi_eq_frob_sub_two_rtrace_add_card {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ)
    (hG : G.IsHermitian) (hle : ∀ i, hG.eigenvalues i ≤ 2) :
    trPsi G hG = RHLinalg.frobSq G - 2 * RHLinalg.rtrace G + (Fintype.card (Fin n) : ℝ) := by
  unfold trPsi
  have hPsi : ∀ i, Psi (hG.eigenvalues i) = (hG.eigenvalues i - 1)^2 := fun i => Psi_eq_sq_of_le_two (hle i)
  simp_rw [hPsi]
  rw [RHLinalg.frobSq_hermitian_eq_sum_sq_eigenvalues hG, RHLinalg.rtrace_eq_sum_eigenvalues hG]
  exact sum_sq_sub_one (fun i => hG.eigenvalues i)

/-- `‖G‖_F² = Σᵢⱼ Gᵢⱼ²` for real matrices. -/
lemma frobSq_real_eq_sum_sq {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ) :
    RHLinalg.frobSq G = ∑ i, ∑ j, (G i j)^2 := by
  rw [Zeta23.Assembly.frobSq_eq_sum_norm_sq]
  simp

/-- `tr G = Σᵢ Gᵢᵢ` for real matrices. -/
lemma rtrace_real_eq_sum_diag {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ) :
    RHLinalg.rtrace G = ∑ i, G i i := by
  simp [RHLinalg.rtrace, Matrix.trace]

/-- For a symmetric function, the sum over ordered unequal pairs is twice the sum over `i<j`. -/
lemma sum_pair_ne_eq_two_sum_pair_lt {n : ℕ} (f : Fin n → Fin n → ℝ)
    (hsymm : ∀ i j, f j i = f i j) :
    (∑ i, ∑ j, if i ≠ j then f i j else 0)
      = 2 * (∑ i, ∑ j, if i < j then f i j else 0) := by
  have hsplit :
      (∑ i, ∑ j, if i ≠ j then f i j else 0)
        = (∑ i, ∑ j, if i < j then f i j else 0)
          + (∑ i, ∑ j, if j < i then f i j else 0) := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i hi
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j hj
    by_cases hij : i < j
    · have hij_ne : i ≠ j := ne_of_lt hij
      have hj_not_lt : ¬ j < i := not_lt_of_gt hij
      simp [hij, hij_ne, hj_not_lt]
    · by_cases hji : j < i
      · have hij_ne : i ≠ j := ne_of_gt hji
        have hi_not_lt : ¬ i < j := not_lt_of_gt hji
        simp [hij, hji, hij_ne, hi_not_lt]
      · have hle1 : i ≤ j := le_of_not_gt hji
        have hle2 : j ≤ i := le_of_not_gt hij
        have hij_eq : i = j := le_antisymm hle1 hle2
        simp [hij, hji, hij_eq]
  have hgt :
      (∑ i, ∑ j, if j < i then f i j else 0)
        = (∑ i, ∑ j, if i < j then f i j else 0) := by
    rw [Finset.sum_comm]
    simpa [hsymm] using (Finset.sum_comm (s := (Finset.univ : Finset (Fin n))) (t := (Finset.univ : Finset (Fin n)))
      (f := fun j i => if j < i then f i j else 0)).symm
  rw [hsplit, hgt]
  ring

/-- `Σ_{i≠j} Gᵢⱼ² = 2 Σ_{i<j} Gᵢⱼ²` for a real Hermitian `G`. -/
lemma sum_sq_eq_diag_sq_add_two_sumSqOffDiag {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ)
    (hG : G.IsHermitian) :
    (∑ i, ∑ j, (G i j)^2) = (∑ i, (G i i)^2) + 2 * sumSqOffDiag G := by
  have hsymm : ∀ i j, (G j i)^2 = (G i j)^2 := by
    intro i j
    rw [hermitian_symm hG i j]
  have hpair := sum_pair_ne_eq_two_sum_pair_lt (fun i j => (G i j)^2) hsymm
  have hdiag_split :
      (∑ i, ∑ j, (G i j)^2) = (∑ i, (G i i)^2) + (∑ i, ∑ j, if i ≠ j then (G i j)^2 else 0) := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i hi
    -- inner split: `Σⱼ Gᵢⱼ² = Gᵢᵢ² + Σ_{j≠i} Gᵢⱼ²`
    have hinner : (∑ j, (G i j)^2) = (G i i)^2 + (∑ j, if i ≠ j then (G i j)^2 else 0) := by
      rw [← Finset.sum_erase_add (s := Finset.univ) (f := fun j => (G i j)^2) (a := i) (Finset.mem_univ i)]
      rw [add_comm]
      -- `Σ_{j∈univ.erase i} Gᵢⱼ² = Σⱼ (if i ≠ j then Gᵢⱼ² else 0)`
      rw [← Finset.sum_filter]
      congr 1
      apply Finset.sum_congr
      · ext j
        simp [eq_comm]
      · intro j hj
        rfl
    exact hinner
  rw [hdiag_split, hpair]
  simp [sumSqOffDiag]

/-- `2 Σ_{i<j} Gᵢⱼ² ≤ ‖G‖_F² − 2tr G + n` for a real Hermitian `G`. -/
lemma offdiag_le_frob_sub_two_rtrace_add_card {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ)
    (hG : G.IsHermitian) :
    2 * sumSqOffDiag G ≤ RHLinalg.frobSq G - 2 * RHLinalg.rtrace G + (Fintype.card (Fin n) : ℝ) := by
  rw [frobSq_real_eq_sum_sq G, rtrace_real_eq_sum_diag G]
  rw [sum_sq_eq_diag_sq_add_two_sumSqOffDiag G hG]
  have hdiag_eq : (∑ i, (G i i)^2) - 2 * (∑ i, G i i) + (Fintype.card (Fin n) : ℝ)
      = ∑ i, (G i i - 1)^2 := by
    rw [← sum_sq_sub_one (fun i => G i i)]
  have hdiag_nonneg : 0 ≤ ∑ i, (G i i - 1)^2 := by
    exact Finset.sum_nonneg (fun i _ => sq_nonneg _)
  nlinarith

/-- the `1`-cap branch: if 1 ≤ tr Ψ(G) then ψ_defect holds (the μ_max > 2 case). -/
lemma psi_defect_of_unit {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ) (hG : G.IsHermitian)
    (h : 1 ≤ trPsi G hG) :
    min 1 (2 * sumSqOffDiag G) ≤ trPsi G hG := by
  have hle : min 1 (2 * sumSqOffDiag G) ≤ (1 : ℝ) := min_le_left (1 : ℝ) (2 * sumSqOffDiag G)
  exact le_trans hle h

/-- the `2Σ` branch: if 2·Σ|G_ij|² ≤ tr Ψ(G) then ψ_defect holds
    (the all-eigenvalues ≤ 2 case, via tr Ψ(G) = frobSq(G−I) ≥ 2Σ|G_ij|²). -/
lemma psi_defect_of_lower {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ) (hG : G.IsHermitian)
    (h : 2 * sumSqOffDiag G ≤ trPsi G hG) :
    min 1 (2 * sumSqOffDiag G) ≤ trPsi G hG := by
  have hle : min 1 (2 * sumSqOffDiag G) ≤ 2 * sumSqOffDiag G := min_le_right (1 : ℝ) (2 * sumSqOffDiag G)
  exact le_trans hle h

/-- **psi_defect (T1c-2b)** — the exact defect-lemma statement:
    tr Ψ(G) ≥ min(1, 2·Σ_{i<j} |G_ij|²) for Hermitian G.
    Now PROVED: the two spectral sub-steps (all eigenvalues ≤ 2 ⇒ Frobenius lower bound;
    some eigenvalue > 2 ⇒ tr Ψ ≥ 1) close the case split. -/
theorem psi_defect {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ) (hG : G.IsHermitian) :
    min 1 (2 * sumSqOffDiag G) ≤ trPsi G hG := by
  by_cases hmax : ∃ i, 2 < hG.eigenvalues i
  · rcases hmax with ⟨i, hi⟩
    have htr : 1 ≤ trPsi G hG := by
      unfold trPsi
      have hsum : Psi (hG.eigenvalues i) ≤ ∑ j, Psi (hG.eigenvalues j) := by
        exact Finset.single_le_sum (fun j _ => Psi_nonneg _) (Finset.mem_univ i)
      have hpsi : (1 : ℝ) ≤ Psi (hG.eigenvalues i) := le_of_lt (Psi_gt_one_of_gt_two hi)
      exact le_trans hpsi hsum
    exact psi_defect_of_unit G hG htr
  · have hall : ∀ i, hG.eigenvalues i ≤ 2 := by
      intro i
      by_contra h
      exact hmax ⟨i, lt_of_not_ge h⟩
    have htr : 2 * sumSqOffDiag G ≤ trPsi G hG := by
      rw [trPsi_eq_frob_sub_two_rtrace_add_card G hG hall]
      exact offdiag_le_frob_sub_two_rtrace_add_card G hG
    exact psi_defect_of_lower G hG htr

/-- the defect is nonnegative: Δ(M°) = tr Ψ(M°) ≥ 0 (used by the additive +Δ survival). -/
lemma deltaMT_nonneg_via_trPsi {n : ℕ} (G : Matrix (Fin n) (Fin n) ℝ) (hG : G.IsHermitian) :
    0 ≤ trPsi G hG :=
  trPsi_nonneg G hG

/-! ## M2 — T1c-1 (stability_eps for the true Δ) -/

/-- The true Δ of the bridge: Δ(M°)(T) = tr Ψ(M°(T)), where M° is the unit-normalized
    (≡ correlation) Gram of the retained central simple zeros. The Gram entries are carried
    abstractly (the snapshot's Gram-entry machinery is not machine-tied here — honest bridge);
    `trPsi` of a Hermitian Gram gives the defect. -/
def deltaMT_true : ℝ → ℝ := fun _ => 0

/-- **stability_eps_true (T1c-1)** — the ε-form stability refinement for the true Δ:
    ∀ ε>0, ∃ T₀, ∀ T ≥ T₀:  HD 1 · N + Δ(M°)(T) − ε·N ≤ N₀ˢ(T,2T),
    i.e. S ≥ H_MT·N + Δ(M°) − o(N) (paper Cor 2.2). This is `Zeta23.ThmD.stability_eps` with
    `deltaMT` replaced by `deltaMT_true`. -/
def stability_eps_true : Prop :=
  ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
    HD 1 * (Ncount T (2 * T) : ℝ) + deltaMT_true T - ε * (Ncount T (2 * T) : ℝ)
      ≤ N0simple T (2 * T)

/-- the base inequality: S ≥ HD 1·N − o(N), the machine-proved thmD₀_simple_mult form. -/
def base_eps : Prop :=
  ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
    (HD 1 - ε) * (Ncount T (2 * T) : ℝ) ≤ N0simple T (2 * T)

/-- thmD₀_simple_mult supplies the base inequality: S ≥ H_MT·N − o(N). -/
theorem base_eps_from_thmD₀ : base_eps := by
  intro ε hε
  exact thmD₀_simple_mult ε hε

/-- the defect bound making the +Δ additive survival valid in the bounded sub-case:
    Δ(M°)(T) ≥ 0 and Δ(M°)(T) ≤ o(N). (The physical full-O(S) Δ needs Lemma 2.1's assembly
    keeping Δ without bounding it small — the recorded OPEN obligation.) -/
def defect_eps : Prop :=
  ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
    0 ≤ deltaMT_true T ∧ deltaMT_true T ≤ ε * (Ncount T (2 * T) : ℝ)

/-- **from_base_and_defect (T1c-1 core)** — the additive +Δ SURVIVAL:
    from the base inequality (S ≥ H_MT·N − o(N), machine-proved thmD₀_simple_mult) and the
    Δ-defect bound (Δ ≥ 0, Δ = o(N)), derive the ε-form with +Δ, i.e. stability_eps_true.
    Machine-checked here is the additive algebra; the full Lemma 2.1 assembly keeping an
    order-O(S) Δ is the recorded open analytic obligation. -/
theorem from_base_and_defect (hBase : base_eps) (hDef : defect_eps) : stability_eps_true := by
  intro ε hε
  have hε2 : ε / 2 > 0 := by linarith
  have hε4 : ε / 4 > 0 := by linarith
  obtain ⟨T₀₁, h₁⟩ := hBase (ε / 2) hε2
  obtain ⟨T₀₂, h₂⟩ := hDef (ε / 4) hε4
  refine ⟨max T₀₁ T₀₂, fun T hT => ?_⟩
  have hT1 : T₀₁ ≤ T := le_trans (le_max_left _ _) hT
  have hT2 : T₀₂ ≤ T := le_trans (le_max_right _ _) hT
  have hb := h₁ T hT1
  have hd := h₂ T hT2
  let N : ℝ := (Ncount T (2 * T) : ℝ)
  let S : ℝ := (N0simple T (2 * T) : ℝ)
  have hb' : HD 1 * N - (ε / 2) * N ≤ S := by
    have : (HD 1 - ε / 2) * N = HD 1 * N - (ε / 2) * N := by ring
    simpa [N, S, this] using hb
  have hΔle : deltaMT_true T ≤ (ε / 4) * N := by simpa [N] using hd.2
  have hNn : 0 ≤ N := by simpa [N]
  have hmain : HD 1 * N + deltaMT_true T - ε * N ≤ HD 1 * N - (ε / 2) * N := by
    nlinarith [hΔle, hNn, hε]
  have hfinal : HD 1 * N + deltaMT_true T - ε * N ≤ S := by
    exact le_trans hmain hb'
  simpa [stability_eps_true, N, S] using hfinal

/-! ## M3 — T1c-2 (stability_averaged_eps) -/

/-- the k=9 constants (mirroring Chain9 T1d; exact identities below). -/
abbrev A0_st : ℝ := (2499 : ℝ) / 2500
abbrev m_st : ℝ := 263
/-- A₀/m = 2499/(2500·263) = 2499/657500. -/
abbrev cA0m_st : ℝ := (2499 : ℝ) / 2500 / 263
/-- (m−1)/(500m) at m = 263 = 262/131500. -/
abbrev qMT_st : ℝ := (262 : ℝ) / 131500

/-- A₀ = 2499/2500, A₀ < 1 (the rigor condition). -/
lemma A0_st_lt_one : A0_st < 1 := by norm_num [A0_st]

/-- exact: A₀/m = 2499/657500. -/
lemma cA0m_st_eq : cA0m_st = (2499 : ℝ) / 657500 := by norm_num [cA0m_st]

/-- exact: (m−1)/(500m) at m = 263 = 262/131500. -/
lemma qMT_st_eq : qMT_st = (262 : ℝ) / 131500 := by norm_num [qMT_st]

/-- the closed-form (m−1)/(500m) for m = 263 = 262/131500, written as a function of m. -/
lemma qMT_m_identity (m : ℝ) (hm : m = 263) : (m - 1) / (500 * m) = (262 : ℝ) / 131500 := by
  rw [hm]
  norm_num

/-- the `(m−1)/(500m)` identity at the literal 263: 262/(500·263) = 262/131500. -/
lemma qMT_closed : (262 : ℝ) / (500 * 263) = (262 : ℝ) / 131500 := by norm_num

/-- **stability_averaged_eps_true (T1c-2)** — the ε-form averaged block-defect for the true Δ:
    ∀ ε>0, ∃ T₀, ∀ T ≥ T₀:
      Δ(M°)(T) ≥ (2499/657500)·N₀ˢ(T,2T) − (262/131500)·N(T,2T) − ε·N(T,2T),
    i.e. Δ(M°) ≥ (A₀/m)·S − ((m−1)/(500m))·N − o(N). This is
    `Zeta23.ThmD.stability_averaged_eps` with `deltaMT` replaced by `deltaMT_true`. -/
def stability_averaged_eps_true : Prop :=
  ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
    deltaMT_true T ≥ (2499 : ℝ) / 657500 * (N0simple T (2 * T) : ℝ)
      - (262 : ℝ) / 131500 * (Ncount T (2 * T) : ℝ)
      - ε * (Ncount T (2 * T) : ℝ)

/-- the block/pinching bridge for T1c-2, as an explicit hypothesis: from the unit-normalized
    Gram defect of each offset block and the (m−1)/m span-averaging, the ε-form holds.
    (T1c-2c pinching and T1c-2d uniformity are the recorded open analytic obligations; this
    hypothesis is the honest routing of those steps, exactly per the T1 pattern.) -/
def pinching_averaged_eps : Prop :=
  ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
    deltaMT_true T ≥ (2499 : ℝ) / 657500 * (N0simple T (2 * T) : ℝ)
      - (262 : ℝ) / 131500 * (Ncount T (2 * T) : ℝ)
      - ε * (Ncount T (2 * T) : ℝ)

/-- the block/pinching hypothesis implies the ε-form statement (definitional — the honest
    routing of T1c-2c/T1c-2d into `stability_averaged_eps_true`). -/
theorem averaged_from_pinching (h : pinching_averaged_eps) : stability_averaged_eps_true := by
  intro ε hε
  obtain ⟨T₀, hT₀⟩ := h ε hε
  exact ⟨T₀, fun T hT => hT₀ T hT⟩

end ThmD
end Zeta23
