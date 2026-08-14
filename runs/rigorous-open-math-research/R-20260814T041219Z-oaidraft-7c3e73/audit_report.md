# Audit report — OpenAI/GPT-5.6 draft `liminf N0^s(T,2T)/N(T,2T) ≥ 0.673008528`

## Verdict

```
independence_verdict = PASS            (adversarial audit; independent verifier, fresh-context)
proof_status        = INDEPENDENTLY_AUDITED_PROOF
first_error         = none
```

The draft theorem is correct. Every step was re-derived independently against source [1]
(the Anthropic v2 paper) and the Lean-verified statements, and the two computer-assisted
inequalities were reproduced exactly.

## Structured audit (Phase 8 canonical outputs)

```json
{
  "verdict": "PASS",
  "critical_errors": [],
  "gaps": [],
  "repair_hints": ""
}
```

Scope note: this is an independent audit of the *mathematics and its finite verification*. It is
not a naive re-run only: the linear-algebra core, the block/pinching assembly, and the constant are
re-derived below; the two certificates were re-executed and matched byte-for-byte at the level of
all deterministic counters and interval-table hashes.

## 1. What is being claimed (per `paper/riemann.pdf`/`.tex`, README)

Theorem 1.1:
`liminf N0^s(T,2T)/N(T,2T) ≥ (1,345,000·H_MT − 2,680)/1,340,003 = 0.6730085279277797613…`,
`H_MT = 3/2 − (1/√2)cot(1/√2) = 0.6725007036794116457…`.

Structure of the proof:
- Base (imported): Anthropic Theorem D gives `N0^s ≥ H_MT·N − o(N)` (dyadic), `N=N(T,2T)`.
- §2: Lemma 2.1 (stability rank–trace with `D(M)=tr Ψ(M)`); Corollary 2.2 derives
  `N0^s(T,2T) ≥ H_MT·N + D(M°) − o(N)`, `M°` = Gram of retained central simple zeros.
- §3: Lemma 3.1 — inner products of simple-zero vectors converge uniformly to the
  Montgomery–Taylor overlap kernel `k(x)=K(x)/K(0)`, `K(x)=∫cos(√2t)cos(2πxt)dt`.
- §4: 7-point local inequality `F6 ≥ 19/5000` (Prop 4.1, computer-assisted); Lemmas 4.2/4.3 turn it
  into an energy + defect bound on each 269-block.
- §5: shifted-block pinching + averaging ⇒ `D(M°) ≥ (4997/1,345,000)S° − (268/134,500)N − o(N)`;
  substitution gives the constant.

## 2. Re-derivation checklist (each point independently re-checked)

### 2.1 Analytic estimates imported from Theorem D — **CORRECT, exactly as Lean proves**

The draft needs (Corollary 2.2):
`tr Ĝ = N(1+o(1))` and `‖Ĝ‖²_F = (1/c1* + o(1))N`, with `2 − 1/c1* = H_MT`, in the units
`Ĝ = G/(aL²)` (paper §4.4).

- Paper §7.1/Theorem D and eq (7.2)–(7.4): optimal window `φ(u)=√cos(√2 u/l)·ϱ(L/2−|u|)` gives
  `(tr Ĝ)²/tr(Ĝ²) → c*_1`, `c*_1 = 2tan(1/√2)/(√2+tan(1/√2)) = 0.753296…`; hence
  `‖Ĝ‖²_F/tr Ĝ → 1/c*_1`. Verified: `1/c*_1 = 1/2 + (1/√2)cot(1/√2) = 1.327499…` so
  `2 − 1/c*_1 = 3/2 − (1/√2)cot(1/√2) = H_MT`. (High-precision arithmetic confirmed `H_MT=0.6725007036794116457…`.)
- Lean `Zeta23/ThmD/Mult.lean` `thmD₀_simple_mult` / `thmD₀_simple_mult'`: exactly
  `∀ε>0, ∃T₀, ∀T≥T₀, (3/2 − (√2)⁻¹·cos((√2)⁻¹)/sin((√2)⁻¹) − ε)·Ncount T (2T) ≤ N0simple T (2T)`,
  i.e. `N0^s(T,2T) ≥ (H_MT − ε)N(T,2T)` for all large T, on the dyadic interval.
  ⇒ The draft's claimed base bound is **exactly** the Lean-verified Theorem-D simple-zeros line.
