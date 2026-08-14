# Window generalization of the pressure method — analysis (2026-08-14)

Manager-level theoretical note. Purpose: assess whether replacing the Montgomery–Taylor (MT)
window by another window ψ can improve the k=9 record via a larger pressure constant f_9.

## Setup

In the pressure-method chain (extpress run, candidate_proof.general-k-derivation.md), the
window enters twice:

1. The baseline: S ≥ H(ψ)·N − o(N) with H(ψ) = 2 − R(ψ), R(ψ) = ‖Ĝ‖²_F/N (λ=1 HS ratio).
   CCLM17 (Cor. 14): among bandwidth-one windows, ψ_MT minimizes R, R(ψ_MT) = 1/c₁*,
   H_MT = 2 − 1/c₁* = 0.6725007. Hence H(ψ) ≤ H_MT for every bandwidth-one ψ.
2. The pressure function F_{k-1}(g) via w(x) = k_ψ(x)², where k_ψ is the normalized overlap
   kernel of the window. The certified constants f_k depend on k_ψ.

## Trade-off

For fixed k=9 (m₉ = 264, n₉ = 256, A₀ = 624/625) the record reads
C₉ = (6875·H − 1315/96)/6849 (formula holds verbatim for any ψ once f₉ = 0.0039 is certified
for that ψ — the chain's window dependence enters only through H and f). Then:

- ∂C₉/∂H = 6875/6849 ≈ 1.0038.
- ∂C₉/∂f (discrete, at f = 0.0039): increasing f by δ raises C₉ by ≈ 0.641·δ·(m-scale
  factor) — numerically, f: 0.0039 → 0.00398 (δ = 8e-5) gives ΔC₉ ≈ 5.1e-5, i.e.
  sensitivity ≈ 0.64 per unit f.

So compensating a window-induced drop ΔH < 0 requires Δf ≳ 1.57·|ΔH|. Any bandwidth-one ψ
with R(ψ) − R(ψ_MT) = 1e-4 needs f_9(ψ) − 0.0039 ≳ 1.57e-4, i.e. f_9(ψ) ≳ 0.00406, which
exceeds the numerically indicated MT-window true minimum (≈ 0.00398) — a nontrivial demand
on the window's correlation structure. Windows with worse R (flat: R = 4/3, ΔH = −5.9e-3)
would need f_9 ≳ 0.0039 + 9.3e-3 ≈ 0.0132, essentially impossible (F ≤ O(1) scale).

## Verdict

- Window generalization is theoretically a wash at best: the MT window is simultaneously
  near-optimal for H (CCLM17) and has a near-minimal F_8 (scoping ≈ 0.00398). Any window
  that could raise f_9 meaningfully would likely lower H by more than the compensation.
- The higher-leverage lever is raising f_9 at the MT window itself (0.0039 → 0.00395 →
  0.00398; C₉ → 0.673086 → 0.673105), currently being computed (f9push run).
- Beyond the pressure class: the bandwidth-one ceiling 0.6818 and the k=1 moment barrier
  remain the structural walls; conditional routes (PCC / HL*+SL) remain the only known
  paths to 1.
