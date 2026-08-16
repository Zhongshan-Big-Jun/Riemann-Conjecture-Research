/-
Record9.XiPrimeAtOneFacts — T3-open-A promotion pass: prove the AtOne analytic facts for the
ξ′ MT-window constant as real lemmas, eliminating (as many as possible of) the hypotheses
vConvMT_closed, two_integral_vConv_vMT, integral_vMT_forms, IvMT_pos, jWin_D1_one_vMT_sandwich
from the open list M3-open-A.

No sorry/admit/axiom.  The snapshot `literature/raw/zeta-23-lean/` is untouched.
-/
import Record9.XiPrimeAtOne

noncomputable section

open Set MeasureTheory
open intervalIntegral
open Real

namespace Zeta23
namespace XiPrime

/-- √2 = 2^(1/2) > 0. -/
lemma sqrt_two_pos : (0 : ℝ) < Real.sqrt 2 := by positivity

lemma sqrt_two_ne_zero : Real.sqrt 2 ≠ 0 := sqrt_two_pos.ne'

/-- √2 · (1/2) = 1/√2. -/
lemma sqrt_two_mul_half_eq_inv : Real.sqrt 2 * (1 / 2 : ℝ) = 1 / Real.sqrt 2 := by
  have h : Real.sqrt 2 * (1 / 2 : ℝ) * Real.sqrt 2 = 1 := by
    rw [show Real.sqrt 2 * (1 / 2 : ℝ) * Real.sqrt 2 = (Real.sqrt 2 * Real.sqrt 2) * (1 / 2 : ℝ) by ring]
    rw [← sq, sqrt_two_sq]
    norm_num
  exact (eq_div_iff sqrt_two_ne_zero).2 h

lemma one_le_sqrt_two : (1 : ℝ) ≤ Real.sqrt 2 := by
  rw [← Real.sqrt_one]
  exact Real.sqrt_le_sqrt (by norm_num : (1 : ℝ) ≤ (2 : ℝ))

lemma one_div_sqrt_two_le_one : (1 : ℝ) / Real.sqrt 2 ≤ 1 := by
  have hs : 0 < Real.sqrt 2 := sqrt_two_pos
  rw [div_le_iff₀ hs]
  simpa using one_le_sqrt_two

lemma one_div_sqrt_two_pos : (0 : ℝ) < 1 / Real.sqrt 2 :=
  div_pos zero_lt_one sqrt_two_pos

lemma one_div_sqrt_two_lt_pi : (1 : ℝ) / Real.sqrt 2 < Real.pi := by
  have hpi : (1 : ℝ) < Real.pi := by linarith [Real.pi_gt_three]
  linarith [one_div_sqrt_two_le_one]

/-- M3-open-A(iv): 0 < IvMT, so the division in κ₁ is well-defined and the D₁-tail enters
    with the correct sign. -/
theorem IvMT_pos_fact : 0 < IvMT := by
  have hsin : 0 < Real.sin (1 / Real.sqrt 2) :=
    Real.sin_pos_of_pos_of_lt_pi one_div_sqrt_two_pos one_div_sqrt_two_lt_pi
  unfold IvMT
  exact mul_pos sqrt_two_pos hsin

/-! ## integral helpers -/

/-- ∫ cos(a·s) ds over [b,c] = (sin(a·c) − sin(a·b))/a, for a ≠ 0. -/
lemma integral_cos_mul {a b c : ℝ} (ha : a ≠ 0) :
    (∫ s in b..c, Real.cos (a * s)) = (Real.sin (a * c) - Real.sin (a * b)) / a := by
  have hder (s : ℝ) : HasDerivAt (fun s : ℝ => Real.sin (a * s) / a) (Real.cos (a * s)) s := by
    have hlast : HasDerivAt (fun s : ℝ => Real.sin (a * s)) (Real.cos (a * s) * a) s := by
      have hinner : HasDerivAt (fun s : ℝ => a * s) a s := by
        simpa [mul_comm] using (hasDerivAt_id s).mul_const a
      exact HasDerivAt.comp s (hasDerivAt_sin (a * s)) hinner
    have hdiv : HasDerivAt (fun s : ℝ => Real.sin (a * s) / a)
        (Real.cos (a * s) * a / a) s := hlast.div_const a
    convert hdiv using 1
    field_simp [ha]
  have hint : IntervalIntegrable (fun s : ℝ => Real.cos (a * s)) MeasureTheory.volume b c := by
    exact ((by fun_prop : Continuous (fun s : ℝ => Real.cos (a * s))).intervalIntegrable b c)
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt (fun s _ => hder s) hint]
  field_simp [ha]

