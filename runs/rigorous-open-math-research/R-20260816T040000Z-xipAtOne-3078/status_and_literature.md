# Status and Literature — M3-open-A AtOne certificate for κ₁(1,vMT)

## Current status
Math-level **closed**: the certified sandwich `κ₉ ≤ κ₁(1, vMT) ≤ κ₉ + ε₉` holds with
κ₉ = (aMT+J1)/( ∫vMT )² enclosed to ~5·10⁻¹⁶ (≪ ε₉ = 3.42·10⁻⁷), and H_{ξ′} = 2 − κ₁
contained in `[2−(κ₉+ε₉), 2−κ₉]`, which contains the canonical
0.8678888651990519355503147104203403132225704976166306446…  (matches to ≥ 56 digits).
**Lean:** `Record9.XiPrimeAtOne` compiles (honest bridge).  Status label
`FINITE_COMPUTATIONAL_RESULT` / `MACHINE_ACCEPTED_PENDING_AUDIT`.

## Literature / provenance (exact sources)
- κ₁(1,v) = 1/c_λ(v;D₁), `cWin`, `jWin`, `vConv`, `D₁` are from the Lean XiPrime snapshot
  (`Zeta23/XiPrime/Defs.lean`), which mirrors [XF′ Thm 8.1/8.2, Lemma 7.1] ("Certified constants").
  The flat/quartic AtOne constants (`kap9Flat`, `kap9Quartic`, `kappaXi_one_*_mem`) are
  formally verified in `Certificate/{Poly,AtOne}.lean` (XIP blue book, the Anthropic-eta paper).
- The MT (cos) profile, ∫v² = a, ∫v⁴ = b, and the profile norms are from
  `reports/admwindow-cos-instance.md` (2026-08-15, mpmath 40 dp).
- The A2-audited κ₁(1,vMT) = 1.132111134800948064449685289579659686777429502383… and
  H_{ξ′}^{MT} = 0.8678888651990519355503147104203403132225704976166306446… are from
  `reports/xi-prime-cor22-derivation.md`, `reports/xi-prime-mt-window.py` (dps=120).

## Blueprint label reconciliation (this run)
The blueprint §1 labels a ↔ ∫v², b ↔ ∫v⁴ are **re-confirmed** by closed form + quadrature:
- a = 1/2 + sin(√2)/(2√2) = ∫cos²(√2·) = **∫vMT²** = 0.84922799931830417992…
- b = 3/8 + sin(√2)/(2√2) + sin(2√2)/(16√2) = **(1/8)∫(3+4cos 2√2s+cos 4√2s) ds** = **∫vMT⁴**
  = 0.73784297545060818785…
Coincidentally ∫cos² and ∫cos⁴ become, after the ½/L normalisation, the same *shape*; the
exact forms are distinct (a differs from b by +1/8 and −sin(2√2)/(16√2)), and both are now
pinned.  (This resolves the "is b = ∫v⁴ or ∫v²?" question raised in the task: b = ∫v⁴.)

## Novelty risk note
No claim of novelty.  This is a formalization/computation-to-proof pass instantiating the
already-established AtOne certificate structure for a new window (the MT/cos profile) whose
exact constants follow from elementary closed forms.  The new content is: the closed-form
vConv for v_MT, the certified J1/κ₉ enclosure, and the Lean honest-bridge theorem.
