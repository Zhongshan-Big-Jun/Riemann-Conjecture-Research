# Adversarial Audit Report — Zenodo 22008814
**Paper**: Hu & Chen, *A Hardy-Gauge Contour Method for Density One of Zeta Zeros on the Critical Line*, DOI 10.5281/zenodo.22008814.
**Audited text**: `reproducibility/zenodo-22008814-main.txt` (4952 lines, plain-text extraction).
**Claim**: Theorem 1.1, `N0,T/NT = 1-o(1)` and hence `N0(T)/N(T) -> 1`.

This is an independent proof-structure audit. No numerical evidence is used as proof. Verdicts are based on the written argument in the supplied plain-text extraction.

---

## 0. Verdict summary for obligations O1–O18

| # | Obligation | Verdict | One-line evidence |
|---|---|---|---|
| O1 | Hardy gauge q, branch choice, reflection law | **FAILED** (as extracted; repairable) | The text asserts `(q†)^2 = χ(s) = q(s)^{-2}` for `q†(s)=q(1-\bar{s})`; actually `q†(s)^2 = χ(\bar{s})`, so `q† = q^{-1}` cannot hold globally. The correct relation is `q† = 1/\overline{q}` and the reflection law must involve conjugation. |
| O2 | Curvature identity (eq 4) | **PROVEN** | Direct derivative identity `Z Z''-Z'^2 = ½∂²_a[Z(s+a)Z(s-a)]|_{a=0}`; algebraic and already a Lean target. |
| O3 | Hermitian symmetry of `A_T` | **PLAUSIBLE** | Would follow from a corrected reflection law and `B_{v,w}(s)` polarization; as written it inherits the O1 branch defect. |
| O4 | Inertia invariance rules (Lemma 2.2) | **PROVEN** | Sylvester, codimension, rank, and the HS-remainder rule are standard; the last is later proved in Lemma 14.1. |
| O5 | Stationary residue blocks (Lemma 3.1) | **PROVEN** | Residue computation gives `-L^{-2}H(c)H''(c)`; conjugate pair has eigenvalues `±|w|` (the block must be Hermitian, so the second off-diagonal is `\bar{w}`; the plain text drops the bar). |
| O6 | Packet evaluation surjectivity (Lemma 3.2) | **PROVEN** | Vandermonde plus real-analytic determinant nonvanishing on an open box. |
| O7 | Near-lattice packet Riesz bounds (Lemma 3.3) | **PROVEN** | Plancherel with flat interval orthogonality; perturbed centres give `o(1)` Gram perturbation. |
| O8 | Right-edge arithmetic source / exact HLP algebra | **FAILED** (as written; partly repairable) | The right-edge pullback identity (22) contains the false/unjustified equality `-L1(1-\bar{s}) = -L1(1-s)` (conjugation is dropped). Lemma 7.1's support statement `n ≥ 2k` is also insufficient for Prop 7.2 unless the intended statement is `n ≥ 2^k`. |
| O9 | One-χ carrier / completed master / common-prefix geometry | **GAP** | The packet-stable HLZ diagonalization (Lemma 6.3) is imported from an external theorem and only asserted to extend by "the same proof"; the exact hypotheses and error constants are not stated or verified. |
| O10 | Factorially controlled HLP hierarchy (§7.1) | **PLAUSIBLE** | Prop 7.2's induction is coherent, but the written support condition in Lemma 7.1 must be `n ≥ 2^k` for the `v ≪ log x` step; as printed `n ≥ 2k` is too weak. |
| O11 | Completed global model / spectral lower bound (Schur) | **PROVEN** | Prop 8.1 gives explicit rational interval bounds for `G`, sign pattern, and Schur row sum; the finite computation is complete as written. |
| O12 | Auxiliary finite divisor comparison (Prop 6.8) | **PLAUSIBLE** | The divisor factorization and Möbius inverse norm are sketched with coarse `Y^{o(1)}` losses; auxiliary only, not used in the invariant source. |
| O13 | Stationary-shell frame / spectral compression / log-unitary Parseval / nonstationary leakage | **PLAUSIBLE** | The exact Parseval and shell-frame estimates are coherent; the nonstationary leakage sum is deferred to Prop 12.4 and not fully carried out in §10. |
| O14 | Uniform rank bound for low-sideband stationary shifts (Prop 11.1) | **PROVEN** | Geometric edge-space dimension `≪ T/J_j^2 + R_j + 1`; the shell sums give `O(T)` plus `o(T)` enlargement. |
| O15 | Relative Hilbert–Schmidt bound for regular remainder (Prop 12.4) | **GAP** | Lemma 12.3's primitive identity (165) has a sign inconsistent with the correctly signed (105); moreover the ten class estimates in Prop 12.4 are asserted with deferred constants and several imported error classes (especially (ix)) are not independently justified. |
| O16 | Reduced spectral space / parameter hierarchy (§13) | **PROVEN** | The order of constants is explicit and non-circular; `codim V_mean = o(NT)` and `codim Pret_T = o(NT)` follow from the stated choices. |
| O17 | Finite-dimensional inertia reduction (Lemma 14.1) | **PROVEN** | The spectral subspace argument gives codimension `≤ r + 16 c_0^{-2} s`; the `16 c^{-2}` claim is correct. |
| O18 | Generic perturbation H + Rouché + final count (Lemmas 15.1–15.2, Thm 1.1) | **GAP** | The Rouché/dyadic assembly is logically sound *conditional* on Prop 12.5, but Prop 12.5 depends on the unestablished O15; the count identity Lemma 15.2 itself is correct once the zero-side identity (14) is accepted. |

