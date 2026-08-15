# Repro manifest — kernel-limit lemma

Run: `runs/rigorous-open-math-research/R-20260816T040000Z-kernellimit-b9e1`
Status line: `RIGOROUS_PARTIAL_RESULT`

## Environment

- Python: 3.10.11 (`py -3.10`)
- mpmath: 1.3.0
- Windows PowerShell runner; `$env:PYTHONUTF8=1` set for every Python invocation.
- git (project root `F:\LaTeX\Riemann Conjecture`): HEAD `c468881859e63edab8b9ca29bf697ea23fc268e1`;
  dirty: `reports/lean-formalization-contract.md` (modified, pre-existing), plus new run dirs.

## Inputs (sha256)

| artifact | sha256 |
|---|---|
| `Zeta23/Defs.lean` | 20F154CA6F9827D277B2C0CCA999720C67CDC279D672FEC220A073C46A848BFB |
| `Zeta23/ThmD/Functional.lean` | B8E084CA52EF8DEB2CD0FDCC25552B423346ABCB53BAB25543AB757AD66FF945 |
| `Zeta23/ThmD/Window.lean` | 876AC78A279E2F2102AE3057F05D821E60DEC360D47E959D692FE6005CD8ED7F |
| `Zeta23/ThmD/ParamsD.lean` | 0167D985F183C6D221F813636F4EE35BD6F4C339FF9868B9F448B025B49DDBEE |
| `Zeta23/XiPrime/Window.lean` | B459194D353734942A237E09489FD37AA10412FB2845903394A8FA65B2F675EF |
| `zeta-simple-zeros/docs/proof.md` (OpenAI §1) | 834B06811B345A4594231C6458582DDB2D76BFA4EC109ABBF265992408DFA6E2 |
| `lean-proof/Record9/Record9/Chain9.lean` | DF52D984B9C0FB9E03452E329558B36526A2E5895C2BCF24582851FD975EAEA3 |
| `literature/raw/claude-paper-main-v2.txt` (§7) | (source doc read; large, see repo) |

## Outputs (sha256, mirrored in SHA256SUMS)

- `problem_contract.md`, `candidate_proof.md`, `numerical_evidence.md`,
  `research_ledger.md`, `status_and_literature.md`, `counterexample_log.md`,
  `whiteboard.md`, `repro_manifest.md`
- `reproducibility/kernel_limit_verify.py`, `reproducibility/ramp_rate_verify.py`

## Reproduction commands

```
cd runs/rigorous-open-math-research/R-20260816T040000Z-kernellimit-b9e1
$env:PYTHONUTF8=1
py -3.10 reproducibility/kernel_limit_verify.py   # tables A, B, D
py -3.10 reproducibility/ramp_rate_verify.py      # table C (slow, dps=12, maxdegree=20)
```

## Unknowns

- The exact taper profile `ϱ` used in the *numerical* ramp check is a piecewise-linear
  monotone ramp; the snapshot's `TaperProfile` is any $C^3$ taper (only its 0/1 values and
  bounds are used, so the O(w/L) bound is profile-independent). Not a fidelity gap for the
  proof.
- No Lean build was run in this bounded pass (analysis-level only): recorded as not-done.
