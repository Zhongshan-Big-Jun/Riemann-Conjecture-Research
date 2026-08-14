# Obligation Graph

Run: `R-20260814T041219Z-mainpush-3cdc81`. Status per obligation from the task packet.

Legend: ✅ discharged (this run), ⬜ open gap, ⚠ partial with flag.

## O1 — Theorem D baseline
- ✅ Re-derive H_MT = 3/2 − (1/√2)·cot(1/√2) = 0.672500703679411646… (mpmath, ≥200 dp; matches claim and Claude §7.1 (7.4) c1* = 2 tan(1/√2)/(2 + tan(1/√2)) = 0.753296…, 2 − 1/c1* = H_MT).
- ✅ Chain (1.2): N0^s + o(N) ≥ 4tr G̃ − 2N − ‖G̃‖²_HS = (2 − R(ψ))N. Confirmed against Claude v2 Prop 4.4(ii), eq (4.6), and Lean `ThmD/Mult.lean thmD₀_simple_mult`: `N₀s(T,2T) ≥ (HD 1 − ε)N(T,2T)`, HD 1 = 3/2 − cot(1/√2)/√2. Verdict: OK.

## O2 — OpenAI draft verification
- ✅ Lemma 2.1 (stability-enhanched rank–trace): re-derived; uses Wielandt–Hoffman/Hoffman–Weyl Frobenius inequality ‖P−Q₋‖² ≥ Σ(pᵢ−nᵢ)² and the min identity min_n[(p−n)²+4n] = 2p−1+Ψ(p). Full algebra checked; **correct**.
- ✅ Corollary 2.2: eq:s1 `s₁ ≥ 4trÂ − ‖Â‖² − 2N(I′) + D(M)` verified using eq:Nlower (`s₁+2s₂+2p ≤ N(I′)`) and n+(Q′) ≤ s₂+p. Also eq:global-defect `N₀s ≥ H_MT·N + D(M°) − o(N)` verified (consistency with Lean Thm D mult2).
- ✅ Theorem 1.1 constant (1,345,000·H_MT − 2,680)/1,340,003 = 0.6730085279277797613… verified (mpmath).
- ✅ 3-point inequality ε4 ≥ 221/10^6 : Arb certificate re-run, byte-match.
- ✅ 7-point six-variable bound F6 ≥ 19/5000: Arb certificate re-run, byte-match.
- ✅ Uses of "analytic estimates of Theorem D in [1]": every use (`tr Ĝ=N(1+o(1))`, `‖Ĝ‖²=(1/c1*+o(1))N`, `S≥H_MT·N`) checked against Claude v2 Theorem D statement + Lean `ThmD`. All faithful.
- ⚠ Caveat: the NEW stability-refinement chain (Lemma 2.1, Cor 2.2, block-energy/defect/averaging) is paper-level; NOT Lean-formalized in the shipped repo. The two certificates ARE machine-checked. Residual risk: none found in paper math, but no machine proof covers the chain end-to-end.

## O3 — Improvement attempt / ceiling
- ✅ Whether the OpenAI class escapes bandwidth-one ceiling 0.6818: **NO**. Computed class ceiling ≈ 0.673058 (m→∞), rigorously 0.6730085 for the exact (A0≤1) OpenAI class (m≤269).
- ✅ Longer blocks (8+, …): the block-energy lemma gives the local pressure for all m ≥ 7; but for m>269 the A0<1 (min{1,·}) device fails and would need spectral control of large blocks (open). Marginal headroom ≤ 5×10⁻⁵.
- ✅ Better Ψ: Ψ in Lemma 2.1 is the pointwise-optimal convex minorant (min identity is exact), so no better Ψ within Lemma 2.1 structure.
- ⬜ Different windows (ψ0 vs ψMT vs quartic) / higher trace moments: not pushed to a proof; the k≥2 moment barrier blocks unconditional gains (§7.2(e)). Marked open.

## O4 — "Probability 1"
- ✅ Verified conditional reduction: PCC (Essential Simplicity form) ⟹ lim N0/N = 1 (via [GLSS25] + [GS25 Thm 2]). Exact named-conjecture reduction.
- ✅ Exact obstruction: (a) lower-bound-only certificate classes (bandwidth-one 0.6818; OpenAI 7pt 0.673058) provably cap < 1 because of ghost/off-line-pair configurations invariant under the method's data; (b) k=1 moment barrier (tr G̃^k k≥2 needs X^k ≤ T^(2−ε)); (c) Prop 7.4 cap (bandwidth ≤ λ1). Proportion 1 unattainable by these.
- ⬜ An unconditional proof of `lim N0/N = 1` — open. Not achieved.

## O5 — Conditional HL* route
- ✅ Internal arithmetic: `1 − 2Λ₂(0) = 13/18 ⟺ Λ₂(0) = 5/36`; general `1 − 2Λ_m(0)`; Γ count `s₁ ≥ 2n+(G̃)−N` ⟹ liminf N₀s/N ≥ 1 − 2Λ_m(0).
- ⚠ Moment values m_k(1) = 1, 3/4, 2, 13/4: NOT independently reproducible as raw moments of a positive spectral measure (m₂ = 3/4 < m₁² = 1 impossible for a positive-measure's raw moments; not reproduced from sine-kernel/DPP models). Flagged as an open normalization subtlety in the informal §7.2(f). m₁=1 fits tr G̃=N; the rest are informal.

## O6 — Numerical corroboration
- ✅ Computed N0(0,T)/N(T) at T=50..700 (mpmath.zetazero): ≈1.0 (deviations ≤ ~6% at low T due to main-term error; ~0.3% at T≥100). Evidence only.

## O7 — Literature integrity
- ✅ CGdL20 (arXiv:1810.08843), PRZZ20, Wu15, BHB13, GLSS25 (2503.15449), GS25 (2511.20059), MV74 resolved.
- ⬜ CCLM17: cannot resolve exact bibliographic data; traceability gap recorded.

## O8 — Honest reporting
- ✅ This artifact set + audit_report + candidate_proof + hashes produced at run root.
