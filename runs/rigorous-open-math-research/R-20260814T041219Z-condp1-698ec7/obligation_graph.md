# Obligation graph — R-20260814T041219Z-condp1-698ec7

Legend: ✅ proved this run · 🔶 proved with an explicit assumption (SL) · ⚠️ exact open gap /
hypothesis required · 🔎 evidence only · ⁉️ statement refuted / corrected · ❌ false as written.

## O1 — Baseline chain & Theorem D (packet O1)
- [✅] N0^s + o(N) ≥ 4trĜ − 2N − ‖Ĝ‖²_F → (2 − R(ψ))N  (Prop 4.4(ii); §1 candidate_proof)
- [✅] R(ψ0) = 4/3 (base window, unconditional m_2 = (1/λ₁+λ₁/3) at λ=1)
- [✅] R(ψ_MT) = 1/c₁*,  H_MT = 2 − 1/c₁* = 3/2 − (1/√2)cot(1/√2)  (v2 §7.1; Lean HD_one forms)
- [✅] c₁* = 0.75329…, CS-simple = 2c₁*−1 = 0.50659 (Lean Final.lean comment)
- Depends on: Prop 4.4(ii) [paper, Lean-endverified], Prop 5.3/Thm 5.8 [paper+Lean].

## O4-conditional / O5-D2 — hypothesis HL*(k0,λ)
- [✅] exact formulation (definition §2 candidate_proof): d^{-1}tr(Ĝ^k) = m_k(λ)+o(1), windows +
  uniformity, meaning of o(1).
- [✅] k=1,2 members are theorems (unconditional trace/HS data; m_1=1, m_2=4/3 at λ=1).
- [🔎] k≥3 conjectural; k=4,λ>1/2 ↔ Hardy–Littlewood-type additive prime correlation (HL*_4 content).
- Depends on: nothing proved inside; it is the hypothesis.

## O5-D3 — Christoffel-function bound
- [✅] Lemma 3.A SOS-witness higher-moment n₊-bound (any Hermitian R); recovers Lemma 3.3 (m=1).
- [✅] Lemma 3.B Christoffel bound 1−Λ_m(0) for a limiting PSD probability measure.
- [✅] Cor 3.C Prop 4.5 route: liminf N0^s/N ≥ 2(1−Λ_m(0))−1 at λ=1.
- Depends on: elementary (Cauchy–Schwarz, Christoffel function).

## O5-D4 — moments & 13/18 normalization gap
- [✅] m_2(1) = 4/3 exact (Lemma C); m_1=1.
- [⁉️] printed list (1,3/4,2,13/4) is NOT a valid probability-moment sequence (m_2<m_1²).
- [✅] corrected list (1,4/3,2,13/4): valid; Λ_2(0)=5/36; 1−Λ_2(0)=31/36; 13/18=2(31/36)−1 exact.
- [🔎] m_3≈2, m_4≈13/4 (CUE). **[F-4]** Exact closed forms for m_3,m_4 not needed for the *ε-theorem*,
  but the *values* m_3=2,m_4=13/4 DO enter Λ_2(0), so **13/18 is conditional on HL*_4** (not a
  free/closed computation). Open (not blocking).
- [✅] Structure: 13/18 = 2(1−Λ_2(0))−1 via Prop 4.5 (+ Prop 7.4 ceiling).

## O5-D5 — convergence (F-1-corrected: ε-form / iterated limit)
- [✅] HL* ∀k0 ⇒ μ_T ⇒ μ_λ (tightness + Carleman determinacy), under the standing regularity
  hypothesis **REG** = uniform spectral-radius bound for the sine-Gram compression (audit F-2;
  to be proved as Lemma R in a formalization pass; if unproved, moment-convergence alone suffices
  for the Christoffel bound).
- [✅] Cor 3.C + Λ_m(0)→0 ⇒ `liminf_T N0^s_λ/N ≥ 2(1−Λ_m)λ − 1` at each fixed λ<1.
- [🔶] REQUIRES **SL**: spectral density of sine-kernel Gram supported on [0,∞) (automatic: Gram is
  PSD) with 0 in support / Λ_m(0)→0. **SL is the exact missing-in-literature ingredient**; the
  proportion-1 statement is conditional on it.
- [✅] **[F-1 fix]** Conclusion is the ε-form/iterated limit `sup_{λ<1} liminf_T N0^s_λ/N = 1`
  (lim_{λ→1⁻} liminf_T after the m→∞/SL passage). NOT the plain `lim_T` at a single λ=1, which
  HL*'s λ<1 domain does not grant (fixed λ<1 has ceiling 2λ−1<1). HL*-at-λ=1, or λ=λ(T)→1 with λ-
  uniformity, would be needed for the plain T-limit.
- [✅] ceiling: n₊≤d (Prop 7.4) ⇒ no certificate in this class exceeds 100% at λ=1 (saturated only
  as λ→1⁻).

## O5-D6 — reconciliation
- [✅] GLSS25/GS Thm 5 (PCC full-support ⇒ 100%): complementary sufficient hypothesis, different
  route; no contradiction (our HL* + SL route also ⇒ 100%, differently).
- [✅] k=1 barrier: unconditional higher moments only for kλ<2; odd moments don't lower Λ_1(0);
  λ≤1/2 vacuous by Prop 7.4. Corrected m_2=4/3 ⇒ m=1 bound n₊/d ≥ 3/4, N0^s/N ≥ 1/2 (matches
  Lean CS 0.50659 after window optimization).
- [⚠️] GLSS25 primary source not bundled; quoted via GS Theorem 5 (packet O7, not fully discharged in this run).

## Open obligations (unresolved this run)
- ⚠️ **Prove/refute SL** (spectral data of sine-kernel Gram at 0). The single conditional weakening:
  without it the proportion-1 (ε-form) theorem is only "≥ m=1 bound" (≥ 1/2 with corrected m_2).
- ⚠️ Prove the regularity bound **REG** (uniform spectral-radius, F-2) to justify Carleman
  determinacy, and detail the 0-atom continuity step (F-3) in formalization (audit §3).
- ⚠️ Exact closed forms for m_3,m_4 of the sine-kernel Gram measure (would lift the "13/18
  conditional on HL*_4" caveat, F-4; not needed for the ε-theorem).
- ⚠️ Verify GLSS25 primary source (packet O7).
- ⚠️ Unconditional 100% remains OPEN (structural; not attempted beyond the conditional ε-theorem).
- ⚠️ Plain `lim_T N0^s/N = 1` at a single λ=1: would need HL*-at-λ=1 or λ=λ(T)→1 with λ-uniformity
  (not granted); open if that stronger hypothesis form is desired (F-1).
