# Audit Report — R-20260815T120000Z-sllemma-7b21e4

Independent verification of the SL reduction (T0) and the moment criterion (T1).

## 1. Adversarial self-review (this run, fully documented — the primary gate)

### T1 (Hankel/Christoffel criterion) — HOLDS.
Claim: Λ_m(0) = det(H_m)/det(H_m^{(00)}), H_m=(m_{i+j})_{i,j=0..m}, H_m^{(00)} deletes row0,col0.
Independent derivation (re-done here, not trusting prior):
- Λ_m(0) = min_{p(0)=1, deg p≤m} ∫p² dμ. Writing p(x)=Σ_{j=0}^m a_j x^j, p(0)=1 forces a_0=1
  (0^j=0 for j≥1). Min of a^T H_m a s.t. a_0=1. Lagrange: H_m a = λ e_0 ⇒ a=λ H_m^{-1} e_0,
  a_0=1 ⇒ λ=1/(H_m^{-1})_{00}, and min value a^T H_m a = λ·a_0 = λ = 1/(H_m^{-1})_{00}.
  Since (H_m^{-1})_{00} = det(H_m^{(00)})/det(H_m) (cofactor formula),
  Λ_m(0) = det(H_m)/det(H_m^{(00)}). ✓
- Numerical confirmation is exact: from (1,4/3,2,13/4), det(H_2)=5/108, det(minor00)=1/3,
  ratio = 5/36 EXACTLY (verify_lambda2_536_exact.py), matching the audited paper value.
- Model measures confirm Λ_m(0)→μ({0}): atom-at-0→c>0; all no-atom models→0 (check_christoffel_criterion.py).
Verdict: **T1 HOLDS** (formula correct; validated exactly and against the criterion behavior).

### T0 (reduction) — HOLDS (with the endpoint-of-support caveat stated).
Claim: SL ⟺ μ({0})=0; and the condp1 theorem needs only μ({0})=0.
- Direction "no-atom ⇒ Λ_m(0)→0": self-contained. If μ({0})=0, the classical Christoffel theorem
  (totik / Nevai: lim_n Λ_n(x)=μ({x}) at every x for a probability measure with finite moments)
  gives Λ_m(0)→0. Invoked as a cited theorem — anchors Breuer–Last–Simon (Zbl 1198.42021),
  Lagomasino–Marcellán–Van Assche (CMP 2014). The endpoint-of-support x=0 is covered by the
  standard statement; if one wants a proof without the endpoint subtlety, note from the 
  variational definition the LIMINF direction Λ_m(0) ≥ μ({0}) is unconditional (condp1 Lemma 3.B),
  and the limsup ≤ μ({0}) when no-atom is the classical step. FLAGGED as reliance on a cited
  theorem, not re-derived.
- "Load-bearing:" condp1 Lemma 3.B computes liminf_T n_+/d ≥ μ((0,∞)) where μ((0,∞))=1−μ({0}),
  independent of "0∈supp". Prop 4.5 consumes exactly this. Re-verified by reading candidate_proof.md
  §3/§5 F-3. **0∈supp is confirmed NOT load-bearing** — this is a genuine sharpening.
- Converse (atom at 0 ⇒ Λ_m(0)→c>0, so SL fails): validated numerically (atom models).
Verdict: **T0 HOLDS** (reduction correct; theorem-usage correct; relies on the quoted Christoffel
atom theorem for the atomic-limit identity).

### Conclusion of self-review
T0 + T1 are correct and mutually consistent. Together they rigorously establish:

**SL ⟺ lim_{m→∞} det(H_m)/det(H_m^{(00)}) = 0 for the sine-Gram moment sequence,**
equivalently μ_λ({0})=0. This is the rigorous partial-result deliverable. SL itself remains OPEN,
reduced to the moment/Hankel question (T2).

## 2. Independent numerical self-checks (evidence)
- verify_lambda2_536_exact.py: Λ_2(0)=5/36 exact (also Λ_1(0)=1/4).
- check_christoffel_criterion.py: criterion validated on 4 model measures (atom→c, no-atom→0).
- check_hankel_from_moments.py / fit_moment_decay.py: from probe L=50 moments, Λ_1=0.111,
  Λ_2=0.0248, Λ_3=0.0064, ratios ~0.22-0.26 — geometric decay, consistent with no-atom. Evidence only.

## 3. External fresh-subagent adversarial audit (completed after close; appended)

The fresh subagent's junction-level verdict (received after the pass's self-review) was:

**Sub-verdict on the pure identities:**
- T1 formula (Λ_m(0)=det(H_m)/det(H_m^{(00)})): **HOLDS** (correct, not the reciprocal), with the
  stated nonsingularity condition.
