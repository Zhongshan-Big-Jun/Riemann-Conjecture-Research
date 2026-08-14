# Reproducibility manifest — OpenAI draft audit

Run: `R-20260814T041219Z-oaidraft-7c3e73`

## Machine / environment (verified 2026-08-14)

- OS: Windows 10/11, AMD64 (`Windows_NT`).
- CPU: Intel(R) Core(TM) Ultra 7 155H; RAM ~32 GiB.
- Python: `C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe` — `3.10.11`
  (tags/v3.10.11:7d4cc5a, MSC v.1929, 64 bit AMD64). `python` on PATH is a WindowsApps stub; use explicit path.
- pip: 25.0.1.
- python-flint: 0.9.0 (bundles FLINT 3.6.0, which includes Arb).
- Console script: `zeta-zero-verify.exe` (installed via `pip install -e <repo>`).

## Sources (local paths; hashes re-computed)

| Item | Path | sha256 (this run) |
|---|---|---|
| Draft repo (paper/.tex/.txt, docs, src, certs, tests) | `literature/raw/zeta-simple-zeros/` | files hashed individually (§ below) |
| Anthropic v2 paper | `literature/raw/claude-paper-main-v2-20260813.pdf` (+`.txt`) | task-packet: sha256 6792988E6CD0E17690621CE898ABD5D534F98407741BC7CB14BBE7D07C77D72F |
| Anthropic expert note | `literature/raw/claude-paper-note.txt` | — |
| Lean snapshot | `literature/raw/zeta-23-lean/` | commit 3635e74826a4c1fcece7d1cd2b6fa75e43a00510 (per packet) |
| Goldston–Suriajaya 2025 | `literature/raw/gs-2511.20059.pdf` (+`.txt`) | arXiv:2511.20059v2 |

Note: `zeta-simple-zeros/` is NOT a git repository in this checkout (history stripped by project
snapshot). The packet's commit `040c5e8` cannot be re-confirmed locally; contents are taken as the
audited snapshot.

## Commands run (verbatim)

```
pip install -e F:\LaTeX\Riemann Conjecture\literature\raw\zeta-simple-zeros
zeta-zero-verify three
zeta-zero-verify seven --progress-every 1000000     # ~2–3 min, run as background job
py -m unittest discover -s <repo>\tests -v
```

## Results

### three-point (`zeta-zero-verify three`)

```
certificate=three-point
verified=true
target=epsilon_4 >= 221/1000000
grid=16000
precision_bits=128
kernel_table_sha256=e19c06374eaf6dfa04a4de0bc0083ba6570cb62cb0888852ddef42bb0f279387
initial_boxes=1
nodes=7157
pruned=3579
splits=3578
maximum_depth=32
elapsed_seconds=0.418387
certified_epsilon=0.000221
domain=u>=0, v>=0, u+v<=4

H0=0.6725007036794116
three_point_bound=0.6725197671136778
seven_point_bound=0.6730085279277798
```

`certificates/three-point.txt` committed values: grid 16000, nodes 7157, pruned 3579, splits 3578,
max depth 32, same table hash → **EXACT reproduction**.

### seven-point (`zeta-zero-verify seven --progress-every 1000000`)

```
verified=true
target=F6 >= 19/5000
grid=4000
precision_bits=128
kernel_table_sha256=a9992300d2bf71665aa2b6bd2727e798624cd297103bb200c7f0ca2baea55a2c
second_derivative_table_sha256=7913c5511a572c32dd573cd53123d8cf3ddf73d3ec63b1aa823faae2ae83570a
initial_boxes=729
nodes=707901
pruned=354315
splits=353586
maximum_depth=37
elapsed_seconds=190.576759
interval_pruned=257493
pressure_pruned=3087
tangent_pruned=93735
surviving_gap_components_cells=[3809,4778];[7221,9363];[10572,44827]
surviving_gap_components_count=3

H0=0.6725007036794116
three_point_bound=0.6725197671136778
seven_point_bound=0.6730085279277798
```

`certificates/seven-point.txt` committed: same table hashes, nodes 707901, pruned 354315, splits 353586,
depth 37, interval_pruned 257493, pressure_pruned 3087, tangent_pruned 93735, surviving components
`[3809,4778];[7221,9363];[10572,44827]`, count 3 → **EXACT reproduction** (elapsed 190.6s vs 136.7s
committed — hardware variance only; all deterministic counters match).

### Unit tests

`Ran 7 tests ... OK` (test_constants ×3, test_kernel ×3, test_three_certificate ×1).

Full logs: `reproducibility/three-point-run.txt`, `reproducibility/seven-point-run.txt`.

## File hashes (draft repo key files)

Computed at audit time:
- `paper/riemann.pdf`, `paper/riemann.tex`, `paper/riemann.txt`, `docs/proof.md`, `docs/verifier.md`,
  `README.md`, `certificates/three-point.txt`, `certificates/seven-point.txt`,
  `src/zeta_simple_zeros/{cli,constants,kernel,report,rounding,verify_three,verify_seven}.py`
  — see `reproducibility/sha256-repo.txt` for hashes.

## Trust base

The finite verifier (docs/verifier.md) trusts: IEEE-754 binary64 semantics as implemented by the JIT,
`python-flint` (Arb/FLINT), the short repo source, and the OS/hardware. It does not trust cached tables,
sampled floating-point optimization, or committed run logs. This audit additionally confirms the source
reconstructs all enclosures from the formulas on each run (hashes match).
