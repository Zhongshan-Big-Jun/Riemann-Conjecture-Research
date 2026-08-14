# Research directions

Project: MRP-20260814-riemann-critical-line-c13b8d

## D1 — Unconditional proportion of zeros on the critical line (primary)
Raise the unconditional lower bound for liminf N0^s(T,2T)/N(T,2T) (and N0*/N, Nd/N) toward 1.
Current: 2/3 (Claude 2026, Lean-verified), 0.6725007 (MT window), 0.6730085 (OpenAI draft, unverified);
bandwidth-one certificate ceiling 0.6818; unconditional higher moments blocked at k=1.
Rationale: the rank–trace + stability-refinement framework is fresh (Aug 2026) and demonstrably
extendable (gap-structure certificates escape the bandwidth-one ceiling).

## D2 — Conditional route to "probability 1"
Make rigorous and formalize the conditional statements: PCC full support ⇒ 100% simple on line
(GLSS25), and the HL* trace-moment route (Claude §7.2(f)): HL*(k0) for all k0 ⇒ N0^s/N → 1.
Rationale: converts the user's "probability 1" target into precisely quantified hypotheses;
gives an exact reduction (100% iff enough moment control), and produces formalizable
RIGOROUS_PARTIAL_RESULTs.

## D3 — ξ′ (derivative of completed zeta) direction
Unconditional 0.86864 simple-on-line for zeros of ξ′ (quartic window) vs 0.8825 under RH.
Window optimization is mechanical and Lean-supported (Zeta23/XiPrime/QuarticWindow).
Rationale: highest known unconditional proportion among these families; closest to its RH ceiling.

## D4 — Literature and tooling upkeep
Maintain FRONTIER/papers index; watch arXiv for post-2026-08-13 improvements (human or AI);
keep the Lean snapshot (zeta-23-lean) as the formalization baseline; verify the OpenAI draft
before promoting its constant.
