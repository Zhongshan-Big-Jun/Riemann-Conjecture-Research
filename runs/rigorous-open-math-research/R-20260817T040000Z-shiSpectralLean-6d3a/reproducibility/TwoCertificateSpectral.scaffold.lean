-- SCAFFOLD (incomplete; contains `sorry`). Not a verified artifact.
import Mathlib.Data.Real.Sqrt
import Mathlib.Algebra.Order.Chebyshev
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.ByContra
import Mathlib.Tactic.GCongr

/-!
# The spectral case split for the two-certificate trace–energy deduction

This module formalizes the missing `hTrace` case split in Yuhang Shi's
two-certificate trace–energy deduction, in the **eigenvalue-list**
formulation.  We do not formalize the matrix spectral theorem here; instead
we take as primitive the list of shifted eigenvalues `xᵢ = λᵢ − 1` satisfying
`xᵢ ≥ −1` and `Σ xᵢ = 0`.

For such a list we prove the concrete alternative

`R ≤ D ∨ phi219 E ≤ D`

where `E = Σ xᵢ²`, `D = Σ Ψ(1+xᵢ)`, `phi219` is the manuscript's Φ₂₁₉
envelope, and `R = phi219(A₉)` is the exact scalar level.  This is exactly
the `hTrace` hypothesis of `TwoCertificate.Exact.concreteSupportingPlane`
(up to the separate matrix-to-eigenvalue bridge, which remains outside this
module).
-/

noncomputable section

open scoped BigOperators

namespace Record9
namespace TwoCertificateSpectral

/-- The shifted trace integrand: `Ψ(1+x)` for `x = λ − 1`.
For `x ≤ 1` (i.e. `λ ≤ 2`) this is `x²`; for `x > 1` it is `2x−1`. -/
def traceShift (x : ℝ) : ℝ :=
  if 1 < x then 2 * x - 1 else x ^ 2

/-- The trace defect `D = tr Ψ(G)` expressed on the eigenvalue shifts. -/
def traceDef {n : ℕ} (x : Fin n → ℝ) : ℝ :=
  ∑ i : Fin n, traceShift (x i)

/-- The energy `E = Σᵢ (λᵢ−1)²`. -/
def energy {n : ℕ} (x : Fin n → ℝ) : ℝ :=
  ∑ i : Fin n, (x i) ^ 2

/-- The set of large shifted eigenvalues `L = {i | xᵢ > 1}` (equivalently `λᵢ > 2`). -/
def largeSet {n : ℕ} (x : Fin n → ℝ) : Finset (Fin n) :=
  Finset.univ.filter fun i => 1 < x i

/-- The manuscript envelope `Φ_m(E)` (defined for `m ≥ 2` in the intended use). -/
def phi (m : ℕ) (E : ℝ) : ℝ :=
  if E ≤ (m : ℝ) / ((m : ℝ) - 1) then E
  else 2 * Real.sqrt ((((m : ℝ) - 1) / (m : ℝ)) * E) - 1 + E / (m : ℝ)

/-- The exact constant `A₉` from the candidate repository. -/
def A9 : ℝ := 3209521 / 2500000

/-- The radicand `scale * A₉` appearing in `R`. -/
def radicand : ℝ := 349837789 / 273750000

/-- The exact scalar level `R = Φ₂₁₉(A₉)`. -/
def R : ℝ := 2 * Real.sqrt radicand - 1 + A9 / 219

/-- The concrete envelope at block length 219. -/
def phi219 (E : ℝ) : ℝ := phi 219 E

/-- The exact identity `D = E + 2X − q − Q`. -/
lemma traceShift_eq (x : ℝ) :
    traceShift x = x ^ 2 + if 1 < x then (2 * x - 1 - x ^ 2) else 0 := by
  by_cases h : 1 < x <;> simp [traceShift, h]

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

/-- `Φ_m(E) ≤ E` for all nonnegative `E` when `m ≥ 2`. -/
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

/-- Exact strict bound `R < 2`. -/
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

/-- In the `q ≥ 2` case the trace defect is strictly larger than `2`. -/
lemma traceD_gt_two_of_two_large {n : ℕ} (x : Fin n → ℝ)
    (hx_lower : ∀ i : Fin n, -1 ≤ x i)
    (hsum : ∑ i : Fin n, x i = 0)
    (hq : 2 ≤ (largeSet x).card) :
    (2 : ℝ) < traceDef x := by
  -- Placeholder; will be replaced.
  sorry

end TwoCertificateSpectral
end Record9
