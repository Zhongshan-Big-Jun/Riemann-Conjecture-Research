# Obligation Graph — R-20260815T120000Z-sllemma-7b21e4

Claims, dependencies, proof status. Target = SL: μ_λ({0})=0 (no atom) + 0∈supp for the random
sine-DPP Gram limiting spectral measure.

## Central claim (the deliverable's reduction)
**T0. [REDUCTION, PROVED RIGOROUSLY this pass]**
SL(λ) ⟺ lim_m Λ_m(0)=0 ⟺ μ_λ({0}) = 0.
  - T0a: Λ_m(0)→μ_λ({0})  [Christoffel atom theorem; anchors Breuer–Last–Simon Zbl 1198.42021,
    Lagomasino–Marcellán–Van Assche CMP] PROVED (references theorem).
  - T0b: the condp1 theorem's SL-leg uses exactly μ_λ({0})=0 (re-examined Lemma 3.B + F-3).
    PROVED (self-contained reading of candidate_proof.md §3/§5).
  - T0c: "0∈supp" is NOT load-bearing for the ε-theorem (needs no-atom only). PROVED (re-reading;
    counterexample C3 shows no-atom alone drives Λ_m→0 and the μ((0,∞))=1 bound).
  Deps: none open. Status: RIGOROUS.

## The moment/Hankel criterion
**T1. [CRITERION, rigorously correct + validated]**
Λ_m(0) = det(H_m) / det(H_m with 0th row&col deleted), H_m=(m_{i+j})_{i,j=0..m}.
  - Derivation: Λ_m(0)=min_{p(0)=1,deg≤m}∫p²dμ = 1/([H_m^{-1}]_{00}) = det(H_m)/det(minor00).
    PROVED (Schur complement of the Hankel moment matrix).
  - Validated: reproduces Λ_2(0)=5/36 EXACTLY from (1,4/3,2,13/4); matches atom→c, no-atom→0 on
    4 model measures. NUMERICALLY VERIFIED.

## The open sub-ingredient (what remains to close SL)
**T2. [OPEN — THE minimal missing ingredient]**
Showing det(H_m)/det(minor00) → 0 for the sine-DPP Gram moment sequence m_k(λ).
  This requires knowing the SINE-GRAM moments m_k (at least enough of them, or their full Hankel
  asymptotics). 
  - T2a: m_1..m_4 exact = (1, 4/3, 2, 13/4). ACCEPTED (probe + condp1; re-checked). 
  - T2b: exact m_5..m_∞ (or moment/Hankel growth): OPEN. The all-distinct terms D_3=D_4=0 are
    known; whether D_k=0 for all k (which would give a closed-form moment source) is UNVERIFIED.
  - T2c: empirical (L=50) Hankel-ratio Λ_1=0.111,Λ_2=0.0248,Λ_3=0.0064 (geometric decay, ~×5/deg) 
    consistent with no-atom. EVIDENCE ONLY.
  Deps: T2 → T0's "SL" direction. OPEN.

## Route status (approach_registry)
- Route B+F (moment→Hankel): the leader, T2 is its crux. Partial (T0,T1 done; T2 open).
- Route A (operator transfer): killed (C2: projection operator has no eigenvalues <1). 
- Route C (direct concentration): open, theoretical, literature is for i.i.d. columns (Yaskov),
  DPP-specific bound missing.
- Route D (MP comparison): open, dependence makes it inapplicable directly.
- Route G (disproof): no counterexample found; C1–C5 all consistent with SL.

**T3. [RESOLUTION (audit): moment-determinacy holds.]** For T0a's Christoffel-atom limit to apply,
μ_λ must be moment-determinate. The sine-Gram limit is compact-supported (PSD Gram of a bounded
kernel ⇒ eigenvalues in a compact [0,c]), and compact support ⇒ Carleman ⇒ moment-determinate.
So the determinacy condition is SATISFIED for μ_λ. A formal (Lean) proof that μ_λ is compact-
supported remains to be written, but the condition is no longer an open block. Kept as a standing
item to formalize, not a burden on the reduction.

## Overall status
RIGOROUS_PARTIAL_RESULT: SL is rigorously reduced to the moment-growth/Hankel question (T2),
the criterion is validated (T1), and the empirical moment structure is consistent with SL (T2c).
The exact high-moment computation (T2b) is the precise remaining gap; moment-determinacy (T3) is
an auxiliary item.
