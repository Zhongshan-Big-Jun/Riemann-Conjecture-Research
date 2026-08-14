# Riemann-Conjucture-Research

**黎曼猜想：临界线上零点比例攻关** — Proportion of zeros of the Riemann zeta function on the critical line

> Research program (DSH `math-research-workflow` pipeline: manage → rigorous research → audit).
> Status: **active**. Latest unconditional world record:
> **liminf N₀ˢ(T,2T)/N(T,2T) ≥ 0.6730536459525899252…** (C₉, 2026-08-14, this project).

## The problem

Let ρ = β + iγ run over the nontrivial zeros of ζ, N(T₁,T₂) count zeros with multiplicity,
and N₀ˢ(T₁,T₂) count **simple zeros on the critical line Re s = 1/2**. The project pushes the
unconditional lower bound on `liminf N₀ˢ(T,2T)/N(T,2T)` toward 1 ("probability 1 on the
critical line" — the user goal), and reduces the full goal to precise conjectures.

## Current records (unconditional, ζ)

| Constant | Lower bound for liminf N₀ˢ(T,2T)/N(T,2T) | Source |
|---|---|---|
| 2/3 | 0.6666… | Claude/Anthropic 2026 (Lean-verified) |
| 0.6725007036… | 3/2 − (1/√2)cot(1/√2), Montgomery–Taylor window | Anthropic Thm D |
| 0.6730085279… | 7-point pressure stability refinement | OpenAI/GPT-5.6 Sol draft (independently audited here) |
| **0.6730536459…** | **(6875·H_MT − 1315/96)/6849, k=9 pressure certificate F₈ ≥ 39/10000** | **This project (extpress run)** |

Distinct zeros: N_d/N ≥ 5/6 (0.83625… with MT window). Zeros of ξ′: 0.86864 simple on line
(quartic window). Bandwidth-one certificate class ceiling: ≈ 0.6818 (Lean-certified).

## "Probability 1" status (honest)

- **Unconditionally OPEN.** Exact obstructions: bandwidth-one ceiling ≈ 0.6818 (ghost
  256-periodic configuration); pressure-class ceilings ≈ 0.6731 (k=9) and beyond; higher trace
  moments unavailable at X ≍ T (Rudnick–Sarnak kλ<2 range).
- **Conditionally reachable:** PCC with full support ⇒ 100% (GLSS25, arXiv:2503.15449);
  HL* (all trace moments = sine-kernel Gram moments) + Spectral Lemma SL ⇒ 100% (proved in
  this project, ε-form/iterated limit; condp1 run). The Anthropic paper §7.2(f) contains one
  transcription error (m₂: 3/4 → 4/3), resolved exactly here (Λ₂(0) = 5/36, 13/18).

## Repository structure

```
literature/   sources (Anthropic v1/v2/note, OpenAI draft, GS, Lean snapshot), FRONTIER.md (B0 audit trail)
runs/         rigorous-open-math-research/R-*/ — per-run standard artifacts, Arb certificates, scripts
reports/      manager-level independent verifications
index/        papers / runs / artifacts / task-packets registries
agenda/       directions, priorities, task packet (contract + B0 novelty preflight)
state/        RESUME.md, current.json, activity log, stage summaries
```

## Reproducibility

- All artifacts hash-bound (sha256 recorded in SHA256SUMS / repro_manifest per run).
- Arb certificates: `verify_kpoint_parallel.py 9 39/10000 --grid 4000 --precision 128 --workers 22`
  (Python 3.10, python-flint/Arb 0.9.0); k=7 validation reproduces the field-accepted
  certificate byte-identically (kernel hash a9992300…).
- Pipeline gate: `validate_pipeline.py --project .` (0 problems at stage close).

## Recent activity

- 2026-08-14: stage B close; new record C₉ = 0.673053646 (k=9 certificate, 53,137,290 nodes);
  independent audits PASS (OpenAI draft ×2, condp1 PASS-CONDITIONAL + F-1 repair);
  manager-level audit PASS-with-limits for C₉; repo synced to GitHub.
- Next: push f₉ toward 0.00395–0.00398 (C₉ ≈ 0.673086–0.673105); k=11 scoping; SL lemma;
  window-generalized pressure method.
