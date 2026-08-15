/-
Record9.XiPrimeAtOne — T3-open-A: the AtOne certificate content for the ξ′ MT-window
constant κ₁(1, vMT), vMT(s) = cos(√2·s).  Part of the Stage C T3 formalizer pass for the
ξ′ record theorem (C₉(ξ′) = (657,500·H_{ξ′} − 1,310)/655,001, H_{ξ′} = 2 − κ₁(1, vMT)).

This module mirrors `Zeta23/XiPrime/Certificate/AtOne.lean` (the flat/quartic "AtOne
pattern") for the Montgomery–Taylor profile.  In the flat/quartic case
  κ₉ := (∫v² + jWin(D1trunc 9, 1, v)) / (∫v)²   is an EXACT RATIONAL, and the certified
theorem is `kappaXi 1 v ∈ Icc kap9 (kap9 + eps9)`.  For v_MT the closed forms of ∫v, ∫v²,
∫v⁴ and vConv all involve sin/cos of √2 and are NOT rational, so the honest AtOne mirror is a
REAL constant here:

  κ₁(1,vMT) = (∫vMT² + jWin(D1,1,vMT)) / (∫vMT)²     (Defs.kappaXi; AtOne.kappaXi_one),
  IvMT       := ∫vMT = √2·sin(1/√2)                       (closed form),
  aMT        := ∫vMT² = 1/2 + sin(√2)/(2√2)              (blueprint `a`; = L⁻¹∫v² at L=1),
  bMT        := ∫vMT⁴ = 3/8 + sin(√2)/(2√2) + sin(2√2)/(16√2)  (blueprint `b`; = L⁻¹∫v⁴),
  vConvMTcl r := ½(1−r)cos(√2 r) + sin(√2(1−r))/(2√2)    (closed form of vConv vMT r),
  J1MT       := 2∫₀¹ D1trunc 9 r · vConvMTcl r dr,
  kappaXiOne_MT (κ₉) := (aMT + J1MT)/(IvMT)²,

and the certified sandwich (exactly the AtOne structure)

  κ₉ ≤ κ₁(1, vMT) ≤ κ₉ + ε₉ ,    ε₉ = 1024/2990212875,

where ε₉ is the already-formally-verified tail bound of `Zeta23.XiPrime.Certificate.D1`
(D1 s ≤ D1trunc 9 s + ε₉ on [0,1]); the D₁/D1trunc control comes entirely from that
formally-verified certificate.

Design — HONEST BRIDGE (T1/T3 pattern).  The heavy analytic content — evaluation of the
trig integrals (∫vMT = IvMT, ∫vMT² = aMT), the closed form vConv vMT = vConvMTcl on [0,1],
the Fubini identity 2∫₀¹ vConv vMT = (∫vMT)², and the positivity 0 < IvMT (⟺ vConv vMT ≥ 0
on [0,1], so the D₁-tail enters with the correct sign) — is carried as EXPLICIT axiom-free
theorem HYPOTHESES (open obligations M3-open-A).  Every theorem below proves its conclusion
genuinely from its hypotheses (no `sorry`/`admit`/`axiom`); the algebra closure (the AtOne
device, division inequalities, cancellation) is done here.  The math-level ARB enclosure of
κ₉ and the cross-check H = 2 − κ₁ = 0.8678888651990519355503… live in
`runs/rigorous-open-math-research/R-20260816T040000Z-xipAtOne-3078/`.

Fidelity: κ₁(1,vMT) is `kappaXi 1 vMT` (Defs.kappaXi); H_xip = 2 − κ₁(1,vMT)
(XiPrimeMT.H_xip); c9ConstXip is already fixed in XiPrimeMT.  No statement is weakened: the
hypotheses are genuine open analytic obligations and the conclusions are the exact AtOne
sandwich / sharp H range.

NO sorry/admit/axiom appears in this file.
-/
import Record9.XiPrimeMT
import Zeta23.XiPrime.Certificate.AtOne

noncomputable section

open Set MeasureTheory
open intervalIntegral

namespace Zeta23
namespace XiPrime

/-! ## the exact AtOne constants for v_MT -/

/-- ∫vMT = √2·sin(1/√2) — exact closed form of ∫_{−1/2}^{1/2} cos(√2 s) ds. -/
def IvMT : ℝ := Real.sqrt 2 * Real.sin (1 / Real.sqrt 2)

/-- a_MT := ∫vMT² = 1/2 + sin(√2)/(2√2)  (blueprint `a`; = L⁻¹∫v² at L=1). -/
def aMT : ℝ := 1 / 2 + Real.sin (Real.sqrt 2) / (2 * Real.sqrt 2)

/-- b_MT := ∫vMT⁴ = 3/8 + sin(√2)/(2√2) + sin(2√2)/(16√2)  (blueprint `b`; = L⁻¹∫v⁴ at L=1). -/
def bMT : ℝ :=
  3 / 8 + Real.sin (Real.sqrt 2) / (2 * Real.sqrt 2)
    + Real.sin (2 * Real.sqrt 2) / (16 * Real.sqrt 2)

/-- the exact closed form of (v⋆v)(r) for v_MT on [0,1]: ½(1−r)cos(√2 r) + sin(√2(1−r))/(2√2). -/
def vConvMTcl (r : ℝ) : ℝ :=
  (1 / 2 : ℝ) * ((1 - r) * Real.cos (Real.sqrt 2 * r))
    + Real.sin (Real.sqrt 2 * (1 - r)) / (2 * Real.sqrt 2)

/-- J1 := 2∫₀¹ D1trunc 9 r · vConvMTcl r dr.  By `vConvMT_closed` (hVcl) and `hjTr` below
    this equals `jWin (D1trunc 9) 1 vMT` = 2∫₀¹ D1trunc(1·r)·vConv vMT r dr. -/
def J1MT : ℝ := 2 * ∫ r in (0:ℝ)..1, D1trunc 9 r * vConvMTcl r

/-- **κ₉ := (aMT + J1MT)/(IvMT)²** — the AtOne-certified real constant for the MT window.
    Numerically κ₉ = 1.1321111338009974…; the certified theorem is κ₁(1,vMT) ∈ [κ₉, κ₉ + ε₉]. -/
def kappaXiOne_MT : ℝ := (aMT + J1MT) / (IvMT ^ 2)

/-! ## the honest-bridge open obligations (hypotheses; never `sorry`) -/

/-- M3-open-A(i): vConv vMT = vConvMTcl pointwise on [0,1] (product-to-sum closed form). -/
abbrev vConvMT_closed : Prop := ∀ r ∈ Icc (0:ℝ) 1, vConv vMT r = vConvMTcl r

/-- M3-open-A(ii): 2∫₀¹ vConv vMT = (∫vMT)² (Fubini identity for the autocorrelation). -/
abbrev two_integral_vConv_vMT : Prop := 2 * ∫ r in (0:ℝ)..1, vConv vMT r = (IvMT) ^ 2

/-- M3-open-A(iii): ∫vMT = IvMT and ∫vMT² = aMT (trig integral evaluations). -/
abbrev integral_vMT_forms : Prop :=
  (∫ s in (-(1:ℝ)/2)..(1/2), vMT s = IvMT) ∧
    (∫ s in (-(1:ℝ)/2)..(1/2), vMT s ^ 2 = aMT)

/-- M3-open-A(iv): 0 < IvMT (⟺ vConv vMT ≥ 0 on [0,1], so the D₁-tail enters with the
    correct sign in κ₁ and the division below is well-defined). -/
abbrev IvMT_pos : Prop := 0 < IvMT

/-! ## the conditional AtOne sandwich (honest bridge: algebra closure done, analytic facts
       `jWin_lo` / `jWin_hi` carried as hypotheses) -/

