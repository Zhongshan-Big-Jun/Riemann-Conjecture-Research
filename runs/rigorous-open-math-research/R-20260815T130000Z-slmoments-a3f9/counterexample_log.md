# Counterexample Log — R-20260815T130000Z-slmoments-a3f9

Tested edge cases / failed approaches / obstacles. (Extends pass 7b21e4's C1–C5.)

## N1. Occupancy-kernel discretization (accepted failure → corrected)
Kernel K_ij = sinc(x_i − x_j) (diagonal 1) as the *occupancy* DPP kernel does NOT reproduce the
exact moments: E[N]=27.5 (ref 25) and m2=1.37, m3=2.12, m4=3.56 (ref 1.3134/1.94/3.1056). The
faithful coarse-graining of a continuous intensity-1 DPP uses A_ij = h·sinc (diagonal h), giving
E[N]=L. NOT a counterexample to the model; a discretization correction. [Accepted as a failure,
the correct form is used everywhere.]

## N2. Möbius power-trace grouping (accepted failure → not used)
cyclic_all_distinct.py expressed C_k as Σ_π μ(π,1̂)·T(π) with T(π)=tr(power-groups). For
revisiting partition walks (e.g. k=5 patterns where a block reappears non-contiguously), the
grouping into matrix powers is NOT a fresh-index trace; it FAILED the direct-enumeration check.
The correct general T(π) is a tensor-network (partial-trace) contraction. Used as a warning,
not a deliverable; the fast evaluator (probe_Dk_fast.C[k]) IS validated against direct
enumeration for k=3..6 on small random G.

## N3. mpmath `mp.sinc` is unnormalized (accepted)
`mp.sinc(t)=sin(t)/t`, NOT sin(πt)/(πt); using it gave c_{2n} wrong (≈3.14, 2.09…). Fixed to the
normalized convention. Not a mathematical counterexample.

## N4. Monte-Carlo error floor for a "zero" measurement
D_k ≈ 0 leaves MC error ~1e-3 (D_3), ~1e-3 (D_4), ~4e-4 (D_5) — too coarse to distinguish an
exact 0 from a tiny nonzero D_k alone. The exact-integral path (translation-invariant 4-D box
evaluation of the D_5 integrand ≈ −1e-4) narrows this. Still, a fully rigorous 0 requires the
exact/box-spline identity (Gap 1), not more MC.

None of N1–N4 contradict SL. The sine-Gram limiting measure with no atom at 0 remains the open
(likely true) lemma; the moment route is supported but the exact fermionic identity is the gap.
