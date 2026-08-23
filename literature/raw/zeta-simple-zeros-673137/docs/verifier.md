# Verifier documentation

## What is proved by machine

1. `zeta-673200-verify fast`
   - min/max of the window v on [−1/2,1/2] via 8192-cell interval evaluation
     (Arb, 256-bit): 3/4 ≤ v ≤ 1; the removable-zero expression for v′/s
     also proves that v is nonincreasing on [0,1/2].
   - H(v) ≥ 3362285207/(5·10⁹) via closed forms (all reducible to sinc = sin z / z at
     exact arguments; see `zeta_ext/h0_cert.py` docstring for the derivation
     of the |s−t| double integral).
   - The final deduction arithmetic (A, R = 2√A−1, η, bound > 1683/2500)
     in 256-bit ball arithmetic.
2. `zeta-673200-verify main`
   - The 6-gap inequality F ≥ 891/200000 (paper §4) for ALL nonnegative gaps,
     by exhaustive subdivision. Recorded run: 2,168,370 nodes, grid 1/4000,
     maximum depth 50.
3. `zeta-673200-verify gate`
   - Reproduces the ainta 7-point certificate
     (`ainta/zeta-simple-zeros`, F₆ ≥ 19/5000) with this code base:
     707,797 nodes, verified. This is the correctness gate: same search
     structure, tables built through an independent evaluation path.
4. `zeta-673200-verify legacy-main`
   - Reproduces the preceding 67.313763% position-weighted construction.

## Enclosure strategy

- Kernel: K_v(x) = Σⱼ cⱼ·S(ωⱼ, 2πx), S(w,c) = (sinc((w−c)/2)+sinc((w+c)/2))/2,
  entire. Values use flint's native `sinc` intersected with a rigorous
  alternating-series evaluation; first/second derivatives use the series
  (|z| ≤ 0.75, 24 terms, explicit tail bound ≤ 2× first omitted term)
  intersected with the closed forms away from z = 0. This handles the
  removable singularities of the derivative formulas at integer x (absent
  for the Montgomery–Taylor kernel, present for the perturbed window).
  Every Arb-to-binary64 tail radius is rounded upward explicitly; disjoint
  independent enclosures raise an error rather than silently falling back.
- Tables: per-cell rigorous lower bounds for w = (K/K(0))² and for w″ on the
  grid, combined by an O(1) sparse-table range-minimum structure.
  All floating-point combination steps are outward-rounded binary64
  (`nextafter` after every add/mul), as in the ainta verifier.
- Search: depth-first subdivision of 6-dimensional cell boxes with three
  pruners: (i) pressure cutoff (p·Σg ≥ target), (ii) interval lower bound
  from the tables, (iii) a convex tangent bound — when the weighted Hessian
  lower bound is certified positive definite (float LDL heuristic re-proved
  in Arb), a first-order Taylor bound at the box center certifies the box.
  A box that reaches single-cell width uncertified raises an error (the
  verifier fails closed).
- Parallelism: initial boxes are partitioned round-robin across worker
  processes; every worker re-verifies its shard independently; table hashes
  are checked identical across workers. Table construction is also
  parallelized by cell ranges. Sharding does not change what is proved —
  the shards partition the initial cover.

## Trust base

- python-flint 0.9.0 (pinned; ships Arb) for ball arithmetic.
- IEEE-754 binary64 with `math.nextafter` outward rounding for table
  combination.
- The Python interpreter and this code (~1100 lines; `src/zeta_ext/`).
- No floating-point optimization result is part of the proof.

## Reproducibility

The recorded runs in `certificates/` include SHA-256 hashes of the exact
binary64 tables. These are reproducible under the pinned python-flint;
the previous record's repository left its dependency unpinned, which is why
its committed auxiliary hash drifts under 0.9.0 (its certificate still
verifies; the drift is packaging, not mathematics — we pin to avoid this).

## Legacy hardening re-verification (no tangent pruning)

`certificates/weighted-p1-grid4000-no-tangent.txt` records a second,
independent certification of the preceding design's F ≥ 1/200 with the convex-tangent pruner
disabled (`use_tangent=False`): 40,511,110 nodes of pure interval
subdivision. In this mode the proof uses only the per-cell lower-bound
tables for w, a code path fully exercised by the correctness gate; an error
in the derivative enclosures could then only cause a false *failure*. Both
legacy runs share identical table hashes. The tighter F ≥ 891/200000 result
has been replayed after rounding hardening and produced identical search
statistics and table hashes, but does not yet have a tangent-free replay.
