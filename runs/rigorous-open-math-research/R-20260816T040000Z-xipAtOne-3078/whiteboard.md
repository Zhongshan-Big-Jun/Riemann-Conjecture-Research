# Whiteboard — R-20260816T040000Z-xipAtOne-3078 (AtOne κ₁(1,vMT) certificate)

- **Run ID:** `R-20260816T040000Z-xipAtOne-3078`
- **Task packet ID:** `Q-20260814-criticalline-p1-507bb5`
- **Last updated:** `2026-08-16T04:10:00Z`

## Current plan

RUN COMPLETE (2026-08-16): FINITE_COMPUTATIONAL_RESULT (math) + MACHINE_ACCEPTED_PENDING_AUDIT
(Lean module `Record9.XiPrimeAtOne`). Deliverable: the certified AtOne sandwich for the ξ′
MT-window constant:
  κ₉ ≤ κ₁(1, vMT) ≤ κ₉ + ε₉,
  κ₉ = (aMT + J1)/(∫vMT)² = 1.132111133800997 ± 2e-16,  ε₉ = 1024/2990212875,
  canonical κ₁ = 1.132111134800948064449685289579659686777429502383… ∈ sandwich ✓,
  H_xip = 2 − κ₁ = 0.8678888651990519355503147104203403132225704976166306446… ∈ [2−(κ₉+ε₉), 2−κ₉] ✓.
Flow: D1trunc9 ≤ D₁ ≤ D1trunc9 + ε₉ (formally verified tail) × vConv ≥ 0 → J1 ≤ jWin ≤ J1 + ε₉(∫v)² →
the κ sandwich. Next steps (not part of this run): promote the closed-form/Fubini facts from
hypotheses to real Lean lemmas (M3-open-A formal); then the xiChain bridge (M3-open-B).

## Route history

- Exact closed forms `[SUCCEEDED]`: ∫vMT = √2·sin(1/√2) = 0.91872536986556843778…, aMT =
  1/2 + sin√2/(2√2) = 0.84922799931830417992…, bMT = 0.73784297545060818785…,
  vConv vMT r = ½(1−r)cos(√2r) + sin(√2(1−r))/(2√2) ≥ 0 on [0,1]; 2∫₀¹vConv = (∫vMT)² =
  0.84405630523462552655… (= 1 − cos √2).
- Rigorous J1 sandwich `[SUCCEEDED]`: J1 = 2∫₀¹ D1trunc9·vConv = 0.10633754139274846 ± 1.8e-16
  (ARB + composite Simpson with a rigorous global M₄ bound); full jWin(D₁,1,vMT) ∈
  [0.10633754…, 0.10633783…] contains the canonical value.
- ε₉ tail `[SUCCEEDED]`: ε₉ = 1024/2990212875 (formally verified D₁ tail; D₁trunc index 9).
- Independent cross-check `[SUCCEEDED]`: audit_kappa.py (mpmath, |H − canonical| ≈ 1.4e-56);
  contain-checks True.
- Lean module `[SUCCEEDED]` (machine-accepted): `Record9.XiPrimeAtOne` declares
  IvMT/aMT/bMT/vConvMTcl/J1MT/kappaXiOne_MT, `kappaXi_one_vMT_mem` (κ₁(1,vMT) ∈ Icc κ₉ (κ₉+ε₉)),
  `H_xip_vMT_mem`; `lake build Record9.XiPrimeAtOne` exit 0 (8846 jobs, manager re-verified);
  axioms base-only; no sorry/admit/axiom.
- Honest-findings `[SUCCEEDED]`: κ₉ is NOT an exact rational for v_MT (real constant enclosed to
  ~1e-16 ≪ ε₉) — unlike the flat/quartic AtOne; transcription typo (∫vMT value) in
  FORMALIZATION_STATUS_XIP.md corrected; F1–F5 implementation defects caught and recorded
  (all in the code path, not the math).
- Formal Lean promotion of the analytic facts `[BLOCKED — budget]`: closed-form/Fubini facts
  currently explicit axiom-free hypotheses.

## Ideas to return to

- Exact-0 of vConv ≥ 0 and Fubini 2∫₀¹vConv = (∫v)² as self-contained Lean lemmas (elementary
  product-to-sum + interval integral).
- The analogous AtOne certificate for the ξ′ quartic window (already in the snapshot:
  AtOne.lean convQ) — no work needed; only the MT instance was missing.

## Open obligations

- M3-open-A formal (Lean): promote (a) ∫vMT = IvMT, ∫vMT² = aMT; (b) vConv vMT = vConvMTcl;
  (c) Fubini 2∫₀¹vConv = (∫vMT)²; (d) 0 < IvMT; (e) jWin(D1trunc9,1,vMT) = J1MT + D₁-cert
  sandwich mechanics — from hypotheses to real lemmas.
- M3-open-B: the ξ′ chain xiChain (pressure-method/stability) — unchanged.
- M1-open-C: the four §1 profile L¹-norms as Lean lemmas — unchanged.

## Key artifacts

- `runs/.../xipAtOne-3078/candidate_proof.md` + `run_report.md` — sandwich derivation + machine evidence.
- `runs/.../xipAtOne-3078/reproducibility/atone_xip_mt.py` — rigorous ARB certificate;
  `audit_kappa.py` — independent mpmath cross-check; `atone_cert.txt`, `audit_kappa_out.txt`,
  `README.md` — captured outputs.
- `lean-proof/Record9/Record9/XiPrimeAtOne.lean` — the Lean module (machine-accepted).
- `lean-proof/Record9/FORMALIZATION_STATUS_XIP.md` — M3-open-A row updated.
- `runs/.../xipAtOne-3078/SHA256SUMS` — hash-bound artifacts.
