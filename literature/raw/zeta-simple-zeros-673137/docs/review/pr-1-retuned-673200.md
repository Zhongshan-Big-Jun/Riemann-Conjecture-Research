# Review: PR #1 — "Certified retuning candidate at 67.3200117%" (viva97)

Reviewer: Claude Fable (maintainer session), 2026-08-12.
Verdict: **GENUINE — recommend accept as record candidate.**

## Claim

Keep the published 7-term window; retune pressure to 1/2736 and the exact
position weights; certify F ≥ 891/200000; deduce, with m = 272 and a sharper
certified window baseline H ≥ 3362285207/5·10⁹,

    liminf N₀ˢ/N ≥ 0.6732001170127618568… > 1683/2500,

i.e. +0.0000625 over the repository's 0.673137630699.

## What this review verified

1. **The finite inequality, replayed through PRISTINE main-branch code.**
   Their candidate JSON (kernel coefficients bit-identical to ours; 21 exact
   rational weights) was run through the unmodified `main` verifier at
   grid 4000: completed with exit 0 and a full report (the report object is
   constructible only on `verified=True`; any failure raises). Search tree
   **node-identical** to their recorded run: 2,168,370 nodes, 1,084,347
   pruned, depth 50, 324 initial boxes, identical prune-class counts, and
   identical w-table SHA-256 (416ac41d…). The second-derivative table hash
   differs as expected (their tail-rounding hardening perturbs last ulps)
   without changing a single pruning decision. Wall: 3213 s on 10 workers.
2. **Span capacities:** all six sums hand-checked to equal 2,000,000/10⁶
   exactly; weights reflection-symmetric.
3. **Deduction arithmetic**, independently in Arb (192-bit): A = 1.18503,
   R = 1.17718166…, B = [0.6732001170127618568182 ± 1.5e-22] ≥ 1683/2500;
   m = 272 confirmed optimal for their (ε, p).
4. **Sharper H baseline:** our certified enclosure
   H(v) = [0.67245704141454428878 ± 4.3e-21] covers 3362285207/5·10⁹ with
   ~1.4e-11 margin.
5. **Their verifier modifications** (reviewed line-by-line): all three are
   rigor *strengthenings* — outward rounding of series tail radii (fixes a
   half-ulp non-rigor in the original), exact-integer pressure cutoff,
   stricter intersection error handling. Plus a new certified monotonicity
   bound (max v′(s)/s ≤ −0.776 on [0, 1/2]), which simplifies the §7.1
   window-interface justification.
6. **Framing:** claims are properly hedged as a certified record candidate
   inheriting the same analytic interface as the base repo; provenance and
   attribution preserved; prior construction retained as `legacy_design`
   with tests.

## Notes / nits (non-blocking)

- Thin certification margin (0.165% vs. our 1.8%): fine — the exhaustive
  interval replay is the decision procedure, and it passes; noted only
  because it explains the 2.2M-node tree.
- `certificates/fast-parts.txt` was regenerated in place (sharper H gate,
  monotonicity line) rather than recorded as a new file; the previous record
  remains in git history and via the legacy gate. Courtesy suggestion only.
- The rewritten paper (490-line diff) was skimmed for claim-consistency,
  not proofread line-by-line; its mathematical content is the same lemma
  chain with retuned constants, all of which were verified directly above.
- README notes two same-day external candidates (tawanerguo-cn 0.6731929,
  npip99 0.6731952); neither has been replayed by us and neither affects
  this PR's verdict.

## Recommended maintainer actions

1. Accept the PR (draft → ready → merge) keeping the "candidate" framing.
2. Optionally ask for the fast-parts record to be split old/new.
3. After merge, replay `zeta-673200-verify all` once more from the merged
   tree and commit the refreshed certificate record.
