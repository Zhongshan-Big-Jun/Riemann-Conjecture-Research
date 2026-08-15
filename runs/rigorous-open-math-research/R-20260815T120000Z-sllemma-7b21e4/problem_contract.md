# Problem Contract — Spectral Lemma (SL) of the sine-process Gram matrix

Run: `R-20260815T120000Z-sllemma-7b21e4`
Task: the single open ingredient **SL** in the conditional "probability 1" theorem of
run `R-20260814T041219Z-condp1-698ec7`. Skill: `rigorous-open-math-research`.
Status target: bounded research pass; deliver strongest audited progress (proof, reduction,
or precise missing ingredient). NO numerical evidence is a delivery.

## 0. Context (exactly how SL enters the theorem)

The condp1 theorem (candidate_proof.md §5, audited F-1) proves:

> **HL\*(k0,λ all, all λ<1) + SL(λ all) ⇒ sup_{λ<1} liminf_{T→∞} N0^s_λ(T,2T)/N(T,2T) = 1.**

The proof uses SL via Lemma 3.B (Christoffel bound): for the limiting spectral measure μ_λ on
[0,∞) with orthonormal polynomials q_0,q_1,… and Christoffel-Darboux kernel
K_m(0,0) = Σ_{j=0}^m q_j(0)², we have μ_λ((0,∞)) ≥ 1 − Λ_m(0), Λ_m(0) := 1/K_m(0,0).
SL supplies **Λ_m(0) → 0** as m→∞, which forces μ_λ((0,∞)) = 1 (no atom at 0) and pushes the
Christoffel bound to the sharp ceiling. SL is NECESSARY for this route (Remark §5).

The object: **the limiting spectral measure of the random sine-process Gram matrix.**

## 1. The exact object (rebuild of the identification; from sl-lemma-random-gram-probe.md and condp1 §2/candidate §2)

Let the **sine kernel** be K(x,y) := sinc(x−y) := sin(π(x−y))/(π(x−y)) (K(x,x)=1 by continuity).
Let (Ω,P) carry the **sine point process**: the determinantal point process (DPP) on ℝ with
kernel K, intensity 1, correlation functions
  ρ_k(x_1,…,x_k) = det[ K(x_a,x_b) ]_{a,b=1..k}   (exact for a DPP).
For a growing window [0,L] (L→∞), let {x_i} be the ⊂[0,L] points, N_L := #{i}. By DPP theory
E N_L = ∫_0^L K(x,x) dx = L (intensity 1), and N_L ≈ L with fluctuations ~√L.

Define the random **Gram matrix** G_L := (G_ij)_{i,j=1..N_L}, G_ij := K(x_i, x_j). G_L is
real symmetric, a.s. positive semidefinite (Gram matrix of a kernel whose operator is PSD —
the sine kernel is a positive-definite type projection kernel). Its entries are 1 on the
diagonal. Its empirical spectral measure (dirac normalization by N_L)
  μ_L := (1/N_L) Σ_{i=1}^{N_L} δ_{λ_i(G_L)},
where λ_i(G_L) are the eigenvalues in nonincreasing order.

**Established exact moments (audited, accepted project facts — re-check vs probe report; this is
E[m_k] := E[(1/N_L)tr G_L^k], k = 1..4, in the bulk L→∞, N_L≍L):**
  E[m_1] = 1,  E[m_2] = 4/3,  E[m_3] = 2,  E[m_4] = 13/4.
These come from the DPP factorial-moment structure (ρ_2 = 1−K², ρ_3 = det, ρ_4 = det) and the
sine-kernel integrals c_2 = 1 (Parseval), c_4 = 2/3, c_6 = 11/20, S_3 = 1/15, D_3 = D_4 = 0.
(The probe derives these EXACTLY under this model; m_2=4/3 also = the paper's unconditional
HS ratio R(ψ0), and the whole corrected list (1,4/3,2,13/4) is exactly reproduced.)

**Task-relevant statement to prove (SL).** For each λ ∈ (0,1): the limiting spectral distribution
μ_λ of the sine-kernel Gram matrix is supported on [0,∞) and has **no mass gap at 0** in the
Christoffel sense:
  SL(λ):  lim_{m→∞} 1/K_m^λ(0,0) = 0,   K_m^λ(0,0) := Σ_{j=0}^{m} q_j^λ(0)²,