---

## 1. Section-by-section audit

### §1–§3: Hardy gauge, contour form, zero-side residue representation

**Strengths.** The contour form `A_T` and the zero-side residue representation are coherent in outline. Lemma 3.1's residue calculation is correct. Lemmas 3.2–3.4 give a credible packet-evaluation mechanism: enough packet centres, surjective evaluation onto stationary nodes, and uniform Riesz bounds. Lemma 3.7 and Proposition 3.10 are standard Rolle/Jensen material and are plausible.

**Critical problems.**

1. **Branch/reflection law (§2.1, eq (2), O1).** The text defines `q(s)=χ(1-s)^{1/2}` and `q†(s)=q(1-\bar{s})`. It then asserts
   `(q†)^2 = χ(s) = q(s)^{-2}`.
   In the standard normalization `χ(s)χ(1-s)=1`, one has
   `q(s)^2=χ(1-s)`, so `q(s)^{-2}=χ(s)`, but
   `q†(s)^2 = χ(1-(1-\bar{s})) = χ(\bar{s})`.
   Thus `q†` and `q^{-1}` have different squares off the critical line. The claimed global identity `q†=q^{-1}` is not justified and is false in general. The correct relation is `q† = 1/\overline{q}` (up to branch sign), and the reflection law should be
   `Z(1-\bar{s}) = \overline{Z(s)}`.
   The extracted text writes `Z(1-\bar{s}) = Z(s)` (eq (2)) and later `F(\bar{z}) = F(z)`, which are also not the correct real-symmetry identities for a holomorphic complex-valued function. If these are plain-text overline losses, the proof must still be repaired; as written this is a foundational wrong statement.

2. **Hermitian symmetry (§2.2, O3).** The conclusion `A_T(w,v)=\overline{A_T(v,w)}` is plausible with the correct reflection law, but the written proof inherits the O1 defect and is therefore not independently established.

3. **Conjugate-pair block (§3.1, O5).** The plain text displays the block as `[[0,w],[w,0]]` while the characteristic polynomial `λ²-|w|²` requires the Hermitian block `[[0,w],[\bar w,0]]`. This is a minor notation/overline issue, not a substantive gap.

### §4–§7: Right-edge arithmetic source, HLP hierarchy, common-prefix geometry

**Strengths.** The algebraic identities (20), (21), and Lemma 4.1 are correct in substance: `Z1(s)=-χ(s)Z1(1-s)`, the curvature source `CZ=q²(ζ²Q+f'ζ²)`, and the nonnegative coefficients `c(n)` are standard. The HLP geometric-series expansion (70) is unconditional on the absolute-convergence line. The factorial majorant in Prop 7.2 is a plausible induction.

**Critical problems.**

1. **Right-edge reflection/pullback (§4.1, eq (22), O8).** The derivation of the completed right-edge source contains
   `-L1(1-\bar{s}) = -L1(1-s) = L1(s)-χ'/χ(s)`.
   The first equality is not a holomorphic substitution: `s ↦ 1-\bar{s}` is anti-holomorphic, while `s ↦ 1-s` reverses the sign of the height. In general `L1(1-\bar{s}) \neq L1(1-s)`. A correct Hermitian pullback must carry a conjugation; the displayed identity is false as written. This threatens the "exact completed right-edge source" `f+L1` and the whole arithmetic-side representation.

2. **HLZ diagonalization (§6.3, O9).** Lemma 6.3 asserts a packet-stable version of the Heap–Li–Zhao diagonal calculation with error
   `T^{-2/\log_3 T}(\log T)^{C \log_3 T} + (\log T)^{-A}`.
   The proof says "Applying the same proof to `H0W`" and absorbs all packet derivatives into constants. No statement of the underlying HLZ lemma, its hypotheses, or the exact contour deformation is given. Since this is a load-bearing bridge between the physical packet weight and the diagonal Mellin model, the argument is not independently verifiable from the text.

