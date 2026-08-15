# Problem contract — exact m_5 (5th sine-Gram trace moment) + Hankel test

## Statement
Let the random sine-process Gram matrix on a length-L window have entries
`G_ij = sinc(x_i − x_j)`, `x_i` drawn from the Bessel/sine DPP with kernel
`K(x,y) = sinc(x−y)` (intensity 1, E[N] = L). Define the k-th trace moment
`m_k = (1/N) E[ tr G^k ]` (N→∞, density 1). The task is:

1. Compute `m_5` **exactly** (a rational/algebraic closed form with a derivation), via the DPP
   factorial-moment / set-partition shape decomposition, given `D_5 = 0` (certified).
2. Test the Hankel criterion Λ_m(0) = det(H_m)/det(H_m^(00)) with the exact moments, checking
   whether the values continue to decay (SL-relevant asymptotics).
3. Record the k=5 instance of Lemma P (the exact coefficient / matching structure).

## Completion criteria
- A concrete exact value for `m_5` with a reproducible derivation (exact rational).
- The value validated numerically (DPP simulation) and by independent exact engines; all
  numerical checks labeled as evidence only.
- Hankel values reported with exact/evidence status honestly distinguished.

## Known exact (prior, audited)
m_1=1, m_2=4/3, m_3=2, m_4=13/4. D_3=D_4=D_5=0 certified (box-spline identity). c_2=1,
c_4=2/3, c_6=11/20, c_8=151/315, c_10=15619/36288.

## Result
`m_5 = 101/18 = 5.6111…` (exact rational). Λ_1(0)=1/4, Λ_2(0)=5/36 exactly; Λ_3,Λ_4 unresolved
(need exact m_6,m_7,m_8).

## Not in scope / open
- General-k proof of the vanishing structure (b≥4 ⇒ J_σ=0) and of Lemma P/H.
- SL (Λ_m→0) — needs exact higher moments; still OPEN.
