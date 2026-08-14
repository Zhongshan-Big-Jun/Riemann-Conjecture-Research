# f₉ = 0.00392 release checklist (2026-08-15, retargeted)

**History**: the original 0.00395 target FAILED certification on 2026-08-15 (both grid-2000
and grid-4000 runs; see f9-ladder.md "CORRECTION" section): the true minimum of F₈ is
≈ 0.00395005 (configuration [1.0465, 1.996, 1.9995, 1.9995, 1.9865, 1.04525, 1.97575,
1.04525], value 0.003950049001339790, verified by exact-kernel evaluation + box
minimization), so the 0.00395 margin is ≈ 5e-8 while the verifier's rigorous box-bound loss
is ≈ 1e-5 — 0.00395 is infeasible with this machinery. **Release target stepped down to
f₉ = 0.00392** (margins ≈ 1.1e-5 above the critical leaf bound, ≈ 3.0e-5 above the presumed
true min). Certification run: pwsh-4 (grid-2000, 8 workers, precision 128, launched
2026-08-15).

To execute when pwsh-4 lands its certificate file in
`runs/…/f9push-d3b58c/reproducibility/certificates/`.

## 1. Certificate validation
- [x] File exists: `nine-point-f8-gt-392over100000-grid2000.txt`, contains
      `verified=true`, `target=F8 >= 392/100000`. (Landed 2026-08-15T04:59+08; sha256
      7F25401A14F897CD1EC26C4B0E0A25A5F87943CFB656329012CB17919280FAC3.)
- [x] `kernel_table_sha256` = **39a209d3e4a897d982023ab49db27a206401824c769980572433dc4c47387297** ✓ (MATCHES expected; independently recomputed in the audit).
- [x] `second_derivative_table_sha256` = **29ca4522e12a991b7ab48943838a174fb2350b328ecc2155d9ecba4cb429f32c** ✓ (MATCHES expected; recomputed in the audit).
- [x] `nodes`, `maximum_depth`, `surviving_gap_components_cells` sanity:
      **components [[1868,2458];[3511,30823]] ✓ MATCH; initial_boxes 2^8 = 256 ✓;
      maximum_depth 80 ≥ 73 ✓; nodes 64,748,524; elapsed 8,765.75 s @ 8 workers
      (≈ 34.8k core-s, within the 20–120k estimate); pruning split
      tangent 11,393,731 / interval 20,874,136 / pressure 106,523.**

## 2. Theorem write-up (candidate_proof.md in the run root)
- [ ] Chain (general-k derivation; only the certificate changes):
      1. S ≥ H_MT·N − o(N) (Lean Thm D); 2. S ≥ H_MT·N + Δ(M°) − o(N) (audited Lemma 2.1);
      3. NEW certificate F₈ ≥ 0.00392; 4. block-energy; 5. block-defect
      (n = ⌈1/0.00392⌉−1 = 255, m = 263, A₀ = 0.9996 < 1); 6. pinching/averaging
      (A₀/m = 2499/657500, (m−1)/(500m) = 131/65750); 7. conclusion
      C₉(0.00392) = (H_MT − 131/65750)/(1 − 2499/657500) = (657500·H_MT − 1310)/655001
      = 0.673066472675939665848…
- [x] Manager arithmetic re-verification (mpmath dps=90, 2026-08-15):
      H_MT = 3/2 − (1/√2)·cot(1/√2) = 0.67250070367941164573437979080329518859340302862626…
      H_{ξ′}^{MT} = 0.86788886519905193555031471042034031322257049761663064461430394239118…
      (canonical dps=120 string, activity log 2026-08-15T05:45Z)
      Exact rational forms (pure-mpmath; integer coefficients):
        C₉(ζ,0.00392)  = (657,500·H_MT − 1,310)/655,001
                        = 0.673066472675939665848379945149956391669879116706338817644865705…
        C₉(ξ′,0.00392) = (657,500·H_{ξ′} − 1,310)/655,001
                        = 0.869200091096619161839954323888625751630669422158034337098576708…
      Cross-check (closed form, already-synced record):
        C₉(ζ,0.0039) = (2,640,000·H_MT − 5,260)/2,630,016
                      = 0.673053645952589925209110000745508505608552950085983191119032970…
                      (matches extpress record 0.6730536459526 ✓ chain form sanity)
      Ladder cross-checks (same m,n family):
        C₉(ζ,0.00391) = 0.67305992191189169;  C₉(ξ′,0.00391) ≈ 0.86919430 (ladder).
- [ ] ξ′ linked record: C₉^{ξ′}(0.00392) = 0.86920009109661916184… (reports/linked-ladder.md;
      same certificate, H_{ξ′}^{MT} canonical).

## 3. Ingestion & sync (user requires sync of every result)
- [ ] index/runs.json updated (status, hashes); FRONTIER.md record rows updated:
      ζ: 0.6730664726759 (0.00392 certificate); ξ′: 0.8692000910966; the 0.00395 row is
      marked INFEASIBLE (see FRONTIER "f₉=0.00395" note) — the old PENDING rows
      (0.6730855621335 / 0.8692247262342) must be replaced by the infeasibility note.
- [ ] validate_pipeline.py --project . clean (0 problems).
- [ ] git add/commit/push; verify `git status` clean and ls-remote matches HEAD.
- [ ] activity log entries.

## 4. Follow-ups
- [ ] Dispatch independent audit of the new certificate + record theorem (audit request
      packet: reports/f9-00395-audit-request.md — RETARGETED to 0.00392 in place; B1–B6
      soundness stack unchanged; expected values in §1 above; extpress precedent: manager
      audit PASS-with-limits; subagents crash-prone — manager-level recommended).
- [ ] Premium targets 0.00393/0.00394: margins at the critical leaf are razor-thin
      (0.00393 grid-4000: 1.02e-5 above the leaf bound; grid-2000: 1.4e-6 — risky); only
      pursue after the 0.00392 release lands (cost 3–10×, several days).
- [ ] Document the true-minimum correction (f9-ladder.md CORRECTION section) in the next
      stage summary; the earlier "true min 0.0039818" scoping claim was a local minimum.
