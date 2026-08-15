# Numerical verification — kernel-limit lemma

Command (low-perf mpmath, `py -3.10`, `PYTHONUTF8=1`):

```
py -3.10 reproducibility/kernel_limit_verify.py
py -3.10 reproducibility/ramp_rate_verify.py
```

## A. Kernel form consistency `kMT(x) == K_1(x)/K_1(0)` (40-digit mpmath)

| x  | |kMT(x) − K_1(x)/K_1(0)| |
|----|--------------------------|
| 0.3 | 1.15e-41 (roundoff) |
| 1.0 | 7.2e-43 |
| 1.9 | 7.2e-43 |

The closed form `kMT = K_1/K_1(0)` holds exactly (to quadrature/roundoff precision);
proof in candidate_proof.md §4.

## B. Fourier (true) overlap `O_L(x)/O_L(0)` → `kMT(x)` — pure cosine profile (ramp w→0)

`O_L(x) = ∫_{−L/2}^{L/2} cos(√2·u/L)·cos(2π·x·u/L) du`. Since `t = u/L` makes the integrand
exactly `L·K_1(x)`, the equality is **exact for every L** (error = quadrature roundoff):

| x | L | O_L(x)/O_L(0) | kMT(x) | err |
|---|----|---------------|--------|-----|
| 0.3 | 100 | 0.8681184754715836 | 0.8681184754715836 | ~1e-41 |
| 0.3 | 1000 | 0.8681184754715836 | same | ~1e-41 |
| 0.3 | 10000 | 0.8681184754715836 | same | ~1e-41 |
| 1.0 | 100 | 0.05336404597208687 | 0.05336404597208687 | ~1e-42 |
| 1.0 | 1000 | 0.05336404597208687 | same | ~1e-42 |
| 1.0 | 10000 | 0.05336404597208687 | same | ~1e-42 |
| 1.9 | 100 | −0.05698597865602731 | −0.05698597865602731 | ~1e-42 |
| 1.9 | 1000 | −0.05698597865602731 | same | ~1e-42 |
| 1.9 | 10000 | −0.05698597865602731 | same | ~1e-42 |

## C. O(w/L) rate with a fixed ramp width w=8 (TaperProfile, linear ramp ϱ)

`O_ramp(x)/O_ramp(0)` with `φ(u)=√cos(√2u/L)·ϱ((L/2−|u|)/w)`, w=8, λ=1.
`err*L` is roughly constant ⇒ error decays like `w/L` (1/L), matching the `2w/L` proof bound.

| x | L | ratio | kMT(x) | err | err·L |
|---|----|-------|--------|-----|-------|
| 0.3 | 100 | 0.89178155 | 0.868118475 | +0.02366 | 2.37 |
| 0.3 | 1000 | 0.870583185 | 0.868118475 | +0.002464 | 2.46 |
| 0.3 | 10000 | 0.86836582 | 0.868118475 | +0.000247 | 2.47 |
| 1.0 | 100 | 0.156692195 | 0.053364046 | +0.10333 | 10.3 |
| 1.0 | 1000 | 0.0627764567 | 0.053364046 | +0.009412 | 9.41 |
| 1.0 | 10000 | 0.0542949712 | 0.053364046 | +0.000931 | 9.31 |
| 1.9 | 100 | −0.138990136 | −0.05698598 | −0.08200 | −8.20 |
| 1.9 | 1000 | −0.065888797 | −0.05698598 | −0.008903 | −8.90 |
| 1.9 | 10000 | −0.057875867 | −0.05698598 | −0.000890 | −8.90 |

`err·L` ≈ const (~ w·(1–8)) confirms **rate O(w/L)**, i.e. O(1/L) for fixed w; matches the
`≤ 2w/L` proved bound (the ratio normalization multiplies by `1/F_L(0)` and x-dependent
`kMT`, explaining the factor up to ~w).

## D. Honest note: `Cfun` autocorrelation does NOT give `kMT`

`Cfun(λ,L,y) = ∫_{−L/2}^{L/2−y} vStar(u/L)·vStar((u+y)/L)du` (autocorrelation).
With the natural identification `y = x·L` (x=0.3, L=100):
`Cfun/L ≈ 0.61454`, but `kMT(0.3) ≈ 0.86812`. The two differ ⇒ `Cfun` (profile
autocorrelation) is not the kernel overlap; the kernel requires the cross-frequency
(Fourier) overlap. Doc detail in candidate_proof.md §6.

## Replay

Files `reproducibility/kernel_limit_verify.py` and `reproducibility/ramp_rate_verify.py`
reproduce A–D. Hash-bound in `repro_manifest.md` / `SHA256SUMS`.
