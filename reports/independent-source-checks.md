# Independent source-level checks (manager, 2026-08-14)

## R2 reduction: "PCC ⇒ N0/N → 1" — verified against primary sources

Sources read directly: `literature/raw/gs-2511.20059.txt` (Goldston–Suriajaya 2025,
arXiv:2511.20059) and the GLSS25 statement quoted there.

1. **GS25 Theorem 2** (lines 198–207): if 1 ≤ C < 2 and, as T → ∞,
   Σ_{ρ,ρ′∈Z(T), γ=γ′} 1 ≤ (C + o(1))·(T/2π)·log T, then the proportion of simple zeros is ≥ 2−C
   and the proportion of zeros on the critical line is ≥ 2−C. With C = 1: **100% simple AND 100%
   critical** (hence liminf N0(T)/N(T) ≥ 1, i.e. N0/N → 1). The diagonal sum counts ordered pairs
   with multiplicity (m_γ² for a zero of multiplicity m_γ) and includes symmetric-diagonal terms
   (5.1): diagonal m_ρ + symmetric-diagonal Σ_{β≠1/2} m_ρ + non-symmetric horizontal terms.
2. **ES ⇒ C = 1**: GS25 line 491: "(8.3) implies C = 1, thus Theorems 2 and 3 follow from ES."
3. **PCC ⇒ ES without RH**: GS25 lines 475–492, attributed to [GLSS25a] (arXiv:2503.15449):
   "we show the results on PCC hold without RH. As a consequence, by Theorem 2, …".
4. **GLSS25 Theorem 5** (lines 479–480): "The Pair Correlation Conjecture implies asymptotically
   100% of the zeros of the ζ(s) are simple and on the critical line."

**Verdict**: mainpush R2 ("PCC in Essential-Simplicity form, equivalently full-support PCC,
implies lim N0(T)/N(T) = 1 and N0^s/N → 1") is consistent with the primary sources, including the
"C = 1" arithmetic (2 − C = 1) and the multiplicity conventions. The remaining audit burden: the
exact definition of ES (8.3) in GLSS25 and the proof that PCC ⇒ ES without RH — these live in
arXiv:2503.15449, which the audit agent must verify against the actual paper.

## Lean-snapshot statement check (manager, 2026-08-14)

condp1's claim: the Lean theorem `thmD₀_simple` (comparator form) states N₀ˢ ≥ (2c₁*−1)N with
2c₁*−1 = 0.50659 (Cauchy–Schwarz constant), while the paper's rank–trace constant
2 − 1/c₁* = 0.67250 lives in the multiplicity forms. Verified against the snapshot:

- `Zeta23/ThmD/Final.lean` L11/L119: `thmD₀_simple : ∀ε>0, ∃T₀, ∀T≥T₀, (2*c₁* − 1 − ε)·N(T,2T) ≤ N₀ˢ(T,2T)` ✓ (CS form, 0.50659).
- Same file L15–18: the fixed-λ constants are HD λ = 2 − 1/c*(λ), 2c*(λ) − 1, c*(λ) — "Numerically 0.67250…, 0.50659…, 0.75329…".
- `comparator/ChallengeDeps.lean` L113: "Theorem D's three proportions are 2 − 1/c₁* = 0.67250…, 2c₁* − 1 = 0.50659… and …".
- `comparator/Solution/Multiplicity.lean` L40: `two_thirds_simple_on_critical_line` imports `Zeta23.ThmD.thmD₀_simple_mult` (the multiplicity form carrying the 0.67250 rank–trace constant, per the oaidraft audit lines 435/441 + HD_one).

Verdict: condp1's statement-fidelity note is CORRECT; both constants are part of Theorem D's
Lean statement set, with the simple (non-multiplicity) comparator form being the weaker CS bound.

## Numerical corroboration datum (evidence only)

GS25 intro (line 30): "By large scale computation with careful error analysis, there are exactly
12,363,153,437,138 zeros and all of them are on the critical line and are simple."
→ Finite computational evidence: 100% simple-and-on-line up to that height (~1.2×10^13 zeros).
Evidence only; never a proof of the asymptotic proportion.

## Cross-check with Theorem 1 (Montgomery, RH)

GS25 Theorem 1: assuming RH, ≥ 2/3 of zeros simple (counted appropriately); with RH the critical
proportion is 1 trivially. The user's "probability 1" target under RH is exactly Montgomery's
framework; the 2026 unconditional results (2/3, 0.6725, 0.6730085) are the RH-free analogues.