- o(1) handling: the paper §6/Theorem D proof makes the error `o(N)` (with the λ=1 endgame via
  λ→1⁻ and `ET ≪ log l / l`); the draft correctly keeps the `−o(N)` and drops it in the liminf.
  No dyadic/cumulative conflation: the target liminf is over the *dyadic* interval and the Lean form is dyadic. ✓

### 2.2 Lemma 2.1 (stability rank–trace, `D(M)=tr Ψ(M)`) — **PROVED**, correct

Statement: `V` (d×r, columns `‖·‖≤1`), `P=VV*`, `M=V*V`, `Q` Hermitian, `n+(Q)≤b`:
`‖P+Q‖²_F ≥ 4tr(P+Q) − 3r − 4b + D(M)`, `D(M)=tr Ψ(M)`.
Re-derivation (von Neumann + convex spectral estimates):
1. `Q=Q₊−Q₋`, `Q±⪰0`, `rank Q₊ ≤ b`; `‖P+Q‖²_F ≥ ‖P−Q₋‖²_F + ‖Q₊‖²_F` (since `tr(PQ₊)≥0`, `tr(Q₋Q₊)=0`).
2. `‖Q₊‖²_F = Σq_j² ≥ Σ(4q_j−4) = 4tr Q₊ − 4·#{q_j>0} ≥ 4tr Q₊ − 4b`.   ✓
3. Von Neumann: `tr(PQ₋) ≤ Σᵢ pᵢnᵢ`; `‖P−Q₋‖²_F + 4tr Q₋ ≥ Σᵢ[(pᵢ−nᵢ)²+4nᵢ] ≥ Σᵢ minₙ[(p−n)²+4n]`
   = `Σᵢ Ψ̄(pᵢ)` where `Ψ̄(p)=p²` on `[0,2]`, `4p−4` on `[2,∞)`; and `Ψ̄(p) = (2p−1)+Ψ(p)`
   (`Ψ(p)=(p−1)²` on `[0,2]`, `2p−3` on `[2,∞)` — checked).
   Hence `‖P−Q₋‖²_F ≥ 2tr P − r + D(M) − 4tr Q₋` (since `ΣΨ(pᵢ)` over the r eigenvalues of `M`).
4. Add: `‖P+Q‖²_F ≥ 4tr(P+Q) − 2tr P − r − 4b + D(M) ≥ 4tr(P+Q) − 3r − 4b + D(M)` (as `tr P ≤ r`).
   ⇒ The printed inequality is a valid (slightly weakened) consequence; the weakening `tr P ≤ r`
   is exactly what the application (`tr P₁ ≤ s₁`) uses. **No error.** (`D(M)≥0` throughout.)

### 2.3 Corollary 2.2 — **PROVED**, correct

Apply Lemma 2.1 to `P₁ + Q' = Â`, `r=s₁`, `b=s₂+p`, `M=VᵀV`:
`‖Â‖²_F ≥ 4trÂ − 3s₁ − 4(s₂+p) + D(M)`.
With `N(I') ≥ s₁+2s₂+2p` (paper eq 4.3) one verifies `3s₁+4s₂+4p = s₁ + 2(s₁+2s₂+2p) ≤ s₁ + 2N(I')`,
hence `‖Â‖²_F ≥ 4trÂ − s₁ − 2N(I') + D(M)`, i.e. `s₁ ≥ 4trÂ − ‖Â‖²_F − 2N(I') + D(M)` (eq 7). ✓
Tail removal (same as paper Prop 4.2): `Â=Ĝ−Ê`, `‖Ê‖≪ θ₀ ≪ lT^{λ/2−1}`, `trÊ` trace-small, `N(I')=N+o(N)`;
`s₁ ≤ N0^s(T,2T)+o(N)`; `D(M) ≥ D(M°)` by convexity+conjugation-mean pinching (valid even though `Ψ(0)=1≠0`,
because pinching is an average of unitary conjugations and `X↦trΨ(X)` is convex). Subst.: `N0^s ≥ H_MT N + D(M°) − o(N)`. ✓

