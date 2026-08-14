# Status and Literature

Run: `R-20260814T041219Z-mainpush-3cdc81`. Compiled 2026-08-14.

## Exact known results (as of 2026-08-14) — with locators

### Unconditional (ζ), dyadic
| Constant | Statement | Source / locator |
|---|---|---|
| > 0 | positive proportion on the line | Selberg 1942 [as cited in Claude v2 §1.3] |
| ≥ 1/3 | simple on line | Levinson 1974; Heath-Brown 1979 (simplicity) |
| > 2/5 | on line | Conrey 1989 |
| 5/12 ≈ 0.4167 | N0^s/N, N0/N (previous records) | Pratt–Robles–Zaharescu–Zeindler, "More than five-twelfths of the zeros of ζ are on the critical line", Res. Math. Sci. 7 (2020) (https://link.springer.com/article/10.1007/s40687-019-0199-8) |
| 0.6603 | Nd/N previous record | Wu, "Distinct zeros of the Riemann zeta-function", Q. J. Math. 66 (2015) (https://zbmath.org/1320.11082) |
| **2/3** | N0*/N, N0^s/N ≥ 2/3−o(1); Nd/N ≥ 5/6−o(1) | Claude/Anthropic 2026; Lean-verified (Zeta23.Unconditional.thm*, ThmD) |
| **0.6725007036794116** = 3/2 − (1/√2)·cot(1/√2) | N0*/N, N0^s/N ≥ 2 − 1/c1*, c1*=0.753296… (Montgomery–Taylor window) | Claude Thm D; Lean `Zeta23.ThmD.thmD₀_simple_mult` |
| **0.83625…** = (3 − 1/c1*)/2 | Nd/N | Claude Thm D; Lean `Zeta23.ThmD.thmD₀_dist_mult` |
| **0.6730085279277797613…** (DRAFT) | N0^s/N ≥ (1,345,000·H_MT − 2,680)/1,340,003 | OpenAI/GPT-5.6 draft (ainta/zeta-simple-zeros). **THIS RUN: independently verified** (certificates byte-match; reduction chain audited). |
| ≤ 0.6818287… | ceiling of all bandwidth-one certificates (2 trace moments, Fourier support ⊂ [−1,1], on/off partition) | Claude §7.2 + Lean `Zeta23.PairCeiling.CeilingLaw256` |
| ≈ 0.673058 | ceiling of the OpenAI 7-point "stability-refinement" certificate class (this run, O3) | THIS RUN — novel. Does not escape 0.6818287. |

### Conditional
| Constant | Hypothesis | Source |
|---|---|---|
| 2/3 simple; 5/6 distinct | RH | Montgomery 1973; Conrey–Ghosh–Gonek 1998 (1.2); Montgomery–Taylor 1975 |
| 0.6792 simple | RH (SDP form-factor positivity) | Chirre–Gonçalves–de Laat, "Pair correlation estimates for the zeros of the zeta function via semidefinite programming", Adv. Math. 361 (2020) 106926 (arXiv:1810.08843). Resolved as CGdL20. |
| 19/27 ≈ 0.7037 simple | RH | Bui–Heath-Brown 2013 (BHB13) |
| ≥ 0.85082 Nd/N | RH + cubic weight | Claude §7.3 (with BHB13) |
| **100% simple on line** (⇒ N0/N → 1) | **PCC full / ES** | Goldston–Lee–Schettler–Suriajaya, "Pair correlation conjecture for the zeros of ζ, I: simple and critical zeros", arXiv:2503.15449 (GLSS25); see also GS25 Thm 2. **This run verified the reduction chain.** |
| ≥ 13/18 ≈ 0.7222 N0^s/N | HL*(4) (4 trace moments) | Claude §7.2(f), informal |
| 100% N0^s/N | HL*(k0) for all k0 | Claude §7.2(f), informal |

## Novelty line (B0 + this run)
- `lim N0/N = 1` is OPEN.
- Any unconditional c > 0.6730085279 is novel. This run did NOT exceed it; it *verified* the
  OpenAI draft value and characterized the certificate class ceiling.
- The OpenAI draft value, now verified, is the current unconditional record for N0^s/N and N0*/N
  (it strictly improves the Lean-verified Thm D 0.6725…).

## References resolved / open
Resolved: CGdL20 (=arXiv:1810.08843), PRZZ20, Wu15, BHB13, GLSS25 (arXiv:2503.15449),
GS25 (arXiv:2511.20059), Montgomery 1973/1975, MV74.
CCLM17: referenced in Claude v2 §7.1 as "[CCLM17, Corollary 14]" (Montgomery–Taylor kernel solves
the one-delta extremal problem given F on [−1,1]). This identifier could NOT be resolved to an
exact bibliographic entry from available sources in this run. It is a traceability gap, not a
theorem input: the OpenAI draft depends on Theorem D (Lean-verified), not on CCLM17.
