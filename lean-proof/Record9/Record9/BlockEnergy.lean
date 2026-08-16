/-
Record9.BlockEnergy — T1c-2a: block energy from the certified F₈ bound (bounded pass).

Part of the Stage C formalizer pass for the C₉ = 0.67306647267… world-record theorem. This
module formalizes the finite-window block-energy statement T1c-2a from
`runs/rigorous-open-math-research/R-20260816T060000Z-stabridge-a3f1/` (candidate_proof.md
§3): with 263 ordered points y₁<…<y_m and gaps gᵢ = y_{i+1}−y_i (i = 0..261, 262 gaps), if
every consecutive 9-window (8 gaps) satisfies the certified bound F₈ ≥ 392/100000, then
E_m(g) + (1/500)·span(g) ≥ A₀ = 2499/2500.

Machine-checked content here (honest bounded milestone):
  • the exact T1c-2a statement frozen as the `Prop` `blockEnergyFromF8`,
  • the precise definitions `blockEnergy`, `blockSpan`, `f8Window`, `f8WindowSum`,
  • the exact constant identity A₀ = (392/100000)·255 = 2499/2500, and
  • the finite bookkeeping sub-lemmas (window membership/counting and the coefficient
    identities) that DO compile.
The full inequality (`blockEnergyFromF8` as a `theorem`) is the recorded OPEN obligation:
closing it requires the sum-over-windows decomposition of `f8WindowSum` into a linear part
(each gap in ≤ 8 windows, coefficient 1/(500·8)) and a pair part (each s-separated pair in
≤ 9−s windows, coefficient 2/(9−s)) together with the certified `CERTIFIED_F8_GE` F₈-bound.
NO sorry/admit/axiom appear anywhere in this module or any Record9 module.

Fidelity notes:
  • The block energy is
        E_m(g) = 2·Σ_{0≤i<j≤262} wMT(y_j − y_i),
    realized here as `blockEnergy g = 2 * Σ_{a,b : Fin 263, if a<b} wMT (gapSpan g a (b-a))`
    over the 263 points y_0..y_262, matching the contract's literal formula.
  • `blockSpan g = Σᵢ gᵢ` is the total gap span y_m − y_1.
  • `f8Window g j = F8 (window j)` is the certified pressure on the 8 gaps j..j+7 for
    j : Fin 255 (255 consecutive 9-windows).
  • `blockEnergyFromF8` freezes the target with the contract's literal rationals 392/100000,
    2499/2500 and 1/500.
-/

import Record9.Chain9

noncomputable section

open scoped BigOperators
open BigOperators Finset

namespace Zeta23
namespace ThmD

/-- lift a `Fin 262 → ℝ` gap vector to an infinite sequence by the mod-262 convention:
    `gapAt g n = g (n mod 262)`. This is the input form required by `gapSpan`. -/
def gapAt (g : Fin 262 → ℝ) (n : ℕ) : ℝ :=
  g ⟨n % 262, Nat.mod_lt n (by decide)⟩

/-- distance between two of the 263 points y_a, y_b (0-based) with a < b: the sum of the
    gaps g_a, g_{a+1}, …, g_{b−1} = `gapSpan (gapAt g) a (b−a)`. -/
def pointDist (g : Fin 262 → ℝ) (a b : Fin 263) : ℝ :=
  gapSpan (gapAt g) a.1 (b.1 - a.1)

/-- **blockEnergy** E_m(g) = 2·Σ_{0≤i<j≤262} wMT(y_j − y_i) (candidate_proof §3). The sum
    is over the unordered point pairs, i.e. all `a.1 < b.1` in `Fin 263`. -/
def blockEnergy (g : Fin 262 → ℝ) : ℝ :=
  2 * ∑ a : Fin 263, ∑ b : Fin 263, if a.1 < b.1 then wMT (pointDist g a b) else 0

/-- **blockSpan** span(g) = Σᵢ gᵢ = y_m − y_1 (total gap span, 262 gaps). -/
def blockSpan (g : Fin 262 → ℝ) : ℝ := ∑ i : Fin 262, g i

/-- the consecutive 9-window starting at gap `j` (8 gaps j..j+7, points y_j..y_{j+8});
    exactly the `F₈` pressure value on that window. `j : Fin 255` since j = 0..254. -/
def f8Window (g : Fin 262 → ℝ) (j : Fin 255) : ℝ :=
  F8 (fun k : Fin 8 => g ⟨j.1 + k.1, by omega⟩)

