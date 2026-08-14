# Problem Contract — Independent audit of the OpenAI/GPT-5.6 draft (0.673008528)

Run: `R-20260814T041219Z-oaidraft-7c3e73` (focused OpenAI-draft audit, obligations O2 + O7 of packet
`agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md`).
Skill: `rigorous-open-math-research` (Phase 8 adversarial proof audit, Phase 12 reporting).

## Object under audit

The repository `literature/raw/zeta-simple-zeros/` (task bookkeeping commit `040c5e8`; local
copy has no `.git` — history stripped at project snapshot time). It claims, via `paper/riemann.pdf`
and `paper/riemann.tex`, the theorem

```
liminf_{T→∞}  N0^s(T,2T)/N(T,2T)
   ≥  (1,345,000·H_MT − 2,680) / 1,340,003  =  0.6730085279277797613…
```

where `H_MT = 3/2 − (1/√2)·cot(1/√2) = 0.6725007036794116457…`, via a *stability refinement of
the rank–trace inequality* with `D(M) = tr Ψ(M)`, `Ψ(t) = (t−1)²` on `[0,2]`, `2t−3` on `[2,∞)`
(Lemma 2.1, Corollary 2.2), a 3-consecutive-zeros bound (eps4 ≥ 221/10^6 → 67.2519767%) and a
7-consecutive-zeros bound (six-variable `F6 ≥ 19/5000` → 67.3008528%), with an Arb interval-arithmetic
verifier (`src/`, `zeta-zero-verify three|seven`) and recorded certificates.

## Counting functions (exact, per paper [1] §1.3 and Lean `Zeta23.Statement`)

- `N(T1,T2)` := zeros with `T1 < γ ≤ T2`, counted with multiplicity.
- `N0s(T1,T2)` := simple, on-line zeros (`β=1/2, m_ρ=1`) in `(T1,T2]`, each distinct point counted once.
- (also `N0*`, `Nd` for context; not the target.)

Target statement is for the **dyadic** interval `[T,2T]`, `T→∞`.

## Completion / verification criteria (what "pass" means)

Every claim of the draft is re-derived from first principles against source [1]
(`literature/raw/claude-paper-main-v2-20260813.pdf`, `.txt`) and the Lean snapshot
(`literature/raw/zeta-23-lean/`), specifically:

1. Lemma 2.1 (stability rank–trace, `D(M)=tr Ψ(M)`) — full analytic proof.
2. Corollary 2.2 — full proof; correct use of Theorem-D estimates and tail removal.
3. Lemma 3.1 (Montgomery–Taylor overlap-kernel limit) — correctness and uniformity.
4. Proposition 4.1 `F6 ≥ 19/5000` — computer-assisted; verify exhaustiveness + reproduce certificate.
5. Lemma 4.2, 4.3 (block energy, tr Ψ(G) bound) — full proofs.
6. §5 shifted-block pinching → eq (21) → Theorem 1.1 constant — full derivation.
7. The analytic estimates imported from Theorem D: exactly `tr Ĝ = N(1+o(1))`,
   `‖Ĝ‖²_F = (1/c1* + o(1))N`, `2 − 1/c1* = H_MT` — check against Lean `ThmD.Mult.thmD₀_simple_mult`.
8. The two new inequalities are actually proved (analytically / finite-computationally), not heuristic.
9. Bibliographic IDs CCLM17, CGdL20, BHB13, PRZZ20, Wu15, GS25/26 resolved as used in [1].

A refutation must localize the first erroneous step (category: statement/proof/dependency/boundary).
Numerical certification is evidence, not proof, unless it is a finite verification of a universally
quantified bound (state which).
