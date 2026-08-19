# Research ledger — Zenodo 22008814 audit

- 2026-08-17T01:05Z: run created; PDF downloaded + hashed; text extracted (72 pp).
- 2026-08-17T01:10Z: dispatched adversarial audit subagent (517141b8) for §1–§15.
- 2026-08-17T01:10Z: dispatched Lean subagent (4c070e46) to formalize eq-(4) curvature identity and the conjugate-pair block negative-eigenvalue statement in `Record9.ZenodoAudit`.
- 2026-08-17 (audit settle): adversarial audit subagent returned; overall verdict **NOT ESTABLISHED**; O1/O8 FAILED, O15 GAP, O9 GAP, O18 GAP conditional.
- 2026-08-17 (Lean settle): `Record9.ZenodoAudit` compiles (`lake build` exit 0, 3076/3077 jobs) proving `curvature_identity`, `conjugate_pair_block_charpoly`, `conjugate_pair_block_has_negative_eigenvalue`; `#print axioms` = `{propext, Classical.choice, Quot.sound}`.
- 2026-08-17: analysis report `reports/zenodo-22008814-analysis.md` written.
