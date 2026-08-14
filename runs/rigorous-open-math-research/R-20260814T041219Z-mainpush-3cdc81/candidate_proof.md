# Candidate Proof / Verified Result

Run: `R-20260814T041219Z-mainpush-3cdc81`.

## R1 (VERIFIED — this run): OpenAI/GPT-5.6 draft, Theorem 1.1

**Theorem R1.** One has, with H_MT = 3/2 − (1/√2)·cot(1/√2) = 0.6725007036794116457…,

  liminf_{T→∞} N0^s(T,2T)/N(T,2T) ≥ (1,345,000·H_MT − 2,680)/1,340,003 = 0.6730085279277797613… .

**Status: verified.** Two computer-assisted inputs re-certified byte-identically
(reproducibility: 3-point ε4 ≥ 221/10^6 and 7-point F6 ≥ 19/5000, both Arb/128-bit, grid
16000/4000, kernel-table and second-derivative-table hashes match committed certificates).
Every algebraic step of the paper's Lemma 2.1, Corollary 2.2, §4 (block-energy, block-defect,
§5 shifted-block pinching and defect numbers), and §6 (final constant) was independently
re-derived and confirmed. The baseline H_MT·N bound on simple on-line zeros is the
Lean-verified Theorem D (`Zeta23.ThmD.thmD₀_simple_mult`).

**Key steps (full proof reconstructed independently — see research_ledger Entries 3–4):**

1. **Lemma 2.1 (stability-enhanced rank–trace).** For V with ||col_j|| ≤ 1, P=VVᵀ ≥ 0,
   M=VᵀV, Q Hermitian with n₊(Q) ≤ b, and Ψ(t) = (t−1)²·1_{t≤2} + (2t−3)·1_{t≥2}:
   ‖P+Q‖²_F ≥ 4tr(P+Q) − 3r − 4b + tr Ψ(M).
   Proof: Q=Q₊−Q₋; ‖Q₊‖² ≥ 4trQ₊−4b; by ‖P−Q₋‖² ≥ Σ(pᵢ−nᵢ)² (Hoffman–Weyl Frobenius) and
   min_n[(p−n)²+4n] = 2p−1+Ψ(p), get ‖P−Q₋‖² ≥ 2trP−r+trΨ(M)−4trQ₋. Combine; use trP ≤ r.

2. **Corollary 2.2.** Â = P₁+Q′ yields s₁ ≥ 4trÂ −‖Â‖² − 2N(I′) + tr Ψ(M), then
   N₀s(T,2T) ≥ H_MT·N(T,2T) + tr Ψ(M°) − o(N).

3. **7-point pressure (certified).** F6(g₁..g₆) := (1/3000)Σgᵢ + Σ_{r=1}^{6} (2/(7−r))Σ_{i=1}^{7−r}
   w(gᵢ+…+g_{i+r−1}) ≥ 19/5000 for all g≥0 (Arb-certified; w = k², k the normalized
   Montgomery–Taylor kernel).

4. **Block-energy.** Summing over (m−6) 7-windows: E_m + (1/500)(y_m−y₁) ≥ (19/5000)(m−6),
   E_m = 2Σ_{i<j}w(y_j−y_i).

5. **Block-defect.** tr Ψ(G) ≥ min{1, 2Σ_{i<j}|G_ij|²}. With m=269, A0 = 4997/5000 < 1 forces
   D(G_B) + (1/500)span(B) ≥ A0 − o(1) uniformly (kernel-limit lemma applies since span<500).

6. **Pinching + averaging.** For 269 offsets, D(M°) ≥ (4997/1,345,000)·N₀s − (268/134,500)·N − o(N).

7. **Conclusion.** (1 − 4997/1,345,000)N₀s ≥ (H_MT − 268/134,500)N ⟹ final constant.
   Arithmetic check: 1,345,000−4997 = 1,340,003; 1,345,000·(268/134,500) = 2680.

## R2 (VERIFIED — this run): conditional "probability 1"

**Theorem R2.** The Pair Correlation Conjecture in its Essential-Simplicity form (equivalently,
PCC of full support, [GLSS25]) implies
  lim_{T→∞} N0(T)/N(T) = 1   (and N0^s/N → 1).
**Proof chain (verified):** [GS25 Thm 2] with C=1 gives proportion ≥ 2−C = 1 of critical zeros,
given ES; [GLSS25] (arXiv:2503.15449) proves PCC ⟹ ES without RH. ES is the λ→0 small-distance
limit of PCC where the diagonal dominates ("essential simplicity").

## R3 (NOVEL — this run): ceiling of the OpenAI certificate class

**Theorem R3.** Let C(m) denote the liminf constant certified by the OpenAI stability-refinement
method using m-point blocks with the 7-point pressure input. For the rigorously valid range
m ≤ 269 (where the A0<1 device applies), C(m) ≤ C(269) = 0.6730085. The formal large-block
symbolic limit (requiring uncontrolled large-block spectral monotonicity) is
lim_{m→∞} C(m) = (H_MT − 1/500)/(1 − 19/5000) = 0.6730583…. In particular the class does not
escape the bandwidth-one ceiling 0.6818287.
(Reproducibility: probe_blocks.py.)

## Status of the user goal
"Point on the critical line, proportion → 1" (lim N0/N = 1):
- **Achieved conditionally:** reduced exactly to PCC (ES) / full-support PCC (R2), a named
  conjecture.
- **Obstructed unconditionally:** the full known lower-bound certificate toolchain caps at
  < 0.69 (R3, bandwidth-one 0.6818, ghost-config invariance, k=1 moment barrier).
- **Not achieved unconditionally.** An unconditional proof remains OPEN and is equivalent-class
  to deep new input (break the ghost invariance / evaluate tr G̃^k k≥2 / PCC-type info).
