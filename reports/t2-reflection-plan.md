# T2 certificate reflection — concrete implementation plan (2026-08-16)

## Goal

Formalize in Lean the finite certificate
`F₈(g) ≥ 392/100000 for all g ∈ [0,∞)^8`
from `nine-point-f8-gt-392over100000-grid2000.txt`.

## Current situation

- The certificate file is **metadata-only** (571 B): kernel/2nd-deriv table hashes,
  node count 64,748,524, maximum depth 80, initial boxes 256, surviving components
  `[[1868,2458];[3511,30823]]`.
- It does **not** contain the branch-and-bound box tree, so Lean cannot directly reflect
  the certificate.
- The verifier `verify_kpoint_parallel.py` computes sound interval lower bounds
  (`down_add`, `down_mul`, `down_ratio`, RangeMinimum tables) and prunes boxes whose
  lower bound ≥ target.

## Preferred route (a): compressed pruning certificate + Lean exact-rational checker

### Step 1 — instrument the verifier to count/dump terminal pruned boxes

**Status 2026-08-16: instrumented copy created** at
`runs/rigorous-open-math-research/R-20260814T131528Z-f9push-d3b58c/reproducibility/verify_kpoint_parallel_t2count.py`
(original audited verifier untouched). It adds `--emit-boxes` and `--boxes-out`; the counting
pass is simply running it without `--emit-boxes` and reading `T2 accepted terminal boxes:`.
The original audited verifier remains byte-identical. **The real counting pass
(`9 392/100000 --grid 2000 --precision 128 --workers 8`) was started 2026-08-16 and is
running in the background.**

Add an optional `--emit-boxes out.json` mode to `verify_kpoint_parallel.py`:

- In `_process_slice`, whenever a box is **pruned** (accepted because `box_lower ≥ target`),
  append the box coordinates `[[lo0,hi0],...,[lo7,hi7]]` (exact dyadic/rational endpoints;
  the B&B splits at grid-aligned points, so endpoints are rationals with denominator
  `grid` or powers of two if midpoint splits) to a per-worker list.
- Also record the `box_lower` rational lower bound used at pruning.
- At the end, merge per-worker lists and write a JSON file:
  ```
  {
    "format": "t2-pruning-cert-v1",
    "grid": 2000,
    "target": "392/100000",
    "kernel_table_sha256": "39a209d3...",
    "boxes": [
      {"box": [[lo0,hi0], ...], "lower": "num/den"},
      ...
    ]
  }
  ```
- Run a **counting pass** first (no dump) to learn how many terminal boxes there are.
  The full B&B visits 64.7M nodes, but the number of **pruned terminal boxes** may be
  much smaller; if it is ≤ ~1–5M, dumping is feasible. If it is too large, proceed to
  Step 1b.

### Step 1b — if terminal boxes are too many: coarser certified partition

Instead of the full B&B tree, run a **separate certified partition pass**:

- Partition each of the 256 initial boxes into a modest number of sub-boxes using the
  same interval arithmetic, but stop splitting once `box_lower ≥ target`.
- The union of accepted sub-boxes must cover the initial box; use the same component
  superset logic to prove coverage.
- Emit only the accepted boxes. This may produce fewer boxes than the full B&B because
  the full B&B also does tangent-pruning refinements; but it is still sound and Lean-checkable.

### Step 2 — embed the kernel table as exact rationals

- `build_kernel_table` currently produces 128-bit fixed-point entries (31368 entries).
  For Lean reflection we need **exact rational** kernel-table values (or verified rational
  enclosures).
- The table is generated from `K(x) = ∫ cos(√2 t) cos(2πxt) dt`; entries are floating
  approximations. We must either:
  - emit the table as exact rationals from a high-precision rational evaluation (e.g.,
    `fmpq` from `python-flint` with enough precision, rounded outward), or
  - keep the 128-bit fixed-point entries and prove in Lean that they are valid lower
    bounds for the true kernel (requires a verified enclosure of the kernel integral,
    feasible with the same integration bound as `KernelLimit`).
- Size: 31368 entries ≈ 500 KB as text; embeddable in Lean as a `def`/`native_decide` data.

### Step 3 — Lean checker

- Add module `Record9.T2Cert` (or `Zeta23.Pressure.f8_cert` in the snapshot extension).
- Parse the emitted JSON at **elaboration time**? Lean cannot parse JSON at runtime in
  `native_decide` without a parser; instead generate a Lean file containing the box list
  as a literal `List (Fin 8 → ℚ × ℚ)`.
- Define `box_lower` exactly as in the verifier but over `ℚ`:
  - sums of box endpoints (dyadic rationals),
  - RangeMinimum replaced by an explicit table lookup with a **precomputed lower-bound
    table** (or, simpler, evaluate the kernel on a dense grid of the box with the same
    monotonicity/range-min argument).
- For each box, prove `box_lower ≥ 392/100000` by `native_decide` (or `norm_num` on the
  rational computation).
- Prove coverage: the union of the box list covers `[0,∞)^8` using the same component
  superset construction (`[[1868,2458];[3511,30823]]` is the surviving component range).
- Conclude `∀ g ≥ 0, F8 g ≥ 392/100000` by the finite case split.

### Step 4 — verification

- Run the generated Lean checker with `lake build Record9.T2Cert`.
- Cross-check the emitted box JSON against a fresh run of the verifier (same hashes).
- Add `#print axioms` check (expect base-only) and update `STATUS.md` O3.

## Fallback route (b): verified verifier

Porting the full RangeMinimum/tangent-pruning machinery into Lean with verified bounds is
a months-scale task. Not preferred.

## Risks / open questions

1. **Terminal box count**: unknown until a counting pass runs. If > ~10M, the coarser
   partition (Step 1b) or a higher-level decomposition (e.g., certified lower envelope)
   is needed.
2. **Rational kernel table**: need a reproducible exact-rational emitter. The existing
   table is 128-bit fixed-point; we must either trust those as proven lower bounds (adds a
   proof obligation) or emit exact rational enclosures.
3. **Runtime of `native_decide`**: 1M+ boxes with 8-dimensional rational arithmetic may be
   slow; can batch/parallelize by splitting the Lean file into modules or using `decide`
   with optimized rationals.

## Status

Not started. This plan is the scoping deliverable for T2; next concrete action is the
instrumentation/counting pass (Step 1) in `verify_kpoint_parallel.py`.
