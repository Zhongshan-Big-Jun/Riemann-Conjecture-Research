# Candidate proof — kernel-limit lemma (T1c item 3)

Run: `R-20260816T040000Z-kernellimit-b9e1`
Status: **analysis-level proof complete** (not machine-formalized). Numerical cross-check
passes at O(w/L) rate. See `problem_contract.md` for the exact statement and the
normalization resolution.

## 0. Notation

- `L = λ·log(T/2π)`, window `[−L/2, L/2]`, grid step `2π/L`.
- `ϱ` a TaperProfile (ϱ=0 on (−∞,0], ϱ=1 on [1,∞)), ramp width `w`, `1 ≤ w ≤ L/8`.
- MT window `φ(u) = √cos(√2λ u/L) · ϱ((L/2−|u|)/w)`.
- Zero atoms `v_γ(u)=φ(u)e^{iγu}`; finite-window overlap
  `⟨v_γ,v_γ′⟩ = ∫_{−L/2}^{L/2} φ(u)² e^{i(γ−γ′)u} du`. By evenness of `φ²`, only the real
  part survives.
- Normalized separation `x := (γ−γ′)·L/(2π)`, i.e. `γ−γ′ = 2πx/L`.
- `K_λ(x) := ∫_{−1/2}^{1/2} cos(√2λ t) cos(2π x t) dt`,  `K_λ(0) = √2 sin(λ/√2)`.

## 1. Reduction to a single scale-free integral

Substitute `t = u/L ∈ [−1/2,1/2]`. Since `φ(u)² = cos(√2λ t)·ϱ((1/2−|t|)·L/w)²` and
`e^{i(γ−γ′)u} = e^{i 2π x t}` with real part `cos(2π x t)`:

```
⟨v_γ, v_γ′⟩ = L · ∫_{-1/2}^{1/2} cos(√2λ t)·ϱ((1/2−|t|)L/w)²·cos(2π x t) dt
            = L · F_L(x)                                                (Eq. 1)
F_L(x) := ∫_{-1/2}^{1/2} cos(√2λ t)·ϱ((1/2−|t|)L/w)²·cos(2π x t) dt.
```

At the diagonal, `⟨v_γ, v_γ⟩ = L·F_L(0)`. (All integrals are Riemann/Lebesgue; the
integrand is continuous in t for each L, x.)

## 2. Key estimate: uniform `|F_L(x) − K_λ(x)| ≤ 2w/L`

Because `ϱ` is 0 on `(−∞,0]` and 1 on `[1,∞)`:

```
ϱ((1/2−|t|)L/w) = 1   ⟺   (1/2−|t|)L/w ≥ 1   ⟺   |t| ≤ 1/2 − w/L.
```

So `ϱ((1/2−|t|)L/w)² = 1` on the bulk `|t| ≤ 1/2 − w/L`, and differs from 1 at most on the
two boundary bands `1/2−w/L < |t| ≤ 1/2`, whose total Lebesgue measure is `2·(w/L)`.

For every t, x: `|cos(√2λ t)| ≤ 1`, `|cos(2π x t)| ≤ 1`, `|ϱ| ≤ 1`. Hence

```
|F_L(x) − K_λ(x)|
  = | ∫_{-1/2}^{1/2} cos(√2λ t)( ϱ((1/2−|t|)L/w)² − 1 ) cos(2π x t) dt |
  ≤ ∫_{|t| ≥ 1/2 − w/L} |ϱ(...)² − 1| · 1 · 1 dt
  ≤ ∫_{|t| ≥ 1/2 − w/L} 1 dt  =  2 w/L,                                      (Eq. 2)
```

uniformly in `x ∈ ℝ`. **This is the O(w/L) rate, uniform in x (no x-dependence).**

## 3. Pointwise convergence and the ratio

`K_λ(x)` is continuous in x (absolutely convergent integral of a bounded oscillatory
product, or dominated convergence). From (Eq. 2), `F_L(x) → K_λ(x)` uniformly in x as
`L → ∞` (since `w` is fixed). Also `K_λ(0) = ∫cos(√2λ t)dt = √2 sin(λ/√2)`, which is
`> 0` for `0 < λ ≤ 1` (sin is positive on `(0, 1/√2] ⊂ (0,π)`). Hence for large `L`,
`F_L(0) ≥ K_λ(0)/2 > 0`, and the quotient is defined. Therefore

