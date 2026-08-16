# Task packet Q-20260814-criticalline-p1-507bb5

- **Task ID:** `Q-20260814-criticalline-p1-507bb5`
- **Project ID:** `MRP-20260814-riemann-critical-line-c13b8d`
- **Task type:** solve
- **Task state:** `READY`
- **Required run location:** `runs/rigorous-open-math-research/R-20260814T041219Z-mainpush-3cdc81`
- **Created:** `2026-08-14T04:20:00Z` · B0 preflight complete

**User request (verbatim intent)**: 搜索最近 Anthropic 和 OpenAI 推进黎曼猜想的论文，参考这些以及其他方法，尝试将黎曼猜想的结果做到"点在目标直线的概率为 1"（即临界线上零点比例 → 1）。

## 1. Problem statement (contract — to be rebuilt and audited by the solver)

Let ρ = β + iγ run over the nontrivial zeros of ζ, m_ρ the multiplicity. For 0 ≤ T1 < T2:

- N(T1,T2) := Σ m_ρ over T1 < γ ≤ T2 (with multiplicity)
- N0(T1,T2) := Σ m_ρ over on-line zeros (β = 1/2), with multiplicity
- N0*(T1,T2) := #{ρ : β = 1/2, T1 < γ ≤ T2} (distinct)
- N0^s(T1,T2) := #{ρ : β = 1/2, m_ρ = 1, T1 < γ ≤ T2} (simple, on line)
- Nd(T1,T2) := #{ρ : T1 < γ ≤ T2} (distinct)

**Target statement (the user's goal)**: `lim_{T→∞} N0(0,T)/N(0,T) = 1` — equivalently, with
probability 1 (in the proportion sense), a zero of ζ lies on the critical line.
Known to be OPEN as of 2026-08-14. No unconditional result reaches 0.69; bandwidth-one
certificates are capped at ≈ 0.6819; 100% is known to follow from deep conjectures
(pair-correlation conjecture with full support [GLSS25]; HL*(k0) for all k0 [Claude §7.2(f)]).

**Deliverable hierarchy** (any of these is an acceptable run outcome, with an honest status label):
1. An unconditional improvement of the current best lower bounds:
   - liminf N0^s(T,2T)/N(T,2T) ≥ 0.6730085279277... (OpenAI draft — currently UNVERIFIED),
   - liminf N0*/N ≥ 0.6725007..., liminf Nd/N ≥ 0.83625... (Claude, Lean-verified),
   or any other proportion constant (N0/N, N0*/N, Nd/N).
2. An independent verification or refutation of the OpenAI draft constant (its own theorem
   "liminf ≥ 0.6730085279277797613" and the 3-point/7-point sub-claims).
3. A rigorous conditional theorem: under a precisely stated hypothesis (HL*(k0), or PCC full
   support), proportion = 1; or a precise reduction proving "N0/N → 1 ⟺ <named conjecture>".
4. An exact obstruction report: why proportion 1 is unreachable by the known methods
   (bandwidth-one ceiling, k = 1 moment barrier, ghost configuration), with citations.

## 2. Completion criteria

- Status label from the rigorous-open-math-research output protocol; numerical evidence never
  labeled as proof.
- Every obligation O1–O8 below either discharged by proof/verification or recorded as an exact
  open gap with its failure mechanism.
- The user's "probability 1" goal explicitly addressed: either achieved (extraordinary claim,
  requires deep new input + audit), reduced to a named conjecture, or blocked with exact reasons.

## 3. Sources (paths, hashes — verified 2026-08-14)

| Source | Local path | Hash / commit |
|---|---|---|
| Claude paper v1 (2026-08-11) + text | literature/raw/claude-paper-main.pdf (+ .txt) | sha256 19F827BE…E7E814 |
| Claude paper v2 (2026-08-13, preferred) + text | literature/raw/claude-paper-main-v2-20260813.pdf (+ .txt) | sha256 6792988E…77D72F |
| Claude expert note | literature/raw/claude-paper-note.pdf (+ .txt) | sha256 45E0330A…7DDF759D |
| Claude appendix (process) | literature/raw/claude-appendix.pdf | sha256 271ABA2D…91DD2D |
| E2 transcript | literature/raw/claude-extra.pdf | sha256 EBB34C5E…0123ADA |
| Anthropic blog | https://www.anthropic.com/research/riemann-zeta | — |
| Lean formalization snapshot | literature/raw/zeta-23-lean/ | commit 3635e74826a4c1fcece7d1cd2b6fa75e43a00510 (Lean v4.33.0-rc2, Mathlib 51e6992) |
| OpenAI/GPT-5.6 Sol draft repo (incl. paper/riemann.pdf, docs/, src/ verifier) | literature/raw/zeta-simple-zeros/ | commit 040c5e899e658aed7b56a2a87f501798fe10761d |
| Goldston–Suriajaya 2025 | literature/raw/gs-2511.20059.pdf (+ .txt) | sha256 7B4F638C…3ED4C6F; arXiv:2511.20059 |
| Aryan 2019 | arXiv:1902.05473 | external |
| BGSTB 2023 | arXiv:2306.04799 | external |
| BGSTB 2025 | arXiv:2501.14545 | external |
| GLSS 2025 (PCC) | arXiv:2503.15449 | external |
| Literature map / B0 | literature/maps/FRONTIER.md | project git |

