# Proof outline with exact constants

This is a web outline; the full write-up is [`paper/main.pdf`](../paper/main.pdf).

## 0. Setup (imported)

From the Anthropic paper (and Lean artifact), for any admissible window
profile v (even, 3/4 ≤ v ≤ 1 here, trig polynomial, standard boundary ramp):
with S = # simple zeros on the line in (T,2T], N = all zeros with multiplicity,

    S ≥ H(v)·N + tr Ψ(M) − o(N),                                   (1)

where H(v) = 2 − 1/c₁(v),
c₁(v) = (∫v)² / (∫v² + ∫∫|s−s′|v(s)v(s′)),
M is the Gram matrix of the simple-zero atoms with entries
k_v(xᵢ−xⱼ) + o(1), k_v = K_v/K_v(0), K_v(x) = ∫v(t)cos(2πxt)dt,
and Ψ(t) = (t−1)² on [0,2], 2t−3 beyond. Inequality (1) is the stability
form of the rank–trace argument from ainta/zeta-simple-zeros (audited; see
provenance).

## 1. The window (certified)

v = Σ cⱼ cos(ωⱼ s), ω = (√2, 2π, 4π, 6π, 8π, 10π, 12π),
c = (10⁹, 3322500, −7609135, 1190194, −731476, −1680572, 1141360)/10⁹.

Certified: 3/4 ≤ v ≤ 1 on [−1/2,1/2] (min 0.750213…, max 0.995633…),
v is nonincreasing on [0,1/2], and

    H(v) = 0.67245704141454… ≥ H_cert := 3362285207/(5·10⁹).

## 2. Sharp block profile

For G ⪰ 0 with E = 2Σ_{i<j}|G_{ij}|²:

    tr Ψ(G) ≥ h(E),   h(E) = E (E ≤ 1),  2√E − 1 (E ≥ 1),

via Ψ(t) = (t−1)² − (t−2)₊² and X ≤ ((Δ−1)/2)²; sharp. Chord bound:
h(E) ≥ (h(A)/A)·E on [0,A].

## 3. The certified 7-point inequality

w = k_v², y_j = g₁+…+g_j,

    F(g) = (1/2736)Σgᵢ + Σ_{i<j} a_{ij} w(y_j−y_i) ≥ 891/200000       (†)

for all g ≥ 0, with the exact rational weights of
[`data/candidate-retuned-p2736.json`](../data/candidate-retuned-p2736.json)
(reflection symmetric; every span capacity Σᵢ a_{i,i+r} = 2 exactly).
Certified by exhaustive interval subdivision: 2,168,370 nodes, grid 1/4000
([certificate](../certificates/retuned-p2736-grid4000.txt)).

## 4. Deduction

q = 6, m = 272, ε = 891/200000, p = 1/2736, B_p = 6p = 1/456.

- Summing (†) over the m−q windows of an m-point block of consecutive simple
  zeros (pair weight totals ≤ 2 by capacity; each gap in ≤ 6 windows):
  E_B + B_p·span(B) ≥ A := ε(m−q) = 1.18503.
- Put R = h(A) = 2√A−1 = 1.1771816644… and η = R/A. If
  B_p·span(B) ≥ A, the pressure term already gives R after multiplication by
  η. Otherwise span(B) < A/B_p is uniformly bounded, so the compact-uniform
  Gram-kernel asymptotic applies to every pair in the fixed-size block. The
  sharp profile and its chord then give
  tr Ψ(G_B) + ηB_p·span(B) ≥ R − o(1), uniformly in B.
- Convex pinching + averaging over the m block offsets (each interior gap
  charged ≤ m−1 of m times; total normalized span ≤ N+o(N)):
  tr Ψ(M) ≥ (R/m)S − ηB_p((m−1)/m)N − o(N).
- Insert into (1) with H(v) ≥ H_cert and rearrange:

      S/N ≥ (272·H_cert − η·(1/456)·271) / (272 − R)
          = 0.6732001170127618…  >  1683/2500.

Sanity gate: with the unit cap (η = 1, R = A ≤ 1) and ainta's parameters
(ε = 19/5000, p = 1/3000, m = 269, MT window) the same formula reproduces
0.673008527927… exactly, and this repository's verifier reproduces their
interval certificate (707,797 nodes, verified).

## 5. Dependencies

The finite certificates prove §1 (window bounds, monotonicity, and H), §3
(†), and the §4 arithmetic. §0 and the compact-uniform asymptotics are cited
from the Anthropic paper / Lean artifact and ainta's stability argument. The
new profile has not yet been instantiated as an `AdmWindow` in Lean, and the
stability/square-root assembly is not yet formalized end to end.
