# Audit request — f₉ = 0.00395 record theorem + certificate (packet, prepared 2026-08-15)

Run root: `runs/rigorous-open-math-research/R-20260814T131528Z-f9push-d3b58c` (project
`F:\LaTeX\Riemann Conjecture`). Prepared BEFORE the certificate landed so the audit can be
dispatched immediately at release. Pattern: extpress precedent (manager-level audit
PASS-with-limits; agent subagents crash-prone in this environment — manager-level execution
recommended).

## Claim

If the certificate `reproducibility/certificates/nine-point-f8-gt-395over100000-grid{2000,4000}.txt`
(`verified=true`) proves F₈(g₁,…,g₈) ≥ 395/100000 = 0.00395 for all gᵢ ≥ 0 (8-variable Arb
branch-and-bound, 128-bit), then unconditionally:

    liminf_{T→∞} N₀ˢ(T,2T)/N(T,2T) ≥ C₉(ζ)  = (26,100,000·H_MT − 52,000)/26,000,065
                                            = 0.673085562133504049073235491525348279794216631656324415345203…
    liminf_{T→∞} N₀ˢ_{ξ′}(T,2T)/N_{ξ′}(T,2T) ≥ C₉(ξ′) = (26,100,000·H_{ξ′} − 52,000)/26,000,065
                                            = 0.869224726234155780682210369165264862803577221356718139899266…
    H_MT   = 3/2 − (1/√2)cot(1/√2)   = 0.67250070367941164573437979080329518859340302862626…
    H_{ξ′} = 2 − κ₁(1, v_MT)         = 0.8678888651990519355503147104203403132225704976166306446…
    n = ⌈1/0.00395⌉ − 1 = 253, m = 8 + n = 261, A₀ = 0.00395·253 = 99935/100000 < 1.

## Audit items

- B1 (certificate): file exists; `verified=true`; `target` = F8 >= 395/100000; recompute
  `kernel_table_sha256` (deterministic) — **expected (precomputed 2026-08-15, manager):
  grid-2000 `c23c661cdcc16a175ebb5bf528e657d5efba5a1f28dbc8ed9b75f4a8a52f9b22` (cutoff
  31608), grid-4000 `0861f5203a42977ad41a8a2f0f727e9bed7042bce5133dd05e6f8f62ae099868`
  (cutoff 63208)** — and `second_derivative_table_sha256` (second_start =
  min(⌊0.95·grid⌋, cutoff−2)); sanity on `nodes` (expect ≫ 53M grid-4000; extpress f=0.0039
  precedent 53,137,290 at a looser target; grid-2000 smaller), `maximum_depth` (≥ 73),
  `surviving_gap_components_cells` (expected [(1867,2460);(3508,31024)] grid-2000 /
  [(3736,4921);(7016,62047)] grid-4000 — discovery logic cross-validated byte-for-byte
  against the extpress certificate 2026-08-15), **`initial_boxes` = (component count)^8 =
  2^8 = 256 for both runs** (box construction itertools.product(comps, repeat=8), NOT the
  product of component sizes — corrected 2026-08-15); no terminal boxes outside the verified
  region (loud-fail semantics of the verifier).
- B2 (formula): C₉(f) = (H − (m−1)/(500m))/(1 − f·n/m) with n = ⌈1/f⌉−1, m = (k−1)+n, k = 9;
  exact rational identity at f = 0.00395: 1 − A₀/m = 1 − 99935/26100000 = 26000065/26100000,
  and (H − 260/130500)·26100000 = 26100000·H − 52000 (since 26100000/130500 = 200), so
  C₉ = (26,100,000·H − 52,000)/26,000,065; recompute at ≥ 60 digits.
- B3 (chain): steps 1–7 of candidate_proof.draft.md (baseline Lean Thm D; stability
  refinement OpenAI Lemma 2.1/Cor 2.2 audited; block-energy (BE₉); block-defect (BD₉) with
  A₀ = 0.99935 < 1; pinching/averaging (AV₉) with defect numbers A₀/m = 99935/26100000 and
  (m−1)/(500m) = 260/130500; conclusion). General-k derivation:
  runs/…/extpress-2f36ae/candidate_proof.general-k-derivation.md (reproduces k=7, k=3).
- B4 (ξ′ transfer): A1–A6 audit closure (reports/xi-prime-audit-manager.md) — the same
  certificate serves both families (window-determined kernel); AdmWindow cos blueprint
  (reports/admwindow-cos-instance.md).
- B5 (dependency honesty): no numerical evidence masquerading as proof; the certificate is
  the only new computational input over the extpress record; everything else is audited
  paper-level (Lean: Thm D baseline, XiPrime formula; extpress: PASS-with-limits).
- B6 (soundness stack, all verified manager-level 2026-08-15): (i) rounding directions —
  down_* are strict binary64 lower bounds (nextafter toward −inf); (ii) component discovery
  keeps a superset (conservative lower-bound test); (iii) truncation soundness — the +8 slack
  in cutoff = ⌊0.00395·4000·grid⌋+8 gives linear-only bound > target_upper at the last
  in-table cell (grid-2000: 0.003950875 at idx 31607; grid-4000: 0.0039504375 at idx 63207),
  so no counterexample involves a gap cell ≥ cutoff; (iv) loud-fail exit 2 on terminal
  violations; (v) kernel identity — scoping kernel = certificate kernel (sinc evenness);
  (vi) true minimum ≈ 0.0039818 re-verified with the actual kernel (margin 3.2e-5);
  (vii) tangent-pruning soundness (audited 2026-08-15 by code reading): s =
  coeff_signed(span, second_min(L,R)) is a pointwise lower bound of the Hessian block
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
