# k-family pressure-ladder feasibility — consolidated assessment (2026-08-15)

Updates and supersedes parts of `reports/k11-feasibility.md` (2026-08-14) with the k=10
scoping data (2026-08-15) and the k=9 ladder reality after the f₉ = 0.00392 certification.

## The data (all evidence-level unless certified)

| k | variables | true-min estimate (evidence) | certified | margin vs verifier bound loss (~1e-5) |
|---|---|---|---|---|
| 9 | 8 | ≈ 0.003950049001339790 (exact-kernel, box minimization 2026-08-15) | **0.00392 (CERTIFIED, grid-2000, 64.7M nodes)** | 1.14e-5 (g2000) ✓ / 3.0e-5 (vs true min) |
| 10 | 9 | **≤ 0.003958082831 (scoping, 631,200 evals, all starts → same basin; scoping_k10.py)** | none | — |
| 11 | 10 | ≈ 0.00405 (scoping 2026-08-14, k11_opt.npy) | none | — |

The k=9 "true min 0.0039818" from the extpress scoping was a LOCAL minimum (CORRECTED
2026-08-15: true min ≈ 0.00395005). Lesson recorded: scoping gives upper bounds only;
certification is the only rigorous statement.

## What the k-family ladder can still give (mpmath 40d, 2026-08-15)

Record constant (certified): C₉(0.00392) = 0.673066472675939665848…

| attempt | n | m | A₀<1 | C (k=10) | gain vs record | margin vs scoped inf 0.00395808 | verdict |
|---|---|---|---|---|---|---|---|
| k=10, f=0.00395 | 253 | 262 | 0.99935 ✓ | 0.67307565848593040355 | +9.2e-6 | 8.1e-6 (< 1e-5) | INFEASIBLE (margin below bound loss) |
| k=10, f=0.00394 | 253 | 262 | 0.99682 ✓ | 0.67306913411555311771 | +2.7e-6 | 1.8e-5 | borderline, but 10–50× k=9 cost (1–5 days) for +2.7e-6 — poor value; NOT recommended |
| k=10, f=0.00393 | 254 | 263 | 0.99822 ✓ | 0.67306292754074137522 | **−3.5e-6 (below record!)** | 2.8e-5 | moot (k=10 with m=263 is worse than k=9 with m=262 at the same f) |

k=9, f=0.00393 (grid-4000): C₉ = 0.673072744423451254556223736062, gain +6.3e-6,
margin vs g4000 leaf bound 1.017e-5 ≈ bound loss → **the last borderline k=9 step**; cost
1–2 days (see f9-ladder.md "0.00393/0.00394 premium assessment").

## Conclusions

1. **The pressure-certificate class is practically exhausted at the certified C₉ = 0.6730665**
   (k=9, f=0.00392). The formal class limit (uncontrolled large-m spectral monotonicity) at the
   true minimum would be ≈ 0.6731597 (f ≈ 0.00395005), but certifying AT the true minimum is
   impossible with the current interval machinery (intrinsic quadratic-dip loss ≈ 3.5e-6 +
   table bound loss ≈ 1e-5 vs margin 0).
2. The only remaining same-class steps: k=9 @ 0.00393 grid-4000 (borderline, +6.3e-6, 1–2 days);
   k=10 @ 0.00394 (poor value, +2.7e-6, 1–5 days). k=11 infeasible (2026-08-14 analysis stands).
3. A recovered-gain route exists in principle: an EXACT-arithmetic certifier (the Stage C T2
   reflection/verified-verifier route) removes the interval rounding loss; the intrinsic dip
   loss would still cap f at ≈ true_min − 3.5e-6 ≈ 0.0039465 → C₉ ≈ 0.673082 (+1.5e-5), i.e.
   the exact route is worth ≈ +1.5e-5 beyond the current record IF the dip-loss bounding is
   also improved (convexity-based span bounds). This is a substantial engineering project tied
   to the Stage C T2 formalization; not scheduled on its own.
4. **Roadmap implication:** further record gains on the unconditional side need either (a) the
   exact-certifier route (≈ +1.5e-5, heavy), (b) new mechanisms beyond the k-family pressure
   class (bandwidth-one ceiling 0.6818 is the theoretical frontier of the whole rank–trace +
   window certificate framework; the OpenAI class ceiling ≈ 0.6730583/0.6731394 has been
   exceeded — we are now beyond the original class limit via the certified 0.00392), or
   (c) the conditional route (HL* + SL ⇒ 100%) — the SL lemma is the single open ingredient and
   carries the far larger payoff.

## Reproducibility

- scoping_k10.py: runs/rigorous-open-math-research/R-20260814T131528Z-f9push-d3b58c/reproducibility/
  (seeds from the k=9 certified-minimum basin + k=9/k=7 scoping configs + 1500 random starts;
  L-BFGS-B, ftol 1e-14, maxiter 2000; log scoping_k10.log: best 0.003958082831 at nfev 631,200).
- Constants: mpmath 40d, exact rational chain C_k(f) = (H − (m−1)/(500m))/(1 − f·n/m),
  n = ⌈1/f⌉−1, m = (k−1)+n.
- All values evidence-only (scoping/minimization), never proof.