/-- the sum of the certified pressure over all 255 windows j = 0..254. -/
def f8WindowSum (g : Fin 262 → ℝ) : ℝ := ∑ j : Fin 255, f8Window g j

/-- **blockEnergyFromF8 (T1c-2a, frozen statement)** — for any 262 nonnegative gaps whose
    every consecutive 9-window (8 gaps) satisfies the certified bound F₈ ≥ 392/100000, we
    have E_m(g) + (1/500)·span(g) ≥ A₀ = 2499/2500. This is the exact contract target; the
    proof is OPEN (see module header). -/
def blockEnergyFromF8 : Prop :=
  ∀ g : Fin 262 → ℝ, (∀ i : Fin 262, 0 ≤ g i) →
    (∀ j : Fin 255, (392 : ℝ) / 100000 ≤ f8Window g j) →
    (2499 : ℝ) / 2500 ≤ blockEnergy g + (1 / 500) * blockSpan g

/-! ## T1c-2a exact constants -/

/-- exact: A₀ = f₉·255 = (392/100000)·255 = 2499/2500 (the frozen RHS constant). -/
lemma A0_eq_f8_255 : (392 : ℝ) / 100000 * (255 : ℝ) = (2499 : ℝ) / 2500 := by norm_num

/-- exact: A₀ = f₉·(m−8) with m = 263 (m−8 = 255). Same identity stated via the
    contract's literal `m−8 = 263−8`. -/
lemma A0_eq_f8_m_sub_8 : (392 : ℝ) / 100000 * ((263 : ℝ) - 8) = (2499 : ℝ) / 2500 := by norm_num

/-! ## T1c-2a finite bookkeeping — window membership

A window `j : Fin 255` covers the 8 gaps j..j+7 (and the 9 points y_j..y_{j+8}). We record
the membership relations used by the "each gap in ≤ 8 windows" / "each s-separated pair in
≤ 9−s windows" counting. These compile as standalone facts; the full counting/coefficient
assembly is the recorded OPEN obligation.
-/

/-- gap `r` lies inside window `j` (j ≤ r ≤ j+7), i.e. the 8-gap window j..j+7 contains it. -/
def windowContainsGap (r : Fin 262) (j : Fin 255) : Prop :=
  j.1 ≤ r.1 ∧ r.1 ≤ j.1 + 7

/-- the 9 points of window `j` are y_j..y_{j+8}; a point with index `a` (0-based, `Fin 263`)
    lies in window `j` iff j ≤ a ≤ j+8. -/
def windowContainsPoint (a : Fin 263) (j : Fin 255) : Prop :=
  j.1 ≤ a.1 ∧ a.1 ≤ j.1 + 8

/-- a pair of points (y_a, y_b) with 0 < b−a = s ≤ 8 is contained in window `j` iff
    j ≤ a and b ≤ j+8 (so j ∈ [a+s−8, a]). For s ≤ 8 this is a nonempty interval, giving the
    ≤ 9−s windows of the bookkeeping claim. -/
def windowContainsPair (a b : Fin 263) (j : Fin 255) : Prop :=
  j.1 ≤ a.1 ∧ b.1 ≤ j.1 + 8

/-- if a pair (a,b), b > a, lies in window j, then the gap-r separation of the pair's
    endpoints is at most 8; conversely `windowContainsPair` demands exactly b ≤ j+8 (s ≤ 8). -/
lemma windowContainsPair_imp_sep_le_eight {a b : Fin 263} {j : Fin 255}
    (hab : a.1 < b.1) (hj : windowContainsPair a b j) :
    b.1 - a.1 ≤ 8 := by
  dsimp [windowContainsPair] at hj
  have hb : b.1 ≤ j.1 + 8 := hj.2
  have ha : j.1 ≤ a.1 := hj.1
  have hsep : b.1 - a.1 ≤ (j.1 + 8) - j.1 := by
    have hle : b.1 ≤ j.1 + 8 := hb
    have hle' : j.1 ≤ a.1 := ha
    omega
  omega

/-- each unordered point pair with separation s ≥ 9 cannot lie in any 8-gap window — the
    "pairs with s ≥ 9 never appear in a window and contribute 0 to the F₈ sum" fact. -/
lemma windowContainsPair_requires_sep_le_eight {a b : Fin 263} {j : Fin 255}
    (hsep : 8 < b.1 - a.1) : ¬ windowContainsPair a b j := by
  intro hj
  have hle := windowContainsPair_imp_sep_le_eight (by omega : a.1 < b.1) hj
  omega

