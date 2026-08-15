# lean-proof — formalization project for the f₉ = 0.00392 records (Stage C)

Status: **INITIALIZED 2026-08-15 — baseline machine-build pending; chain/certificate
obligations OPEN.** Created to satisfy the Stage C handoff contract of
math-research-workflow (lean-verify skill not in the session catalog; manager-level
execution with the local Lean toolchain; full lean-verify dispatch is the intended
path once available).

## Machine evidence policy (from math-research-workflow)

FORMALLY_VERIFIED requires: `lake build` exit 0, zero sorry/admit/axiom hits, obligation
map complete, run-manifest.json + verification.json recorded. No machine evidence => no
FORMALLY_VERIFIED label. Numerical evidence is never a delivery.

## Obligation map (record theorem C₉ = 0.673066472675939665848… / C₉(ξ′) = 0.86920009109661916184…)

| Obl | Statement | Status | Where |
|---|---|---|---|
| O1 | Baseline: N₀ˢ(T,2T) ≥ (2 − 1/c₁*)·N(T,2T) − ε·N, 2 − 1/c₁* = 3/2 − cot(1/√2)/√2 (= H_MT, 0.67250…) — unconditional | ✅ FORMALIZED upstream | literature/raw/zeta-23-lean/Zeta23/ThmD/Mult.lean:435 `thmD₀_simple_mult` (snapshot @3635e748; local build pending) |
| O2 | General-k chain in ε-form (k=9, m=263, A₀ = 2499/2500): (1 − A₀/m)·N₀ˢ(T,2T) ≥ (H_MT − (m−1)/(500m) − ε)·N(T,2T) assuming certified F₈ ≥ 392/100000 | ❌ OPEN (T1) | target declaration `Zeta23.ThmD.chain9_eps` |
| O3 | Certificate: F₈ ≥ 392/100000 (finite Arb B&B, 64,748,524 nodes, grid-2000, 128-bit) | ❌ OPEN (T2; reflection route preferred — emit box data from verify_kpoint_parallel.py, Lean checker with exact rational arithmetic + native_decide) | target `Zeta23.Pressure.f8_cert` |
| O4 | Conclusion: liminf N₀ˢ/N ≥ (657,500·H_MT − 1,310)/655,001 (exact rational form; decimals are documentation) | ❌ OPEN (O2 + O3 ⇒ O4; arithmetic verified manager-level dps=130) | target `Zeta23.ThmD.record_c9` |
| O5 | ξ′ linked record: liminf N₀ˢ_{ξ′}/N_{ξ′} ≥ (657,500·H_{ξ′} − 1,310)/655,001 | ❌ OPEN (T3: import XiPrime.lean + O2; AdmWindow cos blueprint reports/admwindow-cos-instance.md) | target `Zeta23.XiPrime.record_c9xip` |
| O6 | Evidence discipline labels on all deliverables | ✅ documented (candidate_proof.md honest status) | — |

## Build plan (manager-level, this session where possible)

1. Toolchain: snapshot pins leanprover/lean4:v4.33.0-rc2 (local: 4.31.0) — elan auto-install
   on first lake call (background job).
2. `lake exe cache get` in literature/raw/zeta-23-lean (mathlib4 @ 51e6992e prebuilt cache).
3. `lake build Zeta23` → machine evidence for O1 (baseline), sorry/admit/axiom scan.
4. T1/T2/T3: formalizer dispatch (lean-verify skill) — not available in this session;
   contract recorded in reports/lean-formalization-contract.md.
5. On completion: run-manifest.json + verification.json + STATUS.md update + git sync.

## Gate status

validate_pipeline warns: "no lean manifest at lean-proof/run-manifest.json" — the manifest
will be written after the first machine build result.
