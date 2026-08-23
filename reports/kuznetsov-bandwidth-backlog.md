# Kuznetsov Bandwidth Extension — Long-Term Research Backlog

Status: **BACKLOG / RESEARCH IDEA — NOT VERIFIED**  
Date: 2026-08-23  
Retained for future use. Do not report any constant from this route as an
unconditional theorem unless a full analytic proof is completed.

## 1. Idea

Extend the admissible bandwidth beyond the current barrier

\[
\lambda \le 1
\]

in the rank-trace / pair-correlation method by using the Petersson–Kuznetsov
trace formula and automorphic spectral methods to control off-diagonal terms
that otherwise require unproven prime-pair information.

If this were achieved, the new bandwidth would live beyond the current
Bandwidth-1 ceiling, which is approximately

\[
0.6818287\ldots
\]

and could potentially give a substantially larger unconditional simple-zero
proportion on the critical line.

## 2. Why it is hard

The Anthropic paper
(`literature/raw/claude-paper-main-v2.txt`, §7.5) states that:

- The restriction \(\lambda \le 1\) comes from the off-diagonal terms in the
  prime-side evaluation;
- For \(X \gg T^{\lambda}\), those terms are no longer dominated by the
  diagonal;
- Evaluating them requires Hardy–Littlewood-type prime correlation
  asymptotics, or equivalently Montgomery's pair-correlation conjecture beyond
  \(\alpha > 1\).

Therefore this is a genuine mathematical frontier, not a substitution into a
formula.

## 3. Required technical ingredients (future work)

1. A rigorous unconditionally proven estimate for the relevant shifted
   prime-correlation / Kloosterman sums in the needed range.
2. A verified transfer from such an estimate to the trace/quadratic form used
   by the rank-trace certificates.
3. A derivation of the new proportion constant at the resulting bandwidth.
4. Independent verification and, eventually, Lean formalization.

## 4. Existing artifacts

- `reports/novel_technical_routes_riemann.md` — original route proposal
  (now marked as future-work backlog).
- `reports/future-work-roadmap.md` — active roadmap; Kuznetsov listed as
  long-term backlog.
- `lean-proof/Record9/archive-nonverified/` — archived Lean files; no
  verified theorem is claimed for this route.

## 5. Do / don't

- **Do** keep this as a long-term research target.
- **Don't** treat the 70.83% number in the old route report as a verified
  result.
- **Don't** start a full Lean formalization until the analytic estimates are
  established.
