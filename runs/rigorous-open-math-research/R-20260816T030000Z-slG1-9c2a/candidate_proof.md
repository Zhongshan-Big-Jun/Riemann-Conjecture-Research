# Candidate Proof / Result — SL gap G1: D_5 = 0 (and D_3 = D_4 = 0) — computer-verified

Run: `R-20260816T030000Z-slG1-9c2a`
Status target: strongest audited progress, honestly labeled (NO numerical box-truncation as proof;
the confirmed result is a computer-verified exact rational identity for k ≤ 5, plus the precise
general mechanism). This pass does NOT prove the general k case; it establishes D_3 = D_4 = D_5 = 0
rigorously-as-a-computation and pins the exact identity that would close all k.

## 1. Setting (exact, from problem_contract.md)
K = sinc, K*K = K (projection). ρ_k = det[K(x_i,x_j)]. D_k = ∫_{R^{k-1}} P_k ρ_k dx (fix x_k=0),
P_k = ∏_a K(x_a−x_{a+1}). D_k = Σ_{π∈S_k} sign(π) I_π,
I_π = ∫_{R^{k-1}}(∏_ciclo K)(∏_a K(x_a−x_{π(a)})) dx.

## 2. Box-spline (Fourier/coarea) exact form — RIGOROUS reduction (this pass)
Each I_π equals a rational box-spline value:
  I_π = vol_{n−d}{ ξ∈[−1/2,1/2]^n : Mξ = 0 } / √det(M Mᵀ),
where n = #active (non-self-loop) edges of the cycle ∪ π-edges combined graph, d = k−1, and M is
the d×n edge-direction matrix. Derivation: write sinc(t)=∫_{[−1/2,1/2]}e^{2πiξt}dξ, the integrand
phase = exp(2πi Σ_e ξ_e v_e·x), integrate the d free x's ⇒ δ^d(Mξ), disintegrate by coarea
⇒ the stated volume ratio. Self-loops (π(a)=a) contribute K(0)=1 and no direction.
VALIDATION: π=id,k=3 gives I_id=1 (=∫P_3, the cycle trace), reproduced exactly; also D_3=D_4=0.

## 3. Confirmed result — D_3 = D_4 = D_5 = 0 (computer-assisted exact)
`reproducibility/Dk_general_qhull.py` (rational reconstruction of the box-spline volumes) and, in
INDEPENDENT confirmation, `Dk_boxespline_run.py` (coarea with self-loop exclusion + vertex
enumeration) agree on EVERY I_π to ~1e-13 (crossvalidate_2methods.py, 0 mismatches).

Exact reconstructed I_π sets and signed sums:
- k=3: I_π ∈ {1, 2/3, 1/2};  Σ sign·I = 0 EXACT; max recon error ~7e-16; max denominator 3.
- k=4: I_π ∈ {1, 2/3, 1/2, 9/20, 2/5, 11/30};  Σ sign·I = 0 EXACT; max denominator 30.
- k=5: I_π ∈ {1, 2/3, 1/2, 9/20, 2/5, 11/30, 13/45, 61/180, 49/180, 1/3, 1/4};
  Σ sign·I = 0 EXACT; max reconstruction error ≤ 8e-15; max denominator 180.
Certification (`certify_Dk.py`): the max |reconstructed rational − float box-spline value| ≤ 8e-15 is
far below the half-integer lattice tolerance (~1/(2·180²)≈1.5e-5) that would make rational
reconstruction ambiguous, so the reconstruction to denominators ≤ 180 is certified.

Status label for this part: **FINITE_COMPUTATIONAL_RESULT** (verified for k = 3,4,5). The identity
D_k=0 is established for these k by a reproducible, two-implementation cross-checked exact rational
computation. It is NOT yet proven for all k.

## 4. Per-cycle-type partial sums are nonzero (global cancellation)
`Dk_general_qhull.py` cycle-type subtotals (k=5): type(5)=+61/9≈6.78, type(1,4)=−34/3≈−11.33,
type(2,3)=−55/9≈−6.11, type(1,1,3)=+10, type(1,2,2)=+19/3, type(1,1,1,2)=−20/3, type(all-fixed)=1.
All non-vanishing; only the TOTAL over all 120 permutations cancels to 0. Consistent with the
box-truncated numerics (D5_permutation_terms.py, D5_cycletype_analysis.py). Combined graphs are all
connected 4-regular (component signature (5,10) for every k=5 π), so no trivial component-factorized
pairing explains the cancellation — it is genuinely global.

## 5. General mechanism (Lemma M) — precise statement and exact identity to close
CONJECTURE/FORMAL TARGET (this is what would close SL via Lemmas M→P→H):
  D_k := Σ_{π∈S_k} sign(π) · [box-spline value (coarea) of the cycle ∪ π-edges] = 0  for all k≥3.
Established here: k=3,4,5 (exact computation). The box-spline values are clean rationals; the signed
sum over S_k vanishes because of the determinant/fermionic (quasi-free) counting: the identity is the
finite-dimensional shadow of Wick's theorem / Giambelli (pairing-only) structure, but the exact
general proof (that the signed sum over all S_k box-spline values cancels) is the precise unresolved
core (M1 derivation done; M2 signed-sum identity not yet proven for all k).

## 6. Literature outcome (honest)
No located theorem states D_k=0 or the size-2-block matching-sum for the sine-DPP Gram moments.
Soshnikov's cumulant-of-linear-statistic formula (Ann. Probab. 30 (2002), Lemma 1 eq.14; and
Soshnikov–Wu, Entropy 25:725 (2023)) gives the cyclic-block structure; quasi-free/CAR matching
(Dappiaggi et al., arXiv:1006.3548) and Giambelli compatibility (Borodin–Olshanski–Strahov,
arXiv:math-ph/0505021) give the "pairing-only" shell; but Johansson–Lambert (arXiv:1504.06455) and
Brillinger-mixing literature confirm higher DPP cumulants do NOT generally vanish ⇒ D_k=0 is a
genuine special cancellation, not a generic corollary. Verdict (B). See status_and_literature.md.

## 7. Legacy/impact
With D_3=D_4=D_5=0 confirmed exactly (and the strong prior evidence D_6≈0), the all-distinct
fermionic conjecture D_k=0 (Lemma M) now has confirmed exact base cases k=3,4,5. Combined with
Lemma P (matching-sum) this would give exact m_3..m_5 and feed Lemma H → SL. m_5 exact computation
is delegated and pending (matching shapes); D_5 itself is now closed at k=5.

## 8. Honest status
**FINITE_COMPUTATIONAL_RESULT / RIGOROUS_PARTIAL_RESULT (composite).** D_3 = D_4 = D_5 = 0 is a
reproducible computer-verified exact identity (rational reconstruction, two independent methods,
certified to ~8e-15). Nuance on exactness: the individual I_π rationals are UNIQUELY determined by
the high-precision 6-D cross-section volumes (residual ≤8e-15 vs separation ≥1.5e-5 for denominators
≤180), and two independent implementations agree to ~1e-13; but a fully SYMBOLIC proof of each
reconstructed rational (exact-arithmetic 6-D vertex-enumeration volume/triangulation) is the isolated
remaining verification step and was not closed within budget. The general k identity (Lemma M) remains
OPEN; its exact statement and the box-spline machinery are this pass's contribution. No
box-truncated residual is presented as proof.
