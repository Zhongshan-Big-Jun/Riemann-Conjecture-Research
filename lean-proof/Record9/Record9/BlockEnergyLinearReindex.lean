/-
Record9.BlockEnergyLinearReindex — machine-checked linear reindexing lemma for T1c-2a.

This module proves the finite bookkeeping identity behind the linear part of the summed
F₈ windows: summing each of the 255 windows' 8 gaps equals summing over all 262 gaps with
the window-multiplicity weight `linearMultiplicity r`. It is a partial but machine-checked
step toward `f8WindowSum_eq_linear_add_pair` (the remaining finite-counting obligation in
`Record9.BlockEnergy`).

No sorry/admit/axiom; the snapshot `literature/raw/zeta-23-lean/` is untouched.
-/
import Record9.BlockEnergy

noncomputable section

open scoped BigOperators
open BigOperators Finset

namespace Zeta23
namespace ThmD

/-- Summing `g` over each window's 8 gaps equals summing over all gaps weighted by the
    number of windows containing that gap.  This is the linear reindexing identity used in
    `f8WindowSum_eq_linear_add_pair`. -/
lemma f8LinearReindex (g : Fin 262 → ℝ) :
    (∑ j : Fin 255, ∑ n : Fin 8, g ⟨j.1 + n.1, by omega⟩) =
      ∑ r : Fin 262, (linearMultiplicity r : ℝ) * g r := by
  classical
  -- step 1: per window, replace ∑_n g(j+n) with ∑_r (if windowContainsGap r j then g r else 0)
  have h1 : (∑ j : Fin 255, ∑ n : Fin 8, g ⟨j.1 + n.1, by omega⟩) =
      (∑ j : Fin 255, ∑ r : Fin 262, if windowContainsGap r j then g r else 0) := by
    apply Finset.sum_congr rfl
    intro j hj
    -- per-window: ∑_n g(j+n) = ∑_r (if windowContainsGap r j then g r else 0)
    rw [← Finset.sum_filter]
    symm
    let i : ∀ r ∈ (Finset.univ : Finset (Fin 262)).filter (fun r => windowContainsGap r j), Fin 8 :=
      fun r hr => ⟨r.1 - j.1, by
        have hmem : windowContainsGap r j := (Finset.mem_filter.mp hr).2
        have hle : j.1 ≤ r.1 := hmem.1
        have hb : r.1 ≤ j.1 + 7 := hmem.2
        omega⟩
    let k : ∀ n ∈ (Finset.univ : Finset (Fin 8)), Fin 262 := fun n _ => ⟨j.1 + n.1, by omega⟩
    refine (Finset.sum_bij' i k ?hi ?hj ?li ?ri ?h)
    · -- hi : i r hr ∈ univ Fin 8
      intro r hr
      exact Finset.mem_univ (i r hr)
    · -- hj : k n _ ∈ filtered set
      intro n hn
      exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, by
        simp [k, windowContainsGap]
        omega⟩
    · -- li : k (i r hr) (hi r hr) = r
      intro r hr
      apply Fin.ext
      simp [i, k]
      have hmem : windowContainsGap r j := (Finset.mem_filter.mp hr).2
      have hle : j.1 ≤ r.1 := hmem.1
      omega
    · -- ri : i (k n _) (hj n _) = n
      intro n hn
      apply Fin.ext
      simp [i, k]
    · -- h : g r = g ⟨j.1 + (r.1 - j.1), _⟩
      intro r hr
      apply congrArg g
      apply Fin.ext
      simp [i]
      exact (Nat.add_sub_of_le (show j.1 ≤ r.1 from (Finset.mem_filter.mp hr).2.1)).symm
      -- direction: r.1 = j.1 + (r.1 - j.1)
  -- step 2: swap the double sum
  have h2 : (∑ j : Fin 255, ∑ r : Fin 262, if windowContainsGap r j then g r else 0) =
      (∑ r : Fin 262, ∑ j : Fin 255, if windowContainsGap r j then g r else 0) :=
    Finset.sum_comm (s := (Finset.univ : Finset (Fin 255)))
      (t := (Finset.univ : Finset (Fin 262)))
      (f := fun j r => if windowContainsGap r j then g r else 0)
  -- step 3: for each r, ∑_j (if windowContainsGap r j then g r else 0) = (linearMultiplicity r : ℝ) * g r
  have h3 : (∑ r : Fin 262, ∑ j : Fin 255, if windowContainsGap r j then g r else 0) =
      ∑ r : Fin 262, (linearMultiplicity r : ℝ) * g r := by
    apply Finset.sum_congr rfl
    intro r hr
    rw [linearMultiplicity]
    rw [← Finset.sum_filter]
    rw [Finset.sum_const]
    rw [nsmul_eq_mul]
  -- assemble
  exact h1.trans (h2.trans h3)

end ThmD
end Zeta23
