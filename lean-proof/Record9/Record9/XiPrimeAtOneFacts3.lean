/-
Record9.XiPrimeAtOneFacts3 — machine-checked proof of the last M3-open-A AtOne obligation

    jWin_D1_one_vMT_sandwich_fact :
      J1MT ≤ jWin D1 1 vMT ∧ jWin D1 1 vMT ≤ J1MT + eps9 * (IvMT)^2

(i.e. the Lean name for the open obligation `jWin_D1_one_vMT_sandwich` declared in
`Record9.XiPrimeAtOne`).  The route is the generic AtOne certificate comparison
`jWin_one_le_of_le` applied to the MT window:

  lower: D1trunc 9 ≤ D1   ⇒  J1MT = jWin(D1trunc 9,1,vMT) ≤ jWin(D1,1,vMT)
  upper: D1 ≤ D1trunc 9 + eps9  ⇒  jWin(D1,1,vMT) ≤ J1MT + eps9 * 2∫₀¹ vConvMTcl
                                     = J1MT + eps9 * (IvMT)^2  (Fubini).

Uses the already machine-proved `vConvMT_closed_fact`,
`two_integral_vConv_vMT_fact`, and nonnegativity of vMT on the window.

No sorry/admit/axiom; the snapshot `literature/raw/zeta-23-lean/` is untouched.
-/
import Record9.XiPrimeAtOneFacts2
import Zeta23.XiPrime.Window

noncomputable section

open Set MeasureTheory
open intervalIntegral
open Real

namespace Zeta23
namespace XiPrime

/-- vConvMTcl ≥ 0 on [0,1] (because it is the autocorrelation of the nonnegative vMT). -/
lemma vConvMTcl_nonneg {r : ℝ} (hr : r ∈ Icc (0 : ℝ) 1) : 0 ≤ vConvMTcl r := by
  have hv : ∀ s ∈ Icc (-(1 : ℝ) / 2) (1 / 2), 0 ≤ vMT s := by
    intro s hs
    have hs' : s ∈ Icc (-(1 / 2 : ℝ)) (1 / 2) := by
      constructor <;> linarith [hs.1, hs.2]
    exact vMT_nonneg_on hs'
  have h := vConv_nonneg (v := vMT) hv hr
  rwa [vConvMT_closed_fact r hr] at h

/-- jWin(D1trunc 9,1,vMT) = J1MT (definitional/closed-form rewrite). -/
lemma jWin_trunc9_vMT : jWin (D1trunc 9) 1 vMT = J1MT := by
  rw [jWin_one]
  unfold J1MT
  congr 1
  apply intervalIntegral.integral_congr
  intro r hr
  have hcl := vConvMT_closed_fact r (by simpa [uIcc_of_le (by norm_num : (0 : ℝ) ≤ 1)] using hr)
  simp [hcl]

/-- 2∫₀¹ vConvMTcl = (IvMT)², the Fubini identity in closed form. -/
lemma two_integral_vConvMTcl : 2 * ∫ r in (0 : ℝ)..1, vConvMTcl r = (IvMT) ^ 2 := by
  have h := two_integral_vConv_vMT_fact
  have hcl : (∫ r in (0 : ℝ)..1, vConv vMT r) = ∫ r in (0 : ℝ)..1, vConvMTcl r := by
    apply intervalIntegral.integral_congr
    intro r hr
    exact vConvMT_closed_fact r (by simpa [uIcc_of_le (by norm_num : (0 : ℝ) ≤ 1)] using hr)
  rwa [hcl] at h

/-- M3-open-A(v): the two-sided jWin(D1,1,vMT) bound from the D₁-certificate. -/
theorem jWin_D1_one_vMT_sandwich_fact :
    J1MT ≤ jWin D1 1 vMT ∧ jWin D1 1 vMT ≤ J1MT + eps9 * (IvMT) ^ 2 := by
  constructor
  · -- lower: J1MT = jWin(D1trunc 9,1,vMT) ≤ jWin(D1,1,vMT)
    have h := jWin_one_le_of_le (D := D1trunc 9) (E := D1) (w := vConvMTcl)
      (continuous_D1trunc 9).continuousOn (continuousOn_D1 _)
      (by unfold vConvMTcl; fun_prop) (fun r hr => vConvMTcl_nonneg hr)
      (e := 0) (fun r hr => by linarith [D1trunc_le_D1 9 hr.1])
      (fun r hr => vConvMT_closed_fact r hr)
    rw [jWin_trunc9_vMT] at h
    simpa using h
  · -- upper: jWin(D1,1,vMT) ≤ J1MT + eps9*(IvMT)²
    have h := jWin_one_le_of_le (D := D1) (E := D1trunc 9) (w := vConvMTcl)
      (continuousOn_D1 _) (continuous_D1trunc 9).continuousOn
      (by unfold vConvMTcl; fun_prop) (fun r hr => vConvMTcl_nonneg hr)
      (e := eps9) (fun r hr => D1_le_D1trunc9_add hr.1 hr.2)
      (fun r hr => vConvMT_closed_fact r hr)
    rw [jWin_trunc9_vMT] at h
    rw [two_integral_vConvMTcl] at h
    simpa using h

/-- **unconditional AtOne sandwich for v_MT:** all M3-open-A hypotheses are now machine-proved,
    so κ₁(1,vMT) ∈ [κ₉, κ₉ + ε₉]. -/
theorem kappaXi_one_vMT_mem_fact :
    kappaXi 1 vMT ∈ Icc kappaXiOne_MT (kappaXiOne_MT + eps9) :=
  kappaXi_one_vMT_mem integral_vMT_forms_fact jWin_D1_one_vMT_sandwich_fact IvMT_pos_fact

/-- **unconditional sharp H_{ξ′} range:** H_xip = 2 − κ₁(1,vMT) ∈ [2 − (κ₉ + ε₉), 2 − κ₉]. -/
theorem H_xip_vMT_mem_fact :
    H_xip ∈ Icc (2 - (kappaXiOne_MT + eps9)) (2 - kappaXiOne_MT) :=
  H_xip_vMT_mem integral_vMT_forms_fact jWin_D1_one_vMT_sandwich_fact IvMT_pos_fact

end XiPrime
end Zeta23

end
