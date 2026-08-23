# T2 pipeline smoke test: npip proof-tree exporter works locally

Status: **TOOLING VERIFIED** — small synthetic test only.

Date: 2026-08-23

## Commands run

```bat
cd /d F:\LaTeX\Riemann Conjecture\literature\raw\zeta-zeros-npip
py -3.10 -m proof_certificate.export_interval_tree demo C:\Users\HuangZY\AppData\Local\Temp\z23-demo.tree
py -3.10 -m proof_certificate.export_interval_tree from-events C:\Users\HuangZY\AppData\Local\Temp\z23-events.jsonl C:\Users\HuangZY\AppData\Local\Temp\z23-events.tree --q 1 --roots 1
```

## Results

- `demo`: exit 0
  - `q,nodes,splits,leaves = (1, 7, 3, 4)`
  - wrote `z23-demo.tree` (28 bytes)
- `from-events`: exit 0, with a small one-split/two-leaf forest
  - `q,nodes,splits,leaves = (1, 3, 1, 2)`
  - wrote `z23-events.tree` (24 bytes)

## Meaning

The npip99 compact `Z23TREE1` forest exporter runs correctly in this
environment and accepts the documented event-stream interface. This is the
low-level format we would feed with a traced run of our generalized k-point
verifier. It does **not** verify any k=9 certificate yet; it only validates
the tooling path.

## Next step

- Instrument our `verify_kpoint_parallel.py` to emit the `root/path/leaf|split`
  JSONL event streams expected by `export_interval_tree.py from-events` /
  `from-root-dir`.
- Start with a k=7 prototype trace to compare against the npip seven-point
  forest.