3. **HLP support condition (§7.1, O10).** Lemma 7.1 states `Λ_k(n)\neq0 ⇒ n ≥ 2k`. The proof says every term is a product of `k` integers at least 2, which gives `n ≥ 2^k`. The weaker printed condition `n ≥ 2k` is insufficient for the `v = 2k-3 ≪ \log x` requirement in Prop 7.2. This is almost certainly a typo (`2^k` rendered as `2k`), but as written it is a gap in the factorial-control argument.

### §8: Completed global model and spectral lower bound

**Assessment: O11 PROVEN / PLAUSIBLE.** Proposition 8.1 is unusually detailed: closed form (109), exact rational interval bounds (114)–(116), strict convexity of `g`, and Schur's test with `a_G > 5.677 > 5.535`. The argument is complete *as written* provided the listed interval arithmetic is correct. This is a good Lean target. The only caveat is that the sign convention in Lemma 12.3 conflicts with the sign in (105) (see below); Prop 8.1 itself uses the correct sign.

### §9: Auxiliary finite divisor comparison

**Assessment: O12 PLAUSIBLE.** Propositions 6.8, 6.9 and §9 record finite arithmetic comparison maps. For the invariant source the paper specializes to `d=e=1`, so this material is auxiliary. The Möbius inverse bounds are sketched with coarse `Y^{1+o(1)}`/`Y^{10+o(1)}` losses. No fatal issue is apparent, but the section is not load-bearing for the main invariant-source decomposition.

### §10: Stationary-shell frame, spectral compression, log-unitary Parseval

**Assessment: O13 PLAUSIBLE.** The exact isometry (135), log-unitary measure identity (138), bounded-overlap partition (139), and Parseval identity (144) are correct. Lemma 10.1's stable-core frame and Lemma 10.2's shell-local primitive comparison are coherent. The nonstationary leakage is only sketched in §10 and the main quantitative bound is deferred to Prop 12.4; this is acceptable structurally but not complete in §10. The shell enlargement sum `Σ R_j = o(NT)` is consistent with `A0 > B+3`.

### §11: Uniform rank bound for stationary shifts

**Assessment: O14 PROVEN.** Proposition 11.1 is a purely geometric rank bound. For `m∈I_j=[A_j,B_j]`, every compressed shift `P_j S_m P_j` has range in a common edge interval of length `≪ B_j - 2A_j + 2R_j + 1`. The sums
`Σ T/J_j² ≪ T`, `Σ R_j = o(T)`, `Σ ϵ_L d_j = o(T)`
are valid under the §13 parameter choices. The conclusion `rank E_shift^T ≪ T = o(NT)` follows.

### §12: Reference metric and regular remainder

**Assessment: O15 GAP.** This is the least complete section.

- **Lemma 12.3 sign inconsistency.** The text defines
  `JD(x)=∂_x D(x,x+)-∂_x D(x,x-)`
  and then states
  `∫∫ D(x,y)q(x)q(y) = ∫ JD(x)|Q(x)|² + ∫∫ D^{reg}_{xy} Q(x)Q(y)`.
  For `D(x,y)=C(|x-y|)` this gives the wrong sign: `∂_x∂_y C(|x-y|) = -2C'(0+)δ`, so the cusp term should be `-∫ JD |Q|²`, exactly as in the correctly signed (105). The later norm estimates are insensitive to this sign, so the error is likely repairable, but the lemma as written contradicts (105).

- **Class estimates are asserted, not proved.** Proposition 12.4 splits the remainder into ten classes and gives bounds such as (102), (171), (173), and (151). Many of these depend on "fixed losses", "the same calculation", and constants chosen later in §13. In particular class (ix) (HLZ diagonalization error) is controlled only by the imported Lemma 6.3 and the assertion that the error "has no independent stationary carrier index"; this is not demonstrated.

- **Exhaustiveness/decomposition is not formally checked.** The proof asserts mutual exclusivity and exhaustiveness of the classes by "the level split at `K0`" and the stable-core split, but does not provide a term-by-term accounting that every exact source term lands in exactly one of `PT`, `E_edge`, or `R_tri`. For a proof whose entire weight rests on this decomposition, this is a substantial missing formal step.

### §13: Reduced spectral space and parameter hierarchy

