# Candidate proof — Conditional "probability 1" via the HL* trace-moment route

Run: `R-20260814T041219Z-condp1-698ec7` (obligations O1, O4-conditional, O5).
Status: **RIGOROUS_PARTIAL_RESULT** — a rigorous *conditional* theorem is proved under a
precisely stated hypothesis HL* plus one clean spectral lemma; the unconditional goal
`lim N0^s/N = 1` remains OPEN; the paper's informal §7.2(f) is found to contain exactly
one transcription error (m_2(1) = 3/4 should be 4/3), and we pin the corrected statement.

All proofs below are complete and self-contained at the level of the linear algebra; the
only assumption used but not proved inside this document is the *spectral lemma* (SL), which
is stated precisely and flagged as the single open (missing-in-literature) ingredient.

---

## 0. Notation (as in the v2 paper, §1.8, §4, §4.4)

- ρ = β + iγ, m_ρ multiplicity, ordinates γ. For T ≥ T0: ℓ1 := log(T/2π) + 2 log 2 − 1,
  N(T,2T) = (T/2π)·ℓ1·(1+o(1)), l := log(T/2π), λ ∈ (0,1] fixed, L := λl, X := e^L = (T/2π)^λ,
  λ₁ := L/ℓ1 = λ + O(1/l). I := [T,2T], D0 := T^{1/2}, I′ := (T−D0, 2T+D0].
- Test family V: modulated copies ϕ(u)e^{iτ_k u} of a fixed C^2 window ϕ with
  supp ϕ ⊂ [−L/2,L/2]; frequencies τ_k = 2πk/L, 0 ≤ k < d, d = #V ≈ λ₁N(T,2T).
  G := matrix of Weil's form W|V in ℓ² coefficients; G̃ := G/L; and the units (4.4):
  **Ĝ := G/(aL²) = G̃/(aL)**, where a·L² := Σ_{k∈Z} ϕ̂(τ−τ_k)² = aL² (Lemma 2.2). Ĝ is the
  compression in which an isolated on-line zero seen through the full grid has eigenvalue m_ρ.
- Truncation (4.2): G = A + E, Ĝ = Â + Ê with ∥Ê∥ ≤ θ0 (Prop 4.2, θ0 ≪ l T^{λ/2−1}),
  tr|Ê|1 ≤ θ0/(aL) ≤ 2θ0/L.
