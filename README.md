# Riemann-Conjecture-Research

**黎曼猜想：临界线上零点比例攻关** — Proportion of zeros of the Riemann zeta function on the critical line

> 🌏 [中文说明 / Chinese README](README.zh-CN.md)

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
| 0.6730856… (pending cert) | (26,100,000·H_MT − 52,000)/26,000,065 at f₉ = 0.00395 | this project (f9push run, certificate running) |

Distinct zeros: N_d/N ≥ 5/6 (0.83625… with MT window). Zeros of ξ′: 0.86864 simple on line
(quartic window); **0.8691835… simple on line with MT window (this project, audited A1–A6,
reports/xi-prime-audit-manager.md)**; 0.8692247… pending the same f₉ certificate. Bandwidth-one
certificate class ceiling: ≈ 0.6818 (Lean-certified).

## "Probability 1" status (honest)

- **Unconditionally OPEN.** Exact obstructions: bandwidth-one ceiling ≈ 0.6818 (ghost
  256-periodic configuration); pressure-class ceilings ≈ 0.6731 (k=9) and beyond; higher trace
  moments unavailable at X ≍ T (Rudnick–Sarnak kλ<2 range).
- **Conditionally reachable:** PCC with full support ⇒ 100% (GLSS25, arXiv:2503.15449);
  HL* (all trace moments = sine-kernel Gram moments) + Spectral Lemma SL ⇒ 100% (proved in
  this project, ε-form/iterated limit; condp1 run). The Anthropic paper §7.2(f) contains one
  transcription error (m₂: 3/4 → 4/3), resolved exactly here (Λ₂(0) = 5/36, 13/18).
  **2026-08-15: the random sine-process Gram model reproduces the full audited moment list
  (1, 4/3, 2, 13/4) EXACTLY** (m₂ = 4/3, m₃ = 2, m₄ = 13/4 — the latter two upgraded from
  MC to exact; DPP simulation confirms end-to-end); SL (Christoffel form) is supported by
  eigenvalue-scaling and Christoffel-decay evidence (Λ_m(0) ≈ 0.32, 0.13, 0.045, 0.023 →
  0) but remains open as a theorem (reports/sl-lemma-random-gram-probe.md).

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
- 2026-08-15: **world record C₉(ζ) = 0.673066472675939665848…, C₉(ξ′) = 0.86920009109661916184…
  CERTIFIED (f₉ = 0.00392, grid-2000, 64,748,524 nodes; all expected values matched);** ξ′
  candidate audited (A1–A6 PASS); 0.00395 target withdrawn as infeasible (true min
  ≈ 0.00395005); AdmWindow cos blueprint complete; conditional 100% theorem moment side
  exact (random-Gram model reproduces (1, 4/3, 2, 13/4)).
- 2026-08-15 (evening): **Stage C progress — O1 baseline machine-verified** (`lake build
  Zeta23` exit 0, 9010 jobs; `#print axioms` = {propext, Classical.choice, Quot.sound} on all
  headline theorems; independent adversarial audit: O1a–O1f FAITHFUL, FORMALLY_VERIFIED);
  **T1 formalizer pass in progress** (lean-proof/Record9/, separate lake project reusing the
  snapshot packages; snapshot untouched); **k=10 scoping done** — inf F₉ ≤ 0.003958083, k-family
  ladder exhausted at the certified C₉ (k=10 offers at most +2.7e-6 at 1–5 days; k=11
  infeasible; only recovered-gain route = exact-arithmetic certifier, cap ≈ +1.5e-5);
  **SL lemma research run dispatched** (R-20260815T120000Z-sllemma-7b21e4).
- Next: collect the T1 formalizer + SL run results, then the independent verifier pass for
  T1 (fresh agent) and T2 (certificate reflection) / T3 (ξ′ AdmWindow); optional premium
  ladder step 0.00393 grid-4000 (borderline, +6.3e-6, 1–2 days — decision after k=10/Stage C
  settle); independent third-party re-audit of the record theorem (packet ready).
