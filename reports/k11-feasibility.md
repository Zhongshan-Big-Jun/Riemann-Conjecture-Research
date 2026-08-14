# k=11 feasibility assessment (2026-08-14)

Question: can a k=11 pressure certificate (F_10 ≥ f_11, 10 variables) be produced in this
session's environment?

## Cost model (from observed data)

- k=9, 8 variables, f_9 = 0.0039, grid 4000: 53,137,290 nodes, depth 73, ~3464 s at 22
  workers (extress run) — ≈ 15.3M core-s... (22 × 3464 ≈ 76k core-s).
- k=9 scoping: inf F_8 ≈ 0.00398; f_11 scoping: inf F_10 ≈ 0.00405 (evidence only).
- k=11, 10 variables, target f_11 = 0.004 (margin 5e-5 above the indicated minimum):
  boxes = comps^10. With 2–3 surviving components (near-CUE structure, as in k=9), boxes =
  1024–59049; node counts scale roughly with the (dimension − 1)-th power of the grid
  resolution near the tight region: expect ~10^8–10^9 nodes, depth 90+.

## Environment constraints

- 22-worker multiprocessing spawn stalls in this environment (observed twice: worker CPU
  frozen). Only 8-worker pools run reliably (verified healthy; two 8-worker jobs saturate
  16 of 22 cores).
- At 8 workers, a 10^8–10^9-node k=11 run is an estimated 2–10+ days of wall time.

## Verdict

k=11 is **not feasible in this session** (resource-bound). Recorded as an open computational
target with a clear cost model for a future environment with stable >8-worker parallelism or
more cores. The higher-leverage immediate steps remain: (1) certify f_9 = 0.00395 (in
progress, grid-2000 + grid-4000 8-worker runs), pushing ζ to 0.6730856 and ξ′ to 0.8692247;
(2) independent audits A1–A6 of the ξ′ candidate.