/-- ∫ cos(a·s + b0) ds over [b,c] = (sin(a·c + b0) − sin(a·b + b0))/a, for a ≠ 0. -/
lemma integral_cos_mul_add {a b0 b c : ℝ} (ha : a ≠ 0) :
    (∫ s in b..c, Real.cos (a * s + b0)) =
      (Real.sin (a * c + b0) - Real.sin (a * b + b0)) / a := by
  have hder (s : ℝ) : HasDerivAt (fun s : ℝ => Real.sin (a * s + b0) / a)
      (Real.cos (a * s + b0)) s := by
    have hlast : HasDerivAt (fun s : ℝ => Real.sin (a * s + b0)) (Real.cos (a * s + b0) * a) s := by
      have hinner : HasDerivAt (fun s : ℝ => a * s + b0) a s := by
        simpa [mul_comm] using ((hasDerivAt_id s).mul_const a).add_const b0
      exact HasDerivAt.comp s (hasDerivAt_sin (a * s + b0)) hinner
    have hdiv : HasDerivAt (fun s : ℝ => Real.sin (a * s + b0) / a)
        (Real.cos (a * s + b0) * a / a) s := hlast.div_const a
    convert hdiv using 1
    field_simp [ha]
  have hint : IntervalIntegrable (fun s : ℝ => Real.cos (a * s + b0)) MeasureTheory.volume b c := by
    exact ((by fun_prop : Continuous (fun s : ℝ => Real.cos (a * s + b0))).intervalIntegrable b c)
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt (fun s _ => hder s) hint]
  field_simp [ha]

/-- ∫ cos²(a·s) ds over [b,c] = (c−b)/2 + (sin(2ac) − sin(2ab))/(4a), for a ≠ 0. -/
lemma integral_cos_sq_mul {a b c : ℝ} (ha : a ≠ 0) :
    (∫ s in b..c, (Real.cos (a * s)) ^ 2) =
      (c - b) / 2 + (Real.sin (2 * a * c) - Real.sin (2 * a * b)) / (4 * a) := by
  have hident : (fun s : ℝ => Real.cos (a * s) ^ 2) =
      fun s : ℝ => (1 / 2 : ℝ) + Real.cos (2 * a * s) / 2 := by
    funext s
    rw [show 2 * a * s = 2 * (a * s) by ring]
    nth_rewrite 1 [← Real.cos_sq (a * s)]
    ring
  rw [hident]
  have h1 : (∫ s in b..c, (1 / 2 : ℝ) + Real.cos (2 * a * s) / 2) =
      (∫ s in b..c, (1 / 2 : ℝ)) + (∫ s in b..c, Real.cos (2 * a * s) / 2) := by
    apply intervalIntegral.integral_add
    · exact (intervalIntegrable_const : IntervalIntegrable (fun _ : ℝ => (1 / 2 : ℝ)) volume b c)
    · exact ((by fun_prop : Continuous (fun s : ℝ => Real.cos (2 * a * s) / 2)).intervalIntegrable b c)
  rw [h1]
  have hconst : (∫ s in b..c, (1 / 2 : ℝ)) = (c - b) * (1 / 2) := by
    rw [intervalIntegral.integral_const]
    ring
  rw [hconst]
  have ha2 : 2 * a ≠ 0 := by
    exact mul_ne_zero (by norm_num : (2 : ℝ) ≠ 0) ha
  have hc := integral_cos_mul (b := b) (c := c) ha2
  have hcos : (∫ s in b..c, Real.cos (2 * a * s) / 2) =
      (Real.sin (2 * a * c) - Real.sin (2 * a * b)) / (2 * a) / 2 := by
    rw [show (fun s : ℝ => Real.cos (2 * a * s) / 2) =
        fun s : ℝ => (1 / 2 : ℝ) * Real.cos (2 * a * s) by funext s; ring]
    rw [intervalIntegral.integral_const_mul]
    rw [hc]
    ring
  rw [hcos]; ring

