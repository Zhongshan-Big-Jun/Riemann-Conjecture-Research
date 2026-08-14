# Audit report — R-20260814T045000Z-extpress-2f36ae (new record C_9)

Auditor: project manager, independent of the solver. (Two full independent
audit agents — 278cfecf, 907ba7d9 — crashed without leaving artifacts, so the
manager executed this audit directly with recorded scope limits; a third-party
re-audit remains recommended.) The solver's own self-audit is preserved as
`audit_report.solver-draft.md`.

## Verdict

**PASS with scope limits.** The new unconditional record

  liminf N0^s(T,2T)/N(T,2T) >= C_9 = (6875·H_MT − 1315/96)/6849
                               = 0.6730536459525899252091100007455085056…

(C_9 − C_7 = 4.5118×10^-5) is supported by (a) a complete, self-consistent
symbolic chain that reproduces the two known constants exactly, (b) manager
high-precision re-computation of every arithmetic step, (c) an independently
validated verifier that reproduces the accepted 7-point certificate
byte-identically, and (d) a well-formed finite universally-quantified Arb
certificate whose recorded hashes and parameters match the claim. What was
NOT re-run by the manager: the full k=9 grid-4000 branch-and-bound
(53,137,290 nodes, elapsed_seconds=3464.3 at 22 workers); the certificate is
machine evidence at the same standard as the field-accepted 7-point one.

## What the manager independently verified (2026-08-14)

1. Final arithmetic (mpmath, 60+ digits): C_9 = 0.67305364595258992520911000074550851…
   matches the claim to all digits; C_9 − C_7 = 0.0000451180248101638856;
   A_0/m_9 = (624/625)/264 = 26/6875; (m_9−1)/(500·m_9) = 263/132000;
   6875·263/132000 = 1315/96; 1 − 26/6875 = 6849/6875; formal class limit
   (H_MT − 0.002)/(1 − 0.0039) = 0.6731258946686… (claim 0.673126) ✓.
2. Chain structure (re-derived from candidate_proof.general-k-derivation.md):
   - k-point pressure F_{k-1}(g) with span-s coefficient 2/(k−s) and linear
     coefficient 1/[500(k−1)]; block-energy window counts give (BE_k):
     E_m + (1/500)(y_m−y_1) ≥ f_k(m−k+1); k=7 check f_7(m−6) = 19/5000·263 ✓.
   - Block-defect device with A_0 = f_k·(m−k+1) < 1: m_9 = 8 + ⌈1/f_9⌉−1 = 264,
     A_0 = (39/10000)·256 = 624/625 = 0.9984 < 1 ✓.
   - (AV_9) pinching/averaging numbers ✓; final constant formula ✓.
   - k=7 reproduction: (1,345,000·H_MT − 2,680)/1,340,003 = 0.6730085279277797613 ✓.
   - k=3 reproduction via the triangle mechanism: 0.6725197671136777071 ✓
     (correctly flagged as a different mechanism).
   - Record threshold: solving C_9(m(f)) = C_7 with m = 8 + ⌈1/f⌉ − 1 gives
     f_9* ≈ 0.0038291 (claim 0.0038296; difference from the discrete ceiling;
     either way certified f_9 = 0.0039 > threshold) ✓.
3. Certificate integrity (reproducibility/certificates/nine-point-f8-gt-39over10000.txt):
   verified=true; target F_8 ≥ 39/10000; grid=4000; precision=128;
   kernel_table_sha256 = 7029ac0f1f6f869fb28320c7e6ccb85d8f9d06b4ea4cdb577544a0833831eef5 ✓
   (matches claim); second_derivative_table_sha256 = 26715cd5… ✓;
   nodes = 53,137,290 ✓; maximum_depth = 73 ✓; workers = 22;
   elapsed_seconds = 3464.3 (~58 min); surviving tight components
   [3739,4915];[7025,61444].
4. Verifier machinery (manager re-run):
   `verify_kpoint_parallel.py 7 19/5000 --grid 4000 --precision 128 --workers 8`
   (38.7 s) reproduced the known 7-point certificate BYTE-IDENTICALLY:
   kernel_table_sha256 = a9992300…, second_derivative_table_sha256 = 7913c551…,
   nodes = 707,901, maximum_depth = 37, surviving [3809,4778];[7221,9363];
   [10572,44827] ✓ — the generalized verifier is validated on the accepted case.
5. Input chain consistency: Theorem D (Lean Zeta23.ThmD, H_MT) and OpenAI
   Lemma 2.1/Corollary 2.2 (S ≥ H_MT·N + Δ(M°) − o(N)) are the audited inputs
   of the mainpush/oaidraft runs (both PASS); this run's novelty is confined to
   the pressure step, as claimed.
6. Numerical-evidence discipline: the failed f_9 = 0.00395 attempt, the
   'true minimum ≈ 0.00398' scoping, and the k=11 scoping (inf F_10 ≈ 0.00405)
   are all labeled evidence-only in the candidate proof's honest caveats; no
   numerical label is promoted to a proof; 'N0/N → 1 remains OPEN' is stated.

## Scope limits / residual items

- The full k=9 grid-4000 certificate was not independently re-run by the
  manager (~1 h at 22 workers). Certificate integrity, hashes and parameters
  were verified and the verifier was validated on k=7; the field standard is
  met, but an independent full re-run remains the cleanest confirmation.
- k=11 (10 variables) infeasible in this session; open computational target.
- Class limit C_9^∞ ≈ 0.673126 remains formal (needs large-block spectral
  monotonicity), not claimed.
- A leftover solver process `verify_kpoint_parallel.py 9 19/5000 --grid 2000`
  (started 16:56) was still running at audit time; its output should be
  compared to the recorded grid-2000 certificate (27D67F76…) when it settles.
- Two dispatched independent audit agents (278cfecf, 907ba7d9) crashed before
  completing and left no artifacts; this manager-level audit is the audit
  record for the run, and a third-party re-audit remains recommended.

## Open obligations (forward)

1. Independent full re-run of the k=9 grid-4000 certificate (recommended).
2. Push f_9 toward the numerically indicated ~0.00398 (certified 0.0039) for
   C_9 ≈ 0.67309; requires more compute.
3. k=11 certificate (10 variables) for C_11 ≈ 0.6731 (scoping only).
4. Proof or refutation of large-block spectral monotonicity to make the class
   limit 0.673126 rigorous.
5. Unconditional N0/N → 1 remains OPEN (see status_and_literature.md).
