# Obligation graph — M3-open-A AtOne certificate for κ₁(1,vMT)

| Obligation | Statement | Status | Evidence |
|---|---|---|---|
| O1 — ∫vMT = √2·sin(1/√2) | closed form | ✅ (math) | ARB + quadrature agree to 60 dp; Lean `IvMT` def |
| O2 — a = ∫vMT² | ½+sin(√2)/(2√2) | ✅ (math) | closed form + quadrature; blueprint `a` |
| O3 — b = ∫vMT⁴ | 3/8+sin(√2)/(2√2)+sin(2√2)/(16√2) | ✅ (math) | closed form + quadrature; blueprint `b` |
| O4 — ∫vMT transcription error | status doc `…843826` vs `…437784` | ✅ resolved | three-way check; true = …437784 |
| O5 — vConv vMT = vConvMTcl on [0,1] | closed form | ✅ (math) / OPEN (Lean) | quadrature 40 dp; Lean `vConvMT_closed` Prop |
| O6 — vConv vMT ≥ 0 on [0,1] | sandwich sign | ✅ (math, grid) / OPEN (Lean) | grid min 0.0; needed for D₁-tail sign |
| O7 — Fubini 2∫₀¹ vConv vMT = (∫vMT)² | = 0.844056305234626… | ✅ (math) / OPEN (Lean) | numerical 50 dp; Lean `two_integral_vConv_vMT` |
| O8 — 0 < IvMT | positivity | ✅ (math) / OPEN (Lean) | IvMT = ∫cos≥… ; Lean `IvMT_pos` |
| O9 — J1 = 2∫₀¹ D1trunc9·vConvMTcl | = 0.10633754139274846 ± 2e-16 | ✅ (ARB rigorous) | composite Simpson + global M₄ bound |
| O10 — jWin(D1) sandwich | J1 ≤ jWin ≤ J1+ε₉(∫v)² | ✅ (math, via D1 cert) / OPEN (Lean proof mechanics) | D1_trunc≤D1≤trunc+ε₉ + vConv≥0; Lean `jWin_D1_one_vMT_sandwich` Prop |
| O11 — κ₉ in Lean | = (aMT+J1MT)/(IvMT)² | ✅ (Lean def `kappaXiOne_MT`) | compiles |
| O12 — κ₁(1,vMT) ∈ [κ₉,κ₉+ε₉] | AtOne sandwich | ✅ (Lean `kappaXi_one_vMT_mem`, conditional) | compiled; depends on O5–O8, O10 as hyp |
| O13 — H_xip range | 2−κ₁ ∈ [2−(κ₉+ε₉), 2−κ₉] | ✅ (Lean `H_xip_vMT_mem`) | compiled; corollary of O12 |
| O14 — cross-check vs canonical | H = 0.86788886519… | ✅ | |H−canonical| ≈ 1.4·10⁻⁵⁶; sandwich contains canonical |
| O15 — no sorry/admit/axiom | — | ✅ | scan + build clean |

## Open obligations passed to later passes (re-stated exactly)
- **M3-open-A(Lean)** — formal Lean proofs (not just hypotheses) of: O5 (vConv closed form),
  O6 (vConv ≥ 0), O7 (Fubini 2∫₀¹vConv=(∫v)²), O8 (0<IvMT), and the integral-manipulation
  step O10 (jWin(D1trunc9,1,vMT)=J1MT).  These are the analytic/evaluation content.
- **M3-open-B** — the ξ′ chain `xiChain` (pressure method), unchanged from XiPrimeMT.
- **M1-open-C** — the four §1 profile L¹-norms as Lean lemmas (paper constants).

## Non-circularity
O12/O13 use only O5–O8/O10 as hypotheses plus the formally-verified D₁ certificate and the
Defs definitions (AtOne.kappaXi_one, jWin_one, jWin_one_le_of_le).  No circular dependence:
the κ₁ computation and the canonical cross-check are independent code paths (ARB vs mpmath)
agreeing to ≥ 56 digits.
