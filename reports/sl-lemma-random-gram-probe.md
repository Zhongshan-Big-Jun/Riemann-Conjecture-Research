# SL lemma probe — random-Gram model identification (manager, 2026-08-15)

Status of the conditional 100% theorem (condp1 run): `HL* ∀k0 + SL ⇒ sup_{λ<1} liminf_T
N0^s_λ/N = 1` (ε-form, audited F-1 repair). The single open ingredient is **SL**: the
sine-kernel Gram spectral measure has no mass gap at 0 (Christoffel form: Λ_m(0) → 0).
This probe (5th literature/analysis pass) tests which concrete model the "sine-kernel Gram
matrix" of HL* is, using the audited moment list (m₁, m₂, m₃, m₄) = (1, 4/3, 2, 13/4)
(Lemma C exact; m₃, m₄ previously "numerical Monte-Carlo (CUE) only").

## 1. Fixed-lattice (Toeplitz) model — ELIMINATED

Naive model: G_N = (sinc(i−j))_{i,j=0..N−1}, sinc(t) = sin(πt)/(πt). Computation:
sin(πk) = 0 for every k ∈ ℤ∖{0} ⇒ **G_N = I_N (identity)**. Eigenvalues all 1; moments all 1;
spectral measure δ₁ (0 ∉ support — SL fails in the strongest sense, but the model is
trivial). Verified numerically (N = 1500, all eigenvalues 1.000… to 1e-13).
The "Toeplitz symbol = 1_{|θ|≤1/2}" intuition is a Poisson-summation artefact: the Fourier
series of the sampled sequence {sinc(k)} is identically 1 (the "half-band" endpoint W = 1/2
of discrete-prolate theory degenerates — consistent with Slepian DPSS literature).
**Conclusion: the fixed-lattice Gram is irrelevant; HL*'s "sine-kernel Gram" cannot be
this.**

## 2. Random-Gram model (sine process on its own points) — m₂ = 4/3, m₃ = 2 EXACT

Model: sine process with kernel K(x,y) = sinc(x−y) on a window [0,L], N ≈ L points
{xi}; Gram matrix G_ij = K(x_i, x_j). DPP factorial-moment structure (ρ₂ = 1 − K²,
ρ₃ = det(K(x_a,x_b))_{3×3}, all exact for DPPs) gives, with c_p = ∫_ℝ sinc(u)^p du:

- c₂ = 1 (Parseval: sinc ↔ 1_{[−1/2,1/2]}).
- c₄ = 2/3 (B-spline convolution: (1_{[−1/2,1/2]} ∗ 1_{[−1/2,1/2]} ∗ 1_{[−1/2,1/2]} ∗
  1_{[−1/2,1/2]})(0) = (tri ∗ tri)(0) = ∫ tri² = 2∫₀¹(1−t)²dt = 2/3).
- **E[m₂] = 1 + (c₂ − c₄) = 1 + 1/3 = 4/3 — EXACTLY the audited Lemma C value.** (Derivation:
  E tr G² = Σ_i G_ii² + E Σ_{i≠j} K_ij²; G_ii = K(x_i,x_i) = 1; E Σ_{i≠j}K_ij² = ∫∫ K²ρ₂ =
  L(c₂ − c₄) per unit length.) Numerics: c₂ ≈ 0.99953, c₄ ≈ 0.666667 (quadrature tails;
  consistent).
- **E[m₃] = 2 — EXACT.** (E tr G³ = N + 3·E Σ_{i≠j}K_ij² + all-distinct term; all-distinct =
  ∫∫∫K_xyK_yzK_zx·ρ₃ with ρ₃ = 1 − a² − b² − c² + 2abc (a,b,c the three cycle edges);
  per-unit: [⟨sinc, sinc∗sinc⟩] − 3[⟨sinc³, sinc∗sinc⟩] + 2[⟨sinc²∗sinc², sinc²⟩] = 1 − 3c₄
  + 2·∫tri³ = 1 − 2 + 2·(1/2) = 0. Uses sinc∗sinc = sinc (idempotent symbol), ∫tri³ = 2/4
  = 1/2.) Previously "numerical MC ≈ 2" — now exact under the random-Gram model.
