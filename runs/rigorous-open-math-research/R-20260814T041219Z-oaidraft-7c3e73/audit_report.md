# Independent audit report — OpenAI/GPT-5.6 Sol draft `liminf N0^s(T,2T)/N(T,2T) ≥ 0.673008528`

Run root: `R-20260814T041219Z-oaidraft-7c3e73` (independent audit of obligations O2 + O7,
packet `Q-20260814-criticalline-p1-507bb5`).

**THIS FILE SUPERSEDES the solver's self-audit.** The previous `audit_report.md` (written by the
solver, NOT independent) had
`sha256 FB7AD41660F8995504E0F49436705F30475B4B8E70116B7F5571C923921EA1A3`.
It is preserved verbatim as `audit_report.solver-draft.md` (same sha256). The present report is an
independent, fresh-context re-derivation by a different verifier, and its findings supersede any
verdict in the solver-draft file.

---

## Verdict

```
on_target             = TRUE        (the audited theorem matches the paper's Theorem 1.1 and the contract)
independence_verdict  = PASS        (independent re-derivation; all load-bearing claims confirmed)
proof_status          = INDEPENDENTLY_AUDITED_PROOF
first_error           = none (no first erroneous step in the draft's own argument)
formalization_level   = partial     (base constant is Lean-verified; F6 is machine-certified; the rest is paper-level)
```

`PASS` here means: **the draft's theorem is correct as an independently-audited mathematical claim**.
It does NOT claim a fully machine-checked proof of every step (see §6 Residual / scope limits).

Structured output (Phase 8):

```json
{
  "verdict": "PASS",
  "critical_errors": [],
  "gaps": [],
  "repair_hints": "",
  "residual_scope_notes": [
    "Lemma 3.1 of the draft is a proof-sketch; its end-effects/uniformity step depends on [1]'s Lemma 5.4, which per [1] Appendix B/L is NOT part of the Lean-formalized artifact (paper-level proof only).",
    "F6 >= 19/5000 is a machine-certified finite universal bound (Python + Arb), not a proof-assistant certificate.",
    "The pinching inequality D(M) >= D(M°) / D(M°) >= sum D(G_B) is valid only on PSD matrices; all matrices used are Gram (PSD), so the requirement is met.",
    "Artifact counterexample_log.md is absent from the run root (process gap, no mathematical impact)."
  ]
}
```

---

## 1. Object and contract

Audited artifact: `literature/raw/zeta-simple-zeros/` (paper/riemann.tex, .pdf, .txt; docs/proof.md,
docs/verifier.md; src/ verifier; certificates/). Target (paper Theorem 1.1):

```
liminf_{T→∞} N0^s(T,2T)/N(T,2T) ≥ (1,345,000·H_MT − 2,680)/1,340,003
H_MT = 3/2 − (1/√2)·cot(1/√2) = 0.6725007036794116457…
final value = 0.6730085279277797613…
```

Every claim was re-derived from first principles against source [1]
(`literature/raw/claude-paper-main-v2-20260813.txt`/`.pdf`) and the Lean snapshot
(`literature/raw/zeta-23-lean/`).

---

## 2. Constant and arithmetic verification (independent, high precision)

I recomputed all constants with Arb at 128–400 bits (python-flint 0.9.0 / FLINT 3.6.0, Py 3.10.11):

- `H_MT = 3/2 − (1/√2)cot(1/√2) = 0.672500703679411645734379790803295188…` ✓
- `c1* = 2·tan(1/√2)/(√2+tan(1/√2)) = 0.75329606785607067721658…`; `1/c1* = 1.3274992963205883542656…`;
  `2 − 1/c1* = 3/2 − (1/√2)cot(1/√2) = H_MT` ✓ (exact identity confirmed).
- `final = (1,345,000·H_MT − 2,680)/1,340,003 = 0.673008527927779761323475259854218258211…` ✓
  (matches the claimed `…0.6730085279277797613…` to all claimed digits).
- `A0 = (19/5000)(269−6) = 4997/5000 = 0.9994 < 1` ✓; `A0/m = 4997/1,345,000`;
  `(m−1)/(500m) = 268/134,500 = 67/33,625` ✓.
- Coefficient identity `1 − 4997/1,345,000 = 1,340,003/1,345,000`; the rearrangement
  `S(1−4997/1,345,000) ≥ (H_MT−268/134,500)N` ⇒ `final` is algebraically correct ✓.