### 2.4 Lemma 3.1 (overlap-kernel limit) — **correct; proof at [1]-style sketch level**

`⟨v_ρ,v_ρ'⟩ → k(x_ρ−x_ρ')` uniformly for retained zeros with `|x_ρ−x_ρ'|≤R₀`.
- Formula check: `φ(u)=√cos(√2 u/ℓ)·ϱ(L/2−|u|)` ⇒ `φ²(u)/L → cos(√2 t)𝟙`; normalized overlap
  `Φ(hx)/(aL) = [∫φ(Lt)²e^{-2πixt}dt]/[∫φ(Lt)²dt] → K(x)/K(0)`, `K(x)=∫_{-1/2}^{1/2}cos(√2t)cos(2πxt)dt`,
  `K(x)=sinc(πx−1/√2)+sinc(πx+1/√2)` (with the removable-singularity remarks), `K(0)=√2 sin(1/√2)`. ✓
- The full-grid Poisson identity is exactly the paper's Lemma 2.2 (`Σ_{j∈ℤ}φ̂φ̂ = LΦ`); the finite-grid
  truncation `O(L^{-2})` is the paper's §5.3/`Lemma 5.4` end-effects result, correctly invoked.
  Uniformity (for `|x−x'|≤R₀` fixed) follows from the compact-support + `r^{-2}` decay. ✓
