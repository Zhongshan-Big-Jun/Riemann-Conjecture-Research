# Upstream trmdy/zeta-simple-zeros-673137 — key analysis for Record9 continuation

Status: **UPSTREAM_REVIEW / INFORMATION**  
Source: `https://github.com/trmdy/zeta-simple-zeros-673137`  
Commit: `1610b97b7895ff34982260f8dcaf04a0f7b82cf7`  
Copied to: `literature/raw/zeta-simple-zeros-673137/` (2026-08-23)

## Why this matters

This upstream repository contains the **retuned 7-point** and **final 9-point**
certificates used by the Shi two-certificate / multi-certificate LP:

- retuned 7pt: `p=1/2736`, target `891/200000`
- final 9pt: `p=1/2500`, target `15211/2500000`

These are the strong operating points that dominate our canonical k=9
certificates in the multi-certificate LP.

## Key upstream findings

1. **Nine-point family is near-exhausted.**
   - The best final nine-point assembly is about:
     `0.673312742272245998143847403168…`
   - The family is said to be within about `2·10⁻⁶` of exhausted.
   - Horizon ceilings: ≈ `0.67331` (R=6), ≈ `0.67340` (R=8).

2. **Pure pair-energy methods cap at ≈ `0.674826`.**
   - Exact balanced configurations limit any certificate that only reads pair
     energies of simple zeros.

3. **Bandwidth λ > 1 cannot be opened by unconditional sieve bounds.**
   - Signed off-diagonal structure defeats absolute majorization by at least
     factor ≈ 6.1 against the formal gain.
   - Needed future threshold: a direct form-factor cap `C < 17.8373866` or
     Hardy–Littlewood-strength input at `λ > 1.00985`.
   - This is directly relevant to the preserved **Kuznetsov bandwidth** backlog:
     it explains why λ > 1 is a hard frontier, not a formula substitution.

4. **The gate to 0.675+ is the off-line pair bridge.**
   - A single open lemma on multi-pair composition of off-line hyperbolic pairs.
   - If proved with measured constants, the assembled bound lands in
     `0.674–0.675`.

## Implication for our roadmap

- Continuing **canonical k-point pressure certificates** still has some room,
  but the upstream analysis indicates the family is close to exhausted
  (≈0.6734).
- **Retuned q=9 / k=10 search** could still be attempted, but expected
  headroom is small unless it finds a strong retuned operating point.
- The higher-value long-term route is the **off-line pair bridge**, with a
  potential payoff into the `0.674–0.675` range.
- **Kuznetsov bandwidth** remains backlog; the upstream analysis gives strong
  quantitative reasons for why it is hard.

## Artifacts preserved

- Full upstream source: `literature/raw/zeta-simple-zeros-673137/`
- Its `README.md`, `docs/nine-point.md`, `docs/campaign-2.md`,
  `data/candidate-*.json`, `certificates/*.txt`, and `src/zeta_ext/` are all
  included.
