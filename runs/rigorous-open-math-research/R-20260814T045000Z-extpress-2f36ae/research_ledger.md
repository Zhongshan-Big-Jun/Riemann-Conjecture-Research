# Research Ledger

Run: `R-20260814T045000Z-extpress-2f36ae`. Solve role, obligations O3 (extend >7
zeros) + O2 (re-verification). Chronological.

## Entry 1 (env / O2 re-verification)
- Python 3.10.11, python-flint 0.9.0, numpy 2.2.6, mpmath 1.3.0, scipy 1.15.3.
- `pip install -e` in `literature/raw/zeta-simple-zeros` OK. 7 unit tests pass.
- Re-ran repo verifier: 3-point byte-identical (kernel `e19c0637…`, nodes 7157),
  7-point byte-identical (kernel `a9992300…`, second-deriv `7913c551…`,
  nodes 707901, initial 729, components `[3809,4778];[7221,9363];[10572,44827]`).
- O2 re-verified byte-identically. (Ledger of mainpush confirms same values.)

## Entry 2 (general-k chain derived; reproduces k=3,k=7)
- Wrote `derive_general_k.py`: $C_k(m)=\frac{H_{\rm MT}-(m_k-1)/(500m_k)}{1-A_0/m_k}$,
  $A_0=f_k(m_k-k+1)$, $m_k=(k-1)+\lceil1/f_k\rceil-1$.
- Reproduction: k=7 → 0.6730085279277797613235 ✓; k=3 (triangle) →
  0.672519767113677707121 ✓; class limit (formal) = 0.6730583253156… ✓.
- Full symbolic write-up: `candidate_proof.general-k-derivation.md`.

## Entry 3 (generalized verifier `verify_kpoint.py` written + validated)
- Generalized repo `verify_seven.py` to arbitrary k; same certificate format,
  reuses kernel/rounding/report modules.
- Fixed first attempt: second-derivative table start must be ~0.95*GRID (not
  0.95*cutoff). 
- Validation k=7 target 19/5000: byte-identical to the repo certificate
  (same hashes, nodes 707901, pruned 354315, splits 353586, all counts). The
  generalized code is correct.

## Entry 4 (record threshold analysis — key)
- `threshold_analysis.py`: For k=9, $C_9>0.673008528$ exactly when certified
  $f_9\ge f_9^*\approx0.0038296$. Formal class limit beats the record when
  $f_k>0.0037263$.
- Table: at f=1/n, n=262→C_9=0.6730007 (below), n=261→0.6730100 (above).
- So a certified $f_9\in(0.0038296, f_9^{\rm true}]$ yields a new record.

## Entry 5 (scoping: f_8 true min — evidence only)
- Fixed scoping kernel bug (used k not w=k^2) and pressure-term dropout.
- scipy L-BFGS-B multi-start: k=7 min F_6 ~ 0.003826 (consistent with certified
  0.0038); **k=9 min F_8 ~ 0.003982**.
- k=9 optimum gaps ≈ [1.047,1.993,2.002,2.002,2.002,1.993,1.992,1.047], points
  near integers (zeros of w). Evidence only; true min has uncertainty but is well
  above the 0.0038296 record threshold.
- Therefore a certified f_9 = 0.0039 (>0.0038296, < ~0.00398) is expected feasible
  and yields C_9 ≈ 0.673054 (new record).

## Entry 6 (one-body component analysis)
- `inspect_components.py`: k=9 U(g)=g/4000+w(g)/4 target 0.0038 → only 2
  one-body components → initial_boxes = 2^8 = 256 (vs 729 for k=7). Components:
  [3745,4902] (x~0.94-1.23) and [7043,60578] (x~1.76-15.1). Smaller search space
  than k=7; promising for feasibility.
- For targets up to 0.0042 still 2 components (256 boxes).

## Entry 7 (k=9 exhaustive certificate — calibration)
- Single-thread grid-4000 8D too slow (>695s, no 100k nodes). 
- Built `verify_kpoint_parallel.py`: splits the 256 initial boxes across
  multiprocessing workers. Validated byte-identically on k=7 (nodes 707901, all
  hashes/counts match) in 34s vs 195s single-thread.
- 22 CPUs available. 
- **k=9 grid=2000 target 19/5000: CERTIFIED in 1333s / 28,319,266 nodes**,
  max_depth 68, initial_boxes 256, components [1872,2451];[3521,30289], interval
  pruned 10.8M, tangent 3.26M, pressure 96k. kernel `8eb1094b…`, second `3a613576…`.
  First rigorous k=9 certificate (f_9>=0.0038). Feasible but 28M nodes.

## Entry 9 (★ NEW RECORD — k=9, f_9>=39/10000) ★
- **CERTIFIED F_8 >= 39/10000** (k=9, 8 vars), grid 4000, 128-bit, 22 workers.
  kernel `7029ac0f…`, second `26715cd5…`, nodes **53,137,290**, initial 256,
  max_depth 73, components [3739,4915];[7025,61444]. 3464s-equiv, ~35 min wall.
  Report: reproducibility/certificates/nine-point-f8-gt-39over10000.txt.
- General-k chain → **C_9 = (6875·H_MT − 1315/96)/6849 = 0.67305364595258992521**,
  with m_9=264, A0=624/625=0.9984<1, A0/m=26/6875, (m-1)/(500m)=263/132000.
- **NEW UNCONDITIONAL RECORD**: 0.673053646 > 0.673008528 (k=7) by ≈4.51e-5.
- candidate_proof.md written (full chain, RIGOROUS_PARTIAL_RESULT).

## Entry 8 (record plan)
- C_9 at certified targets: f_9=0.0038→0.672990 (below record); f_9=0.0039→
  **0.673053645952589925** (record); f_9=0.00395→0.6730856; f_9=0.004→0.6731171.
- Scoping min F_8 ~0.00398 (evidence). Target **f_9=0.0039** chosen: below true
  min (should certify), comfortably above 0.0038296 record threshold.
- LAUNCHED k=9 grid=4000 target 39/10000 (record-seeking) across 22 workers.

## Entry 10 (record push + k=11 scoping — FINAL)
- **k=9 target 79/20000=0.00395 (grid 2000)**: launched across 22 workers; after
  ~90 min (>36k core-s) NOT certified in time — target too close to true min
  (~0.00398) → near-min subdivision blows up. Record headline kept at f_9=0.0039.
  Honest obstruction: branch-and-bound cost grows steeply as f_9→true min.
- **k=11 scoping min F_10 ~ 0.00405** (numerical, evidence only). Hypothetical C_11
  at f_11=0.004 ≈ 0.673097 (would exceed C_9), but k=11 is 10 variables;
  exhaustive verification infeasible in this session's time (k=9 8D took 53M
  nodes; k=11 10D is orders of magnitude worse). k=11 cert left OPEN/infeasible.
- **FINAL RECORD this run: f_9=0.0039 cert → C_9=0.673053645952589925.**
