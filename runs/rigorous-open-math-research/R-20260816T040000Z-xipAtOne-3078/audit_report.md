# Audit report — M3-open-A AtOne certificate for κ₁(1,vMT)

## What was checked
1. **Constants vs blueprint/derivation (independent code paths).**
   - a=∫vMT², b=∫vMT⁴, Iv=∫vMT from exact closed forms (regex-quality step) and from mpmath
     quadrature (independent path) agree to ≥ 40 dp.  Blueprint labels a↔∫v², b↔∫v⁴ confirmed.
   - ∫vMT = 0.918725369865568437784… — the value `…843826` in `FORMALIZATION_STATUS_XIP.md` was
     a transcription typo; the correct `…437784` matches machine_check.log / audit report.
2. **vConv closed form vs quadrature** at 5 lag values: agree to 40 dp.
3. **Rigorous certificate (ARB).** J1 = 2∫₀¹D1trunc9·vConvMTcl enclosure radius 2·10⁻¹⁶ via
   composite Simpson + rigorous global M₄.  κ₉ width 4·10⁻¹⁶ ≪ ε₉ = 3.42·10⁻⁷.
4. **Sandwich correctness.** κ₁(1,vMT) ∈ [κ₉, κ₉+ε₉] uses only the formally-verified D₁ cert
   (D1_le_D1trunc9_add, D1trunc_le_D1) and vConv≥0 — the tail enters with the correct sign.
5. **Cross-check vs canonical (dps=120):** κ₁(full D1) = 1.1321111348009480644… and
   H = 0.86788886519905193555031471042034031322257049761663…; |H − canonical| ≈ 1.4·10⁻⁵⁶.
   The derived sandwich [κ₉, κ₉+ε₉] **contains** the canonical κ₁; [2−(κ₉+ε₉), 2−κ₉] contains
   the canonical H.
6. **Lean.** `Record9.XiPrimeAtOne` declares the exact constants and the conditional sandwich;
   `lake build Record9.XiPrimeAtOne` exit 0 (see machine_check.log); no sorry/admit/axiom.

## Findings
- No mathematical finding invalidates the target.  All five implementation failures (F1–F5) are
  reproducible defects with fixes; none survived in the final artifacts.
- Statement-fidelity: κ₁(1,vMT) = `kappaXi 1 vMT`, H_xip = 2 − κ₁, C₉(ξ′) — unchanged, matching
  the A2-audited values.  The only "weakening" is that the open analytic facts are hypotheses
  (honest bridge), never `sorry`, and are recorded as M3-open-A.

## Open items (audit does NOT self-close these)
- Formal Lean proofs of ∫vMT=aMT-closed-form, vConv-closed-form, vConv≥0, Fubini 2∫vConv=(∫v)²,
  0<IvMT, and the jWin(D1)-sandwich integral mechanics (O5–O8, O10).  These are genuinely open
  analytic obligations; this pass certifies them at the math level and carries them as Lean
  hypotheses.

## Verdict
Math-level certificate: **sound**.  Lean bridge: **compiles, honest**.  Adversarial review of
the closed-form derivation is recommended for a formal audit of O5–O8 (bounded external
review of the product-to-sum / Fubini steps against [XF′ Thm 8.1]).
