# Problem Contract — f_9 pressure certificate push (R-20260814T131528Z-f9push-d3b58c)

Run: `R-20260814T131528Z-f9push-d3b58c`
Task packet: `agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md` (obligation O3).
Skill: `rigorous-open-math-research`; executed directly by the project manager (subagent
attempts d15fd204 failed without artifacts; manager-level execution with full audit trail).

## 1. Normalized goal

Raise the certified k=9 pressure constant from f_9 = 39/10000 = 0.0039 to
f_9 = 0.00395 (primary) or 0.00398 (stretch), i.e. certify

    F_8(g_1,…,g_8) ≥ f_9   for all g_i ≥ 0

where F_8 is the k=9 pressure function of the general-k chain (extpress run
R-20260814T045000Z-extpress-2f36ae, candidate_proof.general-k-derivation.md),
with a finite universally-quantified Arb certificate (exhaustive branch-and-bound,
grid 4000, 128-bit, reusing the validated verifier verify_kpoint_parallel.py).

If certified, the record becomes

    liminf N0^s(T,2T)/N(T,2T) ≥ C_9(f_9) with
    f_9 = 0.00395 → C_9 = 0.67308556213350404907 (n=253, m=261, A_0 = 0.99935 < 1)
    f_9 = 0.00398 → C_9 = 0.67310463444279257596 (n=251, m=259, A_0 = 0.99898 < 1)
(manager-computed; A_0 < 1 rigor condition verified for both).

## 2. Completion criteria

- C1: certificate for f_9 = 0.00395 (grid 4000) with recorded kernel/second-derivative
  table hashes, node counts, surviving components; verified=true.
- C2: baseline re-run of f_9 = 0.0039 (grid 4000) reproduces the extpress certificate
  (kernel hash 7029ac0f…) — the independent full re-run recommended by the audit.
- C3 (if C1): updated record theorem with the general-k chain; A_0 < 1 check;
  manager arithmetic re-verification.
- C4: honest reporting; if 0.00395 not certified within budget, exact failure mechanism
  (node counts, remaining boxes, pruning shortfall) as BLOCKED_REDUCTION/FINITE_COMPUTATIONAL_RESULT.

## 3. Sources & hashes

- Extpress run (chain + verifier + certificates): runs/…/R-20260814T045000Z-extpress-2f36ae/
  (kernel hash 7029ac0f1f6f869fb28320c7e6ccb85d8f9d06b4ea4cdb577544a0833831eef5;
  second derivative 26715cd56ad6749da44654e793f2bfa6b3f02130bc154ec0bb0c04bb33f294e1;
  nodes 53,137,290; grid 4000; 128-bit).
- Inputs: Lean Theorem D (zeta-23-lean@3635e748), OpenAI Lemma 2.1/Cor 2.2
  (zeta-simple-zeros@040c5e8), audited mainpush/oaidraft runs.

## 4. Constraints

- Unconditional claims only via the audited input chain; novelty confined to the
  certificate. Numerical scoping (true min ≈ 0.00398) is evidence only.
- Long computations acceptable (machine: 22 logical cores; baseline ≈ 58 min at 22 workers).

## 5. History

- 2026-08-14 13:15Z: run created; subagent attempt failed; manager took over.
- 2026-08-14 13:25Z: baseline re-run (f=0.0039, grid 4000) launched (background job).
