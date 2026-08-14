# Status and Literature — R-20260814T041219Z-condp1-698ec7

## 1. Problem status

Target `lim_{T→∞} N0^s(0,T)/N(0,T) = 1` is **OPEN unconditionally**. This run produced a
**RIGOROUS_PARTIAL_RESULT**: a rigorous conditional theorem (HL* ∀k0 + spectral lemma SL ⇒ 100%)
and an exact resolution of the moment-list inconsistency §7.2(f).

## 2. Exact known unconditional bounds (must not be contradicted)

| Quantity | Best bound | Source |
|---|---|---|
| liminf N0*/N (distinct on-line) | ≥ 3/2 − (1/√2)cot(1/√2) = 0.67250… (and = 0.67250 for N0^s) | Claude v2 Theorem D §7.1; Lean `thmD₀`, `thmD₀_simple` |
| liminf Nd/N | ≥ (3 − 1/c₁*)/2 = 0.83625… | Claude v2 Thm D; Lean `thmD₀_dist` |
| liminf N0^s/N (Cauchy–Schwarz route) | ≥ 2c₁* − 1 = 0.50659… | Lean `thmD₀_simple` (weaker CS form) |
| bandwidth-one certificate ceiling | ≈ 0.68185 (any window, any #moments via Prop 4.1 class) | v2 §1.1/§7.5(b); Prop 7.4; pair `CeilingLaw256` |

Constants (Lean `ThmD/Final.lean`, lines 10–19): c₁* = √2 tan(1/√2)/(1 + tan(1/√2)/√2) = 0.75329…,
HD 1 = 2 − 1/c₁* = 3/2 − cot(1/√2)/√2 = 0.67250…, distinct = (3−1/c₁*)/2 = 0.83625…, CS = 2c₁*−1 = 0.50659.
Convention: 1/c₁* = 1.32751… = the (optimal-window, λ=1) HS-ratio R(ψ_MT); base-profile ratio
R(ψ0) = (1/λ₁+λ₁/3) → 4/3.

## 3. Moment/Christoffel exact facts (this run)

- True sine-kernel-Gram 2nd moment m_2(1) = **4/3** (exact, Lemma C). Unconditional counterpart:
  trĜ²/trĜ → (1/λ₁+λ₁/3) → 4/3 (Theorem 5.8).
- The printed §7.2(f) list (1, 3/4, 2, 13/4) is **not a valid probability-moment sequence**
  (m_2 − m_1² = −1/4 < 0). Corrected list **(1, 4/3, 2, 13/4)** is valid (m_2 − m_1² = 1/3 > 0,
  leading Hankel det 5/108 > 0).
- Under the corrected list, Λ_2(0) = **5/36** and 1 − 2Λ_2(0) = **13/18** (exact).
- m_3 ≈ 2, m_4 ≈ 13/4: numerical (CUE) corroboration only.

## 4. Literature and the moment route

- **Reduced higher-moment evals.** vi v2 §5 (diagonal method + Montgomery–Vaughan) evaluates
  tr Ĝ^k exactly in the Rudnick–Sarnak range kλ<2 [RS96]; for λ∈(1/2,1) this is at most k=3 (λ<2/3).
- **k=4, λ>1/2** would need the Hardy–Littlewood-type additive correlation
  Σ_m (Λ∗Λ)(m)(Λ∗Λ)(m+h), |h| ≤ X²/T; conjectural, this is exactly the content of HL*_4 (v2 §7.2(f)).
- **GLSS25 / GS Theorem 5** (PCC, full support ⇒ 100% simple on line): complementary sufficient
  hypothesis, different route; see §6 of candidate_proof.md. Novety risk: the HL*-conditional
  100% is already informally in v2 §7.2(f); our contribution is the rigorous form + the
  inconsistency fix + the explicit spectral-lemma gap.

## 5. The single missing (in-literature) spectral fact: **SL**

Neither v2 (which labels §7.2(d)–(f) "informal") nor the sources we could verify state a theorem
that the limiting spectral distribution of the sine-kernel Gram matrix has **0 strictly inside its
support** (positive density at 0 / no mass gap), equivalently that its Christoffel function at 0
vanishes, Λ_m(0)→0. That is the clean lemma our convergence theorem (§5) requires. It is plausible
(the sine kernel is a positive definite projection-type kernel, so Gram realizations are PSD and
small eigenvalues should accumulate at 0) but we found no citable theorem. We therefore label it
**SL** and make the 100% theorem explicitly conditional on it.

## 6. Novelty/risk

- The conditional "HL* ⇒ 100%" is informal prior (v2 §7.2(f), GLSS route §7.2(f)); our contribution:
  (a) precise HL* formulation with uniformity/window semantics; (b) the SOS-witness Christoffel
  bound (new, self-contained, generalizes Lemma 3.3); (c) exact resolution that the printed moments
  are inconsistent / the corrected list restores the paper's own Λ_2(0)=5/36 & 13/18; (d) explicit
  theorem conditional on the clean SL rather than an unspecified "spectral fact".
- No claim of unconditional 100%; the unconditional 2/3-vs-0.6818 gap is structural (§7.5).
