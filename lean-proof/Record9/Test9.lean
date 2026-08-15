import Zeta23.ThmD.Mult

noncomputable section

open scoped BigOperators
open BigOperators Finset

def gapSpan (g : ℕ → ℝ) (i len : ℕ) : ℝ := (Finset.range len).sum (fun j => g (i + j))

def F8gaps (w : ℝ → ℝ) (g : ℕ → ℝ) : ℝ :=
  (1 / (500 * 8)) * ((Finset.range 8).sum g) +
    (Finset.range 8).sum (fun s0 =>
      ((2 : ℝ) / ((8 - s0 : ℕ) : ℝ)) * ((Finset.range (8 - s0)).sum (fun i => w (gapSpan g i (s0 + 1)))))

end
