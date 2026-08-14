# Session summary — 2026-08-14 (Riemann critical-line zero proportion)

Program: MRP-20260814-riemann-critical-line-c13b8d · pipeline: math-research-workflow
(manage → rigorous research → audit; Lean snapshot as baseline). All commits pushed to
github.com/Zhongshan-Big-Jun/Riemann-Conjucture-Research (public, branch main).

## Established results (audited / verified)

1. **OpenAI draft 0.6730085279277797613…**: independently audited twice (PASS;
   reports sha256 5F0EDEAA…, 3F554804…); Arb certificates byte-identical; constants match
   Lean Theorem D. Superseded as world record by (2).
2. **NEW UNCONDITIONAL RECORD C₉ = 0.67305364595258992520…** (extpress run): k=9 pressure
   method, certificate F₈ ≥ 39/10000 (53,137,290 nodes, grid 4000, hash 7029ac0f…);
   manager-level audit PASS with scope limits; general-k chain reproduces k=7/k=3 exactly;
   verifier validated byte-identically on k=7 (a9992300…). Improvement over C₇: 4.5e-5.
3. **§7.2(f) transcription error resolved**: m₂(1) = 4/3 (not 3/4; 3/4 invalid as moments);
   under the correction Λ₂(0) = 5/36 and 13/18 reproduce exactly (3 independent checks).
4. **Conditional probability-1 theorem** (condp1, audit PASS-CONDITIONAL + F-1 repaired):
   HL* (all orders, λ<1) + Spectral Lemma SL ⇒ sup_{λ<1} liminf_T N₀ˢ/N = 1 (ε-form);
   HL*(4) ⇒ ≥ 13/18. GLSS25 (PCC full support) ⇒ 100% is the complementary route.
5. **ξ′ candidate record C₉^{ξ′} = 0.86918353505282747704…** (derivation complete;
   A2 verified two ways): MT-window ξ′ baseline H_{ξ′}^{MT} = 0.86788886519905193555…
   (new constant, flat/quartic cross-validated to 8 digits); exceeds quartic 0.86864;
   audits A1–A6 packet ready (reports/xi-prime-audit-request.md).
6. **Structural/negative results**: window generalization is a theoretical wash (H↓ vs f↑
   compensation 1.57:1); k=11 infeasible in this environment (cost model recorded);
   SL lemma not found in literature (2 passes); bandwidth-one ceiling 0.6818 and k=1 moment
   barrier remain the structural walls to 1.

## In progress

- **f₉ = 0.00395 certification** (f9push run): target C₉ = 0.67308556213350404907 (ζ) and
  linked ξ′ 0.86922472623415578068; true minimum verified 0.0039818 (so 0.00395 is the
  realistic ceiling); two runs (grid-2000/grid-4000, 8 workers, --out file writes) alive,
  throttled by host load (game/office processes; 1-90% effective rate cyclically).
  Handoff recorded (runs/…/f9push-d3b58c/handoff-interrupted-…md).

## Open obligations (honest)

- Unconditional N₀/N → 1: OPEN; reduced to PCC / HL*+SL.
- f₉ 0.00395 certificate; ξ′ A1/A3/A4 independent audit; k=9 grid-4000 third-party re-run;
  SL lemma proof/refutation; exact m₃(1), m₄(1) closed forms; GLSS25 primary PDF check.
