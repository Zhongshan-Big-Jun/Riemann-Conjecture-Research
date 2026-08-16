# Candidate proof — SL gap G2 residual identity (general-k proof attempt)

Run: `R-20260816T080000Z-g2proof-a24d`
Status line: `RIGOROUS_PARTIAL_RESULT` — the disconnected branch M1 is CLOSED, the b=2 family is
CLOSED, several natural routes are KILLED with recorded counterexamples, and the remaining core
(M2: low-surplus signed box-spline telescoping) is reduced to a precise, exactly-stated
graph/linear-algebra identity. Finite verification through k=6 (275 exact rows) is inherited,
and k=7 new-isoclass checks were started but not completed in budget.

## 1. Setup and inherited anchors

- All notation follows `problem_contract.md` and the upstream G2 run
  `R-20260816T070000Z-g2rule-a1b2`.
- `J_σ = Σ_{π∈S_b} sign(π)·B_{Γ_{σ,π}}(0)`, `Γ_{σ,π} = H_σ ∪ match(π)`,
  `B_Γ(0)` the box-spline value at 0.
- The G2 rule is **verified 100%** on all 275 exact per-partition values (k=3..6):
  `J_σ ≠ 0 ⟺ H_σ connected AND m ≥ 2b−2`.
- Exact moments m_1..m_6 = (1, 4/3, 2, 13/4, 101/18, 640/63); D_3=D_4=D_5=D_6=0.

## 2. M1 — disconnected branch: CLOSED (vacuous)

**Lemma 0 (PROVEN).** For every k and every set-partition σ of {0,…,k−1} with b ≥ 2,
the cycle-crossing multigraph H_σ is **connected**.

*Proof.* The cycle `(0,1,…,k−1,0)` is a closed walk that visits every block. If the blocks
split into two nonempty classes A,B with no H-edge between them, then every step of the walk
stays inside the current class; a closed walk that starts in A and visits both A and B would
have to make an A→B or B→A transition, and that transition is exactly an H-edge. Contradiction.

Consequently the first disjunct of the residual identity (`H_σ disconnected ⇒ J_σ = 0`) is
vacuously true. **M1 is DONE.** The whole content of the general-k proof is M2:

```
J_σ = 0  ⟺  m ≤ 2b−3        (b ≥ 2)
J_σ ≠ 0  ⟺  m ≥ 2b−2
```

## 3. M2 — low-surplus / surplus: exact data, killed routes, open core

### 3.1 Exact certified per-π contributions (small cases)

Using the exact box-spline engine (`coarea_value_exact`) and rational reconstruction, the
following are certified exactly:

- b=3, m=3 (vanish): B-values `+1`, three × `−2/3`, two × `+1/2` ⇒ sum = 0 EXACT.
- b=3, m=4 (nonzero, 1/15): `+1`, −(1/2+2/3+2/3), two × 9/20 ⇒ sum = 1/15 EXACT.
- b=4, m=4, H=4-cycle (vanish): `+1`, six × −2/3, (2,2)={9/20,11/30,9/20}, eight × 1/2,
  (4)=4×11/30+2×2/5 ⇒ sum = 0 EXACT.

These are the base cases that any correct M2 proof must reproduce.

### 3.2 b=2 family: CLOSED (PROVEN)

For b=2, ρ₂ = 1 − K², so the signed sum collapses to `J = c_m − c_{m+2}` with
`c_m = ∫ K^m` and `0 ≤ K ≤ 1`, `K < 1` a.e.; hence `c_m` is strictly decreasing and
`J > 0` for every even `m ≥ 2`. This proves the surplus/nonzero branch for all b=2 shapes.

### 3.3 Killed routes (recorded, with counterexamples)

1. **Multiplicative / cycle-class-function EGF** — KILLED.
   `B_Γ(0)` is not a multiplicative class function of the permutation cycle lengths:
   b=4,m=4 gives `B((2,2)) = 9/20 ≠ (2/3)² = 4/9`, and the (2,2) value splits into
   `{9/20, 11/30, 9/20}` depending on H-adjacency. Therefore the EGF-cancellation trick
   cannot be the proof.
2. **Naive degree-2 contraction** — KILLED.
   Contracting a degree-2 vertex of H does not preserve J: triangle b=3,m=3 has J=0, but the
   contracted b=2,m=2 object has J=1/3 ≠ 0. The determinant ρ_b couples to every block
   variable, so the reduction is not closed without tracking the determinant contraction.

### 3.4 Finite verification beyond the inherited dataset

- The inherited 275-row dataset (k=3..6) already verifies the rule 100%.
- New k=7 H-isoclasses (15 new classes, total 33 at k≤7) were targeted at the surplus
  boundary: b=3,m=7 and b=4,m=7 should be nonzero; b=5,m=7, b=6,m=7, b=7,m=7 should be zero.
  Scripts `verify_k7.py` / `verify_k7_fast.py` were written; the exact run was **not completed
  in budget**, so this is recorded as `[PARTIAL]`, not as proof.

### 3.5 Open core (exact statement)

**Lemma M2 (OPEN).** For b ≥ 3 and a connected H_σ with m = |E(H_σ)|,

```
Σ_{π∈S_b} sign(π) · B_{H_σ ∪ match(π)}(0) = 0   whenever  m ≤ 2b−3,
Σ_{π∈S_b} sign(π) · B_{H_σ ∪ match(π)}(0) ≠ 0   whenever  m ≥ 2b−2.
```

The missing mechanism is a signed box-spline telescoping identity that respects the
determinant `ρ_b` (i.e. the `match(π)` edges), not just the cycle-crossing graph H.

## 4. Honesty and status

- M1 is rigorously proven; b=2 is rigorously proven; the general b≥3 M2 identity is **open**.
- The killed routes are documented with exact counterexamples (`counterexample_log.md`).
- The finite checks are exact computations, not proof for all k; no numerical evidence is
  presented as proof.
- Strongest deliverable: the residual identity is now reduced to the single M2 telescoping
  lemma above, with all small base cases certified.

## 5. Artifacts

- `research_ledger.md` — chronological record.
- `problem_contract.md` — exact target.
- `whiteboard.md` — route/status board.
- `counterexample_log.md` — killed routes.
- `repro_manifest.md` — environment/commands.
- `reproducibility/` — exact box-spline engines, per-J datasets, k7 scripts.
