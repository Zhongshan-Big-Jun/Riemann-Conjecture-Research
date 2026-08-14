# Candidate Proof — C₉ at f₉ = 0.00392 (CERTIFIED 2026-08-15)

Run: `R-20260814T131528Z-f9push-d3b58c`. Status: **RIGOROUS_PARTIAL_RESULT — certified**.
Certificate: `reproducibility/certificates/nine-point-f8-gt-392over100000-grid2000.txt`
(verified=true; grid 2000; 128-bit; nodes 64,748,524; maximum_depth 80; initial_boxes 256;
kernel_table_sha256 39a209d3e4a897d982023ab49db27a206401824c769980572433dc4c47387297;
second_derivative_table_sha256 29ca4522e12a991b7ab48943838a174fb2350b328ecc2155d9ecba4cb429f32c;
surviving_gap_components [1868,2458];[3511,30823]; elapsed 8,765.75 s @ 8 workers;
certificate file sha256 7F25401A14F897CD1EC26C4B0E0A25A5F87943CFB656329012CB17919280FAC3).

## Theorem

The k=9 pressure certificate F₈(g₁,…,g₈) ≥ 392/100,000 = 0.00392 for all gᵢ ≥ 0 is
certified (finite universally-quantified Arb branch-and-bound, grid 2000, 128-bit). Then,
unconditionally,

  liminf_{T→∞} N₀ˢ(T,2T)/N(T,2T) ≥ C₉(f₉) = (H_MT − (m−1)/(500·m)) / (1 − f·n/m),
  n = ⌈1/f⌉ − 1 = 255, m = 8 + n = 263, A₀ = f·n = 2499/2500 < 1,

  C₉(ζ)  = (657,500·H_MT − 1,310)/655,001
         = 0.673066472675939665848379945149956391669879116706338817644865705458885167153…
  H_MT   = 3/2 − (1/√2)·cot(1/√2) = 0.67250070367941164573437979080329518859340302862626…

  **NEW WORLD RECORD** (improves the extpress C₉ = 0.67305364595258992520 by 1.28e-5;
  improves the audited OpenAI C₇ = 0.6730085279277797613 by 5.79e-5).

  Linked ξ′ record (same certificate; window-determined kernel; A6 PASS):

  liminf_{T→∞} N₀ˢ_{ξ′}(T,2T)/N_{ξ′}(T,2T) ≥ C₉(ξ′) = (657,500·H_{ξ′} − 1,310)/655,001
         = 0.869200091096619161839954323888625751630669422158034337098576707703048654253…
  H_{ξ′} = 2 − κ₁(1, v_MT) = 0.8678888651990519355503147104203403132225704976166306446…
  (exceeds the quartic ξ′ record 0.86864 by 5.6e-4; improves the audited 0.0039 candidate
  0.86918353505282747704 by 1.66e-5).

## Proof chain (general-k derivation; only the certificate changes from extpress)

1. Baseline: S ≥ H_MT·N − o(N) (Lean Theorem D).
2. Stability refinement: S ≥ H_MT·N + Δ(M°) − o(N) (OpenAI Lemma 2.1/Cor 2.2, audited).
3. Certified pressure: F₈ ≥ 392/100000 (the certificate above).
4. Block-energy: E_m + (1/500)(y_m−y₁) ≥ f₉(m−8) = 0.00392·255.
5. Block-defect: Δ(G_B) + (1/500)span(B) ≥ A₀ − o(1), A₀ = 0.9996 < 1.
6. Pinching/averaging over m = 263 offsets: Δ(M°) ≥ (A₀/m)S − ((m−1)/(500m))N − o(N)
   with A₀/m = 2499/657500 and (m−1)/(500m) = 262/131,500 = 131/65,750.
7. Conclusion: (1 − A₀/m)S ≥ (H_MT − (m−1)/(500m))N − o(N) ⟹ liminf ≥ C₉.

Exact rational identity at f = 0.00392: 1 − A₀/m = 1 − 2499/657,500 = 655,001/657,500 and
(H − 131/65,750)·657,500 = 657,500·H − 1,310 (since 657,500/65,750 = 10), so
C₉ = (657,500·H − 1,310)/655,001. Manager re-verification at dps=90 and dps=130: digit-exact.

## Certificate provenance

- Verifier: reproducibility/verify_kpoint_parallel.py (validated byte-identically on the
  k=7 certificate and against the extpress f=0.0039 grid-4000 certificate).
- Soundness stack B1–B6 (reports/f9-00395-audit-request.md, retargeted): rounding
  directions (down_* strict binary64 lower bounds), component superset, truncation +8
  slack (verified: linear-only bound 0x1.044096476db45p-8 > target_upper at idx 31367),
  loud-fail exit 2, kernel identity (scoping = certificate kernel), true minimum ≈
  0.00395005 (corrected 2026-08-15; margin ≈ 3.0e-5), tangent-pruning convexity
  (arb_PD Cholesky).
- All expected values precomputed 2026-08-15 and cross-validated against the extpress and
  0.0038 certificates; the landed certificate matches every precomputed value.
- History: the original 0.00395 target failed (true min 0.003950049001339790; margin
  ≈ 5e-8 < bound loss ≈ 1e-5 — infeasible); retargeted to 0.00392 (f9-ladder.md
  CORRECTION).

## Honest status

**RIGOROUS_PARTIAL_RESULT (certified record).** New unconditional constants
0.673066472675939665848… (ζ, N₀ˢ/N) and 0.86920009109661916184… (ξ′, N₀ˢ_{ξ′}/N_{ξ′}).
The probability-1 goal remains OPEN (unconditional 100% needs deep new input; conditional
routes HL*+SL / PCC are proved and documented in the condp1/mainpush runs).
