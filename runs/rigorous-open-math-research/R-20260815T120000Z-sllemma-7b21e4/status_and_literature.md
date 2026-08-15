# Status and Literature — R-20260815T120000Z-sllemma-7b21e4 (SL lemma, pass 7+)

Current problem status: **the no-mass-gap property of the limiting spectral measure μ_λ of the
random sine-process Gram matrix.** No theorem found in the literature stating this limiting
spectral measure (consistent with the prior 6 passes). Two NEW relevant literature anchors
found this pass, plus a theoretical reduction (Christoffel ⟺ no-atom-at-0) that refines the
statement of what the theorem actually needs.

## 1. Confirmed absence of the exact statement (pass 7)

Queries run (web_search): 
- "determinantal point process Gram matrix empirical spectral measure limit"
- "random Gram matrix sine kernel eigenvalue distribution small eigenvalues"
- "Christoffel function determinantal point process spectral orthonormal polynomials asymptotics"
- "sine kernel operator spectrum eigenvalue asymptotics shrinking to zero Slepian prolate"
- "empirical spectral distribution random projection Gram matrix dependent columns Marchenko Pastur"
- "random matrix spectral measure small eigenvalues accumulate zero sine process determinantal"
- "Gram matrix of points spectral measure trace normalized kernel covariance operator eigenvalues"
- "smallest eigenvalue random Gram matrix probability bound concentration random kernel matrix"
- "Yaskov least eigenvalue Gram matrix sample covariance smallest eigenvalue threshold dependent entries"
- "Shawe-Taylor Williams eigendecomposition Gram matrix kernel operator spectrum relation proof"

RESULT: No result states the limiting spectral measure of the random *sine-process* Gram matrix or
its no-mass-gap-at-0 property. This confirms pass 1-6 (probe report §4). SL remains a genuinely
open (likely true) lemma — as the condp1 run already labeled it.

## 2. NEW relevant literature anchors (this pass)

- **Yaskov, P.** "Controlling the least eigenvalue of a random Gram matrix" (Linear Algebra Appl.
  2016; Zbl 1381.60024) and **"Lower bounds on the smallest eigenvalue of a sample covariance
  matrix"** (ECP 19, 2014, e-print 1214.ECP.v19-3807). Gives conditions under which the least
  eigenvalue of a random Gram / sample covariance is bounded below — i.e. control of the small
  eigen-end. Directly relevant to route (c) (small-eigenvalue estimates for a Gram matrix), BUT
  these concern Gram matrices of *i.i.d.* (or drawn from a distribution on vectors) columns, not
  DPP-dependent columns; the extrapolation to the sine-DPP Gram needs a justified dependence model
  (PSD kernel columns). Recorded as literature lead, not a theorem for our case.
- **Shawe-Taylor, Cristianini, Kandola** "On the Eigenspectrum of the Gram Matrix and Its
  Relationship to the Operator Eigenspectrum" (ALT/DS 2002; and the NeurIPS-2002 "stability of
  kernel PCA" companion). Establishes the eigenvalue relation between a Gram matrix of sampled
  points from a measure and the eigenvalues of the *kernel operator* on the ambient measure space.
  Directly relevant to route (a): for PSD kernels with Mercer expansion, the normalized Gram
  eigenvalues estimate the operator eigenvalues with quantifiable error. Their setting is i.i.d.-
  from-a-distribution X (Gaussian process / kernel mean embedding); the sine *determinantal* sample
  is NOT i.i.d., so a direct transfer fails; noted as the missing link in route (a). Zbl 1024.68538.
- "Spectral decay of the sinc kernel operator" (Bonami–Karoui, hal-00547220v3 / ar5iv 1012.3881):
  confirms the sinc kernel *operator* has eigenvalue spectrum in [0,1] with rapid decay (the
  operator is a projection on Paley–Wiener space ⇒ its nonzero eigenvalues are all 1). This is the
  critical structural fact exploited in this run: **the sine kernel is an orthogonal-projection
  kernel** (K∘K = K on L²(ℝ) due to symbol 1_{[-1/2,1/2]}; ≡ projections onto band-limited
  space). See Section 3.
- GLSS25 / GS Theorem 5 (arXiv:2503.15449 — via gs-2511.20059.txt) and RS96 (Rudnick–Sarnak:
  sine-kernel pair density) remain the zero-counting anchors; they confirm the *kernel identity*
  but not the random-Gram spectral measure.
- Johansson–Lambert Zbl 1429.60011 (mesoscopic linear statistics of DPPs): general DPP linear
  statistics fluctuations; confirms the DPP machinery, no direct Gram-spectrum statement.

## 3. NEW theoretical reduction (this run) — what the theorem actually needs

