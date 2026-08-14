# Reproducibility Manifest

Run: `R-20260814T041219Z-mainpush-3cdc81`
Date: 2026-08-14 (UTC). All computations in this run are reproducible with the commands below.

## Host / OS / tools
- Windows environment, x86-64.
- Python 3.10.11 (`C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe`).
- python-flint 0.9.0 (cp310 abi3 win_amd64) providing Arb/FLINT bindings (module `flint`,
  `arb`, `fmpq`).
- numpy 2.2.6, mpmath 1.3.0.
- pip 25.0.1 / 26.2.1.

## Source inputs (exact, hashed at dispatch; verified present)
| Source | Local path | Role |
|---|---|---|
| OpenAI/GPT-5.6 Sol draft repo (commit 040c5e899e658aed7b56a2a87f501798fe10761d) | literature/raw/zeta-simple-zeros/ | O2 subject |
|  — paper/riemann.pdf / .tex / .txt | literature/raw/zeta-simple-zeros/paper/ | proof |
|  — verifier source | literature/raw/zeta-simple-zeros/src/zeta_simple_zeros/ | O2 |
|  — committed certificates | literature/raw/zeta-simple-zeros/certificates/ | comparison |
| Claude paper v2 (2026-08-13) + text | literature/raw/claude-paper-main-v2-20260813.pdf / .txt | Theorem D / §7 baseline |
| Lean snapshot (commit 3635e748…) | literature/raw/zeta-23-lean/ | ThmD verification |
| Goldston–Suriajaya 2025 | literature/raw/gs-2511.20059.pdf / .txt | O4 reduction |
| FRONTIER map | literature/maps/FRONTIER.md | B0 |

## Exact commands executed (O2 verifier)
```
py -3 -m pip install python-flint          # -> python-flint 0.9.0
cd literature/raw/zeta-simple-zeros
py -3 -m pip install -e .
py -3 -m unittest discover -s tests -v      # 7 tests, all pass
zeta-zero-verify three --json               # 3-pt PASS (see below)
zeta-zero-verify seven --progress-every 200000   # 7-pt PASS (exhaustive, ~200 s)
```

## Verification outputs (my runs vs committed)

3-point (`three-point.txt`): kernel_table_sha256 = e19c06374eaf6dfa04a4de0bc0083ba6570cb62cb0888852ddef42bb0f279387 ;
nodes=7157, pruned=3579, splits=3578, max_depth=32, verified=true.  IDENTICAL to committed.
Certifies `epsilon_4 >= 221/1000000` on {u,v ≥ 0, u+v ≤ 4}, grid 16000, 128-bit Arb.

7-point (`seven-point.txt`): kernel_table_sha256 = a9992300d2bf71665aa2b6bd2727e798624cd297103bb200c7f0ca2baea55a2c ;
second_derivative_table_sha256 = 7913c5511a572c32dd573cd53123d8cf3ddf73d3ec63b1aa823faae2ae83570a ;
initial_boxes=729, nodes=707901, pruned=354315, splits=353586, max_depth=37,
surviving gap components = [3809,4778];[7221,9363];[10572,44827].  IDENTICAL to committed.
Certifies `F6 >= 19/5000`, grid 4000, 128-bit Arb.

Note: node/tree counts are deterministic (pure branch-and-bound on an Arb-built lookup table),
so exact replication is expected and observed.

## Constant re-derivations (mpmath, ≥200 dp — scripts in reproducibility/)
- H_MT = 3/2 − (1/√2)·cot(1/√2) = 0.6725007036794116457343797908032951885934…  (matches claim)
- c1 = 1/(2 − H_MT) = 0.7532960678560706772165846282697276822957… ; 2 − 1/c1 = H_MT ✓
- three-point bound (H_MT − ε/4)/(1 − ε/2), ε=221/10^6 = 0.6725197671136777071… (67.2519767%)
- seven-point bound (1,345,000·H_MT − 2,680)/1,340,003 = 0.6730085279277797613… (67.3008528%)
- Psi identity min_{n≥0}[(p−n)² + 4n] = 2p − 1 + Ψ(p) verified at multiple p (exact arithmetic).
- defect numbers: A0=4997/5000, A0/m=4997/1,345,000, (m−1)/(500m)=268/134,500 ✓ (m=269)

## O3 ceiling computation
- c(m) = (H_MT − (m−1)/(500m)) / (1 − 19(m−6)/(5000m)); valid for m ≥ 7 with the 7-pt pressure.
- Rigorous for m ≤ 269 (A0 = 19(m−6)/5000 ≤ 1). At m=269: 0.6730085279….
- Asymptotic (formal, would need large-block spectral control) m→∞: 0.673058….
- script: reproducibility/probe_blocks.py

## O6 numerical
- mpmath.zetazero enumeration; N0(0,T)/N(T) computed at T=50..700 (see ledger/report).
- evidence only; cannot detect off-line zeros.

## Trust base
Python/IEEE-754/code as shipped in the draft repo for the certificates; Arb via python-flint
for all transcendental enclosures. The repository's `docs/verifier.md` was read and is
accurate. Unknown: whether the draft's chain (Lemma 2.1..Thm 1.1) has an independent Lean
formalization (none exists in the shipped repo; the repo ships only the two certificates'
verifier). Marked accordingly.
