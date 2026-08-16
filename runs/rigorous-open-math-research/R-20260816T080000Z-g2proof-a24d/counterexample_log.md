# Counterexample / killed-route log — R-20260816T080000Z-g2proof-a24d

This log records every candidate mechanism that was tried for M2 and killed, with the exact
counterexample that kills it. No entry here disproves the target theorem; each entry disproves
a proposed proof route.

## K1 — Multiplicative class-function / EGF

**Claim tried:** `B_{H∪π}(0)` depends only on the cycle type of π (multiplicatively across
cycles), so the signed sum over S_b can be evaluated by an EGF.

**Killed by:** exact b=4,m=4 data.
- The (2,2)-cycle class splits: `B((2,2)) ∈ {9/20, 11/30, 9/20}` depending on whether the
  transposition pairs are H-adjacent.
- `B((2,2)) = 9/20 ≠ (2/3)^2 = 4/9`, so it is not multiplicative over cycles.

**Status:** `KILLED`.

## K2 — Naive degree-2 vertex contraction

**Claim tried:** Contracting a degree-2 vertex of H (folding a leaf/path) preserves J, giving
an induction on b.

**Killed by:** triangle b=3,m=3 has J = 0 exactly; contracting a degree-2 vertex gives the
b=2,m=2 object with J = 1/3 ≠ 0. The determinant ρ_b couples to every block variable, so the
contraction is not closed without tracking the determinant contraction.

**Status:** `KILLED`.

## K3 — (Recorded caution) Float-noise trap

The exact engine initially produced a spurious `J ≈ 0.399` for the k=6 profile `[3,1,1,1]`
b=4,m=4; the true value is 0 (allJ.json). This is a numerical cancellation artifact, not a
counterexample to the rule. It is logged so future passes do not trust raw float residuals
near cancellations.

**Status:** `CAUTION`.
