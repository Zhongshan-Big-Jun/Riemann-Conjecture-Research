# Provenance

This document separates the original 67.313763% construction from the later
67.3200117% retuning. Floating-point exploration was used for discovery in
both stages; only the exact rational data and interval certificates are
load-bearing.

## Follow-up retuning to 67.3200117%

Starting from upstream commit `e0a2266` of
`trmdy/zeta-simple-zeros-673137`, a user-directed OpenAI Codex session on
2026-08-11 kept the seven-term window fixed and searched the pressure and
position-weight space. It found the exact design now in
`data/candidate-retuned-p2736.json`:

- pressure `1/2736`, target `891/200000`, and all six span capacities exactly
  2;
- block length 272 and tightened certified window baseline
  `3362285207/5000000000`;
- final Arb lower bound `0.6732001170127618568... > 1683/2500`.

The same session hardened the verifier's Arb-to-binary64 tail rounding,
exact removable-zero branches, enclosure intersection behavior, and exact
pressure cutoff arithmetic. The final grid-4000 certificate was replayed
after those changes and reproduced the same 2,168,370 search nodes and table
hashes. It also made explicit two proof-boundary details in the write-up: the
pressure-versus-bounded-span case split needed for uniform Gram asymptotics,
and the endpoint/leftover-block bookkeeping in shifted averaging.

Vivaswat Ojha initiated and directed this follow-up and submitted the research
draft. OpenAI Codex performed the numerical search,
implementation, certificate construction, verifier hardening, and much of the
initial drafting in a ChatGPT Work conversation. The upstream construction
and its contributors remain separately credited below. This follow-up is a
rigorously certified finite extension, not an end-to-end Lean theorem. This
record documents contribution provenance without presuming the project-level
citation or authorship arrangement for any merged or published version.

## Contemporaneous same-day candidates

After the exact design, full certificate replay, and initial draft were
complete, a public scan located two independent repositories reporting nearby
same-day candidates:

- `tawanerguo-cn/zeta-simple-zeros` reports
  `0.6731929114731422535...`;
- `npip99/zeta-zeros` reports `0.6731951989015205755...`.

The present value is numerically higher than the second by
`0.0000049181112412813...` in proportion.  Neither repository supplied code,
data, parameters, or proof ideas used by this retuning.  Their full
certificates were not independently replayed in this session, so this is a
chronology and numerical-comparison note, not a validity or priority finding.

## Original 67.313763% construction

This result was produced on 2026-08-11 in a single coordinated session:
Claude Fable (Anthropic) as orchestrator, dispatching specialized agents over
the Honeybee agent control plane, in response to Tormod Haugland's request to
improve the bound of `ainta/zeta-simple-zeros`.

## Lanes and what each contributed

| Agent | Model | Contribution |
| --- | --- | --- |
| zeta-audit | GPT-5.6 Sol (xhigh) | Independent soundness audit of the ainta stability argument: stability rank–trace lemma, Gram interface, pinching, bookkeeping — all SOUND; flagged a reproducibility hash drift from the unpinned dependency (fixed here by pinning). |
| zeta-design | GPT-5.6 Sol (ultra) | The sharp √-tail block profile with proof; the general position-weighted accounting and its exact final-bound formula; the ε(s,p) landscape; exhaustive zero-tuple enumeration used to validate/falsify candidate targets; the final rational design. |
| zeta-variational | Claude Fable | The kernel lever: perturbing the Montgomery–Taylor profile trades 2nd-order H-loss for 1st-order defect gain; produced the 7-term window family and the pressure retuning. Its original target (53/10000) was falsified by the design lane's enumeration and corrected to the certified design. |
| zeta-landscape | Grok | Independent float landscape of window-size/pressure minima; cross-validated the design lane's grids; characterized the lattice extremal configurations. |
| zeta-ideas2 | GPT-5.6 Sol (xhigh) | Structural analysis: identified the exact certificate-class ceiling p₂₅₆ = 0.68182868746… (marked {1,2} 256-periodic law in the Lean artifact); killed the c≠2, bootstrap, and nearest-neighbor routes; mapped the research-grade routes toward 0.675+. |
| orchestrator | Claude Fable | Problem decomposition; independent re-derivation of every load-bearing lemma; the generalized interval verifier (`src/zeta_ext/`), its correctness gate against the previous record's certificate, and the final certification runs; this write-up. |

(A Kimi K3 lane was planned but its credentials had expired.)

## Method notes

- Floating-point search was used only for discovery. Two lessons that shaped
  the final design: naive multistart minimization systematically
  *overestimates* the minima of these functionals (the true minimizers are
  lattice configurations with all pair sums near kernel zeros), and even
  curated enumeration can miss configurations — one candidate target was
  falsified this way. The interval certificates are the only decision
  procedure trusted here.
- The original verifier reproduces the then-previous record's certificate end-to-end
  (same node-level search, independent enclosure path) before certifying
  anything new.
- The imported analytic inputs are exactly those of the Anthropic paper and
  Lean artifact, as in `ainta/zeta-simple-zeros`.

## References

- Anthropic research article: https://www.anthropic.com/research/riemann-zeta
- Anthropic paper: https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf
- Lean 4 artifact: https://github.com/anthropics/zeta-23-lean
- Ainta record: https://github.com/ainta/zeta-simple-zeros
- Preceding 67.313763% repository: https://github.com/trmdy/zeta-simple-zeros-673137
- Same-day 67.319291% candidate: https://github.com/tawanerguo-cn/zeta-simple-zeros
- Same-day 67.319519% candidate: https://github.com/npip99/zeta-zeros
