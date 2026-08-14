# Riemann Conjecture: Critical-Line Zero Proportion

- **Project ID:** `MRP-20260814-riemann-critical-line-c13b8d`
- **Created:** 2026-08-14T04:03:56Z
- **Lifecycle state:** `ACTIVE` (stage B research)
- **Upstream solver:** `$rigorous-open-math-research`

## Program scope

Push the unconditional lower bounds for the proportion of nontrivial zeros of the Riemann zeta
function on the critical line toward 1 (the user's "probability 1" goal), building on the
2026-08 methods of Anthropic/Claude (rank–trace + Sylvester inertia; 2/3 simple on line,
0.67250 with Montgomery–Taylor window, Lean-verified) and the OpenAI/GPT-5.6 Sol stability
refinement (0.6730085 draft). Included: ζ and primitive Dirichlet L-functions; simple/distinct/
with-multiplicity on-line counts; zeros of ξ′ as a secondary family; conditional theorems
(PCC / HL*) quantifying "probability 1". Excluded: crank "complete RH proofs"; unconditional
RH itself (out of scope of any known mechanism).

## Research objectives

1. Independently verify the OpenAI/GPT-5.6 draft constant 0.6730085279... (adversarial audit).
2. Improve unconditional constants beyond 0.6730085 if possible; compute the real ceiling of
   the stability-refinement certificate class.
3. Prove rigorous conditional "probability 1" theorems (HL* all orders ⇒ 100%; PCC full support
   ⇒ 100%, cf. GLSS25) with exact hypotheses.
4. Deliver an exact obstruction report for unconditional probability 1.
5. Formalize any qualified result in Lean (baseline: anthropics/zeta-23-lean snapshot).

## Literature scope and cutoff

Databases: arXiv, Anthropic research page/GitHub, GitHub (OpenAI draft), web news for 2026-08
AI-math events. Cutoff: 2026-08-14. Papers registered: 7 (index/papers.json), hashed locally
in literature/raw/. B0 audit trail: literature/maps/FRONTIER.md.

## Problem portfolio

- O-2026-criticalline-proportion: liminf N0^s(T,2T)/N(T,2T), N0*/N, Nd/N — records: 2/3,
  0.6725007, 0.673008528 (draft), ceiling 0.6818287 (bandwidth-one), OPEN for ≥0.69 and for →1.

## Knowledge assets

- Sources: literature/raw/ (Anthropic PDFs v1/v2/note/appendix/transcript + text; Lean snapshot
  zeta-23-lean@3635e748; OpenAI draft zeta-simple-zeros@040c5e8; GS 2511.20059).
- Run artifacts: runs/rigorous-open-math-research/R-20260814T041219Z-{mainpush,oaidraft,condp1}*
  (standard upstream artifact names, hashed in index/artifacts.json).
- Knowledge base: freshly initialized (empty); no accepted-knowledge dependencies.

## Research budget

Configured effective-time target: `unset`.

## Current entry point

Read `state/RESUME.md` and `state/current.json` before continuing.
