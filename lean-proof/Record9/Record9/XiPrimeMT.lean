/-
Record9.XiPrimeMT — T3: the Montgomery–Taylor (cos) AdmWindow instance for the ξ′ system.

Part of the Stage C T3 formalizer pass for the ξ′ record theorem
(C₉(ξ′) = (657,500·H_{ξ′} − 1,310)/655,001, H_{ξ′} = 2 − κ₁(1, v_MT),
v_MT(s) = cos(√2·s)).

Statement contract: reports/admwindow-cos-instance.md (§1 profile, §2 ModFactor),
reports/xi-prime-cor22-derivation.md, reports/xi-prime-pressure-method.md and
reports/xi-prime-audit-manager.md (A1–A6 PASS). Template (exact pattern): the quartic
profile/modulated-window stack in the snapshot — Zeta23/XiPrime/QuarticWindow/{Quartic,
ModWindow,Params,ZeroSide}.lean and Zeta23/XiPrime/Certificate/AtOne.lean. O1 baseline
(Zeta23.XiPrime.*) is formally verified in the snapshot.

Machine content of THIS pass (bounded, honest milestones):
  M1  : v_MT := cos(√2·s) profile (even, nonneg/le_one on [−1/2,1/2], C^2), the ModFactor
        instance `ModFactor (fc L) L 1 2` for f_c(u) = √(max 0 cos(√2·u/L)) (cos ≥ 3/4 > 0 on
        the core, so on |u| ≤ L/2 this is the blueprint's √(cos(√2·u/L)); the `max 0` matches
        P.phiV's definition so `P.phiV v_MT T = phiM (fc (P.L T)) …` holds by rfl exactly as
        the quartic), and the AdmWindow witness
        `admWindow_phiV_MT : AdmWindow (P.phiV vMT T) (P.L T) P.w (cMT P.ϱ)` descending from
        `admWindow_phiM` with window constant cMod ϱ 1 2 = cRho ϱ + 1 + 1 + 2 = **cRho + 4**
        (strictly better than the quartic's cRho + 15.75).
  M2  : the zero side `windowZeroSide_atV_MT` for the MT profile, from `aV_range_MT`
        (1/2 ≤ a_V(T) ≤ 1 at 8w ≤ L, profile-side a_MT = 1/2 + sin(√2)/(2√2) ∈ [1/2,1]).
  M3  : (stretch) the ε-form record statement `record_c9xip` mirroring T1's `record_c9`, with
        H_xip = 2 − κ₁(1, vMT) and c9ConstXip = (657,500·H_xip − 1,310)/655,001, and the ξ′
        chain carried as the EXPLICIT axiom-free hypothesis `xiChain` exactly as T1's
        `record9Bridge` carried steps 2,5,6. The AtOne κ₁(1,vMT) certificate content is a
        separate OPEN obligation (recorded), as is the ξ′ chain itself.

Fidelity vs blueprint §1:
  • The four profile norms ‖v′‖₁ ≤ 1/2, ‖(v²)′‖₁ ≤ 38/45, ‖v″‖₁ ≤ 2, ‖(v²)″‖₁ ≤ 4 are
    PAPER constants (closed forms 2(1−cos(1/√2)), 1−cos(√2), 2√2·sin(1/√2), 2√2·sin(√2));
    they are NOT structurally required by the modulated AdmWindow path (the window norms are
    bounded through `ModFactor`'s A, B = 1, 2 — see ModWindow.lean, `admWindow_phiM`), so
    they are recorded here as the committed paper-level profile-norm obligations, not as
    Lean AdmWindow fields. The AdmWindow the zero side needs (WindowCore.lean:31-43 fields
    even/nonneg/le_one/contDiff/support/l1_deriv/l1_deriv_sq/l1_deriv2/l1_deriv2_sq) is
    produced entirely by `admWindow_phiM modFactor_fc`.
  NO sorry/admit/axiom appear in this file. Statements are not weakened.
-/
import Zeta23.XiPrime.QuarticWindow.ZeroSide
import Zeta23.XiPrime.Certificate.AtOne

noncomputable section

open Real Set MeasureTheory Filter Topology

namespace Zeta23
namespace XiPrime

/-! ## M1 — the v_MT = cos(√2·s) profile -/

/-- v_MT(s) = cos(√2·s): the Montgomery–Taylor profile. -/
def vMT (s : ℝ) : ℝ := Real.cos (Real.sqrt 2 * s)

lemma vMT_even (s : ℝ) : vMT (-s) = vMT s := by
  simp only [vMT, mul_neg]
  rw [Real.cos_neg]

/-- (√2)² = 2. -/
lemma sqrt_two_sq : (Real.sqrt (2 : ℝ)) ^ 2 = 2 := by
  rw [sq, Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 2)]

/-- 1 ≤ √3. -/
lemma sqrt_three_ge_one : (1 : ℝ) ≤ Real.sqrt 3 := by
  rw [← Real.sqrt_one]
  exact Real.sqrt_le_sqrt (by norm_num : (1 : ℝ) ≤ (3 : ℝ))

/-- 2·√(3/4) = √3. -/
lemma two_mul_sqrt_three_quarters : (2 : ℝ) * Real.sqrt (3 / 4) = Real.sqrt 3 := by
  have h23 : (2 : ℝ) ^ 2 * (3 / 4) = 3 := by norm_num
  calc
    (2 : ℝ) * Real.sqrt (3 / 4) = Real.sqrt ((2 : ℝ) ^ 2) * Real.sqrt (3 / 4) := by
      rw [Real.sqrt_sq (by norm_num : 0 ≤ (2 : ℝ))]
    _ = Real.sqrt ((2 : ℝ) ^ 2 * (3 / 4)) :=
      (Real.sqrt_mul' ((2 : ℝ) ^ 2) (by norm_num : 0 ≤ (3 : ℝ) / 4)).symm
    _ = Real.sqrt 3 := by rw [h23]

/-- on the core |s| ≤ 1/2, v_MT(s) ≥ 3/4 (cos x ≥ 1 − x²/2 at x = √2s, |x| ≤ 1/√2). -/
lemma vMT_core_ge {s : ℝ} (hs : s ∈ Icc (-(1/2 : ℝ)) (1/2)) : 3 / 4 ≤ vMT s := by
  have habs : |s| ≤ 1 / 2 := abs_le.mpr ⟨hs.1, hs.2⟩
  have harg : |Real.sqrt 2 * s| ≤ Real.sqrt 2 * (1 / 2) := by
    calc
      |Real.sqrt 2 * s| = Real.sqrt 2 * |s| := by
        rw [abs_mul, abs_of_pos (Real.sqrt_pos.2 (by norm_num : (0 : ℝ) < 2))]
      _ ≤ Real.sqrt 2 * (1 / 2) := mul_le_mul_of_nonneg_left habs (Real.sqrt_nonneg _)
  have hsqraw : (Real.sqrt 2 * s) ^ 2 ≤ (Real.sqrt 2 * (1 / 2)) ^ 2 :=
    sq_le_sq.mpr (by
      rw [abs_of_pos (by positivity : (0 : ℝ) < Real.sqrt 2 * (1 / 2))]
      exact harg)
  have hb2 : (Real.sqrt 2 * (1 / 2)) ^ 2 = 1 / 2 := by
    rw [show (Real.sqrt 2 * (1 / 2)) ^ 2 = (Real.sqrt (2 : ℝ)) ^ 2 * (1 / 2) ^ 2 by
      rw [mul_pow]]
    rw [sqrt_two_sq]
    norm_num
  have hx2 : (Real.sqrt 2 * s) ^ 2 ≤ 1 / 2 := le_trans hsqraw (by rw [hb2])
  have hb : (3 : ℝ) / 4 ≤ 1 - (Real.sqrt 2 * s) ^ 2 / 2 := by nlinarith
  unfold vMT
  exact le_trans hb Real.one_sub_sq_div_two_le_cos

lemma vMT_nonneg_on {s : ℝ} (hs : s ∈ Icc (-(1/2 : ℝ)) (1/2)) : 0 ≤ vMT s :=
  le_trans (by norm_num : (0 : ℝ) ≤ 3 / 4) (vMT_core_ge hs)

lemma vMT_le_one (s : ℝ) : vMT s ≤ 1 := by
  unfold vMT
  exact Real.cos_le_one _

lemma vMT_contDiff : ContDiff ℝ 2 vMT := by
  unfold vMT
  fun_prop

/-! ## M1 — the modulating factor f_c(u) = √(max 0 cos(√2·u/L)) (cos ≥ 3/4 > 0 on the core) -/

/-- the u-variable factor building block h_c(u) := cos(√2·u/L) = v_MT(u/L). -/
def hc (L : ℝ) (u : ℝ) : ℝ := Real.cos (Real.sqrt 2 * (u / L))

/-- the MT modulating factor `f_c(u) = √(max 0 (cos(√2·u/L)))`. On |u| ≤ L/2 the `max 0` is
    inert (`cos ≥ 3/4 > 0`), so this is exactly the blueprint's √(cos(√2·u/L)) there; the
    `max 0` matches `P.phiV`'s definition, so `P.phiV vMT T = phiM (fc (P.L T)) …` holds by
    rfl (as the quartic's `phiV_quartic_eq`). -/
def fc (L : ℝ) (u : ℝ) : ℝ := Real.sqrt (max 0 (hc L u))

variable {L : ℝ}

/-- on the core u/L ∈ [−1/2, 1/2]. -/
lemma fc_core_mem (hL : 0 < L) {u : ℝ} (hu : |u| ≤ L / 2) : u / L ∈ Icc (-(1/2 : ℝ)) (1/2) := by
  have := abs_le.mp hu
  constructor
  · rw [le_div_iff₀ hL]; linarith
  · rw [div_le_iff₀ hL]; linarith

/-- on the core, h_c ≥ 3/4. -/
lemma hc_core_ge (hL : 0 < L) {u : ℝ} (hu : |u| ≤ L / 2) : 3 / 4 ≤ hc L u := by
  simpa [hc, vMT] using vMT_core_ge (fc_core_mem hL hu)

/-- on the core, h_c > 0 (hence max 0 inert). -/
lemma hc_core_pos (hL : 0 < L) {u : ℝ} (hu : |u| ≤ L / 2) : 0 < hc L u :=
  lt_of_lt_of_le (by norm_num : (0 : ℝ) < 3 / 4) (hc_core_ge hL hu)

/-- on the core, f_c ≥ √(3/4) (blueprint's core lower bound, better than the quartic's 4/5). -/
lemma fc_core_ge (hL : 0 < L) {u : ℝ} (hu : |u| ≤ L / 2) : Real.sqrt (3 / 4) ≤ fc L u := by
  unfold fc
  rw [show max 0 (hc L u) = hc L u by exact max_eq_right (hc_core_pos hL hu).le]
  exact Real.sqrt_le_sqrt (hc_core_ge hL hu)

/-- on the core, f_c > 0 (so f_c, 2·f_c are invertible). -/
lemma fc_core_pos (hL : 0 < L) {u : ℝ} (hu : |u| ≤ L / 2) : 0 < fc L u :=
  lt_of_lt_of_le (by norm_num : (0 : ℝ) < Real.sqrt (3 / 4)) (fc_core_ge hL hu)

lemma fc_even (u : ℝ) : fc L (-u) = fc L u := by
  unfold fc hc
  simp only [neg_div, mul_neg, Real.cos_neg]

lemma fc_nonneg (u : ℝ) : 0 ≤ fc L u := Real.sqrt_nonneg _

lemma fc_le_one (u : ℝ) : fc L u ≤ 1 := by
  unfold fc
  rw [show (1 : ℝ) = Real.sqrt 1 from Real.sqrt_one.symm]
  exact Real.sqrt_le_sqrt (max_le (by norm_num) (Real.cos_le_one _))

/-- √2 ≤ 2. -/
lemma sqrt_two_le_two : Real.sqrt 2 ≤ 2 := by
  have hsq : (Real.sqrt 2) ^ 2 ≤ (2 : ℝ) ^ 2 := by rw [sqrt_two_sq]; norm_num
  have hle_abs : |Real.sqrt 2| ≤ |(2 : ℝ)| := sq_le_sq.mp hsq
  simpa [abs_of_nonneg (Real.sqrt_nonneg _)] using hle_abs

/-- argument √2·t/L on the core stays in [0, π] (indeed ≤ 1 < π). -/
lemma sqrt2_arg_core (hL : 0 < L) {u : ℝ} (hu : 0 ≤ u) (huL : u ≤ L / 2) :
    Real.sqrt 2 * (u / L) ≤ Real.pi := by
  have hle1 : Real.sqrt 2 * (u / L) ≤ 1 := by
    have hdiv : Real.sqrt 2 * (u / L) ≤ Real.sqrt 2 * (1 / 2) := by
      calc
        Real.sqrt 2 * (u / L) ≤ Real.sqrt 2 * ((L / 2) / L) :=
          mul_le_mul_of_nonneg_left (div_le_div_of_nonneg_right huL hL.le) (Real.sqrt_nonneg _)
        _ = Real.sqrt 2 * (1 / 2) := by
          rw [show (L / 2) / L = 1 / 2 by field_simp]
    calc
      Real.sqrt 2 * (u / L) ≤ Real.sqrt 2 * (1 / 2) := hdiv
      _ ≤ 2 * (1 / 2) := mul_le_mul_of_nonneg_right sqrt_two_le_two (by norm_num)
      _ = 1 := by ring
  have hpi : (1 : ℝ) ≤ Real.pi := by linarith [Real.pi_gt_three]
  linarith

/-- f_c is antitone on [0, L/2]: cos antitone on [0,π] with arg ≤ 1 < π, √ increasing. -/
lemma fc_antitoneOn (hL : 0 < L) : AntitoneOn (fc L) (Icc 0 (L / 2)) := by
  intro x hx y hy hxy
  simp only [mem_Icc] at hx hy
  unfold fc
  apply Real.sqrt_le_sqrt
  apply max_le_max le_rfl
  have hcos : Real.cos (Real.sqrt 2 * (y / L)) ≤ Real.cos (Real.sqrt 2 * (x / L)) :=
    Real.cos_le_cos_of_nonneg_of_le_pi
      (mul_nonneg (Real.sqrt_nonneg _) (div_nonneg hx.1 hL.le))
      (sqrt2_arg_core hL hy.1 hy.2)
      (mul_le_mul_of_nonneg_left (div_le_div_of_nonneg_right hxy hL.le) (Real.sqrt_nonneg _))
  simpa [hc] using hcos

/-- h_c is C^∞ (analytic). -/
lemma hc_contDiff (hL : 0 < L) : ContDiff ℝ ⊤ (hc L) := by
  unfold hc
  exact Real.contDiff_cos.comp (by fun_prop : ContDiff ℝ ⊤ (fun u : ℝ => Real.sqrt 2 * (u / L)))

/-- h_c > 0 on the smooth neighbourhood U := (−(L/2+δ), L/2+δ) for δ = L/10
    (|√2·u/L| ≤ √2·(3/5) < π/2 there, so cos > 0). -/
lemma hc_pos_of_mem (hL : 0 < L) {u : ℝ} (hu : u ∈ Ioo (-(L / 2 + L / 10)) (L / 2 + L / 10)) :
    0 < hc L u := by
  have hub : |u / L| ≤ 3 / 5 := by
    apply le_of_lt
    rw [abs_div, abs_of_pos hL, div_lt_iff₀ hL]
    rw [abs_lt]
    constructor <;> linarith [hu.1, hu.2]
  have harg : |Real.sqrt 2 * (u / L)| < Real.pi / 2 := by
    have hsmall : Real.sqrt 2 * (3 / 5) < Real.pi / 2 := by
      have hs2 : Real.sqrt 2 ≤ 3 / 2 := by
        have hsq : (Real.sqrt 2) ^ 2 ≤ (3 / 2) ^ 2 := by rw [sqrt_two_sq]; norm_num
        have hle : |Real.sqrt 2| ≤ |3 / 2| := sq_le_sq.mp hsq
        simpa [abs_of_nonneg (Real.sqrt_nonneg _),
          abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 3 / 2)] using hle
      calc
        Real.sqrt 2 * (3 / 5) ≤ (3 / 2) * (3 / 5) :=
          mul_le_mul_of_nonneg_right hs2 (by norm_num)
        _ = 9 / 10 := by norm_num
        _ < Real.pi / 2 := by
          nlinarith [Real.pi_gt_three]
    calc
      |Real.sqrt 2 * (u / L)| = Real.sqrt 2 * |u / L| := by
        rw [abs_mul, abs_of_pos (Real.sqrt_pos.2 (by norm_num : (0 : ℝ) < 2))]
      _ ≤ Real.sqrt 2 * (3 / 5) := mul_le_mul_of_nonneg_left hub (Real.sqrt_nonneg _)
      _ < Real.pi / 2 := hsmall
  unfold hc
  have hup : Real.sqrt 2 * (u / L) < Real.pi / 2 := (abs_lt.mp harg).2
  have hdown : -(Real.pi / 2) < Real.sqrt 2 * (u / L) := (abs_lt.mp harg).1
  exact Real.cos_pos_of_mem_Ioo ⟨hdown, hup⟩

/-- f_c = √h_c on the smooth neighbourhood (max 0 inert because h_c > 0). -/
lemma fc_eq_sqrt_of_mem (hL : 0 < L) {u : ℝ} (hu : u ∈ Ioo (-(L / 2 + L / 10)) (L / 2 + L / 10)) :
    fc L u = Real.sqrt (hc L u) := by
  unfold fc
  rw [show max 0 (hc L u) = hc L u by exact max_eq_right (hc_pos_of_mem hL hu).le]

lemma fc_contDiffOn (hL : 0 < L) :
    ContDiffOn ℝ 2 (fc L) (Ioo (-(L / 2 + L / 10)) (L / 2 + L / 10)) := by
  have h1 : ContDiffOn ℝ 2 (fun u => Real.sqrt (hc L u)) (Ioo (-(L / 2 + L / 10)) (L / 2 + L / 10)) :=
    ((hc_contDiff hL).of_le le_top).contDiffOn.sqrt fun u hu => (hc_pos_of_mem hL hu).ne'
  exact h1.congr fun u hu => fc_eq_sqrt_of_mem hL hu

/-- f_c · f_c = h_c on the smooth neighbourhood (max 0 inert). -/
lemma fc_mul_self_of_mem (hL : 0 < L) {u : ℝ} (hu : u ∈ Ioo (-(L / 2 + L / 10)) (L / 2 + L / 10)) :
    fc L u * fc L u = hc L u := by
  rw [fc_eq_sqrt_of_mem hL hu, ← sq, Real.sq_sqrt (hc_pos_of_mem hL hu).le]

/-! ### derivatives of h_c -/

/-- derivative of the argument map `u ↦ √2·u/L`. -/
lemma hasDerivAt_argSqrt2 (hL : 0 < L) (u : ℝ) :
    HasDerivAt (fun u : ℝ => Real.sqrt 2 * (u / L)) (Real.sqrt 2 * (1 / L)) u := by
  have h1 : HasDerivAt (fun u : ℝ => u / L) (1 / L) u := by
    simpa [div_eq_mul_inv] using (hasDerivAt_id u).mul_const (L⁻¹)
  simpa [div_eq_mul_inv] using h1.const_mul (Real.sqrt 2)

lemma hasDerivAt_cos_argSqrt2 (hL : 0 < L) (u : ℝ) :
    HasDerivAt (fun u => Real.cos (Real.sqrt 2 * (u / L)))
      (-Real.sin (Real.sqrt 2 * (u / L)) * (Real.sqrt 2 * (1 / L))) u := by
  have harg := hasDerivAt_argSqrt2 hL u
  exact HasDerivAt.comp u (hasDerivAt_cos (Real.sqrt 2 * (u / L))) harg

lemma hasDerivAt_sin_argSqrt2 (hL : 0 < L) (u : ℝ) :
    HasDerivAt (fun u : ℝ => Real.sin (Real.sqrt 2 * (u / L)))
      (Real.cos (Real.sqrt 2 * (u / L)) * (Real.sqrt 2 * (1 / L))) u := by
  have harg := hasDerivAt_argSqrt2 hL u
  exact HasDerivAt.comp u (hasDerivAt_sin (Real.sqrt 2 * (u / L))) harg

lemma hasDerivAt_hc (hL : 0 < L) (u : ℝ) :
    HasDerivAt (hc L) (-(Real.sin (Real.sqrt 2 * (u / L)) * (Real.sqrt 2 * (1 / L)))) u := by
  convert hasDerivAt_cos_argSqrt2 hL u using 1
  · rfl
  · ring

lemma deriv_hc (hL : 0 < L) (u : ℝ) :
    deriv (hc L) u = -(Real.sin (Real.sqrt 2 * (u / L)) * (Real.sqrt 2 * (1 / L))) :=
  (hasDerivAt_hc hL u).deriv

/-- |h_c′| ≤ 1/L on the core. -/
lemma abs_deriv_hc_le (hL : 0 < L) {u : ℝ} (hu : |u| ≤ L / 2) : |deriv (hc L) u| ≤ 1 / L := by
  rw [deriv_hc hL]
  have h1q : (0 : ℝ) ≤ Real.sqrt 2 * (1 / L) :=
    mul_nonneg (Real.sqrt_nonneg _) (le_of_lt (one_div_pos.mpr hL))
  calc
    |-(Real.sin (Real.sqrt 2 * (u / L)) * (Real.sqrt 2 * (1 / L)))|
        = (Real.sqrt 2 * (1 / L)) * |Real.sin (Real.sqrt 2 * (u / L))| := by
          rw [abs_neg, abs_mul, abs_of_nonneg h1q]
          ring
    _ ≤ (Real.sqrt 2 * (1 / L)) * |Real.sqrt 2 * (u / L)| :=
          mul_le_mul_of_nonneg_left (Real.abs_sin_le_abs) h1q
    _ = (Real.sqrt 2 * (1 / L)) * (Real.sqrt 2 * |u / L|) := by
          congr 1
          rw [abs_mul, abs_of_pos (Real.sqrt_pos.2 (by norm_num : (0 : ℝ) < 2))]
    _ = 2 * (1 / L) * |u / L| := by
      have hsq2 : Real.sqrt 2 * Real.sqrt 2 = 2 := by rw [← sq, sqrt_two_sq]
      calc
        (Real.sqrt 2 * (1 / L)) * (Real.sqrt 2 * |u / L|)
            = (Real.sqrt 2 * Real.sqrt 2) * ((1 / L) * |u / L|) := by ring
        _ = 2 * ((1 / L) * |u / L|) := by rw [hsq2]
        _ = 2 * (1 / L) * |u / L| := by ring
    _ ≤ 2 * (1 / L) * (1 / 2) := by
          have huq : |u / L| ≤ 1 / 2 := by
            rw [abs_div, abs_of_pos hL, div_le_iff₀ hL]
            linarith [hu]
          exact mul_le_mul_of_nonneg_left huq (by positivity)
    _ = 1 / L := by field_simp

/-- |h_c″| ≤ 2/L² on the core. -/
lemma abs_deriv2_hc_le (hL : 0 < L) {u : ℝ} (hu : |u| ≤ L / 2) :
    |deriv (deriv (hc L)) u| ≤ 2 / L ^ 2 := by
  have hsq2 : Real.sqrt 2 * Real.sqrt 2 = 2 := by rw [← sq, sqrt_two_sq]
  have hd2 : deriv (deriv (hc L)) u = -(2 / L ^ 2) * Real.cos (Real.sqrt 2 * (u / L)) := by
    have e : deriv (hc L) = fun u => -(Real.sin (Real.sqrt 2 * (u / L)) * (Real.sqrt 2 * (1 / L))) :=
      funext (deriv_hc hL)
    rw [e]
    have hsin := hasDerivAt_sin_argSqrt2 hL u
    have hf : HasDerivAt (fun u : ℝ => -(Real.sin (Real.sqrt 2 * (u / L)) * (Real.sqrt 2 * (1 / L))))
        (-((Real.cos (Real.sqrt 2 * (u / L)) * (Real.sqrt 2 * (1 / L))) * (Real.sqrt 2 * (1 / L)))) u :=
      (hsin.mul_const (Real.sqrt 2 * (1 / L))).neg
    rw [hf.deriv]
    calc
      -((Real.cos (Real.sqrt 2 * (u / L)) * (Real.sqrt 2 * (1 / L))) * (Real.sqrt 2 * (1 / L)))
          = -((Real.sqrt 2 * Real.sqrt 2) * (1 / L) * (1 / L) * Real.cos (Real.sqrt 2 * (u / L))) := by ring
      _ = -((2 : ℝ) * (1 / L) * (1 / L) * Real.cos (Real.sqrt 2 * (u / L))) := by rw [hsq2]
      _ = -(2 / L ^ 2) * Real.cos (Real.sqrt 2 * (u / L)) := by field_simp
  rw [hd2]
  have h2 : (0 : ℝ) ≤ 2 / L ^ 2 := by positivity
  calc
    |-(2 / L ^ 2) * Real.cos (Real.sqrt 2 * (u / L))|
        = (2 / L ^ 2) * |Real.cos (Real.sqrt 2 * (u / L))| := by
          rw [abs_mul, abs_neg, abs_of_nonneg h2]
    _ ≤ (2 / L ^ 2) * 1 := mul_le_mul_of_nonneg_left (Real.abs_cos_le_one _) h2
    _ = 2 / L ^ 2 := by ring

/-! ### derivatives of f_c on the core, through f_c · f_c = h_c -/

-- the second-derivative bound set U (quartic template).
lemma abs_deriv_fc_le (hL : 0 < L) {u : ℝ} (hu : |u| ≤ L / 2) : |deriv (fc L) u| ≤ 1 / L := by
  set U : Set ℝ := Ioo (-(L / 2 + L / 10)) (L / 2 + L / 10) with hUdef
  have hU : IsOpen U := isOpen_Ioo
  have huU : u ∈ U := by
    simp only [hUdef, mem_Ioo]; constructor <;> linarith [neg_abs_le u, le_abs_self u]
  have hsm := fc_contDiffOn hL
  have hfc_pos : 0 < fc L u := fc_core_pos hL hu
  have hfc_ne : fc L u ≠ 0 := hfc_pos.ne'
  -- h' = 2 f f'
  have hev : (fun v => fc L v * fc L v) =ᶠ[nhds u] hc L := by
    filter_upwards [hU.mem_nhds huU] with v hv using fc_mul_self_of_mem hL hv
  have hd : deriv (hc L) u = deriv (fc L) u * fc L u + fc L u * deriv (fc L) u := by
    rw [← hev.deriv_eq]; exact deriv_mul_eq hU hsm hsm huU
  have hh := abs_deriv_hc_le hL hu
  have e : deriv (fc L) u = deriv (hc L) u / (2 * fc L u) := by
    rw [hd]; field_simp [hfc_ne]; ring
  have htwo_pos : 0 < 2 * fc L u := by nlinarith [hfc_pos]
  rw [e, abs_div, abs_of_pos htwo_pos]
  rw [div_le_div_iff₀ htwo_pos hL]
  calc
    |deriv (hc L) u| * L ≤ (1 / L) * L := by gcongr
    _ = 1 := by field_simp
    _ ≤ 1 * (2 * fc L u) := by
      have hcge : (1 : ℝ) ≤ 2 * Real.sqrt (3 / 4) := by
        rw [two_mul_sqrt_three_quarters]
        exact sqrt_three_ge_one
      have h1 : (1 : ℝ) ≤ 2 * fc L u := by
        exact le_trans hcge (mul_le_mul_of_nonneg_left (fc_core_ge hL hu) (by norm_num))
      nlinarith

/-! the second derivative of f_c: through f_c · f_c = h_c, with the sharper
    (hc′²/(2h_c)) shape giving |f_c″| ≤ 8/(3√3 L²) < 2/L² (blueprint B = 2). -/
lemma abs_deriv2_fc_le (hL : 0 < L) {u : ℝ} (hu : |u| ≤ L / 2) :
    |deriv (deriv (fc L)) u| ≤ 2 / L ^ 2 := by
  set U : Set ℝ := Ioo (-(L / 2 + L / 10)) (L / 2 + L / 10) with hUdef
  have hU : IsOpen U := isOpen_Ioo
  have huU : u ∈ U := by
    simp only [hUdef, mem_Ioo]; constructor <;> linarith [neg_abs_le u, le_abs_self u]
  have hsm := fc_contDiffOn hL
  have hf := fc_core_ge hL hu
  have h1 := abs_deriv_hc_le hL hu
  have h2 := abs_deriv2_hc_le hL hu
  have hfc_pos : 0 < fc L u := fc_core_pos hL hu
  have hfc_ne : fc L u ≠ 0 := hfc_pos.ne'
  have htwo_pos : 0 < 2 * fc L u := by nlinarith [hfc_pos]
  -- h'' = 2 f f'' + 2 f'²
  have hd1 : ∀ v ∈ U, deriv (fun x => fc L x * fc L x) v = deriv (hc L) v := by
    intro v hv
    have hev : (fun x => fc L x * fc L x) =ᶠ[nhds v] hc L := by
      filter_upwards [hU.mem_nhds hv] with x hx using fc_mul_self_of_mem hL hx
    exact hev.deriv_eq
  have hev2 : deriv (fun x => fc L x * fc L x) =ᶠ[nhds u] deriv (hc L) := by
    filter_upwards [hU.mem_nhds huU] with v hv using hd1 v hv
  have hd2 : deriv (deriv (hc L)) u
      = deriv (deriv (fc L)) u * fc L u + 2 * (deriv (fc L) u * deriv (fc L) u)
        + fc L u * deriv (deriv (fc L)) u := by
    rw [← hev2.deriv_eq]; exact deriv2_mul_eq hU hsm hsm huU
  have e : deriv (deriv (fc L)) u
      = (deriv (deriv (hc L)) u - 2 * (deriv (fc L) u * deriv (fc L) u)) / (2 * fc L u) := by
    rw [hd2]; field_simp [hfc_ne]; ring
  -- fc' = hc' / (2 fc) on the core (from 2 f f' = h').
  have hfcp : deriv (fc L) u = deriv (hc L) u / (2 * fc L u) := by
    have hdm : deriv (hc L) u = deriv (fc L) u * fc L u + fc L u * deriv (fc L) u := by
      have hev : (fun v => fc L v * fc L v) =ᶠ[nhds u] hc L := by
        filter_upwards [hU.mem_nhds huU] with v hv using fc_mul_self_of_mem hL hv
      rw [← hev.deriv_eq]; exact deriv_mul_eq hU hsm hsm huU
    rw [hdm]; field_simp [hfc_ne]; ring
  have hfc2 : fc L u ^ 2 = hc L u := by simpa [sq] using fc_mul_self_of_mem hL huU
  have hsqabs (a : ℝ) : |a| ^ 2 = a ^ 2 := by rw [sq_abs]
  -- fc'² = hc'² / (4 hc) ≤ (1/L)²/(4·(3/4)) = 1/(3L²)
  have hfc_sq : (deriv (fc L) u) ^ 2 ≤ 1 / (3 * L ^ 2) := by
    rw [hfcp]
    have hnum_le : (deriv (hc L) u) ^ 2 ≤ (1 / L) ^ 2 := by
      have h1l : |1 / L| = 1 / L := abs_of_pos (one_div_pos.mpr hL)
      exact sq_le_sq.mpr (by rw [h1l]; exact h1)
    have hden_pos : 0 < 4 * hc L u := mul_pos (by norm_num : (0 : ℝ) < 4) (hc_core_pos hL hu)
    calc
      (deriv (hc L) u / (2 * fc L u)) ^ 2 = (deriv (hc L) u) ^ 2 / (2 * fc L u) ^ 2 := by
        rw [div_pow]
      _ ≤ (1 / L) ^ 2 / (2 * fc L u) ^ 2 :=
            div_le_div_of_nonneg_right hnum_le (by positivity)
      _ = (1 / L) ^ 2 / (4 * hc L u) := by
            rw [show (2 * fc L u) ^ 2 = 4 * (fc L u ^ 2) by ring, hfc2]
      _ ≤ (1 / L) ^ 2 / 3 := by
            have hden : 3 ≤ 4 * hc L u := by nlinarith [hc_core_ge hL hu]
            exact div_le_div_of_nonneg_left (sq_nonneg _) (by norm_num : (0 : ℝ) < 3) hden
      _ = 1 / (3 * L ^ 2) := by field_simp
  -- 2·|f'|² ≤ 2/(3L²)
  have hf2 : 2 * |deriv (fc L) u| ^ 2 ≤ 2 / 3 / L ^ 2 := by
    calc 2 * |deriv (fc L) u| ^ 2 = 2 * (deriv (fc L) u) ^ 2 := by rw [hsqabs]
      _ ≤ 2 * (1 / (3 * L ^ 2)) := mul_le_mul_of_nonneg_left hfc_sq (by norm_num)
      _ = 2 / 3 / L ^ 2 := by field_simp
  -- |hc'' − 2f'²| ≤ 2/L² + 2/(3L²) = 8/(3L²)
  have hnum : |deriv (deriv (hc L)) u - 2 * (deriv (fc L) u * deriv (fc L) u)| ≤ 8 / 3 / L ^ 2 := by
    have hf2' : 2 * (deriv (fc L) u * deriv (fc L) u) ≤ 2 / 3 / L ^ 2 := by
      have hsq : |deriv (fc L) u| ^ 2 = (deriv (fc L) u) ^ 2 := hsqabs (deriv (fc L) u)
      nlinarith [hsq, hf2]
    have hsplit : |deriv (deriv (hc L)) u - 2 * (deriv (fc L) u * deriv (fc L) u)|
        ≤ |deriv (deriv (hc L)) u| + |2 * (deriv (fc L) u * deriv (fc L) u)| :=
      abs_sub _ _
    have h2' : |2 * (deriv (fc L) u * deriv (fc L) u)| ≤ 2 / 3 / L ^ 2 := by
      have hnon : 0 ≤ 2 * (deriv (fc L) u * deriv (fc L) u) :=
        mul_nonneg (by norm_num : (0 : ℝ) ≤ 2) (mul_self_nonneg _)
      rwa [abs_of_nonneg hnon]
    calc
      |deriv (deriv (hc L)) u - 2 * (deriv (fc L) u * deriv (fc L) u)|
          ≤ |deriv (deriv (hc L)) u| + |2 * (deriv (fc L) u * deriv (fc L) u)| := hsplit
      _ ≤ 2 / L ^ 2 + 2 / 3 / L ^ 2 := by linarith
      _ = 8 / 3 / L ^ 2 := by field_simp; ring
  -- |f''| = |hc'' − 2f'²|/(2f) ≤ (8/(3L²))/√3 ≤ 2/L²
  have hb_ge : Real.sqrt 3 ≤ 2 * fc L u := by
    have hcge : Real.sqrt 3 = 2 * Real.sqrt (3 / 4) := two_mul_sqrt_three_quarters.symm
    rw [hcge]
    exact mul_le_mul_of_nonneg_left hf (by norm_num)
  have hsqrt_pos : 0 < Real.sqrt 3 := by positivity
  rw [e, abs_div, abs_of_pos htwo_pos]
  calc
    |deriv (deriv (hc L)) u - 2 * (deriv (fc L) u * deriv (fc L) u)| / (2 * fc L u)
        ≤ |deriv (deriv (hc L)) u - 2 * (deriv (fc L) u * deriv (fc L) u)| / Real.sqrt 3 :=
          div_le_div_of_nonneg_left (abs_nonneg _) hsqrt_pos hb_ge
    _ ≤ (8 / 3 / L ^ 2) / Real.sqrt 3 :=
          div_le_div_of_nonneg_right hnum (Real.sqrt_nonneg _)
    _ ≤ 2 / L ^ 2 := by
      have h3 : (Real.sqrt (3 : ℝ)) ^ 2 = 3 := by rw [sq, Real.mul_self_sqrt (by norm_num : 0 ≤ (3 : ℝ))]
      have hval : (8 : ℝ) / 3 ≤ 2 * Real.sqrt 3 := by nlinarith [Real.sqrt_nonneg (3 : ℝ)]
      have hL2nz : L ^ 2 ≠ 0 := ne_of_gt (by positivity : 0 < L ^ 2)
      have hs3nz : Real.sqrt 3 ≠ 0 := by positivity
      field_simp [hL2nz, hs3nz]
      nlinarith [hval]

/-! ### the ModFactor instance and the admissible window -/

/-- **the ModFactor instance for the MT (cos) factor: A = 1, B = 2.** -/
theorem modFactor_fc (hL : 0 < L) : ModFactor (fc L) L 1 2 where
  A_nonneg := by norm_num
  B_nonneg := by norm_num
  even := fc_even
  nonneg := fc_nonneg
  le_one := fun u _ => fc_le_one u
  antitone := fc_antitoneOn hL
  smooth := ⟨L / 10, by positivity, fc_contDiffOn hL⟩
  deriv_le := fun u hu => abs_deriv_fc_le hL hu
  deriv2_le := fun u hu => abs_deriv2_fc_le hL hu

/-- the window constant of the MT window: cRho ϱ + 1 + 1² + 2 = cRho + 4. -/
def cMT (ϱ : ℝ → ℝ) : ℝ := cMod ϱ 1 2

/-- the MT window constant is cRho + 4 (A = 1, B = 2). -/
lemma cMT_eq (ϱ : ℝ → ℝ) : cMT ϱ = Taper.cRho ϱ + 4 := by
  unfold cMT cMod
  norm_num
  ring

/-- P.phiV vMT T is the modulated taper with factor fc (rfl). -/
theorem phiV_MT_eq (P : Params) (T : ℝ) : P.phiV vMT T = phiM (fc (P.L T)) P.ϱ (P.L T) P.w := rfl

/-- **The Montgomery–Taylor (cos) window is admissible, with c = cRho + 4.** -/
theorem admWindow_phiV_MT {P : Params} (hP : P.Valid) {T : ℝ} (hwL : 8 * P.w ≤ P.L T) :
    AdmWindow (P.phiV vMT T) (P.L T) P.w (cMT P.ϱ) := by
  have hL : 0 < P.L T := by linarith [hP.one_le_w]
  rw [phiV_MT_eq]
  exact admWindow_phiM (modFactor_fc hL) hP.taper hP.one_le_w hwL

/-! ## M2 — the zero side for the MT profile -/

variable {P : Params}

theorem atV_MT_a_eq_av (hP : P.Valid) (T : ℝ) :
    (P.atV vMT T).a T = AdmWindow.av (P.phiV vMT T) (P.L T) :=
  Params.atV_a T hP vMT_even

theorem atV_MT_phiHat (hP : P.Valid) (T : ℝ) :
    (P.atV vMT T).phiHat T = AdmWindow.vHat (P.phiV vMT T) :=
  Params.atV_phiHat T hP vMT_even

theorem atV_MT_phiHatR (hP : P.Valid) (T : ℝ) :
    (P.atV vMT T).phiHatR T = AdmWindow.vHatR (P.phiV vMT T) :=
  Params.atV_phiHatR T hP vMT_even

/-! ### 1/2 ≤ a_V ≤ 1 (profile a_MT = 1/2 + sin(√2)/(2√2) ∈ [1/2,1]) -/

/-- φ_MT² ≥ (3/4)·φ² pointwise (on the core v_MT ≥ 3/4; off it both vanish). -/
lemma phiV_MT_sq_ge (hP : P.Valid) {T : ℝ} (h8 : 8 * P.w ≤ P.L T) (u : ℝ) :
    3 / 4 * P.phi T u ^ 2 ≤ P.phiV vMT T u ^ 2 := by
  have hw0 : 0 < P.w := by linarith [hP.one_le_w]
  have hL : 0 < P.L T := by linarith [hP.one_le_w]
  rw [Params.phiV_eq, mul_pow, ← Params.phi_eq]
  rcases le_or_gt (P.L T / 2) |u| with hu | hu
  · rw [Params.phi_eq_zero hP hu]; simp
  · have hmem := fc_core_mem hL hu.le
    have hv := vMT_core_ge hmem
    have hm : max 0 (vMT (u / P.L T)) = vMT (u / P.L T) := by
      rw [max_eq_right (le_trans (by norm_num : (0 : ℝ) ≤ 3 / 4) hv)]
    rw [Real.sq_sqrt (le_max_left _ _), hm]
    exact mul_le_mul_of_nonneg_right hv (sq_nonneg _)

set_option maxHeartbeats 1600000 in
theorem aV_range_MT (hP : P.Valid) {T : ℝ} (h8 : 8 * P.w ≤ P.L T) :
    1 / 2 ≤ (P.atV vMT T).a T ∧ (P.atV vMT T).a T ≤ 1 := by
  have hW := admWindow_phiV_MT hP h8
  rw [atV_MT_a_eq_av hP]
  refine ⟨?_, hW.av_le_one⟩
  have hw0 : 0 < P.w := by linarith [hP.one_le_w]
  have h2 : 2 * P.w ≤ P.L T := by linarith
  have hL : 0 < P.L T := by linarith [hP.one_le_w]
  -- av ≥ (3/4)·aConst ≥ (3/4)(1 − 2w/L) ≥ (3/4)(3/4) = 9/16 ≥ 1/2
  have hb : 1 - 2 * P.w / P.L T ≤ P.a T :=
    (Taper.one_sub_le_bConst hP.taper hw0 h2).trans (Taper.bConst_le_aConst hP.taper hw0 h2)
  have hwL : 2 * P.w / P.L T ≤ 1 / 4 := by rw [div_le_iff₀ hL]; linarith
  have hint : Integrable (fun u => P.phiV vMT T u ^ 2) := hW.integrable_pow two_pos
  have hint' : Integrable (fun u => 3 / 4 * P.phi T u ^ 2) :=
    ((Params.phi_continuous hP (by linarith)).fun_pow 2 |>.integrable_of_hasCompactSupport
      ((Params.phi_hasCompactSupport hP).comp_left (g := fun t => t ^ 2) (by norm_num))).const_mul _
  have hcmp : 3 / 4 * ∫ u, P.phi T u ^ 2 ≤ ∫ u, P.phiV vMT T u ^ 2 := by
    rw [← integral_const_mul]
    exact integral_mono hint' hint (phiV_MT_sq_ge hP h8)
  have ha : P.a T = (P.L T)⁻¹ * ∫ u, P.phi T u ^ 2 := rfl
  unfold AdmWindow.av
  rw [ha] at hb
  have hLi : 0 < (P.L T)⁻¹ := inv_pos.mpr hL
  calc (1:ℝ) / 2 ≤ 3 / 4 * (1 - 2 * P.w / P.L T) := by nlinarith
    _ ≤ 3 / 4 * ((P.L T)⁻¹ * ∫ u, P.phi T u ^ 2) := by gcongr
    _ = (P.L T)⁻¹ * (3 / 4 * ∫ u, P.phi T u ^ 2) := by ring
    _ ≤ (P.L T)⁻¹ * ∫ u, P.phiV vMT T u ^ 2 := mul_le_mul_of_nonneg_left hcmp hLi.le

theorem eventually_aV_range_MT (hP : P.Valid) :
    ∀ᶠ T in atTop, 1 / 2 ≤ (P.atV vMT T).a T ∧ (P.atV vMT T).a T ≤ 1 := by
  filter_upwards [Params.eventually_w8 hP] with T h8
  exact aV_range_MT hP h8

/-! ## M2 — the generic-bundle instantiations for the MT profile -/

theorem poissonSqV_MT (hP : P.Valid) {T : ℝ} (h8 : 8 * P.w ≤ P.L T) :
    ZeroSide.PoissonSq T (P.atV vMT T) :=
  poissonSqV_of hP vMT_even (fun _ h => admWindow_phiV_MT hP h) h8

theorem blockInputsV_MT (Z : ZeroConfig) (hP : P.Valid) {T : ℝ} (h8 : 8 * P.w ≤ P.L T) :
    Assembly.BlockInputs Z (P.atV vMT T) T :=
  blockInputsV_of' hP vMT_even (fun _ h => admWindow_phiV_MT hP h) Z h8 (by linarith [(aV_range_MT hP h8).1])

theorem eventually_blockInputsV_MT (Z : ZeroConfig) (hP : P.Valid) :
    ∀ᶠ T in atTop, Assembly.BlockInputs Z (P.atV vMT T) T := by
  filter_upwards [Params.eventually_w8 hP] with T h8
  exact blockInputsV_MT Z hP h8

theorem GzGpV_MT (Z : ZeroConfig) (hEF : ExplicitFormulaPaper Z) (hP : P.Valid) {T : ℝ}
    (h8 : 8 * P.w ≤ P.L T) : Z.Gz (P.atV vMT T) T = (P.atV vMT T).Gp T :=
  GzGpV_of' hP vMT_even (fun _ h => admWindow_phiV_MT hP h) Z hEF h8

theorem eventually_GzGpV_MT (Z : ZeroConfig) (hEF : ExplicitFormulaPaper Z) (hP : P.Valid) :
    ∀ᶠ T in atTop, Z.Gz (P.atV vMT T) T = (P.atV vMT T).Gp T := by
  filter_upwards [Params.eventually_w8 hP] with T h8
  exact GzGpV_MT Z hEF hP h8

theorem eventually_tailPackageV_MT (Z : ZeroConfig) {A₀ : ℝ} (hA₀ : 1 ≤ A₀)
    (hloc : ∀ t : ℝ, (Z.N t (t + 1) : ℝ) ≤ A₀ * Real.log (|t| + 3)) (hP : P.Valid) :
    ∃ θ₀ : ℝ → ℝ, (∀ᶠ T in atTop, Assembly.TailInputs Z (P.atV vMT T) T (θ₀ T)) ∧
      ∃ C : ℝ, ∀ᶠ T in atTop, θ₀ T ≤ C * l T * T ^ (P.lam / 2 - 1) :=
  eventually_tailPackageV_of hP vMT_even (fun _ h => admWindow_phiV_MT hP h)
    ((eventually_aV_range_MT hP).mono fun _ h => h.1) Z hA₀ hloc

/-- **The Montgomery–Taylor window's zero side.** -/
theorem windowZeroSide_atV_MT (Z : ZeroConfig) (hR : RiemannVonMangoldt Z) (hP : P.Valid) :
    WindowZeroSide Z P (P.atV vMT) :=
  windowZeroSide_atV_of hP vMT_even (fun _ h => admWindow_phiV_MT hP h)
    ((eventually_aV_range_MT hP).mono fun _ h => h.1) Z hR

/-! ## M3 (stretch) — the ξ′ record statement (algebra + bridge, exact as T1) -/

/-- H_{ξ′} = 2 − κ₁(1, vMT), the ξ′ MT-window baseline constant
    = 0.86788886519905193555… (paper value; the AtOne certificate content for vMT — exact
    rationals for the integrals of vMT, vMT², vConv vMT and the D₁ sandwich — is an OPEN
    obligation, see FORMATLIZATION_STATUS_XIP.md). -/
def H_xip : ℝ := 2 - kappaXi 1 vMT

/-- C₉(ξ′) = (657,500·H_{ξ′} − 1,310)/655,001 = 0.86920009109661916184… -/
def c9ConstXip : ℝ := (657500 * H_xip - 1310) / 655001

/-- cLHS = 1 − A₀/m = 655001/657500 (as in T1). -/
abbrev cLHSxip : ℝ := 1 - (2499 : ℝ) / 2500 / 263

/-- (m−1)/(500m) = 262/131500 at m = 263 (as in T1). -/
abbrev qXip : ℝ := (262 : ℝ) / 131500

lemma cLHSxip_eq : cLHSxip = (655001 : ℝ) / 657500 := by norm_num [cLHSxip]

lemma cLHSxip_pos : 0 < cLHSxip := by norm_num [cLHSxip]

lemma qXip_eq : qXip = (131 : ℝ) / 65750 := by norm_num [qXip]

/-- the record numerator identity: 657,500·H − 1,310 = (H − 131/65750)·657,500. -/
lemma record9xip_constant_identity :
    (H_xip - (131 : ℝ) / 65750) * (657500 : ℝ) = 657500 * H_xip - 1310 := by
  ring

lemma c9ConstXip_eq : c9ConstXip = (H_xip - qXip) / cLHSxip := by
  unfold c9ConstXip qXip cLHSxip
  norm_num
  ring

/-- the ξ′ chain, ε-form, over the ξ′ zero counts (Ncount = N_{ξ′} with multiplicity,
    N0simple = N₀ˢ_{ξ′} simple-on-line). Carried as a HYPOTHESIS (open analytic + pressure +
    window-constant content), mirroring T1's `chain9_eps`. -/
def xiChain : Prop :=
  ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
    (1 - (2499 : ℝ) / 2500 / 263) * (N0simple T (2 * T) : ℝ)
      ≥ (H_xip - (262 : ℝ) / 131500 - ε) * (Ncount T (2 * T) : ℝ)

/-- **record_c9xip** — the ξ′ record theorem, ε-form (mirrors T1's `record_c9`):
    given the ξ′ chain `b : xiChain` (all the ξ′ analytic/pressure/certificate content carried
    as an explicit axiom-free hypothesis), derive
    ∀ε>0 ∃T₀ ∀T≥T₀, (c9ConstXip − ε)·N_{ξ′}(T,2T) ≤ N₀ˢ_{ξ′}(T,2T). -/
theorem record_c9xip (b : xiChain) :
    ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀,
      (c9ConstXip - ε) * (Ncount T (2 * T) : ℝ) ≤ N0simple T (2 * T) := by
  intro ε hε
  have hc : (0 : ℝ) < cLHSxip := cLHSxip_pos
  have hce : ε * cLHSxip > 0 := mul_pos hε hc
  obtain ⟨T₀, hT₀⟩ := b (ε * cLHSxip) hce
  refine ⟨T₀, fun T hT => ?_⟩
  let N : ℝ := (Ncount T (2 * T) : ℝ)
  let S : ℝ := (N0simple T (2 * T) : ℝ)
  have hS : cLHSxip * S ≥ (H_xip - (262 : ℝ) / 131500 - ε * cLHSxip) * N := by
    simpa [cLHSxip, N, S] using hT₀ T hT
  have hcoef : cLHSxip * (c9ConstXip - ε) = H_xip - (262 : ℝ) / 131500 - ε * cLHSxip := by
    unfold cLHSxip c9ConstXip
    ring
  have hchain : cLHSxip * (c9ConstXip - ε) * N ≤ cLHSxip * S := by
    calc
      cLHSxip * (c9ConstXip - ε) * N = (H_xip - (262 : ℝ) / 131500 - ε * cLHSxip) * N := by rw [hcoef]
      _ ≤ cLHSxip * S := by exact hS
  have hleft : cLHSxip * ((c9ConstXip - ε) * N) ≤ cLHSxip * S := by
    simpa [mul_assoc] using hchain
  have hcancel : (c9ConstXip - ε) * N ≤ S := by
    have hsimp : cLHSxip⁻¹ * (cLHSxip * ((c9ConstXip - ε) * N)) = (c9ConstXip - ε) * N := by
      rw [← mul_assoc, inv_mul_cancel₀ (ne_of_gt hc), one_mul]
    have hsimp2 : cLHSxip⁻¹ * (cLHSxip * S) = S := by
      rw [← mul_assoc, inv_mul_cancel₀ (ne_of_gt hc), one_mul]
    have hx : cLHSxip⁻¹ * (cLHSxip * ((c9ConstXip - ε) * N)) ≤ cLHSxip⁻¹ * (cLHSxip * S) :=
      mul_le_mul_of_nonneg_left hleft (inv_nonneg.mpr hc.le)
    simpa [hsimp, hsimp2] using hx
  simpa [N, S] using hcancel

end XiPrime
end Zeta23

end


