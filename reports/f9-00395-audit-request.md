# Audit request — f₉ = 0.00392 record theorem + certificate (packet, prepared 2026-08-15, retargeted)

Run root: `runs/rigorous-open-math-research/R-20260814T131528Z-f9push-d3b58c` (project
`F:\LaTeX\Riemann Conjecture`). Prepared BEFORE the certificate landed so the audit can be
dispatched immediately at release. Pattern: extpress precedent (manager-level audit
PASS-with-limits; agent subagents crash-prone in this environment — manager-level execution
recommended).

**Retarget note (2026-08-15)**: the original 0.00395 claim was WITHDRAWN before any
certificate existed — both 0.00395 certification runs failed loudly (true minimum of F₈ ≈
0.00395005; margin ≈ 5e-8 vs verifier bound-loss ≈ 1e-5; see f9-ladder.md CORRECTION). The
packet now targets f₉ = 0.00392 (grid-2000 run pwsh-4; margins ≈ 1.1e-5 above the critical
leaf bound, ≈ 3.0e-5 above the presumed true min).

## Claim

If the certificate `reproducibility/certificates/nine-point-f8-gt-392over100000-grid2000.txt`
(`verified=true`) proves F₈(g₁,…,g₈) ≥ 392/100000 = 0.00392 for all gᵢ ≥ 0 (8-variable Arb
branch-and-bound, 128-bit), then unconditionally:

    liminf_{T→∞} N₀ˢ(T,2T)/N(T,2T) ≥ C₉(ζ)  = (657,500·H_MT − 1,310)/655,001
                                            = 0.673066472675939665848379945149956391669879116706338817644865705…
    liminf_{T→∞} N₀ˢ_{ξ′}(T,2T)/N_{ξ′}(T,2T) ≥ C₉(ξ′) = (657,500·H_{ξ′} − 1,310)/655,001
                                            = 0.869200091096619161839954323888625751630669422158034337098576708…
    H_MT   = 3/2 − (1/√2)cot(1/√2)   = 0.67250070367941164573437979080329518859340302862626…
    H_{ξ′} = 2 − κ₁(1, v_MT)         = 0.8678888651990519355503147104203403132225704976166306446…
    n = ⌈1/0.00392⌉ − 1 = 255, m = 8 + n = 263, A₀ = 0.00392·255 = 2499/2500 < 1.

## Audit items

- B1 (certificate): file exists; `verified=true`; `target` = F8 >= 392/100000; recompute
  `kernel_table_sha256` (deterministic) — **expected (precomputed 2026-08-15, manager):
  grid-2000 `39a209d3e4a897d982023ab49db27a206401824c769980572433dc4c47387297` (cutoff
  31368)** — and `second_derivative_table_sha256` (second_start =
  min(⌊0.95·grid⌋, cutoff−2) = 1900); **expected
  `29ca4522e12a991b7ab48943838a174fb2350b328ecc2155d9ecba4cb429f32c`**; both recipes were
  cross-validated 2026-08-15 against the extpress f=0.0039 grid-4000 certificate (kernel
  7029ac0f…, second-derivative 26715cd5… reproduced exactly; details in the run's
  release-checklist.md §1); sanity on `nodes` (no exact expectation — 0.00392 is a strictly
  smaller search space than the failed 0.00395 run, which consumed ≈ 52k core-s before its
  first loud fail; extpress f=0.0039 grid-4000 precedent 53,137,290 nodes at a looser
  target), `maximum_depth` (≥ 73), `surviving_gap_components_cells` (expected
  [[1868,2458];[3511,30823]] — discovery logic cross-validated byte-for-byte against the
  extpress certificate 2026-08-15), **`initial_boxes` = (component count)^8 = 2^8 = 256**
  (box construction itertools.product(comps, repeat=8), NOT the product of component sizes —
  corrected 2026-08-15); no terminal boxes outside the verified region (loud-fail semantics
  of the verifier).