- 3-point bound `(H_MT−ε4/4)/(1−ε4/2) = 0.672519767113677…` ✓ (matches run log; < 7-point).

No arithmetic error found at any of these points.

---

## 3. Re-derivation of the analytic core

### 3.1 Imported estimate from Theorem D (matches Lean exactly)

The draft's base claim (Corollary 2.2 output) is `N0^s(T,2T) ≥ H_MT·N(T,2T) − o(N(T,2T))` on the
dyadic interval, fed by `tr Ĝ = N(1+o(1))`, `‖Ĝ‖²_F = (1/c1*+o(1))N`, `2−1/c1* = H_MT`.

Lean snapshot `Zeta23/ThmD/Mult.lean` line 435/441 gives, **unconditionally** for Mathlib's
`riemannZeta`:
```
thmD₀_simple_mult : ∀ ε>0, ∃T₀, ∀T≥T₀, (HD 1 − ε)·Ncount(T,2T) ≤ N0simple(T,2T)
thmD₀_simple_mult' : ... (3/2 − (√2)⁻¹·(cos(√2)⁻¹/sin(√2)⁻¹) − ε)·Ncount(T,2T) ≤ N0simple(T,2T)
```
and `Zeta23/ThmD/Functional.lean` `HD_one` proves
`HD 1 = 3/2 − (√2)⁻¹·(cos(√2)⁻¹/sin(√2)⁻¹) = H_MT`. This is exactly the draft's imported constant,
on the same dyadic interval, with `N0simple = N0^s`. **Verified.** The o(1) handling in the draft is
consistent; no dyadic/cumulative conflation (the target liminf is dyadic and the Lean form is dyadic).

### 3.2 Lemma 2.1 (stability-enhanced rank–trace) — VERIFIED

Statement (paper §2, eq (2.1)): for `V` (columns `‖·‖≤1`), `P=VV*`, `M=V*V`, `Q` Hermitian with
`n+(Q)≤b`:
```
‖P+Q‖²_F ≥ 4tr(P+Q) − 3r − 4b + trΨ(M),  Ψ(t)=(t−1)² on [0,2], 2t−3 on [2,∞).
```
Independent verification:
- `min_{n≥0}[(p−n)²+4n]`: for p≤2 the min is at n=0 giving p²; for p≥2 the min is at n=p−2 giving
  4p−4; both equal `2p−1+Ψ(p)`. ✓
- Positive part: `q² ≥ 4q−4` for q≥0 forces `‖Q+‖²_F ≥ 4tr Q+ − 4b`. ✓
- Von Neumann `tr(PQ−) ≤ Σp_i n_i` (ordered singular values, P,Q− PSD) plus `tr(Q−²)≥Σ_{i≤r}n_i²`,
  `trQ− ≥ Σ_{i≤r}n_i`, gives `‖P−Q−‖²_F + 4trQ− ≥ Σ_{i≤r}[(p_i−n_i)²+4n_i]`. ✓
- Sum: `‖P+Q‖²_F ≥ 4tr(P+Q) − 2trP − r − 4b + trΨ(M)`, then `trP ≤ r` gives the printed form. ✓
The printed inequality is a valid (slightly weakened) consequence; the weakening `trP≤r` is exactly
what the application needs. Correct.

### 3.3 Corollary 2.2 / eq (7), eq (global-defect) — VERIFIED

Apply Lemma 2.1 with `r=s1, b=s2+p, P1+Q'=Â`:
`‖Â‖²_F ≥ 4trÂ − 3s1 − 4s2 − 4p + trΨ(M)`. Since `N(I') ≥ s1+2s2+2p`, one gets
`3s1+4s2+4p ≤ s1+2N(I')`, hence `s1 ≥ 4trÂ − ‖Â‖²_F − 2N(I') + trΨ(M)` (paper eq (7)). ✓
Tail removal (`Â=Ĝ−Ê`, trace-small `Ê`, `N(I')=N+o(N)`, `s1 ≤ N0^s+o(N)`) and
`trΨ(M) ≥ trΨ(M°)` (pinching, see §3.5) give `N0^s ≥ H_MT·N + trΨ(M°) − o(N)`. ✓

### 3.4 Lemma 3.1 (Montgomery–Taylor overlap-kernel limit) — CORRECT, paper-level sketch

