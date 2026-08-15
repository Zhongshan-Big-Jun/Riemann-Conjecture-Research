# Candidate proof / exact derivation — m_5 = 101/18

**Status label:** `FINITE_COMPUTATIONAL_RESULT` (exact rational `m_5 = 101/18`), with
`RIGOROUS_PARTIAL_RESULT` framing for the general-k Lemma P it evidences.

## 1. The shape-integral formula (derived, anchored)

For the random sine-process Gram matrix `G_ij = sinc(x_i − x_j)` on a window of length L with
density 1 (N≈L), the k-th trace moment is the limit

```
m_k = (1/N) E[ tr G^k ]  (N→∞, density 1)
    = Σ_{σ∈Part(k)} J_σ
```

where `Part(k)` is the set of set-partitions of {0,…,k−1} (Bell(k)), each block ↔ one distinct
value, and

```
b     = # blocks of σ
rho_b = det[ K(x_i − x_j) ]_{i,j=1..b}     (DPP factorial moment density)
J_σ   = ∫_{R^{b−1}} [ ∏_{a=0}^{k−1} K(x_{σ(a)} − x_{σ(a+1)}) ] · rho_b  dx   (x_b pinned = 0)
```

(the product over the cycle edges; an edge whose endpoints fall in the same block is a
self-loop contributing K(0)=1). Because the integrand is translation-invariant and the density
is 1, each `(1/N)·∫` limit equals `J_σ`.

**Verification of the formula:** it reproduces, with exact rational arithmetic,
`m_2 = 4/3`, `m_3 = 2`, `m_4 = 13/4` exactly (the audited moment list). This is the anchor that
validates the whole machinery before computing k=5. (The G1-round scaffold `m5_shapes.py` was
WRONG — it omitted the ρ_b factor and mis-counted partitions; superseded here.)

## 2. The box-spline (coarea) evaluation of each J_σ

Each `J_σ` is a signed sum of box-spline values at 0. Expanding `rho_b = Σ_{π∈S_b} sign(π) Π_a
K(x_a−x_{π(a)})`, each integrand becomes a product of sincs:

```
J_σ = Σ_{π∈S_b} sign(π) · B_{Γ_{σ,π}}(0)
```

where `B_Γ(0)` is the box-spline value at 0 for the combined edge-direction multigraph
(cycle edges + permutation edges). With `K̂ = 1_{[−1/2,1/2]}` (Paley–Wiener window), the
coarea formula gives a RATIONAL box-spline value at 0:

```
B_Γ(0) = (n−d)-vol{ ξ ∈ [0,1]^n : Mξ = 0 } / sqrt(det(M M^T)),   M = (edge directions)
```

computed by exact vertex enumeration of the section polytope. Individual signed "coarea" terms
may be irrational (they contain √2), but the signed sums `J_σ` are rationals with small
denominators (≤ 180 here), reconstructed and cross-checked.

**Exact B-spline (sinc-power) constants** derived/used (validated by the same engine and by
`int sinc^{2n}` direct):

| c_{2n} | exact | decimal |
|--------|-------|---------|
| c_2    | 1     | 1.0 |
| c_4    | 2/3   | 0.6666666667 |
| c_6    | 11/20 | 0.55 |
| c_8    | 151/315 | 0.4793650794 |
| c_10   | 15619/36288 | 0.4304177690 |

## 3. The k=5 decomposition

Enumerating Bell(5)=52 partitions and grouping by block-size profile (b = #blocks):

| profile | #partitions | J_σ sum | breakdown |
|---------|----|---------|-----------|
| (5) all-equal | 1 | **1** | the unit term |
| (1,4) | 5 | **5/3** | 5 partitions, each J = 1/3 |
| (2,3) | 10 | **9/4** | 5×1/3 + 5×7/60 |
| (1,1,3) | 10 | **1/3** | 5×1/15 + 5×0 |
| (1,2,2) | 15 | **13/36** | 5×1/15 + 5×1/180 + 5×0 |
| (1,1,1,2) | 10 | **0** | (D_4-type cancellation; hp-verified ≈0) |
| (1,1,1,1,1) = D_5 | 1 | **0** | certified |

Summing:

```
m_5 = 1 + 5/3 + 9/4 + 1/3 + 13/36 = 202/36 = 101/18 = 5.6111…
```

## 4. Why the vanishing shapes vanish

- `(1,1,1,1,1)`: the all-distinct term `D_5 = 0`, CERTIFIED by the G1 run (`D5_exact.json`,
  independent box-spline rational reconstruction; `max|recon−float|≤8e−15`).
- `(1,1,1,2)`: each such partition contracts (self-loop edges ≈ K(0)=1) to a closed 4-vertex
  cyclic integral of the SAME form as `D_4`; since `D_4 = 0` (certified), these vanish. Verified
  ≈ (4e−13, −4.5e−13) by the independent high-precision engine.

**Correction to the task framing:** the "surviving shapes = blocks of size ≤ 2" statement is
NOT correct for k=5 — blocks of size 3 and 4 DO contribute (profiles (1,4),(2,3),(1,1,3)).
The actual vanishing condition observed is **by number of blocks: b ≥ 4 ⇒ J_σ = 0**, which
generalizes D_4=D_5=0.

## 5. Validation

1. **Anchor:** engine reproduces m_2=4/3, m_3=2, m_4=13/4 exactly.
2. **Independent engine:** every distinct shape value (1, 1/3, 7/60, 1/15, 1/180, 0) and the
   b=4 vanishings cross-validated by the hp (exact-fraction Delaunay volume) engine — e.g.
   7/60 = 0.1166667, 1/15 = 0.0666667, 1/180 = 0.0055556 all matched.
3. **c_{2n}:** c_8=151/315, c_10=15619/36288 match known box-spline values and direct
   high-precision sinc integrals.
4. **DPP simulation (evidence only):** L=50 gives m_5 ≈ 5.4465±0.084 (h=0.02, 120 samples),
   5.4923±0.079 (h=0.05, 150 samples). These are ~1.5–2σ below 101/18; the task's L=50 h=0.05
   reference (5.4551, bias −0.13±0.08 ⇒ exact≈5.59) is consistent. Finite-L underestimates m_5,
   so the exact 5.6111 is not contradicted but is NOT independently pinned by simulation.

## 6. Exactness and honesty

- The deliverable `m_5 = 101/18` is a rational identity obtained by exact arithmetic over the
  52-partition decomposition, validated by two independent engines and the m_2..m_4 anchor.
- No numerical evidence is used as proof; simulation is labeled evidence only.
- Open: a closed general-k proof (Lemma P / G2) and the exact higher moments m_6..m_8 needed for
  the decisive SL Hankel-decay test.
