# Candidate proof — T1c-1 / T1c-2 stability-bridge statements (Stage C)

Run: `R-20260816T060000Z-stabridge-a3f1`
Status line: `RIGOROUS_PARTIAL_RESULT` — the exact Lean-ready ε-form statements (T1c-1,
T1c-2) are pinned to the true Δ(M°) and the T1c-2 sub-lemma decomposition is complete with
analysis-level proofs of every finite/structural step and numerical spot-checks; one
analytically non-trivial ingredient (the pinching/uniformity step, T1c-2d and the
Δ(M°)-block average) is stated precisely but its full o(N) uniformity is the genuinely new
analytic bridge (same status class as the kernel-limit precedent: statement pinned, proofs
at analysis level, Lean formalization a follow-up).

## 0. Notation and the physical object

All preliminaries are pinned to the snapshot `Zeta23` (literature/raw/zeta-23-lean) and the
preceding kernel-limit run `R-20260816T040000Z-kernellimit-b9e1`.

- `L = λ·log(T/2π)` (`Defs.lean:49,204`), MT window `φ(u) = √cos(√2λu/L)·ϱ((L/2−|u|)/w)`,
  zero atoms `v_γ(u) = φ(u)e^{iγu}` on `[−L/2,L/2]`.
- `⟨v_a, v_b⟩ = ∫_{−L/2}^{L/2} φ(u)² cos((γ_a−γ_b)u) du` = the Fourier (cross-frequency)
  overlap = `L·F_L(x_ab)`, `x_ab := (γ_a−γ_b)·L/(2π)`, `F_L(x)` as in kernel-limit Eq. 1.
- `K_λ(x) = ∫cos(√2λt)cos(2πxt)dt`, `K_1(0) = √2 sin(1/√2)`; normalized kernel
  `kMT(x) = K_1(x)/K_1(0)` (Chain9 `kMT`), `wMT(x) = kMT(x)²`.
- `N = N(T,2T)` (with multiplicity), `S = N₀ˢ(T,2T)` (simple, on-line).
- `HD 1 = H_MT = 3/2 − (1/√2)·cot(1/√2)` (ThmD/Functional.lean:460-465).

**The object of the two bridge hypotheses.** Let `γ_1<…<γ_S` be the ordinates of the
retained central simple zeros (the `𝒮₁` of `Defs.lean:319`). Define the **unit-normalized
correlation Gram**

```
M°_ab(T) := ⟨v_a(T),v_b(T)⟩ / ‖v_a‖‖v_b‖ ,   ‖v_γ‖² = ∫φ(u)²du = L·F_L(0)  (γ-independent),
```

so every diagonal is exactly `1` and every column of `V` (the matrix of unit-normalized
atoms) has norm `1 ≤ 1`, exactly the hypothesis of OpenAI Lemma 2.1. By the kernel-limit
lemma (kernellimit run, Eq. 5), uniformly for bounded normalized separations,

```
M°_ab(T) = kMT(x_ab) + O(w/L),        ‖v_γ‖² independent of γ.
```

**(Honest normalization note — resolve or report.)** The delta of the stability hypotheses is

```
Δ(M°)(T) := tr Ψ(M°(T)),    Ψ(t) := (t−1)²·1_{t≤2} + (2t−3)·1_{t≥2},
```

with `Ψ` exactly proof.md §2. This is with the unit-normalized Gram. A different but
snapshot-native convention — the **hat-unit** Gram `Â = Az/(aL²)` used by `mult_two` /
`N0star_lower_c` (`Defs.lean:286-290`, ZeroSide/Mult.lean) — has diagonal
`‖v_γ‖²/(aL²) = F_L(0)/(aL)·… → 0` and `tr Ψ(Â) ≈ S` trivially, which would make T1c-2
trivially true but **would make Cor 2.2 (`S ≥ H_MT·N + Δ(M°)`) impossible** (`S ≥ 0.67N+S`).
So the physical Δ(M°) of Cor 2.2 must be the unit-normalized (≡ correlation) Gram
`tr Ψ(M°)`, for which the block-defect route gives the order-O(S) lower bound
`Δ(M°) ≥ (A₀/m)S − ((m−1)/(500m))N − o(N)` (T1c-2) that the chain needs — the exact identity
`Δ(M°) = total pair energy + higher-order` is only the magnitude heuristic, not used as a
step. This is the crux the pass pins; see §7 for the exact ambiguity report.

