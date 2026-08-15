# Obligation Graph — R-20260815T130000Z-slmoments-a3f9

Claims, dependencies, proof status. (Extends pass 7b21e4; T0/T1 are rigorous there.)

```
SL   [OPEN]  :=  mu_lam({0}) = 0  (equivalently Lambda_m(0)->0)
 ^
 |-- T0  [RIGOROUS, pass 7]  Lambda_m(0)->0  <=>  mu_lam({0})=0  (Christoffel atom theorem,
 |                                                        compact support => deterministic)
 |-- T1  [RIGOROUS, pass 7]  Lambda_m(0) = det(H_m)/det(minor00)  (Hankel criterion)
 |           validated exactly (Lambda_2=5/36)
 v
Lambda_m(0)->0  [OPEN]  via the moment sequence
   |
   |-- LA (numerical evidence this pass): m_k matches matching-sum growth; Hankel decay observed
   |       at m=1..3 (0.24,0.13,0.092). EVIDENCE ONLY.
   |
   |-- Lemma H  [OPEN]  matching-sum moment sequence => Lambda_m(0)->0
   |       sub-routes: (a) moment-growth/determinacy (m_k ~ poly, alpha<2 => compactly supported
   |       density positive at 0); (b) Szego-Widom direct Hankel asymptotic. Neither proven.
   |
   |-- Lemma P  [OPEN]  m_k = sum over size<=2 matched-block partitions weighted by B-spline c's
   |       verified structurally for k=2,3,4 (exact 4/3,2,13/4). Full generality OPEN.
   |
   |-- Lemma M  [OPEN]  D_k = 0 for all k>=3   (fermionic/Wick)
   |       D_3=D_4=0 exact (probe); D_5≈0 evidence; D_6 measuring. Proof of the general identity
   |       (projection algebra / box-spline sum) NOT yet written.
   |
   |-- [Validated sampler]  Gate A (exact-joint) PASS; Gate B (exact moments) PASS.
   |       [DONE this pass]  => numerical D_k/Hankel evidence is trustworthy
```

## Open obligations
- G1 = Lemma M (prove D_k=0), the central sub-conjecture. Evidence (D_3,D_4,D_5~0) but no proof.
- G2 = Lemma P to full k.
- G3 = Lemma H (the last step to close SL via moments; genuinely hard).
- T0/T1 rest on the cited Christoffel atom theorem (not re-derived; a Lean formalization would pin it).
