/-
Record9.XiPrimeAtOneFacts2 — machine-checked proof of the M3-open-A(ii) obligation

    two_integral_vConv_vMT_fact :
      2 * ∫ r in (0:ℝ)..1, vConv vMT r = (IvMT) ^ 2

(i.e. the Lean name for the open obligation `two_integral_vConv_vMT` declared in
`Record9.XiPrimeAtOne`).  The route:

  1. `vConvMT_closed_fact` (from Record9.XiPrimeAtOneFacts) replaces `vConv vMT r`
     by `vConvMTcl r` inside the integral over r ∈ [0,1].
  2. ∫₀¹ (1−r)·cos(√2·r) dr = (1 − cos √2)/2  (antiderivative (1−r)sin(√2 r)/√2 − cos(√2 r)/2).
  3. ∫₀¹ sin(√2·(1−r)) dr = (1 − cos √2)/√2   (antiderivative cos(√2(1−r))/√2).
  4. Therefore ∫₀¹ vConvMTcl r dr = (1 − cos √2)/2.
  5. (IvMT)² = 1 − cos √2   (via `Real.cos_two_mul_eq_one_sub` and `sqrt_two_mul_half_eq_inv`).
  6. Combine.

No sorry/admit/axiom; the snapshot `literature/raw/zeta-23-lean/` is untouched.
-/
import Record9.XiPrimeAtOneFacts

noncomputable section

open Set MeasureTheory
open intervalIntegral
open Real

namespace Zeta23
namespace XiPrime

/-! ## integral helpers on [0,1] -/

/-- ∫₀¹ (1−r)·cos(√2·r) dr = (1 − cos √2)/2.
    Antiderivative: (1−r)·sin(√2·r)/√2 − cos(√2·r)/2. -/
lemma integral_one_sub_mul_cos_sqrt2 :
    (∫ r in (0 : ℝ)..1, (1 - r) * Real.cos (Real.sqrt 2 * r)) =
      (1 - Real.cos (Real.sqrt 2)) / 2 := by
  have hder (r : ℝ) : HasDerivAt
      (fun r : ℝ => (1 - r) * Real.sin (Real.sqrt 2 * r) / Real.sqrt 2 -
        Real.cos (Real.sqrt 2 * r) / 2)
      ((1 - r) * Real.cos (Real.sqrt 2 * r)) r := by
    have hinner (s : ℝ) : HasDerivAt (fun t : ℝ => Real.sqrt 2 * t) (Real.sqrt 2) s := by
      simpa [mul_comm] using (hasDerivAt_id s).mul_const (Real.sqrt 2)
    have hlin : HasDerivAt (fun t : ℝ => 1 - t) (-1) r := (hasDerivAt_id r).const_sub (1 : ℝ)
    have hsin : HasDerivAt (fun t : ℝ => Real.sin (Real.sqrt 2 * t))
        (Real.cos (Real.sqrt 2 * r) * Real.sqrt 2) r := by
      exact HasDerivAt.comp r (hasDerivAt_sin (Real.sqrt 2 * r)) (hinner r)
    have hprod : HasDerivAt (fun t : ℝ => (1 - t) * Real.sin (Real.sqrt 2 * t))
        ((-1) * Real.sin (Real.sqrt 2 * r) +
          (1 - r) * (Real.cos (Real.sqrt 2 * r) * Real.sqrt 2)) r :=
      hlin.mul hsin
    have hterm1 : HasDerivAt (fun t : ℝ => (1 - t) * Real.sin (Real.sqrt 2 * t) / Real.sqrt 2)
        (((-1) * Real.sin (Real.sqrt 2 * r) +
          (1 - r) * (Real.cos (Real.sqrt 2 * r) * Real.sqrt 2)) / Real.sqrt 2) r :=
      hprod.div_const (Real.sqrt 2)
    have hcos : HasDerivAt (fun t : ℝ => Real.cos (Real.sqrt 2 * t))
        (-Real.sin (Real.sqrt 2 * r) * Real.sqrt 2) r := by
      exact HasDerivAt.comp r (hasDerivAt_cos (Real.sqrt 2 * r)) (hinner r)
    have hterm2 : HasDerivAt (fun t : ℝ => Real.cos (Real.sqrt 2 * t) / 2)
        ((-Real.sin (Real.sqrt 2 * r) * Real.sqrt 2) / 2) r :=
      hcos.div_const 2
    have hsub := hterm1.sub hterm2
    convert hsub
    all_goals try rfl
    field_simp [sqrt_two_ne_zero]
    ring_nf
    rw [sqrt_two_sq]
    ring
  have hint : IntervalIntegrable (fun r : ℝ => (1 - r) * Real.cos (Real.sqrt 2 * r))
      MeasureTheory.volume (0 : ℝ) 1 := by
    exact ((by fun_prop : Continuous (fun r : ℝ => (1 - r) * Real.cos (Real.sqrt 2 * r))).intervalIntegrable 0 1)
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt (fun r _ => hder r) hint]
  simp [Real.sin_zero, Real.cos_zero]
  ring

/-- ∫₀¹ sin(√2·(1−r)) dr = (1 − cos √2)/√2.
    Antiderivative: cos(√2·(1−r))/√2. -/
