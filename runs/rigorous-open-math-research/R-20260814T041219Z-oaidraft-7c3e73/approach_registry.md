# Approach registry — OpenAI draft audit

- **Route 1 — direct adversarial re-derivation (used).** Independently re-derived each lemma/proposition
  of the draft against [1] and Lean. Owner: this solver. State: COMPLETE (all passed).
- **Route 2 — computational reproduction (used).** Run `zeta-zero-verify three|seven`; compare against
  committed certificates (hashes + all counters). State: COMPLETE (exact match for both).
- **Route 3 — constant identity / arithmetic (used).** 60-digit mpmath check of H_MT, c1*, final bound.
  State: COMPLETE.
- **Route 4 — Lean statement cross-check (used).** Compare draft's imported estimates to
  `ThmD.Mult.thmD₀_simple_mult`. State: COMPLETE.

No other routes active. Failed/blocked routes: none (the audited claim holds).

Final: verdict `PASS` / `INDEPENDENTLY_AUDITED_PROOF`.
