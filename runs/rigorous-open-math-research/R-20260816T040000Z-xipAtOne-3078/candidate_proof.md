# Candidate proof — the AtOne certificate κ₉ ≤ κ₁(1, vMT) ≤ κ₉ + ε₉

## The theorem (informal)

For `vMT(s) = cos(√2·s)`, with `D₁` the ξ′ diagonal density and
`κ₁(1,vMT) = (∫vMT² + jWin(D₁,1,vMT)) / (∫vMT)²`:

    κ₉ ≤ κ₁(1, vMT) ≤ κ₉ + ε₉ ,   κ₉ = (aMT + J1)/(IvMT)² ,
    IvMT = √2·sin(1/√2) ,   aMT = 1/2 + sin(√2)/(2√2) ,
    J1 = 2∫₀¹ D1trunc 9 r · vConvMTcl r dr ,
    vConvMTcl r = ½(1−r)cos(√2 r) + sin(√2(1−r))/(2√2) ,
    ε₉ = 1024/2990212875 .

## Proof structure (mirrors AtOne.lean)

1. **D₁ / D1trunc control** (formally verified in `Zeta23.XiPrime.Certificate.D1`):
   on [0,1], `D1trunc 9 ≤ D₁ ≤ D1trunc 9 + ε₉`.  [D1trunc_le_D1, D1_le_D1trunc9_add.]

2. **vConv vMT ≥ 0 on [0,1]** and **vConv vMT = vConvMTcl** on [0,1]
   (closed form, product-to-sum).  [open analytic obligations — Lemma 1 below.]

3. **Fubini identity:** `2∫₀¹ vConv vMT = (∫vMT)² = (IvMT)²`.  [open analytic obligation.]

4. **jWin sandwich:** from (1),(2),(3) — since `D1trunc ≤ D₁ ≤ D1trunc + ε₉` and
   `vConv ≥ 0`, multiplying by the nonnegative vConv and integrating gives
   `jWin(D1trunc,1,vMT) ≤ jWin(D₁,1,vMT) ≤ jWin(D1trunc,1,vMT) + ε₉·2∫₀¹vConv vMT`,
   i.e.  `J1 ≤ jWin(D₁,1,vMT) ≤ J1 + ε₉·(IvMT)²`.   [AtOne device: `jWin_one_le_of_le`.]

5. **κ₁ algebra:** `κ₁(1,vMT) = (aMT + jWin)/(IvMT)²` (uses ∫vMT² = aMT, ∫vMT = IvMT).
   With (4): `(aMT+J1)/(IvMT)² ≤ κ₁ ≤ (aMT+J1)/(IvMT)² + ε₉·(IvMT)²/(IvMT)² = κ₉ + ε₉`.  ∎

## Lemma 1 (open obligations, math-verified)
- ∫vMT = √2·sin(1/√2); ∫vMT² = ½+sin(√2)/(2√2); ∫vMT⁴ = 3/8+sin(√2)/(2√2)+sin(2√2)/(16√2).
- vConv vMT r = ½(1−r)cos(√2r)+sin(√2(1−r))/(2√2) on [0,1], ≥ 0 on [0,1].
- 2∫₀¹ vConv vMT = (∫vMT)² (Fubini).
All are closed-form/elementary; verified by ARB + mpmath to ≥ 50 digits.  Formalized as
*axiom-free hypotheses* in `Record9.XiPrimeAtOne` (honest bridge), not as `sorry`.

## Numerical certificate (ARB, rigorous)
- J1 ∈ 0.10633754139274846 ± 2·10⁻¹⁶.
- κ₉ ∈ [1.132111133800997184…, 1.132111133800997612…]  (width 4·10⁻¹⁶).
- κ₁(1,vMT) ∈ [1.13211113380…, 1.13211147625…].
- Canonical κ₁ = 1.1321111348009480644… is **in** the sandwich (contain check True).

## Status
`FINITE_COMPUTATIONAL_RESULT` at the math level; the Lean module compiles
(`MACHINE_ACCEPTED_PENDING_AUDIT` for the bridge theorems; the open analytic obligations
remain Lemmas 1(1-3), M3-open-A, for a later pass).