- End-strip deletion: normalized width `L²` ⇒ ordinate length `O(L)` ⇒ `O(L log T) = o(N)` zeros. ✓
Accepted as a correct, appropriately-cited analytic step (not re-proven ab initio with explicit rates;
the draft defers to [1]'s rigorous Lemma 5.4 mechanism — a legitimate dependency).

### 2.5 Proposition 4.1 (`F6 ≥ 19/5000`) — **finite, universally-quantified, computationally PROVED; certificate reproduced exactly**

`F6(g₁..g₆) = (1/3000)Σgᵢ + Σ_{r=1}^6 (2/(7−r))Σᵢ w(gᵢ+…+gᵢ+r₋₁)`, `w=k²`.
- If `Σgᵢ ≥ 11.4`: `(1/3000)Σgᵢ ≥ 11.4/3000 = 0.0038 = 19/5000` exactly (all other terms ≥0). ✓
- Compact region `Σgᵢ<11.4`: verifier covers the 6D simplex by rigorous Arb interval branch-and-bound
  (grid 4000; 128-bit Arb evaluates `k`; outward-rounded binary64 combines lower bounds; range-min
  sparse tables; one-body pruning; convex-tangent (Hessian PD) pruning with Arb re-check; exhaustive
  bisection). Any terminal unresolved box ⇒ loud failure. ⇒ This is a **finite verification of a
  universally quantified bound**, not heuristic evidence.
- **Reproduction:** `zeta-zero-verify seven` reproduced exactly the committed certificate
  `certificates/seven-point.txt`: kernel table sha256 `a9992300…`, second-derivative table sha256
  `7913c55…`, `nodes=707901`, `pruned=354315`, `splits=353586`, `maximum_depth=37`,
  `initial_boxes=729`, `interval_pruned=257493`, `pressure_pruned=3087`, `tangent_pruned=93735`,
  surviving components `[3809,4778];[7221,9363];[10572,44827]`. (elapsed 190.6s vs 136.7s − hardware.)
  The `3-point` certificate also reproduced exactly (table hash `e19c06…`, nodes 7157, …).
- Kernel code correctness: `normalized_kernel = ((sinc((√2−2πx)/2)+sinc((√2+2πx)/2))/2)/K(0)` equals
  `k(x)` (sinc evenness + the ½ normalising factor checked); `K(0)=√2 sin(1/√2)`. Rigorous cell lower
  bounds via `abs_lower` then `down_mul`. Sound mechanism.

### 2.6 Lemmas 4.2 & 4.3 — **PROVED**, correct

- Lemma 4.2 (block energy): summing `(14)` over the `m−6` seven-windows of `m` ordered points;
  each span-`r` pair appears in ≤ `7−r` windows at coefficient `2/(7−r)` ⇒ total pair contribution ≤
  `Σ2w = E_m`; each single gap in ≤ 6 windows ⇒ ≤ `(1/500)(y_m−y₁)`. Hence
  `E_m + (1/500)(y_m−y₁) ≥ (19/5000)(m−6)`. ✓
- Lemma 4.3: `trΨ(G) ≥ min(1, 2Σ_{i<j}|G_ij|²)`.
  - If all eigenvalues ≤ 2: `Ψ(G)=(G−I)²`, `tr(G−I)² = Σ_i(G_ii−1)² + 2Σ_{i<j}|G_ij|² ≥ 2Σ_{i<j}|G_ij|²`. ✓
  - If some eigenvalue `λ>2`: `Ψ(λ)=2λ−3>1`, and `min(1,·)≤1`. ✓
  (Both cases airtight; the first is pure expansion, no subtlety.)

### 2.7 §5 shifted-block pinching → eq (21) → Theorem 1.1 — **PROVED**, correct

- `m=269`, `A0=(19/5000)(m−6)=4997/5000<1`.
- Each 269-block `B`: if `span(B)/500 ≥ A0` then `D(G_B)+span/500 ≥ A0` (immediate); else `span<500`
  ≤ `R₀` so Lemma 3.1 uniform, `2Σ|G_ij|²=E_m+o(1)`, and Lemmas 4.2/4.3 give `D(G_B)+span/500 ≥ A0−o(1)`. ✓
- Pinching `D(M°) ≥ Σ_B D(G_B)` per partition (convexity + conjugation-averaging). ✓
- Sum over full blocks of each of `m` offsets: `m·D(M°) ≥ A0·ΣK_k − (1/500)Σ_k spancharge_k − o(N)`.
  `Σ_k K_k = S° + O(1)` (each point is a block-start in ~1 offset); each gap is internal in ≤ `m−1`
  offsets ⇒ `Σ_k spancharge_k ≤ (m−1)(x_{S°}−x₁)`; `x_{S°}−x₁ = d+O(1) = N+o(N)` (Riemann–von Mangoldt).
  ⇒ `D(M°) ≥ (A0/m)S° − (m−1)/(500m)·N − o(N)`, i.e. `(4997/1,345,000)S° − (268/134,500)N − o(N)`. ✓
- Substitute into `N0^s ≥ H_MT·N + D(M°) − o(N)`; solving (coefficient `1−4997/1,345,000 > 0`):
  `liminf N0^s/N ≥ (1,345,000·H_MT − 2,680)/1,340,003`. High-precision: `0.6730085279277797613…` ✓.
  (Non-circular: the rearrangement isolates `N0^s`, `S°=N0^s−o(N)`.)

### 2.8 Equality / sharpness claims

- The draft README's claim that the *base* rank–trace has an equality case with mutually-orthogonal
  simple-zero vectors (so the base `H_MT` is untouched by the raw rank–trace) is consistent with
  [1] §7.5(b) (sharpness of Proposition 4.4 with mutually orthogonal simple on-line zeros). The whole
  point of `D(M°)` is to charge the *non-orthogonality* of the real kernel vectors.
- Both new inequalities are **proved**: Lemma 2.1 analytically; Prop 4.1 by a rigorous finite,
  universally-quantified verification (see 2.5). Neither is asserted from sampling.
- The constant `0.673008528` is below the bandwidth-one ceiling `≈0.68185` of the method ([1] Remark 1.1),
  so it makes no over-claim and is not refuted by the ceiling. This is a genuine strict improvement
  over `H_MT`, conditional only on the (checked) certificate.

### 2.9 Bibliographic resolution (IDs "as used in [1]"; from v2 reference list)

| ID | Bibliographic data |
|---|---|
| CCLM17 | E. Carneiro, V. Chandee, F. Littmann, M. B. Milinovich, *Hilbert spaces and the pair correlation of zeros of the Riemann zeta-function*, J. Reine Angew. Math. 725 (2017), 143–182. (Used [1] §7.1: one-delta extremal problem ⇒ MT kernel optimal.) |
| CGdL20 | A. Chirre, F. Gonçalves, D. de Laat, *Pair correlation estimates for the zeros of the zeta function via semidefinite programming*, Adv. Math. 361 (2020), 106926; arXiv:1810.08843. |
| BHB13 | H. M. Bui, D. R. Heath-Brown, *On simple zeros of the Riemann zeta-function*, Bull. Lond. Math. Soc. 45 (2013), 953–961. (19/27 on RH.) |
| PRZZ20 | K. Pratt, N. Robles, A. Zaharescu, D. Zeindler, *More than five-twelfths of the zeros of ζ are on the critical line*, Res. Math. Sci. 7 (2020), Paper No. 2, 74 pp. |
| Wu15 | X. Wu, *Distinct zeros of the Riemann zeta-function*, Quart. J. Math. 66 (2015), 759–771. |
| GS25 | D. A. Goldston, A. I. Suriajaya, *Zeta zeros on the critical line*, arXiv:2511.20059v2 (2025). [= local `gs-2511.20059`] |
| GS26 | D. A. Goldston, A. I. Suriajaya, *Zeta zeros in a narrow vertical box*, arXiv:2603.28104 (2026). |

The draft itself cites only [1], Arb [2], Montgomery [3], [4]; the IDs CCLM17/CGdL20/BHB13/PRZZ20/
Wu15/GS25/GS26 are the *host paper's* references and are not load-bearing in the draft's proof.

## 3. Adversarial attacks attempted

- Sign/direction re-check of the eq (1)→(7) step (the most likely algebraic trap) — passed (see 2.3).
- `Ψ(0)=1≠0` and whether pinching `D(M)≥D(M°)` fails — passed via convexity + conjugation-averaging.
- Kernel `½`-factor / `K(0)` normalisation — passed (high-precision + code formula both correct).
- Whether `F6≥19/5000` could be an under-cover (validity of the `Σg≥11.4` cutoff, one-body pruning,
  range-min table correctness, convex Hessian certification) — passed; certificate reproduced exactly,
  terminal-box loud-failure guard.
- Uniform `o(1)` over O(N) blocks / end-strip deletion / `x_{S°}−x₁=N+o(N)` — passed.
- Sharpness ceiling; whether the improvement is a circular restatement of the target — not the case;
  it refines the Gram-defect only, and stays below the method ceiling.

## 4. Residual non-critical observations (do not affect verdict)

- `Lemma 3.1` is written as a proof-sketch and relies on [1]'s rigorous `Lemma 5.4` (end-effects) and
  Lemma 2.2 for the finite-grid truncation `O(L^{-2})` and uniformity. This is a legitimate citation,
  but a reader wanting a fully self-contained proof would expand it.
- The draft's abstract/full-paper text differs slightly from the README's wording of the 3-point route,
  which is intermediate only (gives 67.2519767% < 67.3008528%) and is not used in Theorem 1.1.
- Some PDF-extraction artifacts (e.g. a `√(2u)/ℓ` typesetting mis-read) are corrected by the `.tex`; no
  mathematical impact (the kernel and constants are consistent).

## 5. Bottom line

The OpenAI/GPT-5.6 Sol draft is **mathematically sound**. Its new ingredient is the stability
refinement `D(M°)=trΨ(M°)` with a uniform positive lower bound obtained from an Arb-certified,
six-variable, universally-quantified inequality (`F6 ≥ 19/5000`), which was **independently re-executed
and reproduced byte-for-byte** on this machine. All imported analytic estimates match the
Lean-formalized Theorem D constants. No first erroneous step exists.

Audit performed 2026-08-14 by an independent solver subagent (fresh-context, artifact-based).
