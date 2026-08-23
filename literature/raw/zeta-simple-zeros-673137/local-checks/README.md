# Local reproduction checks (2026-08-23)

These logs verify that the copied upstream `zeta-simple-zeros-673137`
verifier works in this environment.

- `fast.log`: upstream fast window/deduction checks, exit 0
  (`fast_parts_verified=True`).
- `gate.log`: canonical 7-point gate verification with the general verifier,
  exit 0, nodes=707797 (expected 707797; upstream README comments their
  committed run records 707901).

Commands used (Windows Python 3.10 with `python-flint 0.9.0`):

```bat
set PYTHONPATH=F:\LaTeX\Riemann Conjecture\literature\raw\zeta-simple-zeros-673137\src
cd /d F:\LaTeX\Riemann Conjecture\literature\raw\zeta-simple-zeros-673137
py -3.10 -m zeta_ext.cli fast
py -3.10 -m zeta_ext.cli gate --workers 4
```
