# Formalization status — T3-open-A AtOne analytic facts (Stage C)

Module: `lean-proof/Record9/Record9/XiPrimeAtOneFacts.lean`, module `Record9.XiPrimeAtOneFacts`,
namespace `Zeta23.XiPrime`. Pinned mathlib `51e6992e`, Lean `v4.33.0-rc2`.

Status line: **MACHINE_ACCEPTED_PENDING_AUDIT / REPAIRABLE_GAP (partial promotion)** —
`lake build Record9.XiPrimeAtOneFacts` exits 0, no `sorry`/`admit`/`axiom`. Three of the five
M3-open-A analytic hypotheses have been promoted to real theorems; two remain open.

## Promoted to theorems (machine-checked)

- `IvMT_pos_fact : 0 < IvMT`
- `integral_vMT_forms_fact : (∫ vMT = IvMT) ∧ (∫ vMT² = aMT)`
- `vConvMT_closed_fact : ∀ r ∈ Icc 0 1, vConv vMT r = vConvMTcl r`
- plus helper lemmas: `sqrt_two_pos`, `sqrt_two_ne_zero`, `sqrt_two_mul_half_eq_inv`,
  `one_le_sqrt_two`, `one_div_sqrt_two_le_one`, `one_div_sqrt_two_pos`,
  `one_div_sqrt_two_lt_pi`, `integral_cos_mul`, `integral_cos_mul_add`,
  `integral_cos_sq_mul`.

## Remaining open M3-open-A hypotheses

- `two_integral_vConv_vMT : 2 * ∫₀¹ vConv vMT = (IvMT)^2` (Fubini/autocorrelation identity)
- `jWin_D1_one_vMT_sandwich : J1MT ≤ jWin D1 1 vMT ∧ jWin D1 1 vMT ≤ J1MT + eps9*(IvMT)^2`
  (D₁-certificate sandwich)

These remain as the existing honest-bridge hypotheses in `XiPrimeAtOne.lean`; the conditional
AtOne theorem `kappaXi_one_vMT_mem` still uses them.

## Machine evidence

| Command | Exit | Evidence |
|---|---|---|
| `lake build Record9.XiPrimeAtOneFacts` | **0** | "Built Record9.XiPrimeAtOneFacts (19s)"; "Build completed successfully (8847 jobs)"; only linter hints |
| comment-aware sorry/admit/axiom scan | clean | no `sorry`/`admit`/`axiom` outside comments |

## Next step

Prove `two_integral_vConv_vMT` (Fubini) and `jWin_D1_one_vMT_sandwich` (D₁ certificate
application), then update `XiPrimeAtOne.lean` to use the promoted facts and remove the
corresponding hypotheses.
