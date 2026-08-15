# Numerical evidence — T1c-1 / T1c-2 stability-bridge (evidence, not proof)

Run: `R-20260816T060000Z-stabridge-a3f1`. All checks deterministic, seeded, mpmath 40-digit.

## `reproducibility/stabridge_checks.py` (15 checks, all PASS)
| # | check | result |
|---|---|---|
| C1 | Ψ continuity (t=0,2), Ψ≥0 | PASS (Ψ(0)=1, Ψ(2)=1) |
| C2 | `min_n[(p−n)²+4n] = 2p−1+Ψ(p)` | PASS (worst 1.1e-16) |
| C3 | Lemma 2.1 `‖P+Q‖²≥4tr(P+Q)−3r−4b+trΨ(M)`, random (d,r,b) | PASS (zero violation) |
| C4 | defect lemma `tr Ψ(G) ≥ min(1,2Σ\|G_ij\|²)`, random PSD | PASS (zero violation) |
| C5 | exact constants A₀/m, (m−1)/(500m), cLHS, A₀<1 | PASS |
| C6 | window-count ≤ 2/pair, ≤ 1/500/gap | PASS |
| C7 | corr-Gram energy `2Σ\|G_ij\|²/E_m → 1` (L=100/400/1000) | PASS (1.046, 1.011, 1.004) |
| C8 | `min{1,·}` branch on A₀<1 | PASS |

## `reproducibility/stabridge_sublemma.py` (6 checks, all PASS)
| # | check | result |
|---|---|---|
| T1c2a | `E_m+(1/500)span ≥ A₀` from window-summed F₈≥f₉ | PASS |
| T1c2c | offset-averaging coeff (m−1)/(500m) | PASS (0.001992) |
| T1c2c | A₀/m = 2499/657500 | PASS |

## Interpretation
These are **spot-checks**, never proof. C3/C4 instantiate the exact real-number inequalities
on concrete random inputs; C7/C2/C5 verify the analytic identities the proofs rely on. The
key negative result is the hat-unit counter-candidate (see `counterexample_log.md` §1): the
hat-unit Gram does NOT reproduce `Σ\|G_ij\|²=(1/2)E_m` and would make Cor 2.2 false, forcing
the unit-normalized (correlation) convention for Δ(M°).
