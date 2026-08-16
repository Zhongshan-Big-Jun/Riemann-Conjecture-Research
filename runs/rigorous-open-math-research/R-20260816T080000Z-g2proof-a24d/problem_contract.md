# Problem Contract — SL gap G2 residual identity (Lemma P / Lemma M general-k)

- **Run ID:** `R-20260816T080000Z-g2proof-a24d`
- **Task packet:** SL gap G2 residual identity — prove, for all k, the vanishing characterization
  of the shape integrals J_σ (Lemma P / Lemma M general-k).
- **Project root:** `F:\LaTeX\Riemann Conjecture`
- **Role:** SOLVER, bounded proof-attempt pass (~2-3 h effective)
- **Skill:** rigorous-open-math-research

## Normalized statement to prove

Let `Part(k)` be set-partitions of `{0,…,k−1}`; σ has `b = #blocks`; `K = sinc`;
`ρ_b = det[K(x_i−x_j)]_{i,j=0..b−1}`; `ρ_b` lives on the b block positions `x_0..x_{b−1}`
with translation pinning (b−1 free variables).

```
J_σ = ∫_{R^{b−1}} [ ∏_{a=0}^{k−1} K(x_{σ(a)} − x_{σ(a+1)}) ] · ρ_b  dx,   (x_{b−1} pinned)
H_σ = cycle-crossing multigraph on blocks: one edge (u,v),u≠v per cycle edge (a,a+1 mod k)
      whose blocks differ (multiplicity = crossing count between u,v); m = |E(H_σ)|.
J_σ = Σ_{π∈S_b} sign(π) · B_{Γ_{σ,π}}(0),   Γ_{σ,π} = H_σ ∪ match(π),
      B_Γ(0) = box-spline value at 0 = (n−d)-vol{ ξ∈[−1/2,1/2]^n : Mξ=0 } / √det(MMᵀ).
```

**Residual identity (target):** for all k ≥ 2 and every σ ∈ Part(k),

```
J_σ = 0  ⟺  H_σ disconnected  OR  (b ≥ 2 and m ≤ 2b−3)
J_σ ≠ 0  ⟺  H_σ connected AND m ≥ 2b−2        (b = 1 base: H empty, m = 0, J_σ = 1)
```

Equivalently: the signed box-spline sum over S_b vanishes precisely on the graph class
`{H_σ : NOT (connected and m ≥ 2b−2)}`.

## Sub-identities (from upstream G2 run §7)

- **M1 (disconnected ⇒ 0):** if H_σ has a proper connected component, the cycle product
  factors over components and the remaining signed sum over S_b reduces to a lower-order
  "D-type" cancellation whose residue vanishes.
- **M2 (low-surplus ⇒ 0 / surplus ⇒ ≠0):** if H_σ is connected and m ≤ 2b−3
  (cyclomatic number c = m−b+1 ≤ b−2), the S_b-signed box-spline sum telescopes to 0;
  if m ≥ 2b−2 a non-cancellable term survives so J_σ ≠ 0.

## Completion criteria (bounded, honest)

- Progress on M1 and M2 as far as rigorous in budget; weakest acceptable is a precise
  reduction of each open sub-identity to an exactly-stated graph/linear-algebra lemma,
  with every failure mechanism of killed routes recorded.
- Every symbolic/numeric claim validated against the exact per-partition dataset
  `reproducibility/allJ.json` (k=3..6, 275 rows) and the audited box-spline engine of
  G1 (`R-20260816T030000Z-slG1-9c2a`).
- Output protocol status label first line; no numerical evidence presented as proof.

## Inherited anchors (authoritative facts, from audited upstream runs)

- Moments m_1..m_6 = (1, 4/3, 2, 13/4, 101/18, 640/63); D_3=D_4=D_5=D_6=0.
- G2 rule verified 100% (275/275, k=3..6): nonzero ⟺ H_σ connected AND m ≥ 2b−2.
- b=2 closed form: J = c_m − c_{m+2} ≠ 0 (c-sequence strictly decreasing).
- K*K = K (projection kernel), sinc Fourier window = 1_{[-1/2,1/2]}.
