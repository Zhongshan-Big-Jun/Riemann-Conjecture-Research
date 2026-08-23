# Multi-certificate integration: mapping general-k pressure certificates into Shi-style `(p_q, eps_q)` inputs

Status: **NUMERICAL_EVIDENCE** — no new proven constant. The conversion formulas below are arithmetic consequences of the certified `F_{k-1} ≥ f_k` inputs; the LP scan is a numerical/diagnostic scan and is not a proof of global optimality.

## 1. Derived conversion formula

Let `k` be the number of points in the local pressure block and put

```
q = k - 1
```

so a local window has `q+1 = k` points and `q` gaps. The general-k pressure certificate is

```
F_{k-1}(g) = 1/(500 q) * sum_{i=1..q} g_i
             + sum_{s=1..q} (2/(q+1-s)) * sum_i w(span_i(s))
```

with `w = k_v^2` and the certified statement `F_{k-1}(g) ≥ f_k`.

For a single `(q+1)`-point window let `E_window` be the trace energy
`tr(G-I)^2` of the corresponding unit-diagonal PSD Gram matrix. In the Gram-entry limit used by the framework (`G_ij = k_v(y_j-y_i)+o(1)`), one has
`E_window = 2 sum_{i<j} w(y_j-y_i)` with `w = k_v^2`. Each pair weight in `F_{k-1}` is at most
`2`, hence the quadratic part of `F_{k-1}` is `≤ E_window`. Therefore the local certificate implies

```
E_window + (1/(500 q)) * span_window ≥ f_k.
```

Now sum this local inequality over the `(m-q)` consecutive `(q+1)`-point windows in an `m`-point block. Let `W_q` be the sum of the spans of all those windows. Because every span capacity is exactly `2`, the total local quadratic contribution is bounded by the full block energy `E_block`; equivalently each pair occurs with total coefficient at most `2`. Thus

```
E_block + p_q W_q ≥ A_q(m),        p_q = 1/(500 q),        A_q(m) = eps_q (m-q),
```

with

```
eps_q = f_k = f_{q+1}.
```

This is exactly the Shi/multi-certificate block form `E + p_q L_q ≥ A_q(m)` with `L_q = W_q`.

### Table of the direct canonical map

| k | q | certified f_k | p_q | eps_q |
|---|---:|---:|---:|---:|
| 7 | 6 | `19/5000 = 0.0038` | `1/3000` | `19/5000` |
| 9 | 8 | `392/100000 = 0.00392` | `1/4000` | `392/100000 = 49/12500` |
| 10 (demo only) | 9 | synthetic `395/100000 = 0.00395` | `1/4500` | `395/100000` |

So the requested conversion for our certified 9-point certificate is

```
q = 8,  p_8 = 1/4000,  eps_8 = 392/100000 = 49/12500,
A_8(m) = (392/100000)(m-8).
```

## 2. Relation to the existing retuned pairs in `multi_cert_scan.py`

The pinned scan uses:

```
q=6: p=1/2736,  eps=891/200000  = 0.004455
q=8: p=1/2500,  eps=15211/2500000 = 0.0060844
```

These are **not the same normalization** as the direct map above.

- The direct canonical 7-point pair from `F_6 ≥ 19/5000` is `(p=1/3000, eps=19/5000=0.0038)`, whereas the retuned 7-point pair is `(p=1/2736, eps=891/200000=0.004455)`.
- The direct canonical 9-point pair from `F_8 ≥ 392/100000` is `(p=1/4000, eps=392/100000=0.00392)`, whereas the retuned 9-point pair is `(p=1/2500, eps=15211/2500000=0.0060844)`.

The retuned pairs are operating points from the more general upstream certificate family

```
p_q * sum_r g_r + sum_{i<j} a_ij^(q) w(y_j-y_i) ≥ eps_q,
sum_i a_{i,i+r} = 2 for every span r,
```

with nonnegative rational weights `a_ij^(q)`. The general-k `F_{k-1}` certificate is a *special case* of this family with the particular weights
`a_{i,i+r}^{(q)} = 2/(q+1-r)`. The retuned pairs use different weights and a different `(p, eps)` trade-off. They are usefully stronger in the supporting-plane LP, but they are not obtained by a simple renormalization of the single `f_k` value.

