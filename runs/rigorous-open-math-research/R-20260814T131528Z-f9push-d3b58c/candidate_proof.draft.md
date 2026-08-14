# Candidate Proof — C₉ at f₉ = 0.00392 (DRAFT, awaiting certificate)

Run: `R-20260814T131528Z-f9push-d3b58c`. Status: **RIGOROUS_PARTIAL_RESULT (pending the
certificate; draft prepared 2026-08-14, retargeted 0.00395 → 0.00392 on 2026-08-15 after
the 0.00395 certification FAILED — see f9-ladder.md CORRECTION: true min of F₈ ≈ 0.00395005,
so 0.00395 is infeasible; numbers below pre-computed and manager-verified at dps=90)**.

## Theorem (draft)

If the k=9 pressure certificate F₈(g₁,…,g₈) ≥ 392/100,000 = 0.00392 for all gᵢ ≥ 0 is
certified (finite universally-quantified Arb B&B, grid 2000, 128-bit; run pwsh-4), then,
unconditionally,

  liminf_{T→∞} N₀ˢ(T,2T)/N(T,2T) ≥ C₉(f₉) with the general chain formula
  C₉(f) = (H_MT − (m(f)−1)/(500·m(f))) / (1 − f·n(f)/m(f)),
  n(f) = ⌈1/f⌉ − 1, m(f) = 8 + n(f), A₀(f) = f·n(f) < 1.

At f₉ = 0.0039 (certified, extpress): n = 256, m = 264, A₀ = 0.9984, and the formula reduces
to the closed form (6875·H_MT − 1315/96)/6849 = 0.67305364595258992520… .
At f₉ = 0.00392 (this run): n = 255, m = 263, A₀ = 0.9996 < 1 ✓,
C₉(0.00392) = (657,500·H_MT − 1,310)/655,001 = 0.673066472675939665848…   (manager, mpmath
dps=90; the (6875·H_MT − 1315/96)/6849 closed form is specific to m = 264 and does NOT apply
at m = 263 — the general formula above is used).

## Proof chain (verbatim from extpress general-k derivation; only the certificate changes)

1. Baseline: S ≥ H_MT·N − o(N) (Lean Theorem D).
2. Stability refinement: S ≥ H_MT·N + Δ(M°) − o(N) (OpenAI Lemma 2.1/Cor 2.2, audited).
3. Certified pressure: F₈ ≥ f₉ (NEW certificate, this run).
4. Block-energy: E_m + (1/500)(y_m−y₁) ≥ f₉(m−8).
5. Block-defect: Δ(G_B) + (1/500)span(B) ≥ A₀ − o(1), A₀ = f₉·(m−8) = 0.9996 < 1.
6. Pinching/averaging over m = 263 offsets: Δ(M°) ≥ (A₀/m)S − ((m−1)/(500m))N − o(N).
7. Conclusion: (1 − A₀/m)S ≥ (H_MT − (m−1)/(500m))N − o(N) ⟹ liminf ≥ C₉.

## To be completed on certification

- Insert the certificate file (kernel_table_sha256, second_derivative_sha256, nodes,
  max_depth, surviving components) into reproducibility/certificates/.
- [DONE 2026-08-15] Exact rational constants (mpmath dps=90, release-checklist.md):
  C₉(0.00392) = (657,500·H_MT − 1,310)/655,001
              = 0.673066472675939665848379945149956391669879116706338817644865705…
  A₀ = f₉·n = 2499/2500 = 0.9996; 1 − A₀/m = 1 − 2499/657,500 = 655001/657500;
  (m−1)/(500m) = 262/131,500 = 131/65,750.
- ξ′ linked record: C₉^{ξ′}(0.00392) = (657,500·H_{ξ′} − 1,310)/655,001
  = 0.869200091096619161839954323888625751630669422158034337098576708…
  (same certificate; H_{ξ′}^{MT} = 0.8678888651990519355503147104203403132225704976166306446…;
  reports/linked-ladder.md).