- B2 (formula): C₉(f) = (H − (m−1)/(500m))/(1 − f·n/m) with n = ⌈1/f⌉−1, m = (k−1)+n, k = 9;
  exact rational identity at f = 0.00392: 1 − A₀/m = 1 − 2499/657500 = 655001/657500,
  and (H − 131/65750)·657500 = 657500·H − 1310 (since 657500/65750 = 10), so
  C₉ = (657,500·H − 1,310)/655,001; recompute at ≥ 60 digits.
- B3 (chain): steps 1–7 of candidate_proof.draft.md (baseline Lean Thm D; stability
  refinement OpenAI Lemma 2.1/Cor 2.2 audited; block-energy (BE₉); block-defect (BD₉) with
  A₀ = 2499/2500 < 1; pinching/averaging (AV₉) with defect numbers A₀/m = 2499/657500 and
  (m−1)/(500m) = 131/65750; conclusion). General-k derivation:
  runs/…/extpress-2f36ae/candidate_proof.general-k-derivation.md (reproduces k=7, k=3).
- B4 (ξ′ transfer): A1–A6 audit closure (reports/xi-prime-audit-manager.md) — the same
  certificate serves both families (window-determined kernel); AdmWindow cos blueprint
  (reports/admwindow-cos-instance.md).
- B5 (dependency honesty): no numerical evidence masquerading as proof; the certificate is
  the only new computational input over the extpress record; everything else is audited
  paper-level (Lean: Thm D baseline, XiPrime formula; extpress: PASS-with-limits).
- B6 (soundness stack, all verified manager-level 2026-08-15; one item SUPERSEDED):
  (i) rounding directions — down_* are strict binary64 lower bounds (nextafter toward −inf);
  (ii) component discovery keeps a superset (conservative lower-bound test); (iii)
  truncation soundness — the +8 slack in cutoff = ⌊0.00392·4000·grid⌋+8 gives linear-only
  bound > target_upper at the last in-table cell (grid-2000: 0.003920875 at idx 31367), so
  no counterexample involves a gap cell ≥ cutoff; (iv) loud-fail exit 2 on terminal
  violations; (v) kernel identity — scoping kernel = certificate kernel (sinc evenness);
  (vi) **SUPERSEDED 2026-08-15**: the earlier "true minimum ≈ 0.0039818" was a LOCAL
  minimum; the certified-true minimum is ≈ 0.00395005 (configuration
  [1.0465, 1.996, 1.9995, 1.9995, 1.9865, 1.04525, 1.97575, 1.04525], value
  0.003950049001339790, exact-kernel mpmath dps=50 + L-BFGS-B box minimization; the 0.00395
  certificate is infeasible, f9-ladder.md CORRECTION) — the 0.00392 target margin ≈ 3.0e-5
  against this value; (vii) tangent-pruning soundness (audited 2026-08-15 by code reading):
  s = coeff_signed(span, second_min(L,R)) is a pointwise lower bound of the Hessian block
  coefficient (sign-aware coefficient rounding + nextafter-down + min of cell lower bounds);
  Hessian ⪰ Σ s·J_block (all-ones J PSD); arb_PD (exact arb Cholesky, pivot > 0) is the
  authoritative convexity check (in_heuristic is only a fast pre-filter); for convex F₈ the
  first-order enclosure lower = value − Σ|grad_j|·rad_j is a rigorous lower bound (exact
  rational midpoints, arb kernel evaluation, upper-rounded |drv|); comparison against the
  exact rational target; any precondition failure returns None (no prune); second-derivative
  table pole-avoided (cells ≥ 0.95·grid) while box_lower uses the singularity-free sinc form.

## Expected verdict format

PASS / F-xxx with exact locations; open obligations; audit report path + sha256.

## Where to write the report

`runs/…/f9push-d3b58c/audit_report.md` (manager-level) + rows updated in FRONTIER.md and
index/runs.json; activity log entry.
