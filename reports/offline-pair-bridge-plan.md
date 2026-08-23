# Off-line Pair Bridge — High-Value Research Plan

Status: **PLAN / OPEN RESEARCH DIRECTION**  
Source: upstream `trmdy/zeta-simple-zeros-673137` (`docs/campaign-2.md`)
Copied upstream source: `literature/raw/zeta-simple-zeros-673137/`

## Why this is now the main long-shot

Upstream analysis indicates the k-point pressure certificate class is near
exhaustion:

- best assembled nine-point value ≈ `0.673312742272...`
- family horizon ceilings ≈ `0.67331–0.67340`
- pure pair-energy methods cap at ≈ `0.674826`

The remaining road to `0.675+` is identified as the **off-line pair bridge**.

## The open lemma (paraphrased from campaign-2)

Current methods price only simple on-line zeros. The extremal law for the class
ceiling `p_256 ≈ 0.68182868746...` uses about `31.8%` mark-2 (off-line pair)
mass. To price that mass, one needs a new theorem:

> Prove the multi-pair composition using the kernel's positive-type
> (band-limited Bochner) structure — e.g. a Szegő-type anti-crowding bound
> controlling eigenvalues near the k₂ kink for Gram matrices of translates of
> a positive-definite band-limited function — or a kink-regularized (taxed)
> defect variant.

## What has already been proved / refuted upstream

Proved:

- Exact complex Gram formulas for pair blocks with normalization
  `D = L(β−1/2)/(2π)`, certified by 82,751-box complex-interval (acb) proof.
- Local bridge theorems: raw `δ ≥ d₁₂ + π`; robust `B ≥ d₁₂` and `≥ T²−1`;
  one-pair positive-environment theorem `Δ ≥ D₂ + (T−1)²`.
- A safe global regrouping `D₊` preserving the entire simple-zero defect.

Refuted:

- Additive local pricing; abstract PSD composition from positivity alone;
  naive safe assembly and several counterexamples.

Evidence for the standing conjecture:

- ~10⁵ adversarial configurations survived,
- exact infinite pair-chain (Bloch) limits sustain `0.0101–0.0271` per pair,
- no transition dead zone,
- if the lemma is proved with the measured constants, the assembled bound
  lands in **0.674–0.675**.

## Next research steps

1. Read the upstream complex-pair machinery in
   `literature/raw/zeta-simple-zeros-673137/` and the campaign-2 summary.
2. Target the **multi-pair composition** lemma.
3. Explore **band-limited positive-definite / Szegő-type anti-crowding**
   methods for Gram matrices of translates.
4. If a certified local lemma is found, assemble the global bound and then
   consider Lean formalization.

## Relationship to current objective

- The k-point pressure certificate family remains active, but with small
  expected headroom.
- The **off-line pair bridge** is the higher-payoff direction for going beyond
  ≈ `0.6734`.
- **Kuznetsov / λ > 1** remains a separate long-term backlog, with quantitative
  hardness evidence captured in `reports/upstream-673137-analysis.md`.

## Honest label

This is a plan, not a proof. No new bound is claimed here.
