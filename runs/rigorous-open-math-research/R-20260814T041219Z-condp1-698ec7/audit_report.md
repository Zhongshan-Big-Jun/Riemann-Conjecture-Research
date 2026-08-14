# Adversarial audit report — R-20260814T041219Z-condp1-698ec7

Auditor: fresh adversarial subagent (rigorous-open-math-research, Phase 8). The auditor did NOT
see the solver's conversation; conclusions rest solely on the artifacts in the run root and the
referenced literature (`literature/raw/claude-paper-main-v2.txt`, `zeta-23-lean/`, `gs-2511.20059.txt`).
Every numeric claim was re-derived independently (by hand and by new scripts), not by re-running the
solver's own code unchanged. The previously-present `audit_report.md` (the solver-authored self-audit,
a predecessor of this file) is archived at `audit_report.initial-race.md` (sha256
`F608FE7BBE70E0ACDD51EEBC4015309146F4135D2C0AFA39F4861EEE379FC26F`). Note: the earlier
empty-root FAIL report (sha256 `042ED9CD…`) is **not** present in this run root; the archived file
explicitly supersedes it. This file is the independent adversarial report. Auditor-added script:
`reproducibility/audit_independent_check.py` sha256
`2EEB5A00BE480B2A064910A763F03FECC2D66628C2520ADB7911071018F59DF2`. This file's own sha256:
`9CDB25E4796665084A7AE71D99FA48E56E6D30F3C477E86C027DF5A506508961`.

## 1. Verdict (headline)

**PASS-CONDITIONAL (F-gaps below are quantifier/nuance gaps, not algebraic errors).**
The three core derived facts are independently confirmed exactly:
- (i) Lemma C: `E[tr G_L²]/L → 4/3` for the sine-kernel Gram (correct).
- (ii) The printed `§7.2(f)` moment list `(1, 3/4, 2, 13/4)` is NOT a valid probability-moment
  sequence (2×2 Hankel det = −1/4 < 0); the corrected list `(1, 4/3, 2, 13/4)` is valid and gives
  exactly `Λ_2(0)=5/36, 1−Λ_2(0)=31/36, 2·(31/36)−1 = 13/18`. The claimed *transcription error*
  (m_2(1): 3/4 → 4/3) is verified against the actual printed text.
- (iii) Lemmas 3.A (SOS-witness), 3.B (Christoffel `1−Λ_m(0)`), and Cor 3.C (factor 2 route via
  Prop 4.5) are sound; the factor-2 form matches the ACTUAL Prop 4.5 statement.
- (iv) The Lean statement-fidelity claims are CORRECT (thmD₀_simple = CS 2c₁*−1 = 0.50659 vs
  thmD₀_simple_mult = rank-trace 2−1/c₁* = 0.67250).

**Single material gap (F-1 below):** §5's conclusion `lim_{T→∞} N0^s/N = 1` overstates the
quantifier reachable from HL*(all λ<1)+SL. The honest consequence is an ε-form/iterated limit, not
the plain λ=1 T-limit. This is the one place the theorem as written goes beyond its hypotheses.

## 2. Independent re-derivations (auditor, fresh)

2a. **Lemma C.** Sine DPP kernel K(u)=sinc(πu), 2-point intensity ρ_2(x,y)=ρ(x)ρ(y)−K(x−y)²=1−K²
(standard DPP/Fredholm identity). E tr G_L² = E[N] + E Σ_{i≠j}K² = L + ∫∫_{[0,L]²}(K²−K⁴)
= L + L(∫K²−∫K⁴)+o(L). With ∫sinc²(πu)du=1 (=(1/π)∫(sin x/x)² dx) and ∫sinc⁴(πu)du=2/3
(=(1/π)·(2π/3)), m_2=1+(1−2/3)=4/3. Boundary term ∫|u||K²−K⁴|du is O(1)=o(L) (|K|≲1/|πu|).
[Re-derived by hand; confirmed numerically by `reproducibility/audit_independent_check.py` (C)-(D).] ✓

2b. **Hankel + Λ_2(0).** (1,3/4,2,13/4): m_2−m_1²=3/4−1=−1/4<0 ⇒ not a positive-measure moment
sequence; its naive L² Christoffel Λ_2(0)=143/100>1 ⇒ 1−Λ_2(0)<0 (non-statement). By hand:
3×3 moment matrix [[1,1,4/3],[1,4/3,2],[4/3,2,13/4]], det=5/108, cof(M_00)=det[[4/3,2],[2,13/4]]=1/3
⇒ Λ_2(0)=det/cof=(5/108)/(1/3)=5/36. Confirmed independently by a *new* method
(min_{p(0)=1,deg≤2}∫p²dμ via rational linear system = 5/36; and Λ_1(0)=1/4 ⇒ 1−Λ_1(0)=m₁²/m₂=3/4).
Confirmed by the three run scripts. All three scripts ran (`py -3`, Python 3.10.11) and reproduced
the claimed outputs exactly. ✓ F-1 note: the m=2 bound and hence **13/18 genuinely depend on the
values m_3=2, m_4=13/4 entering Λ_2(0)**; those two are hypothesized/numerical, so 13/18 is
conditional on HL*_4 (see §7).

