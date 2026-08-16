/-
Record9.BlockEnergyDecomp — T1c-2a: the summed-F₈ decomposition into linear + pair parts.
-/
import Record9.BlockEnergyLinearReindex

noncomputable section

open scoped BigOperators
open BigOperators Finset

namespace Zeta23
namespace ThmD

set_option maxHeartbeats 1000000

/-- Expand a single window into its F₈ gaps form. -/
lemma f8Window_eq (g : Fin 262 → ℝ) (j : Fin 255) :
    f8Window g j = F8gaps wMT (fun n : ℕ => g ⟨j.1 + n % 8, by omega⟩) := by
  unfold f8Window F8
  rfl

/-- For the windows' indices the modulus `% 8` is the identity, so the summed linear term
    over one window equals the sum over `Fin 8`. -/
lemma f8Linear_window_eq (g : Fin 262 → ℝ) (j : Fin 255) :
    (Finset.range 8).sum (fun n : ℕ => g ⟨j.1 + n % 8, by omega⟩) =
      ∑ n : Fin 8, g ⟨j.1 + n.1, by omega⟩ := by
  rw [Finset.sum_range]
  apply Finset.sum_congr rfl
  intro x hx
  apply congrArg g
  apply Fin.ext
  simp [Nat.mod_eq_of_lt x.isLt]

/-- The linear aggregation over all windows (used to connect to `f8LinearPart`). -/
lemma f8Linear_reindex_sum (g : Fin 262 → ℝ) :
    (∑ j : Fin 255, (Finset.range 8).sum (fun n : ℕ => g ⟨j.1 + n % 8, by omega⟩)) =
      ∑ r : Fin 262, (linearMultiplicity r : ℝ) * g r := by
  classical
  rw [← f8LinearReindex g]
  apply Finset.sum_congr rfl
  intro j hj
  exact f8Linear_window_eq g j

/-- For the admissible index range, `(i + q) % 8 = i + q` and `((j.1 + i) + q) % 262 =
    (j.1 + i) + q` as natural numbers. -/
lemma pair_gap_nat (j : Fin 255) {s0 i q : ℕ}
    (hs0 : s0 < 8) (hi : i < 8 - s0) (hq : q < s0 + 1) :
    j.1 + ((i + q) % 8) = ((j.1 + i) + q) % 262 := by
  have hlt8 : i + q < 8 := by omega
  have hlt262 : (j.1 + i) + q < 262 := by omega
  rw [Nat.mod_eq_of_lt hlt8]
  rw [Nat.mod_eq_of_lt hlt262]
  omega

/-- The pointwise gap identity behind the pair part: inside the admissible index range the
    mod-8 lift and the mod-262 `gapAt` agree exactly. -/
lemma pair_gap_pointwise (g : Fin 262 → ℝ) {j : Fin 255} {s0 i q : ℕ}
    (hs0 : s0 < 8) (hi : i < 8 - s0) (hq : q < s0 + 1) :
    g ⟨j.1 + ((i + q) % 8), by omega⟩ = g ⟨((j.1 + i) + q) % 262, by omega⟩ := by
  congr 1
  apply Fin.ext
  exact pair_gap_nat j hs0 hi hq

/-- The pair summand identity: the F₈-window `gapSpan` over the mod-8 lift equals the
    `gapAt`-based `gapSpan` at each admissible `(j, s0, i)`. -/
lemma pair_gapSpan_eq (g : Fin 262 → ℝ) {j : Fin 255} {s0 : ℕ}
    (hs0 : s0 < 8) (i : ℕ) (hi : i < 8 - s0) :
    gapSpan (fun n : ℕ => g ⟨j.1 + n % 8, by omega⟩) i (s0 + 1) =
      gapSpan (gapAt g) (j.1 + i) (s0 + 1) := by
  unfold gapSpan gapAt
  apply Finset.sum_congr rfl
  intro q hq
  change g ⟨j.1 + ((i + q) % 8), by omega⟩ = g ⟨((j.1 + i) + q) % 262, by omega⟩
  congr 1
  apply Fin.ext
  exact pair_gap_nat j hs0 hi (Finset.mem_range.mp hq)

theorem f8WindowSum_eq_linear_add_pair_fact (g : Fin 262 → ℝ) :
    f8WindowSum g = f8LinearPart g + f8PairPart g := by
  classical
  calc
    f8WindowSum g
        = ∑ j : Fin 255, F8gaps wMT (fun n : ℕ => g ⟨j.1 + n % 8, by omega⟩) := by
          rw [f8WindowSum]
          apply Finset.sum_congr rfl
          intro j hj
          exact f8Window_eq g j
    _ = (1 / (500 * 8 : ℝ)) *
            (∑ j : Fin 255, (Finset.range 8).sum (fun n : ℕ => g ⟨j.1 + n % 8, by omega⟩)) +
          ∑ j : Fin 255,
            (Finset.range 8).sum (fun s0 =>
              ((2 : ℝ) / ((8 - s0 : ℕ) : ℝ)) *
                ((Finset.range (8 - s0)).sum (fun i =>
                  wMT (gapSpan (fun n : ℕ => g ⟨j.1 + n % 8, by omega⟩) i (s0 + 1))))) := by
          simp only [F8gaps]
          rw [Finset.sum_add_distrib]
          rw [← Finset.mul_sum]
    _ = f8LinearPart g + f8PairPart g := by
          have hlin : (1 / (500 * 8 : ℝ)) *
              (∑ j : Fin 255, (Finset.range 8).sum (fun n : ℕ => g ⟨j.1 + n % 8, by omega⟩)) =
                f8LinearPart g := by
            unfold f8LinearPart
            rw [f8Linear_reindex_sum g]
          have hpair : (∑ j : Fin 255,
              (Finset.range 8).sum (fun s0 =>
                ((2 : ℝ) / ((8 - s0 : ℕ) : ℝ)) *
                  ((Finset.range (8 - s0)).sum (fun i =>
                    wMT (gapSpan (fun n : ℕ => g ⟨j.1 + n % 8, by omega⟩) i (s0 + 1)))))) =
                f8PairPart g := by
            unfold f8PairPart
            apply Finset.sum_congr rfl
            intro j hj
            apply Finset.sum_congr rfl
            intro s0 hs0
            congr 1
            apply Finset.sum_congr rfl
            intro i hi
            congr 1
            exact pair_gapSpan_eq g (Finset.mem_range.mp hs0) i (Finset.mem_range.mp hi)
          rw [hlin, hpair]

end ThmD
end Zeta23
