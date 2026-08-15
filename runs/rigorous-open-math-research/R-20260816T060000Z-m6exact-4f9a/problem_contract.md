# Problem contract — exact m_6 + Hankel fork resolution

## Statement
Random sine-process Gram matrix `G_ij = sinc(x_i−x_j)`, `x_i` from the sine/Bessel DPP, intensity 1.
`m_k = (1/N) E[tr G^k]` (N→∞, density 1). This pass: (1) compute **m_6 exactly**, (2) use exact
`m_1..m_6` to compute `Λ_3(0)=det(H_3)/det(H_3^{(00)})` and decide the **decay-vs-plateau fork** for
the SL criterion (μ_λ({0})=0 ⟺ Λ_m(0)→0), (3) record the k=6 Lemma P coefficient structure and a
refined general-k conjecture.

## Completion criteria (all met)
- Exact rational `m_6` with a derivation: **m_6 = 640/63 = 10.15873…**.
- Exact `Λ_3(0) = 247/2519 ≈ 0.09805`, `Λ_1=1/4`, `Λ_2=5/36`; fork verdict **DECAY** (Λ_3 < Λ_2,
  plateau impossible).
- k=6 coefficient structure recorded (nonzero values + multiplicities; vanishing shapes).
- Numerics labeled evidence only.

## Known exact (prior, audited) and new
Prior: m_1=1, m_2=4/3, m_3=2, m_4=13/4, m_5=101/18; Λ_1=1/4, Λ_2=5/36;
c_2=1,c_4=2/3,c_6=11/20,c_8=151/315,c_10=15619/36288.
New this run: **c_12=655177/1663200**, **m_6=640/63**, **Λ_3=247/2519**.

## Result
m_6 = 1 + 4297/630 + 479/210 + 2/35 = 640/63. Moment sequence m_0..m_6 positive definite.
Λ_3(0)=247/2519 ≈ 0.098 < Λ_2=5/36 ≈ 0.139 (decay through degree 3). Fork = **decay**.

## Not in scope / open
- Exact m_7, m_8 (⇒ Λ_4 exact); general-k Lemma P/G2 proof; SL asymptotic decay.
