# npip99 proof-certificate infrastructure — relevance to our T2 reflection

Status: **UPSTREAM_REVIEW / INFORMATION**  
Source: `https://github.com/npip99/zeta-zeros`  
Commit: `72a01ac`  
Copied to: `literature/raw/zeta-zeros-npip/` (2026-08-23)

## What this repository contains

This repository proves a 0.673195198901 lower bound, but more importantly for
our project it contains a **proof-certificate infrastructure** for turning a
finite interval certificate into a Lean-checkable artifact:

- `proof_certificate/export_interval_tree.py`: exports the branch-and-bound
  forest as a compact binary/trace format.
- `lean/Zeta23Ext/VerifiedCertificateForest.lean` and related modules: Lean
  decoder + elementary connection theorem for the recorded seven-point
  production layout.
- `lean/Zeta23Ext/VerifiedAnnotatedForestDecoder.lean`,
  `VerifiedAnnotatedForest.lean`, `CurrentInitialRoots.lean`,
  `CurrentWindowFiniteCertificate.lean`, etc.
- Explicit `END_TO_END_TODO.md` checklist.
- `certificates/weighted-p1-grid4000.tree`, `.roots.json`, `.roots.bin` with
  SHA-256 records.

## What is already checked in Lean

The Lean project under `lean/` checks, according to upstream README:

- exact window constants and 21-weight table;
- sharp square-root profile and realizing correlation matrices;
- large-span/small-span block split, pinching, offset averaging, error
  bookkeeping;
- final strict numerical comparison and conditional dyadic-to-cumulative
  passage;
- internal kernel checks for several transcendental inequalities;
- the capstone theorem has exactly **one premise**: the local seven-point
  search certificate.

## What remains open upstream

- Full kernel replay of the local 1,739,356-node search;
- Formal semantics for the 406,186 tangent-pruned leaves;
- Exact dyadic table data for the two transcendental kernel tables.

## Relevance to our T2 reflection

This is essentially a **working prototype of the T2 path** for a seven-point
certificate:

- It already exports production forests and root boxes;
- It already has Lean decoders and a connection theorem;
- The remaining gap is tangent-leaf semantics and exact kernel table data.

This is directly usable as a model for our k=9 T2 certificate:
- We already have the exact-rational kernel table
  (`KernelTableGrid2000.lean`) that compiles.
- We would need to produce a k=9 export forest with the same format, or adapt
  the npip99 proof-certificate pipeline to our generalized k-point verifier.

## Recommendation

1. Keep `literature/raw/zeta-zeros-npip/` as the primary reference for T2.
2. Before designing a new coarser partition, study the npip99
   `proof_certificate` pipeline and its Lean decoders.
3. The k=9 terminal-box count benchmark (likely tens of millions) shows why a
   direct export may be too large; the npip99 approach still demonstrates a
   viable direction: export the forest topology, not the full flat box list.
4. Explore whether the npip99 infrastructure can be adapted to our k=9
   generalized verifier with its uniform weights.

## Honest label

This is a review of another repository. No new bound or proof is claimed here.
