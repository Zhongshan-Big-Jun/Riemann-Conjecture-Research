# Approach Registry

Run: `R-20260814T045000Z-extpress-2f36ae`.

| Route | Owner | State | Exact gap |
|---|---|---|---|
| k=9 pressure certificate (`F_8\ge f_9`, 8 vars) | solver | ACTIVE (compute) | need certified $f_9\ge0.0038296$ for a record |
| k=11 pressure certificate (`F_{10}\ge f_{11}$, 10 vars) | solver | PENDING | feasibility vs time budget; 10 vars |
| General-k chain (symbolic $C_k(m)$) | solver | DONE (verified k=3,k=7) | — |
| Class-limit / ceiling | solver | DONE (formal) | needs large-block spectral control for m→∞ rigor |
| O2 re-verification (3-pt, 7-pt) | solver | DONE (byte-identical) | — |

## Route families considered

- **A. Raise k in the OpenAI pressure class.** The main thrust. Cost grows
  exponentially in $d=k-1$; 8 variables (k=9) is the next feasible step; 10
  variables (k=11) is likely infeasible in-time without a smarter pruner.
- **B. Improve the 3-point (triangle) bound.** Already dominated (< 7-point); not
  a path past 0.6730085.
- **C. Better test-family / kernel (ψ0, quartic).** Requires re-proving Theorem D
  baseline; out of scope for the finite-certificate step, noted as open.
- **D. Escape the bandwidth-one ceiling via gap-dependent inner products.** The
  OpenAI class already does use gap weights; its own ceiling ≈ 0.673058 (formal),
  well below 0.6818. Re-confirmed.

## Decisions (recorded in ledger)

- Choose k=9 as the primary target (next integer after 7), k=11 as secondary.
- Reuse repo kernel/rounding/report infra via a generalized `verify_kpoint.py`.
- Validate the generalized verifier byte-identically against the k=7 certificate
  BEFORE trusting it for k=9 (done: hash-identical).
- Justify grid/precision in the paper trail for any k≥9 certificate.
