# Problem Contract — Conditional probability-1 (HL* trace-moment route) [FINAL]

Run: `R-20260814T041219Z-condp1-698ec7`
Task packet: `agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md` (obligations O1, O4-conditional, O5).
Skill: `rigorous-open-math-research`. Final status target: `RIGOROUS_PARTIAL_RESULT` (achieved).

## 1. Normalized goal statement

Let ρ = β + iγ run over nontrivial zeros of ζ with multiplicity m_ρ. For 0 ≤ T1 < T2:
- N(T1,T2) := Σ m_ρ over T1 < γ ≤ T2 (with multiplicity)
- N0^s(T1,T2) := #{ρ : β = 1/2, m_ρ = 1, T1 < γ ≤ T2} (simple, on line)
- d := number of test functions in the family V (≈ λ₁ N(T,2T)); Ĝ := the (4.4) compression.

**Target (user goal, "probability 1")**: `lim_{T→∞} N0^s(0,T)/N(0,T) = 1`.

## 2. Completion criteria and outcome

| Criterion | Content | Status |
|---|---|---|
| C1 (O1) | Re-derive `N0^s + o(N) ≥ 4trĜ − 2N − ‖Ĝ‖²_F = (2 − R(ψ))N`; constants R(ψ0)=4/3, R(ψ_MT)=1/c₁*; H_MT = 3/2 − (1/√2)cot(1/√2) = 0.67250…; cross-check vs v2 §7.1 and Lean `Zeta23.ThmD`. | **DONE** (proved; confirmed vs text + Lean HD_one/closed forms) |
| C2 (O5-D2) | Exact definition of HL*(k0,λ): which k, windows, uniformity, normalization, meaning of o(1). | **DONE** (§2 of candidate_proof.md) |
| C3 (O5-D3) | Prove Christoffel/SOS higher-moment n₊-bound and the Prop 4.5 (P1,Q′)-regrouping corollary. | **DONE** (§3, with new rigorous SOS-witness Lemma 3.A and Christoffel Lemma 3.B) |
| C4 (O5-D4) | Verify m_k(1) (1,3/4,2,13/4); compute Λ_2(0); resolve 13/18 normalization gap exactly. | **DONE** — the written list is INCONSISTENT (m_2=3/4 < m_1²); correct list is **(1,4/3,2,13/4)** (m_2=4/3 exact); under it **Λ_2(0)=5/36** and **13/18=2·(1−5/36)−1** hold exactly (§4) |
| C5 (O5-D5) | `HL* ∀k0` ⇒ `liminf N0^s/N = 1`, incl. convergence argument and Christoffel-asymptotics. | **DONE** — proved conditional on the clean Spectrum Lemma **SL** (0 in the support of the sine-kernel Gram spectral distribution); SL identified precisely as the single missing-in-literature fact (§5) |
| C6 (O5-D6) | Reconcile with GLSS25 (PCC full-support ⇒ 100%) and with the k=1 barrier (§7.2(e)). | **DONE** (§6) |

## 3. Honest status

**RIGOROUS_PARTIAL_RESULT.** The "probability-1" goal is:
- **proved conditionally** on the precise hypotheses **HL*** (all k0, λ→1) **and** the clean
  spectral lemma **SL**;
- **not reached unconditionally** (liminf N0^s/N → 1 remains OPEN; best unconditional ~2/3,
  bandwidth-one ceiling ≈ 0.6818).

The paper's informal §7.2(f) is found to contain exactly one transcription error (m_2(1): 3/4
→ 4/3); the corrected statement is fully consistent and all quoted derived numbers
(Λ_2(0)=5/36, 13/18) are then exact.

## 4. Key sources & hashes (re-verified this run)

- Claude v2 paper PDF `literature/raw/claude-paper-main-v2-20260813.pdf`
  sha256 `6792988E6CD0E17690621CE898ABD5D534F98407741BC7CB14BBE7D07C77D72F`
- Claude v2 text `literature/raw/claude-paper-main-v2.txt` sha256 `9B02E53C31D7926CF584BEC2BADE8FEACFE17633EE9D4705521EB6D47D902432`
- Claude note `literature/raw/claude-paper-note.txt` sha256 `69BDFCE6E53F691D965F3C4D4AAA1536B2BEA3DEBCD68E3BAA25DDA142ACD984`
- GS 2025 `literature/raw/gs-2511.20059.txt` sha256 `65A87EA32D6C2CB70DC3EC39E9304DFA79F73805C6E30EDBFD52ED3F749BC3F0`
- Lean snapshot `literature/raw/zeta-23-lean/` (commit 3635e74826a4c1fcece7d1cd2b6fa75e43a00510), ThmD in `Zeta23/ThmD/Final.lean`, `Endgame.lean`, `Mult.lean`.
- GLSS25: arXiv:2503.15449 (statement as quoted in `gs-2511.20059.txt` Theorem 5).

Full artifact list and input/output hashes in `repro_manifest.md` and `SHA256SUMS`.
