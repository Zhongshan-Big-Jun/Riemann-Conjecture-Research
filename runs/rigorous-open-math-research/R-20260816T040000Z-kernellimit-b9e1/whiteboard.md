# Whiteboard — R-20260816T040000Z-kernellimit-b9e1 (kernel-limit lemma, T1c-3)

- **Run ID:** `R-20260816T040000Z-kernellimit-b9e1`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5`
- **Last updated:** `2026-08-16T04:10:00Z`

## Current plan

RUN COMPLETE (analysis level): derive and prove the kernel-limit lemma (T1c item 3) with an
exact Lean-ready statement, resolving the normalization against the snapshot's Gram-entry
definitions. Result: with L = λ·log(T/2π), MT window φ(u) = √cos(√2λu/L)·ϱ((L/2−|u|)/w), atoms
v_γ = φ·e^{iγu}, x = (γ−γ′)·L/(2π): |⟨v_γ,v_γ′⟩/L − K_λ(x)| ≤ 2w/L uniform in x; the ratio
→ K_λ(x)/K_λ(0) = kMT(x) at rate O(w/L); K_1/K_1(0) = kMT EXACTLY (matches Chain9 + Arb).
Next step (not part of this run): Lean formalization of the lemma (lean-verify role).

## Route history

- Normalization resolution `[SUCCEEDED]`: pinned the overlap to the snapshot's Gram-entry
  definition (Defs.lean Gsummand/Gentry, atoms v_γ = φe^{iγu}); x = (γ−γ′)·L/(2π);
  L = λ·log(T/2π).
- Uniform estimate `[SUCCEEDED]`: |F_L(x) − K_λ(x)| ≤ 2w/L (ramp = 1 on |t| ≤ 1/2 − w/L;
  discrepancy set has measure 2w/L).
- Kernel identity `[SUCCEEDED]`: K_1(x) = ½[sinc(1/√2−πx) + sinc(1/√2+πx)] (product-to-sum,
  removable singularities), K_1(0) = √2 sin(1/√2), so kMT = K_1/K_1(0) exactly.
- Cfun-framing correction `[SUCCEEDED]` (important): Cfun (Window.lean:1211) is the profile
  AUTOCORRELATION (J-moment object; phase √2λy/L u-independent; normalized limit is
  x-independent, verified numerically), NOT the beat-frequency overlap; the correct kernel
  object is the Fourier overlap (φ²)̂(γ−γ′).
- Numerical verification `[SUCCEEDED]` (evidence): mpmath 40-digit; ratio converges with
  err·L ≈ const (x=0.3→2.4, x=1.0→9.4, x=1.9→8.9), confirming the O(w/L) rate.
- Lean formalization `[BLOCKED — budget]`: analysis-level only; the §3 statement is ready
  for a follow-up lean-verify run.

## Ideas to return to

- Tight uniformity constant for the ratio on a bounded x-range (C₉ only needs λ=1).
- The λ-family version (0 < λ ≤ 1) for the ξ′/conditional chain (same proof, K_λ(0) = √2 sin(λ/√2)).

## Open obligations

- Lean formalization of the kernel-limit lemma (T1c-3 bridge) — statement pinned; proof
  complete at analysis level.
- T1c-1/T1c-2 (stability_eps, stability_averaged_eps for the true Δ(M°)) unchanged.
- T2 certificate reflection unchanged.

## Key artifacts

- `runs/.../kernellimit-b9e1/problem_contract.md` — exact statement + normalization resolution.
- `runs/.../kernellimit-b9e1/candidate_proof.md` — full derivation (Eq. 1–4) + Cfun distinction.
- `runs/.../kernellimit-b9e1/numerical_evidence.md` + `reproducibility/kernel_limit_verify.py`,
  `ramp_rate_verify.py` — O(w/L) verification (evidence).
- `runs/.../kernellimit-b9e1/SHA256SUMS` — hash-bound artifacts.
