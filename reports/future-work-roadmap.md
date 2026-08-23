# Future-Work Roadmap — k-point pressure certificates and long-term research backlog

Date: 2026-08-23  
Owner: project research pipeline  
Status: ACTIVE PLAN — not a claim of verified mathematical results.

## Decision

- **Primary near-term direction:** continue advancing the k-point pressure-certificate family.
- **Preserve for future use:** the Petersson–Kuznetsov bandwidth-extension idea (Route 1).
- Other archived "novel route" Lean modules are not treated as verified results; see
  `lean-proof/Record9/archive-nonverified/README.md`.

---

## 1. Active work: k-point pressure certificates

### Current status (2026-08-23)

- **k=9, f₉ = 0.00393, grid-4000 attempt is running in the background**
  (8 workers, 128-bit). This is the last borderline same-class k=9 step.
- **Multi-certificate LP (Shi generalization):** the existing two-certificate
  supporting-plane scan already reaches `B = 0.673316977142471313480…`
  (`R-20260817T030000Z-shiGeneralize-4f2a`). Further improvement within this
  family requires at least one **additional certified local certificate**
  (e.g. k=10 / q=9, or a stronger q=8 certificate), not just re-weighting the
  current two.
- **T2 reflection:** the detailed implementation plan is
  `reports/t2-reflection-plan.md`. A first concrete T2 data artifact is now
  available:
  `runs/rigorous-open-math-research/R-20260814T131528Z-f9push-d3b58c/reproducibility/kernel_table_exact_grid2000.json`
  (31,368 exact-rational kernel-table entries; binary64 sha256 matches the
  certified k=9 f₉=392/100000 table `39a209d3e4a897d982023ab49db27a206401824c769980572433dc4c47387297`).
  The remaining bottleneck is the terminal-box count and the Lean checker.

Current certified record: **k = 9, f₉ = 392/100000 = 0.00392** (grid-2000, 64,748,524 nodes,
128-bit Arb branch-and-bound), giving

- C₉(ζ)  = 0.673066472675939665848…
- C₉(ξ′) = 0.86920009109661916183995…

The generalized k-point verifier and the general-k chain are already in place:
`runs/rigorous-open-math-research/R-20260814T045000Z-extpress-2f36ae/` and
`R-20260814T131528Z-f9push-d3b58c/`.

### Next steps, in priority order

| Priority | Step | Expected gain vs current record | Cost / risk | Verdict from feasibility analysis |
|---|---|---|---|---|
| 1 | k = 9, f₉ = 0.00393, grid-4000 | +6.3e-6 | 1–2 days @ 8 workers | Borderline; margin ≈ bound loss; last same-class k=9 step worth attempting if compute budget is available |
| 2 | Exact-arithmetic / reflection certifier (T2 formalization route) | ≈ +1.5e-5 | Heavy Lean + engineering project | Removes interval rounding loss; still bounded by intrinsic quadratic-dip loss |
| 3 | Multi-certificate / supporting-plane / continuous saturation | unclear, potentially +0.1–0.4% | Requires rigorous derivation and certificate | Promising but currently only numerical evidence; must be made rigorous |
| 4 | k = 10, f₁₀ = 0.00394 | +2.7e-6 | 1–5 days | Poor value; not recommended with current machinery |
| 5 | k = 11 | none in current session | 2–10+ days | Infeasible with current verifier; keep as future computational target |

### k = 9, f₉ = 0.00393 launch packet (when compute is available)

From `runs/.../R-20260814T131528Z-f9push-d3b58c/f9-ladder.md`:

- Target: `F₈ ≥ 393/100000`
- Grid: 4000, precision: 128-bit
- Expected cutoff: `floor((393/100000) * 4000 * 4000) + 8 = 62888`
- Expected C₉(ζ): `0.673072744423451254556223736062`
- Worker pool: run with 8 workers (16+ worker pools have been observed unstable in this environment)
- Use validated verifier: `runs/.../R-20260814T131528Z-f9push-d3b58c/reproducibility/verify_kpoint_parallel.py`
- If the run cannot close, step back to f₉ = 0.00392 (already certified).

### Why the class is close to exhausted

The k-family feasibility report (`reports/k-family-feasibility.md`) concludes that the
pressure-certificate class is practically exhausted near the certified 0.00392 level with the
current interval machinery:

- k = 9 true minimum ≈ 0.00395005; certifying at the true minimum is infeasible because
  interval bound loss ≈ 1e-5 while the margin is 0.
- k = 10 scoping upper bound ≈ 0.00395808; the k = 10 steps are low value.
- k = 11 is infeasible at current resource levels.

---

## 2. Long-term backlog: Petersson–Kuznetsov bandwidth extension

**Keep this idea.** It is not currently a verified result, but it is a genuine research
direction worth revisiting.

### Idea

Extend the admissible bandwidth beyond the current λ ≤ 1 barrier by using the
Petersson–Kuznetsov trace formula (and automorphic spectral methods) to control the
off-diagonal terms that currently require unproven prime-pair information.

### Why it is hard

The Anthropic paper (`literature/raw/claude-paper-main-v2.txt`, §7.5) states explicitly that:

- λ ≤ 1 arises because for X ≫ T^l the off-diagonal terms are no longer dominated by the
  diagonal;
- evaluating them would require prime-pair information (Hardy–Littlewood type conjectures or
  Montgomery's pair-correlation conjecture beyond α > 1).

Therefore λ > 1 is a genuine frontier, not a formula substitution.

### Status

- **Keep:** yes.
- **Current Lean form:** intentionally archived / not claimed as verified.
- **Next research question:** can Kuznetsov-style spectral averaging give a rigorous
  unconditional bound on the required shifted-prime/off-diagonal sums in the relevant range?
- **Expected payoff if solved:** potentially a large jump (the current Bandwidth-1 ceiling is
  ≈ 0.6818, and λ > 1 would live beyond it).

---

## 3. Related notes

- Conditional higher-moment / Christoffel–Hankel direction (`HL*(k)`, 13/18, probability 1)
  is correct but conditional; keep as theory, not an unconditional record.
- The `SuperTheorem` / "combined >74%" idea remains archived and is not a mathematical route.
