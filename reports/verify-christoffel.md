# Independent verification of the condp1 core finding (manager, 2026-08-14)

Script: `reports/verify-christoffel.py` (exact rational arithmetic + mpmath numerics).

## Verdict: condp1's §7.2(f) transcription-error finding is CONFIRMED independently

### 1. Moment-sequence validity (exact rational arithmetic)

Christoffel function at 0 for the truncated moment functional:
Λ_m(0) = 1 / ((M_m^{-1})_{00}), M_m = (m+1)×(m+1) Hankel matrix [m_{i+j}],
moments m₀ = 1, m₁ = 1, m₂ = m2, m₃ = 2, m₄ = 13/4.

| List | det H₂ | det H₃ | Λ₁(0) | 1−Λ₁(0) | Λ₂(0) | 1−Λ₂(0) | 2(1−Λ₂)−1 |
|---|---|---|---|---|---|---|---|
| corrected (1, **4/3**, 2, 13/4) | **1/3 > 0** | **5/108 > 0** | 1/4 | **3/4** = m₁²/m₂ ✓ | **5/36** | **31/36** | **13/18** ✓ |
| written (1, **3/4**, 2, 13/4) | **−1/4 < 0** | −143/64 < 0 | −1/3 | 4/3 | **143/100 > 1** | −43/100 < 0 | −93/50 (non-statement) |

- The written list is NOT a valid positive-measure moment sequence (det H₂ < 0).
- The corrected list is valid (det H₂, det H₃ > 0) and reproduces the paper's own numbers
  **exactly**: Λ₂(0) = 5/36 (paper's value) and 2·(31/36) − 1 = **13/18** (paper's value).
- Consistency check: m=1 gives 1 − Λ₁(0) = 3/4 = m₁²/m₂ (Lemma 3.3 / Cauchy–Schwarz), and with
  m₂ = 4/3 the paper's own unconditional R(ψ₀) = 4/3 is recovered (m₂ = 4/3 is literally the
  paper's λ=1 HS ratio).

### 2. Lemma C (sine-DPP second moment), numerical check

- ∫_ℝ sinc²(πu)du ≈ 1.00005 (≈ 1; improper-quadrature error ~5e−5) — exact value 1 (standard).
- ∫_ℝ sinc⁴(πu)du ≈ 0.666666666663 ≈ 2/3 (11 digits).
- Lemma C: E[tr G_L²]/L → 1 + (∫sinc² − ∫sinc⁴) = 1 + 1 − 2/3 = **4/3** ✓
  (numerics give 1.33338 within quadrature error).

### 3. Conclusion

The claim "§7.2(f) of the Anthropic paper contains a transcription slip m₂(1) = 3/4 → 4/3"
is confirmed by: (i) the paper's own Λ₂(0) = 5/36 and 13/18 only compute correctly under
m₂ = 4/3; (ii) exact rational arithmetic (this report); (iii) the sine-DPP exact computation
(Lemma C) and its numerical confirmation; (iv) agreement with the condp1 solver's
`check_lambda2_corrected.py`. The corrected HL* statement yields the rigorous conditional
theorem: HL* + SL ⇒ lim N0^s/N = 1, and HL*(4) ⇒ N0^s/N ≥ 13/18 (pending the run's audit).
