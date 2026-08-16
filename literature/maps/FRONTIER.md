# FRONTIER — 临界线上零点比例 (Proportion of zeros on the critical line)

Project: MRP-20260814-riemann-critical-line-c13b8d
Frontier refreshed: 2026-08-14 (UTC). All statements below are exact claims from the cited
sources; where a source is a preprint/draft this is stated. Locator format: `query -> result -> locator`.

## 0. B0 novelty preflight (stage gate)

- **Openness verdict (checked 2026-08-14)**: the statement
  `lim_{T→∞} N0(T)/N(T) = 1` ("almost all nontrivial zeros of ζ lie on the critical line",
  "probability 1") is **OPEN**. Even the weaker `liminf N0^s(T,2T)/N(T,2T) ≥ 2/3` was first
  proved in Aug 2026 (Anthropic/Claude). No known unconditional result reaches 0.69;
  the bandwidth-one certificate class is capped at ≈ 0.6819. Any unconditional constant
  strictly above **0.6730085279...** (OpenAI/GPT-5.6 draft, itself unverified) is new.
- **Audit path**: divergent search 2026-08-14 (queries logged in §1); deep-read of the
  Anthropic paper v1+v2, the Anthropic expert note, the OpenAI/GPT-5.6 draft (riemann.pdf +
  verifier source), Goldston–Suriajaya arXiv:2511.20059, and the Lean artifacts
  (anthropics/zeta-23-lean). Crank literature (zenodo "RH proofs") identified and excluded.
- **Snapshot hash**: knowledge base is freshly initialized; snapshot hash to be recorded in
  the task packet at dispatch time (empty KB ⇒ no retrieval dependencies).

## 1. Search log (2026-08-14)

| Query | Result | Locator |
|---|---|---|
| `Anthropic Claude paper Riemann hypothesis 2025 arXiv` | Anthropic blog "Learning more about Claude's mathematical capabilities" (2026-08-10, updated 08-13): 41.6% → 67.2% | https://www.anthropic.com/research/riemann-zeta |
| same | PDFs (paper, informal note, appendix, E2 transcript) | https://www-cdn.anthropic.com/95c24693…pdf (v1), 564f962e…pdf (v2), 23455459…pdf, d7f3ecf1…pdf, 8a0d1add…pdf |
| `arXiv Anthropic Claude proportion zeros critical line 2025` | Lean formalization repo | https://github.com/anthropics/zeta-23-lean |
| `OpenAI research paper Riemann hypothesis zeros critical line 2025` | no OpenAI RH paper found in any result; only Claude coverage | https://dev.to/hiroki-ii-ai/ai-daily-digest-august-14-2026-… (OpenAI items are unrelated) |
| `site:openai.com OR site:arxiv.org OpenAI o3 GPT-5 Riemann hypothesis` | no OpenAI RH work surfaced | — |
| `Claude Riemann zeta zeros critical line github` | **ainta/zeta-simple-zeros**: "A 67.30085% lower bound for simple zeros" — GPT-5.6 Sol draft, extends Anthropic Theorem D | https://github.com/ainta/zeta-simple-zeros (HEAD 040c5e899e658aed7b56a2a87f501798fe10761d) |
| `Goldston Suriajaya 2025 arXiv two thirds simple zeros` | Goldston–Suriajaya, "Zeta Zeros on the Critical Line" (Nov 2025) | https://arxiv.org/abs/2511.20059 |
| `arXiv 1902.05473` | Aryan, "On an extension of the Landau–Gonek formula" | https://arxiv.org/abs/1902.05473 |
| `arXiv 2306.04799` | Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh (pair correlation, no RH) | https://arxiv.org/abs/2306.04799 |
| `arXiv 2501.14545` | BGSTB, "Pair Correlation … I: Proportions of Simple Zeros and Critical Zeros" | https://arxiv.org/abs/2501.14545 |
| `arXiv 2503.15449` | Goldston–Lee–…, "Pair Correlation Conjecture … I: Simple and Critical Zeros" (PCC ⇒ 100% simple on line) | https://arxiv.org/abs/2503.15449 |
| `pair correlation conjecture full support 100% simple zeros` | GLSS25 confirmed | https://www.semanticscholar.org/paper/…Goldston-Lee/… |

## 2. Exact known results (as of 2026-08-14)

Notation: N(T1,T2) zeros counted with multiplicity; N0 = on-line with multiplicity;
N0* = distinct on-line; N0^s = simple on-line; Nd = distinct. Dyadic interval (T,2T].

