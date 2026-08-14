# Problem Contract — f_9 pressure certificate push (R-20260814T131528Z-f9push-d3b58c)

Run: `R-20260814T131528Z-f9push-d3b58c`
Task packet: `agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md` (obligation O3).
Skill: `rigorous-open-math-research`; executed directly by the project manager (subagent
attempts d15fd204 failed without artifacts; manager-level execution with full audit trail).

## 1. Normalized goal

Raise the certified k=9 pressure constant from f_9 = 39/10000 = 0.0039 to
f_9 = 0.00392 (release target; original 0.00395 WITHDRAWN 2026-08-15 — see
f9-ladder.md CORRECTION: true min of F_8 ≈ 0.00395005, margin ≈ 5e-8 below the
verifier's bound loss ≈ 1e-5, infeasible), i.e. certify

    F_8(g_1,…,g_8) ≥ f_9   for all g_i ≥ 0

where F_8 is the k=9 pressure function of the general-k chain (extpress run
R-20260814T045000Z-extpress-2f36ae, candidate_proof.general-k-derivation.md),
with a finite universally-quantified Arb certificate (exhaustive branch-and-bound,
grid 2000, 128-bit, reusing the validated verifier verify_kpoint_parallel.py;
run pwsh-4 launched 2026-08-15).

If certified, the record becomes

    liminf N0^s(T,2T)/N(T,2T) ≥ C_9(f_9) with
    f_9 = 0.00392 → C_9 = 0.67306647267593966585 (n=255, m=263, A_0 = 2499/2500 < 1)
    (manager-computed; A_0 < 1 rigor condition verified).
    Fallback if the 0.00392 run fails: f_9 = 0.00391 → C_9 = 0.67305992191189169
    (n=255, m=263, A_0 = 0.99705 < 1; exact form (26,300,000·H − 52,400)/26,200,295).

## 2. Completion criteria

- C1: certificate for f_9 = 0.00392 (grid 2000, pwsh-4) with recorded
  kernel/second-derivative table hashes (expected 39a209d3… / 29ca4522…), node
  counts, surviving components (expected [[1868,2458];[3511,30823]]); verified=true.
- C2: baseline re-run of f_9 = 0.0039 (grid 4000) reproduces the extpress certificate
  (kernel hash 7029ac0f…) — SUBSUMED by the 0.00392 certificate (F_8 ≥ 0.00392 ⟹
  F_8 ≥ 0.0039).
- C3 (if C1): updated record theorem with the general-k chain; A_0 < 1 check;
  manager arithmetic re-verification (done: dps=90 exact forms).
- C4: honest reporting; if 0.00392 not certified, fall back to 0.00391; if 0.00391
  also fails, report the exact failure mechanism (node counts, remaining boxes,
  pruning shortfall) as BLOCKED_REDUCTION/FINITE_COMPUTATIONAL_RESULT. (The 0.00395
  failure was reported as such: F-1 loud fail at leaf boxes with bounds
  0.0039314/0.00394017; true min pinned at 0.003950049001339790.)

## 3. Sources & hashes

- Extpress run (chain + verifier + certificates): runs/…/R-20260814T045000Z-extpress-2f36ae/
  (kernel hash 7029ac0f1f6f869fb28320c7e6ccb85d8f9d06b4ea4cdb577544a0833831eef5;
  second derivative 26715cd56ad6749da44654e793f2bfa6b3f02130bc154ec0bb0c04bb33f294e1;
  nodes 53,137,290; grid 4000; 128-bit).
- Inputs: Lean Theorem D (zeta-23-lean@3635e748), OpenAI Lemma 2.1/Cor 2.2
  (zeta-simple-zeros@040c5e8), audited mainpush/oaidraft runs.

## 4. Constraints

- Unconditional claims only via the audited input chain; novelty confined to the
  certificate. Numerical scoping (true min ≈ 0.00395005, corrected 2026-08-15; the
  earlier 0.00398 was a local minimum) is evidence only.
- Long computations acceptable (machine: 22 logical cores; baseline ≈ 58 min at 22 workers).

## 5. History

- 2026-08-14 13:15Z: run created; subagent attempt failed; manager took over.
- 2026-08-14 13:25Z: baseline re-run (f=0.0039, grid 4000) launched (background job).
- 2026-08-15: 0.00395 runs FAILED (loud fail); true min ≈ 0.00395005; contract
  retargeted to f_9 = 0.00392; pwsh-4 (grid 2000) launched; all release artifacts
  prepared (release-checklist, candidate_proof.draft, audit packet + dispatch prompt).