## 1. Prelim: Lemma 2.1 (the Ψ rank-inertia inequality) — statement

**(L2.1)** Let `V ∈ ℂ^{d×r}` have columns of norm `≤ 1`, put `P = VV*`, `M = V*V`, and let
`Q` be Hermitian with `n₊(Q) ≤ b`. With `Ψ` as above,

```
‖P+Q‖_F² ≥ 4 tr(P+Q) − 3r − 4b + tr Ψ(M) .        (proof.md 2.1)
```

*Proof structure (which snapshot theorems supply each step).*
- Write `Q = Q₊−Q₋` (`HermitianPosPart.lean`, `hermPosPart_sub_hermNegPart`).
- `‖Q₊‖_F² ≥ 4 tr Q₊ − 4b` (`RankTrace.lean sum_sq_lower_of_card_pos_le`
  = `rank_trace_ineq` step, `Inertia`/`PosIndex` bound `n₊(Q₊)=n₊(Q)≤b`).
- `‖P‖_F² − 2 Re tr(PQ₋) + ‖Q₋‖_F² ≥ Σ(pᵢ−nᵢ)²` (von Neumann,
  `VonNeumann.lean vonNeumann_trace_ineq`; spectral agreement of `VV*`,`V*V`,
  `Sylvester`/`RankTraceMult` `spectra agree`, `PosIndex`).
- scalar step `(p−n)² + 4n ≥ 2p − 1 + Ψ(p)` for `n≥0` (min identity, §3 C2 verified):
  `min_n[(p−n)²+4n] = 2p−1+Ψ(p) = p²·1_{p≤2} + (4p−4)·1_{p≥2}`.
- sum: `2 trP − r + tr Ψ(M)` (nonzero spectra of `P,M` agree, `tr P ≤ r` since cols ≤ 1)
  plus `4 tr Q₊ − 4b`; weaken `4trQ₊ ≥ 4trQ₊−4trQ₋ = 4tr(P+Q) − 4trP` and use
  `trP ≤ r` to reach `4tr(P+Q) − 3r − 4b + trΨ(M)`. (Re-verified in mainpush Entry 3 and
  numerically §5 C3.)

This lemma is **new to Lean** (the snapshot's `rank_trace_ineq` / `rank_trace_mult_k`
give the `g_c` / `k_c` forms, not the Ψ form); all ingredients exist as stated.

## 2. T1c-1 — the stability refinement (bridge hypothesis `stability_eps`)

**Statement (exact ε-form, == `Zeta23.ThmD.stability_eps` with `Δ := Δ(M°)`).**

```
∀ ε>0, ∃ T₀:ℝ, ∀ T≥T₀:
    HD 1 · N(T,2T) + Δ(M°)(T) − ε·N(T,2T) ≤ N₀ˢ(T,2T).        (T1c-1)
```

That is `S ≥ H_MT·N + Δ(M°) − o(N)` (OpenAI Cor 2.2 / proof.md 2.2).

**Analysis-level derivation (structure).** Apply Lemma 2.1 to the simple-zero part of the
rank-trace decomposition: `V` = unit-normalized retained-simple-zero atoms, `r = S`,
`M° = V*V`, `Q` = the off-line/other parts with `n₊(Q) ≤ p = O(S)-small`, in the **hat-unit
assembly** of `ZeroSide/Mult.lean mult_two` / `ThmD/Mult.lean thmD_mult2_abstract`.

- The base assembly supplies: columns-norm ≤ 1 (`ZeroSide/Mult.lean xsq_vhat_le` with the
  unit-normalized columns trivially =1), `n₊(Q) ≤ p` (`posIndex_blockQ_le`),
  Cauchy–Schwarz / truncated-Poisson column bounds, and the o(1)-uniformity of
  `tr Â → N`, `‖Â‖² ≤ cinv·N + o(N)` (`TracesBoundsD` / `N0star_lower_c`).