/-- M3-open-A(iii): ∫vMT = IvMT and ∫vMT² = aMT (trig integral evaluations). -/
theorem integral_vMT_forms_fact :
    (∫ s in (-(1 : ℝ) / 2)..(1 / 2), vMT s = IvMT) ∧
      (∫ s in (-(1 : ℝ) / 2)..(1 / 2), vMT s ^ 2 = aMT) := by
  have h1 : (∫ s in (-(1 : ℝ) / 2)..(1 / 2), vMT s) = IvMT := by
    have hc := integral_cos_mul (a := Real.sqrt 2) (b := -(1 : ℝ) / 2) (c := 1 / 2) sqrt_two_ne_zero
    have harg1 : Real.sqrt 2 * (1 / 2 : ℝ) = 1 / Real.sqrt 2 := sqrt_two_mul_half_eq_inv
    have harg2 : Real.sqrt 2 * (-(1 : ℝ) / 2) = -(1 / Real.sqrt 2) := by
      have hb : -(1 : ℝ) / 2 = -(1 / 2 : ℝ) := by ring
      rw [hb, mul_neg, sqrt_two_mul_half_eq_inv]
    unfold vMT IvMT
    calc
      (∫ s in (-(1 : ℝ) / 2)..(1 / 2), Real.cos (Real.sqrt 2 * s))
          = (Real.sin (Real.sqrt 2 * (1 / 2)) - Real.sin (Real.sqrt 2 * (-(1 : ℝ) / 2))) / Real.sqrt 2 := by
            exact hc
      _ = (Real.sin (1 / Real.sqrt 2) - Real.sin (-(1 / Real.sqrt 2))) / Real.sqrt 2 := by
            rw [harg1, harg2]
      _ = (Real.sin (1 / Real.sqrt 2) - (-Real.sin (1 / Real.sqrt 2))) / Real.sqrt 2 := by
            rw [Real.sin_neg]
      _ = Real.sqrt 2 * Real.sin (1 / Real.sqrt 2) := by
            have hsq2 : Real.sqrt 2 * Real.sqrt 2 = (2 : ℝ) := by rw [← sq, sqrt_two_sq]
            have hs : Real.sqrt 2 ≠ 0 := sqrt_two_ne_zero
            have hmid : (Real.sin (1 / Real.sqrt 2) - (-Real.sin (1 / Real.sqrt 2))) / Real.sqrt 2
                = (2 * Real.sin (1 / Real.sqrt 2)) / Real.sqrt 2 := by ring_nf
            rw [hmid]
            rw [div_eq_iff hs]
            rw [show (2 : ℝ) * Real.sin (1 / Real.sqrt 2)
                = (Real.sqrt 2 * Real.sqrt 2) * Real.sin (1 / Real.sqrt 2) by rw [hsq2]]
            ring
  have h2 : (∫ s in (-(1 : ℝ) / 2)..(1 / 2), vMT s ^ 2) = aMT := by
    have hcs := integral_cos_sq_mul (a := Real.sqrt 2) (b := -(1 : ℝ) / 2) (c := 1 / 2) sqrt_two_ne_zero
    have ha : 2 * Real.sqrt 2 * (1 / 2 : ℝ) = Real.sqrt 2 := by ring_nf
    have hb : 2 * Real.sqrt 2 * (-(1 : ℝ) / 2) = -Real.sqrt 2 := by ring_nf
    have hr : (1 / 2 - (-(1 : ℝ) / 2) : ℝ) / 2 = 1 / 2 := by norm_num
    unfold vMT aMT
    calc
      (∫ s in (-(1 : ℝ) / 2)..(1 / 2), Real.cos (Real.sqrt 2 * s) ^ 2)
          = (1 / 2 - (-(1 : ℝ) / 2)) / 2
              + (Real.sin (2 * Real.sqrt 2 * (1 / 2)) - Real.sin (2 * Real.sqrt 2 * (-(1 : ℝ) / 2))) / (4 * Real.sqrt 2) := by
            exact hcs
      _ = (1 : ℝ) / 2 + (Real.sin (Real.sqrt 2) - Real.sin (-Real.sqrt 2)) / (4 * Real.sqrt 2) := by
            rw [hr, ha, hb]
      _ = (1 : ℝ) / 2 + (Real.sin (Real.sqrt 2) - (-Real.sin (Real.sqrt 2))) / (4 * Real.sqrt 2) := by
            rw [Real.sin_neg]
      _ = 1 / 2 + Real.sin (Real.sqrt 2) / (2 * Real.sqrt 2) := by
            field_simp [sqrt_two_ne_zero]
            ring
  exact ⟨h1, h2⟩