lemma integral_sin_sqrt2_sub_one :
    (∫ r in (0 : ℝ)..1, Real.sin (Real.sqrt 2 * (1 - r))) =
      (1 - Real.cos (Real.sqrt 2)) / Real.sqrt 2 := by
  have hder (r : ℝ) : HasDerivAt
      (fun r : ℝ => Real.cos (Real.sqrt 2 * (1 - r)) / Real.sqrt 2)
      (Real.sin (Real.sqrt 2 * (1 - r))) r := by
    have hlin : HasDerivAt (fun t : ℝ => 1 - t) (-1) r := (hasDerivAt_id r).const_sub (1 : ℝ)
    have hinner : HasDerivAt (fun t : ℝ => Real.sqrt 2 * (1 - t)) (-Real.sqrt 2) r := by
      simpa [mul_neg] using hlin.const_mul (Real.sqrt 2)
    have hcos : HasDerivAt (fun t : ℝ => Real.cos (Real.sqrt 2 * (1 - t)))
        (-Real.sin (Real.sqrt 2 * (1 - r)) * (-Real.sqrt 2)) r := by
      have hc := HasDerivAt.comp r (hasDerivAt_cos (Real.sqrt 2 * (1 - r))) hinner
      convert hc <;> rfl
    have hdiv : HasDerivAt (fun t : ℝ => Real.cos (Real.sqrt 2 * (1 - t)) / Real.sqrt 2)
        (Real.sin (Real.sqrt 2 * (1 - r))) r := by
      convert hcos.div_const (Real.sqrt 2)
      all_goals try rfl
      field_simp [sqrt_two_ne_zero]
    exact hdiv
  have hint : IntervalIntegrable (fun r : ℝ => Real.sin (Real.sqrt 2 * (1 - r)))
      MeasureTheory.volume (0 : ℝ) 1 := by
    exact ((by fun_prop : Continuous (fun r : ℝ => Real.sin (Real.sqrt 2 * (1 - r)))).intervalIntegrable 0 1)
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt (fun r _ => hder r) hint]
  simp [Real.cos_zero]
  field_simp [sqrt_two_ne_zero]

/-- ∫₀¹ vConvMTcl r dr = (1 − cos √2)/2. -/
lemma integral_vConvMTcl :
    (∫ r in (0 : ℝ)..1, vConvMTcl r) = (1 - Real.cos (Real.sqrt 2)) / 2 := by
  unfold vConvMTcl
  have h1 : (∫ r in (0 : ℝ)..1, (1 / 2 : ℝ) * ((1 - r) * Real.cos (Real.sqrt 2 * r))) =
      (1 / 2 : ℝ) * (∫ r in (0 : ℝ)..1, (1 - r) * Real.cos (Real.sqrt 2 * r)) := by
    simp
  have h2 : (∫ r in (0 : ℝ)..1, Real.sin (Real.sqrt 2 * (1 - r)) / (2 * Real.sqrt 2)) =
      (1 / (2 * Real.sqrt 2)) * (∫ r in (0 : ℝ)..1, Real.sin (Real.sqrt 2 * (1 - r))) := by
    rw [show (fun r : ℝ => Real.sin (Real.sqrt 2 * (1 - r)) / (2 * Real.sqrt 2)) =
        fun r : ℝ => (1 / (2 * Real.sqrt 2)) * Real.sin (Real.sqrt 2 * (1 - r)) by
          funext r; ring]
    simp
  rw [intervalIntegral.integral_add]
  · rw [h1, h2, integral_one_sub_mul_cos_sqrt2, integral_sin_sqrt2_sub_one]
    field_simp [sqrt_two_ne_zero]
    ring_nf
    rw [sqrt_two_sq]
    ring
  · exact ((by fun_prop : Continuous (fun r : ℝ => (1 / 2 : ℝ) * ((1 - r) * Real.cos (Real.sqrt 2 * r)))).intervalIntegrable 0 1)
  · exact ((by fun_prop : Continuous (fun r : ℝ => Real.sin (Real.sqrt 2 * (1 - r)) / (2 * Real.sqrt 2))).intervalIntegrable 0 1)

/-- (IvMT)² = 1 − cos √2. -/
lemma IvMT_sq_eq_one_sub_cos_sqrt2 : (IvMT) ^ 2 = 1 - Real.cos (Real.sqrt 2) := by
  unfold IvMT
  rw [mul_pow, sqrt_two_sq]
  have hcos : Real.cos (Real.sqrt 2) = Real.cos (2 * (1 / Real.sqrt 2)) := by
    congr 1
    calc
      Real.sqrt 2 = (2 : ℝ) * (Real.sqrt 2 * (1 / 2 : ℝ)) := by ring
      _ = (2 : ℝ) * (1 / Real.sqrt 2) := by rw [sqrt_two_mul_half_eq_inv]
  have htwomul : 2 * Real.sin (1 / Real.sqrt 2) ^ 2 = 1 - Real.cos (2 * (1 / Real.sqrt 2)) := by
    rw [Real.cos_two_mul_eq_one_sub (1 / Real.sqrt 2)]
    ring
  rw [htwomul, hcos]

/-! ## the main theorem -/

/-- M3-open-A(ii): 2∫₀¹ vConv vMT = (∫vMT)² (Fubini identity for the autocorrelation). -/
theorem two_integral_vConv_vMT_fact : 2 * ∫ r in (0 : ℝ)..1, vConv vMT r = (IvMT) ^ 2 := by
  have hcl : (∫ r in (0 : ℝ)..1, vConv vMT r) = ∫ r in (0 : ℝ)..1, vConvMTcl r := by
    apply intervalIntegral.integral_congr
    intro r hr
    exact vConvMT_closed_fact r (by simpa [uIcc_of_le (by norm_num : (0 : ℝ) ≤ 1)] using hr)
  rw [hcl, integral_vConvMTcl, IvMT_sq_eq_one_sub_cos_sqrt2]
  ring

end XiPrime
end Zeta23

end
