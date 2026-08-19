# Adversarial audit report — two-certificate trace-energy deduction (0.673316977…)

- **Candidate**: Yuhang Shi, *A two-certificate trace-energy deduction for simple zeros of the Riemann zeta function*, v0.1.0.
- **Claim audited**: `liminf_{T→∞} N_0^s(T,2T)/N(T,2T) ≥ 0.6733169771424713… > 673316977/10^9`.
- **Artifacts read**: `main.tex` (full), `PROOF_OUTLINE.md`, `CLAIM_LEDGER.md`, `VERIFICATION.md`, `REVIEW_GUIDE.md`, `lean/README.md`, `lean/Audit.lean`, `lean/TwoCertificate/SupportingPlane.lean`, `lean/TwoCertificate/Phi219.lean`, `lean/TwoCertificate/ExactConstants.lean`, plus `RESULT.json`, `UPSTREAM.lock`, `check_upstream_inputs.py`, `exact_check.py`, `joint_check.py`, `verify_release.py`, upstream snapshots, tests, and provenance docs.
- **Local checks run**: `py exact_check.py` PASSED; `py check_upstream_inputs.py` PASSED; `py joint_check.py` PASSED and found best `m=219` with displayed `B = 0.673316977142471313480…`.
- **Lean build**: not independently completed in this environment (local Lean 4.31 vs pinned toolchain `v4.33.0-rc2`; `lake build` timed out fetching/building Mathlib). Static inspection only; no `sorry`/`admit` appears in the Lean sources.

## Verdict table

| # | Obligation | Verdict | Notes |
|---|---|---|---|
| O1 | Scaled finite-dimensional envelope (Lemma 1): spectral case split q≥2, q=1, q=0; identity D=E+2X−q−Q; Cauchy–Schwarz; concavity/chord | **PROVEN** | The manuscript proof is complete as a mathematical argument. The q≥2 case gives D>R; q=1 gives D≥Φ_m(E); q=0 gives D=E. The chord and monotonicity steps close the E<A and E≥A cases. |
| O2 | Two-certificate supporting plane (Lemma 2): piecewise-affine minimization, W₆≥3W₈/4, slope inequality, concavity on [A₇,A₉] | **PROVEN** | As written, the affine branches on [0,A₇] start at R with nonnegative slope, the [A₇,A₉] function is concave with endpoints ≥R and =R, and E≥A₉ is monotone. The extra span/slope hypotheses are valid but later shown by the Lean proof to be unnecessary. |
| O3 | Span comparison `W₆ ≥ 3W₈/4` | **PROVEN** | Coefficientwise gap-multiplicity check is correct: interior multiplicities are 6 vs 8; endpoint multiplicities satisfy the ratio throughout. |
| O4 | Block assembly: shifted partitions, window counting `W_q ≤ q·span`, endpoint `o(N)`, convex pinching, global defect formula | **PROVEN (minor exposition gap)** | The algebra/counting is correct. One small bookkeeping step is implicit: after normalizing G_B to unit diagonal, the certificate energies are only `A_q − o(1)`, and the proof says “continuity of Φ₂₁₉” rather than spelling out the δ-perturbation. This is fixable, not a mathematical flaw. |
| O5 | Global accounting: `D(M) ≥ R S°/m − [β6(m−6)+γ8(m−8)]N/m − o(N)`, substitution into interface | **PROVEN (conditional on imported analytic inputs)** | Shifted-partition counting, `m−q` window multiplicity, and the final rearrangement are correct. Convex pinching, compact-uniform Gram asymptotics, endpoint trimming, and Riemann–von Mangoldt span control are imported, not reproved. |
| O6 | Exact arithmetic: R, u, β, γ, tax identity, final rational comparison | **PROVEN** | `exact_check.py` passes; Lean `ExactConstants.lean` proves `R0_lt_R`, `tax_affine`, and `final_strict_bound`; the manuscript’s one-squaring comparison is valid. Decimal displays are not used as proof. |
| O7 | Lean local layer: supporting plane, Φ₂₁₉ profile, exact constants | **PARTIAL** | The Lean theorems are faithful to the scalar supporting-plane and exact-arithmetic layer and contain no visible `sorry`. However `twoCertificateSupportingPlane` and `concreteSupportingPlane` take `hTrace : R ≤ D ∨ phi E ≤ D` as an explicit hypothesis. The spectral case split that supplies `hTrace` is **not formalized**. Build not independently rerun here. |
| O8 | Trust boundary / imported inputs | **HONEST, with scope limits** | The repo clearly states that the analytic interface and the two interval certificates are pinned imports, not replayed. `check_upstream_inputs.py` verifies blob identities, nonnegative weights, capacities, window identity, and log metadata. It does **not** verify the exhaustive interval searches. |

## Imported-input red-flag review

