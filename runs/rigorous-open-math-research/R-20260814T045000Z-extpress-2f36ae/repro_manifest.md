# Reproducibility Manifest

Run: `R-20260814T045000Z-extpress-2f36ae`. Solve role, O3 (extend >7 zeros) + O2 (support).
All computations reproducible with the commands below.

## Host / OS / tools
- Windows x86-64; 22 logical CPUs.
- Python 3.10.11.
- python-flint 0.9.0 (Arb/FLINT; module `flint`, types `arb`, `fmpq`).
- numpy 2.2.6, mpmath 1.3.0, scipy 1.15.3.
- OpenAI draft repo at `literature/raw/zeta-simple-zeros` (commit `040c5e899e…`),
  installed in editable mode; its tests (7/7) pass.

## Inputs (exact, hashed in prior runs)
| Source | Path | Used for |
|---|---|---|
| OpenAI draft repo (verifier, certificates, paper) | `literature/raw/zeta-simple-zeros/` | O2 re-verify; k=9 code base |
| Claude paper v2 | `literature/raw/claude-paper-main-v2-20260813.txt` | Theorem D / baseline |
| mainpush run | `runs/rigorous-open-math-research/R-20260814T041219Z-mainpush-3cdc81/` | verified chain, ceiling |

## O2 re-verification (this run, byte-identical to committed)
```
cd literature/raw/zeta-simple-zeros
py -3 -m pip install -e .
py -3 -m unittest discover -s tests -v            # 7 tests pass
py -3 -m zeta_simple_zeros three --json           # 3pt PASS
py -3 -m zeta_simple_zeros seven                  # 7pt PASS (~210 s)
```
- 3-point: kernel_table_sha256=e19c06374eaf6dfa04a4de0bc0083ba6570cb62cb0888852ddef42bb0f279387,
  nodes=7157. Byte-identical.
- 7-point: kernel_table_sha256=a9992300d2bf71665aa2b6bd2727e798624cd297103bb200c7f0ca2baea55a2c,
  second_derivative_table_sha256=7913c5511a572c32dd573cd53123d8cf3ddf73d3ec63b1aa823faae2ae83570a,
  nodes=707901, initial_boxes=729. Byte-identical.

## General-k derivation (symbolic + numeric checks)
```
py -3 reproducibility/derive_general_k.py     # C_k(m), rigor condition, class limit
```
Reproduces k=7 → 0.6730085279277797613235; k=3 (triangle) → 0.672519767113677707121;
class limit → 0.67305832531561096741. Scripts: `derive_general_k.py`, `threshold_analysis.py`.

## Generalized verifier (validated k=7 byte-identical)
- `verify_kpoint.py` (single-thread) and `verify_kpoint_parallel.py` (multiprocessing).
- Validation: `verify_kpoint_parallel.py 7 19/5000 --grid 4000 --precision 128 --workers 8`
  → byte-identical to repo (kernel `a9992300…`, nodes 707901, etc.).

## ★ k=9 certificate (record) ★
```
cd runs/rigorous-open-math-research/R-20260814T045000Z-extpress-2f36ae/reproducibility
py -3 verify_kpoint_parallel.py 9 39/10000 --grid 4000 --precision 128 --workers 22
```
Output (certificate `nine-point-f8-gt-39over10000.txt`):
```
certificate=9-point   verified=true   target=F8 >= 39/10000
grid=4000   precision_bits=128
kernel_table_sha256=7029ac0f1f6f869fb28320c7e6ccb85d8f9d06b4ea4cdb577544a0833831eef5
second_derivative_table_sha256=26715cd56ad6749da44654e793f2bfa6b3f02130bc154ec0bb0c04bb33f294e1
initial_boxes=256   nodes=53137290   pruned=26568773   splits=26568517   maximum_depth=73
pressure_pruned=108372  interval_pruned=17538303  tangent_pruned=8922098
surviving_gap_components_cells=[3739,4915];[7025,61444]
```
States: **F_8(g1..g8) >= 39/10000 for every gi>=0** (exhaustive branch-and-bound on
Arb-built tables; deterministic counts). Second k=9 certificate (grid 2000, target
19/5000) in `nine-point-f8-gt-19over5000-grid2000.txt`.

## Constant
```
C_9 = (6875*H_MT - 1315/96)/6849 = 0.67305364595258992520911000074550850560855295008598…
     (m_9=264, A0=624/625, A0/m=26/6875, (m-1)/(500m)=263/132000)
```
`py -3 -c "import mpmath as mp; mp.mp.dps=80; H=...; print((6875*H-mp.mpf(1315)/96)/6849)"`.

## Honest note on determinism / parallelism
Node/split/prune counts and both table hashes are deterministic functions of
(grid, precision, target, k): each top-level box branch-and-bound is independent,
so the parallel split yields the same total counts and the same hashes as the
single-thread version (verified on k=7). Non-deterministic fields (`elapsed_seconds`)
vary and are informational only.

## Record-push & k=11 (reported; not part of the record)
- k=9 target 79/20000=0.00395 (grid 2000): attempted on 22 workers, NOT certified
  within ~90 min (>36k core-s); cost grows steeply as f_9→true-min (~0.00398).
  Record headline = f_9=0.0039 certificate above.
- k=11 scoping min F_10 ≈ 0.00405 (numerical, evidence only). Exhaustive k=11
  (10 vars) infeasible in this session's time. Scripts: `scoping_k9.py`, saved
  optima `k7_opt.npy`, `k9_opt.npy`.

## Trust base
Python/IEEE-754/Arb(python-flint)/the generalized source in `reproducibility/`
(validated against the repo's 7-point certificate byte-identically). No proof
assistant formalization of the k=9 certificate (matching the 7-point state).
Status label: FINITE_COMPUTATIONAL_RESULT for the certificate;
RIGOROUS_PARTIAL_RESULT for the record theorem.