/-- M3-open-A(i): vConv vMT = vConvMTcl pointwise on [0,1] (product-to-sum closed form). -/
theorem vConvMT_closed_fact : ∀ r ∈ Icc (0 : ℝ) 1, vConv vMT r = vConvMTcl r := by
  intro r hr
  unfold vConv vMT vConvMTcl
  have hprod (s : ℝ) :
      Real.cos (Real.sqrt 2 * s) * Real.cos (Real.sqrt 2 * (s + r))
        = (1 / 2) * Real.cos (Real.sqrt 2 * r) + (1 / 2) * Real.cos (2 * Real.sqrt 2 * s + Real.sqrt 2 * r) := by
    calc
      Real.cos (Real.sqrt 2 * s) * Real.cos (Real.sqrt 2 * (s + r))
          = (2 * (Real.cos (Real.sqrt 2 * s) * Real.cos (Real.sqrt 2 * (s + r)))) / 2 := by ring
      _ = (Real.cos (Real.sqrt 2 * s - Real.sqrt 2 * (s + r))
              + Real.cos (Real.sqrt 2 * s + Real.sqrt 2 * (s + r))) / 2 := by
            have htwo := Real.two_mul_cos_mul_cos (Real.sqrt 2 * s) (Real.sqrt 2 * (s + r))
            rw [show 2 * (Real.cos (Real.sqrt 2 * s) * Real.cos (Real.sqrt 2 * (s + r)))
                = 2 * Real.cos (Real.sqrt 2 * s) * Real.cos (Real.sqrt 2 * (s + r)) by ring]
            rw [htwo]
      _ = (Real.cos (Real.sqrt 2 * r) + Real.cos (2 * Real.sqrt 2 * s + Real.sqrt 2 * r)) / 2 := by
            rw [show Real.sqrt 2 * s - Real.sqrt 2 * (s + r) = -(Real.sqrt 2 * r) by ring]
            rw [show Real.sqrt 2 * s + Real.sqrt 2 * (s + r) = 2 * Real.sqrt 2 * s + Real.sqrt 2 * r by ring]
            rw [Real.cos_neg]
      _ = (1 / 2) * Real.cos (Real.sqrt 2 * r) + (1 / 2) * Real.cos (2 * Real.sqrt 2 * s + Real.sqrt 2 * r) := by ring
  have hc : (∫ s in (-(1 : ℝ) / 2)..(1 / 2 - r), Real.cos (Real.sqrt 2 * s) * Real.cos (Real.sqrt 2 * (s + r)))
      = (∫ s in (-(1 : ℝ) / 2)..(1 / 2 - r),
          (1 / 2) * Real.cos (Real.sqrt 2 * r) + (1 / 2) * Real.cos (2 * Real.sqrt 2 * s + Real.sqrt 2 * r)) := by
    apply intervalIntegral.integral_congr
    intro s hs
    exact hprod s
  rw [hc]
  have hlen : (1 / 2 - r) - (-(1 : ℝ) / 2) = 1 - r := by ring
  have hconst : (∫ s in (-(1 : ℝ) / 2)..(1 / 2 - r), (1 / 2) * Real.cos (Real.sqrt 2 * r))
      = ((1 / 2) * Real.cos (Real.sqrt 2 * r)) * (1 - r) := by
    rw [intervalIntegral.integral_const]
    rw [hlen]
    ring
  have ha2 : 2 * Real.sqrt 2 ≠ 0 := by
    exact mul_ne_zero (by norm_num : (2 : ℝ) ≠ 0) sqrt_two_ne_zero
  have hsin1 : 2 * Real.sqrt 2 * (1 / 2 - r) + Real.sqrt 2 * r = Real.sqrt 2 * (1 - r) := by ring
  have hsin2 : 2 * Real.sqrt 2 * (-(1 : ℝ) / 2) + Real.sqrt 2 * r = -(Real.sqrt 2 * (1 - r)) := by ring
  have hcos2 : (∫ s in (-(1 : ℝ) / 2)..(1 / 2 - r), (1 / 2) * Real.cos (2 * Real.sqrt 2 * s + Real.sqrt 2 * r))
      = (1 / 2) * (Real.sin (Real.sqrt 2 * (1 - r)) - Real.sin (-(Real.sqrt 2 * (1 - r)))) / (2 * Real.sqrt 2) := by
    rw [show (fun s : ℝ => (1 / 2 : ℝ) * Real.cos (2 * Real.sqrt 2 * s + Real.sqrt 2 * r))
        = fun s : ℝ => (1 / 2) * Real.cos (2 * Real.sqrt 2 * s + Real.sqrt 2 * r) by rfl]
    rw [intervalIntegral.integral_const_mul]
    have hc2 := integral_cos_mul_add (a := 2 * Real.sqrt 2) (b0 := Real.sqrt 2 * r)
      (b := -(1 : ℝ) / 2) (c := 1 / 2 - r) ha2
    rw [hc2]
    rw [hsin1, hsin2]
    ring
  -- assemble
  calc
    (∫ s in (-(1 : ℝ) / 2)..(1 / 2 - r),
        (1 / 2) * Real.cos (Real.sqrt 2 * r) + (1 / 2) * Real.cos (2 * Real.sqrt 2 * s + Real.sqrt 2 * r))
        = (∫ s in (-(1 : ℝ) / 2)..(1 / 2 - r), (1 / 2) * Real.cos (Real.sqrt 2 * r))
            + (∫ s in (-(1 : ℝ) / 2)..(1 / 2 - r), (1 / 2) * Real.cos (2 * Real.sqrt 2 * s + Real.sqrt 2 * r)) := by
          apply intervalIntegral.integral_add
          · exact (intervalIntegrable_const : IntervalIntegrable (fun _ : ℝ => (1 / 2) * Real.cos (Real.sqrt 2 * r)) volume (-(1 : ℝ) / 2) (1 / 2 - r))
          · exact ((by fun_prop : Continuous (fun s : ℝ => (1 / 2) * Real.cos (2 * Real.sqrt 2 * s + Real.sqrt 2 * r))).intervalIntegrable (-(1 : ℝ) / 2) (1 / 2 - r))
    _ = ((1 / 2) * Real.cos (Real.sqrt 2 * r)) * (1 - r)
        + (1 / 2) * (Real.sin (Real.sqrt 2 * (1 - r)) - Real.sin (-(Real.sqrt 2 * (1 - r)))) / (2 * Real.sqrt 2) := by
          rw [hconst, hcos2]
    _ = ((1 / 2) * Real.cos (Real.sqrt 2 * r)) * (1 - r)
        + (1 / 2) * (Real.sin (Real.sqrt 2 * (1 - r)) - (-Real.sin (Real.sqrt 2 * (1 - r)))) / (2 * Real.sqrt 2) := by
          rw [Real.sin_neg]
    _ = (1 / 2) * ((1 - r) * Real.cos (Real.sqrt 2 * r)) + Real.sin (Real.sqrt 2 * (1 - r)) / (2 * Real.sqrt 2) := by
          congr 1
          · ring
          · field_simp [sqrt_two_ne_zero]
            ring

end XiPrime
end Zeta23

end
