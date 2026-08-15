/-
Record9.KernelLimit — T1c item 3: the kernel-limit lemma (KL), Stage C formalizer pass.

Part of the Stage C formalizer pass for the C₉ = 0.67306647267… world-record theorem. This
module formalizes the kernel-limit lemma from
`runs/rigorous-open-math-research/R-20260816T040000Z-kernellimit-b9e1/` (candidate_proof.md
Eq. 1–4, problem_contract.md §3). The analysis-level proof is complete; this module
machine-formalizes it. NO sorry/admit/axiom appear anywhere in this module.

Obligations carried here:
  M1 — KL2 (kernel identity):  `K_of x / K0 = kMT x` for all x ∈ ℝ, where
        K_of x := ∫_{-1/2}^{1/2} cos(√2 t)·cos(2π x t) dt,
        K0    := ∫_{-1/2}^{1/2} cos(√2 t) dt = √2·sin(1/√2) = sincMT(1/√2),
        and kMT is Record9.Chain9's normalized Montgomery–Taylor kernel
        [sinc((√2)⁻¹−πx) + sinc((√2)⁻¹+πx)] / (2·√2·sin((√2)⁻¹)).
        Fully machine-checked via product-to-sum + the exact antiderivative
        ∫_{−1/2}^{1/2} cos(c t) dt = sincMT(c/2).
  M2 — KL1 (uniform closeness):  |F_L(x) − K_of(x)| ≤ 2w/L for all x, where
        F_L(x) := ∫_{-1/2}^{1/2} cos(√2 t)·ϱ((1/2−|t|)·L/w)²·cos(2π x t) dt.
        Proof via the ramp-is-one-on-core lemma `ramp_is_one_on_core` (machine-checked from
        the TaperProfile structure) + a two-band width bound.
  M3 — KL3 (ratio): from KL1 + KL2, the ratio statement in ε-form: for bounded normalized
        separations the overlap ratio ⟨v_γ,v_γ′⟩/⟨v_γ,v_γ⟩ is within O(w/L) of kMT(x).

Fidelity notes:
  • The definitions faithfully mirror the analysis: integrals via `intervalIntegral`
    ∫ t in (-(1:ℝ)/2)..(1/2), …, the MT window via the TaperProfile `ϱ` (Zeta23.Defs),
    sinc via the guarded `if z = 0 then 1 else Real.sin z / z` (Chain9.sincMT).
  • `K0 > 0` (so the ratio is defined) uses `Real.sin_pos_of_pos_of_lt_pi` with
    (√2)⁻¹ ∈ (0,π), mirroring Chain9.kMT_den_pos.
  • Statement freeze vs the analysis artifacts: the exact statements K/K0 = kMT, |F_L−K|≤2w/L
    are preserved (no weakening). M2's bound is the analysis's `2w/L`; the two-band width
    argument is formalized directly.
-/
import Record9.Chain9

noncomputable section

open scoped BigOperators
open Real intervalIntegral

namespace Zeta23
namespace ThmD

/-! ## M1 — KL2 (kernel identity): K_of(x)/K0 = kMT(x) -/

/-- the kernel numerator: K(x) = ∫_{-1/2}^{1/2} cos(√2 t)·cos(2π x t) dt. -/
def K_of (x : ℝ) : ℝ :=
  ∫ t in (-(1:ℝ)/2)..(1/2), Real.cos (Real.sqrt 2 * t) * Real.cos (2 * Real.pi * x * t)

/-- the normalization constant: K0 = ∫_{-1/2}^{1/2} cos(√2 t) dt. -/
def K0 : ℝ := ∫ t in (-(1:ℝ)/2)..(1/2), Real.cos (Real.sqrt 2 * t)

