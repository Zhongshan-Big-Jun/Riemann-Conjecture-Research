# Stage C feasibility: Lean formalization of the ξ′ candidate (2026-08-14)

Question: how much of the ξ′ pressure-method candidate (C₉^{ξ′} = 0.86918353505…) is
Lean-formalizable with the existing zeta-23-lean snapshot (Lean v4.33.0-rc2, Mathlib
51e6992efd06)?

## Components and their status

| Component | Status in snapshot | Formalization cost |
|---|---|---|
| ξ′ rank-trace spine (flat/quartic, any WindowProfile v) | ✅ Lean-certified (XiPrime: fixedLam_atV, familyHyps_atV; certificates at λ=1) | none |
| MT profile v_MT(s) = cos(√2 s) as a WindowProfile | ⚠️ Needs: WindowProfile v_MT instance (smoothness, margin 0 < v_MT ≤ 1 on [−1/2,1/2] — max cos(√2·1/2) = 1, min cos(√2/2) ≈ 0.7602 > 0 ✓) | small (definitional) |
| κ₁(1, v_MT) = 1.1321111348009480644… with certified enclosure | ⚠️ Needs the AtOne.lean pattern: rational κ₉ ≤ κ₁ ≤ κ₉ + ε₉. For the cos profile the integrals ∫v, ∫v², ∫(v⋆v)(r)D₁(r)dr need (a) closed forms (available: ∫v = √2 sin(1/√2), ∫v² = ½ + sin(√2)/(2√2) — transcendental!), (b) rational enclosures of sin/cos values (Mathlib has these bounds) | medium |
| Cor 2.2-type stability refinement for ξ′ (Δ(M°) term) | ❌ Not in snapshot (the Δ(M°) machinery is OpenAI's, paper-level; the ζ version is also not Lean-formalized) | large (new linear-algebra + assembly) |
| Pressure chain (block-energy/defect/pinching, f₉ certificate) | ❌ Not in snapshot (ζ version not formalized; f₉ certificate is Python/Arb) | very large |
| Final constant C₉^{ξ′} arithmetic | trivial | trivial |

## Verdict

- A Lean theorem `2 − κ₁(1, v_MT) ≥ 0.86788` (i.e. the MT-window ξ′ baseline with certified
  decimals) is **feasible** with medium effort, following the AtOne.lean pattern
  (rational enclosures of the cos-profile integrals + D₁ truncation with tail bound).
- The full C₉^{ξ′} = 0.86918353505… theorem would require formalizing the stability
  refinement and the pressure chain for ξ′ — beyond the current snapshot and session
  resources; it is paper-level (like the ζ C₉ record itself).
- Recommendation: if Stage C is pursued, target the baseline theorem
  `xiDeriv_simple_on_line_mt : 0.86788 * Ncount T (2*T) ≤ N0simple T (2*T)` (with a
  certified decimal), extending the XiPrime Certificate module. The pressure part stays
  paper-level pending an independent audit (A1–A6 packet).
