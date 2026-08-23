# npip proof-certificate artifact validation (local)

Date: 2026-08-23

Validated with the npip99 `proof_certificate.export_interval_tree` functions:

| artifact | result |
|---|---|
| `weighted-p1-grid4000.tree` | `(q=6, roots=324, nodes=1739356, splits=869516, leaves=869840)` |
| `weighted-p1-grid4000.roots.bin` | `(q=6, roots=324)` |
| `weighted-p1-grid4000.roots.json` | `q=6, roots=324` |

This confirms the recorded topology/root artifacts are internally consistent
with the certificate report (`nodes=1739356`, `splits=869516`,
`leaves=869840`).

Script: `literature/raw/zeta-zeros-npip/local-checks/artifact-validation.txt`