Re-check every cited classical result (Sel42, Lev74, HB79, Con89, BCY11, Fen12, PRZZ20, Wu15,
Mon73, Mon75, CGG98, CG93, BHB13, CGdL20, CCLM17, RS96, MV74, Bom00, GS25/26, GLSS25) against
its original source before relying on it; record `query -> result -> locator` for each. CCLM17
and CGdL20 identifiers must be resolved to exact bibliographic data.

## 4. Obligations checklist (to be refined into the run's obligation graph)

- O1 — Theorem D baseline: re-derive the Montgomery–Taylor window constant
  H_MT = 3/2 − (1/√2)·cot(1/√2) = 0.672500703679…, i.e. R(ψMT) = 1/c1, c1 = 0.75329…, and the
  chain (1.2): N0^s + o(N) ≥ 4tr G̃ − 2N − ‖G̃‖²_HS = (2 − R(ψ))N. Confirm against v2 text and
  the Lean snapshot (Zeta23.ThmD).
- O2 — OpenAI draft verification: Lemma 2.1 (stability-enhanced rank–trace inequality with
  D(M) = tr Ψ(M), Ψ(t) = (t−1)² on [0,2], 2t−3 on [2,∞)); Corollary 2.2; Theorem 1.1 constant
  (1,345,000·H_MT − 2,680)/1,340,003; the 3-point inequality (ε4 ≥ 221/10⁶) and the 7-point
  six-variable bound (≥ 19/5000); run the repo verifier (zeta-zero-verify three / seven) and
  record certificates; check every use of "analytic estimates of Theorem D in [1]" against the
  actual theorem.
- O3 — Improvement attempt: does the stability refinement extend to more than 7 consecutive
  zeros / better Ψ / different windows (e.g. ψ0 vs ψMT vs quartic)? Any constant > 0.673008528
  with a full proof is a new record. Check whether the OpenAI certificate class escapes the
  bandwidth-one ceiling 0.6818 (it uses gap-dependent inner products); if it does, compute the
  actual ceiling of the extended class.
- O4 — "Probability 1": attack liminf N0/N = 1 directly. Known obstructions: §7.2(f) (HL*
  route), GLSS25 (PCC route), bandwidth-one ceiling, k=1 moment barrier. Attempt a proof, a
  precise reduction, or an exact obstruction statement.
- O5 — Conditional theorem (HL* route): make §7.2(f) rigorous: define HL*(k0) precisely
  (tr G̃^k = d·m_k(1)(1+o(1)), m_k(1) the sine-kernel Gram moments; verify m_1..m_4 = 1, 3/4, 2,
  13/4); prove liminf N0^s/N ≥ 1 − Λ_m(0) from moments k ≤ 2m (Christoffel-function bound,
  extending Lemma 3.2), HL*(4) ⇒ 13/18, and all-k0 ⇒ 1.
- O6 — Numerical corroboration (evidence only): proportions of simple on-line zeros in actual
  computed zero tables (e.g. up to height ~10⁶–10⁷, using the ainta verifier data or zeta
  computations) — labeled NUMERICAL_EVIDENCE, never proof.
- O7 — Literature integrity: resolve CCLM17, CGdL20, BHB13, PRZZ20, Wu15, GS25/26 exact
  bibliographic data + statements; confirm GLSS25's full-support ⇒ 100% theorem.
- O8 — Honest reporting: status label, artifact hashes, open obligations, handoff-quality
  ledger.

## 5. Verification criteria

- Every claimed theorem: full proof with all steps; adversarial audit (independent re-derivation).
- Numerical claims: reproducible commands + certificates (Arb interval arithmetic where claimed).
- No RH or unproven conjecture used inside an "unconditional" claim.
- Status labels from the output protocol; "probability 1" claimed only with complete proof.

## 6. Constraints

- No RH assumed for unconditional results. No mollifier/zero-density/zero-free-region shortcuts.
- Numerical evidence is never a delivery.
- The user's goal must be addressed explicitly in the final report (achieved / reduced / blocked).
- Do not modify the Anthropic Lean snapshot; extend in a new directory if formalizing.

## 7. Run roots (one per concrete task)

- R-20260814T041219Z-mainpush-3cdc81 — main push: verify OpenAI draft (O2) + improve constants (O3) + probability-1 attack (O4) + numerical corroboration (O6).
- R-20260814T041219Z-oaidraft-7c3e73 — focused independent audit of the OpenAI draft (O2 + O7), solver and auditor roles.
- R-20260814T041219Z-condp1-698ec7 — conditional "probability 1" (O5 + O4-conditional + O1 baseline check).

