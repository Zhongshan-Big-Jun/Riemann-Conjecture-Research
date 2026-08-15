# Obligation Graph — SL gap G1 (D_k = 0), run R-20260816T030000Z-slG1-9c2a

Dependency graph of claims, with proof status. Statuses: PROVEN, COMPUTER-VERIFIED (finite k),
EVIDENCE, OPEN.

```
SL  (μ_λ({0})=0)                      [inherited target; runner; OPEN at full SL]
  └─[T0/T1, audited run 7b21e4]─ Λ_m(0)=det(H_m)/det(H_m^{(00)}) → 0     [PROVEN reduction]
       └─[Lemma H]─ the matching-sum moment sequence has Λ_m(0)→0         [OPEN; not this pass]
            └─[Lemma P]─ m_k = Σ_{size-≤2 blocks} ∏c_{2t}                  [PARTIAL; see below]
                 └─[Lemma M]─ D_k = 0 for all k≥3                          [PARTIAL; see below]

Lemma M: D_k = Σ_{π∈S_k} sign(π) I_π = 0  (I_π = box-spline value of cycle∪π-edges)
  |-- (M1) coarea/box-spline exact form of I_π            [PROVEN, this pass; validated I_id=1]
  |-- (M2) signed-sum identity for ALL k                  [OPEN; PROVEN for k=3,4,5 (computer)]
  |-- (M2a) D_3 = 0 (computer-verified exact, this pass)  [DONE: float -4.4e-16, exact 0]
  |-- (M2b) D_4 = 0 (computer-verified exact, this pass)  [DONE: float -2.6e-15, exact 0]
  `-- (M2c) D_5 = 0 (computer-verified exact, this pass)  [DONE: float -5.7e-14, exact 0]
        (two independent box-spline implementations agree to ~1e-13; rational reconstruction
         certified to ~8e-15, denominators ≤180 unique-safe; isolated gap: exact/interval 6-D
         volume of each cross-section to make the individual rationals PROVEN not coincidental)

Lemma P: m_k matching-sum (blocks ≤ 2)
  |-- P1: pattern holds for k≤4 (audited m_4=13/4)        [PROVEN, earlier run]
  |-- P2: k=5 matching-sum vs D_5=0                        [PENDING, subagent adf8ef41]
  `-- P3: full repeated-index algebra ⇒ only ≤2-blocks     [OPEN; not fully closed]

Cross-cutting:
  |-- Literature: no direct D_k=0 theorem                 [PROVEN ABSENCE, two subagents, Verdict B]
  |-- Honesty: Johansson-Lambert + Brillinger ⇒ DPP higher cumulants generically nonzero
         ⇒ D_k=0 is NOT a generic quasi-free corollary     [ESTABLISHED; supports specialness]
  `-- Sanity: D_6 numerical evidence ≈ 0 (earlier pass)    [EVIDENCE only]

Derived impact: if M (all k) + P + H hold, then SL ⟸ matching-sum Hankel decay ⟸ SL.
This pass closes the exact base cases M(3),M(4),M(5) and the box-spline (M1); the general M, P, H
remain.
```

## Legend
- PROVEN: rigorous argument (or rigorous reduction) accepted.
- COMPUTER-VERIFIED (finite): exact rational identity for k≤5, reproducible, two implementations,
  rational reconstruction certified; the individual-var exact symbolicity is the isolated caveat.
- EVIDENCE: numerical/analytical support only.
- OPEN: not closed this pass with exact statement recorded.
