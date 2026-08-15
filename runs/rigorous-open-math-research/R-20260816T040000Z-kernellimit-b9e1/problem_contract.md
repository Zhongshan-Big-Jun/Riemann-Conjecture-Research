# Problem contract — kernel-limit lemma (T1c item 3, Stage C)

Run: `runs/rigorous-open-math-research/R-20260816T040000Z-kernellimit-b9e1`
Status line: `RIGOROUS_PARTIAL_RESULT` (exact statement derived, analysis-level proof
complete, numerical cross-check passed at O(w/L) rate; Lean bridge not opened here).

## 1. Origin and role

The C₉ record theorem's Lean chain (`lean-proof/Record9/Record9/Chain9.lean`,
machine-accepted, `CERTIFIED_F8_GE`) certifies a k = 9 pressure bound built from the
normalized Montgomery–Taylor overlap kernel

    kMT(x) = [sinc((√2)⁻¹ − πx) + sinc((√2)⁻¹ + πx)] / (2·√2·sin((√2)⁻¹)),
    wMT(x)  = kMT(x)²,

where `sinc 0 := 1`. `CERTIFIED_F8_GE` matches the Arb certificate
`nine-point-f8-gt-392over100000-grid2000.txt`. The Arb certificate *certifies the
kernel inequality F₈ ≥ 392/100000 for this kernel*; it does **not** by itself tie the
physical finite-window atom overlaps to `kMT`. That tie is the **kernel-limit lemma**
(T1c item 3): the finite-window overlap ⟨v_γ, v_γ′⟩ of the simple-zero atoms tends,
in the high-T / window limit, to `kMT(x_γ − x_γ′)` after the same central truncation.

Paper statement being made rigorous (OpenAI `literature/raw/zeta-simple-zeros/docs/proof.md`
§1): *"For bounded normalized separations, the inner products of the simple-zero atoms
satisfy ⟨v_γ, v_γ′⟩ = k(x_γ − x_γ′) + o(1) uniformly after the same central truncation
used in the paper."*

## 2. Objects and definitions (pinned from the snapshot)

Source: `literature/raw/zeta-23-lean/Zeta23/…`

- Window length and grid. `l(T) := log(T/2π)` (`Defs.lean:49`). `Params.L T := λ·l T`
  (`Defs.lean:204`). Grid step `h := 2π/L` (`Defs.lean:213`), grid ordinates
  `τ_k := T + k h` (`Defs.lean:219`). `0 < λ ≤ 1`, ramp width `w` with `1 ≤ w ≤ L/8`
  (§6 takes `w = 1`).
- Montgomery–Taylor window (paper §7.1; `BridgeD.lean`, `ParamsD.lean`):
  `φ_λ,T(u) := [cos(√2 λ u/L)]^{1/2} · ϱ((L/2 − |u|)/w)`, where `ϱ` is a `TaperProfile`
  (Defs.lean:176-183), i.e. `ϱ = 0` on `(−∞,0]`, `ϱ = 1` on `[1,∞)`. Hence on the bulk
  `|u| ≤ L/2 − w` the ramp factor is identically `1`, and `φ² = cos(√2 λ u/L)` there.
- Optimal profile (Functional.lean): `vStar λ s := cos(√2 λ s)` (`Functional.lean:32`).
- Zero atoms. The zero side builds the Gram matrix from `φ̂(γ_ρ − τ_k)` building blocks
  (`Defs.lean Gsummand`), where `φ̂(z) = ∫ φ(u) e^{i z u} du` is the (cosine-real) Fourier
  transform of the window. Two simple-zero atoms `v_γ(u) = φ(u)e^{iγu}` have finite-window
  inner product
  `⟨v_γ, v_γ′⟩ := ∫_{−L/2}^{L/2} φ(u)² cos((γ − γ′) u) du = (φ²)̂(γ − γ′)`.
  This is the **Fourier (cross-frequency) overlap**; it is the object that produces the
  kernel. (The real part only, by evenness of `φ²`.)
- Scale-free autocorrelation (Window.lean:1211-1213, `integral_cos_overlap`:
  `Functional.lean`-adjacent):
  `Cfun λ L y := (L−y)/2·cos(√2λ (1/L) y) + sin(√2λ (1/L)(L−y))/(2√2λ (1/L))`,
  with `∫_{u=−L/2}^{L/2−y} vStar(u/L)·vStar((u+y)/L) du = Cfun λ L y`.
  `Cfun` models the **autocorrelation** of the profile `vStar` (a `g = φ²⋆φ²`-type moment
  integral used for the J-moment), **not** the Gram overlap entry. *(Framing note — this
  distinction is the crux of Step 1: see §4.)*

## 3. Exact limit statement (Lean-ready)

Fix `0 < λ ≤ 1`, a `TaperProfile` `ϱ`, and `1 ≤ w` fixed. For real `T ≥ T₀(λ,w)` with
`8w ≤ L`, `L = λ·log(T/2π)`, define

    F_L(x) := ∫_{−1/2}^{1/2} cos(√2 λ t)·ϱ((1/2 − |t|)·L/w)² · cos(2π x t) dt,
    K_λ(x) := ∫_{−1/2}^{1/2} cos(√2 λ t)·cos(2π x t) dt,
             = sin(1/√2 − πx)/(2·(1/√2−πx)) + sin(1/√2 + πx)/(2·(1/√2+πx))   (λ = 1),
    K_λ(0)  = √2·sin(λ/√2)  > 0.

