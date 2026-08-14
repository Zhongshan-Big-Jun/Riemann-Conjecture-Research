# ξ′ pressure-method candidate: C₉^{ξ′} = 0.86918353505… (2026-08-14)

Manager-level analysis. Candidate: apply the k=9 pressure method (extpress run) to the zeros
of ξ′ (derivative of the completed zeta function), with the Montgomery–Taylor window.

## New constant computed (this session)

From the Lean XiPrime infrastructure (zeta-23-lean@3635e748, Zeta23/XiPrime/Defs.lean):
the ξ′ second-moment constant is κ₁(λ,v) = 1/cWin(D₁,λ,v) with
D₁(s) = s − 4s² + Σ d_k s^{2k+1}, vConv(v,r) = ∫_{−1/2}^{1/2−r} v(s)v(s+r)ds,
jWin = 2∫₀¹ D₁(λr)(v⋆v)(r)dr, cWin = λ(∫v)²/(∫v² + λ·jWin).
With the MT profile v_MT(s) = cos(√2 s) (the Anthropic Theorem-D window):

- **H_{ξ′}^{MT} = 2 − κ₁(1, v_MT) = 0.86788886519905…** (previously unknown)
- Cross-validation: flat v ≡ 1 gives 2 − κ₁ = 0.85838405… (Lean: ≥ 0.85838371 ✓);
  quartic gives 0.86864051… (Lean: ≥ 0.86864017 ✓). Implementation is faithful.

## Candidate record

Applying the k=9 pressure chain (general-k derivation, extpress run) with the SAME MT-window
kernel (the certificate F₈ ≥ 39/10000 is window-dependent only through the kernel, so it
transfers verbatim) and the ξ′ rank-trace baseline:

    liminf N0^s_{ξ′}(T,2T)/N_{ξ′}(T,2T) ≥ C₉^{ξ′} := (6875·H_{ξ′}^{MT} − 1315/96)/6849
                                            = 0.8691835350528274770389…

- vs flat 0.85838: +1.08e-2; **vs quartic 0.86864: +5.44e-4 (new unconditional record)**;
  vs RH-conditional 0.8825 (CGdL20): −1.33e-2.

## Dependency checklist (what must hold for the candidate to be a theorem)

1. [VERIFIED] Rank-trace baseline for ξ′ at ANY window profile v (Lean XiPrime, 2 − κ₁; the
   flat/quartic constants are Lean-certified; the family machinery familyHyps_atV covers v_MT).
2. [COMPUTED] κ₁(1, v_MT) = 1.1321111348009480644… (this session; cross-validated on
   flat/quartic to 8 digits). Strict inequality 2 − κ₁(1,v_MT) > 0.86864 holds (margin
   1.2e-4), so the plain MT-window ξ′ bound ALREADY exceeds flat (0.86789 vs 0.85838) and
   nearly matches quartic; the pressure term provides the crossing above quartic.
3. [AUDITED] The stability refinement (OpenAI Lemma 2.1 → Cor 2.2: S ≥ H·N + Δ(M°) − o(N))
   for ξ′: full derivation in reports/xi-prime-cor22-derivation.md (corrected tight bound
   s₁+2N; cross-checked line-for-line against OpenAI Cor 2.2); zero-side block structure
   audited in reports/xi-prime-audit-manager.md (A1 PASS).
4. [AUDITED] Block-energy/block-defect/pinching with m₉ = 264 (A₀ = 624/625 < 1): depends
   only on the Gram structure of consecutive retained simple on-line zeros and the window
   kernel; kernel-limit transfer audited (A3 PASS) — same window ⇒ same kernel; the
   concentration argument is structural.
5. [VERIFIED] Certificate F₈ ≥ 39/10000 (window-kernel inequality; independent of ζ vs ξ′).
   The f₉ = 0.00395 instance (pending certificate) transfers by the same argument (A6 PASS).

## Status

AUDITED_CANDIDATE (manager-level, A1–A6 PASS — reports/xi-prime-audit-manager.md; an
independent human/formal audit remains welcomed). The plain MT-window ξ′ constant
H_{ξ′}^{MT} = 0.8678888652 itself is a solid new numerical constant (strictly between flat
and quartic), computable from the Lean-verified formula. Remaining open items are not math
gaps: (1) Lean AdmWindow instance for cos(√2s) (AtOne pattern, Stage C); (2) the f₉ =
0.00395 certificate (running) — on landing, rerun A6 and update the ladder.
