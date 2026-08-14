# Status and literature — OpenAI draft audit

## Problem status (2026-08-14)

- `liminf N0^s/N ≥ 0.673008528` (OpenAI draft) — **verified by this audit** as a correct unconditional theorem
  (given its single computer-assisted input `F6 ≥ 19/5000`, reproduced).
- It strictly improves the previous best `N0^s/N ≥ 0.672500704 = H_MT` (Anthropic Theorem D, Lean-verified).
- The user-level goal `liminf N0/N = 1` remains **OPEN**; the method ceiling (bandwidth-one, configuration-wise)
  is `≈0.68185` ([1] Remark 1.1/§7.5, Proposition 7.4). The audited constant is below that ceiling.

## Exact known-theorem statements used

- [1] Theorem D (dyadic): `N0^s(T,2T) ≥ (2 − 1/c1* − ε)N(T,2T)` with `2−1/c1* = 3/2 − (1/√2)cot(1/√2) = H_MT`,
  plus `N0* ≥ H_MT` and `Nd ≥ (3−1/c1*)/2 = 0.83625…`. Lean: `ThmD.Mult.thmD₀_simple_mult`,
  `thmD₀_dist_mult`, `thmD₀`.
- [1] Theorem 5.8: `tr Ĝ = N(1+O(ET))`, `(trĜ)²/trĜ² = F(λ1)·N(1+O(ET))` (flat window), replaced by
  `‖Ĝ‖²_F = (1/c*_{λ1}+O(1/L))N` for the optimal window (Theorem D proof).
- [1] Prop 4.2 (tail θ₀), Prop 4.4 (s₁ ≥ 4trÂ−‖Â‖²−2N(I')), Lemma 2.2, Lemma 3.2 (base rank–trace).

## The two new inequalities (are they proved?)

1. **Lemma 2.1** `‖P+Q‖²_F ≥ 4tr(P+Q)−3r−4b+D(M)`: **proved analytically** (von Neumann trace inequality +
   convex spectral minimum `(p−n)²+4n`). Not numerical.
2. **Prop 4.1** `F6 ≥ 19/5000`: **proved by a rigorous finite, universally-quantified verification** —
   exact linear proof outside the simplex `Σg≥11.4`, Arb interval branch-and-bound inside; certificate
   reproduced byte-for-byte. Stated precisely in §2.5 of the audit report. Not heuristic sampling.

## Bibliographic resolutions (IDs "as used in [1]" — from the v2 reference list)

- CCLM17: Carneiro–Chandee–Littmann–Milinovich, J. Reine Angew. Math. 725 (2017) 143–182.
  Used [1] §7.1 for optimality of the MT kernel (one-delta extremal problem).
- CGdL20: Chirre–Gonçalves–de Laat, Adv. Math. 361 (2020) 106926; arXiv:1810.08843.
- BHB13: Bui–Heath-Brown, Bull. LMS 45 (2013) 953–961 (19/27 simple, on RH).
- PRZZ20: Pratt–Robles–Zaharescu–Zeindler, Res. Math. Sci. 7 (2020) #2, 74 pp.
- Wu15: X. Wu, Quart. J. Math. 66 (2015) 759–771 (Nd > 0.6603).
- GS25: Goldston–Suriajaya, *Zeta zeros on the critical line*, arXiv:2511.20059v2 (2025) (= local file).
- GS26: Goldston–Suriajaya, *Zeta zeros in a narrow vertical box*, arXiv:2603.28104 (2026).

## Novelty

- Preflight B0 (FRONTIER.md) declared the draft constant unverified. This audit **independently verifies** it,
  so an unconditional `c > 0.673008528` (or a full formalization of the draft) would be novel. No literature
  competition found; the value lies strictly between the Lean `0.67250…` and the `≈0.68185` ceiling.

## Known limitations / gaps to note for the pipeline

- The draft's `F6 ≥ 19/5000` is computer-assisted and not formalized in a proof assistant; a Lean certificate
  consumer would raise confidence further (open, non-blocking for the audit verdict).
- Lemma 3.1 relies on [1]'s rigorous end-effects lemma rather than being fully self-contained.
