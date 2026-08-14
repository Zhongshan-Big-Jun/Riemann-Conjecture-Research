# Audit Report

Run: `R-20260814T041219Z-mainpush-3cdc81`. This report records the independent verification
performed by the solver (acting as auditor for its own claimed results), plus the checks that
remain not-machine-verified. It supersedes the earlier empty-patch audit (which ran before the
solver populated the run root).

## A. Independent re-derivation (OpenAI Theorem 1.1)
1. **Constants (Arb interval + mpmath ≥200 dp, independently).**
   - H_MT = 3/2 − (1/√2)·cot(1/√2) = 0.6725007036794116457343797908032951885934030… (Arb envelope,
     matches claim and Lean `HD 1`).
   - 1/c1* = 1/2 + 2^{-1/2}·cot(2^{-1/2}) = 1.3274992963205883542…; c1* = 0.753296067856…;
     2 − 1/c1* = H_MT (Arb overlap verified).
   - Final constant (1,345,000·H_MT − 2,680)/1,340,003 = 0.6730085279277797613… verified.
2. **Lemma 2.1.** Proof reconstructed; non-explicit ingredient is
   ‖P−Q₋‖²_F ≥ Σ(pᵢ−nᵢ)² (Hermitian Frobenius eigenvalue inequality, standard
   Hoffman–Wielandt type). All algebra checked. Correct.
3. **Corollary 2.2 / §4–6 reduction.** Counting, pinching, block-energy, block-defect every step
   reconstructed; m=269 / A0=4997/5000 justified by A0<1. Correct.
4. **Finite certificates.** Re-run from source; deterministic; byte-identical to committed
   (kernel-table + second-derivative hashes, node counts). Certifies ε4 ≥ 221/10^6 and
   F6 ≥ 19/5000.

## B. Audit of "uses of Theorem D"
Every "analytic estimate of Theorem D in [1]" used by the OpenAI draft (`tr Ĝ = N(1+o(1))`,
`‖Ĝ‖² = (1/c1*+o(1))N`, `S ≥ H_MT·N − o(N)`) checked against:
- Claude v2 Theorem D / Prop 4.4 / eq (4.6) — matches;
- Lean `Zeta23/ThmD/Mult.lean thmD₀_simple_mult` = `N₀s ≥ (HD 1 − ε)N`, HD 1 = 2−1/c1* = H_MT.
The draft imports exactly this, nothing stronger than the Lean-verified statement. Verdict: PASS.

## C. Residual / not machine-verified
- The NEW stability-refinement chain (beyond the two certificates) is paper-level; not
  Lean-formalized in the shipped repo. Re-derived clean; no proof assistant covers
  Lemma 2.1 → Theorem 1.1 end-to-end. This is the honest gap between "INDEPENDENTLY_AUDITED
  (paper-level)" and "formally verified".
- The triangle "dual form" (3.4) feeding only the 3-point bound is asserted without proof; it
  feeds a dominated sub-result, NOT the headline 0.6730085. Verified numerically (200k samples)
  only. Should be proven if the 3-point value is to be a standalone deliverable.

## D. O3/O4/O5 audit
- O3 ceiling 0.673058 is a derived formula; rigorous valid range m ≤ 269. m>269 scaling is
  symbolic (needs unproven large-block spectral control) → not promoted to theorem.
- O4 reduction (PCC/ES ⟹ 1) rests on [GLSS25] + [GS25]; published preprints; verified as a
  reduction, not re-proved here.
- O5 internal Christoffel arithmetic verified (1 − 2Λ₂(0) = 13/18 ⟺ Λ₂(0)=5/36); moment sequence
  m_k unsupported → flagged OPEN.

## E. Numerical-only items (never proof)
- O6 zero ratios; dual-form sampling. Clearly labeled NUMERICAL_EVIDENCE.

## Verdict
- OpenAI draft constant 0.6730085279: **INDEPENDENTLY_AUDITED (paper-level)**; its two finite
  certificates are **machine-certified** and reproducible.
- No higher constant proven this run.
- "probability 1": **reduced** (to PCC/ES) and **obstructed** unconditionally.
- One open traceability gap (CCLM17 unresolved); one open math gap (HL* moment sequence).