/-- ∫_{-1/2}^{1/2} cos(c·t) dt = 2·sin(c/2)/c, for c ≠ 0 (via substitution + integral_cos). -/
private lemma integral_cos_mul_ne_zero (c : ℝ) (hc : c ≠ 0) :
    ∫ t in (-(1:ℝ)/2)..(1/2), Real.cos (c * t) = 2 * Real.sin (c / 2) / c := by
  have hs2 : (0:ℝ) < Real.sqrt 2 := by positivity
  rw [intervalIntegral.integral_comp_mul_left Real.cos hc, integral_cos, smul_eq_mul]
  -- bounds become c·(-1/2), c·(1/2)
  have hb : c * (1/2) = c / 2 := by ring
  have hb' : c * (-(1:ℝ)/2) = -(c / 2) := by ring
  rw [hb, hb', Real.sin_neg]
  ring

/-- ∫_{-1/2}^{1/2} cos(c·t) dt = sincMT(c/2), total on ℝ (the sinc guard handles c = 0). -/
lemma integral_cos_mul_self (c : ℝ) :
    ∫ t in (-(1:ℝ)/2)..(1/2), Real.cos (c * t) = sincMT (c / 2) := by
  by_cases hc : c = 0
  · -- c = 0: integrand identically 1, integral = 1 = sincMT(0) by the guard.
    have hc2eq : c / 2 = 0 := by simp [hc]
    have hk : ∫ t in (-(1:ℝ)/2)..(1/2), Real.cos (c * t)
        = ∫ t in (-(1:ℝ)/2)..(1/2), (1 : ℝ) := by
      apply intervalIntegral.integral_congr
      intro _ _
      simp [hc]
    have hconst : ∫ t in (-(1:ℝ)/2)..(1/2), (1 : ℝ) = 1 := by
      rw [intervalIntegral.integral_const]
      norm_num
    rw [hk, hconst, sincMT]
    simp [hc2eq]
  · have hc2 : c / 2 ≠ 0 := div_ne_zero hc (by norm_num : (2:ℝ) ≠ 0)
    have hsinc : sincMT (c / 2) = Real.sin (c / 2) / (c / 2) := by
      rw [sincMT]
      exact if_neg hc2
    rw [hsinc]
    have h := integral_cos_mul_ne_zero c hc
    -- 2·sin(c/2)/c = sin(c/2)/(c/2)
    calc
      ∫ t in (-(1:ℝ)/2)..(1/2), Real.cos (c * t) = 2 * Real.sin (c / 2) / c := h
      _ = Real.sin (c / 2) / (c / 2) := by
        field_simp [hc2, hc]

/-- √2/2 = (√2)⁻¹ (so the sinc argument agrees with the kernel's (√2)⁻¹ − πx). -/
private lemma sqrt2_div_two_eq_inv : (Real.sqrt 2 : ℝ) / 2 = (Real.sqrt 2)⁻¹ := by
  have hs2ne : (Real.sqrt 2 : ℝ) ≠ 0 := by positivity
  have hsq : (Real.sqrt 2 : ℝ) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  field_simp [hs2ne]
  ring_nf
  exact hsq

/-- the normalization constant: K0 = ∫ cos(√2 t) = sincMT(1/√2) = √2·sin(1/√2). -/
lemma K0_eq_sincMT : K0 = sincMT ((Real.sqrt 2)⁻¹) := by
  unfold K0
  rw [integral_cos_mul_self (Real.sqrt 2)]
  rw [sqrt2_div_two_eq_inv]

/-- K0 = √2·sin(1/√2). -/
lemma K0_eq_sqrt2_sin : K0 = Real.sqrt 2 * Real.sin ((Real.sqrt 2)⁻¹) := by
  have hs2 : (0:ℝ) < Real.sqrt 2 := by positivity
  have hinv : (Real.sqrt 2 : ℝ)⁻¹ ≠ 0 := by positivity
  rw [K0_eq_sincMT]
  rw [sincMT]
  rw [if_neg hinv]
  field_simp [hs2.ne']

/-- K0 > 0 (the ratio K_of/K0 is therefore well-defined everywhere). -/
lemma K0_pos : 0 < K0 := by
  rw [K0_eq_sqrt2_sin]
  have hsqrt_pos : (0 : ℝ) < Real.sqrt 2 := by positivity
  have hinv_pos : (0 : ℝ) < (Real.sqrt 2)⁻¹ := by positivity
  have hinv_le_one : (Real.sqrt 2)⁻¹ ≤ (1 : ℝ) := by
    rw [inv_le_one₀ hsqrt_pos]
    have hsqrt_ge_one : (1 : ℝ) ≤ Real.sqrt 2 := by
      rw [← Real.sqrt_one]
      exact Real.sqrt_le_sqrt (by norm_num : (1 : ℝ) ≤ (2 : ℝ))
    exact hsqrt_ge_one
  have h1_lt_pi : (1 : ℝ) < Real.pi := by
    linarith [Real.pi_gt_three]
  have hsin : 0 < Real.sin ((Real.sqrt 2)⁻¹) :=
    Real.sin_pos_of_pos_of_lt_pi hinv_pos (lt_of_le_of_lt hinv_le_one h1_lt_pi)
  exact mul_pos hsqrt_pos hsin

/-- product-to-sum: cos(√2 t)·cos(2πxt) = ½[cos((√2−2πx)t) + cos((√2+2πx)t)]. -/
private lemma K_of_integrand (x t : ℝ) :
    Real.cos (Real.sqrt 2 * t) * Real.cos (2 * Real.pi * x * t)
      = (Real.cos ((Real.sqrt 2 - 2 * Real.pi * x) * t)
        + Real.cos ((Real.sqrt 2 + 2 * Real.pi * x) * t)) / 2 := by
  have h := Real.two_mul_cos_mul_cos (Real.sqrt 2 * t) (2 * Real.pi * x * t)
  have ha : Real.sqrt 2 * t - 2 * Real.pi * x * t = (Real.sqrt 2 - 2 * Real.pi * x) * t := by ring
  have hb : Real.sqrt 2 * t + 2 * Real.pi * x * t = (Real.sqrt 2 + 2 * Real.pi * x) * t := by ring
  rw [ha, hb] at h
  linarith

/-- the angle normalization: (√2 − 2πx)/2 = (√2)⁻¹ − πx  and  (√2 + 2πx)/2 = (√2)⁻¹ + πx. -/
private lemma half_angle_sub (x : ℝ) : (Real.sqrt 2 - 2 * Real.pi * x) / 2 = (Real.sqrt 2)⁻¹ - Real.pi * x := by
  rw [sub_div]
  rw [sqrt2_div_two_eq_inv]
  ring
private lemma half_angle_add (x : ℝ) : (Real.sqrt 2 + 2 * Real.pi * x) / 2 = (Real.sqrt 2)⁻¹ + Real.pi * x := by
  rw [add_div]
  rw [sqrt2_div_two_eq_inv]
  ring

/-- **KL2 numerator identity**: K(x) = ½·[sinc((√2)⁻¹ − πx) + sinc((√2)⁻¹ + πx)].
    Equivalently K_of x = ½·(sincMT(1/√2−πx) + sincMT(1/√2+πx)). -/
lemma K_of_closed (x : ℝ) :
    K_of x = (1 / 2) * (sincMT ((Real.sqrt 2)⁻¹ - Real.pi * x)
        + sincMT ((Real.sqrt 2)⁻¹ + Real.pi * x)) := by
  have h1 := integral_cos_mul_self (Real.sqrt 2 - 2 * Real.pi * x)
  have h2 := integral_cos_mul_self (Real.sqrt 2 + 2 * Real.pi * x)
  rw [half_angle_sub x] at h1
  rw [half_angle_add x] at h2
  have hsum :
      ∫ t in (-(1:ℝ)/2)..(1/2),
          (Real.cos ((Real.sqrt 2 - 2 * Real.pi * x) * t)
            + Real.cos ((Real.sqrt 2 + 2 * Real.pi * x) * t)) / 2
        = (sincMT ((Real.sqrt 2)⁻¹ - Real.pi * x)
            + sincMT ((Real.sqrt 2)⁻¹ + Real.pi * x)) / 2 := by
    -- ∫(cosA + cosB)/2 = (∫cosA + ∫cosB)/2, then use h1,h2
    rw [intervalIntegral.integral_div]
    rw [intervalIntegral.integral_add]
    · rw [h1, h2]
    · exact Continuous.intervalIntegrable
        (Real.continuous_cos.comp (continuous_const.mul continuous_id)) _ _
    · exact Continuous.intervalIntegrable
        (Real.continuous_cos.comp (continuous_const.mul continuous_id)) _ _
  unfold K_of
  calc
    ∫ t in (-(1:ℝ)/2)..(1/2), Real.cos (Real.sqrt 2 * t) * Real.cos (2 * Real.pi * x * t)
        = ∫ t in (-(1:ℝ)/2)..(1/2),
            ((Real.cos ((Real.sqrt 2 - 2 * Real.pi * x) * t)
              + Real.cos ((Real.sqrt 2 + 2 * Real.pi * x) * t)) / 2) := by
      apply intervalIntegral.integral_congr
      intro t _
      exact K_of_integrand x t
    _ = (sincMT ((Real.sqrt 2)⁻¹ - Real.pi * x)
        + sincMT ((Real.sqrt 2)⁻¹ + Real.pi * x)) / 2 := hsum
    _ = 1 / 2 * (sincMT ((Real.sqrt 2)⁻¹ - Real.pi * x)
        + sincMT ((Real.sqrt 2)⁻¹ + Real.pi * x)) := by
      ring

/-- `w/L ≤ 1/2`, derived from `8w ≤ L` and `0<L` (so the two boundary bands are properly
    ordered and `1/2 − w/L ≥ 0`). -/
private lemma wL_le_half {L w : ℝ} (hL : 0 < L) (hw : 0 < w) (hwL : 8 * w ≤ L) : w / L ≤ 1 / 2 := by
  have htwo : 2 * w ≤ L := by nlinarith [hw, hwL]
  have hlinv : 0 ≤ L⁻¹ := le_of_lt (inv_pos.mpr hL)
  have hprod : (2 * w) / L ≤ (1 : ℝ) := by
    calc
      (2 * w) / L = (2 * w) * L⁻¹ := rfl
      _ ≤ L * L⁻¹ := mul_le_mul_of_nonneg_right htwo hlinv
      _ = 1 := by field_simp [hL.ne']
  have h2 : 2 * (w / L) = (2 * w) / L := by field_simp [hL.ne']
  have hmul : 2 * (w / L) ≤ (1 : ℝ) := by
    rw [h2]
    exact hprod
  rw [le_div_iff₀ (by norm_num : (0 : ℝ) < 2)]
  rw [mul_comm]
  exact hmul

/-- **M2 auxiliary** — the ramp-is-one-on-core lemma: wherever `|t| ≤ 1/2 − w/L`, the
    MT ramp factor ϱ((1/2−|t|)·L/w) equals 1. (This is the analytical heart of the measure-
    2w/L argument; it uses `TaperProfile.eq_one`.) -/
lemma ramp_is_one_on_core (hϱ : TaperProfile ϱ) (hL : 0 < L) (hw : 0 < w) {t : ℝ}
    (hcore : |t| ≤ 1 / 2 - w / L) :
    ϱ ((1 / 2 - |t|) * L / w) = 1 := by
  apply hϱ.eq_one
  -- (1/2 − |t|)·L/w ≥ 1
  have hm : w / L ≤ 1 / 2 - |t| := by
    linarith [hcore]
  have hLw : 0 ≤ L / w := le_of_lt (div_pos hL hw)
  calc
    (1 : ℝ) = (w / L) * (L / w) := by field_simp [hL.ne', hw.ne']
    _ ≤ (1 / 2 - |t|) * (L / w) := mul_le_mul_of_nonneg_right hm hLw
    _ = (1 / 2 - |t|) * L / w := by ring

/-- the finite-window overlap numerator (normalized by window length):
    F_L(x) = ∫_{-1/2}^{1/2} cos(√2 t)·ϱ((1/2−|t|)·L/w)²·cos(2π x t) dt. -/
def F_L (ϱ : ℝ → ℝ) (L w : ℝ) (x : ℝ) : ℝ :=
  ∫ t in (-(1:ℝ)/2)..(1/2),
    Real.cos (Real.sqrt 2 * t) * (ϱ ((1 / 2 - |t|) * L / w)) ^ 2 * Real.cos (2 * Real.pi * x * t)

/-- the difference integrand: D(t) = cos(√2 t)·cos(2π x t)·(ϱ((1/2−|t|)L/w)² − 1). -/
def KL_D (ϱ : ℝ → ℝ) (L w : ℝ) (x : ℝ) (t : ℝ) : ℝ :=
  Real.cos (Real.sqrt 2 * t) * Real.cos (2 * Real.pi * x * t)
    * ((ϱ ((1 / 2 - |t|) * L / w)) ^ 2 - 1)

/-- the difference integrand is continuous (hence interval-integrable on every interval). -/
lemma KL_D_continuous (hϱ : TaperProfile ϱ) (L w x : ℝ) : Continuous (KL_D ϱ L w x) := by
  have hcos1 : Continuous (fun t : ℝ => Real.cos (Real.sqrt 2 * t)) := by fun_prop
  have hcos2 : Continuous (fun t : ℝ => Real.cos (2 * Real.pi * x * t)) := by fun_prop
  have harg : Continuous (fun t : ℝ => (1 / 2 - |t|) * L / w) := by fun_prop
  have hrho : Continuous (fun t : ℝ => ϱ ((1 / 2 - |t|) * L / w)) := hϱ.continuous.comp harg
  have hrhopow : Continuous (fun t : ℝ => (ϱ ((1 / 2 - |t|) * L / w)) ^ 2) := hrho.pow 2
  have hdiff : Continuous (fun t : ℝ => (ϱ ((1 / 2 - |t|) * L / w)) ^ 2 - 1) :=
    hrhopow.sub continuous_const
  unfold KL_D
  exact (hcos1.mul hcos2).mul hdiff

/-- the difference integrand is bounded by 1 in absolute value on every interval
    (|cos| ≤ 1, |ϱ| ≤ 1 from the TaperProfile structure). -/
lemma KL_D_abs_le_one (hϱ : TaperProfile ϱ) (L w x t : ℝ) : |KL_D ϱ L w x t| ≤ 1 := by
  have hc1 : |Real.cos (Real.sqrt 2 * t)| ≤ 1 := abs_cos_le_one _
  have hc2 : |Real.cos (2 * Real.pi * x * t)| ≤ 1 := abs_cos_le_one _
  let y : ℝ := (1 / 2 - |t|) * L / w
  have hrho : |(ϱ y) ^ 2 - 1| ≤ 1 := by
    have h1 : ϱ y ≤ 1 := hϱ.le_one _
    have hy0 : 0 ≤ ϱ y := hϱ.nonneg _
    have hs0 : 0 ≤ (ϱ y) ^ 2 := sq_nonneg _
    have hs1 : (ϱ y) ^ 2 ≤ 1 := by nlinarith [hy0, h1]
    calc
      |(ϱ y) ^ 2 - 1| = 1 - (ϱ y) ^ 2 := by
        rw [abs_of_nonpos (sub_nonpos.mpr hs1)]
        ring
      _ ≤ 1 := by linarith
  unfold KL_D
  calc
    |Real.cos (Real.sqrt 2 * t) * Real.cos (2 * Real.pi * x * t) * ((ϱ y) ^ 2 - 1)|
        = |Real.cos (Real.sqrt 2 * t)| * |Real.cos (2 * Real.pi * x * t)|
            * |(ϱ y) ^ 2 - 1| := by
      rw [abs_mul, abs_mul]
    _ ≤ 1 * 1 * 1 := by
      have hboth : |Real.cos (Real.sqrt 2 * t)| * |Real.cos (2 * Real.pi * x * t)| ≤ 1 * 1 := by
        exact mul_le_mul hc1 hc2 (abs_nonneg _) (by norm_num)
      have hall : (|Real.cos (Real.sqrt 2 * t)| * |Real.cos (2 * Real.pi * x * t)|)
            * |(ϱ y) ^ 2 - 1| ≤ (1 * 1) * 1 := by
        exact mul_le_mul hboth hrho (abs_nonneg _) (by norm_num)
      simpa using hall
    _ = 1 := by norm_num

/-! ## M2 — KL1 (uniform closeness): |F_L(x) − K(x)| ≤ 2w/L -/

/-- the difference integrand vanishes on the central bulk `|t| ≤ 1/2 − w/L`
    (where the ramp is 1, so ρ² − 1 = 0). -/
lemma KL_D_eq_zero_on_core (hϱ : TaperProfile ϱ) (hL : 0 < L) (hw : 0 < w)
    (x t : ℝ) (hcore : |t| ≤ 1 / 2 - w / L) : KL_D ϱ L w x t = 0 := by
  have hr := ramp_is_one_on_core hϱ hL hw hcore
  unfold KL_D
  rw [hr]
  ring

/-- the three band split points A ≤ B ≤ C ≤ D, ordered under `8w ≤ L`. -/
private lemma band_order (hL : 0 < L) (hw : 0 < w) (hwL : 8 * w ≤ L) :
    -(1:ℝ)/2 ≤ -(1:ℝ)/2 + w / L ∧
      -(1:ℝ)/2 + w / L ≤ 1 / 2 - w / L ∧
        1 / 2 - w / L ≤ 1 / 2 := by
  have hwLge : 0 ≤ w / L := le_of_lt (div_pos hw hL)
  have hwLle : w / L ≤ 1 / 2 := wL_le_half hL hw hwL
  constructor
  · linarith
  constructor
  · linarith
  · linarith

/-- bound on the left boundary band [−1/2, −1/2 + w/L]:
    |∫_{−1/2}^{−1/2+w/L} D| ≤ w/L. -/
lemma left_band_bound (hϱ : TaperProfile ϱ) (hL : 0 < L) (hw : 0 < w) (_hwL : 8 * w ≤ L)
    (x : ℝ) (b : ℝ) (hb : b = -(1:ℝ)/2 + w / L) :
    |∫ t in (-(1:ℝ)/2)..b, KL_D ϱ L w x t| ≤ w / L := by
  have hbnd : ∀ t : ℝ, |KL_D ϱ L w x t| ≤ 1 := KL_D_abs_le_one hϱ (L := L) (w := w) (x := x)
  rw [hb]
  have hnorm := intervalIntegral.norm_integral_le_of_norm_le_const
    (f := KL_D ϱ L w x) (a := -(1:ℝ)/2) (b := -(1:ℝ)/2 + w / L) (C := 1)
    (by intro t ht; exact hbnd t)
  rw [Real.norm_eq_abs] at hnorm
  -- 1 * |w/L| = w/L
  have hleft : (1 : ℝ) * |(-(1:ℝ)/2 + w / L) - (-(1:ℝ)/2)| = w / L := by
    have hsub : (-(1:ℝ)/2 + w / L) - (-(1:ℝ)/2) = w / L := by ring
    have hwL : 0 ≤ w / L := le_of_lt (div_pos hw hL)
    rw [hsub, abs_of_nonneg hwL]
    ring
  rw [hleft] at hnorm
  exact hnorm

/-- bound on the right boundary band [1/2 − w/L, 1/2]:
    |∫_{1/2−w/L}^{1/2} D| ≤ w/L. -/
lemma right_band_bound (hϱ : TaperProfile ϱ) (hL : 0 < L) (hw : 0 < w) (_hwL : 8 * w ≤ L)
    (x : ℝ) (a : ℝ) (ha : a = 1 / 2 - w / L) :
    |∫ t in a..(1/2), KL_D ϱ L w x t| ≤ w / L := by
  have hbnd : ∀ t : ℝ, |KL_D ϱ L w x t| ≤ 1 := KL_D_abs_le_one hϱ (L := L) (w := w) (x := x)
  rw [ha]
  have hnorm := intervalIntegral.norm_integral_le_of_norm_le_const
    (f := KL_D ϱ L w x) (a := 1 / 2 - w / L) (b := (1:ℝ)/2) (C := 1)
    (by intro t ht; exact hbnd t)
  rw [Real.norm_eq_abs] at hnorm
  have hright : (1 : ℝ) * |(1 / 2) - (1 / 2 - w / L)| = w / L := by
    have hsub : (1 / 2) - (1 / 2 - w / L) = w / L := by ring
    have hwL : 0 ≤ w / L := le_of_lt (div_pos hw hL)
    rw [hsub, abs_of_nonneg hwL]
    ring
  rw [hright] at hnorm
  exact hnorm

/-- the middle band [−1/2 + w/L, 1/2 − w/L] (the core): the integrand is identically 0
    there, so its integral is 0 and |∫| = 0 ≤ 0. -/
lemma middle_band_bound (hϱ : TaperProfile ϱ) (hL : 0 < L) (hw : 0 < w) (hwL : 8 * w ≤ L)
    (x : ℝ) :
    |∫ t in (-(1:ℝ)/2 + w / L)..(1 / 2 - w / L), KL_D ϱ L w x t| ≤ 0 := by
  have hmid : ∀ t : ℝ, t ∈ Set.Icc (-(1:ℝ)/2 + w / L) (1 / 2 - w / L) →
      KL_D ϱ L w x t = 0 := by
    intro t ht
    apply KL_D_eq_zero_on_core hϱ hL hw x t
    have htle : t ≤ 1 / 2 - w / L := ht.2
    have htB : -(1:ℝ)/2 + w / L ≤ t := ht.1
    have hneg : -(1 / 2 - w / L) = -(1:ℝ)/2 + w / L := by ring
    rw [abs_le]
    constructor
    · rw [hneg]
      exact htB
    · exact htle
  have hinteg : ∫ t in (-(1:ℝ)/2 + w / L)..(1 / 2 - w / L), KL_D ϱ L w x t = 0 := by
    have hBC : (-(1:ℝ)/2 + w / L) ≤ 1 / 2 - w / L := (band_order hL hw hwL).2.1
    have hcong : ∫ t in (-(1:ℝ)/2 + w / L)..(1 / 2 - w / L), KL_D ϱ L w x t
        = ∫ t in (-(1:ℝ)/2 + w / L)..(1 / 2 - w / L), (0 : ℝ) := by
      apply intervalIntegral.integral_congr (a := -(1:ℝ)/2 + w / L) (b := 1 / 2 - w / L)
      intro t ht
      -- ht : t ∈ Set.uIcc B C = Icc (min B C) (max B C) ; with B ≤ C this is Icc B C
      have hu : t ∈ Set.Icc (-(1:ℝ)/2 + w / L) (1 / 2 - w / L) := by
        have hmin : min (-(1:ℝ)/2 + w / L) (1 / 2 - w / L) = (-(1:ℝ)/2 + w / L) :=
          min_eq_left hBC
        have hmax : max (-(1:ℝ)/2 + w / L) (1 / 2 - w / L) = (1 / 2 - w / L) :=
          max_eq_right hBC
        have h : t ∈ Set.Icc (min (-(1:ℝ)/2 + w / L) (1 / 2 - w / L))
            (max (-(1:ℝ)/2 + w / L) (1 / 2 - w / L)) := by
          simpa [Set.uIcc] using ht
        rw [hmin, hmax] at h
        exact h
      exact hmid t hu
    rw [hcong]
    simp
  rw [hinteg]
  simp

/-- the three band split points, as abbreviations to keep KL1 readable. -/
private abbrev BLeft (w L : ℝ) : ℝ := -(1:ℝ)/2 + w / L
private abbrev BMid  (w L : ℝ) : ℝ := 1 / 2 - w / L

/-- **M2 — KL1 (uniform closeness)**: for every x ∈ ℝ,
    |F_L(x) − K(x)| ≤ 2w/L.
    Proof: F_L − K = ∫_{-1/2}^{1/2} D where D = cos·cos·(ϱ(...)²−1); split the interval at
    −1/2 + w/L and 1/2 − w/L into three bands; the central band contributes 0 (ramp = 1
    there) and each boundary band contributes ≤ w/L in absolute value. -/
theorem KL1 (hϱ : TaperProfile ϱ) (hL : 0 < L) (hw : 0 < w) (hwL : 8 * w ≤ L)
    (x : ℝ) : |F_L ϱ L w x - K_of x| ≤ 2 * (w / L) := by
  let A : ℝ := -(1:ℝ)/2
  let B : ℝ := BLeft w L
  let C : ℝ := BMid w L
  let D : ℝ := 1/2
  -- F_L − K = ∫_{−1/2}^{1/2} D
  have hdiff : F_L ϱ L w x - K_of x = ∫ t in A..D, KL_D ϱ L w x t := by
    unfold F_L K_of at *
    rw [← intervalIntegral.integral_sub]
    · apply intervalIntegral.integral_congr
      intro t _
      unfold KL_D
      ring
    · -- IntervalIntegrable of the F_L-integrand
      have harg : Continuous (fun t : ℝ => (1 / 2 - |t|) * L / w) := by fun_prop
      have hrho : Continuous (fun t : ℝ => ϱ ((1 / 2 - |t|) * L / w)) := hϱ.continuous.comp harg
      have hrhopow : Continuous (fun t : ℝ => (ϱ ((1 / 2 - |t|) * L / w)) ^ 2) := hrho.pow 2
      have hcos1 : Continuous (fun t : ℝ => Real.cos (Real.sqrt 2 * t)) := by fun_prop
      have hcos2 : Continuous (fun t : ℝ => Real.cos (2 * Real.pi * x * t)) := by fun_prop
      exact (hcos1.mul hrhopow).mul hcos2 |>.intervalIntegrable _ _
    · -- IntervalIntegrable of the K_of-integrand
      have hcos1 : Continuous (fun t : ℝ => Real.cos (Real.sqrt 2 * t)) := by fun_prop
      have hcos2 : Continuous (fun t : ℝ => Real.cos (2 * Real.pi * x * t)) := by fun_prop
      exact (hcos1.mul hcos2).intervalIntegrable _ _
  -- IntervalIntegrable for KL_D on every band (KL_D is continuous).
  let hint : ∀ a b : ℝ, IntervalIntegrable (KL_D ϱ L w x) MeasureTheory.volume a b :=
    fun a b => (KL_D_continuous hϱ L w x).intervalIntegrable a b
  -- the three-way split: ∫_A^D = ∫_A^B + ∫_B^C + ∫_C^D
  have hA : A ≤ B := by simp [A, B, BLeft]; exact le_of_lt (div_pos hw hL)
  have hBC : B ≤ C := by
    simp [B, C, BLeft, BMid]
    have : w / L ≤ 1 / 2 := wL_le_half hL hw hwL
    linarith
  have hCD : C ≤ D := by simp [C, D, BMid]; exact le_of_lt (div_pos hw hL)
  have hBD : B ≤ D := le_trans hBC hCD
  have hsplitBD :
      ∫ t in B..D, KL_D ϱ L w x t = (∫ t in B..C, KL_D ϱ L w x t) + ∫ t in C..D, KL_D ϱ L w x t :=
    (intervalIntegral.integral_add_adjacent_intervals (f := KL_D ϱ L w x) (hint B C) (hint C D)).symm
  have hsplitAD :
      ∫ t in A..D, KL_D ϱ L w x t = (∫ t in A..B, KL_D ϱ L w x t) + ∫ t in B..D, KL_D ϱ L w x t :=
    (intervalIntegral.integral_add_adjacent_intervals (f := KL_D ϱ L w x) (hint A B) (hint B D)).symm
  -- triangle inequality
  have htri : |∫ t in A..D, KL_D ϱ L w x t|
      ≤ |∫ t in A..B, KL_D ϱ L w x t| + |∫ t in B..C, KL_D ϱ L w x t|
        + |∫ t in C..D, KL_D ϱ L w x t| := by
    have h1 : |∫ t in A..D, KL_D ϱ L w x t|
        ≤ |∫ t in A..B, KL_D ϱ L w x t| + |∫ t in B..D, KL_D ϱ L w x t| := by
      rw [hsplitAD]
      exact abs_add_le _ _
    have h2 : |∫ t in B..D, KL_D ϱ L w x t|
        ≤ |∫ t in B..C, KL_D ϱ L w x t| + |∫ t in C..D, KL_D ϱ L w x t| := by
      rw [hsplitBD]
      exact abs_add_le _ _
    nlinarith [h1, h2]
  -- combine with the three band bounds
  have hleft : |∫ t in A..B, KL_D ϱ L w x t| ≤ w / L := by
    simpa [A, B, BLeft] using left_band_bound hϱ hL hw hwL x B (by simp [B, BLeft])
  have hmid0 : |∫ t in B..C, KL_D ϱ L w x t| ≤ 0 := by
    simpa [B, C, BLeft, BMid] using middle_band_bound hϱ hL hw hwL x
  have hright : |∫ t in C..D, KL_D ϱ L w x t| ≤ w / L := by
    simpa [C, D, BMid] using right_band_bound hϱ hL hw hwL x C (by simp [C, BMid])
  have hsum : |∫ t in A..B, KL_D ϱ L w x t| + |∫ t in B..C, KL_D ϱ L w x t|
        + |∫ t in C..D, KL_D ϱ L w x t| ≤ 2 * (w / L) := by
    nlinarith [hleft, hmid0, hright]
  -- wrap up
  rw [hdiff]
  exact le_trans htri (le_trans hsum (by linarith))

/-- **M1 — KL2 (kernel identity)**: K(x)/K(0) = kMT(x) for all x ∈ ℝ, where kMT is the
    normalized Montgomery–Taylor kernel of `Record9.Chain9`, K0 = K(0) > 0, and K(x) is the
    Fourier overlap integral. This is candidate_proof.md (Eq. 4). -/
theorem KL2 (x : ℝ) : K_of x / K0 = kMT x := by
  have hK : K_of x = (1 / 2) * (sincMT ((Real.sqrt 2)⁻¹ - Real.pi * x)
        + sincMT ((Real.sqrt 2)⁻¹ + Real.pi * x)) := K_of_closed x
  rw [hK, kMT, K0_eq_sqrt2_sin]
  field_simp [K0_pos.ne']

/-! ## M3 — KL3 (ratio): ⟨v_γ,v_γ′⟩/⟨v_γ,v_γ⟩ = kMT(x) + O(w/L) -/

/-- the normalized finite-window overlap ratio ⟨v_γ,v_γ′⟩/⟨v_γ,v_γ⟩ = F_L(x)/F_L(0). -/
def KL_ratio (ϱ : ℝ → ℝ) (L w : ℝ) (x : ℝ) : ℝ := F_L ϱ L w x / F_L ϱ L w 0

/-- **KL1 at x = 0**: |F_L(0) − K(0)| ≤ 2w/L. -/
private lemma F_L0_close (hϱ : TaperProfile ϱ) (hL : 0 < L) (hw : 0 < w) (hwL : 8 * w ≤ L) :
    |F_L ϱ L w 0 - K0| ≤ 2 * (w / L) := by
  have h := KL1 hϱ hL hw hwL (0 : ℝ)
  simpa [K_of, K0] using h

/-- **KL3 lower bound**: for `4w ≤ K(0)·L`, the diagonal overlap is positive and bounded
    below by K(0)/2 (so the ratio is well defined and its denominator is away from 0). -/
lemma KL_F_L0_ge_half (hϱ : TaperProfile ϱ) (hL : 0 < L) (hw : 0 < w) (hwL : 8 * w ≤ L)
    (hsep : 4 * w ≤ K0 * L) : K0 / 2 ≤ F_L ϱ L w 0 := by
  have hc : |F_L ϱ L w 0 - K0| ≤ 2 * (w / L) := F_L0_close hϱ hL hw hwL
  -- 4w ≤ K0·L ⟹ 4·(w/L) ≤ K0 ⟹ 2·(w/L) ≤ K0/2
  have h4 : (4 : ℝ) * (w / L) ≤ K0 := by
    have hlinv : 0 ≤ L⁻¹ := le_of_lt (inv_pos.mpr hL)
    have hmul : (4 * w) * L⁻¹ ≤ (K0 * L) * L⁻¹ := mul_le_mul_of_nonneg_right hsep hlinv
    have hKinv : (K0 * L) * L⁻¹ = K0 := by field_simp [hL.ne']
    calc
      (4 : ℝ) * (w / L) = (4 * w) * L⁻¹ := by field_simp [hL.ne']
      _ ≤ (K0 * L) * L⁻¹ := hmul
      _ = K0 := hKinv
  have hfall : (2 : ℝ) * (w / L) ≤ K0 / 2 := by nlinarith [h4]
  -- |FL0 − K0| ≤ 2w/L ⟹ FL0 ≥ K0 − 2w/L
  have himp : -(2 * (w / L)) ≤ F_L ϱ L w 0 - K0 := (abs_le.mp hc).1
  have hlower : K0 - 2 * (w / L) ≤ F_L ϱ L w 0 := by nlinarith
  nlinarith [hlower, hfall]

/-- KL3's ratio denominator is positive (hence invertible): F_L(0) > 0 for large L. -/
lemma KL_F_L0_pos (hϱ : TaperProfile ϱ) (hL : 0 < L) (hw : 0 < w) (hwL : 8 * w ≤ L)
    (hsep : 4 * w ≤ K0 * L) : 0 < F_L ϱ L w 0 :=
  lt_of_lt_of_le (div_pos K0_pos (by norm_num : (0 : ℝ) < 2)) (KL_F_L0_ge_half hϱ hL hw hwL hsep)

/-- the perturbation identity: (a/b) − (A/B) = ((a−A)·B − (b−B)·A)/(b·B), for b, B ≠ 0. -/
private lemma div_sub_div (a b A B : ℝ) (hb : b ≠ 0) (hB : B ≠ 0) :
    (a / b - A / B) = ((a - A) * B - (b - B) * A) / (b * B) := by
  field_simp [hb, hB]
  ring

/-- the generic ratio perturbation bound:
    |a/b − A/B| ≤ (|a−A|·|B| + |b−B|·|A|)/(b·B),   for b, B > 0. -/
private lemma div_sub_div_abs_bound (a b A B : ℝ) (hb : 0 < b) (hB : 0 < B) :
    |a / b - A / B| ≤ (|a - A| * |B| + |b - B| * |A|) / (b * B) := by
  have hden : 0 < b * B := mul_pos hb hB
  rw [div_sub_div a b A B hb.ne' hB.ne']
  rw [abs_div]
  rw [abs_of_pos hden]
  have htri : |(a - A) * B - (b - B) * A| ≤ |(a - A) * B| + |(b - B) * A| := by
    have hdef : (a - A) * B - (b - B) * A = (a - A) * B + (-((b - B) * A)) := by ring
    calc
      |(a - A) * B - (b - B) * A| = |(a - A) * B + (-((b - B) * A))| := by rw [hdef]
      _ ≤ |(a - A) * B| + |(b - B) * A| := by
        simpa [abs_neg] using (abs_add_le ((a - A) * B) (-((b - B) * A)))
  have h1 : |(a - A) * B| = |a - A| * |B| := by rw [abs_mul]
  have h2 : |(b - B) * A| = |b - B| * |A| := by rw [abs_mul]
  have hle : |(a - A) * B| + |(b - B) * A| ≤ |a - A| * |B| + |b - B| * |A| := by
    rw [h1, h2]
  have hsum : |(a - A) * B - (b - B) * A| ≤ |a - A| * |B| + |b - B| * |A| :=
    le_trans htri hle
  exact div_le_div_of_nonneg_right hsum (le_of_lt hden)

/-- **M3 — KL3, explicit O(w/L) bound** (the block-energy estimate). For the finite-window
    overlap ratio, uniformly in x:
    |F_L(x)/F_L(0) − kMT(x)| ≤ (2w/L)·(1 + |kMT x|)/F_L(0).
    Combined with the lower bound `F_L(0) ≥ K(0)/2`, this gives O(w/L)×(1+|kMT|) as L→∞. -/
theorem KL3_ratio_bound (hϱ : TaperProfile ϱ) (hL : 0 < L) (hw : 0 < w) (hwL : 8 * w ≤ L)
    (hsep : 4 * w ≤ K0 * L) (x : ℝ) :
    |F_L ϱ L w x / F_L ϱ L w 0 - kMT x|
      ≤ (2 * (w / L)) * (1 + |kMT x|) / F_L ϱ L w 0 := by
  -- a = F_L x, b = F_L 0, A = K(x), B = K0 ; A/B = kMT x (KL2) ; |a−A|,|b−B| ≤ δ = 2w/L (KL1)
  let δ : ℝ := 2 * (w / L)
  have hKL1x : |F_L ϱ L w x - K_of x| ≤ δ := by
    simpa [δ] using KL1 hϱ hL hw hwL x
  have hKL10 : |F_L ϱ L w 0 - K0| ≤ δ := by
    simpa [δ] using F_L0_close hϱ hL hw hwL
  have hbpos : 0 < F_L ϱ L w 0 := KL_F_L0_pos hϱ hL hw hwL hsep
  have hBpos : 0 < K0 := K0_pos
  have hKL2x : K_of x / K0 = kMT x := KL2 x
  -- |a/b − A/B| ≤ (|a−A|·|B| + |b−B|·|A|)/(b·B)
  have hpert := div_sub_div_abs_bound (F_L ϱ L w x) (F_L ϱ L w 0) (K_of x) K0 hbpos hBpos
  -- bound numerator: |a−A|·|B| + |b−B|·|A| ≤ δ·K0 + δ·|K_of x|
  have hK0abs : |K0| = K0 := abs_of_pos hBpos
  have hnumle : |F_L ϱ L w x - K_of x| * |K0| + |F_L ϱ L w 0 - K0| * |K_of x|
      ≤ δ * K0 + δ * |K_of x| := by
    rw [hK0abs]
    have hδ0 : 0 ≤ δ := by unfold δ; positivity
    have hAx : 0 ≤ |K_of x| := abs_nonneg _
    nlinarith [hKL1x, hKL10]
  have hpert' : |F_L ϱ L w x / F_L ϱ L w 0 - K_of x / K0|
      ≤ (δ * K0 + δ * |K_of x|) / (F_L ϱ L w 0 * K0) := by
    exact hpert.trans (div_le_div_of_nonneg_right hnumle (mul_nonneg hbpos.le hBpos.le))
  -- simplify the RHS to δ*(1 + |Kx|/K0)/b = δ*(1+|kMT x|)/b
  have href : (δ * K0 + δ * |K_of x|) / (F_L ϱ L w 0 * K0)
      = δ * (1 + |K_of x| / K0) / F_L ϱ L w 0 := by
    field_simp [hbpos.ne', hBpos.ne']
  -- |Kx|/K0 = |Kx/K0| = |kMT x|
  have hKmT : |K_of x| / K0 = |kMT x| := by
    calc
      |K_of x| / K0 = |K_of x| / |K0| := by rw [hK0abs]
      _ = |K_of x / K0| := by rw [← abs_div]
      _ = |kMT x| := by rw [hKL2x]
  have hfinal : |F_L ϱ L w x / F_L ϱ L w 0 - kMT x|
      ≤ δ * (1 + |kMT x|) / F_L ϱ L w 0 := by
    calc
      |F_L ϱ L w x / F_L ϱ L w 0 - kMT x|
          = |F_L ϱ L w x / F_L ϱ L w 0 - K_of x / K0| := by rw [← hKL2x]
      _ ≤ (δ * K0 + δ * |K_of x|) / (F_L ϱ L w 0 * K0) := hpert'
      _ = δ * (1 + |K_of x| / K0) / F_L ϱ L w 0 := href
      _ = δ * (1 + |kMT x|) / F_L ϱ L w 0 := by rw [hKmT]
  -- final: express δ = 2w/L
  simpa [δ] using hfinal

/-- from the lower bound `F_L(0) ≥ K(0)/2`, the reciprocal is bounded: 1/F_L(0) ≤ 2/K(0). -/
lemma KL_one_div_FL0_le (hϱ : TaperProfile ϱ) (hL : 0 < L) (hw : 0 < w) (hwL : 8 * w ≤ L)
    (hsep : 4 * w ≤ K0 * L) : (1 : ℝ) / F_L ϱ L w 0 ≤ 2 / K0 := by
  have hbv : K0 / 2 ≤ F_L ϱ L w 0 := KL_F_L0_ge_half hϱ hL hw hwL hsep
  have hle : (1 : ℝ) / F_L ϱ L w 0 ≤ 1 / (K0 / 2) :=
    one_div_le_one_div_of_le (div_pos K0_pos (by norm_num : (0 : ℝ) < 2)) hbv
  have hK : 1 / (K0 / 2) = (2 : ℝ) / K0 := by field_simp [K0_pos.ne']
  simpa [hK] using hle

/-- **M3 — KL3, uniform ε-form for bounded separations** (the block-energy estimate that the
    T1 chain consumes). For bounded normalized separations |x| ≤ B, the finite-window overlap
    ratio ⟨v_γ,v_γ′⟩/⟨v_γ,v_γ⟩ = F_L(x)/F_L(0) is within ε of kMT(x) uniformly for L large.
    The boundedness of `1 + |kMT|` on [−B,B] (a compactness fact for the continuous kMT) is
    carried as the explicit hypothesis `hKerBdd` (honest bridge). -/
theorem KL3_eps (hϱ : TaperProfile ϱ) (hw : 0 < w) (B ε : ℝ) (hε : 0 < ε)
    (hKerBdd : ∃ C : ℝ, 0 ≤ C ∧ ∀ x : ℝ, |x| ≤ B → 1 + |kMT x| ≤ C) :
    ∃ L₀ : ℝ, ∀ L ≥ L₀, 0 < L → 8 * w ≤ L → 4 * w ≤ K0 * L →
      ∀ x : ℝ, |x| ≤ B → |KL_ratio ϱ L w x - kMT x| ≤ ε := by
  obtain ⟨C, hC0, hCbdd⟩ := hKerBdd
  -- a pointwise bound: for |x| ≤ B and L large, |ratio − kMT| ≤ (2w/L)·(1+|kMT|)/F_L(0)
  have hpi : ∀ L : ℝ, 0 < L → 8 * w ≤ L → 4 * w ≤ K0 * L → ∀ x : ℝ, |x| ≤ B →
      |KL_ratio ϱ L w x - kMT x| ≤ (2 * (w / L)) * (1 + |kMT x|) / F_L ϱ L w 0 := by
    intro L hL hwL hsep x hx
    simpa [KL_ratio] using KL3_ratio_bound hϱ hL hw hwL hsep x
  -- choose L₀ with (4·w·C/K0)/L ≤ ε  i.e. L ≥ 4·w·C/(K0·ε)
  let L₀ : ℝ := 4 * w * C / (K0 * ε)
  refine ⟨L₀, fun L hLle hLpos hwL hsep x hx => ?_⟩
  have hxbd : 1 + |kMT x| ≤ C := hCbdd x hx
  have hbnd := hpi L hLpos hwL hsep x hx
  -- 1/F_L(0) ≤ 2/K0 and (1+|kMT|) ≤ C, so (2w/L)(1+|kMT|)/F_L0 ≤ (2w/L)·C·(2/K0)
  have hrec : (1 : ℝ) / F_L ϱ L w 0 ≤ 2 / K0 := KL_one_div_FL0_le hϱ hLpos hw hwL hsep
  have hnz : 0 ≤ (1 + |kMT x|) := by positivity
  have hKmT_nonneg : 0 ≤ 2 / K0 := by
    exact div_nonneg (by norm_num : (0 : ℝ) ≤ 2) K0_pos.le
  have hpart : (1 + |kMT x|) / F_L ϱ L w 0 ≤ C * (2 / K0) := by
    -- (1+|kMT|)/b ≤ C·(2/K0) via (1+|kMT|) ≤ C and 1/b ≤ 2/K0, all nonneg
    have h1 : (1 + |kMT x|) / F_L ϱ L w 0 ≤ C / F_L ϱ L w 0 := by
      exact div_le_div_of_nonneg_right hxbd (le_of_lt (KL_F_L0_pos hϱ hLpos hw hwL hsep))
    have h2 : C / F_L ϱ L w 0 ≤ C * (2 / K0) := by
      rw [div_eq_mul_inv]
      -- C·(1/b) ≤ C·(2/K0) since 1/b ≤ 2/K0 and C ≥ 0
      simpa [one_div] using (mul_le_mul_of_nonneg_left hrec hC0)
    exact h1.trans h2
  have h2 : (2 * (w / L)) * (1 + |kMT x|) / F_L ϱ L w 0
      ≤ (2 * (w / L)) * (C * (2 / K0)) := by
    -- (2w/L) ≥ 0 ; (1+|kMT|)/b ≤ C·(2/K0) ; divide: (2w/L)·a₁ ≤ (2w/L)·a₂
    have hb : (1 + |kMT x|) / F_L ϱ L w 0 ≤ C * (2 / K0) := hpart
    have hwLv : 0 ≤ 2 * (w / L) := by positivity
    simpa [div_eq_mul_inv, mul_assoc] using (mul_le_mul_of_nonneg_left hb hwLv)
  -- (2w/L)·C·(2/K0) = (4·w·C/K0)·(1/L) ≤ ε by choice of L₀
  have hwkh : (2 * (w / L)) * C * (2 / K0) = (4 * w * C / K0) / L := by
    field_simp [hLpos.ne', K0_pos.ne']
    ring
  have hmain : |KL_ratio ϱ L w x - kMT x| ≤ (2 * (w / L)) * C * (2 / K0) := by
    calc
      |KL_ratio ϱ L w x - kMT x| ≤ (2 * (w / L)) * (1 + |kMT x|) / F_L ϱ L w 0 := hbnd
      _ ≤ (2 * (w / L)) * (C * (2 / K0)) := h2
      _ = (2 * (w / L)) * C * (2 / K0) := by ring
  -- L ≥ L₀ = 4·w·C/(K0·ε) ⟹ (4·w·C/K0)/L ≤ ε
  have hεle : (4 * w * C / K0) / L ≤ ε := by
    have hεL : ε * L₀ ≤ ε * L := mul_le_mul_of_nonneg_left hLle (le_of_lt hε)
    have hεL₀ : ε * L₀ = 4 * w * C / K0 := by
      unfold L₀
      field_simp [K0_pos.ne', mul_ne_zero K0_pos.ne' (ne_of_gt hε)]
    have hle' : 4 * w * C / K0 ≤ ε * L := by
      rw [← hεL₀]
      exact hεL
    rw [div_le_iff₀ hLpos]
    exact hle'
  -- assemble
  have hfinal2 : |KL_ratio ϱ L w x - kMT x| ≤ ε := by
    rw [hwkh] at hmain
    exact le_trans hmain hεle
  exact hfinal2
