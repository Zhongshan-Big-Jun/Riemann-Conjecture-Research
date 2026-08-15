# Repro manifest — T1c-1 / T1c-2 stability-bridge statements (Stage C)

Run: `runs/rigorous-open-math-research/R-20260816T060000Z-stabridge-a3f1`
Status line: `RIGOROUS_PARTIAL_RESULT`

## Environment
- Python: 3.10.11 (`py -3.10`); numpy 2.2.6; mpmath 1.3.0.
- Windows PowerShell runner; `$env:PYTHONUTF8=1` set on every Python invocation.
- git (project root `F:\LaTeX\Riemann Conjecture`): HEAD `a9d485062d314ba1f07673fd6c9f53589f4efe47`;
  dirty: two new untracked run dirs (`R-…-stabridge-a3f1`, a prerelease `R-…-m6exact-4f9a`).

## Inputs (sha256)
| artifact | sha256 |
|---|---|
| `Zeta23/Defs.lean` | 20F154CA6F9827D277B2C0CCA999720C67CDC279D672FEC220A073C46A848BFB |
| `Zeta23/ThmD/Functional.lean` | B8E084CA52EF8DEB2CD0FDCC25552B423346ABCB53BAB25543AB757AD66FF945 |
| `Zeta23/ThmD/AssemblyD.lean` | 33D8BB75A05B711FEC70805C8EAB0EF3FCC2674E691304E3B13654E69A6AAD07 |
| `Zeta23/ThmD/Mult.lean` | 35ACEA86CCE62640DA5445EEE04FDE0741FC9968188FB90978AA09BDF9865E9B |
| `Zeta23/ZeroSide/Mult.lean` | A332B53F8B20F901C6A4A6B3A336441EA3B2900B2BCF650D1292C7DAB19874F3 |
| `Zeta23/ZeroSide/RankTraceMult.lean` | 1D6D6FD24738F68A121700A79664C4CE651C6D6C84F8C7795C63CDD2181241A8 |
| `Zeta23/LinAlg/RankTrace.lean` | 42354C9A0E2633015F9363B9C97F678FFC363EA35954F3FF04FC743187907020 |
| `Zeta23/LinAlg/HermitianPosPart.lean` | 954AC8D9224E094E15EA3A7902D5923DC9BBAF847FAC03C6A67FBE21CD1D50CA |
| `Zeta23/LinAlg/PosIndex.lean` | B327580D04BD563F3DEB705CCDBFA1C5DACF4BFFA9B2E337F07950574143CE4E |
| `Zeta23/LinAlg/VonNeumann.lean` | A433D16DE0DB84DFCBDAA3684CFE62DF7D06AE9A3B068E546F132D5B75A87780 |
| `Zeta23/LinAlg/Sylvester.lean` | A26F801A4C376AD3238EDDF47B3B2920AFDE26D8B8FE9366C432652DEA5475A6 |
| `zeta-simple-zeros/docs/proof.md` (OpenAI) | 834B06811B345A4594231C6458582DDB2D76BFA4EC109ABBF265992408DFA6E2 |
| `lean-proof/Record9/Record9/Chain9.lean` | DF52D984B9C0FB9E03452E329558B36526A2E5895C2BCF24582851FD975EAEA3 |

## Outputs (sha256 in `SHA256SUMS`; mirrored here)
`problem_contract.md`, `candidate_proof.md`, `research_ledger.md`, `whiteboard.md`,
`counterexample_log.md`, `status_and_literature.md`, `repro_manifest.md`,
`reproducibility/stabridge_checks.py`, `reproducibility/stabridge_sublemma.py`,
`reproducibility/check_run.log`, `reproducibility/sublemma_run.log`.

## Reproduction commands
```
cd runs/rigorous-open-math-research/R-20260816T060000Z-stabridge-a3f1
$env:PYTHONUTF8=1
py -3.10 reproducibility/stabridge_checks.py    # 15 checks (Lemma 2.1, defect lemma, constants, kernel-ratio)
py -3.10 reproducibility/stabridge_sublemma.py  # 6 checks (block energy, offset coeffs, A0/m)
```
All 21 checks PASS; logs under `reproducibility/*.log`.

## Unknowns / not-done
- Lean formalization of T1c-1/T1c-2 and the sub-lemmas: NOT done in this bounded pass
  (analysis-level only; follow-up lean-verify).
- The T2 certificate `F₈ ≥ 392/100000` is an INPUT to T1c-2a, not verified here.
- The precise snapshot notion of the *retained-simple-zeros* Gram at the unit-normalized
  scale is not a single `def` in the snapshot today; ambiguity documented (candidate_proof §7);
  `Gsummand`/`Gentry` (Defs.lean) give the Gram entries, the unit-ratio `⟨v_a,v_b⟩/‖v‖²` is
  the intended object.
