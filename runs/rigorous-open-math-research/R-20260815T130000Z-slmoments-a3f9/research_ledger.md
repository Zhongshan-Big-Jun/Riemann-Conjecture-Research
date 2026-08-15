# Research Ledger — R-20260815T130000Z-slmoments-a3f9 (SL moments pass)

Chronological, every substantial computation/decision recorded before a near-duplicate.

## Step 0 — Context
Read pass 7b21e4 artifacts (problem_contract, candidate_proof, lean audit, approach_registry,
status_and_literature, probe report reports/sl-lemma-random-gram-probe.md). Established the
fermionic/Wick target: D_k=0 for all k≥3; only trust the probe's projection-DPP discretization.

## Step 1 — Faithful sampler + discretization correction (CRITICAL)
Attempt 1 (rejected): kernel K_ij = sinc(x_i−x_j) (diagonal 1) as the *occupancy* DPP kernel.
Measured E[N]=27.5 (vs 25) and moments biased high (m2=1.37,m3=2.12,m4=3.56) — FAILED gate.
**Correction**: the faithful coarse-graining of the continuous (intensity 1) sine DPP to cells
of width h uses the occupancy kernel A_ij = h·sinc(x_i−x_j) (diagonal h, tr A = n·h = L ⇒ E[N]=L).
The sampled cells then form a Gram G_ij = sinc(x_i−x_j) (diagonal 1). With this:
  E[N]=24.9 (ref 25.0); m2≈1.313–1.319 (ref 1.3134→4/3); m3≈1.94–1.95 (ref→2); m4≈3.09–3.14
  (ref 3.1056→13/4). **GATE B PASSED.**
- New file projection_dpp_sampler.py (Kulesza-Taskar eigen-Bernoulli + sequential volume sampling).

## Step 2 — Exact-joint gate A (sampler distributional correctness)
Against the exact L-ensemble joint distribution P(Y)=det(L_Y)/det(I+L) (L=K(I−K)^{-1}) on small
mixed kernels (eigvals in (0,1)), 50k–80k draws: max marginal/per-set deviation matches sampling
error. **GATE A PASSED** for n=5,6. (First reference used ∝det(K_Y), which is only correct for
projection kernels; fixed to the correct L-ensemble form.)
- New file sampler_correctness.py; command `py -3.10 sampler_correctness.py`.

## Step 3 — Extended moments at L=50, h=0.05 (validated sampler)
m_1..m_8 = (1.0000, 1.3239, 1.9716, 3.1813, 5.4551, 9.8092, 18.319, 35.282)
matches probe L=50 reference (1.0,1.322,1.966,3.171,5.435,9.770,18.245,35.148) within MC error.
Hankel Christoffel (mpmath 50 digit): Λ_1=0.2446, Λ_2=0.1332, Λ_3=0.0916. Decaying → consistent
with Λ_m(0)→0 (evidence only). File extended_moments_hankel.py.

## Step 4 — All-distinct D_k measurement (validated sampler; efficient evaluator)
Built efficient all-distinct cyclic-trace evaluator C_k(G) (validated against direct enumeration
for k=3..6 on small random G: exact match). Measured at L=25 h=0.05:
  D_3 = −0.00093 ± 0.0025   (ref 0)
  D_4 = +0.00002 ± 0.0010   (ref 0)
  D_5 = −0.00008 ± 0.00038  (NEW: consistent with 0, tight error)
  D_6 : measured via lighter run + exact integral (see 5b): +0.00051 ± 0.0004 (MC), exact −1e-6
Files probe_Dk_fast.py (fast evaluator), cyclic_all_distinct.py (Möbius attempt — noted the
trace-power grouping is only valid for revisiting-free walks, so it is NOT used; kept for record),
check_Ck_fast.py (validation).

## Step 5 — Exact D_5 integral (translation-invariant 4-D, Gauss–Legendre, vectorized)
D_5 = (1/L)∫ P·ρ_5, P=ΠK(x_a,x_{a+1}), ρ_5=det[K]. Evaluation over [-R,R]^4 (x5=0 fn):
  R=4: −8.2e-5 ; R=6: −9.9e-5 ; R=8: −1.33e-4.
Consistent with D_5 = 0 within truncation error (~1e-4, vs m_5≈5.5). EVIDENCE; the exact-0
(fermionic) proof is the gap. File exact_D5_integral.py.

## Step 5b — Exact D_6 integral (5-D box, vectorized) + numeric D_6
exact_Dk_integral.py: D_6 integral = −4e-7 (R=3), −1.7e-6 (R=4), −1.6e-5 (R=5) — consistent with
D_6=0 (vs m_6≈9.8).
run_D6_light.py (MC, L=20 h=0.05, ns=12): D_6 = +0.00051 ± 0.00040 — consistent with 0.
(The heavier ns=40 L=25 MC D_6 was budget-limited; exact integral is the primary D_6 evidence.)

## Step 6 — Möbius/partition attempt (recorded, NOT used)
cyclic_all_distinct.py tries C_k = Σ_π μ(π,1̂) T(π) with T(π) as trace of matrix-power groups.
Test against direct enumeration FAILED for revisiting walks (k=5 case); the reason is that a
partition walk that revisits a block is NOT a fresh-index matrix power trace. Recorded; the
correct general value is a tensor-network trace. Not used for the probe (fast evaluator used).

## Step 7 — (pending) D_6 numeric; exact m_5 shape decomposition writeup; artifacts.

## Failures / corrections
- Discretization must use occupancy kernel h·sinc (diagonal h), NOT diag-1 sinc (Step 1).
- Phase-2 DPP sampler was validated via TWO gates before any D_k evidence was accepted.
- Möbius power-trace grouping invalid for revisiting partitions (Step 6).

## Decisions
- Route B/F (moment route) active. The fermionic conjecture is supported (D_3,D_4,D_5 ≈ 0) but
  not proven; the remaining gaps are the exact-0 proof and the matching-sum→Hankel lemma.
