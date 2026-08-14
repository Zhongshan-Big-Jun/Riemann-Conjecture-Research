# Repro Manifest [FINAL] — R-20260814T041219Z-condp1-698ec7

Runner: delegated solver subagent (rigorous-open-math-research skill). Scope: danger-full-access;
approval prompts disabled; no sandbox escalation requested. Python 3.10.11 + numpy + scipy + fractions.

## Inputs

| Item | Path | sha256 / identifier |
|---|---|---|
| Task packet | `agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md` | id Q-20260814-criticalline-p1-507bb5 |
| Claude v2 PDF | `literature/raw/claude-paper-main-v2-20260813.pdf` | `6792988E6CD0E17690621CE898ABD5D534F98407741BC7CB14BBE7D07C77D72F` |
| Claude v2 TXT | `literature/raw/claude-paper-main-v2.txt` | `9B02E53C31D7926CF584BEC2BADE8FEACFE17633EE9D4705521EB6D47D902432` (§7.1 Thm D 1400–1427; §7.2(b)–(f) 1602–1658; Prop 4.4/4.5 703–804; Lemma 3.2/3.3 513–556; units (4.4) 590–600) |
| Claude note TXT | `literature/raw/claude-paper-note.txt` | `69BDFCE6E53F691D965F3C4D4AAA1536B2BEA3DEBCD68E3BAA25DDA142ACD984` (Lemma 3.3 HS-norm, Lemma 3.4 rank-trace) |
| GS 2025 TXT | `literature/raw/gs-2511.20059.txt` | `65A87EA32D6C2CB70DC3EC39E9304DFA79F73805C6E30EDBFD52ED3F749BC3F0` (Theorem 5) |
| Lean snapshot | `literature/raw/zeta-23-lean/` | commit `3635e74826a4c1fcece7d1cd2b6fa75e43a00510`; `Zeta23/ThmD/Final.lean` (thmD₀ / thmD₀_simple), `Endgame.lean`, `Mult.lean` (Thm D). Read-only this run; no build performed. |
| GLSS25 | arXiv:2503.15449 | statement via GS Theorem 5 (primary PDF not bundled; primary-source check is open item O7 in packet) |
| Frontier map | `literature/maps/FRONTIER.md` | `6145A358969439BC118F48FE283C0C1C70F11BBD980D027E152B62BC1C3A9098` |

## Tooling / environment

- OS: Windows (PowerShell); `py -3` → Python 3.10.11; numpy, scipy (unitary_group), fractions.
- Commands: `py -3 <script>` run from the run root. No Lean build, no SDP solver used.

## Outputs (all under the run root)

| Artifact | sha256 |
|---|---|
| `problem_contract.md` | `EB0DD131D778871A5AA2112E257B7E0E1A6D68DD8DAB75CABE2A05108DDAF560` |
| `status_and_literature.md` | `FA12749DBF23B8A2E1B414D445C760F57D98BA9ECA15830E2A8E3C637F0B16FA` |
| `obligation_graph.md` | `6772A3BE99A9CB355A2730A5164FBFDB828DAB7F59ED3B873C36075AD8E9DFA4` |
| `approach_registry.md` | `772A659F009DA8F09CD132EBDF293FCBA36317AD1C628C9D2B277B4C5D5E7E13` |
| `research_ledger.md` | `82F45F88AB417488D8C5B3B39EA671A81DC4D9BB8F421D900ABF38BF77ADE2C5` |
| `counterexample_log.md` | `7176894ECEB5D3FC84282BB153FB43081621DE4C58923687C2835A032E8B05A8` |
| `candidate_proof.md` | `65C3E80F94E9CBE37F8C102FC09ABC6C90D53DA59EA43E5E271E8D5ED884B2BE` |
| `audit_report.md` | `F608FE7BBE70E0ACDD51EEBC4015309146F4135D2C0AFA39F4861EEE379FC26F` |
| `repro_manifest.md` | `E8223028C7BD5003DEF26E153BE095C6C0501C601CC9F51E4F5FE0893086EB05` |
| `SHA256SUMS` | (itself unhashed; self-referential) |
| `reproducibility/verify_moments_christoffel.py` | `5D6A14764651A4FBB94564C618D3A0566E84BB05833BAB868585A07C469138A8` |
| `reproducibility/moments_christoffel_full.py` | `FB8E28FDA823EF197744561AF5F95BB99810B10FF59B8C699A061190F6372B28` |
| `reproducibility/check_lambda2_corrected.py` | `582CA8C5F94ABB9D0278F4A263860ABE81074E6E57F050FDD758B96E1D776DE6` |

## Computation provenance (exact vs numerical)

- **Exact (proof-grade):** m_2 = 4/3 (Lemma C derivation, ∫sinc²=1, ∫sinc⁴=2/3, DPP 2-point
  intensity). Λ_2(0) = 5/36 for the corrected list (1,4/3,2,13/4); 1−Λ_2(0)=31/36;
  13/18 = 2·(31/36)−1. Inconsistency: 2×2 Hankel det = −1/4 < 0 for (1,3/4,...). All rational.
- **Numerical only (evidence, never proof):** CUE Monte-Carlo moments m_1≈1.0, m_2≈1.3355,
  m_3≈2.006, m_4≈3.264 (N=200, trials=200, seed=7). Used only to corroborate the corrected
  moment list; no theorem depends on it.
- The spectral lemma **SL** is an assumption (not asserted), proved nowhere in this run; it is the
  precise open/in-later-work ingredient.

## Unknowns / limitations

- GLSS25 primary source not bundled; reconciliation records the GS Theorem 5 quoted statement and
  marks primary-source verification as an open item (packet O7).
- OpenAI draft constant belongs to companion run R-…-oaidraft-7c3e73 (packet O2/O3); not re-audited here.
- No Lean build/run performed; the Lean snapshot was used read-only for statement fidelity.
- Numerical moments (D) carry finite-N/O(1/N) bias; exact closed forms for m_3,m_4 are not
  needed by the theorems and are left open.
