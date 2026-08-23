# Campaign 2 (2026-08-11, afternoon): three attempted improvements and what they proved

After the morning's certified record (0.673137630699…), a second multi-model
campaign attempted to improve it by three successively more ambitious routes.
No route produced a verified bound above the record. Each produced rigorous
knowledge that sharpens where the frontier actually is. This document is the
consolidated account; full lane reports live in the research workspace
(`numerics2/`, `numerics3/` — available on request; summaries below are
self-contained).

## Headline

- **The record 0.673137630699… is provably near-optimal within its method
  family.** The gap-horizon transfer-operator class (which contains the
  published certificate as an exact special case via an explicit coboundary)
  was searched with a rigorous joint branch-and-bound LP at horizon 6:
  the best assembled bound was 0.67249, and ground-state analysis shows the
  published certificate already extracts ~80% of what any horizon-6
  certificate can collect. Horizon ceilings: ≈0.67331 (R=6), ≈0.67340 (R=8).
- **Pure pair-energy methods cap at 0.674826.** The exact balanced word
  g_i = 1 + ⌊(i+1)·327/673⌋ − ⌊i·327/673⌋ (P=673 points on L=1000, all pair
  distances integer) has total pair energy e_full < 0.003523506664, giving a
  first-order per-configuration ceiling 0.674828 for every certificate that
  reads only pair energies of simple zeros.
- **Bandwidth λ > 1 cannot be opened by unconditional sieve bounds.** The
  off-diagonal prime sum is signed; absolute majorization loses at least a
  factor 6.1 against the formal gain even with oracle constants. Exact
  sufficient thresholds for future arithmetic: a direct form-factor cap
  C < 17.8373866, or Hardy–Littlewood-strength input at λ > 1.00985.
- **The off-line pair bridge — the gate to 0.675+ — is now a single open
  lemma with strong evidence.** See below.

## Tier 2: transfer-operator (Bellman/coboundary) certificates

Scheme: replace fixed windows by a state-space certificate
ℓ(σ′) + p·g + H(σ′) − H(σ) ≥ λ over gap states, telescoped over blocks.
Proved: exact boundary lemma (synthetic-overflow startup, c_R = 1, loss ≤
osc(H)); a zero-gain theorem for K-step weighted variants (λ_K*/μ = λ_1*
identically — multi-step mixing can never beat one-step with the same cell
information); equivalence of the published certificate to an explicit
coboundary (delay-line filter H) at λ = 1/200, p = 6/2300.
Certified: joint R=6 LP candidate λ = 0.0039508229 with a 24.2M-node
independent recheck (zero failures) — assembling to 0.67249 < record.
Verdict: class exhausted; negative is rigorous.

## Tier 2.5: tail-capturing certificates

Two-thirds of the collectible pair energy lies in the 1/x² kernel tail beyond
horizon 8, but the phase-locked integer configurations above cap what any
pair-energy instrument can extract at 0.674826. Fixed tail projectors are
evaded (best possible assembled value 0.674983 at infeasible window width
W = 100); density-statistic rows are dead (integer configs cap their yield at
~10⁻⁶). A finite, fail-closed storage-function/S-procedure architecture was
designed, adversarially audited, and archived behind a mandatory pre-LP
screen (periodic-orbit cycle means bound λ from above before any solve) with
an honest gate: e_eff ≥ 0.0032434 for record + 0.0015. Not launched.

## Tier 3: the off-line pair bridge (the gate to 0.675–0.678)

The current method prices only simple on-line zeros; the extremal law for the
class ceiling p₂₅₆ = 0.68182868746… uses ~31.8% mark-2 mass. Pricing that
mass requires a new theorem — the bridge — treating each off-line hyperbolic
pair as a virtual on-line double (retaining Gram-defect interaction) or
charging it a spectral penalty.

**Proved (exact, certified):**
- Exact complex Gram formulas for pair blocks with normalization
  D = L(β−1/2)/(2π), certified by 82,751-box complex-interval (acb) proof.
- Local bridge theorems: raw δ ≥ d₁₂ + π; robust B ≥ d₁₂ and ≥ T²−1;
  one-pair positive-environment theorem Δ ≥ D₂ + (T−1)².
- A safe global regrouping D₊ preserving the entire simple-zero defect.

**Refuted (exact counterexamples):**
- Additive local pricing: an actual-kernel two-pair configuration with
  δ₂ − 2π = −22.14 (certified); a Schur-deficit witness (≈0.1249) against
  stacking local B on the full simple defect; a shifted-kernel-zero escape
  (θ = π = 0) for the naive safe assembly.
- Abstract PSD composition: the two-pair envelope over arbitrary PSD Gram
  matrices is negative (spectral crowding at the k₂ kink at eigenvalue 2) —
  the global claim is not provable from positivity alone.

**Standing conjecture (all evidence positive):** the global virtualized claim
Δ_actual ≥ D₂(fully virtualized) + Σ scalar-residual survived ~10⁵
adversarial configurations (six independent sub-agent lanes, two kernels, an
independent reimplementation) with worst per-pair residual 0.00686 — 5.6×
the assembly break-even κ = 0.00122 — and exact infinite pair-chain (Bloch)
limits sustain 0.0101–0.0271 per pair at all depths, meeting the extremal
law's requirement (0.0117/pair average) for 0.675. No transition dead zone
exists; multiplicity ≥ 3 dodges self-destruct.

**The open lemma:** prove the multi-pair composition using the kernel's
positive-type (band-limited Bochner) structure — e.g. a Szegő-type
anti-crowding bound controlling eigenvalues near the k₂ kink for Gram
matrices of translates of a positive-definite band-limited function — or a
kink-regularized (taxed) defect variant. If proved with the measured
constants, the assembled bound lands in **0.674–0.675**.

## λ > 1 frontier (closed)

Signed off-diagonal structure defeats sieve majorization by ≥6.1×; no
Fejér-positivity rescue; the existing bookkeeping already tolerates
η ≲ (log ℓ)/ℓ with zero liminf gain. Future arithmetic targets quantified
above. This closes the only known route past the class ceiling p₂₅₆.

## Method note

Same protocol as the morning: multi-model lanes (GPT-5.6 Sol design/audit,
Claude Fable refutation, Grok numerics, Kimi excavation, ~20 GPT-5.6 Luna
breadth sub-agents), everything load-bearing either interval-certified or
killed by exact counterexample. Two plausible-but-wrong ideas (a K-step
telescoping gain; an over-optimistic ground-state energy) were caught by
cross-lane adversarial checks before any certification effort was spent.