2c. **Lemma 3.A/3.B/Cor 3.C.** 3.A: p=t·r with r≥0 (SOS) gives p≥0 on λ>0 and p≤0 on λ≤0; so
Σ_{λ>0}p ≥ A_p (drop ≤0 terms) and Σ_{λ>0}p² ≤ B_p; Cauchy–Schwarz ⇒ n₊/d ≥ (A_p/d)²/(B_p/d),
(correct normalization, moments ≤2m). Correct as written. 3.B: min_{p(0)=1,deg≤m}∫p²dμ = 1/K_m(0,0)
(established by Cauchy–Schwarz in the orthonormal basis, equality case a_j∝q_j(0)); μ supported on
[0,∞) ⇒ μ((0,∞))=1−μ({0})≥1−Λ_m(0). Correct, with the "0 not an atom" continuity caveat (see F-3).
**Cor 3.C / factor 2:** the ACTUAL Prop 4.5 in the v2 text is
`N0^s(T,2T) ≥ 2 n₊^θ(G̃) − N(T,2T) − 2N(I′\I)` (eq. (4.8), lines 775–797) — the factor 2 is
**confirmed** verbatim. The paper's own §7.2(f) uses the same Prop 4.5 count and yields 13/18
(line 1654) and 100% (line 1655-1656). ✓

2d. **Main theorem §5.** (i) Tightness: bounded 2nd empirical moment + Markov ⇒ uniform mass decay
… yes (the prose `trĜ²/d²=m_2^{(T)}/d→0` is a red herring; the valid argument is m_2^{(T)}→m_2(λ)<∞
with Markov).(ii) Determinacy: Carleman requires moments bounded by C^k (compactly-supported limit),
which is **asserted** (spectral radius ≤ const for the sine-Gram/compression) but not proved in the
text; plausible from the projection-kernel structure but an unstated regularity fact — see F-2.
(iii)/(final): **F-1 — λ→1 quantifier gap** (below). ✓✗

2e. **Lean claims (task e).** Correct in full:
- `Zeta23/ThmD/Final.lean` line 119-124 `thmD₀_simple`: `(2·c₁*−1−ε)N ≤ N0simple` = 0.50659
  (Cauchy–Schwarz form, weaker). Header comment lines 10–19 explicitly label 0.50659/0.75329 as the
  Cauchy–Schwarz forms and the paper's multiplicity-aware constants as in `ThmD/Mult.lean`.
- `Zeta23/ThmD/Mult.lean` line 436 `thmD₀_simple_mult`: `(HD 1−ε)N ≤ N0simple` with HD1=2−1/c₁*=0.67250
  (rank–trace/multiplicity form) — precisely the paper's Theorem D value.