- **`RESULT.json`**: consistent with the scripts and repository status. It is honest: `trust_boundary` explicitly says the analytic interface and exhaustive certificates were not independently replayed.
- **`UPSTREAM.lock`**: pins the upstream commit, candidate/certificate blob hashes, node counts, and also lists `upstream_proof_blob` and `upstream_verifier_docs_blob`. The local checker verifies only the candidate/certificate blobs and log metadata; the proof/verifier-doc blobs are not checked. This is a completeness caveat, not a deception.
- **`check_upstream_inputs.py`**: passes on the copied snapshots. It verifies exact window identity, nonnegative weights, capacity sums equal to `2`, blob identities, and the presence of `verified=True`/node-count strings in the logs. It does **not** replay the interval searches or verify the actual interval tables.
- **Stale nine-point JSON field**: `interval_certificate_needed: true` and `zero_enumeration_validation.continuous_global_proof: false` remain in the copied candidate file while later certificate logs say `verified=True`. The repository explicitly discloses this in `VERIFICATION.md`; it is a red flag about upstream maturity, but the local repository handles it honestly.

## Overall verdict

**PLAUSIBLE-WITH-GAPS.**

The new finite-dimensional layer — Lemma 1, Lemma 2, span comparison, shifted-block accounting, and exact arithmetic — appears mathematically sound and the local scripts pass. The headline theorem is nevertheless not fully established by this repository alone because:

1. The two upstream interval certificates and the analytic zeta-function interface are imported and not independently replayed here.
2. The Lean formalization stops at a scalar `hTrace` hypothesis; the spectral case split from Lemma 1 is not machine-checked.
3. A small `o(1)`-absorption step in the block-normalization argument is left implicit in the manuscript.

If the imported inputs are accepted, the candidate’s local deduction supports the stated bound and would supersede the project’s `0.673066472675939665848…` record.

## What is machine-proved vs assumed

**Machine-checked in Lean (static inspection; no sorry/admit found):**
- The abstract two-certificate supporting-plane theorem, conditional on:
  - two certificate inequalities,
  - `0 ≤ u ≤ 1`, `β=(1−u)p₇`, `γ=u p₉`, `R=(1−u)A₇+uA₉`,
  - an `EnvelopeProfile`,
  - **the trace disjunction `hTrace : R ≤ D ∨ phi E ≤ D`**.
- The concrete `phi219_profile` (low chord, middle concavity chord, high monotonicity).
- The exact rational identities: `R0 < R`, `R < A₉`, `A₇ < R`, `u` in (0,1), `tax_affine`, and `final_strict_bound > target`.

**Explicitly assumed/imported, not formalized in Lean:**
- The seven- and nine-point interval certificates.
- The arbitrary-window stability inequality `S ≥ H_cert N + tr Ψ(M) − o(N)`.
- The compact-uniform Gram asymptotics, endpoint trimming, convex spectral pinching, and Riemann–von Mangoldt span bound.
- The spectral case split summarized by `hTrace`.

**Mathematically proved in the manuscript but not machine-checked:**
- Lemma 1’s full eigenvalue case split (the source of `hTrace`).
- The block assembly and global defect formula.

## Top risks

1. **Imported nine-point certificate maturity.** The nine-point JSON still contains the stale field `interval_certificate_needed: true` and `zero_enumeration_validation.continuous_global_proof: false`; the repo discloses this and points to later certificate logs, but the large 116,272,426-node run was not replayed here. A defect in that certificate would invalidate the headline.
2. **Analytic interface is a black box.** The stability inequality, Gram asymptotic, endpoint trimming, pinching, and RvM span bound are cited from upstream works. If any of these has an unstated hypothesis (e.g., a required window class or normalization), the global assembly could fail.
3. **Lean `hTrace` gap.** The machine-checked supporting-plane theorem does not prove that a PSD unit-diagonal Gram block satisfies `R ≤ D ∨ phi219(E) ≤ D`; that is exactly Lemma 1’s spectral split. The manuscript proof appears correct, but it is not yet formalized.
4. **Implicit `o(1)` absorption in block normalization.** The transition from unnormalized `G_B` to unit-diagonal `\tilde G_B` changes the certificate right-hand sides by `o(1)`. The intended continuity argument is clear but should be written explicitly for a fully formal block-defect proof.
5. **Certificate semantics are pinned only structurally.** `check_upstream_inputs.py` checks blob hashes, weights, capacities, and window identity. It does not independently confirm that the upstream pair weights are exactly the `w=k_v^2`-kernel coefficients assumed by the manuscript, nor that the verifier’s interval tables were generated from the same window tables. The repository is honest about this, but it is a trust boundary.
6. **Research-draft status.** No independent peer review or end-to-end formalization is claimed. The decimal `0.6733169771424713…` is reproducible by exact/rational and high-precision checks, but the theorem depends on imported results.

## Comparison with our project’s 0.673066… record

Our project’s current record is `C₉(ζ) = 0.673066472675939665848…` (certified k=9 pressure certificate, f₉=0.00392).

- Candidate value: `0.673316977142471313480…`
- Difference: approximately `0.000250504466532` in proportion (`≈0.0250504466532` percentage points).
- The candidate is numerically **higher** and, if its imported inputs are accepted, would **supersede** the project’s record.
- However, the two results use different certificate chains/methods (the candidate builds on `trmdy/zeta-simple-zeros-673137` and its nine-point certificate), so this is not a direct incremental improvement of our own certified pressure-certificate chain; it is a higher external candidate whose imported certificate and analytic interface still need independent review.

## Bottom line

The new finite-dimensional deduction is credible and the exact arithmetic is reproducible. The candidate should remain a **research-draft candidate**, not an independently certified theorem, until the upstream nine-point certificate, the analytic interface, and ideally the `hTrace` spectral split in Lean receive independent verification.
