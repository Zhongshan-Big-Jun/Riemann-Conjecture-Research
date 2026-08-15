# Problem Contract — SL gap G1: prove D_k = 0 exactly (all-distinct cyclic terms)

Run: `R-20260816T030000Z-slG1-9c2a`
Role: SOLVER for gap G1 (bounded research pass) under `rigorous-open-math-research`.
Status target: honest label from the protocol; no numerical evidence presented as proof.
Bounded budget ~2-3h effective.

## 0. Authoritative inherited context (from audited predecessor runs)

1. **SL reduction (audited, run R-20260815T120000Z-sllemma-7b21e4):**
   SL (the condp1 theorem's single open ingredient) is equivalent to μ_λ({0}) = 0
   (no atom at 0 of the limiting spectral measure of the random sine-process Gram
   matrix), equivalently to the Christoffel/Hankel criterion
     Λ_m(0) = det(H_m)/det(H_m^{(00)}) → 0.
   T0 (Christoffel-atom, moment-determinate via compact support) and T1 (Hankel
   criterion) are RIGOROUS. The remaining gap is T2: prove the Hankel ratio → 0.
   Exact known moment prefix (m_0=1 total mass, m_1=1): (1,1,4/3,2,13/4) for k=1..4.
   Exact: Λ_1(0)=1/4, Λ_2(0)=5/36.

2. **Moment route (run R-20260815T130000Z-slmoments-a3f9):**
   - Validated projection-DPP sampler (Gate A exact-joint, Gate B exact moments).
   - D_3 = D_4 = 0 exact; D_5, D_6 ≈ 0 (numerical MC and exact box-integral EVIDENCE,
     values ≈ −1e-4 residuals due to sinc-tail truncation).
   - Framework: Lemma M (D_k=0 all-distinct) → Lemma P (m_k = size-≤2 matching-sum)
     → Lemma H (Hankel → 0) → SL.
   - **Gap G1 (this run's target) = prove D_k = 0 EXACTLY for all k ≥ 3.** D_3, D_4
     exact; D_5, D_6 only evidence.

## 1. Exact object (this pass)

K(x) := sinc(x) := sin(πx)/(πx) (K(0)=1 by continuity); K is the orthogonal projection
onto Paley-Wiener (band-limited) functions; symbol 1_{[-1/2,1/2]}; K*K = K (idempotent).

The sine DPP on ℝ with kernel K has k-point correlation
  ρ_k(x_1,…,x_k) = det[ K(x_a,x_b) ]_{a,b=1..k}.

For points {x_i} of the sine DPP and the random Gram matrix G_{ij}=K(x_i-x_j), define the
all-distinct cyclic term
  D_k := lim_{L→∞} (1/L) E[ Σ_{i_1..i_k pairwise distinct} G_{i_1 i_2} G_{i_2 i_3} … G_{i_k i_1} ].
By DPP theory (distinct-index factorial sums) this equals the translation-normalized integral
  D_k = (lim 1/L)·∫_{[0,L]^k} P_k(x) ρ_k(x) dx = ∫_{ℝ^{k-1}} P_k(x)·ρ_k(x) dx₁…dx_{k-1}
        (fix x_k = 0 by translation invariance; P_k = ∏_{a} K(x_a−x_{a+1}), x_{k+1}:=x_1).

Expanding det[K(x_a,x_b)] = Σ_{π∈S_k} sign(π) ∏_a K(x_a−x_{π(a)}), so
  D_k = Σ_{π∈S_k} sign(π) I_π,
  I_π = ∫_{ℝ^{k-1}} [∏_a K(x_a−x_{a+1})][∏_a K(x_a−x_{π(a)})] dx₁…dx_{k-1}.

### Box-spline (Fourier/indicator) representation — the exact values
sinc(t)=∫_{-1/2}^{1/2} e^{2πiξt}dξ. Thus each I_π is the (2k−(k−1))-dimensional volume of
  I_π = vol{ ξ∈[−1/2,1/2]^{2k} : Σ_{e∋v} σ_{v,e} ξ_e = 0 for each vertex v }
        = box-spline value at 0 of the 4-regular combined graph (cycle ∪ π-edges),
where each vertex has degree 4 (2 cycle edges + 2 permutation edges). Each I_π is a
RATIONAL number (polytope/box-spline volume at a lattice point). D_3, D_4 are exact 0
by this structure; the task is D_5 (and general k).

## 2. Task (two prongs)

**Prong 1 — literature (divergent search, honesty rules):** search for an existing theorem
implying D_k=0 for the sine/projection DPP via the fermion/quasi-free/Wick structure, or
the trace-moment/matching-sum formula for quasi-free states. Exact statement + mapping if
found; otherwise record honest absence. Anchors to check: Soshnikov, Shirai–Takahashi,
Lyons–Steif, Johansson, "quasi-free CAR algebra state truncated functionals vanish".

**Prong 2 — exact D_5 attempt (compute):**
  (a) full expansion over S_5 — which permutation terms survive; Fourier support analysis;
  (b) a rigorous cancellation proof (Fourier/indicator structure; the D_3=D_4 pattern);
  (c) if general k, formulate Lemma M's proof sketch rigorously (Fourier-dual cancellation).
Use mpmath/sympy for exploration (evidence); the deliverable is a rigorous derivation or
the precise obstruction.

## 3. Completion criteria (bounded pass)

- Literature status recorded honestly (found-theorem-with-mapping OR honest absence).
- Exact D_5=0 proven, OR the precise obstruction (which identity missing).
- The general mechanism for D_k=0 stated precisely (Lemma M), with the exact identity to close.
- Compute exact high moments m_5.. if D_k=0 closes; test the Hankel decay (evidence only).
- All standard artifacts + SHA256SUMS + repro_manifest.

## 4. Epistemic limits enforced
- Numerical box-truncation residuals ≈ −1e-4 are NOT proof of 0; only exact/verified
  computation or a rigorous derivation is a result.
- No fabricated citations (every locator from an actual web_search result).
- No numerical evidence presented as a theorem.
