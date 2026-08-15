# Reproducibility — M3-open-A AtOne certificate for κ₁(1,vMT) (run R-…-3078)

## Scripts
- `atone_xip_mt.py` — the RIGOROUS certificate.  ARB interval arithmetic (python-flint 0.9.0)
  at `ctx.dps = 200`; exact closed forms for ∫vMT, aMT, bMT, vConv vMT; the heavy integral
  J1 = 2∫₀¹ D1trunc9·vConv vMT is enclosed by composite Simpson (n=20000) with a rigorous
  remainder from a global bound M₄ = max|f^{(4)}| on [0,1] obtained via the triangle
  inequality on the sympy-reduced exact form `A(r)+cos(√2r)B(r)+sin(√2r)C(r)`.  All printed
  bounds are ARB enclosures = rigorous.
- `audit_kappa.py` — INDEPENDENT cross-check (mpmath native, EVIDENCE): recomputes κ₁ and H by a
  separate code path and confirms the ARB sandwich contains the canonical values.

## How to run (Windows, `$env:PYTHONUTF8=1`)
```
py -3.10 reproducibility/atone_xip_mt.py        # ARB certificate (exit 0)
py -3.10 reproducibility/audit_kappa.py         # independent evidence (exit 0)
```

## Key reproducible results (from the run)
- ∫vMT = 0.9187253698655684377842315251…
- aMT = ∫vMT² = 0.8492279993183041799212983516285479…   (blueprint a)
- bMT = ∫vMT⁴ = 0.7378429754506081878529071314431441…   (blueprint b)
- 2∫₀¹vConv vMT = (∫vMT)² = 0.8440563052346255265453520210914104…
- J1 = 2∫₀¹ D1trunc9·vConv vMT = 0.10633754139274846 ± 2·10⁻¹⁶
- κ₉ = (aMT+J1)/(∫vMT)² ∈ [1.1321111338009971841…, 1.1321111338009976121…]  (width 4·10⁻¹⁶)
- certified: κ₁(1,vMT) ∈ [κ₉, κ₉+ε₉], ε₉ = 1024/2990212875
- canonical κ₁ = 1.1321111348009480644…  ∈ sandwich ✓
- canonical H = 0.8678888651990519355503147104203403132225704976166306446… ∈ [2−(κ₉+ε₉), 2−κ₉] ✓

## Determinism / environment notes
See `repro_manifest.md` for versions.  python-flint `arb` interval operations are deterministic
given `ctx.dps`; the Simpson grid and M₄ are fixed.  mpmath quadrature is used only for the
(marked) evidence path, never for the certified bounds.
