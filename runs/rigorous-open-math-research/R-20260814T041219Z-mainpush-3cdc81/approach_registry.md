# Approach Registry

Run: `R-20260814T041219Z-mainpush-3cdc81`. Route families, owners, states, exact gaps.

| # | Route | Owner | State | Exact gap / blocker |
|---|---|---|---|---|
| A | Verify OpenAI/GPT-5.6 draft (O2): certificates + reduction chain | solver | VERIFIED (this run) | Chain not Lean-formalized end-to-end; only the 2 certificates are machine-checked |
| B | Improve OpenAI class: longer blocks / better Ψ / windows (O3) | solver | ANALYZED | Class ceiling ≈ 0.673058 (m→∞); 0.6730085 rigorous at m=269; needs large-block spectral control to go beyond; better Ψ impossible within Lemma 2.1; k≥2 moments blocked |
| C | Probability-1: unconditional proof (O4) | solver | BLOCKED (obstruction) | lower-bound-only cert classes cap < 0.69 (ghost invariance, k=1 barrier, Prop 7.4) |
| D | Probability-1: reduction to named conjecture (O4) | solver | REDUCED | PCC (ES) ⟹ 1, verified ([GLSS25] + [GS25]) |
| E | Conditional HL* route (O5) | solver | PARTIAL | internal arithmetic OK; moment sequence m_k(1) not reproducible (informal) |
| F | Numerical corroboration (O6) | solver | EVIDENCE | cannot detect off-line zeros; never proof |
| G | Literature integrity (O7) | solver | DONE (1 gap) | CCLM17 unresolved |

## Remarks
- Data flow: Claude Thm D (Lean-verified) provides H_MT baseline → OpenAI adds D(M) defect +
  7-point pressure → verified here. Independence: I re-derived every step; certificates re-run
  from source (not trusting committed logs, per repo's own verifier.md trust note).
- The strongest rigorous outcome is route A (verified draft) + route D (reduction) + route B
  ceiling computation (novel).