```
⟨v_γ,v_γ′⟩ / ⟨v_γ,v_γ⟩ = F_L(x)/F_L(0)  ⟶  K_λ(x)/K_λ(0)                       (Eq. 3)
```

## 4. The C₉ kernel identity: `K_1(x)/K_1(0) = kMT(x)`

```
K_1(x) = ∫_{-1/2}^{1/2} cos(√2 t) cos(2π x t) dt
       = (1/2)[ I(√2−2πx) + I(√2+2πx) ],   I(c):=∫_{-1/2}^{1/2} cos(c t) dt = 2 sin(c/2)/c,
       = sin((√2−2πx)/2)/(√2−2πx) + sin((√2+2πx)/2)/(√2+2πx).
```

Now `(√2±2πx)/2 = 1/√2 ± πx`, and the branch denominator
`√2±2πx = 2(1/√2 ± πx)`. Thus each term equals `sin(1/√2 ± πx)/(2·(1/√2±πx)) = (1/2)sinc(1/√2±πx)`:

```
K_1(x) = (1/2)[ sinc(1/√2 − πx) + sinc(1/√2 + πx) ],  sinc z := sin z / z, sinc 0 := 1.
K_1(0) = ∫_{-1/2}^{1/2} cos(√2 t) dt = √2 sin(1/√2).
```

(The displayed singularities at `x = ±1/(√2 π)` are removable; the `sinc` form evaluates
them as 1. Numerics confirm exact equality at 40-digit precision.) Therefore for λ = 1,

```
kMT(x) := [sinc(1/√2 − πx) + sinc(1/√2 + πx)] / (2·√2·sin(1/√2))  =  K_1(x)/K_1(0),   (Eq.4)
```

which is exactly the C₉ kernel in `Chain9.lean:70-72` and the certificate's
`normalized_kernel`.

## 5. Conclusion of the lemma

Combining (Eq. 1)–(Eq. 4):

```
⟨v_γ, v_γ′⟩/⟨v_γ, v_γ⟩  =  kMT(x) + O(w/L),   x = (γ−γ′)·L/(2π),  λ = 1.
```

Uniformity: the `2w/L` bound in (Eq. 2) is independent of x; for the ratio the constant in
the `O()` grows as `sup|kMT|·(…)` over the bounded x-range (bounded), and `K_λ(0)` is
bounded below on `λ ∈ [λ₀,1]` for any `λ₀ > 0`. So for the C₉ case (λ=1, x bounded — the
"bounded normalized separations" regime of OpenAI §1) the convergence is uniform with
explicit rate `O(w/L)`.

## 6. The `Cfun` distinction (honest note)

`Cfun λ L y` (Window.lean:1211) equals `∫_{−L/2}^{L/2−y} vStar(u/L)·vStar((u+y)/L) du`, the
*autocorrelation* of the profile at separation `y`. It does **not** carry the beat
frequency `γ−γ′ = 2πx/L`; its phase is `√2λ·y/L` (a constant in u), so as `L→∞` it tends
to `L/2 + L·sin(√2λ)/(2√2λ)`, independent of x, and its normalized form does **not** equal
`kMT(x)` (verified numerically: `Cfun(1,100,30)/100 ≈ 0.6145` but `kMT(0.3) ≈ 0.8681`).
`Cfun` is the autocorrelation used for the J-moment; the kernel overlap is the Fourier
(cross-frequency) overlap `(φ²)̂(γ−γ′)` used in §1–§5. This resolves the framing ambiguity.

## 7. Check list

- [x] Exact statement derived from the Gram definition (`Defs.lean` Gsummand/Gentry).
- [x] Uniform O(w/L) rate (Eq. 2), no x-dependence in the absolute bound.
- [x] Ratio normalization `⟨v_γ,v_γ⟩` diagonal.
- [x] `kMT = K_1/K_1(0)` closed form identity (Eq. 4), matching Chain9/certificate.
- [x] Numerical verification (below + `reproducibility/*.py`).
- [ ] Lean formalization / machine acceptance: follow-up (not this bounded pass).