- Keeping the defect: Lemma 2.1 gives `‖P+Q‖_F² ≥ 4tr(P+Q) − 3S − 4b + tr Ψ(M°)`. Rearranged
  in the `mult_two` direction (`4tr· − ‖·‖² − 2N ≤ s₁`), the `+tr Ψ(M°)` survives additively:
  the o(N)-error machinery of `thmD_mult2_abstract` is additive in the constant term, so
```
S ≥ (HD 1)·N + Δ(M°)(T) − o(N).
```
  The only non-mechanical step is that the assembly keeps `tr Ψ(M°)` rather than bounding it
  away (the snapshot's `rank_trace_mult_k_le` is the leak-free version that *drops* this
  term); the positivity `Δ(M°) ≥ 0` (Ψ ≥ 0, verified §3 C1) makes keeping it a strict
  strengthening compatible with the trace machinery.

**Honest status of T1c-1.** Statement pinned exactly; the derivation is the corollary of
Lemma 2.1 + the *verbatim* `thmD_mult2_abstract`/`N0star_lower_c` assembly with the defect
kept. It is not a *mechanical* reuse of the machine-proved Theorem D (which uses the
leak-free form); the step "the +Δ(M°) survives the assembly additively" is the paper-level
audited input (proof.md Cor 2.2). Lean formalization = new `stability_eps`-proof.

## 3. T1c-2 — the averaged block-defect (bridge hypothesis `stability_averaged_eps`)

Let `m = m₉ = 263`, `k = 9`, `A₀ = f₉·n₉ = (392/100000)·255 = 2499/2500 < 1`,
`n₉ = m−8`, `f₉ = 392/100000` (Chain9 constants, C5 verified). The defect numbers are
`A₀/m = 2499/657500`, `(m−1)/(500m) = 262/131500` (exact, C5/T1c2c).

**Statement (exact ε-form, == `Zeta23.ThmD.stability_averaged_eps` with `Δ := Δ(M°)`).**

```
∀ ε>0, ∃ T₀:ℝ, ∀ T≥T₀:
    Δ(M°)(T) ≥ (2499/657500)·N₀ˢ(T,2T) − (262/131500)·N(T,2T) − ε·N(T,2T).    (T1c-2)
```

That is `Δ(M°) ≥ (A₀/m)·S − ((m−1)/(500m))·N − o(N)`.

### Sub-lemma decomposition (exact statements)

**T1c-2a (block energy from the certificate).** For `m=263` ordered points
`y₁<…<y_m` with gaps `gᵢ = y_{i+1}−y_i ≥ 0`, `E_m := 2Σ_{i<j}wMT(y_j−y_i)`:

```
E_m + (1/500)·(y_m − y_1) ≥ f₉·(m−8) = A₀ .          (BE, T1c-2a)
```

*Proof.* Sum the certified `F₈(g) ≥ 392/100000` (`CERTIFIED_F8_GE`, Chain9) over the `m−8`
consecutive 9-windows (general-k §3, proof.md §4). Each pair spanning `s` gaps enters at most
`9−s` windows with coefficient `2/(9−s)`, so total ≤ `2` per pair ⇒ `E_m`; each gap enters at
most `8` windows with linear coefficient `1/(500·8)`, so ≤ `1/500`-per-gap ⇒ `(1/500)(y_m−y_1)`.
Verified numerically for a concrete block (T1c2a.check, `sumF8 ≥ ... = A₀` and
`sumF8 ≤ E_m + (1/500)span`). **Input:** the certified `f₉` (T2 scope), `m−8 = 255 = ⌈1/f₉⌉−1`.
Elementary finite algebra — Lean-friendly.

**T1c-2b (block-defect lemma + A₀<1).** For Hermitian PSD `G` of size ≤ `⌈1/f₉⌉+…`:

```
tr Ψ(G) ≥ min(1, 2 Σ_{i<j} |G_ij|²) .          (defect lemma, proof.md 4.4)
```

and because `A₀ = 2499/2500 < 1`, in the regime `2Σ|G_ij|² ≤ 1` (which is exactly where the
block energy sits relative to `A₀<1`) the bound is **the `2Σ|G_ij|²` branch** (C8 verified).
*Proof.* If all eigvals ≤ 2, `Ψ(G) = (G−I)²`, `tr(G−I)² ≥ 2Σ_{i<j}|G_ij|²` (via the
off-diagonal Frobenius part of `(G−I)²` and `tr(I−G)`? — the row/col identity
`tr(G−I)² = Σ_{i,j}|(G−I)_{ij}|² ≥ 2Σ_{i<j}|G_ij|²` needs one diagonal bound; give the clean
routing in §4). If some eigenvalue > 2, `Ψ(μ) = 2μ−3 > 1` and `trΨ(G) > 1`. New to Lean
(the Schur/Jensen machinery `RankTraceMult.gc_sum_le` supplies the convex-perturbation part).

