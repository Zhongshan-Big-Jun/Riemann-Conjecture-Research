# Approach registry — M3-open-A AtOne certificate for κ₁(1,vMT)

## Route families considered
1. **AtOne pattern instantiation (CHOSEN).** Mirror `AtOne.lean` exactly: define κ₉, prove
   `κ₁(1,vMT) ∈ [κ₉, κ₉+ε₉]` via the D₁ certificate's `D1trunc9 ≤ D₁ ≤ D1trunc9 + ε₉`,
   `vConv ≥ 0`, the Fubini identity, and the `jWin_one_le_of_le` device.  This is the 
   established, formally-verified structure; minimizes novel proof burden.  Status: done
   (math + Lean bridge).
2. **Full-vConv rational approximation (rejected).** Approximate vConv vMT by rational
   tables/polynomials with certified error and produce an exact-rational κ₉.  Rejected: it
   loses the tightness of the closed form and adds a host approximation to certify; the
   closed form is available and exact, so κ₉ is better defined as the real `(aMT+J1MT)/(IvMT)²`
   and enclosed rigorously.  Recorded as the honest resolution of "exact rational κ₉".
3. **Direct analytic evaluation of J1 (not needed).** Because vConv has an exact closed form,
   J1 = 2∫₀¹ D1trunc9·vConvMTcl dr is a finite combination of sin/cos of √2 and rationals;
   it could be evaluated in closed form, but the rigorous Simpson-with-global-M₄ enclosure
   (ARB) already gives width 2·10⁻¹⁶ ≪ ε₉, so a closed form was not required.

## Route state
- Route 1: OWNER M3-open-A, state **COMPLETED** at math level; **MACHINE_ACCEPTED_PENDING_AUDIT**
  for the Lean bridge (open analytic obligations O5–O8, O10 re-declared as hypotheses).
- Route 2: REJECTED (design rationale recorded).
- Route 3: NOT REQUIRED (the ARB enclosure suffices).

## Open obligations to close the Lean part (M3-open-A formal)
- O5 vConv closed form, O6 vConv≥0, O7 Fubini 2∫₀¹vConv=(∫v)², O8 0<IvMT, and the integral
  mechanics O10 (jWin(D1trunc9,1,vMT)=J1MT).  A later formalization pass can discharge these
  as real lemmas (they are all elementary/known results).  Until then `kappaXi_one_vMT_mem` is
  conditional.
