# Counterexample log — R-20260814T041219Z-condp1-698ec7

Concrete falsifications / edge cases tested while making §7.2(d)–(f) rigorous.

## CE-1 `delta_-1` (invalid moment list)
- Claim refuted: "1 − Λ_m(0)" applied to the printed list (1,3/4,2,13/4) is a lower bound on
  n₊/d. Refutation: m_2 − m_1² = 3/4 − 1 = −1/4 < 0; the 2×2 (and 3×3) Hankel matrices are not
  positive semi-definite, so no probability measure has these moments and the Christoffel number
  blows up (Λ_2(0) = 143/100 > 1 ⇒ 1−Λ_2(0) < 0). Search code: `reproducibility/moments_christoffel_full.py`
  §(A),(B); `reproducibility/check_lambda2_corrected.py`.
- Resolution: the sole fix is m_2(1) = 3/4 → 4/3. Under (1,4/3,2,13/4) the Hankel matrices are PSD
  and Λ_2(0) = 5/36 exactly, restoring 1−Λ_2(0) = 31/36 and 13/18 = 2(31/36)−1.

## CE-2 (the paper's own 5/36 is not from its written list)
- Claim under test: "Λ_2(0;1) = 5/36" from m̂=(1,3/4,2,13/4). Result: **false**. The value 5/36
  is obtained exactly only from the corrected list (1,4/3,2,13/4). This proves the authors'
  internal arithmetic used m_2 = 4/3 (i.e. the written 3/4 is a transcription slip).

## CE-3 (m=1 Cantelli: n₊ can exceed d? — impossible)
- For (1,3/4) the m=1 bound n₊/d ≥ m_1²/m_2 = 4/3 > 1, impossible since n₊ ≤ d. Reinforces CE-1.
  With corrected m_2 = 4/3 the m=1 bound is 3/4 ≤ 1 (feasible).

## CE-4 (recommended edge: spectral density at 0 gap)
- Untested hypothesis family for **SL**: if the sine-kernel Gram spectral density vanished on a
  neighbourhood of 0 (mass gap), then Λ_m(0) → c > 0 and the m→∞ limit is only a positive constant,
  not 1. This is precisely the failure-dichotomy recorded; it is the content of the unverified SL.
  (Not a claimed counterexample — a documented conditional failure mode.)

## CE-5 (off-line pairs make Ĝ indefinite)
- Ĝ is not PSD in general (off-line pairs contribute signature (1,1) blocks). The SOS-witness
  Lemma 3.A handles this correctly (negative eigenvalues reduce the bound), so the n₊-bound remains
  valid for the actual (possibly indefinite) Ĝ; the PSD assumption is only needed for the sharp
  "1−Λ_m(0)" spectral form of Lemma 3.B, applied to the *limiting* measure (which HL* forces to be
  the PSD sine-Gram law). Noted so that no false PSD assumption is imported.
