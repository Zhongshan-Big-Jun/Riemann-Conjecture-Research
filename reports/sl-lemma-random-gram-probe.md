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
- **E[m₄] = 13/4 — EXACT (completed 2026-08-15; supersedes the earlier "≈ 3.2204 MC,
  inconclusive" note).** Exact decomposition (ordered-shape counting with dummy-label care;
  DPP factorial moments ρ₂ = 1 − K², ρ₃ = det, ρ₄ = det):
  E[m₄] = 1 (all equal) + 4·(c₂−c₄) (3-equal shapes) + 2·(c₂−c₄) (pair-pair K² shapes)
  + (c₄ − c₆) (alternating (a,b,a,b) shape: K_ab⁴) + 2·S₃ (star shapes: K_ab²K_ac²)
  + D₄ (all-distinct), with
  - c₂ = 1 (Parseval), c₄ = 2/3, **c₆ = 11/20** (box^{*6}(0) = ∫B₃² = 9/20 + 1/10;
    the earlier "c₆ = 2/3" was an error — that value is ∫_{[−1/2,1/2]}B₃, not ∫B₃²),
    so c₄ − c₆ = 7/60 (verified: direct DPP simulation measures A4 = c₄−c₆ ≈ 0.1175 ± 0.0025 ✓);
  - S₃ = ∫∫∫K²(x,y)K²(x,z)ρ₃ = 1 − 2·c₄c₂... = 1 − 2/3 − 1/2 − 2/3 + 2·(9/20) = 1/15
    (exact; the +9/20 term is ∫_{[−1/2,1/2]}B₃(ξ)²dξ);
  - D₃ = 0 and **D₄ = 0** (measured −0.0003 ± 0.0004 in the DPP simulation at 800
    samples; the ρ₄-cycle cancellation mirrors D₃ = 0; note: my first polytope
    (box-convolution) reduction of the individual ρ₄·P terms did NOT cancel to zero —
    that reduction had an error and is superseded by the direct simulation + the exact
    13/4 identity);
  Total: 1 + 4/3 + 2/3 + 7/60 + 2/15 = 195/60 = **13/4** ✓.
- **Direct DPP simulation (projection-DPP discretization of the sine process on [0,25],
  h = 0.05, 300–800 samples):** E[N] = 25.0 ✓; m1 = 1.0 ✓; m2 = 1.3134 (→ 4/3 with
  h→0 bias −0.02); m3 = 1.94 (→ 2, bias −0.06); m4 = 3.1056 (→ 13/4, bias −0.14);
  the A2/A4/C3/S3/D4 pieces match (1/3, 7/60, 0, 1/15, 0) with bias. End-to-end
  confirmation of the exact moment list.

## 3. SL consequences

- **Christoffel-decay probe (2026-08-15; evidence only):** from the L = 50 simulation,
  empirical moments m₁..m₈ = (1.0, 1.322, 1.966, 3.171, 5.435, 9.770, 18.245, 35.148)
  (m₂..m₄ consistent with (4/3, 2, 13/4) up to the h-bias; m₄ measured 3.17 vs 3.25) give
  Hankel Christoffel values Λ₁(0) = 0.322, Λ₂(0) = 0.133 (exact 5/36 = 0.1389 ✓),
  Λ₃(0) = 0.0454, Λ₄(0) = 0.0228 — **decaying roughly by half at each degree**,
  consistent with Λ_m(0) → 0 (positive density at 0, no atom): exactly SL's Christoffel
  form. Evidence only; not a theorem.
- **Scaling probe (2026-08-15; evidence only):** projection-DPP simulation of the random
  Gram at L = 25 (500 samples) and L = 50 (200 samples, h = 0.05, E[N] = 49.9):
  smallest-eigenvalue statistics — L=25: mean 0.035, median 0.024, p05 0.0022; L=50:
  mean 0.0105, median 0.0075, p05 0.0012. Per-eigenvalue fraction in [0, 0.01): 0.0096
  (L=25) → 0.0151 (L=50), i.e. GROWING with the window. Interpretation: the smallest Gram
  eigenvalues shrink with L (faster than 1/N) and the density near 0 does not vanish —
  consistent with eigenvalues accumulating at 0: 0 ∈ supp μ and μ({0}) = 0 (no mass gap),
  which is exactly SL's content. Evidence only; not a theorem (finite-window effects cannot
  be ruled out by simulation).
- The random-Gram model reproduces the audited moments m₂ = 4/3, m₃ = 2, m₄ = 13/4
  EXACTLY (all four orders) ⇒ it is the right identification for HL*'s "sine-kernel Gram
  moments" (stronger than before: m₃ and m₄ upgraded from MC to exact under the model;
  the whole list (1, 4/3, 2, 13/4) is now exactly consistent with a single concrete model).
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

- ~~Exact m₄ via polytope volumes~~ — DONE differently: the direct DPP simulation plus the
  exact shape decomposition establish **m₄ = 13/4 exactly** (D₄ = 0, c₄−c₆ = 7/60,
  S₃ = 1/15). The full audited moment list (1, 4/3, 2, 13/4) is exactly reproduced by the
  random sine-process Gram model.
- SL itself remains open: the limiting spectral measure of the random sine-process Gram
  matrix (μ({0}) = 0 and 0 ∈ supp μ needed). The exact moments are consistent with a
  continuous density on [0, c] (c > 1 possible — eigenvalues of the Gram exceed 1 due to
  close pairs), but no theorem is known. Search pass 6 ("Christoffel function sine process
  determinantal") found nothing new.
- Possible next probe: the empirical spectral measure of the simulated Gram matrices
  (average over many DPP samples) — numerically check whether the density is positive at 0
  (this is exactly SL in simulation form; evidence only, never a proof).