Standard upstream artifacts (problem_contract.md, repro_manifest.md, status_and_literature.md,
obligation_graph.md, approach_registry.md, research_ledger.md, counterexample_log.md,
candidate_proof.md, audit_report.md, reproducibility/) are written by the solver under the run
roots; the manager records paths and hashes only.

## Novelty preflight (B0)

- **Openness verdict:** `OPEN` (checked 2026-08-14): "N0/N → 1" is open; "N0^s/N ≥ 2/3" was proved
  2026-08 (Anthropic); "N0^s/N ≥ 0.673008528" is an unverified 2026-08-13 draft (OpenAI). Any
  unconditional c > 0.673008528 (or a verified proof of that constant) is novel.
- **Novelty audit path:** `literature/maps/FRONTIER.md` §1–§2 (divergent search log with
  query → result → locator; exact known theorems; barrier list; excluded crank noise).
- **Snapshot hash:** `sha256:31A82F8DB77004DE7E92A7C19B6E30897C8387A6A6BD7B4E53A2D93E3F7F7C42`
  (content hash of the B0 artifact literature/maps/FRONTIER.md, refreshed 2026-08-16 after
  the independent third-party audit of the 0.00392 record (PASS-WITH-LIMITS,
  reports/independent-audit-00392.md); previous hash 94F920E5… recorded after the SL run
  ingestion and k-family feasibility update; knowledge base empty at dispatch, no
  accepted-knowledge
  dependencies; dispatch commit recorded per run's repro_manifest).
- **Backfill:** literature/maps/FRONTIER.md refreshed 2026-08-14; index/papers.json has 7
  registered papers; novel-risk line in FRONTIER.md §3.

## Source bundle

| Item | Title | Path | Expected hash |
|---|---|---|---|
| Claude v2 | paper (2026-08-13, preferred) | literature/raw/claude-paper-main-v2-20260813.pdf | 6792988E6CD0E17690621CE898ABD5D534F98407741BC7CB14BBE7D07C77D72F |
| Claude v1 | paper (2026-08-11) | literature/raw/claude-paper-main.pdf | 19F827BEE5834D61AA6DD756CDAEA582492703DDBFD6BDC2058DE10B93F7E814 |
| Claude note | expert note | literature/raw/claude-paper-note.pdf | 45E0330AD37965E5531FA1F4F11E5BEBCAE147A5237A3E5B3D029EFA7DDF759D |
| Claude appendix | process appendix | literature/raw/claude-appendix.pdf | 271ABA2D2083FFA778A53C2994F2061FAD7FDDA450BC296EC49C7CC41E91DD2D |
| Claude E2 | subagent transcript | literature/raw/claude-extra.pdf | EBB34C5ED65B1DC96A72BDF76068814A34DA9CEB1675624F68A2088180123ADA |
| Lean snapshot | anthropics/zeta-23-lean README | literature/raw/zeta-23-lean/README.md | 8FC084A9A51F824FB2A87D7E9C8C20C4DA7A7F6E28A6257473C18276C3C763E4 |
| OpenAI draft | ainta/zeta-simple-zeros README | literature/raw/zeta-simple-zeros/README.md | 9B6EE0DFCE62CA15854B8C544E27DD13397F5EE0399E5CAAA66E5CC1DA0C6631 |
| GS 2025 | Goldston–Suriajaya | literature/raw/gs-2511.20059.pdf | 7B4F638CBD0438123B7A54869FC998FC3D4DEE9B74572C04CEF9DA0463ED4C6F |
| Aryan 2019 | Landau–Gonek extension | https://arxiv.org/abs/1902.05473 | external |
| BGSTB 2023 | pair correlation no RH | https://arxiv.org/abs/2306.04799 | external |
| BGSTB 2025 | proportions I | https://arxiv.org/abs/2501.14545 | external |
| GLSS 2025 | PCC simple/critical | https://arxiv.org/abs/2503.15449 | external |


## Required run location

runs/rigorous-open-math-research/R-20260814T041219Z-mainpush-3cdc81 (primary; companion runs:
R-20260814T041219Z-oaidraft-7c3e73 for the focused OpenAI-draft audit, R-20260814T041219Z-condp1-698ec7
for the conditional probability-1 theorems). Write the standard upstream artifacts there.

## Upstream invocation

```text
Use $rigorous-open-math-research on the concrete problem in TASK_PACKET_PATH
(agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md).
Treat the task packet as project context, not as a verified theorem contract.
Rebuild and audit the exact problem statement and recheck every cited theorem
against its original source. Write the standard upstream artifacts under RUN_ROOT.
Return the upstream result status and artifact locations without changing its protocol.
```

## History

- 2026-08-14: packet created from user request; sources downloaded & hashed; B0 complete.
