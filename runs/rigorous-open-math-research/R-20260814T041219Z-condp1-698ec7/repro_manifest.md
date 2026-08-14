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
| `problem_contract.md` | `EDDEEF09AEACFF67D5A90717DD7B1B51EF302A63207A53AAB752A5F4DA105CE8` |
| `status_and_literature.md` | `71C030649C98999F313148B65B8EA0FEC996FB1C3EE8477CD9142F62317986C3` |
| `obligation_graph.md` | `FC76868465565E5DACAAFCD7E27C522BBD11C1815E89A9D79518728FA2CEEB57` |
| `approach_registry.md` | `772A659F009DA8F09CD132EBDF293FCBA36317AD1C628C9D2B277B4C5D5E7E13` |
| `research_ledger.md` | `DD5A36CC5D483C44C804E56849842E4F9B3B4AEF0097B9C7036A6A023D03F589` |
| `counterexample_log.md` | `7176894ECEB5D3FC84282BB153FB43081621DE4C58923687C2835A032E8B05A8` |
| `candidate_proof.md` | `CD40B471C4A3E9CB85F33EBF0C94000E70E4D43A236765AB8BB58B7DDE0C0DDB` |
| `audit_report.md` | `D6257BCF5085C20F82A2FBD8E5ACEA77A98277F45D6F0708A0385FD977706CC2` (independent adversarial report; untouched) |
| `audit_report.initial-race.md` | `F608FE7BBE70E0ACDD51EEBC4015309146F4135D2C0AFA39F4861EEE379FC26F` (archived earlier self-audit) |
| `repro_manifest.md` | see SHA256SUMS (self-entry is stale-by-design; actual FAD73138...) |
| `SHA256SUMS` | (itself unhashed; self-referential) |
| `reproducibility/verify_moments_christoffel.py` | `5D6A14764651A4FBB94564C618D3A0566E84BB05833BAB868585A07C469138A8` |
| `reproducibility/moments_christoffel_full.py` | `FB8E28FDA823EF197744561AF5F95BB99810B10FF59B8C699A061190F6372B28` |
| `reproducibility/check_lambda2_corrected.py` | `582CA8C5F94ABB9D0278F4A263860ABE81074E6E57F050FDD758B96E1D776DE6` |
| `reproducibility/audit_independent_check.py` | `2EEB5A00BE480B2A064910A763F03FECC2D66628C2520ADB7911071018F59DF2` (auditor-added; untouched) |

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
