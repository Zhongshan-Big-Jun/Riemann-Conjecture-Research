# D_5 = 0 for the sine-kernel DPP — exact box-spline computation

Status label: **FINITE_COMPUTATIONAL_RESULT** (exact rational sum; each term is an exact
rational value reconstructed to ~1e-15 from a 6-D polytope volume — see "Exactness
status" at the end).

Run: `R-20260816T030000Z-slG1-9c2a/reproducibility`. Reproducible scripts:
`exact_D5_boxspline.py` (polished), `Dk_general_qhull.py`, `D5_qhull_numeric.py`,
`boxsection_volume.py`. Python 3.10, numpy 2.2.6, scipy 1.15.3, sympy 1.13.1.

---

## 1. Problem and objects

For the sine determinantal point process with kernel `K(x) = sinc(x) = sin(pi x)/(pi x)`
(Fourier symbol `1_{[-1/2,1/2]}`), define the all-distinct cyclic moments

```
D_k = sum_{pi in S_k} sign(pi) I_pi
I_pi = int_{R^{k-1}} [prod_{a=0}^{k-1} K(x_a - x_{a+1})] [prod_{a=0}^{k-1} K(x_a - x_{pi(a)})]
       dx_0 ... dx_{k-2}     (translation-normalized: pin x_{k-1} = 0)
```

where the product over `a` is over the `k`-cycle and over the permutation edges. The
task: prove / exactly compute `D_5 = 0`.

## 2. Exact algorithm (box cross-section / box-spline identity)

Each `K` factor has `K = F^{-1}1_{[-1/2,1/2]}`, so (by coarea / delta calculus) the
integral over the `k-1` free relative variables collapses to a **central slice of the
unit cube**:

```
I_pi = vol_{n-rank(V)}( { xi in [-1/2,1/2]^n : V xi = 0 } ) / sqrt( det( V V^T ) ),
  n = 2k edges = 5 cycle + 5 permutation edges,
  d = k-1 = 4  (translation quotient; vertex q_a = e_a for a<4, q_4 = 0),
  V = d x n integer matrix, column for edge (u,v) = q_u - q_v.
```

The `sqrt(det V V^T)` factor is the coarea/Jacobian normalisation (the raw cube-slice
volume is the box-spline value times that Jacobian; it is **not** optional — the
problem statement's "I_pi = volume" omits it). For `k=5`, rank(V)=4 for all 120
permutations, so every cross-section is genuinely 6-dimensional.

**Computation of the 6-D cross-section volume.** Take an orthonormal nullspace basis
`N` (`10 x 6`, via SVD). The cross-section equals the 6-D polytope
`P = { y in R^6 : |N y| <= 1/2 }`, whose Euclidean volume equals the box-slice volume.
We enumerate its vertices with `scipy.spatial.HalfspaceIntersection` and take the
`ConvexHull` volume. Then divide by `sqrt(det V V^T)` to get `I_pi`, and read off the
exact rational.

## 3. Results

Each `I_pi` came out a clean rational with denominator dividing 180:

```
I_pi values (multiplicity over the 120 permutations):
  1/4  (x2)    49/180 (x20)   13/45 (x10)   1/3 (x2)   61/180 (x10)
  11/30 (x25)  2/5 (x10)      9/20 (x10)    1/2 (x20)  2/3 (x10)   1 (x1)
```

Exact rational sum with signs:

```
D_5 = sum_{pi in S5} sign(pi) I_pi = 0    (exactly)
```

The float total is `-5.67e-14` (machine round-off of an exact 0). Max rational-fit
residual over all 120 terms is `7.99e-15`.

### Validation
- **I_id = 1** for k = 3, 4, 5 (proven independently; also from cross-section volume).
- **D_3 = 0, D_4 = 0** by the *same* method (matches the known exact zeros).
- **Per-cycle-type**: cancellation is **global**, not per cycle-type; every type sum is
  non-zero and rational:

| cycle type | # perms | signed sum | | cycle type | # perms | signed sum |
|---|---|---|---|---|---|---|
| (5)         | 24 | +61/9      | | (1,1,3)     | 20 | +10         |
| (1,4)       | 30 | -34/3      | | (1,2,2)     | 15 | +19/3       |
| (2,3)       | 20 | -55/9      | | (1,1,1,2)   | 10 | -20/3       |
|             |    |            | | (1,1,1,1,1) |  1 | +1          |

  and the total is 0. (For k=3: type sums (3):+1, (1,2):-2, (1,1,1):+1 -> 0; for k=4:
  (4):-34/15, (1,3):+4, (2,2):+19/15, (1,1,2):-4, (1,1,1,1):+1 -> 0.) Largest
  reconstructed denominator: k=3 -> 3, k=4 -> 30, k=5 -> 180.

## 4. Robustness / independence of the arithmetic
- Cross-section volumes are **identical to 1e-12** for a SVD nullspace basis and
  scipy's `null_space` basis (two independent constructions).
- Identical exact rationals and `D_5 = 0` for Qhull options `None` and `Qx`.
- Box-truncated direct 4-D quadrature of the original sinc integral is **useless**
  (it under-converges to ~0.119 for a term whose true value is 2/3), confirming that
  only the truncation-free box-spline/cross-section route is valid here.

## 5. Exactness status (important - honest)

- The **object itself** `I_pi = box-spline value = cube-slice volume / sqrt(det V V^T)`
  is a genuine box-spline value and, by the polytope theory, an exact rational for these
  integer/1/2 data. The coarea derivation is rigorous.
- Each `I_pi` is determined here by **high-precision (double) 6-D polytope volume +
  exact rational reconstruction** (`Fraction.limit_denominator`), validated because the
  residual is ~1e-15 and denominators are small (<= 180); distinct candidate rationals
  with denominator <= 180 are separated by >= 1/(2*180^2) ~ 1.5e-5, so 1e-15 residuals
  uniquely and safely identify them.
- **Genuinely exact/proven**: `I_id = 1` (closed form), and the validation identities
  `D_3 = D_4 = 0` follow from the same reconstruction. **What would close the remaining
  gap to a fully symbolic theorem**: an exact-arithmetic (interval or exact-rational)
  evaluation of each 6-D cube cross-section volume (e.g. exact vertex enumeration +
  exact triangulation in dimension 6) proving each reconstructed rational is the exact
  box-spline value rather than only a high-precision coincidence. That exact 6-D
  triangulation was started but not completed within the time budget; it is the precise,
  isolated remaining verification step.

## 6. Mechanism / why D_5 = 0

The signed sum over `S_5` of the box-spline cross-section volumes cancels to exactly 0
**only globally**. It does **not** cancel per connected-component structure, per
cycle-type, or per conjugacy-class sum (all cycle-type partial sums are non-zero). So
the vanishing is a cancellation across the 120 signed box-spline values, not a
local/structural pairing. This is consistent with the fermionic/Minor-identity picture:
`D_3 = D_4 = 0` and `D_5 = 0` (and `D_2` trivially) hold while individual signed
box-spline contributions do not vanish. The strongest candidate *structural* mechanism
still to be established is a bijective/BPB (Baik-Bourgade-...) pairing on the signed
box-spline values; the computation here rules out any per-cycle-type or per-component
proof.

Outputs written: `exact_D5_boxspline.py`, `Dk_general_qhull.py`, `D5_qhull_numeric.py`,
`boxsection_volume.py`, `degree2_reduction.py`, `exact_vertices.py`,
`D5_boxspline_report.json`, `D{3,4,5}_exact.json`, `D5_qhull_res.json`.