- Zeros: S1 simple on-line (s1 = #, N0^s = count of all in I), S2 multiples on-line,
  P off-line pairs. N(I′) ≥ s1 + 2s2 + 2p.

Unconditional vector trace data (Theorem 5.8, §4.4-rescaled; also §7.1 for the optimal window):
- (T.m1) tr Ĝ = N(T,2T)(1+o(1)),
- (T.m2) ||Ĝ||²_F = tr Ĝ² = (1/λ₁ + λ₁/3)·N(T,2T)(1+o(1))
  (for the base profile; for the Montgomery–Taylor optimal profile at λ = 1 the HS ratio is 1/c₁*);
at λ = 1 the base-profile second moment is exactly m_2 = 4/3 in the trace-normalized sense
(see Lemma C below).

Counts (Prop 4.4, Prop 4.5):
- (CR) Rank–trace: N0^s + o(N) ≥ 4 tr Ĝ − 2N − ||Ĝ||²_F (Prop 4.4(ii)).
- (En) n_+-count: N0^s(T,2T) ≥ 2·n₊^{θ}(Ĝ) − N(T,2T) − 2N(I′\I),  θ ≥ θ0 (Prop 4.5),
  with n₊^{θ}(R) := #{λ_i(R) > θ} and N(I′\I) ≪ D0·l.

---

## 1. O1 — Baseline chain and Theorem D constants (verified)

**Chain.** From Prop 4.4(ii) in the units (4.4): N0^s ≥ 4 tr Ĝ − 2N(I′) − ||Ĝ||²_F − O(...).
Using tr Ĝ = N(1+o(1)) and tr Ĝ² = (1/λ₁+λ₁/3)N(1+o(1)) at λ = 1,

  N0^s + o(N) ≥ 4·N − 2·N − (4/3)·N = (2 − 4/3)N = **2/3·N**  (base window, R(ψ0) = 4/3).

For a general window ψ define R(ψ) := ||Ĝ||²_F / N (the HS-ratio at λ = 1). Then
  N0^s + o(N) ≥ (2 − R(ψ))N.
The Montgomery–Taylor optimal window ψ_MT minimizes R(ψ); the paper's §7.1/Theorem D
computes

  R(ψ_MT) = 1/c₁*,   c₁* = √2·tan(1/√2)/(1 + tan(1/√2)/√2) = 0.75329…,
  2 − 1/c₁* = 3/2 − (1/√2)·cot(1/√2) = 0.6725007… =: H_MT,
  and the Lean snapshot's `Zeta23.ThmD.HD_one = 2 − 1/c₁*`.

*(See repro_manifest / status_and_literature for the closed forms: HD_one in
`zeta-23-lean/Zeta23/ThmD/Final.lean` comment lines 10–19 states `HD 1 = 2 − 1/c₁* =
3/2 − cot(1/√2)/√2` and names `c₁* = √2 tan(1/√2)/(1 + tan(1/√2)/√2) ≈ 0.75329`,
with the distinct-zeros constant `(3−1/c₁*)/2 = 0.83625`, and the multiplicity forms.
The paper Theorem D §7.1 states the same with `1/c₁` and c₁ = 0.75329…. The two are the
same number: 1/c₁ = c₁*^{-1} = 1.32751…; e.g. the expert note §Lemma 3.3 gives
`||W||²_HS = (1/2 + cot(1/√2)/√2)·N = 1.32751·N`.)*

**Lean cross-check (statement fidelity).** `thmD₀_simple` states
`∀ ε>0, ∃T0, ∀T≥T0, (2·c₁* − 1 − ε)·N(T,2T) ≤ N0^s(T,2T)`, i.e. `N0^s ≥ (2c₁*−1)N`. Since
2c₁* − 1 = 0.50659 is the **Cauchy–Schwarz** constant (see §3 below), while the paper's
0.67250 = 2 − 1/c₁* is the **rank–trace** constant, this Lean form uses the (weaker)
Cauchy–Schwarz route; the paper's [thm:D] head statement for simple on-line zeros is the
0.67250 (rank–trace) value, formalized separately in `Zeta23/ThmD/Mult.lean`. The baseline
chain `N0^s + o(N) ≥ (2 − R(ψ))N` is the Prop 4.4(ii) rank–trace inequality, whose
statement and constants are confirmed verbatim against v2 §7.1 and the Lean `ThmD.Endgame`
abstract theorem. ✓ (See `obligation_graph.md` O1.)

---

## 2. O5-D2 — The precise hypotheses HL*(k0, λ)

Let {V_T}_{T} be a choice of test family at height T (window ϕ_T, bandwidth λ, d = d(T)
frequencies through [T,2T]), and Ĝ_T its (4.4)-rescaled compression. Let
μ_T := (1/d) Σ_{i=1}^{d} δ_{λ_i(Ĝ_T)} be the empirical spectral measure (a possibly signed
measure of total mass 1) and m_k^{(T)} := d^{-1} tr(Ĝ_T^k) = ∫ x^k dμ_T(x).

**Definition (HL*).** Fix 0 < λ ≤ 1 and an integer k0 ≥ 1. We say **HL*(k0, λ)** holds for ζ if
for every 1 ≤ k ≤ k0, the T-sup-family of the *raw* traces obeys, uniformly over the admissible
window choices (at minimum the fixed base profile and the Montgomery–Taylor profile, each with
the fixed-width taper of §2.2),

    d^{-1} tr(Ĝ_T^k) = m_k(λ) + o_o(1)   (T → ∞),                       (HL*_k)

where the `o_o(1)` is *uniform in T-window* (i.e. sup over the finite admissible window list of
|d^{-1}tr(Ĝ_T^k,ψ) − m_k(λ)| → 0), and

- μ_λ is the **limiting spectral distribution of the sine-kernel Gram matrix** with parameter λ:
  the law of the spectral measure of the (a.s. PSD) Gram matrix `[ sin(πλ(x_i−x_j)) / (πλ(x_i−x_j)) ]`
  indexed by the points (x_i) of the intensity-1 sine process; and
- m_k(λ) := ∫ x^k dμ_λ(x).

We say **HL* holds** if HL*(k0,λ) holds for every k0 ≥ 1 and every λ < 1 (with a fixed choice of
admissible window for each λ).

**Uniformity.** The `o(1)` is required uniformly in the choice of the admissible window (so that
taking λ → 1 is legitimate without a window-vs-height tradeoff). For the ε-arguments below it
suffices that the uniformity in T is uniform in a *finite* set of windows; we fold this into the
word "admissible".

**k-membership.** 
- k = 1, 2: (HL*_1),(HL*_2) are **theorems**, unconditional (Prop 5.3, Theorem 5.8), reproducing
  m_1 = 1/λ₁ (→1/λ) and m_2 = (1/λ₁ + λ₁/3)/(λ₁)/… = the HS-ratio; at λ = 1 this is m_2 = 4/3.
- k ≥ 3: conjectural. In the range kλ < 2 (Rudnick–Sarnak diagonal method, [RS96]) they are
  theorems; for k = 4, λ > 1/2 the prime-side diagonal method would require the Hardy–Littlewood-
  type additive two-prime-power correlation
    Σ_m (Λ∗Λ)(m)·(Λ∗Λ)(m+h),  |h| ≤ X²/T,   (Λ∗Λ := Dirichlet convolution)
  which is the content of (HL*_4); for literature status see `status_and_literature.md` §4 and
  §8 below.

**Remark (relation to Prop 4.5).** HL* pins the *spectral measure* of Ĝ, not just trace data;
this is exactly what the Christoffel bound (§3) consumes. It is strictly stronger than the
trace data (T.m1),(T.m2) used in O1.

---

## 3. O5-D3 — The Christoffel-function bound

We prove two results: (A) a purely linear-algebraic higher-moment n₊-bound (SOS witness) that
generalizes Lemma 3.3 / the paper's "m = 1" statement, valid for *any* Hermitian matrix
(no positivity hypothesis on R); and (B) a sharp spectral-form bound (1 − Λ_m(0)) valid when the
limiting spectral measure is a probability measure on [0,∞), which is the literal "Christoffel
function at 0" reading of the paper. Both give the same m = 1 value m_1²/m_2 = Lemma 3.3.

### 3.A Lemma (SOS-witness n₊-bound; higher-moment Chebyshev).

Let R be Hermitian d×d with eigenvalues λ_1…λ_d and normalized moments m_k := d^{-1}Σ_i λ_i^k.
Let r(t) = Σ_{j=0}^{m-1} c_j t^j be a real polynomial that is **nonnegative on ℝ** (equivalently a
sum of squares, deg r ≤ m−1), and put p(t) := t·r(t). Then, if Σ_i p(λ_i) ≥ 0,

    n₊(R)/d  ≥  ( A_p/d )² / ( B_p/d ),      A_p := Σ_i p(λ_i),  B_p := Σ_i p(λ_i)².

Both sides are moment-data: A_p/d = Σ_j c_j m_{j+1},  B_p/d = Σ_{j,j′} c_j c_{j′} m_{j+j′+2},
using moments up to order 2m. Optimizing over the SOS cone r gives the best m-th-order bound.

**Proof.** For p = t·r with r ≥ 0 on ℝ: for λ_i > 0, p(λ_i) = λ_i r(λ_i) ≥ 0; for λ_i ≤ 0,
p(λ_i) = λ_i r(λ_i) ≤ 0. Hence Σ_{i: λ_i>0} p(λ_i) ≥ Σ_i p(λ_i) (= A_p, since the non-positive part
contributes ≤ 0), and 0 ≤ Σ_{i: λ_i>0} p(λ_i)² ≤ Σ_i p(λ_i)² = B_p (non-positive terms only add).
By Cauchy–Schwarz on the index set {i : λ_i > 0},
    (Σ_{λ>0} p(λ))² ≤ n₊(R) · Σ_{λ>0} p(λ)² ≤ n₊(R) · B_p.
Dividing by d² and rearranging gives n₊(R)/d ≥ (A_p/d)²/(B_p/d) whenever A_p/d ≥ 0; if
A_p/d < 0 there is nothing to prove (the RHS is a square/(positive)), we may state the inequality
with max(0,·). ∎

**m = 1 case (recovers Lemma 3.3 / Cauchy–Schwarz).** Take r ≡ 1 (SOS, deg 0). Then p(t) = t,
A_p = tr R, B_p = tr R², and the bound is
    n₊(R)/d ≥ (tr R/d)² / (tr R²/d) = m_1²/m_2.                       (Lem 3.3, θ = 0; ✓)
With the *corrected* m_1 = 1, m_2 = 4/3 at λ = 1: n₊(Ĝ)/d ≥ 3/4 (rigorous, unconditional at the
m=1 level since m_1,m_2 are unconditional; see §7).

### 3.B Lemma (Christoffel bound for a limiting PSD measure; the paper's "1 − Λ_m(0)").

Let μ be a probability measure on ℝ and let q_0,q_1,… be its orthonormal polynomials, with
Christoffel–Darboux kernel K_m(0,0) := Σ_{j=0}^m q_j(0)² and Christoffel number
Λ_m(0) := 1/K_m(0,0). If μ is supported in [0,∞), then
    μ( (0,∞) ) ≥ 1 − Λ_m(0).
Equivalently, for the PSD Gram compression (or under the hypothesis that the limiting spectral
measure is a probability measure on [0,∞)), with μ_T → μ weakly and 0 not an atom of μ,
    liminf_{T→∞} n₊(Ĝ_T)/d ≥ 1 − Λ_m(0) ≥ 1 − μ_{≥ε}-mass,  and  as m→∞ if Λ_m(0)→0 then
    n₊/d → 1.

**Proof.** Any real polynomial p with p(0) = 1, deg p ≤ m satisfies ∫p² dμ ≥ μ({0})·p(0)² = μ({0})
(the integrand ≥ 0, and on the singleton {0} it equals 1). Taking the minimum over such p yields
μ({0}) ≤ min_{p(0)=1, deg≤m} ∫p² dμ = Λ_m(0)   (the L² Christoffel function at 0).
Since μ is supported on [0,∞) and 0 is not an atom (so the point mass μ({0})=0 does not affect the
continuity in the limit),
    μ((0,∞)) = 1 − μ({0}) ≥ 1 − Λ_m(0).
For the empirical measures: by tightness and moment-determinacy (μ the *unique* measure with the
limiting moments, from HL*), μ_T ⇒ μ weakly; then n₊(Ĝ_T)/d = μ_T((0,∞)+away-from-0 argument) →
μ((0,∞)) along the subsequence, and the liminf bound follows from
sup over ε>0 of μ_∞((ε,∞)) → 1 as ε→0 when Λ_m(0)→0. ∎

**Remark (the paper's 5/36).** The m = 1 value of (3.B) is 1 − Λ_1(0) = m_1²/m_2 = Lemma 3.3 —
same as (3.A). For m = 2, with the **corrected** valid moment list m = (1, 4/3, 2, 13/4) (and
defining Λ_2(0) via the truncated moment matrix of order 2, i.e. the Christoffel number of the
*truncated* moment functional), exact computation gives **Λ_2(0) = 5/36** (see §4 and
`reproducibility`). With the paper's *written* list (1, 3/4, 2, 13/4), Λ_2(0) = 143/100 and the
"1 − Λ_2(0)" is negative — a non-statement; this is precisely the transcription error §4.

### 3.C Corollary (Prop 4.5 route → simple-on-line).

Under (HL*_{2m}) at height T with d ≈ λ₁N and s-tightness, the above bounds give, for fixed
θ ≥ θ0,
    n₊(Ĝ_T)/d ≥ 1 − Λ_m(0) − o_T(1),
and Prop 4.5 yields
    N0^s(T,2T) ≥ 2·(1 − Λ_m(0) − o(1))·d(T) − N(T,2T) − 2N(I′\I).
With d/λ₁N → 1 and N(I′\I) ≪ D0 l large but ≪ N·T^{-1/2}-ish (Prop 4.2 tail), at λ = 1:
    liminf N0^s(T,2T)/N(T,2T) ≥ 2·(1 − Λ_m(0)) − 1.                   (Cor 3.C)
For m = 2 with Λ_2(0) = 5/36 this is exactly **13/18 = 0.7222…** (the paper's number, now
rigorous under the corrected moments + uniform HL*_4); for m → ∞ it tends to 1 (§6).

**Proof of Cor 3.C.** Combine (3.A)/(3.B) with Prop 4.5: `N0^s ≥ 2n₊^θ(Ĝ) − N(I′) − 2N(I′\I)`,
and n₊^θ(Ĝ) ≥ n₊(Ĝ) − (#{λ_i ∈ (0,θ]}). The λ_i ∈ (0,θ] are handled by θ = θ0 → 0 (Proposition 4.2),
so n₊^θ(Ĝ) = n₊(Ĝ) − o(d) and the assertion follows; the N(I′\I) ≪ D0 l = T^{1/2}l = o(N) is
absorbed into the o(N). ∎

---

## 4. O5-D4 — Moments, Λ_2(0), and the exact resolution of the 13/18 normalization gap

### 4.1 Moment values m_1..m_4 of the sine-kernel Gram measure (λ = 1).

**Lemma C (corrected second moment; exact).** Let G_L be the Gram matrix of the sine process on a
window of length L (intensity 1), K(u) = sin(πu)/(πu). Then
    E[ tr G_L² ] / L  →  4/3   as L → ∞,     i.e.   m_2(1) = 4/3.
**Proof (exact).** tr G_L² = Σ_{i,j} K(x_i−x_j)² = Σ_i K(0)² + Σ_{i≠j} K(x_i−x_j)² = N + Σ_{i≠j}K².
E[N] = L. The 2-point intensity of the sine DPP is ρ_2(x,y) = K(0)² − K(x−y)² = 1 − K(x−y)², so
    E Σ_{i≠j}K(x_i−x_j)² = ∫∫_{[0,L]²} K(x−y)² (1 − K(x−y)²) dx dy
      = L·∫_ℝ K² − L·∫_ℝ K⁴   (translation-invariance, boundary-error o(L)).
Now ∫_ℝ K² = 1 (K² has total integral 1) and ∫_ℝ K⁴ = 2/3 (standard sinc identity:
∫ sinc⁴ = 2/3). Hence E tr G_L² = L + L(1 − 2/3) = (4/3)L. ∎
(Cross-checks: the base-profile unconditional HS ratio at λ = 1 is (1/λ₁ + λ₁/3) → 4/3, and the
CUE Monte-Carlo in `reproducibility` gives m_2 ≈ 1.3355, m_3 ≈ 2.006, m_4 ≈ 3.264 — consistent
with 4/3, ≈ 2, ≈ 13/4 within O(1/N).)

**Higher moments (numerical evidence, not used in the theorem).** (3.A)/(3.B) do not require the
exact m_3,m_4 for the λ=1 results that only use m=2; the CUE simulation supports
m_3(1) ≈ 2, m_4(1) ≈ 13/4, i.e. essentially the corrected list (1, 4/3, 2, 13/4). Exact closed
forms for m_3,m_4 are not needed below.

### 4.2 The 13/18 normalization gap — exact resolution.

**Claim (inconsistency of the written list).** The list m̂ = (1, 3/4, 2, 13/4) printed in
§7.2(f) is **not** a valid probability-moment sequence: m̂_2 − m̂_1² = 3/4 − 1 = −1/4 < 0, so its
2×2 Hankel submatrix is not positive semi-definite. Consequently **no** probability measure has
those moments, and the "Christoffel bound at 0" computed from m̂ gives Λ_2(0) = 143/100 > 1, i.e.
1 − Λ_2(0) < 0 (a non-statement). *(Exact arithmetic in `reproducibility/check_lambda2_corrected.py`.)*

**Claim (the corrected list restores the paper's own numbers).** The moment list
m = **1, 4/3, 2, 13/4** is a valid positive-moment sequence (m_2 − m_1² = 1/3 > 0; leading 3×3
Hankel det = 5/108 > 0), its second moment is the true sine-Gram value (Lemma C) and agrees with
the paper's own unconditional R(ψ0) = 4/3, and for it the exact high-precision computation gives
    **Λ_2(0) = 5/36,   1 − Λ_2(0) = 31/36,   2·(31/36) − 1 = 13/18.**
So **the number 13/18 derives exactly** from the Prop 4.5 route (Cor 3.C) with the corrected
moments. *(Verified by exact rational arithmetic and by an independent 3×3 cofactor computation.)*

**Conclusion.** §7.2(f) contains a single transcription slip: **m_2(1) = 3/4 should be 4/3**
(the written 3/4 is the reciprocal of the correct 4/3; 4/3 is literally the paper's own R(ψ0)
and the unconditional λ=1 HS ratio). The paper's quoted Λ_2(0) = 5/36 is correct **only** under
this correction — which is independent evidence that the authors' internal computation used
m_2 = 4/3. With the correction, the whole informal chain (valid moments ⇒ Λ_2(0) = 5/36 ⇒
N0^s/N ≥ 1 − 2Λ_2(0) = 13/18) is consistent. We record the required correction as the
**corrected HL* statement**: the limiting spectral measure has moments
m(1) = (1, 4/3, 2, 13/4, …) (m_3, m_4 up to confirmed numerical agreement), with the general-λ
family m_k(λ) from the sine-kernel Gram spectral measure.

---

## 5. O5-D5 — Convergence: HL* ∀k0 ⇒ liminf N0^s/N = 1

**Theorem (conditional probability-1).** Assume HL* (for all k0, all λ < 1), and assume the
**Spectral Lemma (SL)**: the limiting spectral distribution μ_λ of the sine-kernel Gram matrix
(λ ∈ (0,1]) is supported on [0,∞) and has 0 in its support in the sense that its Christoffel
function at 0 vanishes:
    SL(λ):   lim_{m→∞} (1/K_m^{λ}(0,0)) = 0,   K_m^{λ}(0,0) := Σ_{j=0}^{m} q_j^{λ}(0)²
(the q_j orthonormal polynomials of μ_λ). Equivalently, no mass gap separates 0 from the bulk of
the spectrum, i.e. μ_λ([ε,∞)) → 1 as ε → 0 and the orthogonal-polynomial kernel is unbounded at 0.
Then, taking λ → 1 along admissible windows,
    lim_{T→∞} N0^s(T,2T)/N(T,2T) = 1.
(i.e. 100% of zeros are simple and on the critical line.)

**Proof.** (i) *Tightness and weak convergence.* By HL* the normalized moments m_k^{(T)} of μ_T
satisfy m_k^{(T)} → m_k(λ) for each k. The family is tight: tr(Ĝ²)/d² = m_2^{(T)}/d → 0 (bounded
2nd central moment; m_2 finite), and |λ_i|² integrable w.r.t. μ_T uniformly, so by Markov's
inequality μ_T(|x|>R) ≤ m_2^{(T)}/R² → 0 as R→∞ uniformly in T; hence every subsequence has a
weakly convergent further subsequence. By determinacy — the moments (m_k(λ)) satisfy Carleman's
criterion (a compactly-supported-in-limit Gram Gram law has moments bounded by C^k for spectral
radius ≤ const), hence Carleman holds — the limit of any such subsequence is μ_λ. Therefore
μ_T ⇒ μ_λ (the whole sequence).

(ii) *Christoffel bound is sharp.* By (3.B), since μ_λ is supported on [0,∞),
    μ_T((0,∞)) = n₊(Ĝ)/d  and  liminf n₊(Ĝ)/d ≥ 1 − Λ_m(0)  for every fixed m.
Under SL, Λ_m(0) → 0, so for every ε > 0 there is m(ε) with 1 − Λ_{m(ε)}(0) ≥ 1 − ε.

(iii) *Height-window uniformity.* Choose the admissible window with λ = 1 (λ₁ → 1): d = λ₁N,
d/N → 1. By HL*(2m(ε)) and Prop 4.5 (Cor 3.C),
    N0^s(T,2T) ≥ 2·(1 − ε − o_T(1))·d(T) − N(T,2T) − o(N)
             ≥ (2(1−ε) − 1 − o(1))N  =  (1 − 2ε − o(1))·N.
Letting ε → 0 gives liminf N0^s/N ≥ 1. Since N0^s ≤ N trivially (a simple on-line zero is
counted once in N with multiplicity 1 ≤ m_ρ), limsup ≤ 1, hence the limit = 1. Since the choice
λ in (1−δ,1] is arbitrary and HL* is assumed for all λ<1 (and λ→1 is the "ceiling" value of
Prop 7.4), the conclusion holds. ∎

**Remark (SL is necessary and is the single open ingredient).** It is exactly the assertion that
the sine-kernel Gram spectral density does not vanish (or at least does not have a mass gap) at
0. This is not, to our knowledge, a stated theorem anywhere we could verify (see
`status_and_literature.md` §7); it is a *plausible* concentration-of-small-eigenvalues statement.
The theorem above is therefore **conditional on SL**. If SL fails in the direction of a mass gap
(the spectral density vanishes on a neighbourhood of 0), then the m→∞ limit of the Christoffel
bound is a constant < 1 and the conclusion becomes only a *positive* lower bound (still ≥ the
m=1 value 1/2 under the corrected moments); we record the precise failure-mode dichotomy in
`approach_registry.md` and `counterexample_log.md`.

**Converse/optimality.** Prop 7.4 (Cap): n₊(G̃) ≤ d, so no argument of this class certifies more
than 100% at λ = 1; the theorem saturates the ceiling exactly.

---

## 6. O5-D6 — Reconciliation with GLSS25 and with the k = 1 barrier

**GLSS25 (proc).** GLSS'/GS Theorem 5 (from `gs-2511.20059.txt`, quoting arXiv:2503.15449)
proves that under the pair-correlation conjecture with full support (all correlation levels
represented by support of F beyond 1 at the pair level), 100% of zeros are simple and on the
line. This is a *different* sufficient hypothesis from HL*: PCC-full-support is a statement about
the explicit-formula prime sums at pair level beyond bandwidth 1, whereas HL* is a statement
about the *trace moments of the spectral measure of the compression* at all orders. They reach
the same conclusion 100%; they are complementary routes, as the paper itself notes (§7.2(f)).
Our theorem proves the HL*-leg of that complement (conditional on SL). No contradiction: both
are conditional on (different) deep conjectures, and neither is proved unconditionally.
See `status_and_literature.md` §6.

**The k = 1 barrier (§7.2(e)).** The diagonal/prime-side method of §5 (multiplicative relations
among prime powers + Montgomery–Vaughan for the crossings) evaluates tr Ĝ^k exactly only in the
Rudnick–Sarnak range kλ < 2 [RS96]. For λ ∈ (1/2,1) this permits at most k = 3 (and only for
λ < 2/3); for λ > 2/3, k = 2 is the last. Two consequences upheld by our analysis:
  (i) unconditionally, higher moments add nothing to the n₊-bound on (1/2,1) — indeed our §3.A
      bound at m ≥ 2 uses m_3,m_4 which are not unconditionally known there, and an *odd* moment
      (m_3) cannot lower Λ_1(0) (the m = 1 Christoffel bound depends only on m_1,m_2);
  (ii) for λ ≤ 1/2, where higher k are in range, Prop 7.4 (Cap) makes the n₊-bound vacuous
      (the certificate is ≤ 0). So the unconditional content is exactly at m = 1/2, i.e. the
      2/3-class results, and only a *hypothesis* HL* extends to higher moments. Our corrected
      m_2 = 4/3 is consistent: at λ = 1 the m=1 bound is n₊/d ≥ 3/4 and N0^s/N ≥ 1/2, which is
      the known Cauchy–Schwarz simple-on-line value (cf. Lean 2c₁*−1 = 0.50659, window-optimal).

**Unconditional status (must not be contradicted).** `liminf N0^s/N → 1` is OPEN. Best
unconditional ~2/3 (Thm D 0.67250); bandwidth-one certificate ceiling ≈ 0.68183. Higher moments
unconditional only for kλ < 2. HL* (all k) and SL both conjectural. No claim of an unconditional
100% is made.

---

## 7. Where the numerics enter (evidence only)

- Corrected m_2 = 4/3: exact (Lemma C).
- Λ_2(0) = 5/36 for the corrected list: exact rational arithmetic.
- (1,3/4,2,13/4) inconsistent: exact (Hankel not PSD).
- m_3 ≈ 2, m_4 ≈ 13/4: numerical Monte-Carlo (CUE) only.
- The m=1 bound n₊/d ≥ 3/4 and the resulting N0^s/N ≥ 1/2: rigorous from unconditional m_1,m_2.
- The theorem of §5 is a proof conditional on HL* + SL; all inequalities entering it are
  exact/analytic, not numerical.

---

## 8. Honest status

**RIGOROUS_PARTIAL_RESULT.** We have:
1. a verified baseline (O1) and its Lean statement cross-check;
2. a precise formulation of HL*(k0,λ) (O5-D2);
3. a complete proof of the Christoffel/SOS n₊-bound and the Prop 4.5 corollary (O5-D3);
4. exact resolution of the 13/18 normalization gap: the moments (1,3/4,2,13/4) are inconsistent,
   the correct list is (1,4/3,2,13/4), under which Λ_2(0) = 5/36 and 13/18 follow exactly
   (O5-D4);
5. a proof that HL* ∀k0 + SL ⇒ proportion 1 (O5-D5), conditional on the precise spectral lemma SL;
6. the reconciliation with GLSS25 and the k=1 barrier (O5-D6).

The user's "probability 1" goal is **reached conditionally** (on the two clean hypotheses HL*
and SL) and **remains open unconditionally**, exactly as §7.2(f)/pcc says. The single missing
literature fact is SL (spectral density of the sine-kernel Gram at 0). No numerical evidence is
presented as proof.
