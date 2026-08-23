# Current status snapshot — Record9 continuation

Date: 2026-08-23

## Certified record

- k=9 pressure certificate: `F₈ ≥ 392/100000` (grid-2000, 64,748,524 nodes)
- C₉(ζ)  = `0.673066472675939665848…`
- C₉(ξ′) = `0.86920009109661916184…`

## Background jobs

| Job | Purpose |
|---|---|
| `bash-36` | ~~k=9 f₉=0.00393 grid-4000 certificate attempt~~ **FAILED** (exit 2; see `runs/.../k9-f393-grid4000-failure.log`) |
| `bash-39` | k=9 T2 terminal-box counting |
| `bash-41` | independent upstream verification of canonical k=9 |

## T2 / reflection progress

- Exact rational kernel table generated (31,368 entries; binary64 hash matches
  the certified table).
- Lean chunked kernel table compiles (`KernelTableGrid2000.lean`).
- npip99 proof-certificate pipeline preserved and smoke-tested:
  - `Z23TREE1` forest exporter works locally;
  - audit of npip report: 1,739,356 nodes / 869,516 splits / 869,840 leaves.
- T2 adaptation plan: `reports/t2-adapt-npip-pipeline.md`.
- Trace exporter prototype: attempted on k=7; instrumented copy diverged
  from the original verifier on the same certificate (unresolved), so the
  prototype was not committed.
- Remaining: trace-event emission from our verifier; k=9 forest size; tangent
  leaf semantics.

## Multi-certificate findings

- Canonical q=8/k=9 certificates do not improve the retuned 7+9 LP.
- Canonical q=9/k=10 point is useless; a strong synthetic q=9 gives about
  `0.673387328` if certified.
- Upstream trmdy analysis says the k-point pressure family is near exhaustion
  (≈0.67331–0.67340).
- Retuned k=10 search plan: `reports/retuned-k10-search-plan.md`.

## Long-term directions

- **Off-line pair bridge**: main high-payoff route to 0.675+; plan in
  `reports/offline-pair-bridge-plan.md`.
- **Kuznetsov / λ>1**: retained backlog; quantitative hardness recorded in
  `reports/kuznetsov-bandwidth-backlog.md`.
- **Conditional higher-moment Christoffel**: correct but conditional.

## Key artifacts

- `literature/raw/zeta-simple-zeros-673137/` — upstream retuned certificates + verifier
- `literature/raw/zeta-zeros-npip/` — proof-certificate/Lean infrastructure
- `runs/rigorous-open-math-research/R-20260814T131528Z-f9push-d3b58c/` — k=9 record run
- `reports/future-work-roadmap.md` — master roadmap