**Assessment: O16 PROVEN.** The order of choices is explicit: `Cpkt`, `D`, `Creg`, `Adiag`, `σ`, `M*`, `N`, `B`, `Msb`, `Csb`, `A0`. There is no obvious circularity. Lemma 13.1 gives `codim V_mean = o(NT)` and with Lemma 10.1 and (185) gives `codim Pret_T = o(NT)`. This section is sound.

### §14: Finite-dimensional inertia reduction

**Assessment: O17 PROVEN.** Lemma 14.1 is correct. After whitening by `G`, `E` is killed on the orthogonal complement of its range, and the spectral subspace of `R` with `|λ|≥c0/4` has dimension `≤16 c0^{-2} s`. Thus `A` is positive on a subspace of codimension `≤ r + 16 c0^{-2}s`, and the ambient-codimension statement (190) follows from the intersection inequality.

### §15: Generic perturbation, Rouché, and final count

**Assessment: O18 GAP (conditional assembly).** The final section is logically coherent *assuming* Proposition 12.5:

- Lemma 15.1 is a standard fixed-`T` generic perturbation argument; the compactness/continuity step for (191) is valid.
- Lemma 15.2's identity `D(H)=B(H)+P(H')+o(NT)` follows from the homotopy count (194), Lemma 3.7, and real symmetry.
- The Rouché step `D_good(F) ≤ D(H)` and the final dyadic summation are correct.

However the theorem depends critically on `n_-(AH)=o(NT)`, which is obtained by applying Lemma 14.1 to `AH = (PT+Δ)+E+R` with `PT+Δ ⪰ 3c0/4 G`. The positivity of `PT+Δ` is established only through Prop 12.5, which in turn rests on the unproved O15 (and on the O1/O8 branch/reflection issues). Thus the final theorem is not established by the written argument.

---

## 2. Most serious risks and gaps

1. **Branch/reflection law (O1, §2.1).** As extracted, `(q†)^2 = χ(s)` is false; the correct identity involves `χ(\bar{s})` and conjugation. This undermines the Hermitian symmetry of `A_T` and the "same invariant Hermitian object" on which the whole method depends.

2. **Right-edge pullback identity (O8, §4.1 eq (22)).** The equality `-L1(1-\bar{s})=-L1(1-s)` drops the conjugation inherent in the Hermitian reflection `s ↦ 1-\bar{s}`. The exact completed right-edge source `f+L1` is not established as written.

3. **Relative Hilbert–Schmidt remainder (O15, §12 / Prop 12.4).** The central eps/delta bridge is the least rigorous part: Lemma 12.3 has a sign inconsistency with (105), and the ten class estimates plus exhaustiveness are asserted rather than proved. This is the main reason the main theorem is not substantiated.

4. **HLZ diagonalization with packet weight (O9, §6.3).** Lemma 6.3 depends on an unstated external theorem and an unverified "same proof" extension to packet Mellin weights. If this step fails, the principal term `PT` is not the correct diagonalization.

5. **Factorial support condition (O10, §7.1).** The printed `n ≥ 2k` is insufficient for Prop 7.2; the proof requires `n ≥ 2^k`. This is likely a typo but must be corrected for the HLP hierarchy to be airtight.

---

## 3. Overall assessment

**Main theorem `N0(T)/N(T) -> 1`: NOT ESTABLISHED by what is written.**

The paper has a coherent high-level architecture and several individually correct components (packet lemmas, rank bound, inertia lemma, spectral-floor computation). But the load-bearing analytic bridges — especially the branch/reflection algebra, the right-edge pullback, the HLZ diagonalization, and the relative Hilbert–Schmidt remainder — contain false or insufficiently justified statements. The conclusion is not contradicted by anything in this audit, but the proof as written does not meet the standard of an independent proof.

---

## 4. Recommended Lean targets (beyond eq (4) and conjugate-pair eigenvalues)

1. **Proposition 8.1 (spectral floor `A_G^T ⪰ 0.06 G_T`)** — a finite explicit real-analysis/interval-arithmetic theorem; formalizing it would certify the crucial positivity of the model.
2. **Lemma 14.1 (rank + relative Hilbert–Schmidt inertia reduction)** — a pure finite-dimensional linear algebra lemma; formalizing it would validate the `16 c^{-2}` loss and the final inertia step.
3. **Lemma 12.3 (two-variable primitive remainder criterion)** — with the sign corrected; this is the analytic heart of the `o(NT)` HS-remainder estimates and can be formalized for piecewise `C^2` kernels.
4. **Proposition 11.1 (low-sideband stationary shift rank bound)** — a discrete/finite-rank geometric statement that is well-suited to Lean and independent of analytic number theory.
5. **Lemma 3.3 (near-lattice packet Riesz bounds)** — Fourier/Plancherel and Gram perturbation; formalizing it would secure the packet frame used throughout.
