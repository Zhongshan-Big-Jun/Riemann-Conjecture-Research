# Analysis report — Zenodo 22008814: "A Hardy-Gauge Contour Method for Density One of Zeta Zeros on the Critical Line"

**Status label**: `RIGOROUS_PARTIAL_RESULT` / **AUDIT: NOT ESTABLISHED**.

- **Authors**: Chaoyu Hu, Jizheng Chen
- **DOI**: 10.5281/zenodo.22008814
- **Version**: 2026-08-19, 72 pp., non-peer-reviewed Zenodo preprint
- **Audit run**: `runs/rigorous-open-math-research/R-20260817T010500Z-zenodoAudit-9b2c/`
- **Audit report**: `runs/rigorous-open-math-research/R-20260817T010500Z-zenodoAudit-9b2c/audit_report.md`
- **Lean module**: `lean-proof/Record9/Record9/ZenodoAudit.lean`

---

## 1. The claim

Theorem 1.1 asserts, unconditionally,

```
N0,T / NT = 1 − o(1),   hence   N0(T)/N(T) → 1,
```

where `NT = N(T,2T)` counts nontrivial zeros of ζ (with multiplicity) and `N0,T` counts
those on the critical line. This is the **density-one conjecture on the critical line**, a
dramatically stronger statement than any published positive-proportion theorem.

## 2. Methodology

1. **Adversarial proof audit**: a fresh independent auditor read the full 72-page plain-text
   extraction and assigned verdicts (PROVEN / PLAUSIBLE / GAP / FAILED) to obligations O1–O18,
   with the hardest scrutiny on §§10–15.
2. **Targeted Lean verification**: two load-bearing early structural lemmas were formalized in
   Lean 4/mathlib:
   - eq (4) curvature identity (Lemma 2.1/2.2 source),
   - Lemma 3.1's conjugate-pair residue block negative-eigenvalue statement (real-symmetric
     characteristic-polynomial proxy).
   Both compile with `#print axioms = {propext, Classical.choice, Quot.sound}`.

## 3. Audit conclusion

**The main theorem is NOT ESTABLISHED by the written argument.** No internal contradiction
was found, but the proof as written has several false or insufficiently justified load-bearing
steps.

### Strong components (as written)

- **O2 curvature identity**: `Z Z″ − Z′² = ½∂²ₐ[Z(s+a)Z(s−a)]|_{a=0}` — **PROVEN**, and now
  **machine-verified in Lean**.
- **O4 inertia rules**, **O6 packet surjectivity**, **O7 Riesz bounds**, **O11 spectral-floor /
  Schur estimate**, **O14 low-sideband rank bound**, **O16 parameter hierarchy**, **O17
  inertia reduction** — audited as PROVEN (the inertia reduction's `16c₀⁻²` loss is correct).
- **O5 stationary residue blocks** — PROVEN modulo the known overline/bar loss in the plain
  text; the real-symmetric block `[[0,w],[w,0]]` negative-eigenvalue fact is **machine-verified
  in Lean**.

### Fatal or major gaps

1. **O1 branch/reflection law (§2.1)** — **FAILED as written**. The text asserts
   `(q†)² = χ(s)`, but with `q†(s)=q(1−s̄)` the correct square is `χ(s̄)`. The claimed
   reflection `Z(1−s̄)=Z(s)` is not the correct Hermitian symmetry. This threatens the
   Hermitian nature of the central contour form `A_T`.
2. **O8 right-edge pullback (§4.1 eq (22))** — **FAILED as written**. The equality
   `-L1(1−s̄) = -L1(1−s)` drops the anti-holomorphic conjugation; the "exact completed
   right-edge source" is not established.
3. **O15 relative Hilbert–Schmidt remainder (§12 / Prop 12.4)** — **GAP**. Lemma 12.3 has a
   sign inconsistency with eq (105), ten class estimates are asserted rather than fully proved,
   and exhaustiveness of the decomposition `PT + E_edge + R_tri` is not checked term-by-term.
4. **O9 HLZ diagonalization (§6.3)** — **GAP**. A packet-stable diagonalization is imported
   from an external Heap–Li–Zhao lemma with "same proof" extension; exact hypotheses/errors are
   not stated.
5. **O10 HLP support (§7.1)** — **PLAUSIBLE but needs correction**: the printed `n ≥ 2k` should
   be `n ≥ 2^k`.

### Final assembly (§15)

The Rouché/dyadic assembly is logically coherent **conditional** on Proposition 12.5, but
Prop 12.5 depends on the unestablished O15 (and O1/O8). Therefore Theorem 1.1 is not
substantiated.

## 4. Lean evidence

Module `Record9.ZenodoAudit` (mathlib only):

- `theorem curvature_identity (f : ℝ → ℝ) (s : ℝ) (hf : ContDiff ℝ 2 f) : ...` — the
  curvature identity eq (4), machine-proved.
- `theorem conjugate_pair_block_charpoly (w : ℝ) : (conjugatePairBlock w).charpoly = X² - w²`
- `theorem conjugate_pair_block_has_negative_eigenvalue (w : ℝ) (hw : w ≠ 0) : ∃ x < 0, eval x charpoly = 0`
  (real-symmetric proxy for "exactly one negative eigenvalue").

`lake build Record9.ZenodoAudit` exit 0; `#print axioms` = `{propext, Classical.choice,
Quot.sound}`.

This verifies two early algebraic/calculus ingredients, **not** the full proof.

## 5. Relation to our project

- Our project's current record is the **conditional** `C₉(ζ) = 0.673066472675939665848…`
  (k=9, f₉=0.00392, grid-2000, 64.7M nodes), with Stage C Lean formalization in progress
  (T1c-2a block energy already closed).
- If Zenodo 22008814 were correct, density one would supersede our record and render the
  quantitative race obsolete.
- **Our audit does not support that.** The preprint is not in a state where it should replace
  or supersede the project's results. It should be treated as a **high-risk unverified preprint**
  until the O1/O8/O9/O15 gaps are repaired and independently re-audited.

## 6. Recommendation

1. **Do not** import this result as a theorem or update FRONTIER to "density-one proved".
2. Record it in the literature frontier as `unverified preprint, claim = N0/N→1, audit NOT
   ESTABLISHED` with pointer to this report.
3. If the authors or community produce a revision addressing O1/O8/O9/O15, re-run the audit.
4. Next useful Lean targets (from the audit):
   - Prop 8.1 spectral floor `A_G^T ⪰ 0.06 G_T`;
   - Lemma 14.1 rank + relative-HS inertia reduction;
   - Lemma 12.3 (with sign corrected);
   - Prop 11.1 low-sideband rank bound;
   - Lemma 3.3 near-lattice Riesz bounds.

---

*This analysis is a preliminary independent audit, not a formal endorsement or rejection of
the underlying mathematics. The verdict may change after the identified gaps are repaired.*
