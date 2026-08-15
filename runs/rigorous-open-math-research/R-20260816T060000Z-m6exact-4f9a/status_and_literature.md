# Status and literature — R-20260816T060000Z-m6exact-4f9a

## Problem status
The exact 6th trace moment of the random sine-process Gram matrix is **m_6 = 640/63**. Together with
the audited exact m_1..m_5, this gives the exact Hankel values Λ_1=1/4, Λ_2=5/36, **Λ_3=247/2519**,
and the sequence (1/4, 5/36, 247/2519) is strictly decreasing. The **decay-vs-plateau fork is
resolved in favor of decay** at the exact level; the "plateau" estimate (Λ_3≈0.149) is impossible
for any positive spectral measure consistent with m_1..m_5.

## Known anchors
- Sinclair/Bessel sine-DPP kernel K(x,y)=sinc(x−y); the Gram matrix `[sinc(t_j−t_k)]` of sinc
  translates in Paley–Wiener space is a central object in random sampling/Riesz-basis theory (e.g.
  arXiv:1409.8494, the KdV/Hill random-operator thread — same Gram matrix; confirms provenance but
  does not supply m_6).
- Reduction SL ⟺ μ_λ({0})=0 ⟺ Λ_m(0)→0 and exact m_1..m_4 (Λ_1=1/4, Λ_2=5/36) from run
  R-20260815T120000Z-sllemma-7b21e4.
- Exact m_5=101/18 and the shape-decomposition + exact box-spline machinery from run
  R-20260816T050000Z-m5exact-3f8a.
- c_{2n}=B_{2n}(0) classical; this run derives c_12 and re-derives c_2..c_10.

## Novelty / risk note
The finding that b≥4 shapes do not all vanish at k=6 (they do at k=5) is new and must be weighed
carefully: it invalidates the naive "b≥4⇒0" extension. The positivity/anchor makes the numbers
self-consistent; full sympy re-verification of b=4 (65 shapes) is the residual audit.

## Citation URLs
- https://ar5iv.labs.arxiv.org/html/1409.8494#11 — Gram matrix `[sinc(t_j−t_k)]` in Paley–Wiener
  sampling / random Hill-eigenvalue thread (exact object matched).
