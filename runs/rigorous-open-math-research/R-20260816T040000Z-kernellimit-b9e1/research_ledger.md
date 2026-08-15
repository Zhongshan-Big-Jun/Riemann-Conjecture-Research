# Research ledger — kernel-limit lemma

Run: `R-20260816T040000Z-kernellimit-b9e1`

## Timeline

**Gate 0. Snapshot inventory.**
Located run dir `runs/rigorous-open-math-research/R-20260816T040000Z-kernellimit-b9e1`.
Read snapshot dirs: `Zeta23/ThmD/{ParamsD,Functional,Window,BridgeD}.lean`,
`Zeta23/Defs.lean`, `Zeta23/ZeroSide/RankTraceMult.lean`, `Zeta23/XiPrime/Window.lean`,
`lean-proof/Record9/Record9/Chain9.lean`, OpenAI `proof.md`, paper §7. Clean `git` state
noted (one pre-existing modified report file).

**Gate 1. Kernel form.**
The task gives `kMT(x)=[sinc(1/√2−πx)+sinc(1/√2+πx)]/(2√2 sin(1/√2))`; proof.md gives
`k(x)=K(x)/K(0)`, `K(x)=∫cos(√2t)cos(2πxt)dt`. Initial 40-digit numeric check with an
*incorrect* (dropped factor) K closed form showed a factor-2 discrepancy; corrected the
closed form (used `∫cos(ct)dt=2 sin(c/2)/c`), then kMT == K1/K1(0) exactly. Resolution:
`kMT = K_1/K_1(0)`; no factor-of-2 issue. (Ledger of the arithmetic slip is recorded for
reproducibility, not hidden.)

**Gate 2. Normalization pinning (the crux).**
Determined `⟨v_γ,v_γ′⟩` from Defs: zero-side Gram entry
`Gz k l = Σρ mρ φ̂(γρ−τk)φ̂(γρ−τl)`; atom `v_γ(u)=φ(u)e^{iγu}`; overlap
`⟨v_γ,v_γ′⟩=(φ²)̂(γ−γ′)=∫_{−L/2}^{L/2}φ²cos((γ−γ′)u)du`. With `x=(γ−γ′)L/2π`, substitution
`t=u/L` gives `⟨v_γ,v_γ′⟩ = L·F_L(x)`, and normalization by the diagonal gives
`F_L(x)/F_L(0) → K_λ(x)/K_λ(0)`. For λ=1 this is `kMT`. This matches the paper §1 statement.

**Gate 3. Cfun conflict resolved.**
Chain9 sidebar says "high-T limit of the finite-window overlap Cfun to this k". Analyzed
`Cfun` = *autocorrelation* `∫vStar(u/L)vStar((u+y)/L)du`; its cross phase is `√2λy/L`
(u-independent), so it cannot carry the `cos(2πxt)` beat. Confirmed numerically (Cfun/L
≠ kMT). Conclusion: the kernel-limit lemma's correct finite-window object is the
**Fourier** overlap, not `Cfun`. This is the precise, evidence-based resolution of the
normalization ambiguity; recorded as such, not glossed.

**Gate 4. Proof.**
Derived `|F_L(x)−K_λ(x)| ≤ 2w/L` from ramp-measure + bounded integrand; ratio limit;
`kMT=K1/K1(0)` closed form. Full detail in `candidate_proof.md`.

**Gate 5. Numerical cross-check.**
`reproducibility/kernel_limit_verify.py`: kMT==K1/K1(0) (40 digits); Fourier ratio O_L(x)/O_L(0)
== kMT exactly (pure-cosine profile, rate 0/roundoff). `ramp_rate_verify.py`: with fixed
ramp w=8, ratio → kMT with error·L ≈ const ⇒ O(w/L) rate (matches `2w/L` bound).
`numerical_evidence.md` records exact tables.

**Gate 6. Artifacts + hashes.**
Wrote all run artifacts; SHA256SUMS generated.

## Decisions / failed routes

- **Rejected**: interpreting `Cfun`/`integral_cos_overlap` as the direct finite-window model
  of the Gram overlap entry. It is the profile autocorrelation (J-moment), not the kernel
  overlap. Failure mechanism recorded (no beat frequency ⇒ no cos(2πxt)).
- **Rejected**: assuming a factor-2 normalization difference between paper `K/K(0)` and C₉
  `kMT`; they are exactly equal (arithmetic slip resolved).
- **Not pursued (bounded pass)**: Lean formalization of §3 statement. Requires opening a Zeta23
  .lean bridge; left as a follow-up `lean-verify` run with this run as the informal contract.
