/-
Record9.ZenodoAudit — formalization of two key structural lemmas from the preprint
Zenodo 22008814.

Lemma A (eq (4) curvature identity, real calculus).
Lemma B (conjugate-pair residue block characteristic polynomial and existence of a
strictly negative real eigenvalue, via a negative real root of the characteristic
polynomial).

The module is standalone (mathlib only).  No sorry/admit/axiom.
-/
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.Shift
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

noncomputable section

open scoped ContDiff
open Polynomial

namespace ZenodoAudit

/-! ## Lemma A: curvature identity -/

/-- The curvature identity (eq. (4) of the preprint).

With `g (a) = f (s + a) * f (s - a)`, for a twice continuously differentiable real
function `f`, the second derivative of `g` at `0` divided by two equals
`f''(s) * f(s) - (f'(s))^2`. -/
theorem curvature_identity (f : ℝ → ℝ) (s : ℝ) (hf : ContDiff ℝ 2 f) :
    let g : ℝ → ℝ := fun a => f (s + a) * f (s - a)
    1 / 2 * (deriv (fun a : ℝ => deriv g a) 0) =
      (deriv (fun t : ℝ => deriv f t) s) * f s - (deriv f s) ^ 2 := by
  intro g
  have hf' (x : ℝ) : HasDerivAt f (deriv f x) x :=
    (hf.differentiable (by norm_num : (2 : ℕ∞ω) ≠ 0)).differentiableAt.hasDerivAt
  have hf'' (x : ℝ) :
      HasDerivAt (fun t : ℝ => deriv f t) (deriv (fun t : ℝ => deriv f t) x) x :=
    (ContDiff.differentiable_deriv_two hf).differentiableAt.hasDerivAt
  have hleft (a : ℝ) :
      HasDerivAt (fun x : ℝ => f (s + x)) (deriv f (s + a)) a := by
    simpa [add_comm] using (hf' (a + s)).comp_add_const a s
  have hright (a : ℝ) :
      HasDerivAt (fun x : ℝ => f (s - x)) (-deriv f (s - a)) a := by
    simpa using (hf' (s - a)).comp_const_sub s a
  have hleft' (a : ℝ) :
      HasDerivAt (fun x : ℝ => deriv f (s + x))
        (deriv (fun t : ℝ => deriv f t) (s + a)) a := by
    simpa [add_comm] using (hf'' (a + s)).comp_add_const a s
  have hright' (a : ℝ) :
      HasDerivAt (fun x : ℝ => deriv f (s - x))
        (-deriv (fun t : ℝ => deriv f t) (s - a)) a := by
    simpa using (hf'' (s - a)).comp_const_sub s a
  have hg (a : ℝ) :
      HasDerivAt g (deriv f (s + a) * f (s - a) - f (s + a) * deriv f (s - a)) a := by
    change HasDerivAt (fun x : ℝ => f (s + x) * f (s - x))
      (deriv f (s + a) * f (s - a) - f (s + a) * deriv f (s - a)) a
    have hd : HasDerivAt (fun x : ℝ => f (s + x) * f (s - x))
        (deriv f (s + a) * f (s - a) + f (s + a) * (-deriv f (s - a))) a :=
      (hleft a).mul (hright a)
    simpa [sub_eq_add_neg] using hd
  have hderiv_g (a : ℝ) :
      deriv g a = deriv f (s + a) * f (s - a) - f (s + a) * deriv f (s - a) :=
    (hg a).deriv
  have hF (a : ℝ) :
      HasDerivAt
        (fun x : ℝ =>
          deriv f (s + x) * f (s - x) - f (s + x) * deriv f (s - x))
        (deriv (fun t : ℝ => deriv f t) (s + a) * f (s - a)
          + deriv f (s + a) * (-deriv f (s - a))
          - (deriv f (s + a) * deriv f (s - a)
            + f (s + a) * (-deriv (fun t : ℝ => deriv f t) (s - a)))) a := by
    have hp1 : HasDerivAt (fun x : ℝ => deriv f (s + x) * f (s - x))
        (deriv (fun t : ℝ => deriv f t) (s + a) * f (s - a)
          + deriv f (s + a) * (-deriv f (s - a))) a :=
      (hleft' a).mul (hright a)
    have hp2 : HasDerivAt (fun x : ℝ => f (s + x) * deriv f (s - x))
        (deriv f (s + a) * deriv f (s - a)
          + f (s + a) * (-deriv (fun t : ℝ => deriv f t) (s - a))) a :=
      (hleft a).mul (hright' a)
    exact hp1.sub hp2
  have hsecond :
      HasDerivAt (fun a : ℝ => deriv g a)
        (2 * deriv (fun t : ℝ => deriv f t) s * f s - 2 * (deriv f s) ^ 2) 0 := by
    convert hF 0 using 1
    · ext a
      exact hderiv_g a
    · ring_nf
  have hderivg0 :
      deriv (fun a : ℝ => deriv g a) 0 =
        2 * deriv (fun t : ℝ => deriv f t) s * f s - 2 * (deriv f s) ^ 2 :=
    hsecond.deriv
  rw [hderivg0]
  ring_nf

/-! ## Lemma B: conjugate-pair residue block -/

/-- The real symmetric conjugate-pair block `[0, w; w, 0]`. -/
def conjugatePairBlock (w : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![0, w; w, 0]

/-- The characteristic polynomial of the conjugate-pair block is `X² - w²`. -/
theorem conjugate_pair_block_charpoly (w : ℝ) :
    (conjugatePairBlock w).charpoly = Polynomial.X ^ 2 - Polynomial.C (w ^ 2) := by
  unfold conjugatePairBlock Matrix.charpoly Matrix.charmatrix
  simp [Matrix.diagonal]
  have hmat :
      ((Matrix.of fun i j => if i = j then (X : ℝ[X]) else 0) -
        (!![0, w; w, 0] : Matrix (Fin 2) (Fin 2) ℝ).map Polynomial.C) =
      (!![X, -Polynomial.C w; -Polynomial.C w, X] : Matrix (Fin 2) (Fin 2) ℝ[X]) := by
    ext i j <;> fin_cases i <;> fin_cases j <;> simp [Matrix.sub_apply]
  rw [hmat, Matrix.det_fin_two_of]
  ring_nf

/-- For `w ≠ 0`, the conjugate-pair block has a strictly negative real eigenvalue.

This is stated through the characteristic-polynomial proxy: the polynomial has a real
root `< 0`.  Since the matrix is symmetric and `2 × 2`, every real root of the
characteristic polynomial is an eigenvalue; the intended meaning is exactly
"the conjugate-pair residue block has one negative eigenvalue". -/
theorem conjugate_pair_block_has_negative_eigenvalue (w : ℝ) (hw : w ≠ 0) :
    ∃ x : ℝ, Polynomial.eval x (conjugatePairBlock w).charpoly = 0 ∧ x < 0 := by
  refine ⟨-|w|, ?_, ?_⟩
  · rw [conjugate_pair_block_charpoly]
    simp [pow_two]
  · have hpos : 0 < |w| := abs_pos.mpr hw
    linarith

end ZenodoAudit