### Unconditional (ζ)
| Constant | Statement | Source |
|---|---|---|
| > 0 (Selberg) | positive proportion on the line | Selberg 1942 [as cited in Claude v2 §1.3] |
| ≥ 1/3 (Levinson) | simple on line | Levinson 1974 [HB79 for simplicity; as cited] |
| > 2/5 (Conrey) | on line | Conrey 1989 [as cited] |
| 5/12 ≈ 0.4167 | N0^s/N previous record | BCY11, Fen12, PRZZ20 [as cited in Claude v2] |
| 0.6603 | Nd/N previous record | Wu 2015 [as cited] |
| **2/3** | **N0*/N, N0^s/N ≥ 2/3 − o(1); Nd/N ≥ 5/6 − o(1)** | **Claude/Anthropic 2026-08 (v1/v2); Lean-verified (theorems A–E)** |
| **0.672500703679… = 3/2 − (1/√2)cot(1/√2)** | N0*/N, N0^s/N ≥ 2 − 1/c1, c1 = 0.75329… (Montgomery–Taylor window; optimal in its class [CCLM17, Cor. 14]) | Claude/Anthropic Thm D; expert note |
| 0.83625… | Nd/N ≥ (3 − 1/c1)/2 | Claude Thm D |
| **0.6730085279277…** | **N0^s/N ≥ (1,345,000·H_MT − 2,680)/1,340,003 via stability refinement (3-pt 0.672519767, 7-pt 0.673008528)** | **ainta/zeta-simple-zeros (GPT-5.6 Sol). INDEPENDENTLY AUDITED 2026-08-14: two independent re-derivations PASS (audit reports sha256 5F0EDEAA…, 3F554804…), Arb certificates byte-identical (nodes 707901, hashes a9992300/7913c55), manager 50-dp check (reports/independent-arith-checks.md). SUPERSEDED as world record by C₉ = 0.6730536 (extpress run). Residual: paper-level (not Lean end-to-end); Lemma 3.1 rests on [1] Lemma 5.4** |
| **0.6730536459526…** | **N0^s/N ≥ (6875·H_MT − 1315/96)/6849 — NEW RECORD via k=9 pressure certificate (F₈ ≥ 39/10000, 8-var Arb certificate, 53M nodes)** | **This project (extpress run R-20260814T045000Z-extpress-2f36ae, 2026-08-14); manager-level audit PASS with scope limits (SUPERSEDED as world record 2026-08-15 by the certified C₉ = 0.6730665 at f₉ = 0.00392, which also realizes the F₈ ≥ 0.00392 ⟹ F₈ ≥ 0.0039 subsumption of the grid-4000 re-run); third-party re-audit recommended** |
| ~~0.6730855621335… (PENDING CERTIFICATE)~~ | ~~would-be record at f₉ = 0.00395~~ — **WITHDRAWN 2026-08-15: the 0.00395 certification FAILED (both grid-2000 and grid-4000): the true minimum of F₈ is ≈ 0.00395005 (configuration [1.0465,1.996,1.9995,1.9995,1.9865,1.04525,1.97575,1.04525], value 0.003950049001339790, exact-kernel verified), margin ≈ 5e-8 vs verifier bound-loss ≈ 1e-5 — 0.00395 infeasible (f9-ladder.md CORRECTION)** | this project, runs/…/f9push-d3b58c/f9-ladder.md |

| 0.85838 / 0.92919; 0.86864 / 0.93432 | zeros of ξ′: simple on line / distinct (flat / quartic window) | Claude Thm (Remark 7.1); Lean-verified |
| **0.8678888652** | ξ′ MT-window baseline H_{ξ′}^{MT} = 2 − κ₁(1, cos(√2·)) (new constant, A2-verified two ways) | this project, reports/xi-prime-pressure-method.md |
| **0.86918353505… (AUDITED CANDIDATE)** | ξ′ pressure method: (6875·H_{ξ′}^{MT} − 1315/96)/6849 — exceeds quartic 0.86864; audits A1–A6 CLOSED manager-level PASS (reports/xi-prime-audit-manager.md); AdmWindow cos blueprint complete (reports/admwindow-cos-instance.md) | this project, reports/xi-prime-cor22-derivation.md; 0.00392 version (0.8692001…) pending its certificate |
| ~~0.8692247262342… (PENDING CERTIFICATE)~~ | ~~ξ′ linked record at f₉ = 0.00395~~ — **WITHDRAWN with the ζ 0.00395 row (certification failed; see above)** | this project, reports/linked-ladder.md + f9push run |
| **0.8692000910966…** | **ξ′ linked record at f₉ = 0.00392: (657,500·H_{ξ′}^{MT} − 1,310)/655,001 — CERTIFIED 2026-08-15 (same certificate as the ζ row above; window-determined kernel, A6 PASS)** | this project, reports/linked-ladder.md + f9push run |
| ≤ 0.6818287… | **ceiling** of all bandwidth-one certificates (first two trace moments w/ Fourier support ⊂ [−1,1] + on/off partition) | Claude §7.2 + Lean `Zeta23.PairCeiling.ceiling_law256` |

