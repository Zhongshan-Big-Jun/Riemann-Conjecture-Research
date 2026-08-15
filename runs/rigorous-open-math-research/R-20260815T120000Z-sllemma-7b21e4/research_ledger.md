# Research Ledger — R-20260815T120000Z-sllemma-7b21e4 (SL lemma)

Chronological. Every substantial computation / decision / failure recorded before a near-duplicate
is attempted.

## Step 0 — Contract (done)
Read sl-lemma-random-gram-probe.md (full) + condp1 problem_contract/candidate_proof §2-§5/
status_and_literature. Wrote problem_contract.md with the exact object, the λ role, completion
criteria, and 4 contract ambiguities. 

## Step 1 — Literature pass 7 (done, recorded in status_and_literature.md)
10 web_search queries; confirm no theorem states the random sine-Gram limiting spectral measure.
NEW anchors: Yaskov (least eig of random Gram, Zbl 1381.60024 / ECP19) — i.i.d.-column setting,
not DPP; Shawe-Taylor–Cristianini–Kandola (Gram-vs-operator spectrum, Zbl 1024.68538) — i.i.d.-
sample from measure, not DPP-determinantal sample (the missing link for route A); Bonami–Karoui
sinc-operator = projection ⇒ operator spectrum {0,1}.

## Step 2 — THE REDUCTION (rigorous), status_and_literature §3
Established (using classical Christoffel atom theorem, invoked not re-derived):
  SL's Christoffel form Λ_m(0)→0 ⟺ μ_λ({0}) = 0  (alone).
AND re-examined condp1 Lemma 3.B + F-3: the theorem's bound uses μ_λ((0,∞)) = 1−μ_λ({0}), so the
load-bearing clause is EXACTLY no-atom-at-0 (0∈supp is not separately needed for the ε-theorem).
This sharpens the task: prove μ_λ({0})=0.

## Step 3 — Criterion (rigorous + numerically validated)
Λ_m(0) = 1/K_m(0,0) = det(H_m)/det(H_m with 0th row&col deleted), H_m = (m_{i+j})_{i,j=0..m}.
[First attempt had ratio inverted (computed K not Λ); corrected. Also atom-moments bug: m_0=1.]
Validated against known measures: atom-at-0 (→c>0, no-atom→0), triang (rho>0 →0), linear (rho(0)=0
→0), away-from-0 (→0). **Reproduced Λ_2(0)=5/36 EXACTLY from (1,4/3,2,13/4)** — validates the
criterion against the audited paper value.
Empirical sine-Gram (probe L=50 moments): Hankel-ratio Λ_1=0.111,Λ_2=0.0248,Λ_3=0.0064 — decays
~5x/degree (geometric), consistent with no-atom-at-0 and an MP-like edge at 0. Evidence only.
Command: `py check_christoffel_criterion.py; py check_hankel_from_moments.py`.

## Step 4 — DPP higher-moment probe (in progress, background pwsh-38)
Test whether the non-repeated interaction terms D_k vanish for k≥3 (D_3=D_4=0 known from probe).
If D_k=0 for all k: moments come from repeated-index combinatorics → possible closed form → exact
moment growth → Hankel/Christoffel → SL. Computing raw m_1..m_6 by DPP Monte Carlo.

## Step 5 — Route B general-moment structure
Re-derived m_3 decomposition by hand (matching probe): diag 1 + 3·(1/3) [two-distinct K² terms]
+ D_3 (all-distinct), D_3=0 per probe. Structure: m_k = 1 [all-equal] + (k choose *)·repeated-term
+ D_k. Whether D_k=0 for all k is the decisive open sub-question (being Monte-Carlo tested).

## Step 6 — DPP higher-moment probe FAILED (sampler not faithful)
`dpp_higher_moments_probe.py` used a hand-rolled projection-DPP sampler that does NOT reproduce the
audited exact moments (measured m_2=1.798, m_3=3.90 vs exact 4/3, 2.0). The sampler is defective
(ad-hoc eigen-based selection, not a faithful DPP). Result DISCARDED as evidence. The validated
simulation approach that reproduces the exact moments is the probe's projection-DPP discretization
(reports/sl-lemma-random-gram-probe.md §2); do NOT use my broken sampler. The probe's L=50 moment
list is the trustworthy source and was used for the Hankel/Christoffel computation in step 3.
The exact m_5 shape decomposition (full ρ_5 determinant, 52 set partitions, order-5 signs) is
error-prone by hand; stopped (matches probe's choice to stop at m_4).

## Step 7 — Christoffel-atom theorem literature anchors
Classical result invoked: for a prob. measure μ on ℝ, Λ_n(x)=1/K_n(x,x) → μ({x}) (pointwise at
appropriate x). Anchors: Breuer–Last–Simon "The Nevai condition" (Zbl 1198.42021, math.caltech.edu
SimonPapers/333); Lagomasino–Marcellán–Van Assche "Stability of Asymptotics of Christoffel–Darboux
Kernels" (Commun. Math. Phys. 2014). Used as a theorem, not re-derived.

## Step 8 — Adversarial audit outcome & rebuttal
The external fresh-subagent audit returned. Its sub-verdicts: (1) T1 formula HOLDS; (2) T0a HOLDS
-but-requires-moment-determinacy (satisfied for μ_λ by compact support); (3) T0b load-bearing
internal bound sound, "0∈supp not load-bearing" needs the condp1 text (now quoted); (4) 
SL⟺Hankel-ratio HOLDS as an identity, but finite prefixes don't decide the limit. It FLAGGED the
"Λ₂=5/36 from (1,4/3,2,13/4)" evidence as inconsistent (monotonicity, Cauchy-Schwarz, missing m₄)
and the empirical computation as ill-conditioned.
REBUTTAL (verified): all three inconsistency claims are MIS-INDEXING. The list is (m1,m2,m3,m4)=
(1,4/3,2,13/4) with m0=1 (total mass) separate from m1=1. Under that convention (exact rationals,
verify_lambda2_536_exact.py): Λ_1(0)=1/4, Λ_2(0)=5/36, monotonicity HOLDS (5/36<1/4), Cauchy-
Schwarz HOLDS (4≤13/3), 3×3 Hankel det=5/108>0, and m4 IS present. The auditor's Λ_1=1/9 used the
"1" as m0 and 4/3 as m1 (its own misassignment). High-precision (50-digit mpmath,
verify_empirical_hankel_highprec.py) reproduces the empirical decay exactly (Λ₁=0.11105,Λ₂=0.02476,
Λ₃=0.00641), so the low-order decay is NOT a float artifact.
ACCEPTED from the audit (improvements): make the m0-vs-m1 convention explicit (done in all docs);
state the determinacy condition for T0a (done); note finite prefixes don't decide the limit (this is
gap T2); conditioning caveat at very large order (note added). T0/T1 stand rigorously established.
- Criterion ratio inverted initially (returned K_m(0,0) not Λ_m(0)); fixed.

## Failures / corrections
- atom_moments set m_0=(1-c) erroneously; must be m_0=1 (total mass). Fixed.
- np.math.factorial removed in numpy 2.2.6; use math.factorial. 

## Decisions
- Leader routes B+F (moment computation → Hankel/Christoffel ratio → μ({0})=0). A rigorous
  deliverable: the reduction + criterion turning SL into a moment-growth question, even if the
  exact high moments are not closed this pass.
