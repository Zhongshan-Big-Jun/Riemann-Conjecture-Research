# Reproducibility manifest — M3-open-A (AtOne κ₁(1,vMT) certificate)

## Run
R-20260816T040000Z-xipAtOne-3078 (suffix 3078).  Project root `F:\LaTeX\Riemann Conjecture`.

## Statement freeze (must match A2-audited values)
- κ₁(1,vMT) = `Zeta23.XiPrime.kappaXi 1 vMT` (Lean `Defs.kappaXi`).
- H_{ξ′} = 2 − κ₁(1,vMT) = `Record9.XiPrimeMT.H_xip` = **0.8678888651990519355503147104203403132225704976166306446…**
  (canonical, `reports/xi-prime-mt-window.py` @ dps=120).
- C₉(ξ′) = (657,500·H − 1,310)/655,001 = `c9ConstXip` (= 0.86920009109661916184…).

## Inputs (read, unmodified)
| Input | Path | Role |
|---|---|---|
| AtOne pattern | `literature/raw/zeta-23-lean/Zeta23/XiPrime/Certificate/AtOne.lean` | κ₉ structure, jWin_one_le_of_le, kappaXi_one |
| D₁ certificate | `literature/raw/zeta-23-lean/Zeta23/XiPrime/Certificate/D1.lean` | eps9 = 1024/2990212875, D1trunc/D1 control |
| Defs | `literature/raw/zeta-23-lean/Zeta23/XiPrime/Defs.lean` | D1, D1trunc, vConv, jWin, cWin, kappaXi |
| AdmWindow blueprint | `reports/admwindow-cos-instance.md` | a=∫v²=0.84922799931830417992…, b=∫v⁴=0.73784297545060818785…, profile norms |
| A2 derivation | `reports/xi-prime-cor22-derivation.md` | κ₁, vConv closed form, H canonical |
| Canonical script | `reports/xi-prime-mt-window.py` | dps=120 analytic vConv computation |
| AdmWindow instance | `lean-proof/Record9/Record9/XiPrimeMT.lean` | vMT, H_xip, kappaXi 1 vMT |

All inputs read-only; **no files created under `literature/raw/zeta-23-lean/`**.  The snapshot
was NOT modified (per hard rule).

## Outputs (this run)
| Output | Path |
|---|---|
| Main certificate script | `reproducibility/atone_xip_mt.py` |
| Independent audit script | `reproducibility/audit_kappa.py` |
| Lean module | `lean-proof/Record9/Record9/XiPrimeAtOne.lean` |
| Status update | `lean-proof/Record9/FORMALIZATION_STATUS_XIP.md` (M3-open-A row) |

## Environment
| Tool | Version / pin | Notes |
|---|---|---|
| Python | 3.10 (Windows) | `py -3.10` |
| python-flint | 0.9.0 | `arb` interval arithmetic at `ctx.dps = 200` (rigorous) |
| sympy | 1.13.1 | exact symbolic derivative of the integrand (rigor of M₄) |
| mpmath | (0.19/current) | EVIDENCE-onlys quadrature cross-checks |
| Lean | leanprover/lean4:v4.33.0-rc2 (pinned `lean-toolchain`) | `lake build Record9.XiPrimeAtOne` |
| Path | `lean-proof/Record9/` (workdir) | uses snapshot `.lake/packages`; no network |

## Commands (recorded; see machine_check.log / whiteboard)
1. `py -3.10 reproducibility/atone_xip_mt.py` → exit 0.  (ARB certificate.)
2. `py -3.10 reproducibility/audit_kappa.py` → exit 0.  (independent evidence cross-check.)
3. `lake build Record9.XiPrimeAtOne` (workdir `lean-proof/Record9`) → exit 0 (after field_simp
   fix).  (Lean machine check.)

## Reproducibility notes
- The ARB path depends on `flint`, `sympy`, `mpmath`.  The certificate uses ONLY ARB interval
  arithmetic for the bounds; sympy provides the exact `f^{(4)}` used only to obtain the
  rigorous global `M₄` bound via the triangle inequality; mpmath is used ONLY for labelled
  EVIDENCE cross-checks and never contributes to the certified bounds.
- The Lean module re-uses the already-downloaded snapshot packages (no network).

## Unknowns
- Exact python-flint/mpmath minor versions on this machine (reported by `importlib` for
  python-flint 0.9.0; mpmath version not pinned).  Recorded as unknown.
