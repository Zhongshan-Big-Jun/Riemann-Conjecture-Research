# Approach Registry — R-20260815T120000Z-sllemma-7b21e4

Routes to prove SL (= μ_λ({0}) = 0, equivalently Λ_m(0)→0 for the limiting spectral measure of
the random sine-DPP Gram matrix). Owner: solver. State: per-route.

## Route A — Operator/spectral-theory connection (sine kernel = orthogonal projection)
State: **OPEN, dependence gap identified.**
Idea: the sine kernel K is the projection onto Paley–Wiener space (Fourier symbol 1_{[-1/2,1/2]}),
so K∘K=K, spectrum {0,1}. The Gram matrix of point samples G_ij=K(x_i,x_j). Relate empirical
spectral measure of the random Gram to the *operator* spectrum via the point-process structure.
Gap: Shawe-Taylor–Cristianini–Kandola's Gram-vs-operator bound is for i.i.d. samples from a
measure; the sine *determinantal* sample is not i.i.d. The operator has no eigenvalues strictly
below 1 (projection), so a naive "small operator eigenvalues" transfer fails — the small Gram
eigenvalues must come from the *finite-sample / identity-mixing* structure, not from the operator.
Needs: a DPP-specific concentration replacing the i.i.d. kernel-PCA bound. No easy theorem found.
Status: not the fastest route; recorded.

## Route B — Moment route: exact m_k for all k from DPP factorial moments
State: **MOST PROMISING, partially executed.**
Idea: E[m_k] for the sine-DPP Gram is computable exactly via ρ_k = det[K] and the sinc-kernel
integrals. We have m_1..m_4 exact (accepted: 1, 4/3, 2, 13/4). Key conjecture being tested: the
"all-distinct" (non-repeated-index) terms D_k VANISH for all k (D_3=D_4=0 found; structural,
via projection idempotence + determinant sign cancellation). If D_k=0 for all k, the moments come
from a simpler "self-avoiding/repeated" combinatorics that may yield a closed form. Then feed into
the Hankel / Christoffel ratio criterion (Route F). 
Sub-task being executed THIS run: extend to m_5..m_8 via (a) exact shape decomposition if tractable,
and (b) DPP Monte-Carlo (evidence only) to identify the pattern and conjecture the closed form.
Gap to closure: even with all D_k=0, need to prove the resulting moment sequence has the 
Hankel-ratio →0 property (no atom at 0); this needs moment determinacy + Hankel/det asymptotics
of the specific sequence. Being attacked via exact moment asymptotics (Route F).

## Route C — Direct small-eigenvalue / concentration bounds
State: **OPEN, partial literature.**
Idea: bound P(λ_min(G_L) ≤ δ) via K²-integrals and Ledoux/Dudley-type concentration for DPPs
(finding a "most likely" co-rank-1 vector near the nullspace; use the DPP to control the projection
onto low-frequency/band-limited functions). 
Gap: a rigorous concentration bound for the smallest eigenvalue of a *dependent-columns* Gram in
the L→∞ limit, uniform enough to show the density of μ near 0 is positive (no mass gap). Yaskov's
least-eigenvalue control (Zbl 1381.60024) is for i.i.d.-sample Gram/sample-cov, not DPP columns.
Status: theoretical and non-trivial; parked as a fallback.

## Route D — Comparison with known ensembles (Marchenko–Pastur-like)
State: **OPEN, dependence makes it inapplicable directly.**
Idea: treat the Gram as a random matrix with dependent columns; MP-type limits (Efron-like) assume
independent (or weakly dependent) columns. The sine-DPP columns are strongly dependent
(projection kernel). Status: the naive MP transfer is unjustified; recorded, low priority.

## Route E — Reduction via a cleaner statement
State: **OPEN.**
Reduce SL to a statement about the Christoffel function of the (stationary) point process's
intensity or to a well-posed "sandwich" of the empirical measure. No clean reduction found yet that
doesn't reintroduce route B/F's moment work.

## Route F — Christoffel/Hankel asymptotics from moments (the decisive computational lever)
State: **MOST PROMISING, criterion proved (T1), reduction proved (T0).**
Idea/progress: Λ_m(0) = [(H_m with 0th row/col deleted) det] / [det H_m] with H_m the (m+1)×(m+1)
Hankel matrix of moments (m_0..m_2m). Christoffel atom theorem: Λ_m(0) → μ({0}). So SL ⟺ this ratio
→0. If the exact moment sequence m_k is known (Route B) and grows like C·k^α with α<2, classical
Hankel asymptotic (Borodin–Deift / Szegő–Widom for a measure on [0,∞) supported up to the top but 
with mass near 0) gives Λ_m(0)→0. Being tested in this run with (i) the known exact m_1..m_4 and 
(ii) numerical m_5..m_8 to fit the growth and predict Λ_m(0).
Gap to closure: we need either the exact all-k moments (Route B) or a theorem that the *specific*
numerically-observed moment growth (observed decay Λ_m(0)~half per degree ⇒ m_k grows fast enough)
is rigorous. Partial: the ratio criterion turns the analytic SL into a moment-growth question.

### Route B/F sub-conjecture — FERMIONIC/WICK CANCELLATION (the concrete route to exact m_k)
State: **CONJECTURED, UNVERIFIED — the single most promising next step.**
Claim: for the sine (projection) DPP, the "all-distinct" and all non-MATCHED interaction terms
D_k in the moment decomposition VANISH for ALL k≥3 (D_3=D_4=0 already verified in the probe).
Heuristic: K is the projection onto Paley–Wiener space; E[Σ trace-cycles against det[K]] reduces
via the free-fermion/Wick pairing of a projection DPP to a sum over PAIRINGS only — unmatched
factor loops cancel like contracted fermion loops (sign balance). If D_k=0 for all k, the moments
m_k come from a computable combinatorial sum over index partitions into size-≤2 matched blocks
weighted by the sinc-power integrals c_{2n} = ∫sinc^{2n} = B-spline values (c_2=1,c_4=2/3,c_6=11/20).
This would give EXACT m_k for all k → exact Hankel → rigorous Λ_m(0)→0 → SL closes.
Verification needed: compute m_5, m_6 EXACTLY (ρ_5, ρ_6 determinants) or via a FAITHFUL DPP
simulation with enough samples to resolve the tiny non-zero D_5,D_6. My hand-rolled sampler was
defective (C5); a correct projection-DPP sampler (orthogonalization/Durbin method) is required.

## Route G — Failure-mode / disproof check
State: **OPEN.**
Verify no easy counterexample: μ has no atom at 0 in the random-Gram model. Cross-check against
numerical scaling (smallest eigenvalues shrink with L, density near 0 growing — probe §3). Recorded.

Leader is **B + F** (moment computation feeding the Christoffel/Hankel ratio → μ({0})=0). 
