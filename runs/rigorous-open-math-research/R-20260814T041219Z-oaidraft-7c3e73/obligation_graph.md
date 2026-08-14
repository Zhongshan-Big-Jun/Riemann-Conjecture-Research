# Obligation graph — OpenAI draft audit

Node → dependency → proof status. Root = Theorem 1.1 (target). All leaf obligations closed.

## Root
- **T01** `liminf N0^s(T,2T)/N(T,2T) ≥ (1,345,000·H_MT−2,680)/1,340,003 = 0.673008528` — **PROVED** (this audit). Depends on T02–T05.

## Path (draft §1→§5)
- **T02** Base bound `N0^s ≥ H_MT·N − o(N)` and constants `trĜ=N(1+o(1))`, `‖Ĝ‖²_F=(1/c1*+o(1))N`, `2−1/c1*=H_MT`.
  - Source: [1] Theorem D + §7.1; Lean `ThmD.Mult.thmD₀_simple_mult`. — **VERIFIED** (matches Lean exactly).
- **T03** Lemma 2.1 stability rank–trace, `D(M)=trΨ(M)`. — **PROVED** (von Neumann + convex min; §2.2 of audit).
- **T04** Corollary 2.2 `N0^s ≥ H_MT·N + D(M°) − o(N)` (tail removal + pinching `D(M)≥D(M°)`). — **PROVED**.
- **T05** Uniform positive lower bound `D(M°) ≥ (4997/1,345,000)N0^s − (268/134,500)N − o(N)`.
  - Depends on T06 (kernel), T07 (Prop 4.1), T08 (Lemmas 4.2/4.3), T09 (pinching/averaging).
- **T06** Lemma 3.1 overlap-kernel limit `⟨v_i,v_j⟩ = k(x_i−x_j)+o(1)` uniform. — **PROVED** (via [1] Lemma 2.2, Lemma 5.4; §2.4).
- **T07** Prop 4.1 `F6 ≥ 19/5000` ∀ nonneg gaps. — **PROVED** finite & universally quantified (Arb); **CERTIFICATE REPRODUCED**.
- **T08** Lemmas 4.2, 4.3 (block energy; `trΨ(G) ≥ min(1,2Σ|G_ij|²)`). — **PROVED**.
- **T09** Shifted-block pinching + m-offset averaging + RvM `x_{S°}−x1 = N+o(N)`. — **PROVED**.
- **T10** Final algebra `(1−4997/1345000)S° ≥ (H_MT−268/134500)N` → constant. — **PROVED** (high-precision arithmetic check).

## Leaf / supporting
- **Bibliographic IDs** CCLM17, CGdL20, BHB13, PRZZ20, Wu15, GS25, GS26 — **RESOLVED** (as used in [1]; see status_and_literature.md).
- **Computational inputs** — 3-point `eps4≥221/1e6` (verified=reproduced), 7-point `F6≥19/5000` (verified=reproduced).
- **Sharpness / equality** — base equality case mutually-orthogonal simple vectors ([1] §7.5(b)); new inequalities fully proved, constant below method ceiling ≈0.68185.

## Status
All leaves **closed**; no open obligations. Verdict `PASS` / `INDEPENDENTLY_AUDITED_PROOF`.
