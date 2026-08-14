# Manager-level audit report — ξ′ pressure-method candidate (A1–A6)

Date: 2026-08-15. Auditor: research manager (subagent audits crash-prone in this
environment; manager-level audit is the established working pattern — extpress precedent:
manager audit PASS-with-limits). Scope: reports/xi-prime-pressure-method.md,
reports/xi-prime-cor22-derivation.md, reports/xi-prime-mt-window.py,
reports/linked-ladder.md, Lean sources (zeta-23-lean@3635e748), and the general-k
derivation (extpress run, candidate_proof.general-k-derivation.md).

## Claim under audit (two instances)

- f₉ = 0.0039 (extpress certificate, closed form):
  C₉^{ξ′} = (6875·H_{ξ′}^{MT} − 1315/96)/6849 = 0.8691835350528274770392388622387462383908672479612151585…
- f₉ = 0.00395 (certificate in progress):
  C₉^{ξ′} = (26,100,000·H_{ξ′}^{MT} − 52,000)/26,000,065 = 0.869224726234155780682210369165264862803577221356718139899266…
  H_{ξ′}^{MT} = 2 − κ₁(1, v_MT) = 0.8678888651990519355503147104203403132225704976166306446…

## Verdicts

### A1 — zero-side block structure: PASS (math level; one formalization gap noted)

Audited against the Lean sources:
- `Zeta23/ZeroSide.lean` + `Zeta23/ThmD/ZeroSideD.lean` provide the generic zero-side facts
  (PoissonSq, BlockInputs, Gz=Gp, tail package, a_half, H-RvM).
- `Zeta23/XiPrime/Assembly.lean:277` defines `WindowZeroSide Z P Pf` — the zero-side bundle
  for ANY ZeroConfig Z; instantiated at the ξ′ zeros: `xiDerivZeros hF2 hs` (Assembly.lean:445)
  and `wZeros hZ hs` (Assembly.lean:562).
- `Zeta23/XiPrime/QuarticWindow/ZeroSide.lean:110` `windowZeroSide_atV_of`: for any
  `RiemannVonMangoldt Z`, any `P.Valid`, any even admissible profile v (via an
  `admWindow_phiV` proof), `WindowZeroSide Z P (P.atV v)` holds. The modulated window
  `φ_v := √(v(·/L))·φ₀` inherits support from the taper φ₀; the profile only supplies
  evenness, range, and derivative norms.
- Note §1 bookkeeping check (s₁/s₂/p): N ≥ s₁ + 2s₂ + 2p (simple on-line weight 1;
  multiple on-line points weight ≥ 2 each; off-line zeros closed under ρ ↦ 1−ρ̄ which
  preserves ordinate, ξ′(1−s) = −ξ′(s), real coefficients — each pair {ρ, 1−ρ̄} contributes
  2m ≥ 2); rank(P₁) ≤ s₁ and tr(P₁) ≤ s₁ (rank-one PSD terms, ‖v_ρ‖² ≤ 1 via PoissonSq);
  n₊(Q₀) ≤ s₂ + p via the (1,1)-signature pair blocks and the inertia lemma. Mechanism
  v_{1−ρ̄} = v_ρ holds because vectors are indexed by ordinates only. All consistent with
  the generic ZeroSide pattern (Prop 4.1-type).
- **AdmWindow bounds for v_MT = cos(√2s) verified numerically (mpmath 40 digits)** on
  [−1/2, 1/2]:
  - even ✓ (cos); 0.76024459707563 ≤ v ≤ 1 ✓ (nonneg, le_one); analytic ✓ (ContDiff ℝ 2);
  - ‖v′‖₁ = 0.47950766837245341798 ≤ 2 ✓
  - ‖(v²)′‖₁ = 0.84405003027614658193 ≤ 2 ✓
  - ‖v″‖₁ = 1.8374507397311368756 ≤ c/w (4) ✓
  - ‖(v²)″‖₁ = 2.7938239945464334394 ≤ c/w (4) ✓  (c = 4, w = 1 admissible)
  - a = L⁻¹∫v² = 0.84922799931830417992 ∈ [1/2, 1] ✓ (a_half)
  Support: supplied by the taper φ₀ in the P.atV construction (same as quartic).
  GAP (formalization, not math): a Lean `admWindow_phiV` instance for cos(√2s) must be
  written following the quartic template (AtOne pattern; Stage-C scope). All numeric
  ingredients verified above.

