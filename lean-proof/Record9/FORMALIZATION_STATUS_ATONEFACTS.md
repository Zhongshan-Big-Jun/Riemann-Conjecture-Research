# Formalization status — T3-open-A AtOne analytic facts (Stage C)

Modules: `lean-proof/Record9/Record9/XiPrimeAtOneFacts.lean` (`Record9.XiPrimeAtOneFacts`),
`lean-proof/Record9/Record9/XiPrimeAtOneFacts2.lean` (`Record9.XiPrimeAtOneFacts2`), and
`lean-proof/Record9/Record9/XiPrimeAtOneFacts3.lean` (`Record9.XiPrimeAtOneFacts3`),
namespace `Zeta23.XiPrime`. Pinned mathlib `51e6992e`, Lean `v4.33.0-rc2`.

Status line: **MACHINE-ACCEPTED (AtOne facts fully promoted)** — all five M3-open-A
analytic hypotheses have been proved as real theorems. `lake build` for all three facts
modules exits 0; no `sorry`/`admit`/`axiom`; `#print axioms` on the unconditional sandwich
theorems is `{propext, Classical.choice, Quot.sound}`.

## Promoted to theorems (machine-checked)

In `Record9.XiPrimeAtOneFacts`:
- `IvMT_pos_fact : 0 < IvMT`
- `integral_vMT_forms_fact : (∫ vMT = IvMT) ∧ (∫ vMT² = aMT)`
- `vConvMT_closed_fact : ∀ r ∈ Icc 0 1, vConv vMT r = vConvMTcl r`
- plus helper lemmas: `sqrt_two_pos`, `sqrt_two_ne_zero`, `sqrt_two_mul_half_eq_inv`,
  `one_le_sqrt_two`, `one_div_sqrt_two_le_one`, `one_div_sqrt_two_pos`,
  `one_div_sqrt_two_lt_pi`, `integral_cos_mul`, `integral_cos_mul_add`,
  `integral_cos_sq_mul`.

In `Record9.XiPrimeAtOneFacts2`:
- `two_integral_vConv_vMT_fact : 2 * ∫₀¹ vConv vMT = (IvMT)^2`
  (Fubini/autocorrelation identity)
- plus helper lemmas: `integral_one_sub_mul_cos_sqrt2`, `integral_sin_sqrt2_sub_one`,
  `integral_vConvMTcl`, `IvMT_sq_eq_one_sub_cos_sqrt2`.

In `Record9.XiPrimeAtOneFacts3`:
- `vConvMTcl_nonneg : 0 ≤ vConvMTcl r` on `[0,1]`
- `jWin_trunc9_vMT : jWin (D1trunc 9) 1 vMT = J1MT`
- `two_integral_vConvMTcl : 2 * ∫₀¹ vConvMTcl = (IvMT)^2`
- `jWin_D1_one_vMT_sandwich_fact : J1MT ≤ jWin D1 1 vMT ∧ jWin D1 1 vMT ≤ J1MT + eps9*(IvMT)^2`
- `kappaXi_one_vMT_mem_fact : kappaXi 1 vMT ∈ Icc kappaXiOne_MT (kappaXiOne_MT + eps9)`
- `H_xip_vMT_mem_fact : H_xip ∈ Icc (2 − (κ₉+ε₉)) (2 − κ₉)`

## Remaining open M3-open-A hypotheses

None. All five analytic facts are now machine-proved; the unconditional AtOne sandwich and
sharp H_{ξ′} range are available as `kappaXi_one_vMT_mem_fact` / `H_xip_vMT_mem_fact` in
`Record9.XiPrimeAtOneFacts3`.

## Machine evidence

| Command | Exit | Evidence |
|---|---|---|
| `lake build Record9.XiPrimeAtOneFacts` | **0** | "Build completed successfully (8847 jobs)"; only linter hints |
| `lake build Record9.XiPrimeAtOneFacts2` | **0** | "Build completed successfully (8848 jobs)"; only linter hints |
| `lake build Record9.XiPrimeAtOneFacts3` | **0** | "Build completed successfully (8850/8851 jobs)"; only linter hints |
| `#print axioms` (Facts3 headline theorems) | clean | `[propext, Classical.choice, Quot.sound]` |
| comment-aware sorry/admit/axiom scan | clean | no `sorry`/`admit`/`axiom` outside comments |

## Next step

The T3-open-A AtOne certificate content is now machine-checked. Remaining Stage C work is
outside this module: T1c-2a block-energy finite counting, T1c-2c/2d, and T2 certificate
reflection; plus the ξ′ record theorem assembly that consumes this AtOne sandwich.
