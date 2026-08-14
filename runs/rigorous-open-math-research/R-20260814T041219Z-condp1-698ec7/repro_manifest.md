# Repro Manifest — R-20260814T041219Z-condp1-698ec7

Runner: delegated solver subagent (rigorous-open-math-research skill). Permission scope: danger-full-access, approval prompts disabled (no escalation).

## Environment
- Host OS: Windows (PowerShell). Python availability: to be checked (used for finite verifications only).
- Skill: `rigorous-open-math-research` (loaded), references under `C:\Users\HuangZY\.dsh\skills\rigorous-open-math-research`.

## Inputs (paths + identifiers)
| Item | Path | Identifier |
|---|---|---|
| Task packet | `agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md` | id Q-20260814-criticalline-p1-507bb5 |
| Claude v2 text | `literature/raw/claude-paper-main-v2.txt` | §7.2(d)(e)(f) lines 1628–1658; Thm D 1400–1427; Prop 4.4/4.5 703–804; Lem 3.2/3.3 503–556 |
| Claude v2 PDF | `literature/raw/claude-paper-main-v2-20260813.pdf` | sha256 6792988E6CD0E17690621CE898ABD5D534F98407741BC7CB14BBE7D07C77D72F |
| Lean snapshot | `literature/raw/zeta-23-lean/` | commit 3635e74826a4c1fcece7d1cd2b6fa75e43a00510; Lean v4.33.0-rc2, Mathlib 51e6992 |
| GLSS25 | arXiv:2503.15449 (statement via `gs-2511.20059.txt`) | GS Theorem 5 / GLSS25a |
| GS 2025 PDF+TXT | `literature/raw/gs-2511.20059.{pdf,txt}` | sha256 7B4F638C…3ED4C6F |
| Frontier map | `literature/maps/FRONTIER.md` | sha256 6145A358969439BC118F48FE283C0C1C70F11BBD980D027E152B62BC1C3A9098 |

## Run root
`F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260814T041219Z-condp1-698ec7`

## Tools
- read/edit/write/pwsh/glob/grep on the project tree.
- Python for finite verification (exact rational / high-precision float / SDP via cvxpy if available).
- No Lean build performed this run (snapshot read-only; formalization is a candidate prepared for a later stage-C `lean-verify` run, not executed here unless toolchain is already present).

## Unknowns / limitations
- Whether Python + cvxpy (or mpmath) are installed on this host: to be checked. If absent, finite checks fall back to exact rational arithmetic or are deferred as open items.
- GLSS25/GS Theorem 5 is quoted from the GS September-2025 arXiv (2511.20059) which itself cites the GLSS preprint; the primary 2503.15449 PDF is not in the bundle, so the reconciliation records the exact quoted statement and marks the primary-source check as an open item for O7.
- No independent audit of the OpenAI draft constant is performed in this run (companion run R-…-oaidraft-7c3e73 owns O2).
- Hash binding: all artifact hashes are recorded at the end in audit_report.md / a SHA256SUMS file under reproducibility/.
