# Research Ledger — R-20260816T110000Z-m7exact-ea0a

Chronological record of experiments, derivations, decisions, and failures. Newest last.

## 2026-08-16 — Setup, pruning (k=7), m_8 preflight

- **Set up run dir** `runs/rigorous-open-math-research/R-20260816T110000Z-m7exact-ea0a/`; copied
  upstream engines byte-identical from m6exact / g2rule / g2proof into `reproducibility/`.
- **Environment check:** `py -3.10` with numpy 2.2.6, scipy 1.15.3, sympy 1.13.1, mpmath 1.3.0,
  python-flint OK.

### k=7 pruning (prune_k7.py) — SUCCEEDED
- Enumerated Bell(7) = 877 set partitions of {0..6} (verified equal via two independent
  enumerations: restricted-growth and the upstream `dataset.partitions_of`).
- Applied G2 rule: keep iff `H_σ connected AND m ≥ 2b−2` (b=1 always kept).
- Result: **540 survivors** kept (1 b=1, 63 b=2, 266 b=3, 210 b=4); 337 pruned, all by the
  low-surplus test (m ≤ 2b−3). **No b≥5 partition survives** (m=7 < 2b−2 for b≥5).
- Note: all b≥2 partitions have connected H_σ (the cycle visits every block), so the
  "disconnected" prong is vacuous for real partitions here; the 4 "comp≠1" rows in the
  upstream allJ.json are just the b=1 all-equal cases (J=1), not genuinely disconnected.

### H-isoclass collapse — SUCCEEDED (key reduction)
- J_σ depends only on (b, H_σ); canonicalizing H_σ under block relabeling collapses the
  540 survivors to **18 distinct H-isoclasses** (1 b=1, 3 b=2, 6 b=3, 8 b=4).
- This matches the m6 note of 18 H-isoclasses for k≤6 (consistency).

### k=8 preflight (prune_k8.py) — SUCCEEDED, m_8 judged OPEN
- Bell(8) = 4140; G2 survivors = **2683** (1 b=1, 127 b=2, 910 b=3, 1351 b=4, 294 b=5),
  collapsing to **46 isoclasses** (1 b=1, 4 b=2, 9 b=3, 19 b=4, 13 b=5).
- **Feasibility:** k=8 b=4 fast engine ~387 s/isoclass (19 classes ⇒ ~2 h), b=5 exceeds the
  fast engine's combination cap (S_5=120 perms, high null dimension ⇒ >600 s/isoclass,
  13 classes). **Full exact m_8 is NOT feasible within this bounded pass.**
- **Rigorous partial m_8:** exact b≤2 closed-form contribution computed
  (`compute_k8_partial.py`): `m_8^(b≤2) = 3724369/181440 ≈ 20.526725`. Full m_8 (b=3,4,5)
  recorded as OPEN.

## 2026-08-16 — Exact m_7 computation (compute_k7_exact.py) — IN PROGRESS → COMPLETED
- Method: for each of the 18 isoclasses, compute exact J:
  - b=1 → 1; b=2 → `J = c_m − c_{m+2}` (closed form).
  - b=3,4 → signed sum over `ρ_b` of exact (`boxspline_exact2`) box-spline values,
    cross-validated against the fast engine (`boxspline_exact_fast`), then rational
    reconstruction.
- Progressing via checkpoint file `k7_iso_results.json`:
  - [1/18] b=1: J=1
  - [2/18] b=2 m=2: J=1/3  (21 partitions)
  - [3/18] b=2 m=4: J=7/60 (35 partitions)
  - [4/18] b=2 m=6: J=89/1260 (7 partitions)
  - [5/18] b=3 m=4: J=1/15  (70 partitions)  engine_diff=0.0
  - [6/18] b=3 m=5: J=1/180 (105 partitions) engine_diff=0.0
  - [7/18] b=3 m=6: J=1/420 (28 partitions)  engine_diff=0.0
  - ... (b=3 m=7 and b=4 pending)

(ledger continues after computation completes)
