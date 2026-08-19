# Obligation graph — Zenodo 22008814 audit

| # | Obligation | Sections | Status |
|---|---|---|---|
| O1 | Hardy gauge q, branch choice, reflection law Z(1−s̄)=Z(s) | §2.1 | FAILED (as extracted; correct relation involves conjugation) |
| O2 | Curvature identity Z Z″−Z′² = ½∂²ₐ[Z(s+a)Z(s−a)]\|ₐ₌₀ (eq 4) | §2.2 | PROVEN (Lean: `ZenodoAudit.curvature_identity`) |
| O3 | Hermitian symmetry of contour matrix A_T | §2.2 | PLAUSIBLE (inherits O1 defect as written) |
| O4 | Inertia invariance rules (Sylvester, codim, rank, HS remainder) Lemma 2.2 | §2 | PROVEN |
| O5 | Stationary residue blocks incl. conjugate-pair block eigenvalues ±\|w\| (Lemma 3.1) | §3 | PROVEN (Lean real-symmetric proxy: `ZenodoAudit.conjugate_pair_block_*`) |
| O6 | Packet evaluation surjectivity (Vandermonde) Lemma 3.2 | §3.1 | PROVEN |
| O7 | Near-lattice packet Riesz bounds Lemma 3.3 | §3.1 | PROVEN |
| O8 | Right-edge arithmetic source / exact HLP algebra | §4–§7 | FAILED (eq (22) drops conjugation; support `n≥2^k`) |
| O9 | One-χ carrier, completed master, common-prefix geometry | §5–§6 | GAP (HLZ diagonalization imported unstated) |
| O10 | Factorially-controlled HLP hierarchy §7.1 | §7.1 | PLAUSIBLE (support typo `2^k`) |
| O11 | Completed global model / spectral lower bound (Schur) | §8 | PROVEN |
| O12 | Auxiliary finite divisor comparison Lemma (Prop 6.8) | §9 | PLAUSIBLE (auxiliary) |
| O13 | Stationary-shell frame / spectral compression / log-unitary Parseval | §10 | PLAUSIBLE (leakage deferred to §12) |
| O14 | Low-edge rank for stationary shifts (Prop 11.1) | §11 | PROVEN |
| O15 | Relative Hilbert–Schmidt bound for regular remainder (Prop 12.4) | §12 | GAP (sign inconsistency; class estimates asserted) |
| O16 | Reduced spectral space / parameter hierarchy | §13 | PROVEN |
| O17 | Finite-dimensional inertia reduction (Lemma 14.1) | §14 | PROVEN |
| O18 | Perturbation generic H + Rouché + final count (Lemmas 15.1–15.2, Thm 1.1) | §15 | GAP (conditional on O15) |

Legend: PENDING / PROVEN / PLAUSIBLE / GAP / FAILED.