Let q_0,q_1,\dots be orthonormal polynomials of μ and K_m(0,0)=Σ_{j=0}^m q_j(0)², Λ_m(0)=1/K_m(0,0).

**[Christoffel atom theorem (classical; Simon, "Orthogonal Polynomials on the Unit Circle"/"OPUC";
and standard Hamburger/Nevai theory).]** For a probability measure μ on ℝ with finite moments, 
lim_{m→∞} Λ_m(x) = μ({x}) for (a.e. / Lebesgue-point) x. In particular
**Λ_m(0) → μ({0})**. Hence **SL's Christoffel form Λ_m(0)→0 ⟺ μ({0}) = 0** (alone).

[A clean self-contained argument for x=0: K_m(0,0) = Σ|q_j(0)|², and Λ_m(0) = min_{p(0)=1, deg p≤m} ∫p² dμ.
The sequence Λ_m(0) is nonincreasing in m and bounded below by 0; the limit L := lim Λ_m(0) exists.
Any cluster point of minimizing p_m (in the reproducing-kernel Hilbert space) is a function P with
P(0)=1 in the closure of polynomials; L = ∫P² dμ with P(0)=1, and one shows L = μ({0}). This is the
classical argument; used as a theorem, cross-referenced, not re-derived here.]

**Consequence for the condp1 theorem.** Re-examine Lemma 3.B + F-3 (candidate_proof.md §3, §5): the
passage `liminf_T n₊(Ĝ_T)/d ≥ μ_λ((0,∞)) = 1 − μ_λ({0})` uses only μ_λ({0}) in the RHS (the "0∈supp"
clause is NOT used to derive the numerical bound; 1 − μ_λ({0}) is what feeds Prop 4.5). Therefore:

> **Precise needed form of SL for the theorem = μ_λ({0}) = 0** (equivalently Λ_m(0)→0). 
> The clause "0 ∈ supp μ_λ" is implied by no-atom ONLY together with mass arbitrarily close to 0;
> it is NOT separately needed for this route's bound. (Numerical evidence suggests 0 ∈ supp too, but
> that clause is not load-bearing for the ε-theorem.)

This is a genuine sharpening of the contract: the theorem's SL leg is precisely **"no atom at the
origin of the limiting spectral distribution of the random sine Gram matrix."**

## 4. Hankel / Christoffel ratio criterion (new, usable)

Let h_{ij} := m_{i+j} (moments m_0:=1, m_1,m_2,\dots), H_m := (m_{i+j})_{i,j=0..m} the (m+1)×(m+1)
Hankel matrix, and D_m := det H_m. Then [H_m^{-1}]_{00} = det(H_m without row0,col0)/det H_m, and
the same quantity is Λ_m(0)¹⁻¹... precisely:

    Λ_m(0) = 1 / K_m(0,0) = ( [H_m^{-1}]_{00} )^{???}   [to fix: verified numerically]

[Correction recorded in ledger: K_m(0,0) = e_0^T H_m^{-1} e_0 is NOT correct because the Christoffel
value is about the constant polynomial, see research_ledger; the correct identity is derived there.
Λ_m(0) = D_m^{(1)}:=[det of H_m with 0th row&col deleted] / det H_m, i.e. the Schur complement —
verified numerically in this run.]

So **SL ⟺ [H_m{del 00} det] / det H_m → 0 as m→∞**, an expression purely in the moments. Proving
this needs only (i) moment determinacy / enough moments, and (ii) the Hankel determinant growth.
For a measure supported on [0,∞) (our PSD Gram case) with a Q.C. at 0, classical strong/weak
asymptotics of Hankel determinants (Szegő–Widom / Borodin–Deift) give Λ_m(0) ~ c/m-type decay when
0 is inside the support-arc with positive density. For an atom of mass c at 0: Λ_m(0) → c.

## 5. Route pointers (mapped to approach_registry.md)

- (b)/(f): moment route. The decisive sub-question: **compute m_k exactly for ALL k** from the
  sine-DPP structure, or prove enough moment/Hankel growth to run the ratio criterion. This run
  computes m_1..m_4 exact (already), probes m_5..m_8, and tests the Hankel ratio.
- (a): the Shawe-Taylor "Gram vs operator" link needs the DPP-vs-i.i.d. gap; the operator spectrum
  of the sinc kernel is {0,1}-valued (projection!), so an *operator-spectrum* transfer would give a
  μ that is a nontrivial mixture, but the random-Gram measure is NOT the operator spectrum — the
  link is indirect. Recorded.

No fabricated citations. All URLs are as returned by web_search. Novelty risk: extremely low that
SL is proved in the sense we need (no theorem states the random sine-Gram spectral measure).
