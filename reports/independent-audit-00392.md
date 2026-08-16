# Independent Third-Party Audit Report — f₉ = 0.00392 record theorem + certificate (2026-08-15)

**Verdict: PASS-WITH-LIMITS**

Auditor: INDEPENDENT THIRD PARTY (fresh, adversarial; no shared chain of thought with the
solvers/formalizers). Scope: the certified world record of 2026-08-15 — C₉(ζ) =
0.673066472675939665848… and C₉(ξ′) = 0.86920009109661916184…, driven by the k=9 pressure
certificate F₈ ≥ 392/100000.

This report is the third-party re-audit queued by the project (audit-dispatch-prompt.md). It
was produced from artifacts only; every numeric claim was independently re-derived rather
than copied.

---

## Per-item results

| Item | Result | Notes |
|---|---|---|
| B1 certificate integrity | **PASS** | kernel + second-derivative table hashes independently recomputed and **match**; metadata all consistent |
| B2 formula | **PASS** | C₉(ζ), C₉(ξ′), H_MT, H_{ξ′} re-derived to ≥ 50 digits; exact rational identity confirmed |
| B3 chain | **PASS** (with limits) | steps 1–7 re-derived; k=7/k=3 reproductions confirmed; paper-level kernel-limit step is the recorded limit |
| B4 ξ′ transfer | **PASS** | A1–A6 trail read; same certificate serves both families; H_{ξ′} re-derived |
| B5 dependency honesty | **PASS** | certificate is the sole new computational input; no numerical evidence masquerades as proof |
| B6 soundness stack | **PASS** | all 7 sub-items independently checked, incl. down-rounding direction, component superset, +8 truncation slack, loud-fail exit 2, kernel identity, true-min/margin, tangent convexity, range-min validity |
| B7 Lean scope | **PASS** | honest status confirmed: O1 machine-verified; O2/O4/O5 machine-accepted (in progress); O3 (certificate T2) open; no overclaim |

---

## B1 — Certificate integrity: PASS

Certificate file:
`runs/rigorous-open-math-research/R-20260814T131528Z-f9push-d3b58c/reproducibility/certificates/nine-point-f8-gt-392over100000-grid2000.txt`

### Recomputation commands

```bash
# independent kernel + second-derivative table hash (python-flint, py -3.10, PYTHONUTF8=1)
# via zeta_simple_zeros.kernel: build_kernel_table / build_second_derivative_lower_table / table_sha256
grid=2000; cutoff=31368; precision=128; second_start=min(int(0.95*grid), cutoff-2)
```

Result (this audit, independent):

| item | certificate | this audit (recomputed) | match |
|---|---|---|---|
| kernel_table_sha256 | `39a209d3e4a897d982023ab49db27a206401824c769980572433dc4c47387297` | `39a209d3e4a897d982023ab49db27a206401824c769980572433dc4c47387297` | **✓** |
| second_derivative_table_sha256 | `29ca4522e12a991b7ab48943838a174fb2350b328ecc2155d9ecba4cb429f32c` | `29ca4522e12a991b7ab48943838a174fb2350b328ecc2155d9ecba4cb429f32c` | **✓** |
| second_start | 1900 | 1900 | ✓ |
| surviving components | `[[1868,2458];[3511,30823]]`, count 2 | `[[1868, 2458], [3511, 30823]]` (recomputed by independent component code) | **✓** |
| initial_boxes | 256 | `(component count)^8 = 2^8 = 256` (product over the 8 gaps, each choosing one of 2 comps) | **✓** |
| maximum_depth | 80 | ≥ 73 required — 80 ✓ | ✓ |
| nodes | 64,748,524 | pruned+splits = 32,374,390+32,374,134 = 64,748,524 ✓; pruning split tangent 11,393,731 + interval 20,874,136 + pressure 106,523 = 32,374,390 = pruned ✓ | ✓ |
| elapsed | 8,765.75 s @ 8 workers | 70,126 core-s (see Note below) | ✓ (within 20–120k estimate) |
| target | F8 >= 392/100000 | target_n/target_d = 392/100000 → cutoff = 31368 ✓ | ✓ |
| certificate file sha256 | 7F25401A14F897CD1EC26C4B0E0A25A5F87943CFB656329012CB17919280FAC3 | 7F25401A14F897CD1EC26C4B0E0A25A5F87943CFB656329012CB17919280FAC3 | **✓** |

