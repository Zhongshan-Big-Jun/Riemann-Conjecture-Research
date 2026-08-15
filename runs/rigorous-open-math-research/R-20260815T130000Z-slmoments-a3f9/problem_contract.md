# Problem Contract — SL lemma: exact/numerical progress on the moment route (pass 8)

Run: `R-20260815T130000Z-slmoments-a3f9`
Task: this bounded pass makes concrete progress on the EXACT-MOMENT route that closes SL
(the no-mass-gap / no-atom-at-0 property of the sine-process Gram limiting spectral measure μ_λ).
Predecessor run: `R-20260815T120000Z-sllemma-7b21e4` (RIGOROUS_PARTIAL_RESULT). Status target:
honest label from {NUMERICAL_EVIDENCE, RIGOROUS_PARTIAL_RESULT, BLOCKED_REDUCTION}.
It is a *research-pass* artifact; it records progress, evidence, and the exact remaining gap.
NO numerical evidence is presented as proof.

## 0. Object and standing facts (accepted; from problem_contract of run 7b21e4 and the probe)

- **SL** (as the condp1 theorem needs it): the limiting spectral measure μ_λ of the random
  sine-process Gram matrix satisfies **μ_λ({0}) = 0** (no atom at 0), equivalently the
  Christoffel/Hankel criterion Λ_m(0) = det(H_m)/det(H_m^{(00)}) → 0 as m→∞.
- Moment sequence (trace-normalized, m_0 = 1 total mass, m_1 = 1): (m_0,m_1,m_2,m_3,m_4) =
  (1, 1, 4/3, 2, 13/4) EXACT (accepted project facts; probe §2).
- Exact shape decomposition (probe §2): m_k = 1 [all-equal] + repeated-index shapes
  (B-spline integrals c_{2n} = ∫sinc^{2n}; c_2=1, c_4=2/3, c_6=11/20, S_3=1/15) + **D_k**
  (all-distinct interaction terms). Known: D_3 = D_4 = 0. c_6=11/20 (corrected value).
- **Fermionic/Wick conjecture**: D_k = 0 for ALL k ≥ 3. If true, m_k is a computable sum over
  set partitions with block size ≤ 2, weighted by c_{2n}-type B-spline integrals → exact high
  moments → Hankel ratio → SL.
- Trustworthy numerics: the projection-DPP discretization (probe report §2) reproduces
  (1, 4/3, 2, 13/4) with h→0 bias. A previous hand-rolled sampler (7b21e4) was DEFECTIVE and
  was discarded; it is not reused.

## 1. This pass's questions

1. (Numerical, evidence) Measure D_5 and D_6 via the validated projection-DPP discretization:
   are they consistent with 0 within MC error? Sanity-check the sampler against m_2=4/3,
   m_3=2, m_4=13/4 first (hard gate) and against D_3=D_4=0.
2. (Exact) Compute m_5 (and m_6 if feasible) via the DPP factorial-moment structure
   (ρ_5 = det K)_{5×5}, 120 terms; the all-distinct 5-cycle may simplify as D_3=D_4=0 did.
3. (Hankel) Combine exact/probed m_5..m_8 with exact m_1..m_4; evaluate Λ_m(0) for m=1..4
   (exact rationals) and higher (mpmath); look for a decay pattern consistent with Λ_m(0)→0.
   Evidence only.
4. (Lemma) If D_5=D_6=0 (+ exact matching-sum for m_5 works), formulate the lemma that would
   close SL (matching-sum formula + Hankel decay), mark unproven steps explicitly.

## 2. Completion criteria for this bounded pass

Strongest audited progress, honestly labeled. Acceptable:
- A faithful validated sampler (Gate A exact-joint + Gate B exact moments) — done → enables
  trustworthy D_k evidence.
- D_5/D_6 measured consistent with 0 (evidence), recorded.
- Exact m_5 / D_5 via ρ_5 computed (or a precise reduction to computable form).
- Extended-moment Hankel test showing Λ_m(0) decay pattern (evidence).
- Exact remaining gap stated (the fermionic identity / a proof that D_k=0 and that the
  matching-sum sequence has Λ_m(0)→0).

A full proof of SL is NOT expected this pass; that is the long-term goal.

## 3. Honest epistemic limits
- Numerical D_k ≈ 0 and exact-integral D_5 ≈ −1e-4 are EVIDENCE, not a proof.
- The exact rational D_5=0 (or a proof that the box-spline sum vanishes) is NOT closed this pass.
- All hard epochal claims remain as in pass 7b21e4 (T0/T1 rigorous; gap T2 = prove Λ_m(0)→0).
