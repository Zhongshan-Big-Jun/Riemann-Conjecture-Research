# Research Ledger — M3-open-A AtOne certificate for κ₁(1,vMT)

Chronological record of the T3-open-A bounded pass. Run
`R-20260816T040000Z-xipAtOne-3078`.

## 2026-08-16 — context load
- Read the flat/quartic AtOne pattern (`Zeta23/XiPrime/Certificate/AtOne.lean`):
  `jWin_one`, `kappaXi_one`, `jWin_one_le_of_le`, `jWin_D1_one_*_le`, `kappaXi_one_*_mem`.
- Read `Defs.lean` §4 for `D1`, `D1trunc`, `vConv`, `jWin`, `cWin`, `kappaXi`;
  `Certificate/D1.lean` for `eps9 = 1024/2990212875`, `D1_le_D1trunc9_add`, `D1trunc_le_D1`.
- Read `reports/xi-prime-mt-window.py` (analytic vConv closed form, dps=120 canonical), the
  A2-audited derivation (`xi-prime-cor22-derivation.md`: H_{ξ′}^{MT} =
  0.8678888651990519355503147104203403132225704976166306446…), the blueprint
  (`admwindow-cos-instance.md`: a=∫v²=0.84922799931830417992…, b=∫v⁴=0.73784297545060818785…,
  profile norms), and `Record9.XiPrimeMT.lean` (H_xip = 2 − κ₁(1,vMT), c9ConstXip).

## Step 1a — exact constants (closed forms), verified
- ∫vMT = 2·sin(1/√2)/√2 = √2·sin(1/√2) = **0.9187253698655684377842315251…** (ARB + quadrature agree).
- a = ∫vMT² = ½ + sin(√2)/(2√2) = **0.8492279993183041799212…** (blueprint `a` ✓).
- b = ∫vMT⁴ = 3/8 + sin(√2)/(2√2) + sin(2√2)/(16√2) = **0.7378429754506081878529…** (blueprint `b` ✓).
- **Discrepancy found & resolved:** `FORMALIZATION_STATUS_XIP.md` line 113 recorded
  `∫_{−1/2}^{1/2} vMT s ds = 0.91872536986556843826…`.  That last digit block is a
  **transcription error**: the true value is `0.91872536986556843778…` (=√2·sin(1/√2)),
  confirmed three ways (closed form, quadrature, and the earlier machine_check.log / audit
  report value `K(0) = √2·sin(1/√2) = 0.91872536986556843778`).  Recorded for the status update.
- Fubini identity: `2∫₀¹ vConv vMT = (∫vMT)² = 0.8440563052346255265…`, verified to 50 digits.
  Note (∫vMT)² = 2 sin²(1/√2) = 1 − cos(√2) (matches the blueprint `‖(v²)′‖₁` row — consistent).

## Step 1b — vConv vMT closed form
- Derived: vConv vMT r = ∫_{−1/2}^{1/2−r} cos(√2s)cos(√2(s+r)) ds
  = ½∫[cos(√2r) + cos(√2(2s+r))] ds = **½(1−r)cos(√2r) + sin(√2(1−r))/(2√2)** (product-to-sum).
- Verified against quadrature at r ∈ {0.1, 0.2, 0.25, 0.5, 0.75} to 40+ digits.
- `vConv vMT r ≥ 0` on [0,1] (sqrt2-based; min on grid = 0.0 at r=1); `vConv vMT r = 0` only
  at r=1.  Needed for the sandwich sign.
- **Bug encountered (recorded):** the first ARB vConv had `/(2·SQ2)` outside-and-inside
  double-division; root-caused against mpmath and corrected to `/SQ2` inside the ½-parens
  (final form matches the derivation).  See also the `arb(mid,rad)` constructor pitfall below.

