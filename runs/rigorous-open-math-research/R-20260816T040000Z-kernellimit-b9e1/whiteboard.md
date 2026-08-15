# Whiteboard — kernel-limit lemma (T1c item 3)

Run: `R-20260816T040000Z-kernellimit-b9e1`

## The statement (Lean-ready)

```
⟨v_γ, v_γ′⟩ = ∫_{−L/2}^{L/2} φ(u)² cos((γ−γ′)u) du,   φ(u) = √cos(√2λu/L)·ϱ((L/2−|u|)/w)
x = (γ−γ′)·L/(2π)
K_λ(x) = ∫_{−1/2}^{1/2} cos(√2λt)cos(2πxt)dt,   K_λ(0)=√2 sin(λ/√2)
| ⟨v_γ,v_γ′⟩/L − K_λ(x) | ≤ 2w/L                  (uniform in x)
⟨v_γ,v_γ′⟩/⟨v_γ,v_γ⟩ → K_λ(x)/K_λ(0) = kMT(x)      (λ=1, C₉ kernel), rate O(w/L)
```

## Chain of identities

1. `t = u/L`,  `(γ−γ′)u = 2π x t`  ⇒  `⟨v_γ,v_γ′⟩ = L ∫ cos(√2λt)·ϱ(...)²·cos(2πxt) dt`.
2. `ϱ(...)=1` iff `|t|≤1/2−w/L`; discrepancy set has measure `2w/L`; integrand ≤1 ⇒
   `|F_L−K_λ|≤2w/L`.
3. `K_1(x)=½[sinc(1/√2−πx)+sinc(1/√2+πx)]`, `K_1(0)=√2 sin(1/√2)`.
4. `kMT(x)=K_1(x)/K_1(0)` = Chain9 kernel = Arb normalized_kernel.

## Key distinction (crux)

- **Fourier overlap** `(φ²)̂(γ−γ′)` — carries beat freq `γ−γ′=2πx/L` ⇒ `cos(2πxt)` ⇒ **kMT**. ✅
- **Autocorrelation** `Cfun`/`vConv = ∫ vStar(u/L)vStar((u+y)/L)du` — phase `√2λy/L`
  (u-independent), no beat freq ⇒ does **not** give kMT; it is the J-moment object. ❌

## Open for a follow-up

- Lean formalization of §3, then `lake build` / machine acceptance (lean-verify role) —
  not done in this bounded pass.
- Uniformity constant for the *ratio* on a bounded x-range (straightforward, not computed as
  a tight constant here; C₉ only needs λ=1).
