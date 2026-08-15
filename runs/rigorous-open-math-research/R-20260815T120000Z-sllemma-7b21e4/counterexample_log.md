# Counterexample Log — R-20260815T120000Z-sllemma-7b21e4

Tested edge cases / failed lemmas / model eliminations for SL.

## C1. Atom-at-0 moment characterization (validated the criterion detects atoms)
For μ = c·δ_0 + (1−c)·ν (ν on (0,∞), e.g. exp(1)), the Hankel-ratio Christoffel number
Λ_m(0) = det(H_m)/det(minor00) → **c** (validated numerically for c=0.3,0.5,0.7 → the atom mass).
⇒ An atom at 0 is DETECTABLE and gives a positive Λ-limit. So SL (Λ_m(0)→0) is exactly the
assertion that the limiting μ has NO atom at 0. No contradiction: the sine-Gram has no reason to
have an atom.

## C2. Models ELIMINATED (from prior probe; do not revisit)
- Fixed-lattice Toeplitz Gram sinc(i−j) = I_N (identity): μ=δ₁, fails strongly (0∉supp). Not the model.
- Any model with an atom at 0 (e.g. hypothetic (δ₀+δ₁)/2): fails SL strongly. Not the random-Gram model.
- Route-A operator-spectrum transfer: the sine kernel operator is the projection onto Paley–Wiener
  (spectrum exactly {0,1}); a "small operator eigenvalue → small Gram eigenvalue" reasoning is
  FALSE here because the operator has NO eigenvalues strictly below 1 — small Gram eigenvalues come
  from finite-sample/mixing structure, not the operator spectrum. Kill-verified.

## C3. No-atom does NOT imply 0∈supp (and vice versa) — sharpens what's needed
- μ uniform on [1,2]: μ({0})=0, 0∉supp, yet Λ_m(0)→0 fast (validated: →0 in ≤4 steps). 
- μ with density ρ(x)=x on [0,1]: μ({0})=0, 0∈supp (ρ(0)=0 but 0 in support), Λ_m(0)→0 fast.
Conclusion: Λ_m(0)→0 ⟺ μ({0})=0 regardless of 0∈supp. The condp1 theorem needs ONLY no-atom
(its bound μ((0,∞))=1−μ({0})). Hence "0∈supp" is not load-bearing for this route; no sub-case
where 0∈supp and no-atom is needed but the Christoffel number fails to vanish.

## C4. Moment growth test for the atom at 0 (why m_k growth alone does not decide)
In all three no-atom tests (triangular, linear-vanishing, away-from-0) Λ_m(0)→0, while the atom
test →c>0. The deciding quantity is the full Hankel-ratio sequence, NOT the leading exponent
m_k^{1/k} (which measures the top of the support and is blind to the atom at 0). So the atom-at-0
question is genuinely a "small-end" question balanced against the whole moment sequence.

## C5. My DPP sampler is not a faithful DPP (failed probe, NOT a counterexample to SL)
dpp_higher_moments_probe.py reproduced m_2, m_3 poorly (1.80, 3.90 vs 4/3, 2.0). This is a sampler
defect, not evidence against the moment model. Use the probe's validated projection-DPP simulation
for empirical moments. Documented to avoid re-shipping a broken sampler.

None of C1–C5 contradict SL. SL remains undisturbed as the open (likely true) lemma.
