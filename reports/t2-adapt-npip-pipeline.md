# T2 adaptation plan: use npip99 proof-certificate pipeline for our k=9 certificate

Status: **PLAN / REFERENCE** — based on `literature/raw/zeta-zeros-npip/`.

## Reference already available

- `proof_certificate/export_interval_tree.py`: compact `Z23TREE1` forest
  topology format, generic in `q` and root count.
- `proof_certificate/export_annotated_tangent.py`: `Z23ANN1` leaf-tagged
  topology + exact rational tangent payloads (currently specialized for
  q=6/7-point weights).
- `lean/Zeta23Ext/VerifiedCertificateForest.lean`,
  `VerifiedAnnotatedForest.lean`, `VerifiedAnnotatedForestDecoder.lean`,
  `CurrentInitialRoots.lean`: Lean decoders and connection theorems.
- `lean/END_TO_END_TODO.md`: the exact remaining gaps for upstream.

## Steps to adapt to our k=9 certificate

1. **Instrument our generalized verifier** (`verify_kpoint_parallel.py`) to emit
   `root`, `path`, `leaf/split` JSON/event records, or gzip per-root streams
   compatible with `export_interval_tree.py from-events / from-root-dir`.
2. **Run a traced export** of the k=9 `F₈ ≥ 392/100000` certificate
   (grid-2000). The topology will be much larger than npip's 1.7M-node
   seven-point forest, but the binary `Z23TREE1` format is compact (1 byte per
   node). This export is a long-running job and should wait until current
   background jobs settle.
3. **Emit root boxes** in `Z23ROOT1` format (integer grid-cell intervals).
4. **Reuse the generic Lean forest decoder** (or port it) for any `q`; verify
   root count and node counts.
5. **Use our already-compiled exact kernel table**
   (`KernelTableGrid2000.lean`) for the ordinary-leaf lower-bound side.
6. **Handle tangent leaves**:
   - The npip pipeline already has scalable/tangent semantic machinery, but
     the concrete tangent artifact for a 64M-node k=9 forest may be enormous.
   - Need to decide whether to:
     a. Reuse npip's `export_annotated_tangent` by generalizing from q=6 to
        q=8 and adapting weights; or
     b. Generate a tangent-free coarser certificate for T2 (harder, but
        avoids 406k+ tangent payloads).

## Main risks

- The k=9 forest has ~64.7M nodes; topology is large but maybe manageable
  (~64 MB binary). Lean replay of millions of nodes is a serious engineering
  challenge.
- The exact rational kernel table is done; the next trust boundary is the
  per-leaf lower-bound arithmetic and tangent evidence.
- Upstream npip itself has not yet completed full Lean replay; we should not
  expect the k=9 version to be easy.

## Recommendation

1. Wait for `bash-39` (k=9 terminal-box count) and `bash-41` (independent
   upstream verification) before deciding on full trace export.
2. Study `literature/raw/zeta-zeros-npip/lean/END_TO_END_TODO.md` as the
   canonical checklist.
3. First attempt a **prototype trace export for our canonical k=7 or k=9**
   and compare its topology size/count to npip's seven-point reference.
