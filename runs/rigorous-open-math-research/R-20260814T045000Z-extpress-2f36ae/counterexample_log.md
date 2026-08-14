# Counterexample Log

Run: `R-20260814T045000Z-extpress-2f36ae`. Tested edge cases, failed lemmas, and
obstruction mechanisms.

## Tested / ruled out
- **k=9 with target f_9=19/5000 = 0.0038**: certificate EXISTS but yields
  C_9=0.67298995 < 0.67300853 (below k=7 record). Not a counterexample — a
  valid but non-improving certificate. Root cause: at f_9=0.0038 the max rigorous
  m_9=271 vs k=7's m_7=269, and the extra penalty $(m-1)/(500m)$ + smaller $A_0/m$
  for 8 gaps makes C_9 slightly worse than C_7 at the same f. Improvement requires
  f_9 strictly above the k=7 value.
- **Record threshold**: $C_9>0.673008528 \iff f_9\ge0.0038296$ (exact scan,
  `threshold_analysis.py`); class limit beats it iff $f_9>0.0037263$.
- **3-point (triangle) mechanism** does not reach the k=7 record (0.6725198).
- **Scoping of F_8**: numerical min $\approx0.00398$ (evidence only) — comfortably
  above the record threshold, enabling f_9=0.0039.

## Exact obstructions / infeasibility (honest)
- **Single-thread 8D verification** (grid 4000) >695s with no 100k nodes: per-node
  cost of 8D Arb tangent bounds (36 sinc evals + 8×8 LDL) is ~25-40x the 6D case.
  Required the parallel verifier.
- **k=11 (10 variables)** exhaustive: expected explosion (per-node 10D Arb LDL *and*
  node count) makes it infeasible in this session's time budget (see scoping).
- **m→∞ class-limit improvement** requires uncontrolled large-block spectral
  monotonicity; not a rigor statement on its own.

## No counterexample to the k=9 chain
No configuration with F_8 < 39/10000 exists (certificate FAILs loudly if any
terminal box is unresolved); k=9 constant verified at high precision.
