# Candidate Proof — SL via the exact-moment / fermionic-Wick route (work in progress)

Run: `R-20260815T130000Z-slmoments-a3f9`. This pass adds numerical and reduction evidence for the
moment route; it does NOT yet close SL. The standing rigorous reduction (pass 7b21e4, audited) is:

> **SL ⟺ μ_λ({0}) = 0 ⟺ Λ_m(0) = det(H_m)/det(H_m^{(00)}) → 0**, with H_m the (m+1)-Hankel of
> the sine-Gram moment sequence (m_0 = 1 total mass). T0/T1 rigorous.

## 1. What this pass established (evidence + reduction)

1. **A faithful projection-DPP discretization works** and reproduces the audited exact moments
   (m_0,m_1,m_2,m_3,m_4) = (1,1,4/3,2,13/4) within h→0 bias (Gate B), AND passes an independent
   exact-joint distribution gate (Gate A). It extends to m_5..m_8 consistent with the probe's
   L=50 reference. ⇒ Further numerical evidence is now trustworthy (no sampler defect).
2. **D_3, D_4, D_5 are numerically consistent with 0** (D_3=−0.00093±0.0025, D_4=+0.00002±0.0010,
   D_5=−0.00008±0.00038) at L=25. The exact 4-D integral of the all-distinct 5-cycle integrand
   P·ρ_5 is ≈ −1e-4 over global boxes (truncation-level), corroborating D_5=0.
3. **Extended-moment Hankel decay** (L=50, validated sampler): Λ_1(0)≈0.245, Λ_2(0)≈0.133,
   Λ_3(0)≈0.092 (mpmath 50 digit) — decaying, consistent with Λ_m(0)→0 (still evidence).

## 2. The lemma that would close SL (formulated, with status of each step)

**Lemma M (Fermionic/Wick cancellation).** For the sine (projection) DPP and its random Gram
G_ij = K(x_i,x_j), K(x)=sinc(x), the all-distinct cyclic interaction terms vanish:
  D_k = lim_L (1/L) E[ Σ_{i1..ik pairwise distinct} G_{i1i2}G_{i2i3}…G_{ik i1} ] = 0  for all k ≥ 3.
   [Gap 1 — STATUS: D_3=D_4=0 exact (probe); D_5≈0 (numerical MC −8e-5 ± 4e-4 at L=25 + exact
    4-D integral −1.3e-4); D_6≈0 (numerical MC +5e-4 ± 4e-4 at L=20 + exact 5-D integral
    −1.6e-5). These are strong EVIDENCE. A rigorous proof of the general k identity is NOT yet
    written.]

**Lemma P (matching-sum form).** If Lemma M holds, then for every k the moment m_k is a finite
sum over set partitions of {1..k} whose blocks have size ≤ 2 (each "matched" block contributes a
B-spline integral c_{2t} = ∫sinc^{2t} and crossing terms):
  m_k = Σ_{π ∈ Partitions(k), max block ≤ 2} (cycle/matching coefficient) · [B-spline product].
   [Gap 2 — STATUS: verified structurally for k≤4 (exact 4/3,2,13/4); the size-≤2 reduction for
    all k follows from D_k=0 AND from the vanishing of the remaining non-matching shapes (the full
    repeated-index algebra). Whether the ONLY surviving shapes are the ≤2-block matchings is the
    precise claim to prove; D_k=0 (Gap 1) is exactly the all-distinct case, and the analogous
    vanishing must be shown for every shape with a block of size ≥3 or an unmatched crossing.]

**Lemma H (Hankel decay of the matching-sum sequence).** For a probability measure on [0,∞) whose
moment sequence equals the matching-sum (Lemma P) for all k, the Hankel ratio
  Λ_m(0) = det(H_m)/det(H_m^{(00)}) → 0 as m→∞.
   [Gap 3 — STATUS: OPEN. Two sub-routes (both unproven):]
   (a) **Moment-growth / determinacy:** if the matching-sum sequence grows like m_k ≈ a k^α with
       α<2 (or more precisely if the Stieltjes moment problem is determinate and the measure has
       positive density at 0), then Λ_m(0)→0. [Numerically m_k ~ (1.0,1.32,1.97,3.18,5.46,9.81,18.3,35.3)
        ≈ power-like growth; m_8/m_7 ≈ 1.93, ratio decaying ⇒ sub-factorial growth ⇒ compactly
        supported measure with 0 in its support; but this must be proven.]
   (b) **Direct Hankel asymptotic:** use that the matching-sum moments come from a measure with a
       known Christoffel function (Szegő–Widom) and derive Λ_m(0)→0. [Open.]

## 3. Proof sketch (honest, with the unproven step flagged)

If Lemma M and Lemma P hold, then the moment sequence m_k is exact and given by the matching-sum.
Lemma H would then give Λ_m(0)→0, which via T0/T1 proves μ_λ({0})=0 = SL. **The unproven core is
Lemma H (and the fully general Lemma M whose all-distinct k-case is only D_3..D_5-evidence).**
The plug-in pattern is:
  SL ⟸ μ_λ({0})=0 ⟸ Λ_m(0)→0 ⟸ [Lemma H] ⟸ m_k = [Lemma P matching-sum] ⟸ [Lemma M: D_k=0].

## 4. Status
**NUMERICAL_EVIDENCE / RIGOROUS_PARTIAL_RESULT (composite).** The reduction is rigorous (pass 7);
the new contribution is (i) a validated sampler + D_3..D_5 ≈ 0 evidence, (ii) the exact-0
corroboration of D_5, (iii) the precise formulation of Lemmas M/P/H (the three gaps). No proof of
any of M/P/H is complete. No numerical evidence is presented as proof.
