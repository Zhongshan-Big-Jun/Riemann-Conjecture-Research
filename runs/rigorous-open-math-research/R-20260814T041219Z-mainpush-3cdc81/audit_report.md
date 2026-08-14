# Audit Report (adversarial, independent)

Run: `R-20260814T041219Z-mainpush-3cdc81`
Auditor: independent adversarial verification agent (this report replaces the earlier
pre-population audit). Supersedes: `audit_report.md` sha256 `DCE3B765D6C1F6642AADC3032DAB9CE34265C92527F5528CEE228BBBE834505E`,
which is preserved verbatim as `audit_report.initial-race.md` in this run root.
Audit method: Phase 8 adversarial, independent re-derivation, with re-execution of every
reproducibility script (`py -3`, Python 3.10.11, python-flint 0.9.0 / Arb available) and an
independent re-run of both finite searchers in the OpenAI repo.

Audit scope: R1 (OpenAI draft Theorem 1.1 constant 0.6730085279277797613...),
R2 (PCC/ES ⟹ lim N0/N = 1), R3 (OpenAI certificate-class ceiling). Every obligation
O1–O8 of the task packet was checked.

---

## Verdict summary

- **R1**: `INDEPENDENTLY_AUDITED_PROOF` (paper-level chain). The two finite universal certificates
  are **machine-verified** and byte-identical to committed (independent re-run, see §B). The full
  algebraic chain Lemma 2.1 → Cor 2.2 → §4–6 → final constant was **independently re-derived and
  confirmed** (see §C). Residual: the chain is not Lean-formalized end-to-end (no machine proof
  covers Lemma 2.1 → Theorem 1.1); baseline Theorem D is Lean-verified.
- **R2**: `VERIFIED_CONDITIONAL_REDUCTION` (faithful to primary sources GS25 & GLSS25; reduction
  only, not re-proved).
- **R3**: ceiling analysis correct and numerically confirmed; minor rigor caveat on monotonicity
  (see §E).
- **Overall**: no claim exceeds the OpenAI value; the OpenAI draft value itself is independently
  verified. The user goal `lim N0/N = 1` is **reduced to PCC/ES** and **obstructed unconditionally**
  by the known certificate toolchain; it is **OPEN** unconditionally.

Structured verdict record (canonical promotion shape):
```json
{
  "verdict": "REPAIRABLE_GAP",
  "critical_errors": [],
  "gaps": [
    {"location": "R1 chain (Lemma 2.1..Thm 1.1)", "issue": "paper-level, not Lean-formalized end-to-end; rests on Claude [1] Prop 4.4 inertia, tail & kernel-limit lemmas"},
    {"location": "O5 moment sequence m_k=1,3/4,2,13/4", "issue": "not reproducible as raw positive-measure moments; informal operator convention in Claude §7.2(f)"},
    {"location": "R3 monotonicity/ceiling", "issue": "max-at-269 over rigorous window established numerically, not by a proven-inequality-on-m"},
    {"location": "reproducibility/audit_arb.py", "issue": "cosmetic: .contains(claim) False because claim string is truncated beyond the 10^-74 Arb envelope (constant itself correct)"}
  ],
  "repair_hints": "1) Lean-formalize Lemma 2.1→Thm 1.1 (already: certificates + Thm D baseline). 2) Pin the operator convention for m_k or drop O5 as a claim. 3) Prove c(m) monotone on [7,269] to fully justify C(269) as rigorous window max. 4) In audit_arb.py compare the full claim decimal inside the envelope."
}
```

---

## A. Environment (what could / could not be run)

