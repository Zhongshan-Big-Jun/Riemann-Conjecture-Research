# Analysis report — yuhangshi888/zeta-simple-zeros-673316977 (0.673316977…)

**Status label**: `CANDIDATE` / **AUDIT: PLAUSIBLE-WITH-GAPS**.

- **Author**: Yuhang Shi
- **Repository**: https://github.com/yuhangshi888/zeta-simple-zeros-673316977
- **Version**: v0.1.0 (commit `1469eeef…`), Zenodo DOI 10.5281/zenodo.21926962
- **Audit run**: `runs/rigorous-open-math-research/R-20260817T020000Z-shiAudit-7c1e/`
- **Audit report**: `runs/rigorous-open-math-research/R-20260817T020000Z-shiAudit-7c1e/audit_report.md`

## 1. Claim

The repository claims

```
liminf_{T→∞} N_0^s(T,2T) / N(T,2T) ≥ 0.6733169771424713… > 673316977/10^9,
```

a modest improvement over the upstream `trmdy/zeta-simple-zeros-673137` candidate
`0.6733127422722…` and over our project's certified `0.673066472675939665848…`.

## 2. Method

The new step is finite-dimensional:

1. Import (without replay) the analytic stability interface and two certified local
   inequalities (7-point and 9-point) from `trmdy/zeta-simple-zeros-673137` at pinned
   commit `1610b97b…`.
2. Prove a **scaled finite-dimensional envelope** (Lemma 1): for a PSD unit-diagonal Gram
   matrix, `D + ηP ≥ R` whenever `E+P ≥ A`, with `η = Φ_m(A)/A`.
3. Prove a **two-certificate supporting plane** (Lemma 2): using both certificate
   inequalities simultaneously, `D + βW₆ + γW₈ ≥ R`.
4. Average over shifted 219-point blocks and substitute into the stability interface to get
   the final constant.

## 3. Local verification performed

- `py -3.10 verify_release.py` → **PASSED** (manifest, upstream input audit, exact check,
  joint check).
- `py -3.10 -m unittest discover -s tests` → **OK** (3 tests).
- `exact_check.py` → passes exact rational identities and the final strict comparison.
- `joint_check.py` → best `m=219`, `B = 0.673316977142471313480…`.

## 4. Audit verdict: PLAUSIBLE-WITH-GAPS

The new finite-dimensional layer is mathematically sound as written:

- **O1 Lemma 1 (scaled envelope)**: PROVEN — spectral case split q≥2/q=1/q=0 is correct.
- **O2 Lemma 2 (supporting plane)**: PROVEN as written; the Lean formalization shows the
  span/slope hypotheses are unnecessary.
- **O3 span comparison `W₆ ≥ 3W₈/4`**: PROVEN coefficientwise.
- **O4/O5 block assembly and global accounting**: correct; one small `o(1)`-absorption step
  is implicit.
- **O6 exact arithmetic**: PROVEN (both Python and Lean exact constants).
- **O7 Lean local layer**: PARTIAL — supporting plane, `Φ₂₁₉` profile, and exact constants
  are machine-proved, but the spectral case split `hTrace` is left as an explicit hypothesis.
- **O8 trust boundary**: HONEST — upstream certificates and analytic interface are pinned and
  disclosed as not replayed.

### Main gaps

1. The two imported interval certificates (2,168,370-node and 116,272,426-node runs) were not
   independently replayed; only structural source checks were run.
2. The analytic interface (stability inequality, Gram asymptotic, endpoint trimming, convex
   pinching, RvM span bound) is a pinned import, not reproved.
3. The Lean formalization stops at `hTrace : R ≤ D ∨ phi219(E) ≤ D`; the spectral case split
   of Lemma 1 is not machine-checked.
4. A small `o(1)`-absorption step in block normalization should be written explicitly for a
   fully formal proof.
5. The nine-point candidate JSON retains stale fields (`interval_certificate_needed: true`,
   `continuous_global_proof: false`) despite later certificate logs saying `verified=True`; the
   repo discloses this, but it is a maturity concern.

## 5. Lean evidence (current)

The repository's `lean/` project formalizes:

- `TwoCertificate.twoCertificateSupportingPlane`
- `TwoCertificate.Exact.phi219_profile`
- `TwoCertificate.Exact.concreteSupportingPlane`
- `TwoCertificate.Exact.R0_lt_R`
- `TwoCertificate.Exact.tax_affine`
- `TwoCertificate.Exact.final_strict_bound`

Static inspection found no `sorry`/`admit`. The Lean build in our environment is still
fetching/building Mathlib; when it settles, this report will be updated with the exit status.
The known trust boundary is exactly the `hTrace` assumption.

## 6. Comparison with our project

- Our record: `C₉(ζ) = 0.673066472675939665848…` (certified k=9 pressure certificate).
- This candidate: `0.6733169771424713…`, higher by ≈ `0.0002505044665` in proportion.
- **If** the candidate's imported inputs are accepted and the `hTrace` spectral split is
  independently verified, it would **supersede** our record.
- The two results use different certificate chains/methods, so this is not a direct
  incremental improvement of our own certified pressure-certificate chain.

## 7. Recommendation

1. Treat this as a **research-draft candidate**, not an independently certified theorem.
2. The most valuable next steps are:
   - Independently replay or audit the upstream nine-point certificate (116M nodes).
   - Independently review the imported analytic interface.
   - Formalize the missing spectral case split (`hTrace`) in Lean.
3. Record the candidate in the project's literature frontier with status
   `CANDIDATE (PLAUSIBLE-WITH-GAPS)` and pointer to this report.

---

*This analysis is based on the repository as of commit `1469eeef…` and does not replace an
independent replay of the imported certificates.*
