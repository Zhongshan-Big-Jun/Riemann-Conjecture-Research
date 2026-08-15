# papers — human-readable proofs of Lean-verified theorems

Per the project-repository spec (manage-math-research-program,
references/project-repository-spec.md §"File ownership", workflow 8c), this workspace holds
human-readable LaTeX proofs of theorems that have passed machine verification (Lean 4,
`lean-proof/`), each bound to its machine verification record.

## Convention

```
papers/<SLUG>/
    <SLUG>-en.tex   arXiv-style human-readable proof, English
    <SLUG>-zh.tex   Chinese companion, same statement/proof structure
    <SLUG>-en.pdf   compiled, when a toolchain is available
    build/          intermediate LaTeX artifacts
```

Every `<SLUG>-en.tex` / `<SLUG>-zh.tex` header carries the formalization contract: the Lean
paths (e.g. `lean-proof/Record9/Record9/Chain9.lean`), the verification commit hash, the
zero-sorry/axiom statement, and the machine evidence reference
(`lean-proof/lean-audit-report.md`, `lean-proof/verification.json`).

## Status (2026-08-16)

- No paper drafted yet. Candidates when the corresponding obligations close:
  - `record-c9` — the certified world record
    C₉(ζ) = (657,500·H_MT − 1,310)/655,001 = 0.673066472675939665848… (ζ, N₀ˢ/N) and
    C₉(ξ′) = 0.86920009109661916184… (ξ′, N₀ˢ_{ξ′}/N_{ξ′}); Stage C: O1 FORMALLY_VERIFIED,
    T1 (chain9_eps + record_c9) MACHINE_ACCEPTED_PENDING_AUDIT (open analytic bridges:
    kernel-limit lemma, stability/block-defect; T2 certificate; T3 ξ′).
  - `sl-conditional-100` — the conditional theorem HL*+SL ⇒ proportion 1 (condp1 run,
    audited); SL remains open (moment route in progress).
