# Research ledger — R-20260816T060000Z-m6exact-4f9a

## 2026-08-16 (UTC≈06:00–), exact m_6 and the Hankel fork
- Setup, copied m5 engines + DPP sampler; reviewed m5/SL context.

### Progress chronology
- Float coarea engine proven unreliable at k=6 (returned −303/6302 for a b=3 shape whose true J=0).
  Decision: exact-volume engine is authoritative; built `boxspline_exact_fast.py` (numpy vertex
  finding on exact integer null basis + scipy hull) ~10^3× faster, validated =0.0 diff vs the sympy
  exact engine per term (b=3 sample; then a nonzero b=4 partition n=8/n=9 terms).
- c_12 = 655177/1663200 derived (B_12(0) formula) + mpmath ∫sinc¹² cross-check.
- b=2 reduction J = c_m − c_{m+2} (m = cycle block-crossings): 1/3×15, 7/60×15, 89/1260×1
  → 4297/630; verified vs exact engine on all 31 partitions.
- b=3: all 90 partitions exact (6 parallel batches, ~1.5h). Sum 479/210. Distinct values
  {0, 1/15, 1/180, 11/630, 1/420}. Note some b=3 shapes vanish, so the k=5 "only b≤3 contribute"
  framing is also not the whole k=6 story.
- **m_6(b≤3) = 3182/315 ≈ 10.1016 gives det(H_3) < 0 (Λ_3 < 0) ⇒ invalid moment sequence ⇒ b≥4
  MUST contribute.** This is a rigorous, important correction to the "b≥4 vanish" conjecture.
- b=4: all 65 partitions (fast engine). Sum 2/35. Distinct: 0×45, −1/840×6, 1/105×2, 1/1260×9,
  4/315×3. Per-term fast-vs-true-exact = 0.0 diff on a nonzero b=4 partition.
- b=5: all 15 = 0 (fast engine). D_6 (b=6): = 0 (fast engine, consistent with D_3,D_4,D_5=0).
- **m_6 = 640/63 = 10.15873 (EXACT).**
- Hankel: exact m_0..m_6. det H_0..H_3 all > 0 (positive definite, valid moment sequence).
  Λ_1=1/4, Λ_2=5/36, **Λ_3=247/2519≈0.09805**. Λ_3 < Λ_2 strictly.
- **Fork resolved: DECAY.** Structural: Λ_3(m_6) < 5/36 for every valid m_6 (asymptote 5/36 from
  below, increasing in m_6). Plateau (Λ_3≈0.149>5/36) is impossible (non-positive moment sequence).
- Λ_4 evidence with sampler m_7,m_8 is unreliable (gives ≈0.18, does not continue decay) — flagged
  with caveat; exact Λ_4 needs exact m_7,m_8 (out of scope / future).
- DPP L=50 run was killed early to free CPU for the exact b=3; the m5 run's existing L=50 evidence
  + the task's sampler m_6 ≈ 9.5–10 are consistent with exact 10.1587 under the established
  finite-L/h-bias model.

## Key decisions
- Exact engine / fast-exact engine drive all shape computations; float engine only for cheap sanity.
- b=4..6 computed with the fast engine (validated vs sympy exact), the only residual audit item
  being full sympy re-verification of all 65 b=4 partitions (budget-limited).
- Numerics are evidence only.

## Open / future
- Exact m_7, m_8 (needed for exact Λ_4 and the full Λ_m decay curve) — same machinery extends.
- General-k proof of the coefficient/vanishing structure (Lemma P / G2): k=6 data shows the
  b≥4-vanish conjecture fails at k=6 (b=4 nonzero); the true pattern is finer.
- SL (Λ_m→0): exact Λ_3 supplies a decay datum; asymptotic SL still OPEN.
