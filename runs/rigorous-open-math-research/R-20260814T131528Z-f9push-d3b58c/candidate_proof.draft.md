# Candidate Proof — C₉ at f₉ = 0.00395 (DRAFT, awaiting certificate)

Run: `R-20260814T131528Z-f9push-d3b58c`. Status: **RIGOROUS_PARTIAL_RESULT (pending the
certificate; draft prepared 2026-08-14, numbers pre-computed and manager-verified)**.

## Theorem (draft)

If the k=9 pressure certificate F₈(g₁,…,g₈) ≥ 39,500/10,000,000 = 0.00395 for all gᵢ ≥ 0
is certified (finite universally-quantified Arb B&B, grid 4000 (preferred) or 2000, 128-bit),
then, unconditionally,

  liminf_{T→∞} N₀ˢ(T,2T)/N(T,2T) ≥ C₉(f₉) with the general chain formula
  C₉(f) = (H_MT − (m(f)−1)/(500·m(f))) / (1 − f·n(f)/m(f)),
  n(f) = ⌈1/f⌉ − 1, m(f) = 8 + n(f), A₀(f) = f·n(f) < 1.

At f₉ = 0.0039 (certified, extpress): n = 256, m = 264, A₀ = 0.9984, and the formula reduces
to the closed form (6875·H_MT − 1315/96)/6849 = 0.67305364595258992520… .
At f₉ = 0.00395 (this run): n = 253, m = 261, A₀ = 0.99935 < 1 ✓,
C₉(0.00395) = 0.67308556213350404907…   (manager, mpmath 70 digits,
exact rational form: (26,100,000·H_MT − 52,000)/26,000,065;
note: the (6875·H_MT − 1315/96)/6849 closed form is specific to m = 264 and does NOT apply
at m = 261 — the general formula above is used).

## Proof chain (verbatim from extpress general-k derivation; only the certificate changes)

1. Baseline: S ≥ H_MT·N − o(N) (Lean Theorem D).
2. Stability refinement: S ≥ H_MT·N + Δ(M°) − o(N) (OpenAI Lemma 2.1/Cor 2.2, audited).
3. Certified pressure: F₈ ≥ f₉ (NEW certificate, this run).
4. Block-energy: E_m + (1/500)(y_m−y₁) ≥ f₉(m−8).
5. Block-defect: Δ(G_B) + (1/500)span(B) ≥ A₀ − o(1), A₀ = f₉·(m−8) < 1.
6. Pinching/averaging over m = 261 offsets: Δ(M°) ≥ (A₀/m)S − ((m−1)/(500m))N − o(N).
7. Conclusion: (1 − A₀/m)S ≥ (H_MT − (m−1)/(500m))N − o(N) ⟹ liminf ≥ C₉.

## To be completed on certification

- Insert the certificate file (kernel_table_sha256, second_derivative_sha256, nodes,
  max_depth, surviving components) into reproducibility/certificates/.
- [DONE 2026-08-15] Exact rational constants (mpmath 70 digits, release-checklist.md):
  C₉(0.00395) = (26,100,000·H_MT − 52,000)/26,000,065
              = 0.673085562133504049073235491525348279794216631656324415345203…
  A₀ = f₉·n = 99935/100000 = 0.99935; 1 − A₀/m = 1 − 99935/26,100,000;
  (m−1)/(500m) = 260/130,500.
- ξ′ linked record: C₉^{ξ′}(0.00395) = (26,100,000·H_{ξ′} − 52,000)/26,000,065
  = 0.869224726234155780682210369165264862803577221356718139899266…
  (same certificate; H_{ξ′}^{MT} = 0.8678888651990519355503147104203403132225704976166306446…;
  reports/linked-ladder.md).