/-- each gap lies in at most 8 valid windows: if r ∈ window j then j is squeezed into the
    ≤ 8 consecutive values max(0, r−7)..min(254, r). This lemma records the membership
    bound `r − 7 ≤ j ≤ r` that underlies the "≤ 8 windows" count. -/
lemma windowContainsGap_bounds {r : Fin 262} {j : Fin 255} (hj : windowContainsGap r j) :
    j.1 + 7 ≥ r.1 ∧ j.1 ≤ r.1 := by
  exact ⟨hj.2, hj.1⟩

/-! ## T1c-2a finite bookkeeping — linear coefficient identity

The linear part of the summed F₈ is
    Σ_{j} (1/(500·8))·Σ_{t<8} g_{j+t} = (1/(500·8))·Σ_{r} (count of windows containing r)·g_r.
Since each gap is in ≤ 8 windows, the aggregate linear contribution is ≤ (1/500)·Σ g_r.
We record the pointwise coefficient representation as a standalone definition so the bound
`≤ (1/500)·span` is the documented assembly step (OPEN).
-/

/-- the number of windows (out of j = 0..254) that contain the gap `r`, i.e. the linear
    multiplicity `c_r = #{j : j ≤ r ≤ j+7}`. -/
def linearMultiplicity (r : Fin 262) : ℕ := by
  classical
  exact (Finset.univ.filter (fun j : Fin 255 => windowContainsGap r j)).card

/-- the aggregate linear contribution of the summed F₈ as a function of the gaps:
    (1/(500·8))·Σ_r (linearMultiplicity r)·g_r. This is the exact linear part before the
    `≤ (1/500)·span` bound (the multiplicity ≤ 8 bound is the OPEN assembly step). -/
def f8LinearPart (g : Fin 262 → ℝ) : ℝ :=
  (1 / (500 * 8 : ℝ)) * ∑ r : Fin 262, (linearMultiplicity r : ℝ) * g r

/-- exact coefficient: 1/(500·8)·8 = 1/500 (the aggregate linear-rate identity used when
    bounding the linear part by the ≤ 8-windows multiplicity). -/
lemma linear_rate_identity : (1 : ℝ) / (500 * 8) * (8 : ℝ) = (1 : ℝ) / 500 := by norm_num

/-! ## T1c-2a finite bookkeeping — pair coefficient identity

The pair part of the summed F₈ over window j is, for s0 = 0..7 (s = s0+1), the sum over
8−s0 starting points of (2/(8−s0))·wMT over the window's internals. An unordered pair of
points separated by s gaps appears in ≤ 9−s windows with coefficient 2/(9−s), so its total
contribution is ≤ 2·wMT(distance) — which is exactly one E_m summand. The `2/(9−s)` coefficient
identity and the `(9−s)·(2/(9−s)) = 2` identity are the standalone algebra facts recorded here.
-/

/-- the pair coefficient for separation s = s0+1 (1≤s≤8): 2/(9−s) = 2/(8−s0). -/
def pairCoeff (s : ℕ) : ℝ := 2 / (9 - s : ℝ)

/-- exact: pairCoeff (s0+1) = 2/(8−s0), matching the `(2/((8−s0):ℕ):ℝ)` term in `F8gaps`. -/
lemma pairCoeff_of_s0 (s0 : ℕ) (hs0 : s0 ≤ 8) :
    pairCoeff (s0 + 1) = (2 : ℝ) / ((8 - s0 : ℕ) : ℝ) := by
  rw [pairCoeff]
  have h1 : (9 - (s0 + 1 : ℕ) : ℝ) = 8 - (s0 : ℝ) := by
    rw [Nat.cast_add]
    norm_num
    ring
  have h2 : ((8 - s0 : ℕ) : ℝ) = 8 - (s0 : ℝ) := by
    rw [Nat.cast_sub hs0]
    norm_num
  rw [h1, h2]

/-- exact: (9−s)·pairCoeff s = 2 for 1 ≤ s ≤ 8 — each s-separated pair times its ≥ 9−s
    window multiplicity yields the 2·wMT(distance) E_m summand. -/
lemma pairCoeff_mul_windows {s : ℕ} (h1 : 1 ≤ s) (h8 : s ≤ 8) :
    ((9 - s : ℕ) : ℝ) * pairCoeff s = 2 := by
  have hs : s ≤ 9 := by omega
  rw [Nat.cast_sub hs]
  dsimp [pairCoeff]
  have hne : (9 : ℝ) - s ≠ 0 := by
    have hlt : (s : ℝ) < 9 := by exact_mod_cast (lt_of_le_of_lt h8 (by norm_num))
    linarith
  field_simp [hne]

end ThmD
end Zeta23