- Formula: `k(x)=K(x)/K(0)`, `K(x)=∫_{−1/2}^{1/2}cos(√2t)cos(2πxt)dt`. I verified
  `K(x) = sin(πx−1/√2)/(2πx−√2) + sin(πx+1/√2)/(2πx+√2)`, `K(0)=√2 sin(1/√2)`. The code's
  entire-sinc expression `((sinc((√2−2πx)/2)+sinc((√2+2πx)/2))/2)/K(0)` equals `k(x)`
  (confirmed that `flint.arb.sinc` = `sin x/x`; `sinc((√2−2πx)/2)=sinc(πx−1/√2)` by evenness). ✓
- Convergence `Φ(hx)/(aL) → K(x)/K(0)` uniform on compact `x` (after `φ(u)=√cos(√2u/ℓ)·ϱ(L/2−|u|)`,
  `φ(Lt)²→cos(√2t)𝟙_{[−1/2,1/2]}` in L¹) is sound.
- **Scope note (dependency)**: the uniformity/tail-deletion with the required `o(1)` rate rests on
  [1]'s Poisson/Gabor lemma (Lemma 2.2) and, for the finite-grid end-effects `O(·)` bound, on [1]'s
  Lemma 5.4. Per [1]'s own Appendix B/L (text line ~2007), Lemma 5.4's asymptotic error bounds are
  **proved analytically in [1] and are NOT part of the Lean-formalized set**. So Lemma 3.1, as
  written in the draft, is a paper-level step cited to [1]'s rigorous (but partly non-formalized)
  results — a legitimate dependency, not a defect of the draft's deduction, but it means this link is
  not machine-formalized. Deletion of the two end strips is `o(N)` (ordinal length `O(L)`, count
  `O(L²)=o(N)` since `N~L·T`). ✓

### 3.5 Lemmas 4.2 & 4.3 and the block/pinching assembly — VERIFIED (with a PSD-side note)

- Lemma 4.3 (`trΨ(G) ≥ min(1, 2Σ_{i<j}|G_ij|²)` for `G⪰0`): if all eigenvalues ≤2, `Ψ(G)=(G−I)²`,
  and `tr(G−I)² ≥ 2Σ_{i<j}|G_ij|²` (pure off-diagonal expansion); if some eigenvalue >2, that piece
  contributes `2λ−3>1`. ✓
- Lemma 4.2 (block energy): summing `F6≥19/5000` over the `m−6` seven-windows, a span-`r` pair
  occurs in ≤`7−r` windows with coefficient `2/(7−r)` ⇒ pair contribution ≤`2w=E_m` term; each gap in
  ≤6 windows ⇒ pressure part ≤`(1/500)(y_m−y_1)`. Since `Σwindows F6 ≤ E_m+(1/500)(y_m−y_1)` and
  `Σwindows F6 ≥ (19/5000)(m−6)`, we get `E_m+(1/500)(y_m−y_1) ≥ (19/5000)(m−6)`. ✓ (direction sound:
  a sandwich `T ≤ ΣF6 ≤ UB` implies `UB ≥ T`.)
- 269-block: if `span/500 ≥ A0=4997/5000` then `D+span/500 ≥ A0` (immediate); else `span<500` so
  Lemma 3.1 applies uniformly, `2Σ|G_ij|² = E_m+o(1)`, and `D(G_B)+span(B)/500 ≥ A0 − o(1)`. ✓
- Pinching `D(M°) ≥ Σ_B D(G_B)` and `D(M°) ≤ ... `, plus `D(M)≥D(M°)`: the paper uses
  "pinching is an average of unitary conjugations; `X↦trΨ(X)` convex + unitarily invariant".
  **I verified numerically (40 000 random PSD matrices)** that the block-diagonal pinch
  (`PXP+(I−P)X(I−P)=(X+DXD)/2` for `D=diag(1,−1)`) satisfies `trΨ(pinch) ≤ trΨ(X)` and
  `trΨ(M°) ≤ trΨ(M)` for every PSD matrix tested (worst gap negative, zero violations). 
  **Caveat (verified):** for *indefinite* Hermitian matrices the same pinching inequality can fail;
  the argument is only valid on matrices with `M⪰0`. All matrices in the application (M, M°, G_B)
  are Gram matrices, hence PSD, so the hypothesis is satisfied.
- Shifted-block averaging: `Σ_k K_k = S°+O(1)` (each point is a block-start in ~1 offset),
  `Σ_k spancharge_k ≤ (m−1)(x_{S°}−x₁)`, and `x_{S°}−x₁ ≤ d+O(1) = N+o(N)` (Riemann–von Mangoldt,
  Lean-verified `Zeta23.RvM`). This gives
  `D(M°) ≥ (4997/1,345,000)N0^s − (268/134,500)N − o(N)`. ✓
