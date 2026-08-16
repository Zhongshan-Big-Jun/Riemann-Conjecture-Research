# Counterexample Log — R-20260816T070000Z-g2rule-a1b2

Documented failed rules / edge cases encountered while determining the vanishing rule. The final
rule (connected & m ≥ 2b−2) had **0 counterexamples** on the 275-partition exact dataset.

## Candidate rules falsified by the data

1. **"(a) block-count threshold b ≥ T ⇒ 0"** — the k=5 finding "b≥4 ⇒ 0" does NOT generalize.
   At k=6, b=4 partitions are NONZERO (m=6: 20 partitions, values {1/105, −1/840, 1/1260, 4/315}).
   Ruled out as a universal rule (any fixed T fails on either k=5 or k=6).
2. **"(b) isolated block (degree-0 vertex in H_σ) ⇒ 0"** — never fires for b ≥ 2: since the cycle
   is closed, every block that is a proper subset is entered and exited ≥ 2 times, so H_σ has
   min-degree ≥ 2 for b ≥ 2. Trivially no predictive power.
3. **"(b') disconnected H ⇒ 0"** — NECESSARY but not sufficient: at k=6 every H_σ is connected
   (all blocks have degree ≥ 2, one component), and yet most partitions vanish. So connectivity
   alone leaves FP=0 but FN>0 (many connected partitions vanish).
4. **"(d) all-degrees-even (Eulerian) ⇒ nonzero / anything"** — always true (cycle closed),
   degenerately non-discriminating (control test with 0 accuracy contribution).
5. **"(c) H simple-support is a forest ⇒ 0"** — fails: e.g. b=3 m=5 with simple-support a triangle
   (all three support edges present) is NONZERO (J=1/180), while b=3 m=3 (also triangle support,
   m < 4) is 0. Forest-ness of the support is not the discriminator.
6. **"(e) m % 4 parity ⇒ 0"** — fails: b=2 m=2 (m%4=2) nonzero and b=3 m=4 (m%4=0) nonzero;
   b=3 m=3 and b=4 m=4 (m%4=3,0) vanish. No m-parity rule matches.
7. **"pure (b,m) threshold"** — fails: b=3 m=4 nonzero but b=4 m=5 zero; a threshold on m alone
   per b (e.g. "m > b") would misfire on these.

## Edge cases handled / recorded
- **k=5 exact-engine float noise**: 4 partitions (b=3 m=4 iso=01x2|02x2 ×2, b=4 m=4 4-cycle,
  b=5 D_5) returned spurious small rationals (5178/86089, 2954/44309, 87/70634, −41/89756).
  All corrected: the first two are the 1/15 over-counts, the latter two are genuine 0 (D_5
  certified =0; b=4 m=4 matches the k=6 exact 4-cycle = 0). Verified corrected sums give
  m_5=101/18 exactly. Not a rule counterexample — a data hygiene fix.
- **k=4 value-set note**: task brief lists k=4 nonzero {1,1/3,7/60,1/15,1/180}; the exact engine
  gives {1,1/3,7/60,1/15,0} with m_4=13/4 (1/180 first appears at k=5). The 1/180 in the brief is
  a mild over-count; no rule impact.

## Final rule counterexample count
- **0** (FP=0, FN=0 on all 275 exact partitions; `final_rule.py`).
