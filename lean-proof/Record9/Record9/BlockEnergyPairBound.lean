/-
Record9.BlockEnergyPairBound — T1c-2a: the pair-part is bounded by the block energy.

This module proves the second (final) T1c-2a finite-counting obligation:
    `f8PairPart g ≤ blockEnergy g`
for every 262-gap vector `g : Fin 262 → ℝ` (nonnegativity of `g` is not actually
needed for the pair bound: the bound is a pure coefficient-counting argument using
`wMT_nonneg`, which holds for every input).

The proof route:
  1. Unfold `f8PairPart` and `blockEnergy`.
  2. Each `f8PairPart` summand indexed by `(j, s0, i)` (window `j`, separation
     `s = s0+1`, offset `i < 9-s`) corresponds to the unordered point pair
     `(a, b) = (j+i, j+i+s)`.  `pair_gapSpan_eq` (in `Record9.BlockEnergyDecomp`)
     rewrites the `gapSpan (gapAt g) (j+i) s` in the summand into
     `gapSpan (gapAt g) (j+i) (b.1 - a.1)` — i.e. `pointDist g a b`.
  3. For a fixed pair `(a,b)`, `a.1 < b.1`, with separation `s = b.1-a.1`, the
     occurrences `(j, s0, i)` mapping to it are exactly the windows `j` satisfying
     `windowContainsPair a b j` (with `s0 = s-1`, `i = a.1-j.1`).  Their number is
     `pairMultiplicity a b ≤ 9 - s` (`pairMultiplicity_le`), and it is `0` for
     `s ≥ 9` (`windowContainsPair_requires_sep_le_eight`).
  4. Reindex the triple sum over occurrences by the pair they map to; the total
     coefficient on `wMT(pointDist g a b)` is
     `pairMultiplicity a b · (2/(9-s)) ≤ (9-s) · (2/(9-s)) = 2`
     (`pairCoeff_mul_windows`).  For `s ≥ 9` the contribution is `0`, while
     `blockEnergy` contains the nonnegative term `2·wMT(pointDist g a b)`
     (`wMT_nonneg`).
  5. Assemble with `Finset.sum_le_sum` / `Finset.sum_bij` and
     `linarith`/`ring`/`field_simp` for the coefficient arithmetic.

No sorry/admit/axiom; the snapshot `literature/raw/zeta-23-lean/` is untouched.
-/
import Record9.BlockEnergyDecomp

noncomputable section

open scoped BigOperators
open BigOperators Finset

namespace Zeta23
namespace ThmD

set_option maxHeartbeats 1000000
set_option maxRecDepth 10000

/-- the number of windows (out of `j = 0..254`) that contain the unordered point pair
    `(a,b)` — i.e. the occurrence-multiplicity of that pair inside `f8PairPart`. -/
noncomputable def pairMultiplicity (a b : Fin 263) : ℕ := by
  classical
  exact (Finset.univ.filter (fun j : Fin 255 => windowContainsPair a b j)).card

/-- each unordered point pair with separation `s = b−a` (1 ≤ s ≤ 8) lies in at most
    `9−s` windows.  The injective witness sends a containing window `j` to the offset
    `a − j ∈ Fin (9−s)`. -/
