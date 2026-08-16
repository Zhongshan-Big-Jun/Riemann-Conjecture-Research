# Problem Contract — Exact m_7 for the sine-DPP Gram moment sequence

**Run ID:** `R-20260816T110000Z-m7exact-ea0a`
**Task packet ID:** `Q-m7exact-ea0a` (bounded exact-computation pass, solver stage B)
**Status label (target):** `FINITE_COMPUTATIONAL_RESULT` (exact m_7); `RIGOROUS_PARTIAL_RESULT`
for the Λ_4 / m_8 forks if those cannot be closed in budget.

## 1. Exact statement

For the random sine-process (density 1) Gram moment sequence, the k-th trace moment is

```
m_k = Σ_{σ∈Part(k)} J_σ ,   Part(k) = set partitions of {0..k−1}
J_σ = ∫_{R^{b−1}} ∏_{a=0}^{k−1} K(x_{σ(a)} − x_{σ(a+1)}) · ρ_b  dx
ρ_b = det[K(x_i − x_j)]_{i,j=0..b−1},   K(t) = sinc(t) = sin(πt)/(πt)
```

with `b = #blocks(σ)`, translation pinning fixing one integration variable (hence `b−1`
free variables), self-loop cycle edges contributing `K(0)=1`. Empty/self-loop product factors
are exactly 1.

**Deliverable for this pass:** the exact rational `m_7 = Σ_{σ∈Part(7)} J_σ`, where
`Part(7)` has Bell(7) = 877 elements. If the budget permits, also exact `m_8`
(Bell(8) = 4140); otherwise record the strongest exact partial result and state that
m_8 remains open.

## 2. Completion criteria

1. Enumerate all 877 partitions of {0..6}; apply the verified G2 vanishing rule
   (100% on the 275 exact rows k=3..6, authoritative context):
   `J_σ = 0 ⟺ H_σ disconnected OR m ≤ 2b−3`, equivalently
   **`J_σ ≠ 0 ⟺ H_σ connected AND m ≥ 2b−2`** (b=1 always nonzero).
   Here `H_σ` is the cycle-crossing multigraph on the `b` blocks and
   `m = #cycle block-crossings`. **Verify the surviving count.**
2. For every surviving σ produce an **exact rational J_σ**:
   - b=2 closed form `J = c_m − c_{m+2}` (exact, previously certified);
   - b≥3 via the exact/`fast` box-spline engine from the m6 run, cross-validated on a
     random subset against the second engine to ≥ 1e-12 agreement **before** rational
     reconstruction.
3. Sum the per-partition J_σ to get exact m_7 (and m_8 if feasible).
4. **Hankel test:** with `m_0..m_7` (plus m_8 if available), compute the exact Christoffel
   (Hankel ratio) values. Check positive definiteness (det H_0..H_4 > 0). Determine
   whether `Λ_4(0) < Λ_3(0) = 247/2519` (decay continues) or not; if Λ_4 needs m_8
   (check the determinant sizes), say so and compute what is possible.
5. **Validation:** reproduce m_2..m_6 exactly; check m_7 against the finite-L sampler
   evidence (labeled evidence, not proof).

## 3. Honesty boundary

- Exact rationals are the deliverable; numerical evidence is not proof.
- If an exact engine cannot certify a value within budget, record the strongest partial
  result and the exact gap.

## 4. Known exact anchors (authoritative context)

- m_1=1, m_2=4/3, m_3=2, m_4=13/4, m_5=101/18, m_6=640/63.
- Λ_1(0)=1/4, Λ_2(0)=5/36, Λ_3(0)=247/2519 (decay fork decided: DECAY).
- G2 rule verified 100% on 275 exact rows k=3..6.
- c_{2n} = ∫sinc^{2n} = B_{2n}(0): c_2=1, c_4=2/3, c_6=11/20, c_8=151/315, c_10=15619/36288,
  c_12=655177/1663200.
