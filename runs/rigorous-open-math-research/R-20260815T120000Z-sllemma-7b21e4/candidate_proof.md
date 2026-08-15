# Candidate Proof — Spectral Lemma: reduction to the moment/Hankel question

Run: `R-20260815T120000Z-sllemma-7b21e4`. Status target: **RIGOROUS_PARTIAL_RESULT**.
This pass establishes a rigorous reduction of SL to a moment-growth/Hankel question, validates the
criterion against the audited exact value, and records the precise remaining gap. It does NOT close
SL. No numerical evidence is presented as proof.

## 1. The exact claim SL and its sharpened form

**CONVENTION (moment indexing — made explicit after adversarial audit).** The trace-normalized
sine-Gram moment sequence is (m_0, m_1, m_2, m_3, m_4) = (1, 1, 4/3, 2, 13/4), where m_0 = 1 is the
TOTAL MASS (μ_λ is a probability measure on [0,∞)) and m_1 = 1 = (1/N)tr G_L is the first trace
moment. The audited/probei list "(1,4/3,2,13/4)" means (m_1,m_2,m_3,m_4). Under this convention the
exact (rational) criterion values are Λ_1(0)=1/4, Λ_2(0)=5/36, with monotonicity (5/36<1/4) and
Cauchy–Schwarz (4≤13/3) satisfied — a mis-indexed reading that puts "1" in the m_0 slot and treats
4/3 as m_1 is NOT the correct reading and would (only then) appear inconsistent.

**object** (from problem_contract / probe): μ_λ = limiting spectral distribution of the random
sine-DPP Gram matrix (sine kernel K(x,y)=sinc(x−y), window [0,L], N≍L points, empirical measure
N⁻¹Σδ_{λ_i(G_L)}, λ a bandwidth parameter). G_L is a.s. PSD (Gram of a PSD projection kernel).

**SL (as needed by the condp1 theorem)** — Christoffel form:
  lim_{m→∞} 1/K_m^λ(0,0) = 0,  K_m^λ(0,0) := Σ_{j=0}^m q_j^λ(0)²,  (q_j orthonormal polys of μ_λ).

**Sharpened (T0).** SL ⟺ μ_λ({0}) = 0 (no atom at 0). In particular the condp1 theorem's SL-leg
uses EXACTLY the no-atom clause; the "0 ∈ supp" clause is not load-bearing for the ε-theorem.

Proof sketch (T0):
- (⇒, Christoffel atom theorem) For a **moment-determinate** probability measure μ on ℝ with finite
  moments, the Christoffel function Λ_m(0)=1/K_m(0,0) satisfies Λ_m(0) → μ({0}). [Invoke; anchors:
  Breuer–Last–Simon Zbl 1198.42021; Lagomasino–Marcellán–Van Assche, CMP. The determinacy condition
  is required because Λ_m depends only on the moment sequence; compact support (which ⇒ determinacy)
  holds for μ_λ, being the limit of PSD Gram measures with bounded eigenvalues ⇒ supp⊆[0,c].]
  Hence SL gives μ({0})=0.
- (⇐) If μ({0})=0 then Λ_m(0)→0 by the same theorem. So the two are equivalent.
- (Load-bearing clause) condp1 Lemma 3.B / candidate §5(ii) F-3 computes liminf_T n₊/d ≥ μ_λ((0,∞))
  = 1−μ_λ({0}); the right side uses ONLY μ_λ({0}). Prop 4.5 then yields the count. "0∈supp" never
  enters the inequality. [Verified against the quoted condp1 passage.] ∎

**Consequence:** the whole question of SL for the theorem collapses to **proving μ_λ({0}) = 0**
for each λ<1. This is a clean, minimal statement.

## 2. The moment/Hankel criterion (T1)

For a probability measure μ on ℝ with moments m_0:=1, m_1, m_2, …: 
  Λ_m(0) = det(H_m) / det(H_m^{(00)}) ,  H_m := (m_{i+j})_{i,j=0..m},  H_m^{(00)} := H_m without row0,col0.

