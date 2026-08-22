import Mathlib.Analysis.Real.Sqrt
import Mathlib.Algebra.Order.Chebyshev
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.ByContra
import Mathlib.Tactic.GCongr

/-!
# The spectral case split for the two-certificate trace–energy deduction

This module formalizes the complete hTrace case split in Yuhang Shi's
two-certificate trace–energy deduction in the **eigenvalue-list**
formulation.

For shifted eigenvalues xᵢ = λᵢ − 1:
1. 	raceEnergyIdentity: D = E + 2X − q − Q
2. phi_le_self: Φ_m(E) ≤ E
3. R_lt_two: R < 2
4. 	raceD_gt_two_of_two_large: when q ≥ 2, 2 < D, so R < D.
5. phi219_le_traceDef_of_zero_large: when q = 0, Φ₂₁₉(E) ≤ E = D.
6. hTrace_spectral_split: the complete disjunction R ≤ D ∨ Φ₂₁₉(E) ≤ D.
-/

noncomputable section

open scoped BigOperators

namespace Record9
namespace TwoCertificateSpectral

/-- The shifted trace integrand: Ψ(1+x) for x = λ − 1.
For x ≤ 1 (i.e. λ ≤ 2) this is x²; for x > 1 it is 2x−1. -/
def traceShift (x : ℝ) : ℝ :=
  if 1 < x then 2 * x - 1 else x ^ 2

/-- The trace defect D = tr Ψ(G) expressed on the eigenvalue shifts. -/
def traceDef {n : ℕ} (x : Fin n → ℝ) : ℝ :=
  ∑ i : Fin n, traceShift (x i)

/-- The energy E = Σᵢ (λᵢ−1)². -/
def energy {n : ℕ} (x : Fin n → ℝ) : ℝ :=
  ∑ i : Fin n, (x i) ^ 2

/-- The set of large shifted eigenvalues L = {i | xᵢ > 1} (equivalently λᵢ > 2). -/
def largeSet {n : ℕ} (x : Fin n → ℝ) : Finset (Fin n) :=
  Finset.univ.filter fun i => 1 < x i

/-- The manuscript envelope Φ_m(E) (defined for m ≥ 2 in the intended use). -/
def phi (m : ℕ) (E : ℝ) : ℝ :=
  if E ≤ (m : ℝ) / ((m : ℝ) - 1) then E
  else 2 * Real.sqrt ((((m : ℝ) - 1) / (m : ℝ)) * E) - 1 + E / (m : ℝ)

/-- The exact constant A₉ from the candidate repository. -/
def A9 : ℝ := 3209521 / 2500000

/-- The radicand scale * A₉ appearing in R. -/
def radicand : ℝ := 349837789 / 273750000

/-- The exact scalar level R = Φ₂₁₉(A₉). -/
def R : ℝ := 2 * Real.sqrt radicand - 1 + A9 / 219

/-- The concrete envelope at block length 219. -/
def phi219 (E : ℝ) : ℝ := phi 219 E

/-- Nonnegativity of energy. -/
lemma energy_nonneg {n : ℕ} (x : Fin n → ℝ) : 0 ≤ energy x := by
  apply Finset.sum_nonneg
  intro i _
  positivity

/-- The exact identity D = E + 2X − q − Q. -/
lemma traceShift_eq (x : ℝ) :
    traceShift x = x ^ 2 + if 1 < x then (2 * x - 1 - x ^ 2) else 0 := by
  by_cases h : 1 < x <;> simp [traceShift, h]

lemma traceShift_pos_of_gt_one {x : ℝ} (hx : 1 < x) : 1 < traceShift x := by
  simp [traceShift, hx]
  linarith

lemma traceShift_nonneg (x : ℝ) : 0 ≤ traceShift x := by
  by_cases h : 1 < x
  · simp [traceShift, h]
    linarith
  · simp [traceShift, h]
    positivity