where q_j^λ are the orthonormal polynomials of μ_λ. Equivalently:
  (i) μ_λ({0}) = 0   (no atom at 0),  AND
  (ii) 0 ∈ supp μ_λ  (equivalently μ_λ admits no mass gap separating 0 from the bulk, i.e.
       μ_λ([ε,∞)) → 1 as ε→0⁺).

## 2. Where the λ enters

HL* (condp1 §2) defines μ_λ as the law of the spectral measure of the scaled Gram matrix
`[ sin(πλ(x_i−x_j))/(πλ(x_i−x_j)) ]` on the intensity-1 sine process — i.e. the kernel is
sinc_λ(u) := sin(πλu)/(πλu), a lower-bandwidth (band [−λ/2,λ/2]) version. The limit regime is
L→∞ with N ≍ L. The theorem needs SL(λ) for all λ<1 (uniform role: the m→∞/SL passage precedes
the λ→1⁻ passage). At λ=1 this is sinc(u)=sin(πu)/(πu); the λ-family is the specialization to
bandwidth λ. By the DPP scaling/scaling-property of the sine process (self-similar: bandwidth-λ
sine kernel ⟺ intensity-λ′ reparameterization), proving SL at a generic bandwidth suffices if a
clean equivalence holds; this is part of the contract to reconstruct (see §4, "λ-reduction").

## 3. Completion criteria

A **complete solution** of SL: a rigorous proof of SL(λ) for all λ ∈ (0,1): μ_λ supported on
[0,∞), μ_λ({0}) = 0, and 0 ∈ supp μ_λ (equivalently Λ_m(0)→0), with every quantifier/domain/
regularity assumption explicit and no hidden regularity swap.

**Acceptable intermediate deliveries** (in decreasing order of value):
- a rigorous reduction of SL to a strictly smaller clean open statement (record it);
- exact higher-moment asymptotics m_k of the sine-Gram random model (any range) that, together
  with a Stieltjes/Carleman determinacy argument, would pin μ near 0;
- a correct proof that a specific relaxation of SL (that actually suffices for the theorem) is
  decidable/non-vacuous/true;
- the exact minimal missing ingredient, stated purely, with the chain SL ⟵ [that] ⟵ proven facts
  made explicit;
- the precise failure mechanism of each killed route (recorded), establishing that no easy route
  closes SL.

A **negative result** (SL false — a mass gap or atom) would also be a complete solution, but would
contradict the accepted moment model + numerical probes; must be cross-checked and would require
upending the condp1 theorem's SL leg.

## 4. Contract ambiguities to resolve before claiming anything

1. **Limit order / almost-sure vs in-mean convergence.** The theorem (§5) consumes only weak
   convergence of μ_λ^{(T)} ⇒ μ_λ and SL(λ) as a statement about the continuous-time limit μ_λ.
   For SL itself we need: does the empirical measure μ_L converge (a.s., or in probability, or in
   expectation of test functions) to a deterministic μ_λ as L→∞? The exact moments E[m_k] exist
   for each fixed k (expectation of the empirical measure's moments), but a.s./in-probability
   convergence and the identification of the a.s. limit is a genuine analytic question. The
   theorem only needs the *limiting* μ_λ to have the no-mass-gap property; prove whatever
   convergence is needed and state the mode.
2. **λ-reduction / self-similarity.** Is SL(λ) for a single λ (say λ=1) equivalent to SL(λ) for
   all λ<1? (sinc_λ(λu) = sinc(u) after scaling; the sine process DPP also scales). If yes the
   theorem's "for all λ<1" reduces to one bandwidth; if the needed m→∞ passage interacts with λ
   non-trivially, must state the precise domination.
3. **Normalization.** "supported on [0,∞)" is automatic (PSD) but "0 ∈ supp" is not; and
   "no atom at 0" is distinct from "positive density at 0". SL's Christoffel form Λ_m(0)→0 is
   equivalent to: probability measure, 0 not a point mass, and positive total mass arbitrarily
   close to 0 scaled correctly — reconstruct the precise equivalence and use the cleanest form.
4. **Dependency of columns.** The Gram columns are strongly dependent (sine DPP), so classical
   independent-columns random-matrix limits (Marchenko–Pastur) do not apply directly. Any
   comparison route must justify why a dependent-Gram limit nonetheless behaves like an MP-type
   limit near 0.

Contract v1. Reviewed against sl-lemma-random-gram-probe.md (re-read, §1-§3, §5) and condp1
candidate_proof.md §2-§5. Hash: see repro_manifest.