- `comparator/Challenge.lean` lines 76–80 (`montgomery_taylor_simple_on_critical_line`): the 2c₁*−1
  form. ✓ (Solver's §1 claim is accurate.)

2f. **GLSS25 + k=1 barrier.** GS Theorem 5 (gs-2511.20059.txt line 479-480): "PCC ⇒ 100% simple
and on the line"; the paper's own §7.2(f) (lines 1656-1658) calls this complementary and states the
"full support" phrasing the solver reproduces. §7.2(e) (lines 1633-1639) matches the solver's §6:
"kλ<2 Rudnick–Sarnak; λ∈(1/2,1) at most k=3 (λ<2/3); odd moment doesn't lower Λ_1(0); λ≤1/2 vacuous
by Prop 7.4." All consistent. GLSS25 primary PDF not bundled (open O7) — honestly flagged. ✓

## 3. Flags / findings

- **F-1 [MAIN, quantifier gap — not an algebra error].** §5 step (iii) writes "Choose the admissible
  window with λ = 1 (λ₁ → 1): d = λ₁N, d/N → 1" and concludes `lim_{T→∞} N0^s(T,2T)/N(T,2T) = 1`.
  But HL* is assumed only for **λ < 1**; at any fixed λ<1, d/N → λ < 1, so the Prop-4.5 bound has the
  ceiling 2λ−1 < 1 and cannot reach 1 in the T-limit. Reaching 1 requires λ → 1. The rigorous,
  hypothesis-consistent conclusion is the **ε-form / iterated limit**:
    for every ε>0 there exist λ=λ(ε)<1 and T₀(ε,λ) with `N0^s_λ(T,2T)/N(T,2T) ≥ 1 − ε` for T≥T₀,
    equivalently `sup_{λ<1} liminf_{T→∞} N0^s_λ(T,2T)/N(T,2T) = 1` (i.e. `lim_{λ→1⁻} liminf_T`
    after the m→∞/SL passage). It is **not** the plain `lim_{T→∞}` at a single λ=1.
  To claim the plain T-limit at λ=1 one needs HL* at λ=1, or a diagonal λ=λ(T)→1 **with uniformity in
  λ** — neither is granted (HL* uniformity is only over a *finite* admissible window list, def §2).
  Note the paper/Lean reach their own λ=1 constants by an explicit eps-form λ→1⁻ passage
  (`Limit.eps_form_*`), consistent with this reading. *This is the single correction the proof needs.*
- **F-2 [minor, unstated regularity].** Determinacy/Carleman ("compactly-supported-in-limit") is laid
  on an asserted uniform spectral-radius bound for the sine-Gram compression. Plausible (PSD projection
  kernel), but not proved in the artifact. Milder than F-1.
- **F-3 [minor, boundary].** Lemma 3.B's "n₊/d → μ_λ((0,∞))" and the "1−Λ_m" step pass through an
  away-from-0 / atom handling note that is gestured at, not detailed; acceptable but leave as an
  obligation for a formalization pass.
- **F-4 [minor, labeling].** §4.1 says the theorem "does not require the *exact* m_3,m_4" — true, but
  13/18 (m=2) still *uses the values* m_3=2, m_4=13/4; so "not used in the theorem" is imprecise.
  13/18 is genuinely conditional on `HL*_4` (k=4 additive prime correlation). This is honestly stated
  in Cor 3.C/§8 but the §4.1 line could mislead. Task-3 check: m_3≈2, m_4≈13/4 are clearly labeled
  NUMERICAL/evidence-only in §7, `moments_christoffel_full.py` §(D), repro_manifest, obligation_graph;
  they are not load-bearing for an unconditional claim. ✓ (with F-4 caveat)

## 4. Task-4 / open-ingredient check

**SL** is precisely and honestly stated (§5): "limiting spectral distribution of the sine-kernel Gram
is supported on [0,∞) (automatic: Gram is PSD) with 0 in support / Christoffel function at 0 vanishes
Λ_m(0)→0". It is flagged as the single missing-in-literature fact (status_and_literature §5,
candidate_proof §5 remark, obligation_graph O5-D5). The failure-mode dichotomy (if SL fails as a mass
gap at 0, the m→∞ limit is a positive constant < 1 and the conclusion degrades to the m=1 bound ≥ 1/2)
is recorded in `approach_registry.md` R3/Failure-modes and `counterexample_log.md` CE-4. ✓
No claim of *unconditional* 100% appears anywhere; the 2/3-class unconditional bound and the Prop 7.4
ceiling are stated correctly. ✓

## 5. Artifact / provenance notes

- Run root standard artifact set is present and hashes match `SHA256SUMS` exactly (verified by
  recomputation). `repro_manifest.md`'s *self*-entry for its own hash (line 36, E8223028) is stale
  (actual FAD73138, matching SHA256SUMS) — cosmetic.
- This run's `audit_report.md` was replaced by this adversarial report; the prior version is preserved
  at `audit_report.initial-race.md`. A new independent script
  `reproducibility/audit_independent_check.py` (sha256 below) was added by the auditor.
- Inputs (paper v2 txt sha256 `9B02E53C…4302`; Lean snapshot commit `3635e748…a00510`) read read-only.

## 6. Open obligations (forward)

1. **Fix F-1 quantifier**: restate the §5 theorem as the ε/iterated limit (sup over λ<1 of liminf_T = 1),
   or add HL*-at-λ=1 / uniformity-in-λ to the hypothesis if the plain T-limit claim is wanted.
2. **Prove/refute SL** (spectral density of sine-kernel Gram at 0 — the single real open ingredient).
3. Prove the uniform spectral-radius bound (F-2) to justify Carleman, and detail the 0-atom continuity
   step (F-3).
4. Obtain exact closed forms m_3, m_4 (only needed for a fuller m=2 statement; not for the ε-theorem).
5. Verify GLSS25 primary source (arXiv:2503.15449 — packet O7).
6. Optional: stage-C `lean-verify` formalization of the corrected Christoffel argument (F-1-corrected).

## 7. Bottom line

The run's core claims — the exact m_2=4/3, the transcription-error diagnosis ((1,3/4,2,13/4)
inconsistent; (1,4/3,2,13/4) valid with Λ_2(0)=5/36 ⇒ 13/18 exact), the soundness of Lemmas 3.A/3.B
and the Prop-4.5 factor-2 corollary, the Lean/thmD₀_simple-vs-mult fidelity, and the honest labeling of
SL and of the numerical m_3,m_4 — are **all independently verified**. It is an honest
RIGOROUS_PARTIAL_RESULT, **provided the §5 theorem is corrected from `lim_{T→∞}=1` at λ=1 to the
ε-form / λ→1 iterated limit (F-1)**. With that single correction, PASS.
