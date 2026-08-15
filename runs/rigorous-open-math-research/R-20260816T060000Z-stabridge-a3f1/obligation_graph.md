# Obligation graph — T1c-1 / T1c-2 stability-bridge

Run: `R-20260816T060000Z-stabridge-a3f1`.

```
T1c (bridge, OPEN -> statement-pinned) 
├── T1c-1 stability_eps: S >= H_MT·N + Δ(M°) − o(N)
│   ├── [P] Lemma 2.1 (Ψ rank-inertia)            ← new; proof structure from snapshot LinAlg + RankTraceMult
│   ├── [P] base assembly Thm-D                    ← EXISTS (machine): mult_two/N0star_lower_c/thmD_mult2_abstract
│   └── [A] additive survival of +Δ(M°) in assembly ← NEW analytic (OpenAI Cor 2.2 audited); formalize
└── T1c-2 stability_averaged_eps: Δ(M°) ≥ (A₀/m)S − ((m−1)/(500m))N − o(N)
    ├── T1c-2a block energy E_m+(1/500)span ≥ A₀    ← [P] finite window-sum; INPUT CERTIFIED_F8_GE (T2, OPEN)
    ├── T1c-2b defect lemma trΨ(G) ≥ min(1,2Σ|G|²)  ← [P] elementary Hermitian; A₀<1 machine (A0_lt_one)
    ├── T1c-2c pinch/average → defect numbers       ← [P] finite algebra; [A] pinching trΨ(M°)≥block avg
    └── T1c-2d uniformity Σ|G_ij|²=(1/2)E_m+o(1)    ← [A-P] kernel-limit (machine-proved) + block×finite transfer
```
[P] = proved at analysis level in this pass (finite/structural). [A] = analytic ingredient
stated precisely, Lean formalization is a follow-up. Statement forms (ε-form) == Chain9's
`stability_eps`/`stability_averaged_eps`; `deltaMT` placeholder to be replaced by `tr Ψ(M°)`.
