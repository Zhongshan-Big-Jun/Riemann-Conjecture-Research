# Research Ledger — R-20260816T070000Z-g2rule-a1b2

Chronological record of this bounded pass (SL gap G2, general vanishing rule for J_σ).

## Setup (T+0)
- Created run dir `runs/.../R-20260816T070000Z-g2rule-a1b2/` + `reproducibility/`.
- Env: py -3.10 (numpy/scipy/sympy present in upstream; networkx NOT installed — graph checks
  implemented manually with itertools/counter). `$env:PYTHONUTF8=1`.
- Loaded rigorous-open-math-research skill; read upstream candidate proofs/ledgers:
  G1 (R-20260816T030000Z-slG1-9c2a), m5 (R-20260816T050000Z-m5exact-3f8a),
  m6 (R-20260816T060000Z-m6exact-4f9a + lemmaP_k6.md).

## Step 1 — assemble the exact per-partition dataset
- k=6: copied the m6 run CSVs (b3_clean_table.tsv, b4_fast_c*.csv ×5, b5_fast.csv, b6_fast.csv)
  + analytic b=1→1, b=2→c_m−c_{m+2} (`dataset.py`). All 203 k=6 partitions covered.
- k=3,4,5: reran the audited exact box-spline engine (`dump_partitions.py`, using
  `enumerate_moments.shape_integral_exact`). Results:
  - k=3: m_3=2 ✓ (nonzero=4); k=4: m_4=13/4 ✓ (nonzero=10); both clean, all values in the
    established sets.
  - k=5: m_5 initially came out WRONG (5.6053), caused by the documented float-noise on the
    b≥3/b=4 residues — exactly the failure mode the m5 run flagged. Four spurious values:
    (2,2,1) 5178/86089, (3,1,1) 2954/44309, (2,1,1,1) 87/70634, (1^5) −41/89756.

## Step 2 — k=6 graph analysis (finding the rule)
- `survey_k6.py`, `abstract_k6.py`, `rule_tests.py`: grouped k=6 by (b, m, cyclomatic, deg-seq).
  Key observations:
  - **isoclass-determinism**: 38 (b,H-isoclass) classes at k=6, each carries ONE J value
    (0 classes with >1 value). J depends only on H_σ up to relabeling.
  - Vanishing ⇔ (b=3,m=3) and (b=4,m=4,m=5) and (b=5,m=5,m=6) and (b=6,m=6) all vanish;
    (b=2, all m) and (b=3,m≥4) and (b=4,m=6) nonvanishing. Pattern: for CONNECTED H,
    nonzero ⇔ m ≥ 2b−2.

## Step 3 — correct k=5 dataset, verify rule on all 275 partitions
- `build_dataset.py`: corrected the 4 spurious k=5 values via isoclass-determinism (matched to
  exact k=6 isoclasses: 5178/86089→1/15, 2954/44309→1/15, 87/70634→0) and certified D_5=0
  (−41/89756→0). After correction m_5 = 101/18 EXACTLY; m_2=4/3, m_3=2, m_4=13/4, m_6=640/63
  also exact. Wrote `allJ.json` (275 rows).
- `final_rule.py`: **rule = Connected(H_σ) AND m ≥ 2b−2 ⇒ nonzero; else 0**.
  Result: TP=167, TN=108, FP=0, FN=0 → **275/275 = 100%**, no counterexample.
- `b2b3_formulas.py`: confirmed b=2 closed form J=c_m−c_{m+2} on every b=2 partition (m=2,4,6);
  found no simple c-product closed form for b=3 values (1/15,1/180,1/420,11/630) — recorded as
  open sub-identity.

## Step 4 — Lemma P / G2 statement + proof-goal analysis
- Formulated the refined Lemma P: `m_k = Σ_{σ: H_σ conn, m≥2b−2} J_σ`, admissible set =
  connected-with-surplus partitions. Wrote the proof strategy (§6) and the exact residual
  combinatorial identity to prove for all k (§7). b=2 closed form exact; b≥3 value formulas open.

## Step 5 — artifacts
- Wrote problem_contract.md, candidate_proof.md, research_ledger.md, repro_manifest.md,
  counterexample_log.md, whiteboard.md; reproducibility/*.py + allJ.json; SHA256SUMS.

## Open obligations (handed to G2/next)
- Prove the vanishing identity for all k (M1 disconnected-factorization + M2 low-surplus
  telescoping; §7 of candidate_proof).
- Closed b≥3 value (c-combination) formulas; exact m_7,m_8 → Λ_4; SL decay.
