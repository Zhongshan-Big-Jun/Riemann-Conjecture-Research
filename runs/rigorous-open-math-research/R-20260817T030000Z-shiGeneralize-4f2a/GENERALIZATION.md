# Generalization of the two-certificate trace–energy method

Run: `R-20260817T030000Z-shiGeneralize-4f2a`
Status: **NUMERICAL_EVIDENCE** (the reproduced Shi constant is a research
draft `CANDIDATE`; no new certified constant is claimed here).

## 1. What was reproduced

The candidate repository `zeta-simple-zeros-673316977` was copied/kept in
`reproducibility/` and both scripts were run successfully:

- `py reproducibility/joint_check.py`
  - confirms `m=219` is the best block length in the closed-form
    two-certificate scan;
  - prints `B = 0.673316977142471313480…`.
- `py reproducibility/exact_check.py`
  - verifies the exact rational side conditions and the strict comparison
    `B > 673316977/10^9` by exact rational arithmetic.

## 2. Generalized supporting-plane construction

### Inputs

For a finite set of local certificates indexed by `q` (the number of gaps in
the local window minus one), each certificate is an exact rational triple

```
(p_q, eps_q),   A_q(m) = eps_q (m-q),   q = 6,8,...
```

with block inequality

```
E + p_q L_q >= A_q(m).
```

Here `E` is the trace energy of a unit-diagonal PSD `m x m` block and `L_q`
is the pressure sum over all `(q+1)`-point windows inside the block.

The span normalization comparison, which is coefficientwise in the gaps, is

```
L_a / q_a >= L_b / q_b   for q_a < q_b.
```

### Minimal feasible pressure for a proposed tax vector

Order the certificates by increasing `q`. Define

```
c_i(E) = max(0, (A_i - E)/(p_i q_i)),        l_i(E) = max_{j >= i} c_j(E).
```

The minimal feasible normalized pressures are exactly `l_i(E)`, because the
feasible set is `l_1 >= l_2 >= ... >= l_k >= 0` with `l_i >= c_i(E)`.

For nonnegative block taxes `tau_i >= 0`, the minimal total pressure at
energy `E` is

```
F_tau(E) = sum_i tau_i q_i l_i(E).
```

### Supporting-plane LP

Let `R = Phi_m(A_max)` with `A_max = max_i A_i(m)`, and require `R < 2`
(the envelope lemma needs `R < 2`). If

```
F_tau(E) >= R - Phi_m(E)      for all E in [0, A_max],
```

then the scalar envelope lemma gives the block inequality

```
D + sum_i tau_i L_i >= R.
```

The functions `c_i(E)` are affine, so `F_tau` is piecewise linear. Between
the breakpoints `0`, `A_i`, and all pairwise intersections `c_i(E)=c_j(E)`,
`F_tau` is linear and `Phi_m` is concave; therefore checking the inequality
at those finitely many breakpoints is sufficient.

The best taxes for a fixed `m` are the solution of the finite LP

```
minimize   sum_i tau_i q_i (m - q_i)
subject to F_tau(E) >= R - Phi_m(E) at all breakpoints,
           tau_i >= 0.
```

### Global block-averaging formula

Using the shifted `m`-block partitions and convex spectral pinching, the
global defect satisfies

```
D(M) >= (R/m) S - (1/m) (sum_i tau_i q_i (m-q_i)) N - o(N).
```

Substituting into the imported interface `S >= H_cert N + D(M) - o(N)`
and rearranging gives the exact generalized formula

```
B(m) = ( m H_cert - sum_i tau_i q_i (m-q_i) ) / ( m - R ).
```

The coefficient `c_q(m) = q(m-q)` is derived as follows: a fixed
`(q+1)`-point window is fully contained in a block for exactly `m-q` of the
`m` shifts, and the sum of all `(q+1)`-window spans is at most `q` times
the total normalized span, which is at most `N + o(N)`.

## 3. Implementation

The script `reproducibility/multi_cert_scan.py` implements the LP above for
an arbitrary number of certificates.

- Certified inputs: the same two pinned certificates as the candidate
  (`q=6`, `p=1/2736`, `eps=891/200000` and
  `q=8`, `p=1/2500`, `eps=15211/2500000`).
- The script uses `Fraction` for all exact certificate data and Decimal only
  for display/verification. The LP scan itself uses floating point through
  `scipy.optimize.linprog`; the best solution is re-checked at all
  breakpoints with high-precision Decimal.
- `py reproducibility/multi_cert_scan.py` scans `m=9..1000`.
- `py reproducibility/multi_cert_scan.py --demo-three 219` runs a clearly
  labelled **synthetic** third certificate (`q=7`) to exercise the three-or-more
  certificate code path. It is not certified and is not used as evidence.

## 4. Best constant found

For the two certified certificates, the LP optimum coincides with Shi's
closed-form two-certificate plane:

| quantity | value |
|---|---|
| best `m` | `219` |
| `R = Phi_219(A_9)` | `1.266787844082389873520…` |
| `tau_7` | `0.00001857595109422622…` |
| `tau_9` | `0.00037967047912247882…` |
| pressure tax | `0.66462383425716536…` |
| `B` | `0.67331697714247131348…` |

The scan found no certified three-or-more certificate input in the pinned
repository that would improve this value.

A variable-`R` scan (helper `reproducibility/explore_R.py`) confirms that
for the two-certificate set at `m=219`, the best target is the maximal
`R = Phi_219(A_9)`; lowering `R` lowers the resulting bound.

## 5. Comparison with Shi 0.673316977…

- Reproduced value: `0.67331697714247131348…`.
- Shi’s stated lower bound: `0.673316977…` (strictly greater than
  `673316977/10^9`).
- Exact rational check gives the strict lower bound
  `23320853620214932709/34635772470125253000 =
  0.6733169771319553231… > 673316977/10^9`.
- Our LP scan reproduces the same numerical optimum, and the exact rational
  comparison in `exact_check.py` passes.
- Difference from the project’s previously audited record
  `0.673066472675939665848…`: approximately `0.000250504466532`.

## 6. Honest label and gaps

Label: **NUMERICAL_EVIDENCE**.

- The two-certificate closed form and its exact arithmetic are reproducible.
- The generalized LP is a numerical scan. It is not a proof that the LP
  optimum is globally optimal over all possible multi-certificate planes,
  and the supporting-plane verification is done with high-precision Decimal
  rather than a fully exact rational simplex.
- No third certified certificate with the same `H_cert` baseline is present
  in the pinned candidate repository. The `--demo-three` run uses a
  synthetic certificate only to demonstrate the code path.
- The imported analytic interface and the upstream seven/nine-point
  certificates remain trust boundaries, exactly as in the audit.

## 7. Exact obstruction / why the method does not exceed the value here

For the pinned two-certificate set, the LP at every scanned `m` is
feasible only while `R = Phi_m(A_max) < 2`. With the seven/nine-point data,
this gives `174 <= m <= 377` (the scan found 204 feasible integer `m` in
`9..1000`). The optimum over those feasible `m` is `m=219`.

Within the supporting-plane family described above, the taxes `tau_i` are
chosen by an LP whose constraints are exactly the finite-dimensional
envelope and the coefficientwise span comparison. The LP optimum at `m=219`
is the Shi plane, so a strictly larger certified bound from this exact
method would require at least one additional certified local certificate
(or a different analytic interface) rather than a different weighting of the
same two certificates.