**T1c-2c (pinching/averaging finite algebra).** Averaging over the `m=263` offset block
partitions, with total normalized retained length `= N + o(N)`:

```
Δ(M°) ≥ (A₀/m)·S − ((m−1)/(500m))·N − o(N) .
```

The two rationals `2499/657500` and `262/131500` are exact (C5, T1c2c); the offset-averaging
counting (≤ `m−1` interior-gap charges per offset, span averaged by `(m−1)/m`) is finite
algebra verified in T1c2c (periodic exact model gives coeff `(m−1)/(500m)`).

**T1c-2d (analytic uniformity).** For a fixed block `B` of `m` retained zeros,

```
Σ_{i<j} |(M°)_ij|² = (1/2)·E_m(B) + o(1)  uniformly in B, as L → ∞,
```

*via the kernel-limit lemma* (`wMT(x_ij) → |M°_ij|²`, proved in kernellimit run Eq. 5,
numerically C7: `2Σ|G_ij|²/E_m → 1` at L = 100/400/1000). Consequently
`Δ(G_B) ≥ 2Σ|G_ij|² = E_m(B) + o(1) ≥ A₀ − (1/500)span(B) − o(1)` (BE). The o(1) is uniform
because a block has fixed `m` and the kernel-limit rate `O(w/L)` is uniform in x. This is
the genuinely analytic ingredient; its Lean formalization is the kernel-limit (now machine
proved for Item 3) plus this block×finitesum transfer.

### Assembly T1c-2 → ε-form

Per block `B` of every offset: `Δ(G_B) + (1/500)span(B) ≥ A₀ − o(1)`.
Sum over the `≈ S/m` blocks of an offset, average over the `m` offsets: pinch `Δ(M°)` down
(`trΨ(M°) ≥` block-averaged defect — standard unitarily-invariant convex pinching, flagged as
the sub-step to formalize), giving (T1c-2).

## 4. The Ψ-defect lemma (T1c-2b) — clean routing and why PSD matters

(T1c-2b detail.) `tr Ψ(G) ≥ min(1, 2Σ_{i<j}|G_ij|²)`.

- Case `μ_max(G) ≤ 2`: `Ψ(G) = (G−I)²`, so `tr Ψ(G) = ‖G−I‖_F² =
  Σ_{i≠j}|G_ij|² + Σ_i|G_ii−1|²` (G Hermitian). Now `2Σ_{i<j}|G_ij|² = Σ_{i≠j}|G_ij|²`
  (symmetric off-diag; `G_ij = conj(G_ji)`). So `tr Ψ(G) = 2Σ_{i<j}|G_ij|² + Σ_i |G_ii−1|²
  ≥ 2Σ_{i<j}|G_ij|²`. (Here we use `tr(G−I)² = Σ_{ij}|(G−I)_{ij}|²`, exact; the diagonal
  square term is `≥0`.) (Correcting the sketch in general-k §4: no extra majorization is
  needed for the `2Σ` bound once `μ_max ≤ 2`; the off-diagonal Frobenius of `G−I` is exactly
  `2Σ_{i<j}|G_ij|²` and the diagonal square `Σ_i(G_ii−1)²` is `≥0`.)
- Case `μ_max(G) > 2`: some eigenvalue `μ>2`, `Ψ(μ) = 2μ−3 > 1`, and since `Ψ≥0` on the
  other eigenvalues, `tr Ψ(G) ≥ Ψ(μ) ≥ 1`, giving `tr Ψ(G) ≥ 1 ≥ min(1,2Σ|G_ij|²)`.

So the lemma holds for every Hermitian `G` (PSD not even needed for the bound, but the side
`E_m`/`Σ|G_ab|²` uses PSD/Gram structure). §5 C4 verified on random PSD samples.

## 5. Numerical spot-checks (evidence, not proof)