- **E[m₄] = 3 + all-distinct₄** where all-distinct₄ = 1 − 4U − 2V + 8X + 2Y₁ + Y₂ − 4Z₁ −
  2Z₂; U = c₄ = 2/3 and V = c₅ = 19/32 EXACT (c₅ = ∫tri·B₃, B₃ the cubic B-spline: 2(49/192
  + 1/24) = 57/96 = 19/32); X, Y₁, Y₂, Z₁, Z₂ are 3-dim absolutely-convergent sinc-product
  integrals (box-convolution polytope volumes), Monte-Carlo estimates at 8e7 samples:
  X ≈ 0.51495, Y₁ ≈ 0.45355, Y₂ ≈ 0.38745, Z₁ ≈ 0.37977, Z₂ ≈ 0.41025 ⇒ all-distinct₄ ≈
  0.2204, **E[m₄] ≈ 3.2204 vs target 13/4 = 3.25 — within MC noise (σ ≈ ±0.05–0.2),
  INCONCLUSIVE; exact values = polytope volumes, pending** (each is a volume of a
  4-dim polytope {boxes with linear constraints}; exact rationals computable by
  vertex enumeration — next round).

## 3. SL consequences

- The random-Gram model reproduces the audited moments m₂ = 4/3, m₃ = 2 exactly ⇒ it is
  the right identification for HL*'s "sine-kernel Gram moments" (stronger than before:
  m₃ upgraded from MC to exact under the model).
- SL (Christoffel form) ⟺ limiting spectral measure μ of the random sine-Gram satisfies
  μ({0}) = 0 and 0 ∈ supp μ. This is a statement about a random (non-Toeplitz) Gram matrix
  of a determinantal point process; no theorem found in the literature (5th pass:
  "Gram matrix determinantal point process empirical spectral distribution limit",
  "sine kernel random Gram matrix eigenvalues" — hits were completeness of random
  exponentials (Ghosh), Sine_β characteristic polynomials (Chhaibi–Hovhannisyan–Najnudel–
  Nikeghbali–Rodgers), DPSS/prolate spectrum (Slepian; Bonami–Jaming–Karoui) — none states
  the needed spectral measure). **SL remains open, now precisely located: the limiting
  spectral measure of the random sine-process Gram matrix.**
- Refinement of the failure-mode dichotomy in condp1's remark: "mass gap at 0" must be
  read as μ({0}) > 0 OR 0 ∉ supp μ — atoms count (the fixed-lattice identity model would
  fail via μ = δ₁, i.e., 0 ∉ supp; the Toeplitz-type (δ₀+δ₁)/2 model, had it existed,
  would fail via μ({0}) = 1/2 > 0 — neither is the random-Gram model).

## 4. Literature anchors (5th pass, 2026-08-15)

- Slepian DPSS / prolate matrix theory (half-band degeneracy consistent with §1):
  https://ccrma.stanford.edu/~jos/sasp/Slepian_DPSS_Window.html ;
  https://www.emergentmind.com/topics/discrete-prolate-spheroidal-sequence
- Sinc-kernel operator spectrum, non-asymptotic: Bonami–Jaming–Karoui,
  https://hal.science/hal-01756828v1 (Zbl 1461.81040).
- Random point fields / DPP background: https://www.cambridge.org/core/books/abs/random-matrices-high-dimensional-phenomena/random-point-fields-and-random-matrices/3ABEF2AA9A747C36EA24E51CDFE23EE8
- No source found stating the limiting spectral measure of the random sine-process Gram
  matrix; the SL lemma (as needed by the theorem) remains an open (likely true) lemma.

## 5. Next steps

- Exact m₄ via polytope volumes (X, Y₁, Y₂, Z₁, Z₂) — tests 13/4 exactly; if it lands on
  13/4, the full moment list (1, 4/3, 2, 13/4) is exact under the random-Gram model.
- Search pass 6: "spectral measure random Gram matrix determinantal process sine" with
  different phrasing; also check the Christoffel-function literature for the sine process
  (christoffel function sine process zeros) — the Christoffel function of the sine process
  on a window is related to prolate-type determinants.