## Step 1c — the jWin / κ₉ sandwich (ARB)
- J₁ := 2∫₀¹ D1trunc 9 r·vConvMTcl r dr, integrated by composite Simpson (n=20000) with a
  rigorous remainder from a global bound M₄ = max|(D1trunc9·vConv)^{(4)}| on [0,1] computed by
  triangle inequality (`|f^{(4)}| ≤ Σ_i |a_i| + Σ_j |b_j| + Σ_k |c_k|` after reducing f₄ to
  `A(r)+cos(√2r)B(r)+sin(√2r)C(r)` with exact rational coeffs via sympy).  M₄ = 2601.3…;
  Simpson error ≤ M₄·h⁴/180 ≈ 9·10⁻¹⁷ (≪ ε₉ = 3.42·10⁻⁷).
  - **Result: J₁ = 2∫₀¹ D1trunc9·vConv ∈ 0.10633754139274846 ± 2·10⁻¹⁶.**
- **Bug encountered (recorded):** python-flint `arb(mid, rad)` treats its two args as
  (midpoint, radius), NOT (lo, hi).  Naive `arb(lo,hi)` silently produced a correct midpoint
  but radius = upper endpoint, inflating the κ₉ interval to width 0.25.  Fixed with an explicit
  `enc(lo,hi) = arb((lo+hi)/2,(hi−lo)/2)`; the resulting κ₉ width is ~5·10⁻¹⁶.
- **κ₉ = (aMT + J1)/(IvMT)² ∈ [1.132111133800997184…, 1.132111133800997612…]**.
- Sandwich (ARB-certified): `jWin(D1,1,vMT) ∈ [J1, J1 + ε₉·(∫vMT)²]` and
  `κ₁(1,vMT) ∈ [κ₉, κ₉ + ε₉] = [1.13211113380…, 1.13211147625…]`.

## Step 1d — cross-check vs canonical (dps=120)
- Independent mpmath recomputation (`audit_kappa.py`, no shared code with the ARB path):
  κ₁(full D1) = 1.132111134800948064449685289579659686777429502383… ,
  H = 0.86788886519905193555031471042034031322257049761663… ,
  |H − canonical| ≈ 10⁻⁵⁶ — matches to ≥ 56 digits.
- The certified sandwich `[κ₉, κ₉+ε₉]` **contains** the canonical κ₁ (=1.1321111348…);
  `H ∈ [2−(κ₉+ε₉), 2−κ₉]` **contains** the canonical H.  Both "contain" checks = True.
- Difference κ₁(full) − κ₉ ≈ 1.0·10⁻⁹ = the actual D₁ tail /(∫v)², comfortably below ε₉ = 3.4·10⁻⁷,
  so the trunc9 certificate is safely on the correct side.

## Step 2 — Lean (Record9.XiPrimeAtOne)
- Declared the exact AtOne constants (`IvMT`, `aMT`, `bMT`, `vConvMTcl`, `J1MT`,
  `kappaXiOne_MT = κ₉`), the open-obligation `Prop`s (`vConvMT_closed`,
  `two_integral_vConv_vMT`, `integral_vMT_forms`, `IvMT_pos`, `jWin_D1_one_vMT_sandwich`),
  and the honest-bridge theorems `kappaXi_one_vMT_mem` (κ₉ ≤ κ₁ ≤ κ₉+ε₉) and
  `H_xip_vMT_mem` (sharp H range).  Algebra closure proved genuinely from hypotheses;
  the analytic facts are explicit axiom-free hypotheses.
- Verified by `lake build Record9.XiPrimeAtOne` (see machine log); no sorry/admit/axiom.

## Design decisions
- The "exact rational κ₉" of the flat/quartic case cannot be literally Rational for v_MT
  (∫v, a, vConv all contain sin/cos of √2).  The honest AtOne mirror is the REAL constant
  `kappaXiOne_MT = (aMT+J1MT)/(IvMT)²` plus the certified sandwich — numerically enclosed to
  10⁻¹⁶ (width ≪ ε₉).  This is recorded, not hidden.
- Quadrature = EVIDENCE; ARB interval enclosures = rigorous bounds.  Both are labelled as such
  in the scripts and reports.