lemma pairMultiplicity_le (a b : Fin 263) (hab : a.1 < b.1) :
    pairMultiplicity a b ≤ 9 - (b.1 - a.1) := by
  classical
  unfold pairMultiplicity
  -- define the injection into Fin (9 - (b.1 - a.1)):  j ↦ a.1 − j.1
  let f : {j : Fin 255 // windowContainsPair a b j} → Fin (9 - (b.1 - a.1)) := fun j =>
    ⟨a.1 - j.1.1, by
      have hj : windowContainsPair a b j := j.2
      have hlej : j.1.1 ≤ a.1 := hj.1
      have hb : b.1 ≤ j.1.1 + 8 := hj.2
      omega⟩
  have hf : Function.Injective f := by
    intro j₁ j₂ h
    apply Subtype.ext
    apply Fin.ext
    have hh := congrArg (fun x : Fin (9 - (b.1 - a.1)) => (x : ℕ)) h
    simp [f] at hh
    have h₁ : j₁.1.1 ≤ a.1 := j₁.2.1
    have h₂ : j₂.1.1 ≤ a.1 := j₂.2.1
    omega
  have hcard : (Finset.univ.filter (fun j : Fin 255 => windowContainsPair a b j)).card
      ≤ Fintype.card {j : Fin 255 // windowContainsPair a b j} := by
    exact (Fintype.card_subtype (fun j : Fin 255 => windowContainsPair a b j)).ge
  have hcard8 : Fintype.card {j : Fin 255 // windowContainsPair a b j} ≤ 9 - (b.1 - a.1) := by
    rw [← Fintype.card_fin (9 - (b.1 - a.1))]
    exact Fintype.card_le_of_injective f hf
  exact le_trans hcard hcard8

/-- the flattened occurrence finset: `occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ` with
    `occ.1 : Fin 255` the window, `occ.2.1 : ℕ = s0 < 8` and `occ.2.2 : ℕ = i < 8 − s0`. -/
def occFinset : Finset (Σ j : Fin 255, Σ s0 : ℕ, ℕ) :=
  (Finset.univ : Finset (Fin 255)).sigma (fun _ => (Finset.range 8).sigma (fun s0 => Finset.range (8 - s0)))

/-- the summand of `f8PairPart` at a single occurrence `(j, s0, i)`. -/
def occSummand (g : Fin 262 → ℝ) (occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ) : ℝ :=
  ((2 : ℝ) / ((8 - occ.2.1 : ℕ) : ℝ)) *
    wMT (gapSpan (gapAt g) (occ.1.1 + occ.2.2) (occ.2.1 + 1))

/-- a pair-occurrence: an unordered pair `(a,b)` (with `a.1 < b.1`) together with a window
    `j` containing it.  `po.1.1.1 = a`, `po.1.1.2 = b`, `po.1.2 = j`. -/
def PairOcc : Type := {q : (Fin 263 × Fin 263) × Fin 255 //
  q.1.1.1 < q.1.2.1 ∧ windowContainsPair q.1.1 q.1.2 q.2}

instance : Fintype PairOcc := by
  classical
  unfold PairOcc
  refine Fintype.ofFinite (α := {q : (Fin 263 × Fin 263) × Fin 255 //
    q.1.1.1 < q.1.2.1 ∧ windowContainsPair q.1.1 q.1.2 q.2})

instance : DecidableEq PairOcc := by
  classical
  unfold PairOcc
  infer_instance

/-- the summand over a pair-occurrence: coefficient `2/(9−s)` with `s = b.1−a.1`, times
    `wMT` of the pair's distance.  Here `po.1.1.1 = a`, `po.1.1.2 = b`, `po.1.2 = j`. -/
def pairSummand (g : Fin 262 → ℝ) (po : PairOcc) : ℝ :=
  ((2 : ℝ) / ((9 - (po.1.1.2.1 - po.1.1.1.1) : ℕ) : ℝ)) * wMT (pointDist g po.1.1.1 po.1.1.2)

/-- `f8PairPart g` equals the sum of `occSummand` over `occFinset`. -/
lemma f8PairPart_eq_occSum (g : Fin 262 → ℝ) :
    f8PairPart g = (occFinset.sum fun occ => occSummand g occ) := by
  classical
  unfold f8PairPart occFinset occSummand
  rw [Finset.sum_sigma]
  apply Finset.sum_congr rfl
  intro j hj
  rw [Finset.sum_sigma]
  apply Finset.sum_congr rfl
  intro s0 hs0
  simp [Finset.mul_sum]

/-- an occurrence in `occFinset` has `s0 < 8`. -/
lemma occ_mem_s0_lt {occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ} (h : occ ∈ occFinset) :
    occ.2.1 < 8 := by
  simp [occFinset] at h
  omega

/-- an occurrence in `occFinset` has `i < 8 − s0`. -/
lemma occ_mem_i_lt {occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ} (h : occ ∈ occFinset) :
    occ.2.2 < 8 - occ.2.1 := by
  simp [occFinset] at h
  omega

/-- the left endpoint of an occurrence's pair fits in `Fin 263`. -/
lemma occ_fin_a {occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ} (h : occ ∈ occFinset) :
    occ.1.1 + occ.2.2 < 263 := by
  have hs := occ_mem_s0_lt h
  have hi := occ_mem_i_lt h
  omega

/-- the right endpoint of an occurrence's pair fits in `Fin 263`. -/
lemma occ_fin_b {occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ} (h : occ ∈ occFinset) :
    occ.1.1 + occ.2.2 + occ.2.1 + 1 < 263 := by
  have hs := occ_mem_s0_lt h
  have hi := occ_mem_i_lt h
  omega

/-- for an occurrence in `occFinset`, `i + s0 + 1 ≤ 8`. -/
lemma occ_i_add_s0_le_eight {occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ} (h : occ ∈ occFinset) :
    occ.2.2 + occ.2.1 + 1 ≤ 8 := by
  have hi := occ_mem_i_lt h
  omega

/-- the endpoints of an occurrence's pair are ordered. -/
lemma occ_pair_lt {occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ} (h : occ ∈ occFinset) :
    occ.1.1 + occ.2.2 < occ.1.1 + occ.2.2 + occ.2.1 + 1 := by
  exact Nat.lt_add_of_pos_right (Nat.succ_pos occ.2.1)

/-- the window `occ.1` contains the pair of the occurrence. -/
lemma occ_pair_contains {occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ} (h : occ ∈ occFinset) :
    windowContainsPair (⟨occ.1.1 + occ.2.2, occ_fin_a h⟩) (⟨occ.1.1 + occ.2.2 + occ.2.1 + 1, occ_fin_b h⟩)
      occ.1 := by
  constructor
  · exact Nat.le_add_right occ.1.1 occ.2.2
  · have h' := occ_i_add_s0_le_eight h
    simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using (Nat.add_le_add_right h' occ.1.1)

/-- the forward map: an occurrence `(j, s0, i)` maps to the pair `(j+i, j+i+s0+1)` in the
    window `j`. -/
def occToPair (occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ) (h : occ ∈ occFinset) : PairOcc :=
  ⟨(((⟨occ.1.1 + occ.2.2, occ_fin_a h⟩ : Fin 263),
      (⟨occ.1.1 + occ.2.2 + occ.2.1 + 1, occ_fin_b h⟩ : Fin 263)), occ.1),
    ⟨occ_pair_lt h, occ_pair_contains h⟩⟩

/-- the backward map: a pair-occurrence `((a,b),j)` maps back to the occurrence
    `(j, b−a−1, a−j)`, which lies in `occFinset` and is the inverse of `occToPair`. -/
def pairToOcc (po : PairOcc) : Σ j : Fin 255, Σ s0 : ℕ, ℕ :=
  ⟨po.1.2, ⟨po.1.1.2.1 - po.1.1.1.1 - 1, po.1.1.1.1 - po.1.2.1⟩⟩

/-- for a pair-occurrence, `s0 = b−a−1 < 8`. -/
lemma pairToOcc_s0_lt (po : PairOcc) : po.1.1.2.1 - po.1.1.1.1 - 1 < 8 := by
  have hab : po.1.1.1.1 < po.1.1.2.1 := po.2.1
  have hw : windowContainsPair po.1.1.1 po.1.1.2 po.1.2 := po.2.2
  have hse := windowContainsPair_imp_sep_le_eight hab hw
  omega

/-- for a pair-occurrence, `i = a−j < 8 − s0`. -/
lemma pairToOcc_i_lt (po : PairOcc) :
    po.1.1.1.1 - po.1.2.1 < 8 - (po.1.1.2.1 - po.1.1.1.1 - 1) := by
  have hab : po.1.1.1.1 < po.1.1.2.1 := po.2.1
  have hw : windowContainsPair po.1.1.1 po.1.1.2 po.1.2 := po.2.2
  have hlej : po.1.2.1 ≤ po.1.1.1.1 := hw.1
  have hb : po.1.1.2.1 ≤ po.1.2.1 + 8 := hw.2
  have hse : po.1.1.2.1 - po.1.1.1.1 ≤ 8 := windowContainsPair_imp_sep_le_eight hab hw
  omega

/-- `pairToOcc po` is a valid occurrence. -/
lemma pairToOcc_mem (po : PairOcc) : pairToOcc po ∈ occFinset := by
  classical
  rw [occFinset]
  rw [Finset.mem_sigma]
  constructor
  · exact Finset.mem_univ _
  · rw [Finset.mem_sigma]
    constructor
    · rw [Finset.mem_range]
      exact pairToOcc_s0_lt po
    · rw [Finset.mem_range]
      exact pairToOcc_i_lt po

/-- the round-trip `pairToOcc (occToPair occ h) = occ`. -/
lemma pairToOcc_occToPair (occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ) (h : occ ∈ occFinset) :
    pairToOcc (occToPair occ h) = occ := by
  classical
  have h1 : occ.1.1 + occ.2.2 + occ.2.1 + 1 - (occ.1.1 + occ.2.2) - 1 = occ.2.1 := by omega
  have h2 : occ.1.1 + occ.2.2 - occ.1.1 = occ.2.2 := by omega
  simp [pairToOcc, occToPair, h1, h2]

/-- the round-trip `occToPair (pairToOcc po) h = po`. -/
lemma occToPair_pairToOcc (po : PairOcc) (h : pairToOcc po ∈ occFinset) :
    occToPair (pairToOcc po) h = po := by
  classical
  rcases po with ⟨q, hq⟩
  rcases q with ⟨p, j⟩
  rcases p with ⟨pa, pb⟩
  apply Subtype.ext
  -- after rcases, pa pb : Fin 263, j : Fin 255
  -- bounds: hq : pa.1 < pb.1 ∧ windowContainsPair pa pb j
  have hlej : j.1 ≤ pa.1 := hq.2.1
  have hab : pa.1 < pb.1 := hq.1
  have hs0 : 1 ≤ pb.1 - pa.1 := by omega
  simp [pairToOcc, occToPair]
  constructor
  · apply Fin.ext
    simp [pairToOcc]
    exact Nat.add_sub_of_le hlej
  · apply Fin.ext
    simp [pairToOcc]
    omega

/-- the summand of `f8PairPart` at an occurrence equals the `pairSummand` of the pair that
    occurrence maps to. -/
lemma occSummand_eq_pairSummand (g : Fin 262 → ℝ)
    {occ : Σ j : Fin 255, Σ s0 : ℕ, ℕ} (h : occ ∈ occFinset) :
    occSummand g occ = pairSummand g (occToPair occ h) := by
  classical
  unfold occSummand pairSummand occToPair
  have hs : occ.2.1 < 8 := occ_mem_s0_lt h
  have hsep : occ.1.1 + occ.2.2 + occ.2.1 + 1 - (occ.1.1 + occ.2.2) = occ.2.1 + 1 := by
    rw [show occ.1.1 + occ.2.2 + occ.2.1 + 1 = (occ.1.1 + occ.2.2) + (occ.2.1 + 1) by ac_rfl]
    omega
  have hden : (8 - occ.2.1 : ℕ) = (9 - (occ.1.1 + occ.2.2 + occ.2.1 + 1 - (occ.1.1 + occ.2.2)) : ℕ) := by
    rw [hsep]
    omega
  have hcoef : ((2 : ℝ) / ((8 - occ.2.1 : ℕ) : ℝ)) =
      ((2 : ℝ) / ((9 - (occ.1.1 + occ.2.2 + occ.2.1 + 1 - (occ.1.1 + occ.2.2)) : ℕ) : ℝ)) := by
    rw [hden]
  have hk : wMT (gapSpan (gapAt g) (occ.1.1 + occ.2.2) (occ.2.1 + 1)) =
      wMT (pointDist g (⟨occ.1.1 + occ.2.2, occ_fin_a h⟩)
        (⟨occ.1.1 + occ.2.2 + occ.2.1 + 1, occ_fin_b h⟩)) := by
    congr 1
    unfold pointDist
    simp [hsep]
  rw [hcoef, hk]

/-- `f8PairPart g` re-indexed as a sum of `pairSummand` over all pair-occurrences. -/
lemma f8PairPart_eq_pairSum (g : Fin 262 → ℝ) :
    f8PairPart g = (Finset.univ : Finset PairOcc).sum (fun po => pairSummand g po) := by
  classical
  rw [f8PairPart_eq_occSum g]
  -- re-index the sum over occFinset to the sum over PairOcc
  refine Finset.sum_bij' (i := fun occ h => occToPair occ h) (j := fun po _ => pairToOcc po)
    ?hi ?hj ?li ?ri ?h
  · intro occ h
    exact Finset.mem_univ (occToPair occ h)
  · intro po h
    exact pairToOcc_mem po
  · intro occ h
    exact pairToOcc_occToPair occ h
  · intro po hp
    exact occToPair_pairToOcc po (pairToOcc_mem po)
  · intro occ h
    exact occSummand_eq_pairSummand g h

/-- the unordered pair `(a,b)` of a pair-occurrence. -/
def pairKey (po : PairOcc) : Fin 263 × Fin 263 := (po.1.1.1, po.1.1.2)

/-- the pair of a pair-occurrence satisfies `a.1 < b.1` and is separated by ≤ 8. -/
lemma pairKey_prop (po : PairOcc) : po.1.1.1.1 < po.1.1.2.1 ∧ po.1.1.2.1 - po.1.1.1.1 ≤ 8 :=
  ⟨po.2.1, windowContainsPair_imp_sep_le_eight po.2.1 po.2.2⟩

/-- `pairSummand g po` for a pair-occurrence with pair `(a,b)`: coefficient `2/(9−s)`. -/
lemma pairSummand_eq_of_key (g : Fin 262 → ℝ) {po : PairOcc} {a b : Fin 263}
    (hk : pairKey po = (a, b)) :
    pairSummand g po = ((2 : ℝ) / ((9 - (b.1 - a.1) : ℕ) : ℝ)) * wMT (pointDist g a b) := by
  rcases hk with ⟨rfl, rfl⟩
  simp [pairSummand]

/-- the number of pair-occurrences with a given (ordered) pair equals `pairMultiplicity`. -/
lemma pairFiber_card (a b : Fin 263) (hab : a.1 < b.1) :
    ((Finset.univ : Finset PairOcc).filter (fun po => pairKey po = (a, b))).card = pairMultiplicity a b := by
  classical
  -- bijection between {po : PairOcc | pairKey po = (a,b)} and {j : Fin 255 | windowContainsPair a b j}
  let f : {po : PairOcc // pairKey po = (a, b)} → {j : Fin 255 // windowContainsPair a b j} := fun po =>
    ⟨po.1.1.2, by
      rcases po with ⟨ppo, hk⟩
      rcases ppo with ⟨r, hprop⟩
      rcases r with ⟨p, jj⟩
      rcases p with ⟨pa, pb⟩
      rcases hprop with ⟨hlt, hw⟩
      simp [pairKey] at hk
      rcases hk with ⟨ha, hb⟩
      subst pa; subst pb
      exact hw⟩
  let g : {j : Fin 255 // windowContainsPair a b j} → {po : PairOcc // pairKey po = (a, b)} := fun j =>
    ⟨⟨(((a, b), j.1)), ⟨hab, j.2⟩⟩, by simp [pairKey]⟩
  -- cardinalities: filter card = card of {po // key = (a,b)} = card of {j // windowContainsPair a b j}
  have hc1 : ((Finset.univ : Finset PairOcc).filter (fun po => pairKey po = (a, b))).card
      = Fintype.card {po : PairOcc // pairKey po = (a, b)} := by
    rw [Fintype.card_subtype]
  have hc2 : Fintype.card {po : PairOcc // pairKey po = (a, b)} = Fintype.card {j : Fin 255 // windowContainsPair a b j} := by
    apply Fintype.card_congr
    refine ⟨f, g, ?_, ?_⟩
    · intro po
      -- g (f po) = po
      rcases po with ⟨ppo, hk⟩
      rcases ppo with ⟨r, hprop⟩
      rcases r with ⟨p, jj⟩
      rcases p with ⟨pa, pb⟩
      rcases hprop with ⟨hlt, hw⟩
      apply Subtype.ext
      apply Subtype.ext
      simp [f, g, pairKey] at hk ⊢
      rcases hk with ⟨ha, hb⟩
      subst pa; subst pb
      simp [f, g]
    · intro jj
      apply Subtype.ext
      simp [f, g]
  have hc3 : Fintype.card {j : Fin 255 // windowContainsPair a b j} = pairMultiplicity a b := by
    rw [pairMultiplicity]
    rw [Fintype.card_subtype]
  rw [hc1, hc2, hc3]

/-- if a pair has separation > 8, its multiplicity is 0. -/
lemma pairMultiplicity_eq_zero_of_gt_eight (a b : Fin 263) (h : 8 < b.1 - a.1) :
    pairMultiplicity a b = 0 := by
  unfold pairMultiplicity
  rw [Finset.card_eq_zero]
  ext j
  simp [windowContainsPair_requires_sep_le_eight (a := a) (b := b) h]

/-- the sum of `pairSummand` over all pair-occurrences with a given pair `(a,b)` equals
    `m · (2/(9−s)) · wMT(dist)` for `a.1 < b.1`. -/
lemma pairFiber_sum (g : Fin 262 → ℝ) (a b : Fin 263) (hab : a.1 < b.1) :
    (Finset.univ : Finset PairOcc).sum (fun po =>
        if pairKey po = (a, b) then pairSummand g po else 0)
      = (pairMultiplicity a b : ℝ) * ((2 : ℝ) / ((9 - (b.1 - a.1) : ℕ) : ℝ)) * wMT (pointDist g a b) := by
  classical
  let c : ℝ := ((2 : ℝ) / ((9 - (b.1 - a.1) : ℕ) : ℝ)) * wMT (pointDist g a b)
  have hterm : ∀ po : PairOcc,
      (if pairKey po = (a, b) then pairSummand g po else 0) =
        (if pairKey po = (a, b) then (1 : ℝ) else 0) * c := by
    intro po
    by_cases h : pairKey po = (a, b)
    · rw [if_pos h, if_pos h]
      have hp := pairSummand_eq_of_key g h
      simp [c, hp]
    · rw [if_neg h, if_neg h]
      simp [c]
  calc
    (∑ po, if pairKey po = (a, b) then pairSummand g po else 0)
        = ∑ po, (if pairKey po = (a, b) then (1 : ℝ) else 0) * c := by
            apply Finset.sum_congr rfl
            intro po hpo
            exact hterm po
    _ = (∑ po, if pairKey po = (a, b) then (1 : ℝ) else 0) * c := by rw [Finset.sum_mul]
    _ = ((∑ po, if pairKey po = (a, b) then (1 : ℝ) else 0) : ℝ) * c := rfl
    _ = ((pairMultiplicity a b : ℝ)) * c := by
            have hcard : (∑ po, if pairKey po = (a, b) then (1 : ℝ) else 0) = (pairMultiplicity a b : ℝ) := by
              rw [← Finset.sum_filter]
              simp [pairMultiplicity, pairFiber_card a b hab]
            rw [hcard]
    _ = (pairMultiplicity a b : ℝ) * ((2 : ℝ) / ((9 - (b.1 - a.1) : ℕ) : ℝ)) * wMT (pointDist g a b) := by
            simp [c, mul_assoc]

/-- the (possibly empty, for `a.1 ≥ b.1`) fiber sum is bounded by the corresponding
    `2·wMT(dist)` block-energy term. -/
lemma pairFiber_sum_le (g : Fin 262 → ℝ) (a b : Fin 263) :
    (Finset.univ : Finset PairOcc).sum (fun po =>
        if pairKey po = (a, b) then pairSummand g po else 0)
      ≤ if a.1 < b.1 then 2 * wMT (pointDist g a b) else 0 := by
  classical
  by_cases hab : a.1 < b.1
  · rw [if_pos hab]
    rw [pairFiber_sum g a b hab]
    by_cases hsep8 : b.1 - a.1 ≤ 8
    · have h1 : 1 ≤ b.1 - a.1 := by omega
      have hm : (pairMultiplicity a b : ℝ) ≤ ((9 - (b.1 - a.1) : ℕ) : ℝ) := by
        exact_mod_cast pairMultiplicity_le a b hab
      have hwn : 0 ≤ wMT (pointDist g a b) := wMT_nonneg _
      have hcoef : 0 ≤ ((2 : ℝ) / ((9 - (b.1 - a.1) : ℕ) : ℝ)) := by positivity
      have hmul0 := mul_le_mul_of_nonneg_right hm hcoef
      have hmul := mul_le_mul_of_nonneg_right hmul0 hwn
      have hne : (9 - (b.1 - a.1) : ℕ) ≠ 0 := by omega
      have heq : ((9 - (b.1 - a.1) : ℕ) : ℝ) * ((2 : ℝ) / ((9 - (b.1 - a.1) : ℕ) : ℝ)) * wMT (pointDist g a b)
          = 2 * wMT (pointDist g a b) := by
        field_simp [hne]
      calc
        (pairMultiplicity a b : ℝ) * ((2 : ℝ) / ((9 - (b.1 - a.1) : ℕ) : ℝ)) * wMT (pointDist g a b)
            ≤ ((9 - (b.1 - a.1) : ℕ) : ℝ) * ((2 : ℝ) / ((9 - (b.1 - a.1) : ℕ) : ℝ)) * wMT (pointDist g a b) := hmul
        _ = 2 * wMT (pointDist g a b) := heq
    · have hgt : 8 < b.1 - a.1 := by omega
      have hm0 : pairMultiplicity a b = 0 := pairMultiplicity_eq_zero_of_gt_eight a b hgt
      rw [hm0]
      norm_num
      nlinarith [wMT_nonneg (pointDist g a b)]
  · rw [if_neg hab]
    have hno : ∀ po : PairOcc, pairKey po ≠ (a, b) := by
      intro po hk
      have ha : po.1.1.1 = a := congrArg Prod.fst hk
      have hb : po.1.1.2 = b := congrArg Prod.snd hk
      have hp : po.1.1.1.1 < po.1.1.2.1 := po.2.1
      rw [ha, hb] at hp
      exact absurd hp hab
    have hsum : (∑ po, if pairKey po = (a, b) then pairSummand g po else 0) = 0 := by
      apply Finset.sum_eq_zero
      intro po hpo
      have hne : pairKey po ≠ (a, b) := hno po
      simp [hne]
    rw [hsum]

/-- regrouping `f8PairPart` over all pairs. -/
lemma f8PairPart_eq_pairFiberSum (g : Fin 262 → ℝ) :
    f8PairPart g =
      ∑ ab : Fin 263 × Fin 263,
        (Finset.univ : Finset PairOcc).sum (fun po => if pairKey po = ab then pairSummand g po else 0) := by
  classical
  rw [f8PairPart_eq_pairSum g]
  calc
    (∑ po : PairOcc, pairSummand g po)
        = ∑ po : PairOcc, ∑ ab : Fin 263 × Fin 263,
            if ab = pairKey po then pairSummand g po else 0 := by
            apply Finset.sum_congr rfl
            intro po hpo
            simp [Finset.sum_ite_eq]
    _ = ∑ ab : Fin 263 × Fin 263, ∑ po : PairOcc,
            if ab = pairKey po then pairSummand g po else 0 := by
            rw [Finset.sum_comm]
    _ = ∑ ab : Fin 263 × Fin 263, ∑ po : PairOcc,
            if pairKey po = ab then pairSummand g po else 0 := by
            apply Finset.sum_congr rfl
            intro ab hab
            apply Finset.sum_congr rfl
            intro po hpo
            simp [eq_comm]

/-- the second (final) T1c-2a finite-counting obligation: the pair part of the summed F₈ is
    bounded by the block energy. -/
theorem f8PairPart_le_blockEnergy_fact (g : Fin 262 → ℝ) :
    (∀ i : Fin 262, 0 ≤ g i) → f8PairPart g ≤ blockEnergy g := by
  classical
  intro hg
  rw [f8PairPart_eq_pairFiberSum g]
  unfold blockEnergy
  calc
    (∑ ab : Fin 263 × Fin 263,
        (Finset.univ : Finset PairOcc).sum (fun po =>
          if pairKey po = ab then pairSummand g po else 0))
      ≤ ∑ ab : Fin 263 × Fin 263, (if ab.1.1 < ab.2.1 then 2 * wMT (pointDist g ab.1 ab.2) else 0) := by
          apply Finset.sum_le_sum
          intro ab hab
          exact pairFiber_sum_le g ab.1 ab.2
    _ = 2 * (∑ ab : Fin 263 × Fin 263, if ab.1.1 < ab.2.1 then wMT (pointDist g ab.1 ab.2) else 0) := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro ab hab
          by_cases h : ab.1.1 < ab.2.1
          · rw [if_pos h, if_pos h]
          · rw [if_neg h, if_neg h]
            ring
    _ = blockEnergy g := by
          rw [blockEnergy]
          congr 1
          calc
            (∑ ab : Fin 263 × Fin 263, if ab.1.1 < ab.2.1 then wMT (pointDist g ab.1 ab.2) else 0)
                = ((Finset.univ : Finset (Fin 263)).product (Finset.univ : Finset (Fin 263))).sum
                    (fun ab : Fin 263 × Fin 263 =>
                      if ab.1.1 < ab.2.1 then wMT (pointDist g ab.1 ab.2) else 0) := by simp
            _ = ∑ a : Fin 263, ∑ b : Fin 263, if a.1 < b.1 then wMT (pointDist g a b) else 0 := by
                    simpa using (Finset.sum_product (s := (Finset.univ : Finset (Fin 263)))
                      (t := (Finset.univ : Finset (Fin 263)))
                      (f := fun p : Fin 263 × Fin 263 => if p.1.1 < p.2.1 then wMT (pointDist g p.1 p.2) else 0))

/-- **T1c-2a CLOSED:** both finite-counting obligations are machine-proved, so the full
    block-energy statement `blockEnergyFromF8` follows from the closing assembly lemma. -/
theorem blockEnergyFromF8_fact : blockEnergyFromF8 :=
  blockEnergyFromF8_of_parts
    (fun g => f8WindowSum_eq_linear_add_pair_fact g)
    (fun g => f8PairPart_le_blockEnergy_fact g)

end ThmD
end Zeta23
