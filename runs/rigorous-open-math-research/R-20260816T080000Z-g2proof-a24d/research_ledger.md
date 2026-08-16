# Research Ledger — R-20260816T080000Z-g2proof-a24d

Chronological record of the bounded proof-attempt pass on the G2 residual identity
(Lemma P / Lemma M general-k).

## Setup (T+0..T+0.5h)
- Created run dir + `reproducibility/` + `whiteboard/`. Random suffix `a24d`.
- Env: `py -3.10` (numpy/scipy/sympy/mpmath; no networkx). `$env:PYTHONUTF8=1`.
- Loaded `rigorous-open-math-research`. Read upstream: G2 rule run `R-20260816T070000Z-g2rule-a1b2`
  (candidate_proof §7 residual identity; allJ.json 275 rows; exact engine files), G1 run
  `R-20260816T030000Z-slG1-9c2a` (box-spline/coarea machinery, D_k=0, obligation/approach registries).
- Copied engine + data files into `reproducibility/`; verified exact engine reproduces m_3=2.

## Step 1 — M1: connectivity of H_sigma (T+0.5h)
- Computed: for k=3..7, ALL partitions have H_sigma connected (0 disconnected across 1152 partitions).
- **Lemma 0 (PROVEN): H_sigma is ALWAYS connected** (for b>=2), because the cycle is a closed walk
  visiting every block; if blocks split into two nonempty classes A,B with no crossing edge between
  them, the closed walk could never transition between A and B while visiting both (any A->B position
  transition IS a crossing edge), contradiction. M1 (disconnected => 0) is therefore VACUOUS.
- Consequence: residual identity reduces to: J_sigma = 0 <==> m <= 2b-3 (b>=2); nonzero iff m >= 2b-2.
  (M1 is done; all the content is M2.)

## Step 2 — per-pi box-spline decomposition (T+1h)
- float engine per-pi expansion of J_sigma = sum_pi sign(pi)*B_Gamma(0):
  - b=3,m=3 (vanish): B values = {identity:1, 3 transpositions:2/3 each, 2 three-cycles:1/2 each}.
    Sum = 1 - 3*(2/3) + 2*(1/2) = 0. Multiplicative cycle-class-function here.
  - b=3,m=4 (nonzero, 1/15): B DEPENDS on which transposition/cycle (0.5, 2/3, 2/3; 3-cycles 0.45)
    => NOT a cycle-length class function. EGF/multiplicative route FAILS generally.
  - b=4,m=4 H=4-cycle (vanish): identity 1, all 6 transpositions 2/3, (2,2) = {9/20,9/20,11/30},
    (3,1) all 1/2, (4,) = {11/30 x4, 2/5 x2}. Sum = 0 exactly but NOT a multiplicative class
    function (B(2,2)=9/20 != (2/3)^2; B splits within cycle type by H-interaction).
- **Route 1 (class-function EGF) KILLED**: B_Gamma(0) is not a multiplicative class function of the
  cycle lengths in general (verified b=4,m=4: (2,2) splits, B(2,2)=9/20 != 4/9). The cancellation is
  a genuine combinatorial sum, not the EGF-via-class-function trick.
- Also confirmed float-noise: b=4,m=4 k=6 profile [3,1,1,1] gave a spurious J~0.399; true value 0
  (allJ.json). Individual B values themselves were accurate; only the cancellation residual is noisy.

## Step 4 — M1 fully closed (Lemma 0)
- PROVEN (rigorous, above): H_sigma always connected for b>=2. The disconnected branch of the
  residual identity is vacuous. M1 = DONE. Residual identity reduces to:
     J_sigma = 0  <==>  m <= 2b-3   (b>=2);  b=1 base J=1.
  All content is now in M2.

## Step 5 — M2: exact certified contributions (T+~1.5h)
- Exact engine (`coarea_value_exact`) + rational reconstruction gives certified per-pi B values:
  - b=3,m=3 (vanish): +1, three x -2/3, two x +1/2  => sum = 0 EXACT.
  - b=3,m=4 (nonzero, 1/15): +1, -(1/2+2/3+2/3), two x 9/20 => sum = 1/15 EXACT.
  - b=4,m=4 H=4-cycle (vanish): +1, six x -2/3, (2,2)={9/20,11/30,9/20}, eight x 1/2,
    (4,)= 4x 11/30 + 2x 2/5  => sum = 0 EXACT (verified by hand: 1-4+19/15+4-34/15=0).
- **Route 1 (cycle-class-function / multiplicative EGF) KILLED** by exact counterexample:
  b=4,m=4 has B((2,2)) = 9/20 != (2/3)^2 = 4/9 and (2,2) splits into {9/20, 11/30, 9/20}
  depending on whether the transposition pairs are H-adjacent. So B is NOT a multiplicative
  class function of cycle lengths; the EGF-cancellation trick does not apply in general.
- **Naive degree-2 contraction (contract a deg-2 vertex of H, keep J) KILLED**: triangle b=3,m=3
  -> J=0, but contracting a deg-2 vertex gives b=2,m=2 with J=1/3 != 0. The determinant rho_b
  couples to every block variable, so the "fold a leaf" reduction is NOT closed without tracking
  the determinant contraction. Recorded as dead-end.
- **b=2 family fully closed (PROVEN):** rho_2 = 1 - K^2, so J = c_m - c_{m+2} with
  c_m = int K^m strictly decreasing (0<=K<=1, K<1 a.e.), hence J > 0 for all even m>=2. NONZERO
  always (matches m >= 2b-2 = 2 always true for b=2).

## Step 6 — new k=7 verification (extends the 275-row dataset to new H-isoclasses)
- k=7 adds 15 new H-isoclasses (18 at k<=6 -> 33 at k=7), not covered by the upstream 275 rows.
- Running exact-engine verification on the surplus boundary:
    b=3,m=7 -> nonzero (m>=4); b=4,m=7 -> nonzero (m>=6);
    b=5,m=7 -> zero (m<=7); b=6,m=7 -> zero; b=7,m=7 (all-singletons, tree-like H) -> zero.
- This checks the rule on shapes NOT in the original dataset -> strengthens finite evidence for M2.

## Open obligations (M2)
- Prove the general box-spline identity sum_pi sign(pi) B_{H U pi}(0) = 0 <==> m<=2b-3.
- The exact missing step is stated as Lemma M2 in candidate_proof.md. PROVEN so far: Lemma 0 (M1,
  vacuous), b=2 family, finite k<=7 checks incl new shapes. Killed: class-function/EGF, naive
  degree-2 contraction.