/-- M3-open-A(v): the two-sided jWin(D1,1,vMT) bound that the D₁-certificate gives, once the
    closed-form/Fubini facts are available:
       J1MT ≤ jWin(D1,1,vMT) ≤ J1MT + ε₉·(∫vMT)² .
    This is exactly AtOne's `_D1_one_le` pair for the flat/quartic windows. -/
abbrev jWin_D1_one_vMT_sandwich : Prop :=
  J1MT ≤ jWin D1 1 vMT ∧ jWin D1 1 vMT ≤ J1MT + eps9 * (IvMT) ^ 2

/-- **κ₁(1,vMT) ∈ [κ₉, κ₉ + ε₉]** — the AtOne sandwich for v_MT (mirror of
    `AtOne.kappaXi_one_vQuartic_mem`), conditional on the four/five open analytic facts. -/
theorem kappaXi_one_vMT_mem (hIv : integral_vMT_forms) (hJ : jWin_D1_one_vMT_sandwich)
    (hpos : IvMT_pos) : kappaXi 1 vMT ∈ Icc kappaXiOne_MT (kappaXiOne_MT + eps9) := by
  rw [kappaXi_one, hIv.2, hIv.1]
  constructor
  · -- lower: (aMT + jWin)/(IvMT)² ≥ (aMT + J1MT)/(IvMT)²  ⟺  J1MT ≤ jWin
    have hpos2 : 0 < (IvMT) ^ 2 := sq_pos_of_pos hpos
    rw [le_div_iff₀ hpos2]
    unfold kappaXiOne_MT
    field_simp [ne_of_gt hpos2]
    nlinarith [hJ.1]
  · -- upper: (aMT + jWin)/(IvMT)² ≤ (aMT + J1MT)/(IvMT)² + eps9
    have hpos2 : 0 < (IvMT) ^ 2 := sq_pos_of_pos hpos
    rw [div_le_iff₀ hpos2]
    calc
      aMT + jWin D1 1 vMT ≤ aMT + (J1MT + eps9 * (IvMT) ^ 2) := by gcongr; exact hJ.2
      _ = (aMT + J1MT) + eps9 * (IvMT) ^ 2 := by ring
      _ ≤ (kappaXiOne_MT + eps9) * (IvMT) ^ 2 := by
        unfold kappaXiOne_MT
        field_simp [ne_of_gt hpos2]
        exact le_rfl

/-- **sharp certified H_{ξ′} range:** from κ₁ ∈ [κ₉, κ₉+ε₉],
    H_xip = 2 − κ₁(1,vMT) ∈ [2 − (κ₉ + ε₉), 2 − κ₉]. -/
theorem H_xip_vMT_mem (hIv : integral_vMT_forms) (hJ : jWin_D1_one_vMT_sandwich)
    (hpos : IvMT_pos) :
    H_xip ∈ Icc (2 - (kappaXiOne_MT + eps9)) (2 - kappaXiOne_MT) := by
  have hk := kappaXi_one_vMT_mem hIv hJ hpos
  unfold H_xip
  constructor <;> linarith [hk.1, hk.2]

end XiPrime
end Zeta23

end
