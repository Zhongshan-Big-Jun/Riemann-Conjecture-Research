# Audit dispatch prompt — f₉ = 0.00392 record theorem + certificate (2026-08-15)

Dispatch this prompt verbatim (or manager-level execute its steps) the moment the certificate
`runs/rigorous-open-math-research/R-20260814T131528Z-f9push-d3b58c/reproducibility/certificates/nine-point-f8-gt-392over100000-grid2000.txt`
exists and contains `verified=true`. Packet: `reports/f9-00395-audit-request.md` (retargeted
to 0.00392 in place). Precedent: extpress audit PASS-with-limits; subagents crash-prone in
this environment — manager-level execution recommended.

---

You are the independent auditor for a new world-record lower bound on the proportion of
simple zeros on the critical line, project root `F:\LaTeX\Riemann Conjecture`.

## Claim under audit

If the certificate `runs/rigorous-open-math-research/R-20260814T131528Z-f9push-d3b58c/reproducibility/certificates/nine-point-f8-gt-392over100000-grid2000.txt`
(verified=true) proves F₈(g₁,…,g₈) ≥ 392/100000 for all gᵢ ≥ 0 (8-variable Arb
branch-and-bound, grid 2000, 128-bit), then unconditionally:

    liminf N₀ˢ(T,2T)/N(T,2T) ≥ C₉(ζ)  = (657,500·H_MT − 1,310)/655,001
                                      = 0.673066472675939665848379945149956391669879116706338817644865705…
    liminf N₀ˢ_{ξ′}/N_{ξ′}     ≥ C₉(ξ′) = (657,500·H_{ξ′} − 1,310)/655,001
                                      = 0.869200091096619161839954323888625751630669422158034337098576708…
    H_MT   = 0.67250070367941164573437979080329518859340302862626…
    H_{ξ′} = 0.8678888651990519355503147104203403132225704976166306446…
    n = 255, m = 263, A₀ = 2499/2500 < 1.

## Audit items (packet: reports/f9-00395-audit-request.md)

- B1 (certificate): verified=true; target = F8 >= 392/100000; kernel_table_sha256 =
  39a209d3e4a897d982023ab49db27a206401824c769980572433dc4c47387297 (recompute:
  cutoff 31368, build_kernel_table(2000, 31368, 128)); second_derivative_table_sha256 =
  29ca4522e12a991b7ab48943838a174fb2350b328ecc2155d9ecba4cb429f32c (second_start 1900);
  surviving_gap_components_cells = [[1868,2458];[3511,30823]]; initial_boxes = 2^8 = 256;
  maximum_depth ≥ 73; nodes and elapsed_seconds consistent with a ~20–120k core-s search.
- B2 (formula): C₉(f) = (H − (m−1)/(500m))/(1 − f·n/m); at f = 0.00392: 1 − A₀/m =
  655001/657500; (m−1)/(500m) = 131/65750; exact identity (657500/65750 = 10) ⇒
  C₉ = (657,500·H − 1,310)/655,001; recompute at ≥ 60 digits.
- B3 (chain): runs/…/f9push-d3b58c/candidate_proof.draft.md steps 1–7; general-k derivation:
  runs/…/extpress-2f36ae/candidate_proof.general-k-derivation.md (reproduces k=7, k=3).
- B4 (ξ′ transfer): reports/xi-prime-audit-manager.md (A1–A6 CLOSED); same certificate
  serves both families (window-determined kernel); reports/admwindow-cos-instance.md.
- B5 (dependency honesty): the certificate is the only new computational input over the
  extpress record.
- B6 (soundness stack): reports/f9-00395-audit-request.md B6(i)–(vii) — note B6(vi) is
  SUPERSEDED: the true minimum of F₈ is ≈ 0.00395005 (NOT 0.0039818; f9-ladder.md
  CORRECTION); the 0.00392 margin ≈ 3.0e-5 against it; 0.00395 was withdrawn as
  infeasible (margin 5e-8 < bound loss 1e-5).

## Verdict format

PASS / F-xxx with exact locations; open obligations; report path + sha256. Write the report
to `runs/…/f9push-d3b58c/audit_report.md`; update FRONTIER.md rows and index/runs.json;
activity log entry.
