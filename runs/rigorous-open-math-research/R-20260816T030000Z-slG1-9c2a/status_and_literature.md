# Status and Literature — R-20260816T030000Z-slG1-9c2a

Current status: **SL gap G1 = prove D_k = 0 exactly for all k ≥ 3** (all-distinct cyclic
terms of the sine-DPP random-Gram trace moments). Two diverging literature passes (subagent
951e7118, f0978f70) both returned verdict **(B) strong structural lead / no directly
applicable theorem**. The general identity D_k=0 is, to our honest search, **NOT stated in
the located literature**. Exact D_5=0 is the concrete deliverable under construction.

## 1. Literature verdict (honest synthesis)

**No located theorem states:** ∫ (∏_a sinc(x_a−x_{a+1})) det[K(x_a,x_b)] dx = 0 for k≥3 on a
projection kernel, nor "each all-distinct cyclic DPP Gram moment D_k = 0", nor the exact
size-≤2-block matching-sum formula for the sine-Gram m_k. This is a genuinely narrow gap.

### Directly relevant theorems (verified, with locators)
1. **Soshnikov, "Gaussian limit for determinantal random point fields", Ann. Probab. 30
   (2002) 171–187**; arXiv:math/0006037; Zbl 1033.60063 — **Lemma 1, eq.(14) (fetched full
   text by subagent)**: the n-th cumulant of a DPP linear statistic is a signed sum over all
   block/cycle decompositions of cyclic kernel-integrals ∫f^{p1}(x1)K(x1,x2)…f^{pm}(xm)K(xm,x1).
   The single-cycle (m=1) block is exactly the **D_k-integrand shape**. **Primary anchor.**
2. **Soshnikov & Wu, "A Note on Cumulant Technique in Random Matrix Theory", Entropy
   25(5):725 (2023)**, DOI:10.3390/e25050725 — same cumulant formula, Remark 4 = sum over
   cycles covering {1..p}. Locator https://pmc.ncbi.nlm.nih.gov/articles/PMC10217726/.
3. **Dappiaggi, Lechner, Morfa-Morales, arXiv:1006.3548** — at operator level, a quasi-free
   state has ω_n=0 for odd n and ω_n = linear combination of products of two-point functions
   for even n (Wick matching). This is the "size-≤2 / pairing-only" principle at the operator
   level (candidate for Lemma P).
4. **Olshanskii, "Determinantal point processes and fermion quasi-free states",
   arXiv:2002.10723** — DPP ↔ fermion quasi-free CAR-state correspondence; correlation
   functions are minors of a kernel; confirms the sine DPP = free-fermion DPP.
5. **Free fermions and the classical compact groups, arXiv:1705.05932**; **Free fermions and
   α-determinantal processes, Cunden–Majumdar–O'Connell, J. Phys. A 52 (2019) 155202,
   arXiv:1811.11556** — sine kernel is the free-fermion n-point density; K_J projective
   kernels give free-fermionic DPPs.
6. **Borodin–Olshanski–Strahov, "Giambelli compatible point processes", arXiv:math-ph/0505021,
   Zbl 1108.05093**; **Bufetov–Lazag, arXiv:2111.05606** — higher correlation structure is
   determined by 2-point (pairing) data (Giambelli compatibility); the representational shell
   for "only size-2 blocks survive".
7. **Hardy et al., "Average characteristic polynomials of DPPs", arXiv:1211.6564** (Ann. Inst.
   H. Poincaré Probab. Stat. 51 (2015) 283) — E[Tr((π_N M π_N)^ℓ)] computed via subset/kernel
   products; closest published trace-moment expansion.

### Critical honesty caveats (why D_k=0 is NONTRIVIAL)
- **Johansson–Lambert, arXiv:1504.06455 (Ann. Probab. 46 (2018))**: higher (≥3) cumulants of
  DPP linear statistics are GENERALLY NONZERO (mesoscopic non-Gaussianity). So "quasi-free ⇒
  higher correlations vanish" is FALSE as a blanket statement for density/linear-statistic
  observables. The desired D_k=0 is a SPECIAL cancellation, not a generic quasi-free corollary.
- **Biscio–Lavancier, arXiv:1507.06506**; **Heinrich, Kybernetika 52 (2016), Zbl 1488.60126**:
  factorial cumulants (connected/Ursell) of DPPs **decay (Brillinger-mixing) but do not
  identically vanish**. Again confirms D_k=0 is a genuine special identity.
- **No source located** for the integral ∫sinc(x1−x2)…sinc(xk−x1)dx vanishing for k≥3, nor for
  "truncated/connected correlation vanishes n≥3" as a verbatim theorem (several subagent
  queries returned nothing or only cluster-decay statements).
- Classical anchors checked: Soshnikov ✓, Shirai–Takahashi (Zbl 1051.60052/3 via Mendeley/
  zbMATH listing, not fetched), Lyons–Steif (arXiv:math/0204325, Zbl 1068.82010), Johansson ✓,
  Balian–Brezin (no result returned), Ursell/Araki–Wichtermann (Balslev–Verbeure, CMP 7 (1968)).

### Mapping to the gap
If D_k is the single-cycle (m=1) block in Soshnikov's cumulant formula with f≡1, then D_k=0
means that m=1 block cancels against the (opposite-signed) higher-block terms — a cancellation
the classical cumulant formula does NOT automatically imply (and which Johansson–Lambert/Brillinger
literature warns is NOT generic). The precise engineering: **D_k = exact cyclic integral; prove it
vanishes by the box-spline/Fourier signed-sum (Prong 2) or by showing the m=1 cumulant block
cancels the remainder.** This is the stated gap.

## 2. Novelty statement
The specific identity D_k=0 (all-distinct cyclic Gram moments for the sine/projection DPP) and
the resulting size-≤2 matching-sum for m_k are NOT in the literature as stated theorems. No
fabricated citations: all locators come from actual web_search returns; two subagents independently
cross-checked.

## 3. Technical status of the two prongs
- Prong 1 (literature): **complete, honest (B)**. No direct theorem; strongest scaffolding =
  Soshnikov cumulant cycle-sum + quasi-free pairing + Giambelli compatibility. The exact "m=1
  block vs higher blocks cancel" bridge is the missing piece.
- Prong 2 (exact D_5): in progress via (i) box-spline/coarea vertex-enumeration volume
  (D_3≈0, D_4≈0 at ~1e-10 confirmed; k=5 under robustness refinement), (ii) delegated compute
  subagent, (iii) delegated exact m_5 decomposition.
