# Research Ledger

Run: `R-20260814T041219Z-mainpush-3cdc81`. Chronological experiments/derivations/decisions.

## Entry 1 (provenance / env)
- Confirmed run root empty; read task packet, PROJECT.md, FRONTIER map.
- Python 3.10.11; python-flint not installed. Installed python-flint 0.9.0, then `pip install -e .`
  in literature/raw/zeta-simple-zeros.

## Entry 2 (O2 finite verifier — both PASS, byte-match)
- Unit tests: 7/7 pass.
- `zeta-zero-verify three --json`: PASS. certifies ε4 ≥ 221/10^6 on {u,v≥0,u+v≤4}, grid 16000,
  128-bit. kernel_table_sha256 e19c0637…; nodes 7157, pruned 3579, splits 3578, depth 32.
  Byte-identical to certificates/three-point.txt.
- `zeta-zero-verify seven --progress-every 200000` (background): PASS after ~200 s. certifies
  F6 ≥ 19/5000, grid 4000. kernel_table_sha256 a9992300…, second-derivative 7913c551…,
  nodes 707901, depth 37, components [3809,4778];[7221,9363];[10572,44827].
  Byte-identical to certificates/seven-point.txt (including all deterministic counts).
- Hash match ⇒ reproducible, deterministic certificates.

## Entry 3 (independent math audit of OpenAI draft)
- Read paper/riemann.tex fully. Re-derived:
  * min_{n≥0}((p−n)²+4n) = p² (0≤p≤2) else 4p−4 = 2p−1+Ψ(p). Verified exact at many p.
  * Lemma 2.1 assemblage: uses ‖P−Q₋‖² ≥ Σ(pᵢ−nᵢ)² (Wielandt–Hoffman/Hoffman–Weyl Frobenius),
    ‖Q₊‖² ≥ 4trQ₊−4b, von Neumann. Final form ‖P+Q‖² ≥ 4tr(P+Q)−3r−4b+D(M) is correct
    (the intermediate 4tr(P+Q)−2trP−r = 4trQ+2trP−r, then trP≤r ⇒ −3r).
  * Corollary 2.2: eq:s1 verified via eq:Nlower. 
  * Final constant and block-averaging verified (see Entry 4).
- Outcome: OpenAI draft mathematics is internally consistent and correct; depends on
  (a) Lean-verified Thm D baseline, (b) the two certificates (re-verified).

## Entry 4 (block-energy / defect / averaging algebra)
- Verified block-energy lemma: Σ over (m−6) 7-windows gives E_m + (1/500)(y_m−y_1) ≥ (19/5000)(m−6).
- Verified block-defect lemma: tr Ψ(G) ≥ min{1, 2Σ_{i<j}|G_ij|²}.
- Verified m=269 → A0 = (19/5000)(263) = 4997/5000 < 1 (the reason for m=269).
- Verified the block inequality D(G_B)+(1/500)span ≥ A0 − o(1) for both E_m ≥ A0 and E_m < A0.
- Verified defect numbers 4997/1,345,000 and 268/134,500; final ratio (1,345,000 H_MT −2680)/1,340,003.
- Outcome: Theorem 1.1 fully derived and correct.

## Entry 5 (3-point triangle dual form)
- Checked the "dual form" (3.4) triangle case tr Ψ(M) ≥ (3/2)Σ_{i<j}M_ij²: empirical min ratio
  over 200k random 3×3 PSD Gram matrices = 1.6723 ≥ 1.5 (evidence; a known majorization-type
  inequality). Numerical min of k(u)²+k(v)²+k(u+v)² on {u+v≤4} = 0.0002229 at (1.054,2.012),
  consistent with certified 0.000221. The 3-point result (67.2519767%) is dominated by the
  7-point (67.3008528%) and not needed for the headline.

## Entry 6 (O1/Lean baseline)
- Lean `Zeta23/ThmD/Mult.lean` thmD₀_simple_mult: N₀s(T,2T) ≥ (HD 1 − ε)N(T,2T), HD 1 =
  3/2 − cot(1/√2)/√2. Confirms OpenAI's H_MT baseline (0.6725…) is Lean-verified for SIMPLE
  on-line zeros. The 0.5065 "Cauchy–Schwarz" thmD₀_simple is weaker; the mult version is the one
  used. Consistency OK.

## Entry 7 (O3 ceiling — novel)
- Derived c(m) = (H_MT − (m−1)/(500m))/(1 − 19(m−6)/(5000m)) for m ≥ 7.
- Numerically: increasing in m; m=269 → 0.6730085 (OpenAI value); m→∞ → 0.6730583.
- Rigorous only for m ≤ 269 (A0 ≤ 1). For m>269 the min{1,·} device requires large-block
  spectral control (open). Ceiling of the class ≈ 0.673058, NOT above bandwidth-one 0.6818.
- Outcome: the OpenAI class does NOT escape the 0.6818 ceiling; its own ceiling ≈ 0.673058.

## Entry 8 (O4 reduction and obstruction)
- Read GS25 (arXiv:2511.20059). Verified: Thm 2 (C<2 ⟹ proportion ≥ 2−C of critical zeros);
  ES (8.3), C=1 ⇒ 100% on line; [GLSS25a/GLSS25] prove PCC ⟹ ES without RH.
- So `lim N0/N = 1 ← PCC (ES)`, named-conjecture reduction verified.
- Obstruction: ghost off-line-pair configs invariant to method data; k=1 moment barrier;
  Prop 7.4 cap. Lower-bound-only cert classes cannot reach 1.

## Entry 9 (O5 HL* partial)
- Verified arithmetic: 1 − 2Λ₂(0) = 13/18 ⟺ Λ₂(0)=5/36; general count s₁ ≥ 2n+(G̃)−N gives
  liminf N₀s/N ≥ 1 − 2Λ_m(0); all-k0 ⇒ Λ_m(0)→0 ⇒ 1.
- Could NOT reproduce m_k(1) = 1,3/4,2,13/4 as raw moments of a positive spectral measure
  (m₂=3/4 < m₁²=1 infeasible). Flagged as informal normalization issue in §7.2(f). Exact
  moment values + Christoffel interpretation require the paper's specific operator convention
  (open).

## Entry 10 (O6 numerical evidence)
- mpmath.zetazero enumeration. N0(0,T)/N(T): T=50→1.061, 100→0.9999, 200→0.9976, 300→1.0021,
  500→0.9978, 700→0.9987. All computed zeros on line; consistent with RH verified to 3e12 [PT21].
  Evidence only.

## Entry 11 (O7 literature)
- Resolved CGdL20, PRZZ20, Wu15, GLSS25, GS25 via web search. CCLM17 unresolved (traceability gap).