### A2 — κ₁(1, v_MT) numeric: CLOSED (already, 2026-08-14)
Two independent paths (quadrature; analytic vConv) agree to 20 digits;
flat/quartic reproduce the Lean-certified constants.

### A3 — kernel-limit concentration transfer: PASS
The kernel-limit lemma (extpress general-k derivation, step 4) asserts uniform convergence
Σ_{i<j}|G_ij|² = ½E_m + o(1) for fixed-m blocks. Its proof uses only (i) the window profile
(via the overlap kernel k = K/K(0) from φ̂) and (ii) uniform Poisson–Gabor concentration of
‖v_ρ‖² at ordinates γ (PoissonSq; uniformity from the fixed window). For ξ′ the test family
(P.atV v_MT) and ordinates are the same class of objects (ξ′ zeros have the same RvM density
and the vectors v_ρ are built from the same φ̂); nothing in the lemma references the zero
family beyond the ordinates themselves. Transfer is verbatim.

### A4 — RvM and trace identities: PASS
N_{ξ′}(I′) ≥ s₁ + 2s₂ + 2p: elementary counting (verified in A1). tr Â = N(1+o(1)): per-zero
‖v_ρ‖² = (aL²)⁻¹Σ_k φ̂(γ−τ_k)² → 1 uniformly — Lean `WindowZeroSide.poisson` (PoissonSq) and
`xiDerivZeros₀_rvm` (RiemannVonMangoldt for ξ′), XiPrime Final.lean:387/411.

### A5 — arithmetic: PASS (mpmath 70 digits, 2026-08-15)
- Closed form: C₉^{ξ′}(0.0039) = 0.8691835350528274770392388622387462383908672479612151585…
- General form: C₉^{ξ′}(0.00395) = (26,100,000·H − 52,000)/26,000,065
  = 0.869224726234155780682210369165264862803577221356718139899266…
- Auxiliaries: 6875/6849 = 1.0037961746240327…; 1315/96 = 13.697916…;
  263/132000 = 0.001992424… = (m₉−1)/(500m₉) at m₉ = 264; 26/6875 = 0.003781818…
  = A₀/m₉ = (624/625)/264 = 624/165000 ✓ (identity 26·165000 = 624·6875 = 4,290,000);
  A₀ = 624/625 = 0.9984 = 0.0039·256 ✓ (n₉ = 256, m₉ = 264).
  Closed-form identity (2,640,000·H − 5,260)/2,630,016 = (6875·H − 1315/96)/6849
  verified to 1e-71; float64-division pitfalls identified and avoided
  (pure-integer-coefficient evaluation).

### A6 — certificate dependency honesty: PASS
F₈(g₁,…,g₈) depends on the kernel table w = k² only, which is window-determined
(MT window; the verifier kernel table is generated from the window, independent of ζ vs ξ′).
The extpress certificate F₈ ≥ 39/10000 (audited PASS-with-limits) transfers verbatim to the
ξ′ chain; the f₉ = 0.00395 instance awaits its own certificate (in progress) and transfers
by the same argument.

## Verdict

**PASS (manager-level) for A1–A6 at math level**, with two open items, neither of which is a
math gap:
1. Lean `admWindow_phiV` instance for cos(√2s): **math-level blueprint now complete** —
   reports/admwindow-cos-instance.md (ModFactor A = 1, B = 2; cMod = cRho + 4, better than
   quartic's cRho + 15.75; all elementary bounds verified at 40 digits). Remaining work is
   Lean code following the quartic template (AtOne pattern; Stage C).
2. The f₉ = 0.00395 certificate itself (running; when it lands, rerun A6 for the new file
   and update this report).

Supersedes the "open" flags in reports/xi-prime-cor22-derivation.md §7 and
reports/xi-prime-pressure-method.md (dependency checklist items 3–4).