**Minor documentation nit (not a soundness issue):** both the manager audit report (B1 row)
and release-checklist.md state "≈ 34.8k core-s", but 8,765.75 s × 8 workers = 70,126 core-s.
The correct figure is ≈ 70.1k core-s. Either way it lies inside the stated 20–120k core-s
estimate, so B1 is unaffected.

No off-by-one, no hash mismatch. The component superset (see B6) was re-derived
independently and matches exactly at all four boundaries (idx 1867/1868, 2458/2459,
3510/3511, 30823/30824).

---

## B2 — Formula: PASS

Re-derived with pure mpmath (dps=120), independent of project code:

- `f = 392/100000 = 0.00392`, `n = ⌈1/f⌉−1 = 255`, `m = (k−1)+n = 8+255 = 263`, `A₀ = f·n = 2499/2500 = 0.9996 < 1`.
- `(m−1)/(500m) = 262/131500 = 131/65750` (exact).
- `1 − A₀/m = 1 − 2499/657500 = 655001/657500` (exact).
- `657500/65750 = 10` ⇒ `(H − 131/65750)·657500/655001 = (657500·H − 1310)/655001`. Exact identity confirmed.

Computed values (independent):

```
H_MT = 3/2 − (1/√2)cot(1/√2)
     = 0.672500703679411645734379790803295188593403028626264078929589…
C₉(ζ)  = (657500·H_MT − 1310)/655001
     = 0.6730664726759396658483799451499563916698791167063388176448657054…
     claimed 0.673066472675939665848…  ✓ digit-exact to displayed precision

H_{ξ′}^{MT} = 2 − κ₁(1, v_MT)   (recomputed: κ₁ = 1.132111134800948064449685289579659686777…)
     = 0.8678888651990519355503147104203403132225704976166306446…
C₉(ξ′) = (657500·H_{ξ′} − 1310)/655001
     = 0.869200091096619161839954323888625751630669422158034337098576708…
     claimed 0.86920009109661916184…  ✓ digit-exact to displayed precision
```

Both ζ and ξ′ constants match the claim to 55+ digits. The `(657500·H − 1310)/655001` closed
form equals the general form `(H − (m−1)/(500m))/(1 − f·n/m)` to machine zero (abs diff 0.0).

Also re-confirmed: the general-k machinery reproduces k=7, `C₇ = 0.6730085279277797613…`
(mpmath, independent), matching the previously audited extpress record — a strong independent
check that the coefficient identities are correct, not tailored to k=9.

---

## B3 — Chain: PASS (with a recorded, honest limit)

Re-derived steps 1–7 for k=9, m=263:

1. Baseline `S ≥ H_MT·N − o(N)` — **Lean Theorem D, machine-verified** (STATUS.md O1).
2. Stability `S ≥ H_MT·N + Δ(M°) − o(N)` — audited OpenAI Lemma 2.1/Cor 2.2 (paper-level input).
3. Pressure `F₈ ≥ 392/100000` — the new certificate (B1/B6).
4. Block-energy `E_m + (1/500)(y_m−y₁) ≥ f₉(m−8)`; at m=263, `m−8 = 255 = n`, RHS = 0.00392·255 = 0.9996.
5. Block-defect `Δ(G_B) + (1/500)span(B) ≥ A₀ − o(1)`, `A₀ = 0.9996 < 1`.
6. Pinching/averaging `Δ(M°) ≥ (A₀/m)S − ((m−1)/(500m))N − o(N)`, with `A₀/m = 2499/657500`, `(m−1)/(500m) = 131/65750`.
7. Conclusion `(1 − A₀/m)S ≥ (H_MT − (m−1)/(500m))N − o(N)` ⇒ `liminf ≥ C₉`.

