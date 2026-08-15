# Problem Contract — M3-open-A: AtOne certificate content for κ₁(1, vMT)

## Normalized statement

Let `vMT(s) = cos(√2·s)` on `[−1/2, 1/2]`, and let `D₁` be the ξ′ diagonal density
(`D1 s = s − 4s² + Σ_k D1coeff k·s^{2k+3}`, `D1coeff k = 2·4^{k+1}·k!/(2k+2)!`,
Lean `Zeta23.XiPrime.Defs.D1`).  Define the ξ′ second-moment constant at λ=1
(`Defs.kappaXi`, `AtOne.kappaXi_one`):

    κ₁(1, vMT) = (∫_{−1/2}^{1/2} vMT²  +  jWin(D₁, 1, vMT)) / (∫_{−1/2}^{1/2} vMT)² ,
    jWin(D, 1, v) = 2 ∫₀¹ D(1·r)·(v⋆v)(r) dr ,   (v⋆v)(r) = ∫_{−1/2}^{1/2−r} v(s)v(s+r) ds .

The open item is the **AtOne certificate**: the exact-rational *sandwich*
`κ₉ ≤ κ₁(1, vMT) ≤ κ₉ + ε₉` (mirroring the flat/quartic AtOne pattern), where
`ε₉ = 1024/2990212875 < 3.425·10⁻⁷` is the formally-verified D₁ tail bound
(`Zeta23.XiPrime.Certificate.D1.eps9`) and the D₁/D1trunc control is
`D1trunc 9 ≤ D₁ ≤ D1trunc 9 + ε₉` on [0,1].  This pins `H_{ξ′} = 2 − κ₁(1,vMT)` in Lean
(`Record9.XiPrimeMT.H_xip`).

## Objects (exact closed forms; √2 = sqrt 2)

| Constant | Closed form | Lean name |
|---|---|---|
| Iv = ∫vMT | √2·sin(1/√2) | `IvMT` (= 0.91872536986556843778…) |
| a = ∫vMT² | 1/2 + sin(√2)/(2√2) | `aMT` (= 0.84922799931830417992…) |
| b = ∫vMT⁴ | 3/8 + sin(√2)/(2√2) + sin(2√2)/(16√2) | `bMT` (= 0.73784297545060818785…) |
| (v⋆v)(r) = vConv vMT r | ½(1−r)cos(√2r) + sin(√2(1−r))/(2√2) | `vConvMTcl r` |
| J₁ = jWin(D1trunc 9,1,vMT) | 2∫₀¹ D1trunc 9 r · vConvMTcl r dr | `J1MT` (= 0.10633754139274846…) |
| κ₉ | (a + J₁)/(Iv)² | `kappaXiOne_MT` (= 1.1321111338009974…) |

Certified: `vConv vMT r ≥ 0` on [0,1] (min 0; it is the integral of a nonnegative product),
and `2∫₀¹ vConv vMT = (∫vMT)²` (Fubini identity, verified numerically to 50 digits).

## Conclusion to certify

    κ₉ ≤ κ₁(1, vMT) ≤ κ₉ + ε₉ ,   i.e.   kappaXi 1 vMT ∈ Icc kappaXiOne_MT (kappaXiOne_MT + eps9).

Cross-check against the A2-audited canonical value (reports/xi-prime-mt-window.py, dps=120):

    κ₁(1, vMT) = 1.132111134800948064449685289579659686777429502383…  (in [κ₉, κ₉+ε₉])
    H_{ξ′}     = 2 − κ₁(1,vMT) = 0.8678888651990519355503147104203403132225704976166306446…

## Completion criteria

1. **Math-level (this pass):** certified ARB enclosure of κ₉ with width ≪ ε₉, and a rigorous
   sandwich `κ₉ ≤ κ₁(1,vMT) ≤ κ₉+ε₉` whose bounds are evaluated with error < 10⁻¹², containing
   the canonical value.  → `FINITE_COMPUTATIONAL_RESULT`.
2. **Lean (stretch):** `Record9.XiPrimeAtOne` declaring `kappaXiOne_MT` and the sandwich
   `kappaXi_one_vMT_mem : kappaXi 1 vMT ∈ Icc kappaXiOne_MT (kappaXiOne_MT + eps9)`, with the
   heavy integral/Fubini/trig facts carried as explicit axiom-free hypotheses (honest bridge);
   `lake build Record9.XiPrimeAtOne` exit 0; no sorry/admit/axiom.  → `MACHINE_ACCEPTED_PENDING_AUDIT`.
3. **Statement freeze:** κ₁(1,vMT) = `kappaXi 1 vMT`, H_xip = 2 − κ₁(1,vMT), matching the
   A2-audited values exactly.

## Out of scope (recorded, not closed here)
- The ξ′ chain `xiChain` (M3-open-B) and the four §1 profile L¹-norms as Lean lemmas
  (M1-open-C) from FORMALIZATION_STATUS_XIP.md.
- The *proof-managed* evaluation of ∫vMT, aMT, vConvMTcl-closed-form, and the Fubini identity
  inside Lean (the statements are carried as hypotheses; see Lean module FIDELITY note).
