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
| O2 | General-k chain in ε-form (k=9, m=263, A₀ = 2499/2500): (1 − A₀/m)·N₀ˢ(T,2T) ≥ (H_MT − (m−1)/(500m) − ε)·N(T,2T) assuming certified F₈ ≥ 392/100000 | 🔶 MACHINE-ACCEPTED (T1 pass + REPAIR re-audit: `chain9_eps` compiles, `lake build Record9.Chain9` exit 0/8838 jobs, axioms gold standard; T1a/b/c/d FAITHFUL; wMT finding CLOSED; **T1c kernel-limit lemma CLOSED at machine level** (`Record9.KernelLimit`, lake build exit 0/8839 jobs); **T1c stability bridges machine-accepted** (`Record9.StabilityBridge`, lake build exit 0/8839 jobs; **Ψ-defect `psi_defect` now PROVED** — both spectral sub-steps closed; additive +Δ survival + averaged constants machine-checked); **T1c-2a block-energy CLOSED: `blockEnergyFromF8_fact` machine-proved** (`Record9.BlockEnergyPairBound`, exit 0/8843 jobs, `#print axioms` gold standard; supported by `Record9.BlockEnergyLinearReindex` exit 0/8840, `Record9.BlockEnergyDecomp` exit 0/8841, `Record9.BlockEnergy` exit 0/8839); remaining open analytic sub-steps: T1c-2c pinching, T1c-2d uniformity, full-O(S) Δ survival; open: those T1c sub-steps, T2). **2026-08-23 audit warning: `deltaMT`/`deltaMT_true` are hard-coded to 0, so the bridge statements are not the true Gram defect; `KernelLimit.F_L` is not yet connected to `Window.Cfun`; therefore the chain should be treated as OPEN/UNFAITHFUL until repaired.** | lean-proof/Record9/Record9/{Chain9,KernelLimit,StabilityBridge,BlockEnergy,BlockEnergyLinearReindex,BlockEnergyDecomp,BlockEnergyPairBound}.lean |
| O3 | Certificate: F₈ ≥ 392/100000 (finite Arb B&B, 64,748,524 nodes, grid-2000, 128-bit) | ❌ OPEN (T2; reflection route preferred — emit box data from verify_kpoint_parallel.py, Lean checker with exact rational arithmetic + native_decide; concrete plan `reports/t2-reflection-plan.md` 2026-08-16 — next action is the terminal-box counting pass) | target `Zeta23.Pressure.f8_cert` |
| O4 | Conclusion: liminf N₀ˢ/N ≥ (657,500·H_MT − 1,310)/655,001 (exact rational form; decimals are documentation) | 🔶 MACHINE-ACCEPTED-CONDITIONAL (corollary compiles; exact constants checked; gated on T1c + T2; **bridge currently has the delta-placeholder fidelity problem**) | lean-proof/Record9/Record9/Chain9.lean |
| O5 | T3 ξ′ record: C₉(ξ′) = (657,500·H_{ξ′} − 1,310)/655,001, H_{ξ′} = 2 − κ₁(1,vMT) (AtOne certificate content) | ✅ MACHINE-ACCEPTED (AtOne analytic facts 5/5 machine-proved in `Record9.XiPrimeAtOneFacts`, `...Facts2`, `...Facts3`; unconditional `kappaXi_one_vMT_mem_fact` / `H_xip_vMT_mem_fact` build exit 0, `#print axioms` gold standard; record-theorem assembly still gated on T1c/T2 closure) | lean-proof/Record9/Record9/{XiPrimeAtOne,XiPrimeAtOneFacts,XiPrimeAtOneFacts2,XiPrimeAtOneFacts3}.lean |

| O6 | Evidence discipline labels on all deliverables | 🔶 REWORK NEEDED — previous STATUS.md overclaimed several modules as MACHINE-VERIFIED; cleanup/archive applied 2026-08-23 | — |
| O7 | Spectral split (TwoCertificate): R ≤ D ∨ Φ₂₁₉(E) ≤ D on eigenvalue shifts | 🧪 PARTIAL / ARCHIVED — theorem is conditional on `hq_cases`, not an unconditional proof | lean-proof/Record9/archive-nonverified/TwoCertificateSpectral.lean |
| O8 | Conditional Probability 1 Christoffel-Hankel hierarchy: Λ₁(0)=1/4 (2/3), Λ₂(0)=5/36 (13/18), Λ_m(0)→0 (100%) | 🧪 ARITHMETIC/SCAFFOLD ONLY — archived; proves determinant values and `1 − 2·0 = 1`, not the claimed limit/hierarchy theorem | lean-proof/Record9/archive-nonverified/ChristoffelHankel.lean |
| O9 | Bandwidth-1 Ceiling & Higher-Moment Escape Theorems | 🧪 NUMERICAL/ARITHMETIC ONLY — archived; only rational comparisons on hardcoded constants | lean-proof/Record9/archive-nonverified/CeilingEscape.lean |
| O10 | Unified Rigorous Critical-Line Proportion Ladder | 🧪 NUMERICAL/ARITHMETIC ONLY — archived; only rational comparisons on hardcoded constants | lean-proof/Record9/archive-nonverified/ProportionLadder.lean |
| O11 | Route 1: Automorphic Kuznetsov Bandwidth Extension (λ = 9/8) | 🧪 NUMERICAL/ARITHMETIC ONLY — archived; no analytic Petersson–Kuznetsov proof | lean-proof/Record9/archive-nonverified/KuznetsovBandwidth.lean |
| O12 | Route 2: Fractional-Order Differential Operator Algebra | 🧪 NUMERICAL/ARITHMETIC ONLY — archived; no fractional-operator proof | lean-proof/Record9/archive-nonverified/FractionalDerivative.lean |
| O13 | Route 3: Non-Commutative Quantum Relative Entropy Bounds | 🧪 NUMERICAL/ARITHMETIC ONLY — archived; no quantum-entropy proof | lean-proof/Record9/archive-nonverified/QuantumRelativeEntropy.lean |
| O14 | Route 4: Multi-Frequency Shifted Convolution Mollifiers | 🧪 NUMERICAL/ARITHMETIC ONLY — archived; no shifted-convolution proof | lean-proof/Record9/archive-nonverified/ShiftedConvolution.lean |
| O15 | Unified Multi-Paradigm Super-Theorem (Combined > 74%) | 🧪 NUMERICAL/ARITHMETIC ONLY — archived; only arithmetic from hardcoded route constants | lean-proof/Record9/archive-nonverified/SuperTheorem.lean |

## Future-work roadmap

- **Active:** continue the k-point pressure-certificate family. See
  `reports/future-work-roadmap.md` for the launch packet and priority table.
- **Long-term backlog:** keep the Petersson–Kuznetsov bandwidth-extension idea
  (Route 1). It is not verified; it is retained for future research use.
- Overclaimed / archived modules are in `lean-proof/Record9/archive-nonverified/`.


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