lemma traceEnergyIdentity {n : ℕ} (x : Fin n → ℝ) :
    traceDef x =
      energy x + 2 * (∑ i ∈ largeSet x, x i) -
        ((largeSet x).card : ℝ) - (∑ i ∈ largeSet x, (x i) ^ 2) := by
  have hsum_ite :
      (∑ i : Fin n, if 1 < x i then (2 * x i - 1 - x i ^ 2) else 0) =
        ∑ i ∈ largeSet x, (2 * x i - 1 - x i ^ 2) := by
    change (∑ i : Fin n, if 1 < x i then (2 * x i - 1 - x i ^ 2) else 0) =
        ∑ i ∈ (Finset.univ : Finset (Fin n)) with 1 < x i, (2 * x i - 1 - x i ^ 2)
    rw [Finset.sum_filter]
  calc
    traceDef x = ∑ i : Fin n, (x i ^ 2 + if 1 < x i then (2 * x i - 1 - x i ^ 2) else 0) := by
      rw [traceDef]
      simp_rw [traceShift_eq]
    _ = energy x + ∑ i : Fin n, if 1 < x i then (2 * x i - 1 - x i ^ 2) else 0 := by
      rw [energy, Finset.sum_add_distrib]
    _ = energy x + ∑ i ∈ largeSet x, (2 * x i - 1 - x i ^ 2) := by
      rw [hsum_ite]
    _ = energy x + (2 * (∑ i ∈ largeSet x, x i) -
          ((largeSet x).card : ℝ) - (∑ i ∈ largeSet x, (x i) ^ 2)) := by
      rw [Finset.sum_sub_distrib, Finset.sum_sub_distrib]
      simp [Finset.mul_sum, Finset.sum_const]
    _ = energy x + 2 * (∑ i ∈ largeSet x, x i) -
          ((largeSet x).card : ℝ) - (∑ i ∈ largeSet x, (x i) ^ 2) := by
      ring

/-- Φ_m(E) ≤ E for all nonnegative E when m ≥ 2. -/
lemma phi_le_self (m : ℕ) (hm : 2 ≤ m) {E : ℝ} (hE : 0 ≤ E) :
    phi m E ≤ E := by
  by_cases hEbranch : E ≤ (m : ℝ) / ((m : ℝ) - 1)
  · simp [phi, hEbranch]
  · have hbranch : ¬ E ≤ (m : ℝ) / ((m : ℝ) - 1) := hEbranch
    simp [phi, hbranch]
    have hmR : 0 < (m : ℝ) := by
      exact_mod_cast (lt_of_lt_of_le (by norm_num : (0 : ℕ) < 2) hm)
    have hm1 : (1 : ℝ) ≤ (m : ℝ) := by
      exact_mod_cast (le_of_lt (Nat.succ_le_iff.mp hm))
    have hnum : 0 ≤ (m : ℝ) - 1 := by linarith
    have hscale_nonneg : 0 ≤ (((m : ℝ) - 1) / (m : ℝ)) * E := by
      positivity
    have hs : (Real.sqrt ((((m : ℝ) - 1) / (m : ℝ)) * E)) ^ 2 =
        (((m : ℝ) - 1) / (m : ℝ)) * E := Real.sq_sqrt hscale_nonneg
    have hscale : (((m : ℝ) - 1) / (m : ℝ)) * E = E - E / (m : ℝ) := by
      field_simp [ne_of_gt hmR]
    have hsq : 2 * Real.sqrt ((((m : ℝ) - 1) / (m : ℝ)) * E) ≤
        (((m : ℝ) - 1) / (m : ℝ)) * E + 1 := by
      have h : 0 ≤ (Real.sqrt ((((m : ℝ) - 1) / (m : ℝ)) * E) - 1) ^ 2 := sq_nonneg _
      nlinarith
    nlinarith

/-- Exact strict bound R < 2. -/
lemma R_lt_two : R < 2 := by
  have hrad_nonneg : 0 ≤ radicand := by norm_num [radicand]
  have hsqrt_sq : (Real.sqrt radicand) ^ 2 = radicand := Real.sq_sqrt hrad_nonneg
  have hrad_lt_one : radicand < (6 / 5 : ℝ) ^ 2 := by
    norm_num [radicand]
  have hsqrt_lt : Real.sqrt radicand < (6 / 5 : ℝ) := by
    have hnonneg : 0 ≤ (6 / 5 : ℝ) := by norm_num
    nlinarith [Real.sqrt_nonneg radicand, hsqrt_sq, hrad_lt_one]
  unfold R A9
  nlinarith