**Theorem (kernel-limit lemma, analysis level).** For every `x ∈ ℝ`,
`| F_L(x) − K_λ(x) | ≤ 2w/L` (uniform rate bound). Consequently, for the inner products
of two simple-zero atoms with normalized separation `x = (γ−γ′)·L/(2π)`,

    ⟨v_γ, v_γ′⟩ / ⟨v_γ, v_γ⟩  =  F_L(x) / F_L(0)  ⟶  K_λ(x) / K_λ(0)      (L → ∞),

uniformly for bounded x, with explicit `O(w/L)` error.  For λ = 1 (the C₉ case)

    K_1(x) / K_1(0) = kMT(x)
    = [sinc((√2)⁻¹ − πx) + sinc((√2)⁻¹ + πx)] / (2·√2·sin((√2)⁻¹)),

so `⟨v_γ, v_γ′⟩/⟨v_γ, v_γ⟩ = kMT(x) + O(w/L)` uniformly for bounded x.

**Normalization determined from the Gram definition.** The Gram entries are
`Gz k l = Σ_ρ m_ρ φ̂(γ_ρ−τ_k) φ̂(γ_ρ−τ_l)` (`Defs.lean:304`); the matching atom overlap is the
Fourier overlap `(φ²)̂(γ−γ′)`, whose normalized ratio is `K_λ(x)/K_λ(0)`. The diagonal
normalization is `⟨v_γ,v_γ⟩ = L·F_L(0)`, i.e. `⟨v_γ,v_γ′⟩/⟨v_γ,v_γ⟩`. (The `1/(aL²)`
"hat" units `Defs.lean:290` differ by the *same* constant on every entry and cancel in the
ratio; see §4.)

## 4. Normalization / ambiguity resolution (honest)

The task suggested reading the finite-window side through `Cfun`/`integral_cos_overlap`.
The resolution is **precise and evidence-based**, not a guess:

- `Cfun`/`vConv` is the *autocorrelation* of the profile `vStar`: `∫ v(t)v(t+y/L)dt`. As
  `L→∞` it tends to a constant independent of the normalized separation x, **not** to
  `kMT(x)`. (Verified numerically, §5/§7; `Cfun(1,100,0.3·100)/100 = 0.6145… ≠ kMT(0.3)
  = 0.8681…`.)
- The kernel `kMT(x) = K_1(x)/K_1(0)` is the **Fourier (cross-frequency) transform** of the
  MT profile: `K_1(x) = ∫cos(√2 t)cos(2π x t)dt = v̂(2πx)`. It arises from the overlap
  `(φ²)̂(γ−γ′)` where the second oscillation has the *beat* frequency `γ−γ′ = 2πx/L`,
  which is exactly the `cos(2π x t)` factor. `Cfun` has no such beat frequency.
- Therefore the correct finite-window object is `⟨v_γ,v_γ′⟩ = (φ²)̂(γ−γ′)` (used by the
  Gram in Defs.lean), and `Cfun` is the J-moment autocorrelation. The Chain9 sidebar's
  phrase "high-T limit of the finite-window overlap Cfun to this k" is **imprecise** if read
  literally; the precise overlap is the Fourier one, and `Cfun` is not a faithful finite-
  window model for the Gram overlap entry. This is the ambiguity this run resolves.

What would fully close the resilience against re-reading: if a Lean bridge is later built
against `Cfun` directly, it must add the beat-frequency cross term `cos(2π x t)` that the
two `vStar` factors in `Cfun` do **not** carry. `reproducibility/*.py` and `candidate_proof.md`
document both the correct limit and the `Cfun` non-match.

## 5. Completion criteria

- [x] Exact Lean-ready statement derived (this file §3).
- [x] Analysis-level proof complete: `|F_L − K_λ| ≤ 2w/L`, dominated convergence, ratio
      normalization, `kMT = K_1/K_1(0)` identity (`candidate_proof.md`).
- [x] Numerical cross-check at x ∈ {0.3, 1.0, 1.9}, L ∈ {100,1000,10000}: Fourier-ratio
      → `kMT` at O(w/L) rate (`reproducibility/kernel_limit_verify.py`,
      `ramp_rate_verify.py`).
- [ ] Lean formalization / machine acceptance of the bridge: **not** in scope of this
      bounded pass (the snapshot's Zeta23 files are the source of the statement, not this
      run's outputs); a follow-up lean-verify run would formalize `§3`.

## 6. Forbidden moves / discipline

- Numerical evidence used only as verification of an already-proved limit, never as proof.
- No silent change of quantifier (x bounded vs unbounded), λ-range, ramp width w, or the
  definition of the finite-window overlap: all pinned to the snapshot lines cited.
- The `Cfun` non-match is reported, not papered over (epistemic rule: report ambiguity,
  never guess silently).

## 7. Tool / citation constraints

- Python `py -3.10`, `PYTHONUTF8=1`, mpmath (high precision) for all numerics.
- Snapshot sources read (not assumed): `ThmD/{ParamsD,Window,Functional,BridgeD}.lean`,
  `Defs.lean`, `ZeroSide/RankTraceMult.lean`, `XiPrime/Window.lean`, `Chain9.lean`,
  OpenAI `proof.md`, paper `claude-paper-main-v2.txt` §7.
- Version/sha256 recorded in `repro_manifest.md` and `SHA256SUMS`.
