# Status & literature — kernel-limit lemma (T1c item 3)

Run: `R-20260816T040000Z-kernellimit-b9e1`
Status line: `RIGOROUS_PARTIAL_RESULT`

## Status

The kernel-limit lemma is **derived and proved at analysis level** in this run:

- Exact statement pinned to the snapshot's Gram definition (`Defs.lean` Gsummand/Gentry)
  and the MT window (`BridgeD`/`ParamsD`/`Functional`).
- Proof: uniform `O(w/L)` rate to `K_λ(x)`, ratio normalization, `kMT = K_1/K_1(0)`.
- Numerical cross-check at x∈{0.3,1.0,1.9}, L∈{100,1000,10000}, both with and without the
  ramp; the ramp case confirms `O(w/L)` decay.
- Not reached: Lean machine formalization / `lake build` acceptance of the §3 statement.
  The snapshot's Zeta23 files are the *source* (read + hash-pinned), not outputs of this run.

## Novelty / status risks

- This is a **verified analytical bridge**, not new mathematics: it re-derives the standard
  Fourier-transform-of-window overlap limit for the MT window. No novelty claim beyond:
  (a) exact Lean-ready statement, (b) explicit `O(w/L)` uniform rate, (c) the resolved
  normalization/Cfun ambiguity.
- Literature grounding: the MT kernel and the `⟨v_γ,v_γ′⟩ = k(x_γ−x_γ′)+o(1)` statement
  appear in OpenAI `zeta-simple-zeros/docs/proof.md` §1 and are sourced from the MT
  construction in the cited paper (Montgomery–Taylor). Chain9.lean (`CERTIFIED_F8_GE`)
  records that the high-T limit is an OPEN analytic-bridge sub-obligation; this run closes
  the *statement-level* analytic bridge and proves it.

## Known / adjacent results

- `Proof.md` §1: `k(x)=K(x)/K(0)`, `K(x)=∫_{−1/2}^{1/2}cos(√2t)cos(2πxt)dt`, the exact
  `sinc` forms, `K(0)=√2 sin(1/√2)`.
- Paper §7.1: optimal profile `v_λ*(s)=cos(√2λs)`, `c_λ*`, window
  `φ(u)=√cos(√2u/l)·ϱ`, and the `g=φ²⋆φ²`/`J` moment machinery. The `kMT` kernel is the
  Fourier transform of `v*` evaluated on the normalized beat frequency `2πx`.
- XiPrime transfer block (`XiPrime/Window.lean` `vConv`) formalizes the *autocorrelation*
  `g(y)≈L·vConv(v,y/L)` used for the moments; it is the same autocorrelation family as
  `Cfun`, and is distinct from the Fourier overlap used here.
