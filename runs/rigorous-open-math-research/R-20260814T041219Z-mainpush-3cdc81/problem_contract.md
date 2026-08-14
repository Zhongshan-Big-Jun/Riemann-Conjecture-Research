# Problem Contract — Proportion of Critical-Line Zeros Toward 1 (Main Push)

Run root: `runs/rigorous-open-math-research/R-20260814T041219Z-mainpush-3cdc81`
Task packet: `agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md`
Prepared: 2026-08-14. Protocol labels follow the rigorous-open-math-research Output protocol.

## 1. Normalized statement

Fix 0 ≤ T1 < T2. Let ρ = β + iγ run over the nontrivial zeros of the Riemann zeta
function ζ, m_ρ the multiplicity of ρ. Define:

- N(T1,T2) := Σ_ρ∈Z, T1<γ≤T2 m_ρ   (with multiplicity)
- N0(T1,T2) := Σ over on-line zeros (β = 1/2), with multiplicity
- N0*(T1,T2) := #{ρ : β = 1/2, T1<γ≤T2}   (distinct on-line)
- N0^s(T1,T2) := #{ρ : β = 1/2, m_ρ = 1, T1<γ≤T2}  (simple on-line)
- Nd(T1,T2) := #{ρ : T1<γ≤T2}  (distinct)

**Target (user's goal):**
  lim_{T→∞} N0(0,T)/N(0,T) = 1,
equivalently "with probability 1 (in the proportion sense), a zero of ζ lies on the
critical line."

**Dyadic convention:** throughout the literature and this run, upper/lower bounds are
stated (unless cumulative) for dyadic windows (T, 2T]; cumulative forms follow by dyadic
summation (verified in [Claude v2] and Lean `Main.cumulative_of_dyadic`).

## 2. Deliverable hierarchy (any one is an acceptable outcome with an honest label)

1. An unconditional improvement of current best lower bounds:
   - liminf N0^s(T,2T)/N(T,2T) ≥ C for C > 0.6730085279277797613... (OpenAI draft),
   - liminf N0*/N ≥ 0.6725007036794116..., liminf Nd/N ≥ 0.83625... (Claude Thm D, Lean-verified),
   - or any other proportion (N0/N, N0*/N, Nd/N).
2. Independent verification or refutation of the OpenAI draft constant and its sub-claims.
3. A rigorous conditional theorem: under a precise hypothesis (HL*, or PCC full support),
   proportion = 1; or a precise reduction "N0/N → 1 ⟺ <named conjecture>".
4. An exact obstruction report: why proportion 1 is unreachable by the known methods.

## 3. Completion criteria

- Honest status label from the Output protocol; numerical evidence never labeled proof.
- Every obligation O1–O8 either discharged by proof/verification or recorded as an exact
  open gap with its failure mechanism.
- The "probability 1" goal explicitly addressed: achieved / reduced to a named conjecture /
  blocked with exact reasons.

## 4. Verification criteria

- Every claimed theorem: full proof with all steps; adversarial (independent) audit.
- Numerical claims: reproducible commands + certificates (Arb interval arithmetic where claimed).
- No RH or unproven conjecture used inside an "unconditional" claim.
- "Probability 1" claimed only with complete proof.

## 5. Status summary (set by this run)

- OpenAI draft constant 0.6730085279277797613: **INDEPENDENTLY VERIFIED** at the level of
  (a) both finite certificates (3-point ε4 ≥ 221/10^6 and 7-point F6 ≥ 19/5000) re-run
  byte-identically to committed Arb certificates; (b) every algebraic step of Lemma 2.1,
  Corollary 2.2, the block-energy/block-defect/block-averaging reduction, and the final
  constant (1,345,000·H_MT − 2,680)/1,340,003 re-derived and confirmed. Caveat: the new
  stability-refinement chain is paper-level (not Lean-formalized); it builds on the
  Lean-verified Theorem D baseline (see audit_report).
- OpenAI certificate class ceiling: ≈ 0.673058 (m→∞), below the bandwidth-one ceiling
  0.6818287. It does NOT escape the bandwidth-one ceiling (O3).
- Probability-1 (O4): verified reduction `PCC (ES form) ⟹ lim N0/N = 1` via [GLSS25] and
  [GS25 Thm 2]; exact obstruction given (lower-bound-only certificate classes cap < 0.69,
  ghost-configuration invariance; k=1 moment barrier).
- No unconditional constant strictly above 0.6730085 was reached; no improvement beyond the
  OpenAI value was proven. The improved constant is the verified OpenAI draft value itself.