Proof: Λ_m(0) = min_{p(0)=1, deg p≤m} ∫p²dμ = 1 / [H_m^{-1}]_{00} (quadratic-form min over the
affine constraint p(0)=1, i.e. the free coefficient =1); and [H_m^{-1}]_{00} =
det(H_m^{(00)})/det(H_m) (cofactor). Hence Λ_m(0) = det(H_m)/det(H_m^{(00)}). ∎

**Validated** (reproducibility/check_christoffel_criterion.py):
- Σ over model measures: atom-at-0 (Λ→c), no-atom (Λ→0) — confirms Λ_m(0)→μ({0}).
- From the exact sine-Gram list (1, 4/3, 2, 13/4): **Λ_2(0)=0.138888… = 5/36 EXACTLY**, matching
  the audited paper value. (reproducibility/check_hankel_from_moments.py)

Therefore SL ⟺ lim_m det(H_m)/det(H_m^{(00)}) = 0 for the sine-Gram moment sequence. This is a
pure moment-statements criterion: **SL is a statement about the moment sequence of μ_λ.**

## 3. The remaining gap (T2) — the minimal missing ingredient

To apply the criterion we must show the sine-Gram Hankel ratio → 0. This requires the moment
sequence m_k(λ) (or its Hankel asymptotics).

**Established (accepted project facts, re-checked):**
- m_1..m_4 = (1, 4/3, 2, 13/4) exact (probe §2; re-verified the m_3 decomposition matches).
- From the exact list the first two criteria values are Λ_1(0)=1/4, Λ_2(0)=5/36 (both > 0; no
  statement about the limit yet).
- DPP all-distinct interaction terms D_3=D_4=0 (probe). Whether D_k=0 for all k (giving a closed
  moment source) is UNVERIFIED (my attempt to extend Monte-Carlo was invalid — sampler defect, C5).

**Open sub-ingredient (precise):** prove that the sine-DPP Gram moment sequence m_k(λ) (k→∞)
satisfies det(H_m)/det(H_m^{(00)}) → 0. Concretely, any one of:
  (i) exact m_5, m_6, … via the DPP ρ_k-determinant shape decomposition, showing a growth/decay
      pattern that forces the Hankel ratio → 0;
  (ii) a moment-growth bound (e.g. m_{2k} growth slower than the sequence that would produce an
      atom), or a direct Hankel-determinant asymptotic;
  (iii) a positivity/edge argument showing mass of μ_λ accumulates at 0 (no atom, 0∈supp).
Any of (i)-(iii), made rigorous, closes SL via T1.

## 4. Empirical support (EVIDENCE ONLY, never proof)

From the probe's validated L=50 simulation moments (1.0,1.322,1.966,3.171,5.435,9.770,18.245,35.148),
the Hankel-ratio criterion gives (reproducibility/check_hankel_from_moments.py):
  Λ_1(0)=0.1110, Λ_2(0)=0.02476, Λ_3(0)=0.006414  —  geometric decay ~×5 per degree,
consistent with μ({0})=0 and hence with SL; also consistent with an MP-like square-root edge at 0
(the local density near 0 gives geometric Christoffel decay). This is simulation evidence ONLY;
it does not imply the theorem.

## 5. Honest status

**RIGOROUS_PARTIAL_RESULT.** This pass proved the reduction SL ⟺ μ({0})=0 ⟺ Hankel-ratio→0
(T0, rigorous) and the moment criterion (T1, rigorous + validated against exact 5/36). SL itself
remains OPEN, now precisely located: **prove the sine-Gram Hankel ratio → 0** (T2), equivalently
μ_λ({0})=0. The empirical moment structure is consistent with SL but is evidence only.

No complete solution is claimed; the quantifiers/domains are unchanged from the condp1 theorem's
SL statement (no silent relaxation of λ or regularity).

## 6. Provenance
All literature anchors and queries recorded in status_and_literature.md (pass 7). All code in
reproducibility/. No fabricated citations. The broken-sampler probe is recorded (C5) and excluded.