Coefficient identities independently confirmed (exact rational):

- `A₀/m = 2499/657500` (i.e. 2499/657500, correct — from 263·2500 = 657500).
- `(m−1)/(500m) = 262/131500 = 131/65750` (exact).
- `1 − A₀/m = 655001/657500`.

The sign conventions are consistent: subtracting the defect terms from the denominator
`(1 − A₀/m)` and from the numerator `(H_MT − (m−1)/(500m))` both increase the lower bound
appropriately (A₀ < 1 keeps the leading coefficient positive).

**Limit (honest, not a gap):** step 5's block-defect uses the *kernel-limit lemma*
`Σ_{i<j}|G_ij|² = ½E_m + o(1)` with uniform `o(1)`. This is a paper-level (audited) statement:
per the project's own STATUS.md, T1c (`Record9.KernelLimit`) is machine-accepted with
"spectral/pinching/uniformity sub-steps carried as honest hypotheses", and the sub-step
proofs are open. The `o(N)`/`o(1)` uniformity and the stability refinement rest on the
previously-audited extpress chain; I found **no circularity and no unproven new step** beyond
what the project itself flags. The only new computational input is the certificate (B5).

No off-by-one found in n=255, m=263, A₀=2499/2500, or the exponents in the conclusion.

---

## B4 — ξ′ transfer: PASS

- `reports/xi-prime-audit-manager.md` (A1–A6) closes at math level: A1 (zero-side block
  structure, incl. `windowZeroSide_atV_of` for `P.atV v_MT`), A2 (κ₁(1,v_MT) computed by two
  independent paths), A3 (kernel-limit transfer verbatim — same kernel class), A4 (RvM &
  trace), A5 (arithmetic), A6 (certificate dependency, same kernel).
- `reports/admwindow-cos-instance.md` supplies the math-level AdmWindow/ModFactor blueprint
  for `v_MT = cos(√2s)` (all elementary bounds verified at 40 digits; A=1, B=2, c = cRho+4).
- **Same certificate serves both families** because F₈ depends only on the window-determined
  kernel `w = k²` (k = K/K(0) from the MT window), which is independent of ζ vs ξ′. The
  verifier's kernel table is generated from the same kernel (B6/v), so the certified
  `F₈ ≥ 392/100000` transfers verbatim to the ξ′ chain.
- The H_{ξ′} input for the constant was re-derived here: `H_{ξ′}^{MT} = 0.86788886519905193555…`
  (matches the claim to 50+ digits), and `C₉(ξ′) = 0.86920009109661916184…` confirmed (B2).

