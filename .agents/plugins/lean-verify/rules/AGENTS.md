# lean-verify Rules

# Antigravity Mathematical Research Rules

## Epistemic Integrity & Truth Discipline
1. **Never claim completion with open obligations**: A mathematical problem is only marked as FORMALLY_VERIFIED or CANDIDATE_COMPLETE_PROOF when all required proof obligations are fully closed and independently audited.
2. **Distinguish Evidence from Proof**: Numerical simulations, score functions, finite computational checks, and heuristic evidence must be labeled NUMERICAL_EVIDENCE or FINITE_COMPUTATIONAL_RESULT. They must never be promoted to a general theorem without a rigorous proof or certificate.
3. **No Silent Modifications**: Never silently modify definitions, quantifiers, domains, regularity conditions, or boundary assumptions.
4. **Citation & Literature Authenticity**: Every cited paper, theorem, and locator must be verified against authentic sources (DOI, arXiv, zbMATH, MathOverflow). Never fabricate citations or claim a paper proves what it does not.

## Subagent Orchestration & Isolation
1. **Planner-Worker-Verifier Pattern**: Use Antigravity subagents (invoke_subagent) to isolate reasoning. Workers exploring independent proof routes must not observe other workers' reasoning traces or CoT to prevent premature convergence on flawed ideas.
2. **Adversarial Auditing**: Proof verification must be conducted by an independent auditor subagent with fresh context, applying the 14 automated failure checks and first-error taxonomy.

## Artifact & Math Presentation
1. **Interactive Artifacts**: All key outputs (task packets, candidate proofs, research ledgers, whiteboards, verification reports) must be written as Antigravity Markdown Artifacts.
2. **KaTeX Math Formatting**: Render mathematical formulas cleanly using KaTeX display math (\\[ ... \]\ or \$$ ... \) and inline math (\\( ... \)\ or \$ ... $\).