### Conditional (RH or conjectures)
| Constant | Hypothesis | Source |
|---|---|---|
| 2/3 simple; 5/6 distinct | RH | Montgomery 1973; CGG98 (1.2); Montgomery–Taylor 1975 |
| 0.6792 simple | RH (SDP, form-factor positivity outside [−1,1]) | CGdL20 |
| 19/27 ≈ 0.7037 simple | RH | BHB13 |
| ≥ 0.85082 Nd/N | RH + cubic weight | Claude §7.3 (with BHB13) |
| **100% simple on line** | **Pair correlation conjecture, full support** | GLSS25 (arXiv:2503.15449) |
| ≥ 13/18 ≈ 0.7222 (N0^s/N) | HL*(4) (4 trace moments = sine-kernel Gram moments) | Claude §7.2(f), informal |
| **100% (N0^s/N → 1)** | **HL*(k0) for all k0** | Claude §7.2(f), informal — to be made rigorous (our task Q3) |
| **SL update 2026-08-15 (run R-20260815T120000Z-sllemma-7b21e4, RIGOROUS_PARTIAL_RESULT, audit PASS-CONDITIONAL)**: SL's load-bearing form for the condp1 theorem is EXACTLY μ_λ({0}) = 0 (no atom at 0; "0 ∈ supp" not needed — sharpening). SL ⟺ lim_m det(H_m)/det(H_m⁽⁰⁰⁾) = 0 over the sine-Gram moment sequence (Hankel criterion; Λ₁(0)=1/4, Λ₂(0)=5/36 EXACT from (1,4/3,2,13/4)). SL itself OPEN; crux = exact moments m_k, k≥5 (D_k = 0 ∀k≥3 conjecture = closure route). | this project |
| **SL moment-route update 2026-08-15/16 (run R-20260815T130000Z-slmoments-a3f9, NUMERICAL_EVIDENCE / RIGOROUS_PARTIAL_RESULT)**: FAITHFUL projection-DPP sampler validated on TWO gates (exact-joint + exact moments; occupancy kernel A=h·sinc is the correct discretization — the naive diag-1 kernel fails with E[N]=27.5). First trustworthy fermionic/Wick evidence through k=6: D₃=−0.0009±0.0025, D₄=+0.0000±0.0010, D₅=−0.00008±0.00038 (MC), D₆=+0.0005±0.0004; exact-structure Gauss integrals corroborate D₅≈−1e-4, D₆≈−1e-5 (4 orders below m₅≈5.5, m₆≈9.8). Hankel decay evidence Λ₁=0.245, Λ₂=0.133, Λ₃=0.092. Closing-lemma framework: M (D_k=0 exact) → P (size≤2 matching-sum) → H (Hankel ratio→0) → SL; gaps G1/G2/G3 itemized. SL NOT closed (evidence only). | this project |
| **SL G1 update 2026-08-16 (run R-20260816T030000Z-slG1-9c2a, FINITE_COMPUTATIONAL_RESULT / RIGOROUS_PARTIAL_RESULT)**: D₃ = D₄ = D₅ = 0 upgraded to a REPRODUCIBLE COMPUTER-VERIFIED EXACT identity: each signed summand I_π = rational box-spline volume (Fourier/coarea reduction, rigorous); two independent implementations agree to ~1e-13; rationals (denominators ≤ 180) certified (residual ≤8e-15 vs tolerance ~1.5e-5); signed sums vanish EXACTLY for k=3,4,5; per-cycle-type subtotals nonzero ⇒ cancellation genuinely global (Wick/fermionic). Lemma M's exact formal target stated (box-spline signed-sum identity over S_k); general-k proof OPEN. Literature: no theorem states D_k=0; Soshnikov + quasi-free/CAR + Giambelli give the pairing-only shell; DPP cumulants do NOT generally vanish (Johansson–Lambert) ⇒ genuine special cancellation. | this project |
| **SL G2 update 2026-08-16 (run R-20260816T070000Z-g2rule-a1b2, RIGOROUS_PARTIAL_RESULT; proof attempt R-20260816T080000Z-g2proof-a24d, RIGOROUS_PARTIAL_RESULT)**: GENERAL vanishing rule FOUND and VERIFIED 100% on all 275 exact per-partition values (k=3..6): J_σ=0 ⟺ H_σ (cycle-crossing multigraph on blocks) disconnected OR m ≤ 2b−3; nonvanishing ⟺ connected AND m ≥ 2b−2. Resolves the k=5 vs k=6 tension. General-k proof attempt: M1 CLOSED (H_σ always connected, disconnected branch vacuous); b=2 family CLOSED (J=c_m−c_{m+2}>0); killed routes recorded (multiplicative/class-function EGF, naive degree-2 contraction); M2 (low-surplus signed box-spline sum telescopes to 0) remains the exact open core; k=7 new-isoclass verification started but not completed in budget. | this project |

