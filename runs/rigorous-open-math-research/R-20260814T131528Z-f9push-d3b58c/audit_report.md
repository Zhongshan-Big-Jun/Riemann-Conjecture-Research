# Audit report — f₉ = 0.00392 record theorem + certificate (manager-level, 2026-08-15)

**Verdict: PASS (manager-level, with the scope limits noted below).** Audit of the claim
that the certificate `reproducibility/certificates/nine-point-f8-gt-392over100000-grid2000.txt`
(verified=true) proves F₈ ≥ 392/100000 and hence the new world records
C₉(ζ) = 0.673066472675939665848… and C₉(ξ′) = 0.86920009109661916184….

## B1 — certificate (PASS, every expected value matched)

| item | expected (precomputed 2026-08-15) | certificate | independent recomputation (this audit) |
|---|---|---|---|
| verified / target | verified=true, F8 >= 392/100000 | verified=true, F8 >= 392/100000 | ✓ |
| kernel_table_sha256 | 39a209d3e4a897d982023ab49db27a206401824c769980572433dc4c47387297 | 39a209d3… (same) | **39a209d3e4a897d982023ab49db27a206401824c769980572433dc4c47387297** ✓ (cutoff 31368, grid 2000, 128-bit) |
| second_derivative_table_sha256 | 29ca4522e12a991b7ab48943838a174fb2350b328ecc2155d9ecba4cb429f32c | 29ca4522… (same) | **29ca4522e12a991b7ab48943838a174fb2350b328ecc2155d9ecba4cb429f32c** ✓ (second_start 1900) |
| components / initial_boxes | [[1868,2458];[3511,30823]] / 2⁸ = 256 | [1868,2458];[3511,30823] / 256 | **[[1868, 2458], [3511, 30823]] / 256** ✓ |
| maximum_depth | ≥ 73 | 80 | ✓ |
| nodes | plausible (20–120k core-s) | 64,748,524 (elapsed 8,765.75 s @ 8 workers ≈ 34.8k core-s) | ✓ within range |
| certificate file sha256 | — | 7F25401A14F897CD1EC26C4B0E0A25A5F87943CFB656329012CB17919280FAC3 | ✓ recorded |
| pruning split | tangent/interval/pressure | 11,393,731 / 20,874,136 / 106,523 | consistent with the B6(vii) tangent-pruning stack |

## B2 — formula (PASS)

C₉(f) = (H − (m−1)/(500m))/(1 − f·n/m), n = ⌈1/f⌉−1 = 255, m = 8+n = 263;
1 − A₀/m = 1 − 2499/657500 = 655001/657500; (m−1)/(500m) = 131/65750;
exact identity (657500/65750 = 10) ⇒ C₉ = (657,500·H − 1,310)/655,001.
Recomputed at dps=90 and dps=130 (this session): digit-exact
ζ: 0.673066472675939665848379945149956391669879116706338817644865705458885167153…
ξ′: 0.869200091096619161839954323888625751630669422158034337098576707703048654253…
Cross-checks: C₉(ζ,0.0039) closed form reproduces the extpress record; ladder monotonicity
in n re-verified (n=200 → 0.6730342, n=255 → 0.6730665).

## B3 — chain (PASS)

Steps 1–7 of candidate_proof.md (baseline Lean Thm D; audited Lemma 2.1/Cor 2.2;
block-energy; block-defect with A₀ = 2499/2500 < 1; pinching/averaging with A₀/m =
2499/657500 and (m−1)/(500m) = 131/65750; conclusion). The general-k derivation
(extpress run) reproduces k=7 and k=3 exactly; only the certificate changes.

## B4 — ξ′ transfer (PASS)

A1–A6 closed manager-level PASS (reports/xi-prime-audit-manager.md); the kernel is
window-determined, so one certificate serves both families; AdmWindow cos blueprint
(reports/admwindow-cos-instance.md) is the Stage C formalization path.

## B5 — dependency honesty (PASS)

The certificate is the only new computational input over the extpress record; everything
else is audited paper-level (Lean Thm D baseline; XiPrime formula; extpress
PASS-with-limits). No numerical evidence is presented as proof.

## B6 — soundness stack (PASS; one item superseded)

(i) rounding: down_* strict binary64 lower bounds ✓; (ii) component superset ✓;
(iii) truncation +8 slack: re-verified this session — linear-only bound at idx 31367 =
0x1.044096476db45p-8 > target_upper 0x1.00e6afcce1c59p-8 ✓; (iv) loud-fail exit 2 ✓
(the 0.00395 runs failed exactly this way — machinery trustworthy); (v) kernel identity
(scoping = certificate kernel, sinc evenness) ✓; (vi) true minimum: SUPERSEDED —
0.003950049001339790 (was 0.0039818 local min); the 0.00392 margin ≈ 3.0e-5 ✓;
(vii) tangent-pruning convexity (arb_PD Cholesky; sign-aware coefficients) ✓.

## Scope limits (as in extpress precedent)

- The verifier itself is validated by byte-identical reproduction of the k=7 certificate
  and by matching every precomputed table hash, not by a proof-assistant check.
- The chain is paper-level (not Lean end-to-end); the Lean Thm D baseline is formalized.
- A third-party re-audit is recommended (dispatch: audit-dispatch-prompt.md).

Report file sha256: (computed on commit).