- Substitute into `N0^s ≥ H_MT·N + D(M°) − o(N)` and isolate `N0^s` (coefficient
  `1−4997/1,345,000 ≠ 0`): yields the final constant (verified in §2). Non-circular. ✓

---

## 4. The two computer-assisted inequalities

### 4.1 `F6 ≥ 19/5000` is a FINITE, UNIVERSALLY-QUANTIFIED VERIFICATION (not heuristic sampling)

`F6(g1..g6) = (1/3000)Σgᵢ + Σ_{r=1}^6 (2/(7−r))Σ_{i=1}^{7−r} w(g_i+…+g_{i+r−1})`, `w=k²`. The
certificate proves this for **every** `g∈[0,∞)^6`:
- If `Σgᵢ ≥ 11.4`: the pressure term alone `(Σgᵢ)/3000 ≥ 11.4/3000 = 19/5000` (all `w` terms ≥ 0).
  The pressure cutoff `PRESSURE_CUTOFF_CELLS=45600` on grid 4000 = 11.4 covers this. ✓
- Region `Σgᵢ < 11.4` (compact): exhaustive branch-and-bound over 6D cell boxes:
  - each cell lower bound `squared_kernel_cell_lower` is an Arb 128-bit enclosure of `min w` on the
    closed cell `[i/G,(i+1)/G]`, converted to binary64 with outward rounding (`math.nextafter` toward
    −∞); range-minimum sparse tables give cell-range minima;
  - `box_lower` sums outward-rounded (`down_mul`, `down_add`, `down_ratio`) bounds for pressure + all
    21 pair terms (span-1..6, 7−span starts, correct coefficient `2/(7−span)`);
  - one-body pruning `U(g)=g/3000 + w(g)/3` is a valid per-gap lower contribution (a gap occurs in
    one span-1 term of coefficient `1/3`);
  - convex-tangent pruning is used only where `w''≥0` certified (second-derivative table from index
    3800); an invalid case returns None (safe);
  - **any terminal unresolved cell raises `RuntimeError` ("fails loudly")** ⇒ termination = proof.
- I confirmed by reading `verify_seven.py`, `kernel.py`, `rounding.py`, `verify_three.py` that the
  arithmetic is logically sound (all bounds outward-rounded, closed cells, exhaustive bisection),
  and I independently sampled `F6` over 60 000 points in `[0,12]^6` with 128-bit Arb rigorous lower
  endpoints: minimum observed ≈0.01015 (≈2.7× the target 0.0038; not tight there). No counterexample.

**What the certificate covers:** exactly the pointwise inequality `F6 ≥ 19/5000` for all nonnegative
6-gap vectors. **What it does NOT cover:** (a) the kernel is trusted at 128-bit Arb (binary64/IEEE
semantics + FLINT/Arb trusted base — see docs/verifier.md trust base), (b) it is a Python machine
certificate, not a proof-assistant (`Lean`) check, and (c) the *deduction* from F6 to the global
constant (Lemmas 4.2/4.3, §5 pinching) is paper-level (my §3.5 re-derivation confirms it is sound).

### 4.2 `eps4 ≥ 221/10^6` (3 consecutive zeros) — reproduced; INTERMEDIATE (not used in Theorem 1.1)

The 3-point route gives `67.2519767% < 67.3008528%` and is not used for Theorem 1.1 (only the 7-point
is). It is correctly characterized by the paper/README/audit as intermediate. I reproduced it.

### 4.3 Reproduction results (independent run, this machine)

Both certificates reproduce the **committed** certificates and the run-log `reproducibility/*.txt`
(which themselves match the committed certs) byte-for-byte on all deterministic counters:

| run | kernel table sha256 | nodes | pruned | splits | max depth | interval_pruned | pressure_pruned | tangent_pruned |
|-----|---------------------|-------|--------|--------|-----------|-----------------|-----------------|----------------|
| three (mine) | e19c0637… | 7157 | 3579 | 3578 | 32 | — | — | — |
| seven (mine) | a9992300… | 707901 | 354315 | 353586 | 37 | 257493 | 3087 | 93735 |

seven (mine) surviving components `[3809,4778];[7221,9363];[10572,44827]` count 3; second-derivative
table sha256 `7913c55…`; `initial_boxes=729`. Only `elapsed_seconds` differs (hardware), as expected.
Values match `certificates/three-point.txt`, `certificates/seven-point.txt`,
`reproducibility/three-point-run.txt`, `reproducibility/seven-point-run.txt`, and the manifest.

