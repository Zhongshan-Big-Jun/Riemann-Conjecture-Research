# f₉ = 0.00395 release checklist (2026-08-14)

To execute the moment either certification run (pwsh-1 grid-4000 / pwsh-2 grid-2000) lands its
certificate file in `runs/…/f9push-d3b58c/reproducibility/certificates/`.

## 1. Certificate validation
- [ ] File exists: `nine-point-f8-gt-395over100000-grid{2000,4000}.txt`, contains
      `verified=true`, `target=F8 >= 395/100000`.
- [ ] `kernel_table_sha256` recorded; recompute on the kernel table for the given
      (grid, precision) and compare (deterministic). **Expected values (precomputed
      2026-08-15, manager; recipe: cutoff = floor(15.8·grid)+8, table =
      build_kernel_table(grid, cutoff, 128), hash = table_sha256(table)):
      grid-2000: cutoff 31608 → `c23c661cdcc16a175ebb5bf528e657d5efba5a1f28dbc8ed9b75f4a8a52f9b22`;
      grid-4000: cutoff 63208 → `0861f5203a42977ad41a8a2f0f727e9bed7042bce5133dd05e6f8f62ae099868`.**
- [ ] `second_derivative_table_sha256` recorded (recompute with
      build_second_derivative_lower_table(grid, cutoff, second_start=min(⌊0.95·grid⌋, cutoff−2), 128)).
- [ ] `nodes`, `maximum_depth`, `surviving_gap_components_cells` sanity:
      **expected initial_boxes / components (precomputed):
      grid-2000: initial_boxes 16,345,098, components [(1867,2460);(3508,31024)];
      grid-4000: initial_boxes 65,267,952, components [(3736,4921);(7016,62047)].**
      Nodes ≥ initial_boxes (each box visited ≥ once); depth ≥ 73; elapsed consistent
      with the CPU budget (~300k core-s grid-2000, ~800k grid-4000 at 8 workers).

## 2. Theorem write-up (candidate_proof.md in the run root)
- [ ] Chain (general-k derivation; only the certificate changes):
      1. S ≥ H_MT·N − o(N) (Lean Thm D); 2. S ≥ H_MT·N + Δ(M°) − o(N) (audited Lemma 2.1);
      3. NEW certificate F₈ ≥ 0.00395; 4. block-energy; 5. block-defect
      (n = ⌈1/0.00395⌉−1 = 253, m = 261, A₀ = 0.99935 < 1); 6. pinching/averaging
      (A₀/m = 0.99935/261, (m−1)/(500m) = 260/130500); 7. conclusion
      C₉(0.00395) = (H_MT − 260/130500)/(1 − 0.99935/261) = 0.67308556213350404907…
- [x] Manager arithmetic re-verification (mpmath 70 digits, 2026-08-15 00:20 +08):
      H_MT = 0.67250070367941164573437979080329518859340302862626…
      H_{ξ′}^{MT} = 0.8678888651990519355503147104203403132225704976166306446…
      (re-derived from reports/xi-prime-mt-window.py at dps=60; matches record)
      Exact rational forms (pure-mpmath; float64 pitfalls avoided by integer coefficients):
        C₉(ζ,0.00395)  = (26,100,000·H_MT − 52,000)/26,000,065
                        = 0.673085562133504049073235491525348279794216631656324415345203…
                        (matches synced record …04907; earlier intermediate check at
                         …04898 was a float64-division artifact — superseded)
        C₉(ξ′,0.00395) = (26,100,000·H_{ξ′} − 52,000)/26,000,065
                        = 0.869224726234155780682210369165264862803577221356718139899266…
                        (matches synced record …78068)
      Cross-checks (already-synced ladder, exact forms):
        C₉(ζ,0.00398)  = (25,900,000·H_MT − 51,600)/25,800,102
                        = 0.673104634442792575956499574373982916213631188024769810765723…
        C₉(ξ′,0.00398) = 0.869249338962126782706252517912015003369543883519171113941332…
      Closed-form identity at f=0.0039: (2,640,000·H − 5,260)/2,630,016
                        = (6875·H − 1315/96)/6849 verified to 1e-71.
- [ ] ξ′ linked record: C₉^{ξ′}(0.00395) = 0.86922472623415578068… (reports/linked-ladder.md;
      same certificate, H_{ξ′}^{MT} = 0.86788886519905193555…).

## 3. Ingestion & sync (user requires sync of every result)
- [ ] index/runs.json updated (status, hashes); FRONTIER.md record rows updated
      (ζ: 0.6730856; ξ′: 0.8692247).
- [ ] validate_pipeline.py --project . clean (0 problems).
- [ ] git add/commit/push; verify `git status` clean and ls-remote matches HEAD.
- [ ] activity log entries.

## 4. Follow-ups
- [ ] Dispatch independent audit of the new certificate + record theorem (audit request
      packet pre-prepared: reports/f9-00395-audit-request.md (B1–B5); extpress precedent:
      manager audit PASS-with-limits; subagents crash-prone — manager-level recommended).
- [ ] Consider a 0.00396 run only if the 0.00395 runs close comfortably (cost gradient:
      5-10×).