- Host: Windows, Python 3.10.11 (`py -3`). python-flint 0.9.0 provides `flint.arb` → **Arb IS
  installed** (contrary to the audit brief's allowance). numpy, mpmath present.
- Re-ran (all pass): `verify_constants.py`, `audit_arb.py`, `probe_blocks.py`, `verify_hl.py`,
  `check_triangle_dual.py`, OpenAI repo `unittest discover` (7/7), and both finite searchers.
- `numerical_corroboration3.py`: mpmath `zetazero` enumeration (only needs mpmath; ran implicitly
  consistent with the ledger's table).
- NOT re-run here: Lean `lake build` (Lean toolchain not activated in this session). The Lean
  snapshot artifacts (ThmD/Mult.lean, PairCeiling/CeilingLaw256.lean) were **read** to confirm the
  constants the chain depends on.

## B. Finite certificates (machine-verified, byte-identical, on my independent re-run)

Three-point search (from `zeta-simple-zeros`, `py -3 -m zeta_simple_zeros three --json`):
kernel_table_sha256 `e19c06374eaf6f...`, nodes 7157, pruned 3579, splits 3578, depth 32,
verified=true, `certified_epsilon = 0.000221` on `{u,v≥0,u+v≤4}`, grid 16000, 128-bit.
This certifies **ε4 ≥ 221/10^6** (universally on the stated compact domain).

Seven-point search (`... seven --json`, ~210 s): kernel_table_sha256
`a9992300d2bf7166...`, second_derivative `7913c5511a572c32...`, initial_boxes 729, nodes 707901,
pruned 354315, splits 353586, depth 37, surviving gap components `[3809,4778];[7221,9363];[10572,44827]`,
verified=true, grid 4000, 128-bit. This certifies **F6 ≥ 19/5000 for all g1..g6 ≥ 0** (universal).

Both outputs match the committed `certificates/*.txt` byte-for-byte, including all deterministic
counter fields and the kernel/second-derivative table hashes. These two inputs are therefore
**real, reproducible, machine-checked universal inequalities**; they are not the source of any
error.

## C. Independent re-derivation of R1 (OpenAI Theorem 1.1)

Target: `liminf N0^s(T,2T)/N(T,2T) ≥ (1,345,000·H_MT − 2,680)/1,340,003 = 0.6730085279277797613...`,
H_MT = 3/2 − (1/√2)cot(1/√2).

### C.1 Constants (exact)
- H_MT = 0.6725007036794116457343797908032951885934030286...   (mpmath ≥ 200 dp; paper claims ...6457 ✓).
- 1/c1* = 1/2 + 2^{-1/2}cot(2^{-1/2}) = 1.32749929632...; c1* = 2·tan(1/√2)/(√2 + tan(1/√2)) =
  0.753296067856...; `2 − 1/c1* = H_MT` (exact; Arb overlap confirmed).
- Final constant `(1,345,000·H_MT − 2,680)/1,340,003 = 0.6730085279277797613...` (re-derived, matches).
- Defect numbers: A0 = (19/5000)·263 = 4997/5000 = 0.9994 < 1 (m=269); A0/m = 4997/1,345,000;
  (m−1)/(500m) = 268/134,500; 268/134,500 = 2680/1,345,000. All exact.
- Final arithmetic: 1 − 4997/1,345,000 = 1,340,003/1,345,000; H_MT − 268/134,500 =
  (1,345,000·H_MT − 2680)/1,345,000, ratio = (1,345,000·H_MT − 2680)/1,340,003. ✓

### C.2 Lemma 2.1 (stability-enhanced rank–trace inequality) — CORRECT
`‖P+Q‖²_F ≥ 4tr(P+Q) − 3r − 4b + trΨ(M)`, Ψ(t)=(t−1)² on [0,2], 2t−3 on [2,∞). Independent proof:
- Q = Q₊ − Q₋, Q± ⪰ 0, rank Q₊ ≤ b; q_j² ≥ 4q_j − 4 ⇒ ‖Q₊‖² ≥ 4trQ₊ − 4b. ✓
- Von Neumann: tr(PQ₋) ≤ Σ pᵢnᵢ ⇒ ‖P−Q₋‖²_F + 4trQ₋ ≥ Σ[(pᵢ−nᵢ)² + 4nᵢ]. The min identity
  min_n≥0[(p−n)²+4n] = p² (0≤p≤2) else 4p−4 = 2p−1+Ψ(p) is exact (verified at p∈{0,0.5,…,10}). ✓
- Hence ‖P−Q₋‖² ≥ 2trP − r + D(M) − 4trQ₋ (with D(M)=trΨ(M) over the r×r Gram matrix). ✓
- Combine: ‖P+Q‖² ≥ 2trP − r + D(M) + 4trQ − 4b = 4tr(P+Q) − 2trP − r − 4b + D(M); trP ≤ r
  (column norms ≤ 1) ⇒ ≥ 4tr(P+Q) − 3r − 4b + D(M). ✓ **No error found.**

### C.3 Corollary 2.2 — CORRECT
Apply Lemma 2.1 to P₁ + Q₀ = Â with r = s₁, b = s₂ + p (using (1) N(I⁰) ≥ s₁+2s₂+2p and (2)
n₊(Q₀) ≤ s₂+p from Claude [1] Prop 4.4). Rearrangement gives
`s₁ ≥ 4trÂ − ‖Â‖² − 2N(I⁰) + D(M)`. Substituting Theorem D (`trĜ=N(1+o)`,
`‖Ĝ‖²=(1/c1*+o)N`, N(I⁰)=N(T,2T)+o(N)); `4−2−1/c1* = 2−1/c1* = H_MT`:
`s₁ ≥ H_MT·N + D(M)`. Pinching `D(M) ≥ D(M°)`. → eq (8). ✓ (Consistent with Lean
`Zeta23.ThmD.thmD₀_simple_mult` N0s ≥ (HD1−ε)N, HD1 = 3/2 − cot(1/√2)/√2 = H_MT.)

### C.4 Lemma 4.2 (block-energy) — CORRECT
Summing F6 ≥ 19/5000 over (m−6) consecutive 7-windows: a pair spanning r gaps appears in ≤ 7−r
windows at coefficient 2/(7−r) ⇒ per-pair contribution ≤ 2w(y_j−y_i) = E_m term; each gap counted
≤ 6 times ⇒ linear part ≤ (1/3000)·6·Σg = (1/500)(y_m−y₁). Hence
`E_m + (1/500)(y_m−y₁) ≥ (19/5000)(m−6)`. ✓

### C.5 Lemma 4.3 (block-defect) — CORRECT, and A0<1 is essential
`trΨ(G) ≥ min{1, 2Σ_{i<j}|G_ij|²}`:
- all eigenvalues ≤ 2 ⇒ Ψ(G)=(G−I)², tr(G−I)² ≥ 2Σ|G_ij|² (since |G_ii−1|≥0). ✓
- some λ>2 ⇒ Ψ(λ)=2λ−3 > 1 ≥ min{1,·}. ✓
- **Crucially, the whole block-exit uses `min{1,·}` and requires A0<1**: in the case E_m ≥ A0,
  `min{1,E_m} ≥ A0` needs A0 ≤ 1. At m=269, A0 = 4997/5000 < 1. For m>269 (A0>1) the device
  fails — confirming the solver's claim that m>269 is NOT rigorous without large-block spectral
  control. **The paper's A0<1 boundary is exactly m=269.**

### C.6 Pinching + averaging (§5) — CORRECT
D(M°) ≥ Σ_B D(G_B) (pinching = average of unitary conjugations, X↦trΨ(X) convex + unitarily
invariant). Per offset, sum (18) over full m-blocks; average over m offsets: #full blocks = S°/m +
O(1), each gap internal to a block-span for at most (m−1) offsets, Σ_gaps ≤ (m−1)(x_{S°}−x₁) ≤ (m−1)N(1+o).
⇒ `D(M°) ≥ (A0/m)N0^s − ((m−1)/(500m))N − o(N)` = (21). With m=269: (4997/1,345,000)N0^s − (268/134,500)N. ✓

### C.7 Final combination — CORRECT
`[1 − 4997/1,345,000]N0^s ≥ [H_MT − 268/134,500]N` ⇒ `N0^s/N ≥ 0.6730085279277797613...`. ✓
No RH or unproven conjecture used; every "analytic estimate of Theorem D in [1]" matches the
Lean-verified Theorem D statement (nothing stronger imported).

**R1 audit verdict: independently re-derived and correct.** Residual risk is single-layer:
the paper-level chain is not Lean-formalized end-to-end. The two certificates and the Theorem D
baseline are machine-verified. This precisely matches the run's honest label.

## D. R2 — PCC(ES)/full-support PCC ⟹ lim N0/N = 1 (verified as a reduction)

Cross-checked against GS25 (arXiv:2511.20059) directly:
- **GS25 Theorem 2** (p.4): if for 1 ≤ C < 2 the horizontal same-height sum
  `Σ_{γ=γ′} 1 ≤ (C+o(1))(T/2π)log T`, then ≥ (2−C) of zeros are simple and ≥ (2−C) are on the
  critical line. With C = 1 this gives proportion ≥ 1 ⇒ = 1 for critical-line zeros.
- **ES (Essential Simplicity)** (GS25 (8.3)): if λ→0 then `Σ_{|γ−γ′|≤2πλ/logT} 1 = (1+o(1))(T/2π)logT`;
  GS25 states "Clearly (8.3) implies C = 1, thus Theorems 2 and 3 follow from ES."
- **GLSS25** (arXiv:2503.15449) proves PCC ⟹ ES without RH (GS25 lines 456–492, and its
  reference list/statement "PCC implies asymptotically 100% of the zeros are simple and on the
  critical line" — Theorem 5).

Linking to the user's with-multiplicity ratio: if ≥ (1−o(1))·N(T) distinct zeros are on the line,
the off-line multiplicity contribution to N is o(N(T)), hence N0(T)/N(T) → 1. **R2 is faithful**
(reduction to named preprints; not re-proved here, as the run honestly states).

## E. R3 — certificate-class ceiling (correct; minor monotonicity caveat)

- Formula (independent): `C(m) = (H_MT − (m−1)/(500m)) / (1 − 19(m−6)/(5000m))`, m ≥ 7.
- Re-ran `probe_blocks.py`: c(m) strictly increasing on the computed range; c(269)=0.6730085279…,
  asymptotic m→∞ = (H_MT − 1/500)/(1 − 19/5000) = **0.6730583253…**.
- Comparison: 0.673058 < **0.68182868746** (the Lean-verified bandwidth-one ceiling,
  `PairCeiling/CeilingLaw256.lean`, N=256 law's simple-point fraction). The class does NOT escape it. ✓
- Claims validated: three-point result (0.672519767) < seven-point (0.673008528); 7-point dominates.
- **Caveat (REPAIRABLE):** "C(m) ≤ C(269) rigorously for m≤269" asserts a proven inequality, but
  the max-at-269 relies on numerically observed monotonicity of c(m) (A_m→numerator and
  denominator move against each other; monotonicity is computed, not proven). It is harmless to the
  substantive conclusion (no constant above 0.6730085 is claimed, and the infinite-window limit is
  smaller), but the file should state "computed maximum over m∈[7,269]" unless monotonicity is
  proven.

## F. O5 conditional HL* (internal arithmetic OK; moment sequence OPEN)

- Identity `1 − 2·Λ2(0) = 13/18 ⟺ Λ2(0) = 5/36` confirmed (13/18 = 1 − 10/36).
- Clause (b) of the task (1 − 2Λ_m(0) ⟹ liminf N0s/N ≥ 1 − 2Λ_m(0)) verified structurally.
- **Open gap (faithfully reported):** m_k(1)=1, 3/4, 2, 13/4 cannot be raw moments of a positive
  spectral measure (m₂ = 3/4 < m₁² = 1 is impossible); `verify_hl.py` confirms the raw-moment
  Christoffel does NOT reproduce 5/36. The source `claude-paper-main-v2.txt` (lines 1651–1655)
  itself states these as "One computes m_k(1)=…" within an informal §7.2(f); the run correctly
  does not promote O5 to a theorem.

## G. O6 / O7 / O8

- **O6:** `N0(0,T)/N(T)` ≈ 1.0 at T=50..700 from `mpmath.zetazero` — NUMERICAL_EVIDENCE only; cannot
  detect off-line zeros; never a proof. Labeled correctly.
- **O7:** GS25 (2511.20059) confirmed in-source; GLSS25 (2503.15449) confirmed in GS25's reference
  list and statement; PRZZ20 "More than five-twelfths" (Res. Math. Sci. 7, 2020), BHB13 (BLMS 45,
  2013), CGdL20 (Adv. Math. 361, 2020), Wu15, MV74 consistent with the Claude reference list.
  **CCLM17 remains unresolved** as an exact bibliographic entry (referenced only in the Claude
  paper §7.1 as "[CCLM17, Corollary 14]"); it is NOT a theorem input to the OpenAI draft (which
  cites only [1] Claude, [2] Arb, [3] Mon73, [4] Mon75), so it does not affect R1. Traceability gap,
  correctly recorded.
- **O8:** artifact set, hashes, honest labels, open-obligation list all present and consistent.

## H. Full findings list (smallest failing claim / exact location)

1. R1 chain Lemma 2.1→Thm 1.1: paper-level, not Lean-formalized end-to-end. No error found in the
   mathematics; label is INDEPENDENTLY_AUDITED (paper-level), not formally verified. [candidate_proof.md R1; run_report.md]
2. O5 m_k moment sequence: infeasible as raw positive-measure moments; informal. Documented open. [obligation_graph.md O5; verify_hl.py]
3. R3: "rigorous C(m)≤C(269)" should read "computed max over the rigorous window [7,269]" unless
   monotonicity of c(m) is proven. No effect on the 0.6730085 / 0.673058 / 0.6818287 conclusions. [candidate_proof.md R3]
4. reproducibility/audit_arb.py: final `.contains(claim)` prints False because the claim string is
   truncated beyond the 10^-74 Arb envelope; the constant H_MT itself is correctly enclosed. Cosmetic;
   fix by comparing the full decimal. [audit_arb.py:25]
5. O7 CCLM17: unresolved bibliography. Traceability only. [obligation_graph.md O7]
6. O4 / user goal: `lim N0/N = 1` reduced to PCC/ES (R2) and obstructed unconditionally; **OPEN**. [candidate_proof.md; run_report.md]

## I. Which obligations remain open

- **O4 (unconditional "probability 1"):** OPEN. Achieved only conditionally (reduction to PCC/ES);
  exact obstruction given (lower-bound-only certificate classes cap < 0.69, ghost-configuration
  invariance, k=1 moment barrier, Prop 7.4).
- **O3:** no unconditional constant strictly above 0.6730085279278 proven; the OpenAI value itself
  is the (verified) result. m>269 needs large-block spectral control (open).
- **O5:** the HL* moment sequence normalization is open (the §7.2(f) values are not pinned).
- **O7:** CCLM17 traceability gap unresolved (non-load-bearing for R1).

## J. Final verdict line

`INDEPENDENTLY_AUDITED_PROOF` for the OpenAI draft value (0.6730085279277797613…) — chain re-derived
correctly, both finite certificates machine-verified and byte-identical on an independent re-run,
baseline Theorem D Lean-verified; the only residual is the lack of an end-to-end Lean formalization
of Lemma 2.1 → Theorem 1.1. `VERIFIED_CONDITIONAL_REDUCTION` for R2. R3 ceiling analysis correct
(minor monotonicity-caveat documented). No finding falsifies any candidate result; the correct, honest
status is `RIGOROUS_PARTIAL_RESULT` — the user's `lim N0/N = 1` remains open unconditionally.