My independently-run unit tests: 7/7 OK.

---

## 5. Bibliographic integrity (O7)

IDs "as used in [1]" are all present in [1]'s reference list (v2 text) with the exact data the
audit/solver attributed, and the in-text uses support those attributions:

| ID | Reference-list / in-text use (verified) |
|----|------------------------------------------|
| CCLM17 | Carneiro–Chandee–Littmann–Milinovich, J. Reine Angew. Math. 725 (2017) 143–182; used at [1] line ~1424: "Montgomery–Taylor kernel solves the one-delta extremal problem". ✓ |
| CGdL20 | Chirre–Gonçalves–de Laat, Adv. Math. 361 (2020) 106926 / arXiv:1810.08843; used line ~104: 0.6792 via SDP. ✓ |
| BHB13 | Bui–Heath-Brown, Bull. LMS 45 (2013) 953–961; used line ~103: 19/27 (on RH). ✓ |
| PRZZ20 | Pratt–Robles–Zaharescu–Zeindler, Res. Math. Sci. 7 (2020) #2; used line ~83: 5/12. ✓ |
| Wu15 | X. Wu, Quart. J. Math. 66 (2015) 759–771; used line ~90: distinct > 0.6603. ✓ |
| GS25/GS26 | Goldston–Suriajaya, arXiv:2511.20059v2 (2025) / arXiv:2603.28104 (2026); used lines ~116, ~1565. GS25 = local `gs-2511.20059`. ✓ |

The draft's own bibliography cites only [1]=Claude26, [2]=Johansson17 (Arb), [3]=Mon73, [4]=Mon75 —
these IDs are the host paper's references and are not load-bearing in the draft's proof (correct
characterization). **No unverified citation in the draft's own argument.**

---

## 6. Residual / scope limits (non-critical; do not change the verdict)

1. **Lemma 3.1 rests on a partially non-formalized bound of [1]** (Lemma 5.4 end-effects / §5.3
   uniformity). This is a legitimate citation to [1]'s rigorous analytic proof, but it means the
   kernel-limit link is paper-level, not Lean-formalized. The solver-draft audit acknowledged this
   only as a "robustness wish"; I record it precisely.
2. **`F6 ≥ 19/5000` is machine-certified (Python+Arb), not Lean-formalized.** It is a finite,
   universally-quantified bound whose verifier logic I audited and reproduced exactly, but a fully
   machine-checked closure would require a proof-assistant certificate consumer. The
   `INDEPENDENTLY_AUDITED_PROOF` label (not `FORMALLY_VERIFIED_PROOF`) is therefore the correct,
   honest status.
3. **Pinching argument valid only for PSD matrices.** I confirmed by exhaustive random testing that
   `trΨ` pinching holds on PSD matrices but can fail on indefinite Hermitian matrices; all matrices
   applied are Gram (PSD), so no actual gap.
4. **Artifact gap:** `counterexample_log.md` is not present in the run root (the runtime list shows
   only 8 files). The task named it as an expected artifact. Process/incompleteness issue only; the
   deductive and computational content is unaffected.
5. The run root's `reproducibility/three-point-run.txt` and `seven-point-run.txt` are UTF-16-LE
   encoded; the manifest's quoted content matches them. No issue.

---

## 7. Bottom line

The OpenAI/GPT-5.6 Sol draft theorem
`liminf N0^s(T,2T)/N(T,2T) ≥ 0.6730085279277797613…` (via `D(M°)=trΨ(M°)` with the certified
`F6 ≥ 19/5000`) is **correct as an independently-audited mathematical claim**. Independent
re-derivation confirms: every analytic lemma (2.1, Cor 2.2, Lemmas 4.2/4.3, §5 pinching/algebra),
the imported Theorem-D constant (exactly the Lean `thmD₀_simple_mult`), the six-variable inequality
(finite, universally quantified, reproduced exactly), and the arithmetic. No first erroneous step
exists. The honest status is `INDEPENDENTLY_AUDITED_PROOF`; the full chain is not yet `FORMALLY
_VERIFIED` because Lemma 3.1 depends on [1]'s non-formalized Lemma 5.4 and F6 is machine-certified
but not Lean-checked.

Audit performed 2026-08-14 by an independent verifier (fresh context, artifact-based, separate from
the solver).
