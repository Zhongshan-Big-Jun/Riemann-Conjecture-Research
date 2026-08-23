# Plan: search for a retuned k=10 / q=9 operating point

Status: **PLAN / FUTURE WORK** — no retuned q=9 certificate has been found or
certified yet.

## Motivation

The multi-certificate LP scans show:

- The canonical q=9 point `(p=1/4500, eps≈0.00395)` is useless in the LP.
- A stronger q=9 operating point would be valuable: e.g. a synthetic
  `(p=1/4500, eps=0.00450)` raises the two-certificate bound to about
  `0.67338732768334`.
- So the next useful input is a **retuned q=9 certificate**, not the canonical
  general-k `F_9 ≥ f_10` result.

## What a retuned q=9 certificate is

A local certificate of the form

```
p * sum_{r=1..9} g_r + sum_{0≤i<j≤9} a_ij w(y_j - y_i) ≥ eps,
sum_{i=0}^{q-r} a_{i,i+r} = 2  for every span r,
a_ij ≥ 0 rational,
```

with a chosen pressure coefficient `p` and pair weights `a_ij` that are not
necessarily the equal-weight canonical choice `2/(q+1-r)`.

The retuned 7pt and 9pt inputs used by the Shi LP are examples of this more
general family.

## Proposed search route

1. Extend the current verifier to accept **variable rational weights**
   `a_ij` (not just the canonical equal weights).
2. For each candidate `p`, solve/optimize the certificate target `eps` over:
   - the rational weight matrix `a_ij` satisfying span capacities 2;
   - all gap configurations where the certificate could fail.
3. This is a **global nonconvex optimization / semialgebraic certificate
   search**. The existing Arb branch-and-bound machinery is the natural base,
   but it must be generalized to optimize over `a_ij` as well as over `g`.
4. Use the existing generalized verifier to certify any promising retuned
   point found by the search.
5. Feed the result into the multi-certificate LP to see the new bound.

## Expected payoffs

- A retuned q=9 point with `eps ≈ 0.0045` could move the multi-certificate
  bound from `0.673316977` to about `0.673387328`.
- A retuned q=8 point could also matter, but the existing retuned 9pt-final is
  already strong and dominates our canonical q=8 points.

## Related artifacts

- `reports/multi-cert-q9-sweep.md`
- `reports/multi-cert-q8-canonical-negative.md`
- `runs/.../R-20260817T030000Z-shiGeneralize-4f2a/`
- `literature/raw/zeta-simple-zeros/` (verified verifier base)

## Honest label

This is a research plan, not a verified result. No retuned q=9 certificate
exists yet.
