# Research ledger — R-20260816T050000Z-m5exact-3f8a

## 2026-08-16 (UTC≈05:00–07:10)
- Set up run dir; loaded skill; reviewed G1 whiteboard, m5_shapes.py scaffold, D5_exact.json,
  probe report, moment-run whiteboard & scripts.
- Discovered the scaffold `m5_shapes.py` is WRONG: shape_integral omits the ρ_b determinant and
  count_tuples miscounts; its "m_5 ≈ 474" is meaningless.
- Derived the correct formula m_k = Σ_σ J_σ, J_σ = ∫Πcycle·ρ_b, and verified it reproduces
  m_2=4/3, m_3=2, m_4=13/4 exactly (the anchor).
- First box-spline coarea engine had a bug ([-1/2,1/2]^n cube + wrong m=1 length) giving wrong
  c_2; switched to [0,1]^n cube + proper vertex enumeration (boxspline2.py), validated on
  c_2..c_10 (c_8=151/315, c_10=15619/36288).
- Ran k=5 enumeration: clean rationals but the all-distinct D_5 and (1,1,1,2) showed float
  cancellation residues (~1e-3) that spurious-reconstructed. A single b=4 partition was
  numerically buggy (returned −0.00436 instead of 0).
- Root-caused the coarea float hull bug: over-coarse vertex dedup. Fixed dedup to start at
  ndec=12 → the b=4 anomaly resolved; D_5 residual dropped to ~1e-6.
- Built an INDEPENDENT high-precision engine (exact-fraction Delaunay simplex volumes) and
  cross-validated every distinct shape value: 1/3, 7/60, 1/15, 1/180, 0, and the b=4 vanishing
  (≈4e−13, −4.5e−13) and confirmations of all hp values. The "(1,2,2) 5178/86089" and
  "(1,1,3) 2954/44309" noise = true 1/15.
- Resolved the exact decomposition to m_5 = 1 + 5/3 + 9/4 + 1/3 + 13/36 = 101/18.
- Hankel: Λ_1=1/4, Λ_2=5/36 exactly; Λ_3,Λ_4 need m_6..m_8 (sampler evidence shows plateau
  ~0.149,~0.148 — decay NOT pinned).
- DPP simulation: L=25 noisy (5.26 at h=0.05); L=50 high-stat gives m_5≈5.4465±0.084 (h=0.02),
  ≈5.4923±0.079 (h=0.05). Consistent-with but ~1.5–2σ below 101/18 (finite-L + h-bias).
- Documented everything; generated SHA256SUMS.

## Decisions
- Not computing m_6 exactly this pass: Bell(6)=203 partitions with higher-dim box-splines are
  heavy and the float engine is fragile at m=7..9; flagged as the natural next step to pin Λ_3.
- Reported the task's "surviving shapes = blocks size ≤ 2" as INCORRECT (blocks of size 3,4
  contribute); actual vanishing is by #blocks b≥4.
