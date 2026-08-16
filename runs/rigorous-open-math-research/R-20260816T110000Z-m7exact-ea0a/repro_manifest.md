# Repro Manifest — R-20260816T110000Z-m7exact-ea0a

## 1. Run identity
- **Run ID:** `R-20260816T110000Z-m7exact-ea0a`
- **Task packet ID:** `Q-m7exact-ea0a`
- **Project root:** `F:\LaTeX\Riemann Conjecture`
- **Started:** 2026-08-16T11:00:00Z (approx; timestamps stamped by artifact writes)
- **Skill:** `rigorous-open-math-research` (solver, stage B), bounded exact-computation pass.

## 2. Inputs and authoritative upstream context
| Input | Path | Role |
|---|---|---|
| m6 exact run | `runs/rigorous-open-math-research/R-20260816T060000Z-m6exact-4f9a/` | master_summary6.py, boxspline_exact_fast.py, boxspline_exact.py, boxspline_exact2.py, boxspline2.py, exact_volume.py, reduce_b2.py, per-batch CSVs; m_6 = 640/63, Λ_3 = 247/2519 |
| G2 rule run | `runs/rigorous-open-math-research/R-20260816T070000Z-g2rule-a1b2/` | allJ.json (275 exact rows k=3..6), final_rule.py, graph_rule.py, dataset.py |
| G2 proof run | `runs/rigorous-open-math-research/R-20260816T080000Z-g2proof-a24d/` | verify_k7.py, verify_k7_fast.py (exact per-π box-spline engines for k=7) |
| Authoritative exact values | problem_contract §4 | m_1..m_6, Λ_1..Λ_3, G2 rule, c_{2n} |

The G2 rule (J_σ=0 ⟺ H_σ disconnected OR m ≤ 2b−3; nonzero ⟺ connected AND m ≥ 2b−2)
was **not re-derived** in this pass; it is taken as the authoritative verified rule from
the context (100% on 275 exact rows k=3..6) and used only to **prune** the partition set.
The survival count is verified directly from the enumeration here (a reproducibility check,
not a new proof of the rule).

## 3. Environment
- OS: Windows; interpreter **`py -3.10`**; `$env:PYTHONUTF8=1`.
- Packages: numpy 2.2.6, scipy 1.15.3, sympy 1.13.1, mpmath 1.3.0, python-flint (available).
- No networkx used.

## 4. Methods / engines (copied byte-identical from upstream, then used as-is)
| File (in reproducibility/) | Origin | Purpose |
|---|---|---|
| `boxspline_exact.py` | m6exact | cycle_edges, rho_terms, perm_edges (edge-vector setup for the det rho expansion) |
| `boxspline_exact2.py` | m6exact | **AUDIT-GRADE exact** box-spline value at 0 (`coarea_value_exact`, exact rational vertices) |
| `boxspline_exact_fast.py` | m6exact | fast exact-vertex box-spline (`eq_coarea_value_exact_fast`) |
| `boxspline2.py` | m6exact | float box-spline engine (`coarea_value`) |
| `exact_volume.py` | m6exact | upstream exact-volume helper |
| `dataset.py` | g2rule | partition enumeration, cycle_multigraph, crossing_count, profile, exact c-values |
| `allJ.json` | g2rule | 275-row exact dataset (validation context) |
| `verify_k7.py`, `verify_k7_fast.py` | g2proof | upstream k=7 verification probes (context/reference) |

### New scripts (this run)
| File | Purpose |
|---|---|
| `prune_k7.py` | enumerate 877 k=7 partitions, apply G2 rule, save `k7_survivors.json` |
| `prune_k8.py` | same for k=8 (4140 partitions), save `k8_survivors.json` |
| `compute_k7_exact.py` | group 540 survivors into 18 H-isoclasses; compute exact J per isoclass (b=1,2 closed form; b=3,4 exact+fast box-spline with cross-check + rational recon); sum m_7; writes `k7_iso_results.json` and `k7_allJ.json` |
| `compute_k8_partial.py` | exact b≤2 contribution to m_8 (closed form) |

## 5. Canonical J-value identity used
`J_σ` depends only on `(b, H_σ)` (the cycle-crossing multigraph) — the integral's integrand
and domain depend only on the block-crossing pattern and b, not on the labelling. Hence the
540 (resp. 2683) G2-surviving partitions collapse to 18 (resp. 46) distinct H-isoclasses,
each sharing a single J value. This is the core computational reduction; it is checked
directly by canonicalizing `H_σ` under block relabelings.

## 6. Determinism / hashes
SHA256 of every artifact in this run is recorded in `SHA256SUMS`. Input upstream scripts are
copied byte-identical (verified against upstream SHA256SUMS where available) and not edited.

## 7. Unknowns / limitations
- The G2 vanishing rule is used as given (upstream-verified), not re-proved here.
- Full m_8 (b=3,4,5 blocks) is reported as **open** if not completed within budget; only the
  exact b≤2 part is claimed as rigorous unless stated otherwise.
- Λ_4 needs m_8 if the requisite Hankel determinant requires moments beyond m_7; the exact
  size check is recorded in `candidate_proof.md`.
