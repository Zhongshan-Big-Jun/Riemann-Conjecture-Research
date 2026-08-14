# Record theorem — zeros of ξ′ on the critical line (consolidated statement, 2026-08-15)

Consolidates reports/xi-prime-pressure-method.md, reports/xi-prime-cor22-derivation.md,
reports/xi-prime-audit-manager.md, reports/admwindow-cos-instance.md, reports/linked-ladder.md.

## Notation

ξ(s) the completed zeta function; ξ′(s) its derivative (ξ′(1−s) = −ξ′(s)). N_{ξ′}(T,2T) =
#{zeros of ξ′ in the open strip with T < Im ≤ 2T, with multiplicity} (Riemann–von Mangoldt:
N_{ξ′}(T,2T) = (T/2π)ℓ₁(1+o(1))). N₀ˢ_{ξ′}(T,2T) = #{simple zeros of ξ′ with Re = 1/2,
T < Im ≤ 2T}. v_MT(s) = cos(√2 s) on [−1/2,1/2] (Montgomery–Taylor profile).

## Theorem (unconditional, pending only the f₉ certificate)

For f₉ ∈ {0.0039, 0.00395} with n = ⌈1/f₉⌉ − 1, m = 8 + n, A₀ = f₉·n < 1, if the k=9
pressure certificate F₈(g₁,…,g₈) ≥ f₉ for all gᵢ ≥ 0 holds (Arb branch-and-bound, 128-bit),
then

    liminf_{T→∞} N₀ˢ_{ξ′}(T,2T)/N_{ξ′}(T,2T) ≥ C₉^{ξ′}(f₉)
        := (H_{ξ′}^{MT} − (m−1)/(500m)) / (1 − A₀/m),

  f₉ = 0.0039 (CERTIFIED, extpress):  n = 256, m = 264, A₀ = 624/625,
        C₉^{ξ′} = (6875·H_{ξ′}^{MT} − 1315/96)/6849 = (2,640,000·H_{ξ′} − 5,260)/2,630,016
                = 0.8691835350528274770392388622387462383908672479612151585…
  f₉ = 0.00395 (CERTIFICATE RUNNING): n = 253, m = 261, A₀ = 99935/100000,
        C₉^{ξ′} = (26,100,000·H_{ξ′}^{MT} − 52,000)/26,000,065
                = 0.869224726234155780682210369165264862803577221356718139899266…
  H_{ξ′}^{MT} = 2 − κ₁(1, v_MT) = 0.8678888651990519355503147104203403132225704976166306446…

Both exceed the quartic-window record 0.86864051… and the flat-window 0.85838405…
(Lean-certified); the RH-conditional ξ′ comparandum is 0.8825 (CGdL20).

## Proof chain

1. **Baseline (Lean XiPrime formula):** S₁ ≥ H_{ξ′}^{MT}·N_{ξ′} − o(N) — rank–trace with the
   ξ′ second moment κ₁(λ,v) = 1/cWin(D₁,λ,v) (Zeta23/XiPrime, Lean-certified formula;
   κ₁(1,v_MT) computed A2-verified two ways to 20 digits).
2. **Stability refinement (Cor 2.2-type, audited):** S₁ ≥ H_{ξ′}^{MT}·N_{ξ′} + Δ(M°) − o(N) —
   OpenAI Lemma 2.1 applied to (P₁, Q₀) with r = s₁, b = s₂ + p; tight bound
   4(s₂+p) ≤ 2(N − s₁) (reports/xi-prime-cor22-derivation.md §4; cross-checked line-for-line
   against the OpenAI original).
3. **Pressure certificate:** F₈ ≥ f₉ (window-determined kernel; A6 transfer — the ζ and ξ′
   families share the certificate).
4. **Block-energy (BE₉):** E_m + (1/500)(y_m−y₁) ≥ f₉(m−8) (general-k derivation).
5. **Block-defect (BD₉):** Δ(G_B) + (1/500)span(B) ≥ A₀ − o(1), A₀ = f₉(m−8) < 1
   (Lemma 4.3 + kernel-limit concentration, A3 transfer).
6. **Pinching/averaging (AV₉):** Δ(M°) ≥ (A₀/m)S₁ − ((m−1)/(500m))N_{ξ′} − o(N).
7. **Conclusion:** (1 − A₀/m)S₁ ≥ (H_{ξ′}^{MT} − (m−1)/(500m))N_{ξ′} − o(N) ⟹ the stated
   constants (exact rational forms verified at mpmath 70 digits; float64-division pitfalls
   documented in release-checklist.md).

## Audit status (reports/xi-prime-audit-manager.md, 2026-08-15)

- A1 zero-side structure: PASS (Lean WindowZeroSide machinery covers the ξ′ zeros; AdmWindow
  bounds for cos(√2s) verified numerically: ‖v′‖₁ = 0.47951, ‖(v²)′‖₁ = 0.84406, ‖v″‖₁ =
  1.83745, ‖(v²)″‖₁ = 2.7938, a = 0.84923 ∈ [1/2,1]).
- A2 κ₁(1,v_MT): CLOSED (two independent paths, 20-digit agreement).
- A3 kernel-limit transfer: PASS (window-only inputs).
- A4 RvM/counting: PASS (elementary + Lean xiDerivZeros₀_rvm, PoissonSq).
- A5 arithmetic: PASS (70-digit exact forms; all synced values confirmed).
- A6 certificate transfer: PASS (window-determined kernel).
- Formalization blueprint: reports/admwindow-cos-instance.md (ModFactor A = 1, B = 2,
  cMod = cRho + 4).

## Open items

1. The f₉ = 0.00395 certificate itself (running; release checklist + audit packet
   reports/f9-00395-audit-request.md prepared; expected values precomputed and
   cross-validated). On landing, A6 re-run and this document updated to the 0.00395 row.
2. Lean AdmWindow instance for cos(√2s) (Stage C, AtOne pattern; math blueprint complete).
3. Independent human/formal audit welcomed (packet: reports/xi-prime-audit-request.md).