`reproducibility/stabridge_checks.py` (15 checks) and `stabridge_sublemma.py` (6 checks):
- C1 Ψ continuity (t=0,2) and Ψ≥0; C2 `min_n` identity to 1e-16; C3 Lemma 2.1 on random
  `(d,r,b)` (zero violation); C4 defect lemma on random PSD (zero violation).
- C5 exact constants `A₀=2499/2500`, `A₀/m=2499/657500`, `(m−1)/(500m)=262/131500`,
  `cLHS=655001/657500`, `A₀<1`.
- C6 window-counting (≤ `k−s` per pair, ≤ `k−1` per gap); C7 correlation-Gram energy
  `2Σ|G_ij|²/E_m → 1` (1.046→1.004 with L); C8 `min{1,·}` branch on `A₀<1`.
- T1c2a block energy `E_m+(1/500)span ≥ A₀`; T1c2c offset coeffs exact.

## 6. Mapping to snapshot theorems (exists / new)

| Step | Status | Proof obligation | Snapshot supply |
|---|---|---|---|
| L2.1 assembly | New | Ψ rank-inertia | `RankTrace` `rank_trace_ineq`, `sum_sq_*`, `VonNeumann`, `HermitianPosPart`, `PosIndex`, `Sylvester`-spectra-agreement (all exist) |
| base assembly | Exists | `S ≥ H_MT·N − o(N)` | `ZeroSide/Mult.lean mult_two`, `ThmD/Mult.lean thmD_mult2_abstract`, `N0star_lower_c` (machine-proved) |
| keep `+Δ(M°)` | **New** | T1c-1 | combines L2.1 + above; additive in the o(N) machinery |
| T1c-2a block energy | New, elementary | `E_m+(1/500)span ≥ A₀` | finite window-sum algebra; input `CERTIFIED_F8_GE` (T2) |
| T1c-2b defect lemma | New | `trΨ(G) ≥ min(1,2Σ|G_ij|²)` | elementary Hermitian; `A₀<1` branch |
| T1c-2d uniformity | New (anal.) | `Σ|G_ij|²=(1/2)E_m+o(1)` | kernel-limit lemma (machine-proved, preceding run) |
| T1c-2c pinching/averaging | New | ε-form | finite algebra + Δ(M°)∓pinching sub-step |
| statement forms | Exists | `stability_eps`/`stability_averaged_eps` | `Chain9.lean` (machine-accepted, over `deltaMT`) |

## 7. Honest ambiguity report

1. **The normalization of `Δ(M°)`.** The unit-normalized (≡ correlation) Gram is the only
   available convention that (a) satisfies Lemma 2.1's columns-≤1, (b) makes the per-block
   square-energy `Σ_{i<j}|G_ij|² = (1/2)E_m(B) + o(1)` (T1c-2d), so the per-block defect
   `Δ(G_B) ≥ E_m(B) − o(1)`, and (c) keeps Cor 2.2 consistent (not `Δ≈S`). This is argued
   and numerically supported (C7). The **hat-unit** Gram (`Defs.lean` scale `aL²`, used by
   `mult_two`) gives `Δ(Â)≈S` and would break Cor 2.2; a reader modelling Δ on the hat-unit
   object would mis-pin T1c-2. *File that would resolve
   definitively:* a `ZeroSide`/`ThmD` file stating the columns used by the simple-zero-rank-
   trace and its exact normalization (the correlation convention is not written as a single
   `def Mzero` in the snapshot today); the `Gsummand`/`Gentry` (`Defs.lean:299,304`) give the
   Gram entries but not the unit-normalization factor.
2. **`min(1,·)` branch.** A₀<1 is machine-proved (`A0_lt_one`); the `2Σ`-branch is the active
   one where `2Σ|G_ij|² < 1`; the `1`-branch otherwise is a harmless cap. Both directions are
   elementary.
3. **The `+Δ(M°)` survival (T1c-1)** and **the pinching `Δ(M°) ≥ block average` (T1c-2c)**
   are the two paper-level ingredients carried as the OpenAI-audited steps; they are stated
   precisely here and would be the two new formalization obligations. No numerical evidence
   is claimed as proof; all inequalities above are exact real-number statements whose finite
   instances were machine-evaluated only as spot-checks.
