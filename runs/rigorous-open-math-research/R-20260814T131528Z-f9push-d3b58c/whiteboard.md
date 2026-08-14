# Whiteboard — f9push-d3b58c

- **Run ID:** R-20260814T131528Z-f9push-d3b58c
- **Task packet ID:** Q-20260814-criticalline-p1-507bb5

## Current plan

✅ RELEASE EXECUTED 2026-08-15: f₉ = 0.00392 certified (grid-2000, 64,748,524 nodes;
all expected values matched). New records: C₉(ζ) = 0.673066472675939665848…,
C₉(ξ′) = 0.86920009109661916184… (candidate_proof.md, FRONTIER, index/runs.json,
audit_report.md all updated; manager-level audit PASS).

**2026-08-15 correction**: the original 0.00395 target FAILED certification (both grid-2000
and grid-4000): true min of F₈ ≈ 0.00395005 (configuration
[1.0465, 1.996, 1.9995, 1.9995, 1.9865, 1.04525, 1.97575, 1.04525], value
0.003950049001339790, exact-kernel verified + box-minimization); margin ≈ 5e-8 vs
verifier bound-loss ≈ 1e-5 → infeasible (f9-ladder.md CORRECTION section). The earlier
"true min 0.0039818" was a local minimum (k9_opt); the scoping optimization missed the
lower basin. Release retargeted to 0.00392 (margins 1.1e-5 / 3.0e-5).

## Route history

- 22-worker spawn stall; 8-worker restart (grid-2000 and grid-4000, 128-bit) [SUCCEEDED]
- Verifier patched with --out atomic write (job-system stdout loss workaround) [SUCCEEDED]
- 0.00395 runs launched 2026-08-14T23:13Z (pwsh-1 grid-4000, pwsh-2 grid-2000), still running [PARTIAL]
- Final constants verified via exact rational forms (mpmath 70 digits) [SUCCEEDED]
- whiteboard + release-checklist + candidate_proof.draft prepared [SUCCEEDED]
- ξ′ candidate audits A1–A6 CLOSED manager-level PASS; AdmWindow cos blueprint complete (reports/admwindow-cos-instance.md) [SUCCEEDED]
- Canonical ξ′ computation script established (analytic vConv, dps=120; nested-quadrature noise documented); all record tails digit-exact (dps=80/120 pure-mpmath) [SUCCEEDED]
- Release expectations precomputed + cross-validated against TWO known certificates (0.0039 grid-4000, 0.0038 grid-2000: components + kernel hashes byte-for-byte); initial_boxes = (count)^8 = 256 interpretation corrected [SUCCEEDED]
- Soundness stack B6 (i–vii) complete: rounding, components, truncation, loud-fail, kernel identity, true minimum 0.0039818, tangent-pruning convexity audit [SUCCEEDED] — **note: B6(vi) "true minimum 0.0039818" SUPERSEDED 2026-08-15 (local minimum only; see CORRECTION)**
- Records consistency audit across FRONTIER/README/index (no drift) [SUCCEEDED]
- 0.00395 runs FAILED (loud fail at leaf boxes; bounds 0.0039314/0.00394017 below target) [FAILED] (informative: pinned true min ≈ 0.00395005)
- 0.00392 constants precomputed (exact forms (657,500·H_MT − 1,310)/655,001; mpmath dps=90) [SUCCEEDED]
- 0.00392 grid-2000 certification launched (pwsh-4, 8 workers) 2026-08-15 [PARTIAL]
- 0.00392 grid-2000 certificate LANDED 2026-08-15T04:59+08 (verified=true, nodes 64,748,524, depth 80; all precomputed expected values matched; kernel sha 39a209d3…, second 29ca4522…, components [[1868,2458];[3511,30823]], initial_boxes 256) [SUCCEEDED]
- Release executed: candidate_proof.md finalized; FRONTIER/index/RESUME updated (records ζ 0.673066472675939665848, ξ′ 0.86920009109661916184); manager-level audit PASS (audit_report.md); checklist items checked [SUCCEEDED]
- Expected certificate values precomputed for 0.00392 grid-2000: cutoff 31368, kernel sha256 39a209d3e4a897d982023ab49db27a206401824c769980572433dc4c47387297, components [[1868,2458];[3511,30823]], initial_boxes 256, second-deriv sha256 29ca4522e12a991b7ab48943838a174fb2350b328ecc2155d9ecba4cb429f32c [SUCCEEDED]

## Ideas to return to

- 0.00393/0.00394 premium runs: margins at the critical leaf are razor-thin (0.00393
  grid-4000: 1.02e-5; grid-2000: 1.4e-6) — only after the 0.00392 release lands.
- SL lemma (sine-kernel Gram): 5th literature pass + random-Gram model probe
  (m₂ = 4/3, m₃ = 2 EXACT under the random sine-process Gram model — see
  reports/sl-lemma-random-gram-probe.md; m₄ ≈ 3.22 ± MC noise vs 13/4 target, pending
  exact polytope computation). Toeplitz/lattice Gram model ELIMINATED (degenerates to
  identity — sinc(πk) = 0 for k ∈ ℤ∖{0}).

## Open obligations

- Independent (third-party) re-audit of the 0.00392 certificate + record theorem
  (audit-dispatch-prompt.md; manager-level pattern; subagents crash-prone).
- Optional premium step 0.00393 grid-4000 (razor-thin margin 1.02e-5 at the critical
  leaf) — only if a premium record is wanted.
- SL lemma (open theorem; moment side exact, spectral evidence strong).
- Stage C Lean instances (AdmWindow cos blueprint ready).

## Key artifacts

- reproducibility/verify_kpoint_parallel.py, release-checklist.md (0.00392),
  candidate_proof.draft.md (0.00392), f9-ladder.md (CORRECTION section)
- reproducibility/certificates/ (pending: nine-point-f8-gt-392over100000-grid2000.txt)
