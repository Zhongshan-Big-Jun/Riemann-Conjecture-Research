# lean-proof — formalization project for the f₉ = 0.00392 records (Stage C)

Status: **O1 BASELINE MACHINE-VERIFIED 2026-08-15 — `lake build Zeta23` PASSED (exit 0,
9010 jobs); gold-standard `#print axioms` = {propext, Classical.choice, Quot.sound} on all
headline theorems (axioms-check.log); O2–O5 (chain/certificate/records) OPEN — T1
formalizer dispatched 2026-08-15 (subagent 5e03176d, working in lean-proof/Record9/).**
Created to satisfy the Stage C handoff contract of math-research-workflow (lean-verify
skill now in the session catalog; full lean-verify dispatch is the intended path).

## Machine evidence policy (from math-research-workflow)

FORMALLY_VERIFIED requires: `lake build` exit 0, zero sorry/admit/axiom hits, obligation
map complete, run-manifest.json + verification.json recorded. No machine evidence => no
FORMALLY_VERIFIED label. Numerical evidence is never a delivery.

## Obligation map (record theorem C₉ = 0.673066472675939665848… / C₉(ξ′) = 0.86920009109661916184…)

| Obl | Statement | Status | Where |
|---|---|---|---|
| O1 | Baseline: N₀ˢ(T,2T) ≥ (2 − 1/c₁*)·N(T,2T) − ε·N, 2 − 1/c₁* = 3/2 − cot(1/√2)/√2 (= H_MT, 0.67250…) — unconditional | ✅ FORMALIZED + MACHINE-VERIFIED (build exit 0, 9010 jobs; axioms {propext, Classical.choice, Quot.sound}; fidelity FAITHFUL) | literature/raw/zeta-23-lean/Zeta23/ThmD/Mult.lean:435 `thmD₀_simple_mult` (snapshot @3635e748; machine_check.log 2026-08-15) |
| O2 | General-k chain in ε-form (k=9, m=263, A₀ = 2499/2500): (1 − A₀/m)·N₀ˢ(T,2T) ≥ (H_MT − (m−1)/(500m) − ε)·N(T,2T) assuming certified F₈ ≥ 392/100000 | 🔶 MACHINE-ACCEPTED (T1 pass + REPAIR re-audit: `chain9_eps` compiles, `lake build Record9.Chain9` exit 0/8838 jobs, axioms gold standard; T1a/b/c/d FAITHFUL; wMT finding CLOSED; **T1c kernel-limit lemma CLOSED at machine level** (`Record9.KernelLimit`, lake build exit 0/8839 jobs); **T1c stability bridges machine-accepted** (`Record9.StabilityBridge`, lake build exit 0/8839 jobs; **Ψ-defect `psi_defect` now PROVED** — both spectral sub-steps closed; additive +Δ survival + averaged constants machine-checked; remaining open analytic sub-steps: T1c-2a block energy (T2 input), T1c-2c pinching, T1c-2d uniformity, full-O(S) Δ survival); open: those T1c sub-steps, T2) | lean-proof/Record9/Record9/{Chain9,KernelLimit,StabilityBridge}.lean |

| O4 | Conclusion: liminf N₀ˢ/N ≥ (657,500·H_MT − 1,310)/655,001 (exact rational form; decimals are documentation) | 🔶 MACHINE-ACCEPTED (`Zeta23.ThmD.record_c9` corollary of chain9_eps compiles; exact rational identities machine-checked; gated on T1c + T2 closure) | lean-proof/Record9/Record9/Chain9.lean |
| O5 | ξ′ linked record: liminf N₀ˢ_{ξ′}/N_{ξ′} ≥ (657,500·H_{ξ′} − 1,310)/655,001 | 🔶 MACHINE-ACCEPTED (T3 pass 2026-08-16: `Zeta23.XiPrime.record_c9xip` + AdmWindow MT instance `admWindow_phiV_MT` (cMT = cRho+4), `windowZeroSide_atV_MT`; `lake build Record9.XiPrimeMT` exit 0/8845 jobs; axioms gold standard; open: AtOne κ₁(1,vMT) sandwich, xiChain bridge, profile L¹-norms) | lean-proof/Record9/Record9/XiPrimeMT.lean (module `Record9.XiPrimeMT`, namespace `Zeta23.XiPrime`; FORMALIZATION_STATUS_XIP.md) |
| O6 | Evidence discipline labels on all deliverables | ✅ documented (candidate_proof.md honest status) | — |

## Build plan (executed 2026-08-15)

1. ✅ Toolchain: snapshot pins leanprover/lean4:v4.33.0-rc2 — installed at
   C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.33.0-rc2.
2. ✅ Mathlib4 @ 51e6992e fetched (git) + oleans built; `lake build Zeta23` PASSED
   (9010 jobs, exit 0) — build-run.log.
3. ✅ sorry/admit/axiom scan + gold-standard `#print axioms` (axioms-check.log):
   clean (see machine_check.log for the full resolution of the 44 naive-scan hits).
4. T1/T2/T3: T1 formalizer dispatched 2026-08-15 (lean-proof/Record9/); T2 (certificate
   reflection) and T3 (ξ′) follow the lean-verify protocol; contract:
   reports/lean-formalization-contract.md.
5. ✅ run-manifest.json + verification.json + this STATUS.md updated; git sync at stage close.

## Gate status

validate_pipeline: "no lean manifest" warning CLEARED 2026-08-15 (lean-proof/run-manifest.json
written by verify_lean_project.py). Remaining gate: O2–O5 obligations open (T1 pass in
progress); independent verifier audit of O1 pending.
