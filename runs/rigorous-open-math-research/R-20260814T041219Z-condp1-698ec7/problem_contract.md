# Problem Contract — Conditional probability-1 (HL* trace-moment route)

Run: `R-20260814T041219Z-condp1-698ec7`
Task packet: `agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md` (obligations O5, O4-conditional, O1 baseline check).
Skill: `rigorous-open-math-research`. Status target: `RIGOROUS_PARTIAL_RESULT` or better.

## 1. Normalized goal statement

Let ρ = β + iγ run over nontrivial zeros of ζ, m_ρ the multiplicity. For 0 ≤ T1 < T2:

- N(T1,T2) := Σ m_ρ over T1 < γ ≤ T2 (with multiplicity)
- N0^s(T1,T2) := #{ρ : β = 1/2, m_ρ = 1, T1 < γ ≤ T2} (simple, on line)

**Target (user goal, "probability 1")**: `lim_{T→∞} N0^s(0,T)/N(0,T) = 1` (100% simple zeros on the line).

This run makes the informal §7.2(d),(e),(f) statements of the Anthropic paper
(`literature/raw/claude-paper-main-v2-20260813.pdf` / `.txt`, §7.2 lines ~1628–1658) into a
RIGOROUS conditional theorem: from precise hypotheses HL*(k0, λ) on the trace moments of the
d×d compression G~ of Weil's form, prove lower bounds on the proportion of simple on-line zeros,
reaching 1 when all moments are known.

## 2. Completion criteria

- C1 (O1): Re-derive from scratch the baseline chain
  `N0^s(T,2T) + o(N) ≥ 4·tr[Ĝ] − 2N(T,2T) − ‖Ĝ‖²_F = (2 − R(ψ))·N(T,2T)` (Theorem D), and
  confirm statement/constants against v2 §7.1 text and the Lean theorem `Zeta23.ThmD.thmD₀_simple`.
- C2 (task 2): Define HL*(k0, λ) with exact statements: which k, which windows, the uniformity in T
  (and in the window), precise normalisation of G~, and the meaning of "o(1)".
- C3 (task 3): State and PROVE the Christoffel-function bound:
  given trace moments `d⁻¹ tr(Ĝ^k) → m_k(λ)`, k ≤ 2m, the sharp lower bound
  `n₊(G~)/d ≥ 1 − Λ_m(0) − o(1)`, plus the simple-on-line corollary via the P1/Q' regrouping.
  **The informal §7.2(d) statement is NOT true as literally written (see counterexample delta_-1);
  the correct rigorous statement requires the positive-mean (m_1>0) / positive-semidefinite-type
  normalization; this run pins that down.**
- C4 (task 4): Verify m_k(1) for k ≤ 4 = (1, 3/4, 2, 13/4); compute Λ_2(0) = 5/36 hence
  `1 − Λ_2(0) = 31/36`; explain precisely how 13/18 (~0.7222) arises from the simple-on-line
  regrouping (task condition: "check how 13/18 arises").
- C5 (task 5): Prove `HL*(k0, λ) ∀ k0` ⇒ `liminf N0^s/N = 1`, including the convergence argument
  `Λ_m(0) → 0` for the spectral measure of the sine-kernel Gram matrix (identify support / show
  positive density at 0, or prove the needed Christoffel asymptotics).
- C6 (task 6): Reconcile with GLSS25 (PCC full support ⇒ 100% simple on line; GS/GLSS Theorem 5)
  and with the unconditional k = 1 barrier (§7.2(e), RS96 range kλ < 2).

Status is honest: no claim of an unconditional 100% (that is OPEN); deliver a rigorous conditional
theorem with exact hypotheses and exact open gaps.

## 3. Sources & hashes (re-verified this run)

- Claude v2 paper: `literature/raw/claude-paper-main-v2-20260813.pdf` + `.txt` (§7.2(d),(e),(f); §7.1 Thm D; Prop 4.4, 4.5; Lemma 3.2, 3.3).
- Lean snapshot: `literature/raw/zeta-23-lean/` (`Zeta23.ThmD.thmD₀_simple`, `Zeta23.LinAlg.RankTrace`).
- GLSS25: `arXiv:2503.15449`; statement quoted in `literature/raw/gs-2511.20059.txt` Theorem 5.
- Frontier map: `literature/maps/FRONTIER.md` (snapshot `sha256:6145A358...3C9098`).

## 4. Normalization of the compression (unit conventions, from §2 and (4.4))

From the v2 text (§2.1, (2.20), eq (4.2), (4.4)):
- V = {φ(u) e^{iτ_k u}}, τ_k = 2πk/L, 0 ≤ k < d, d ≈ λ1 N(T,2T) (λ1 = L/ℓ1).
- Ẽ := E/L. Ĝ := G/(aL²) are the units (4.4) in which an isolated on-line zero seen through the
  full grid contributes eigenvalue = m_ρ (its multiplicity).
- In these units (unconditionally): tr Ĝ = N(T,2T)(1+o(1)); ‖Ĝ‖²_F = tr Ĝ² = (1/λ1 + λ1/3)·N(1+o(1)).

For the moment route, the correctly-normalised object is the spectral (empirical eigenvalue)
measure of (Ĝ/d)·(d/tr Ĝ)... precise definition in status_and_literature.md and the theorem files.
The trace-moment hypothesis is on `d⁻¹ tr((Ĝ/d)ᵏ)` type objects rescaled so that the first moment = 1.

## 5. Known barrier / open-problem status (must not be contradicted)

- `liminf N0^s(0,T)/N(0,T) → 1` is OPEN. Best unconditional ~2/3 (#2/3, ThmD 0.67250; OpenAI draft 0.673008 unverified).
- Bandwidth-one certificate ceiling ≈ 0.6818287 (Lean-certified `PairCeiling.ceiling_law256`).
- Unconditional higher-moment evaluation `tr Ĝ^k`, k ≥ 2, requires X^k ≤ T^(2−ε) (§7.2(e)); only k=1 unconditionally in the band λ∈(1/2,1). HL* is a *hypothesis*, not a theorem.
- The informal §7.2(d) bound needs a positivity normalization (the literal reading has counterexample delta_-1). See obligation_graph / counterexample_log.