Limit (consistent with project's own stance): the ξ′ chain is paper/computer-level; the Lean
`admWindow_phiV_MT` instance and the AtOne κ₁(1,v_MT) sandwich are Stage-C items reported
"open" in STATUS.md O5. Not a math gap, but not fully formalized.

---

## B5 — Dependency honesty: PASS

- The only new computational input over the audited extpress record is the f₉=0.00392
  certificate (which is itself the only new input in `candidate_proof.md`: "only the
  certificate changes").
- No numerical evidence is presented as proof. The "true minimum ≈ 0.00395005" and the
  margin ≈ 3e-5 are documented as scoping/numerical context; the theorem rests on the
  rigorous finite certificate `F₈ ≥ 392/100000`, which is what the release claims.
- The 0.00395 target was explicitly WITHDRAWN as infeasible (noted in candidate_proof.md,
  release-checklist.md, f9-ladder.md CORRECTION) — an honest handling of a failed target.
- The certificate file is byte-identical to the recorded sha256.

---

## B6 — Soundness stack: PASS

Adversarial code-reading of `verify_kpoint_parallel.py`, `kernel.py`, `rounding.py`,
`report.py`. All seven sub-items independently checked:

**(i) Down-rounding — conservative ✓.**
`down_ratio` = `nextafter(n/d, −inf)` (strict binary64 lower bound of a nonnegative rational);
`down_mul` = `nextafter(l·r, −inf)` clamped ≥ 0; `down_add` = `nextafter(l+r, −inf)` clamped ≥ 0.
All are valid lower bounds. `target_upper = up_ratio(392,100000) = 0.003920000000000001` is an
upper bound of the exact target, so `lower ≥ target_upper` ⇒ `F₈ ≥ 392/100000`. Direction sound.

**(ii) Component superset — sound (re-derived).**
For cell `idx`, the survivor test is `ub(idx) = down_ratio(idx, grid·P_DEN) +
down_mul(coeff1, table[idx]) < target_upper`, with `coeff1 = down(2/(k−1)) = down(1/4)`.
This is a valid *necessary* condition: if a single gap `g_j` lies in cell `idx`, then (linear
term from `g_j` alone) `≥ idx/(grid·4000)`, and (span-1 single-gap kernel term)
`≥ (1/4)·w_min(idx)`, so `F₈ ≥ down_ratio(idx, grid·P_DEN) + down_mul((1/4), table[idx])`.
If that ≥ `target_upper`, no counterexample can contain a gap in cell `idx` — the cell is
safely excluded. The contiguous runs form a **superset** of all cells that can appear in a
counterexample; enumerating `product(comps, repeat=8)` covers every potential counterexample
box. Independent recomputation gave exactly `[[1868,2458];[3511,30823]]`, count 2, and all
four boundary cells flip exactly at the recorded cutoffs. **Sound.**

**(iii) Truncation +8 slack — verified.**
`cutoff = ⌊(392/100000)·4000·2000⌋+8 = 31360+8 = 31368`. The pre-prune
`if sum(lo_i) >= cutoff` is sound because the linear term alone then exceeds the target:
`min linear = sum_lo/(grid·P_DEN) ≥ 31368/8,000,000 = 0.003921 > target_upper`. Independently
checked the last in-table cell: linear-only at idx 31367 = `0x1.00f55de58e64ap-8` =
0.003920875 > target_upper `0x1.00e6afcce1c59p-8` = 0.003920000000000001. So no
counterexample needs a gap cell ≥ cutoff, and the +8 slack makes the boundary airtight with
margin.

**(iv) Loud-fail exit 2 — in code.**
`_process_slice` returns `fail=True` when a fully-refined (width-0) box still cannot be
proved ≥ target; `main` then prints `FAILED at …` and `sys.exit(2)`. A genuine
counterexample forces an exit code 2, so the certificate cannot silently pass a false claim.
The 0.00395 runs failed exactly this way — confirming the machinery actually exercises the
loud-fail path. **Conservative (no false positives).**

**(v) Kernel identity — consistent.**
The verifier imports `zeta_simple_zeros.kernel` (the project kernel); the table is built by
`build_kernel_table` → `squared_kernel_cell_lower` → `normalized_kernel` (= K(x)/K(0),
K(x)=∫cos(√2t)cos(2πxt)dt), squared with down-rounding. This is exactly the `w = k²` in the
F₈ pressure function of the chain. Kernel symmetry k(−x)=k(x) lets the table cover all
nonnegative gaps. **Identical kernel.**

**(vi) True-minimum story — documented honestly.**
The withdrawn 0.00395 (true min ≈ 0.00395005, margin ≈ 5e-8 < bound loss ≈ 1e-5) vs the
certified 0.00392 (margin ≈ 3e-5) is consistent with the certificate passing at a
comfortably larger margin. The earlier "0.0039818" was a local minimum, correctly superseded.
This is numerical context, not proof — and it is presented as such.

**(vii) Tangent-pruning convexity — sound.**
`s = coeff_signed(span, second_min(L,R))` is a pointwise lower bound of the Hessian block
coefficient (sign-aware coefficient rounding + nextafter-down + min-of-cell lower bounds).
Each `J_block` (all-ones) is PSD, so `H ⪰ Σ s·J_block = M`; `arb_PD` (exact Arb Cholesky with
`pivot > 0`) is the authoritative PD check, and `in_heuristic` is only a fast pre-filter whose
false-negatives merely skip tangent pruning (conservative). For convex F₈, the first-order
enclosure `value − Σ|∇F_j|·r_j` (exact rational midpoints, arb kernel eval, upper-rounded
`|drv|`) is a rigorous lower bound compared against the exact rational target. Any
precondition failure returns `None` (no prune). `squared_kernel_derivatives` divides by z³ but
the smallest mid (~0.934, cell 1868) still has `z = πx − 1/√2 ≈ 2.227 > 0` — no pole; the
docstring's "x ≥ 0.95" is conservative, not a correctness boundary. **Sound.**

**Range-min validity (kernel + second-derivative tables):** `RangeMinimum` is a sparse table;
`query(left,right)` returns `min` over two length-`2^level` intervals that overlap and jointly
cover `[left, right]`, so it is the exact range minimum of the (lower-bound) entries, and is
thereby a valid lower bound for `min w`/`min w''` over the covered cell range. Where `right ≥
length`, `kernel_min` returns 0.0 and `second_min` returns −inf — both conservative (no
over-estimate). **Valid lower bounds everywhere.**

---

## B7 — Lean/formalization scope: PASS

`lean-proof/STATUS.md` is honest:

- **O1 baseline** (`thmD₀_simple_mult`, Zeta23/ThmD) — machine-verified (`lake build` exit 0,
  9010 jobs; gold-standard axioms).
- **O2 (chain9_eps), O4 (record_c9), O5 (ξ′)** — **MACHINE-ACCEPTED** (compiles, gold
  axioms) but gated on open sub-steps (T1c kernel-limit sub-proofs; T3 AtOne κ₁ sandwich,
  xiChain bridge, L¹-norms).
- **O3 certificate (T2)** — **OPEN** (not yet formalized).
- The claim under audit is labeled `RIGOROUS_PARTIAL_RESULT (certified record)` — accurate.
  No FORMALLY_VERIFIED overclaim for the chain+certificate; the formalized part is precisely
  the baseline. **No overclaim.**

---

## Critical findings

1. **No hash mismatch, no off-by-one, no rounding-direction error, no component-superset
   gap, no truncation flaw** found. The claim's arithmetic and the verifier's bound
   directions are sound.
2. **Independently confirmed** the two constants to 55+ digits and both kernel/2nd-derivative
   table hashes byte-for-byte, plus the k=7 reproduction of the general chain (strong
   cross-check of the coefficient identities).
3. **Recorded limits (already acknowledged by the project, not new gaps):**
   - The chain's kernel-limit uniformity (`o(1)`) and stability refinement are paper-level;
     T1c sub-step proofs and T2 (certificate formalization) are open.
   - The ξ′ chain is paper/computer-level; the Lean `admWindow_phiV_MT` / AtOne κ₁ sandwich
     are Stage-C open items.
   - The verifier's own soundness is established by code-reading + byte-identical table
     reproduction, not by a proof assistant.
4. **Minor documentation nit:** "≈ 34.8k core-s" should read ≈ 70.1k core-s (8,765.75 s × 8
   workers = 70,126); magnitude still well inside the 20–120k estimate, so no material impact.

## Governance / file provenance

- This report: `reports/independent-audit-00392.md` (created; no existing file overwritten).
- No Lean files or project artifacts were modified. Temporary mpmath/flint scratch was run
  inline (not committed) and removed.

## Recommended follow-ups (for the project)

- Optionally correct the core-s figure in release-checklist.md / audit_report.md (cosmetic).
- Continue the Stage C formalization toward T2 (certificate reflection) and close the T1c
  sub-step proofs and ξ′ AtOne/AdmWindow items; the record's unconditional status does not
  depend on these, but full FORMALLY_VERIFIED does.
