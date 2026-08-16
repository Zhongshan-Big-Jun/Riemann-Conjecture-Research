# Counterexample / edge-case log — R-20260816T110000Z-m7exact-ea0a

## G2-rule survival edge cases (k=7)
- **b=1 (all-equal block {0..6}):** H_σ has no edges; `components()` returns 0. This is the
  trivially-nonzero case (J=1, every cycle edge is a self-loop, ρ_1=1). Kept (not counted as
  disconnected). Verdict: PASS (J=1, matches m_1..m_6 pattern).
- **b=5,6,7 partitions:** all fail `m ≥ 2b−2` (for k=7, m ≤ 7 while 2b−2 ≥ 8 for b≥5).
  All 337 pruned are low-surplus; none is called disconnected by the G2 rule, matching the
  structural fact that the closed cycle visits every block. The upstream D_5=D_6=0 result is
  reproduced in spirit (all-singleton b=5,6 of k=7 vanish). Verdict: consistent.

## Independent cross-check of partition count
- Two independent enumerations of Bell(7) both give 877 (restricted-growth strings vs
  upstream `partitions_of`). No counterexample found.

## H-isoclass collapse correctness
- Canonical H_σ under block relabeling is a purely combinatorial fact (permutation-invariant
  canonical string). 540 survivors → 18 isoclasses. Verified each isoclass has a single
  (b, profile, m) tuple. No anomaly.

## Engine agreement
- For every computed b=3 isoclass so far, the audit-grade exact engine and the fast engine
  agree to `engine_diff = 0.0` at float precision (well under 1e-12). No discrepancy found.

## Open items (not counterexamples)
- Full m_8 (b=3,4,5) is open; only b≤2 exact partial computed. Recorded as a budget gap,
  not a mathematical obstruction.
- Λ_4 needs m_8 (Hankel determinant size) — see candidate_proof.md.
