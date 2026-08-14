# Audit Report — k=9 record

Run: `R-20260814T045000Z-extpress-2f36ae`.

Status: **RIGOROUS_PARTIAL_RESULT** — new record $C_9=0.673053645952589925\ldots$
established with a finite Universally-quantified Arb certificate.

## Scope of this audit
Adversarial, independent re-check of every link in the k=9 chain, performed by the
solver within this run (the k=9 certificate itself is a deterministic Arb
branch-and-bound whose counts/hashes are recorded).

## 1. Code correctness (generalized verifier)
- `verify_kpoint.py` / `verify_kpoint_parallel.py` were derived from the repo's
  `verify_seven.py` by making k a parameter. To rule out transcription bugs, both
  were run at k=7 target 19/5000 and compared byte-for-byte with the committed
  repo certificate:
  - kernel_table_sha256 `a9992300…` (identical)
  - second_derivative `7913c551…` (identical)
  - nodes=707901, pruned=354315, splits=353586, maximum_depth=37,
    initial_boxes=729, surviving components `[3809,4778];[7221,9363];[10572,44827]`
    (all identical).
  The k=9 run uses the same code path with k=9; structural soundness is inherited.

## 2. Certificate soundness (k=9)
- Coverage: (a) pressure cutoff handles Σg≥cutoff; (b) one-body pruning
  $U(g)=g/4000+w(g)/4$ removes cells that alone force $F_8\ge0.0039$; (c) the
  remaining 256 product boxes are subdivided with valid interval and convex-tangent
  (Arb-LDL-certified positive-definite Hessian) lower bounds. A terminal unresolved
  cell raises an error (verified present in code) and did NOT occur.
- Therefore `verified=true` ⟹ $F_8(g)\ge39/10000\ \forall g_i\ge0$.

## 3. Derivation correctness (general-k chain)
- `derive_general_k.py` independently reproduces k=7 (0.6730085279277797613235)
  and k=3 (0.672519767113677707121).
- Exact rational: m_9=264, A0=624/625 (A0<1 ✓), A0/m=26/6875,
  (m-1)/(500m)=263/132000, denominator 1−A0/m=6849/6875,
  $C_9=(6875H_{\rm MT}-1315/96)/6849$. Verified at 80 dps.

## 4. Honest limits
- The k=9 certificate is not machine-formalized in a proof assistant (matches the
  accepted 7-point state; no Lean artifact ships in the repo). Label is
  RIGOROUS_PARTIAL_RESULT / FINITE_COMPUTATIONAL_RESULT for the certificate, not
  FORMALLY_VERIFIED.
- Scoping minima (k=9 ~0.00398, k=11 TBD) are numerical evidence ONLY, not used
  in any theorem.

## Findings
No error found in the record claim. Residual risk: correctness of python-flint/Arb
0.9.0 and IEEE-754 semantics (the same trust base the field already accepts for the
7-point certificate).