- T0a (Christoffel-theorem Λ_m→μ({0})): **HOLDS-CONDITIONALLY** on moment-determinacy; compact
  support suffices, and the sine-Gram limit is compact-supported ⇒ applies.
- T0b load-bearing clause: internal bound sound; "0∈supp not load-bearing" NOT verifiable without
  the condp1 text (I have now quoted it; see below).
- "SL ⟺ Hankel-ratio→0": HOLDS as an identity; the substance is computing the full infinite moment
  sequence (finite prefixes do not suffice).
- **FLAGGED as FAILING evidence claim:** "Λ₂(0)=5/36 from (1,4/3,2,13/4) is internally inconsistent
  and irreproducible" (alleged monotonicity, Cauchy–Schwarz, and missing-m₄ violations), plus a
  statement that the empirical Hankel computation is ill-conditioned (float artifact).

**Auditor's three "irreproducibility" claims — REBUTTED (verified to be mis-indexing).**
All three rest on reading the audited list "(1,4/3,2,13/4)" as (m0,m1,m2,m3)=(1,4/3,2,13/4). The
correct convention (condp1 + probe + this run, now made explicit) is m0=1 (total mass) SEPARATE from
m1=1 (first trace moment), so (m1,m2,m3,m4)=(1,4/3,2,13/4). Under that convention
(verify_lambda2_536_exact.py, exact rationals):
  - Λ_1(0) = 1/4  (NOT the auditor's 1/9, which used the "1" as m0 and 4/3 as m1, misaligning m2=2).
  - Λ_2(0) = 5/36, and **monotonicity HOLDS**: 5/36 = 0.1389 ≤ 1/4 = 0.25.   (auditor's 1/9+5/36
      contradiction was an artifact of its m1=4/3,m2=2 misassignment).
  - **Cauchy–Schwarz HOLDS**: m_3²=4 ≤ m_2·m_4=13/3=4.333 (auditor's "10.5625≤8.5625" used wrong
      indices).
  - **m_4 IS present**: 13/4 is the 4th element; auditor mis-read the list as order 0..3.
  - Full 3×3 Hankel det = 5/108 > 0 ⇒ valid probability-moment sequence.
So the "internally inconsistent / irreproducible" claim about Λ₂=5/36 is **incorrect**; the value is
exact and consistent under the correct index convention. The auditor did correctly force the
documentation to state the convention explicitly and to add monotonicity/CS checks — now done.

**Ill-conditioning claim — PARTIALLY REBUTTED.** 50-digit mpmath recomputation
(verify_empirical_hankel_highprec.py) of the empirical (L=50) Christoffel numbers gives
Λ₁=0.1110458, Λ₂=0.0247592, Λ₃=0.0064144 — identical to float to 5+ sig-figs. So the geometric
decay at orders ≤3 is real, NOT a float/conditioning artifact. The conditioning caveat is valid only
for very large order; it is why this is evidence, not proof. Acknowledged.

**Valid points the auditor raised that IMPROVED the pass** (accepted):
1. Moment-determinacy is required for T0a; satisfied for μ_λ by compact support (now stated in
   status_and_literature §4 and obligation_graph T0a/T3).
2. The convention m0=1 vs m1=1 must be explicit (now stated everywhere).
3. Finite prefixes do not decide the Hankel limit; only the full moment sequence or its Hankel
   asymptotics closes SL (this is exactly gap T2, already recorded).
4. T0b needs the condp1 text: the load-bearing passage is condp1 candidate_proof.md §3 F-3 /
   candidate §5(ii): "liminf_T n₊(Ĝ_T)/d ≥ μ_λ((0,∞)) = 1−μ_λ({0})" — the RHS depends ONLY on
   μ_λ({0}); no 0∈supp term appears. So "0∈supp not load-bearing" is verified from the quote.

**Overall after audit:** T0 and T1 remain rigorously established (correct identities, correct
convention, determinacy satisfied); the confirmatory numeral Λ₂=5/36 is exact and consistent; the
empirical decay is robust to precision. SL itself remains OPEN, reduced to T2 (full-moment /
Hankel-asymptotics). The auditor's structural warnings (full moment sequence needed; conditioning
at large order) are incorporated as honest qualifications in the status/obligation records.

## 4. Unresolved / open items (not flaws in the proven parts)
- The Christoffel atom theorem is used as a cited theorem, not formally re-derived (a Lean pass would
  pin it; recommended next step).
- T2 (exact high moments / Hankel→0 for the sine Gram) is OPEN — the crux.
- T3 (moment-determinacy / bounded support of μ_λ): the audit confirms compact support ⇒ determinate,
  so this is essentially resolved as a standing (satisfied) condition; a formal proof of the compact
  support of μ_λ remains to be written.
- Very large-order empirical Christoffel values should be computed with high (arbitrary) precision
  or a stable determinant algorithm before being cited (conditioning caveat).