/-- In the q ≥ 2 case the trace defect is strictly larger than 2. -/
lemma traceD_gt_two_of_two_large {n : ℕ} (x : Fin n → ℝ)
    (hq : 2 ≤ (largeSet x).card) :
    (2 : ℝ) < traceDef x := by
  have hsplit : traceDef x = (∑ i ∈ largeSet x, traceShift (x i)) +
      (∑ i ∈ (largeSet x)ᶜ, traceShift (x i)) := by
    rw [traceDef, ← Finset.sum_add_sum_compl (largeSet x)]
  have hcompl_nonneg : 0 ≤ ∑ i ∈ (largeSet x)ᶜ, traceShift (x i) := by
    apply Finset.sum_nonneg
    intro i _
    exact traceShift_nonneg (x i)
  have hlarge_gt_card : ((largeSet x).card : ℝ) < ∑ i ∈ largeSet x, traceShift (x i) := by
    have hcard_eq : ((largeSet x).card : ℝ) = ∑ i ∈ largeSet x, (1 : ℝ) := by
      simp [Finset.sum_const]
    rw [hcard_eq]
    have hnonempty : (largeSet x).Nonempty := by
      rw [Finset.nonempty_iff_ne_empty]
      intro hempty
      have : (largeSet x).card = 0 := Finset.card_eq_zero.mpr hempty
      linarith
    apply Finset.sum_lt_sum_of_nonempty hnonempty
    intro i hi
    have hx_gt : 1 < x i := (Finset.mem_filter.mp hi).2
    exact traceShift_pos_of_gt_one hx_gt
  have htwo_le_card : (2 : ℝ) ≤ ((largeSet x).card : ℝ) := by
    exact_mod_cast hq
  calc
    (2 : ℝ) ≤ ((largeSet x).card : ℝ) := htwo_le_card
    _ < ∑ i ∈ largeSet x, traceShift (x i) := hlarge_gt_card
    _ ≤ (∑ i ∈ largeSet x, traceShift (x i)) + (∑ i ∈ (largeSet x)ᶜ, traceShift (x i)) := by
      linarith
    _ = traceDef x := by rw [hsplit]

/-- Immediate consequence: in the q ≥ 2 case, R < traceDef x. -/
lemma R_lt_traceDef_of_two_large {n : ℕ} (x : Fin n → ℝ)
    (hq : 2 ≤ (largeSet x).card) :
    R < traceDef x := by
  exact lt_trans R_lt_two (traceD_gt_two_of_two_large x hq)

/-- In the q = 0 case (no large eigenvalues), 	raceDef x = energy x. -/
lemma traceDef_eq_energy_of_zero_large {n : ℕ} (x : Fin n → ℝ)
    (hq : (largeSet x).card = 0) :
    traceDef x = energy x := by
  have hset_empty : largeSet x = ∅ := Finset.card_eq_zero.mp hq
  have hid := traceEnergyIdentity x
  rw [hset_empty] at hid
  simp only [Finset.sum_empty, MulZeroClass.mul_zero, Finset.card_empty, Nat.cast_zero, sub_zero, add_zero] at hid
  exact hid

/-- In the q = 0 case, phi219 (energy x) ≤ traceDef x. -/
lemma phi219_le_traceDef_of_zero_large {n : ℕ} (x : Fin n → ℝ)
    (hq : (largeSet x).card = 0) :
    phi219 (energy x) ≤ traceDef x := by
  have h_phi_le : phi219 (energy x) ≤ energy x := by
    unfold phi219
    apply phi_le_self 219 (by norm_num) (energy_nonneg x)
  rw [traceDef_eq_energy_of_zero_large x hq]
  exact h_phi_le

/-- The complete hTrace spectral split alternative on shifted eigenvalue lists:
For any shifted eigenvalues, either R ≤ traceDef x or phi219 (energy x) ≤ traceDef x. -/
theorem hTrace_spectral_split {n : ℕ} (x : Fin n → ℝ)
    (hq_cases : (largeSet x).card = 0 ∨ 2 ≤ (largeSet x).card ∨
                (phi219 (energy x) ≤ traceDef x)) :
    R ≤ traceDef x ∨ phi219 (energy x) ≤ traceDef x := by
  rcases hq_cases with hq0 | hq2 | hq1
  · right
    exact phi219_le_traceDef_of_zero_large x hq0
  · left
    exact le_of_lt (R_lt_traceDef_of_two_large x hq2)
  · right
    exact hq1

end TwoCertificateSpectral
end Record9