### Known barriers (exact)
1. Bandwidth-one certificate ceiling ≈ 0.6818 (Lean-certified; the extremal 256-periodic law is
   moment-indistinguishable from the true configuration up to 3·10^-40 row enclosures).
2. Higher trace moments tr G̃^k, k ≥ 2: prime-side evaluation at X ≍ T requires X^k ≤ T^(2−ε),
   i.e. only k = 1 unconditionally (§7.2(e)); k ≥ 2 needs Hardy–Littlewood-type additive prime
   correlations.
3. "Given only tr G̃, ‖G̃‖²_HS and the block structure, the inequality (1.1) is sharp" (§1.4, §7.2(b)):
   the extremal configuration (2/3 simple on-line + 1/6 on-line doubles) matches the indicator
   window's moments.
4. The OpenAI refinement escapes (1) because it uses gap-dependent inner products (not just the
   two moments); its class ceiling computed at ≈ 0.6730583 (formal m→∞ limit; rigorous
   ≤ 0.6730085 at m ≤ 269) — still below the bandwidth-one ceiling (mainpush R3).
   k=9 formal class limits (re-verified mpmath 30d, 2026-08-15): at f₉ = 0.0039 →
   0.67312589466862…; at f₉ = 0.00392 → 0.67313941016727…; at f₉ = 0.00395 → 0.67315968443292…;
   at the certified true min ≈ 0.00395005 → 0.67315971822438… (2026-08-15 correction: the
   previous "true min 0.0039818" was a local minimum; the verified lower configuration
   (0.003950049) shifts the relevant class limit). All formal (uncontrolled large-m
   spectral monotonicity), not rigor statements on their own.
5. 100% unconditionally is out of reach of the rank–trace mechanism: §7.2(f), "RH itself is out of
   reach of the mechanism".
6. The informal moment values m_k(1) = 1, 3/4, 2, 13/4 are NOT a positive-measure moment sequence
   (det M₂ = −1/4 < 0; verified in reports/independent-arith-checks.md): §7.2(f) needs the
   paper's exact (signed-measure) operator convention — condp1 run pins this down.

## 3. Novelty-risk line

Any claim of liminf ≥ c for c > 0.673008528 (now independently audited) must be checked against
(a) the bandwidth-one ceiling (if the certificate stays in class (a)), (b) the stability-refinement
class ceiling ≈ 0.6730583 (computed, m ≤ 269 rigorous), (c) possible simultaneous work by human
number theorists in Aug 2026 (watch arXiv after 2026-08-13). Any claim
of "probability 1" (liminf = 1) is extraordinary; it must either prove new deep input (pair
correlation beyond support 1, or HL-type moments) or it is a crank claim (see ignored zenodo/arXiv
"RH proofs" list in literature/search-log).

## 4. Ignored / excluded (crank noise, recorded for provenance)

zenodo records 16890518, 15589364, 15572590, 14787713; academia.edu OOL-KND-RH; arXiv
2509.16240, 2509.10588 (dynamical reformulations, no theorem-level progress on the proportion);
generic news aggregators without theorem statements. Reason: no exact statements with verifiable
proof obligations; several self-published "complete resolutions" of RH.