## 3. Script and LP scan

I created a modified scan script at `/tmp/multi_cert_f9_scan.py`. It imports the original `multi_cert_scan.py` read-only (its functions/certificates are unchanged) and runs additional certificate sets over `m=9..1000`. All certificate inputs are exact `Fraction`s; the LP uses `scipy.linprog`, and each best solution is re-verified with high-precision `Decimal` at all breakpoints.

### Results

| certificate set | best m | R = Φ_m(A_max) | tau_6 | tau_8 | tau_9 | tax | B |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline retuned 7+9 | 219 | 1.266787844082389873520 | 1.8575951e-5 | 3.7967048e-4 | — | 0.6646238342572 | **0.6733169771424713** |
| requested replacement: retuned 7pt + f9 canonical | 243 | 1.055188728810169485 | 3.6527336e-4 | 0.0 | — | 0.5194187138491 | **0.6732429659910096** |
| canonical 7pt + f9 canonical | 280 | 1.065294842063271574 | 0.0 | 2.4977839e-4 | — | 0.5435177765629 | 0.6730767105840543 |
| replacement + synthetic q=9 demo | 243 | 1.055188728810169485 | 3.6527336e-4 | 0.0 | 0.0 | 0.5194187138491 | 0.6732429659910096 |
| baseline + f9 canonical added as extra certificate | 219 | 1.266787844082389873520 | 1.8575951e-5 | 3.7967048e-4 | 0.0 | 0.6646238342572 | 0.6733169771424713 |

The requested configuration — existing retuned 7-point certificate plus our `F_8 ≥ 392/100000` mapped to
`(q=8, p=1/4000, eps=392/100000)` — has best numerical LP value

```
m = 243
tau_6 = 0.0003652733571372011
tau_8 = 0
tax   = 0.5194187138490999642
B     = 0.673242965991009636464267698…
```

At that `m`, `R = Φ_243(A_6) = 1.055188728810169485…`, with `A_6 = 211167/200000 = 1.055835` and `A_8 = 2303/2500 = 0.9212`. The 9-point mapped certificate is not active (`tau_8=0`).

### Key observations

1. **Replacing the retuned 9pt-final by our canonical f9 weakens the LP.** The bound drops from `0.6733169771424713` (baseline) to `0.6732429659910096` (replacement), because the canonical f9 pair is much weaker than the retuned 9pt-final pair and the LP simply uses the 7pt-retuned certificate alone at `m=243`.
2. **Adding the mapped f9 as an extra certificate to the baseline changes nothing**; the LP sets its tax to zero.
3. **The synthetic q=9 demo is unused** (`tau_9=0`) in the tested configuration, so it does not change the LP value.
4. The direct canonical map is therefore arithmetically correct but not competitive with the retuned upstream operating points already in `multi_cert_scan.py`. To obtain a better Shi/LP constant from our certified general-k family we would need either a much stronger `f_k` or a retuned `(p_q, eps_q)` point from the same certificate search, not the canonical pair.

## 4. Caveats

- All LP results are **NUMERICAL/EVIDENCE**, not proofs. The LP uses floating-point `linprog`; the published best solutions were re-checked at the finite breakpoints with `Decimal(80)` and all `ok=True`, but this is not a formal proof of the whole supporting-plane theorem.
- The multi-certificate framework imports `H_cert = 3362285207/5000000000 = 0.6724570414`, not the `H_MT = 0.6725007036794116457…` used in the general-k derivation. Therefore the `B` values above are **not directly comparable** with `C_9(f_9) = 0.673066472675939666` from the general-k chain.
- The conversion formulas are valid conditional on the certified `F_{k-1} ≥ f_k` input, the span-capacity-2 structure, and the imported analytic zeta interface. They are not an independent proof of the local or global bound.
- The synthetic q=9 certificate is only a demonstration and is not certified.

## Reproducibility artifact

- Report: `/mnt/f/LaTeX/Riemann Conjecture/reports/multi-cert-integration-analysis.md`
- Scan script: `/tmp/multi_cert_f9_scan.py` (modification of the unmodified original `runs/…/shiGeneralize-4f2a/reproducibility/multi_cert_scan.py`)
- Raw scan output: `/tmp/multi_cert_f9_scan.out`
