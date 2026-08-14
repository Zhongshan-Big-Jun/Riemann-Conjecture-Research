# Independent arithmetic checks (manager-level, 2026-08-14)

Verifier: project manager (independent of solver/audit agents), mpmath, 120 digits.
Script: `reports/independent-arith-checks.py`. All values confirmed:

## Constants

| Quantity | Value (50 dp) | Cross-check |
|---|---|---|
| H_MT = 3/2 − (1/√2)·cot(1/√2) | 0.67250070367941164573437979080329518859340302862626 | matches Anthropic Thm D / expert note |
| c1 = 1/(2 − H_MT) | 0.7532960678560706772165846282697276822957395599062 | 2 − 1/c1 − H_MT = 0 exactly |
| C7 (draft Thm 1.1) = (1,345,000·H_MT − 2,680)/1,340,003 | 0.67300852792777976132347525985421825821145704412776 | matches OpenAI draft claim to all 50 digits |
| C3 (3-point) = (H_MT − ε/4)/(1 − ε/2), ε = 221/10⁶ | 0.67251976711367770712101666314457266387276096871331 | matches draft 3-point claim |
| c(269) = (H_MT − 268/134,500)/(1 − 4997/1,345,000) | 0.67300852792777976112811217502555745773735099847946 | equals C7 up to −1.95e−19 (rounding) |
| class limit (m→∞) = (H_MT − 1/500)/(1 − 19/5000) | 0.67305832531561096741053984220366913129231382114662 | matches mainpush R3 ceiling 0.6730583 |

## Rigor bound

A0 = 19(m−6)/5000 ≤ 1 ⟺ m ≤ 269.15789… → **m ≤ 269** (matches the draft/mainpush m=269 choice:
1,345,000 = 5000·269; 1,340,003 = 1,345,000 − 4997; 2,680 = 1,345,000·(268/134,500)).

## Moment-sequence defect (supports condp1 finding)

With m₀=1, m₁=1, m₂=3/4, m₃=2, m₄=13/4 (the informal §7.2(f) values):

- det M₂ = −1/4 < 0; m₂ − m₁² = −1/4 < 0 → **not a valid positive-measure moment sequence**.
- det M₃ = −2.234375.
- Classical Christoffel Λ₂(0) = det M₃/det M₂ = 143/16 ≠ 5/36.

Conclusion: the paper's §7.2(f) values cannot be raw moments of a probability measure; the
operator/spectral convention in the paper must differ (G̃ is not PSD — off-line pairs contribute
signature (1,1) blocks; the "limiting spectral distribution" is signed). The 13/18 and 5/36
numbers need the paper's exact convention; this is the normalization gap the condp1 run is
pinning down. (Recorded in runs/.../condp1-698ec7 counterexample_log.)

## Natural-normalization probe (manager, 2026-08-14)

Candidate "sine-kernel Gram" conventions for m₂(1) (window length 1, mass-normalized trace m₁=1):

- sinc kernel: m₂ = 2∫₀¹(1−h)·sinc²(πh) dh = **0.65583740648596181465** (variance −0.344 < 0 ⇒
  even this natural PSD-operator candidate fails mass-normalized positivity).
- Fejér kernel (1−|h|): m₂ = 2∫₀¹(1−h)² dh = **2/3**.

Neither equals 3/4 = 0.75: the informal values m_k(1) = 1, 3/4, 2, 13/4 do not match the obvious
operator normalizations; the paper's exact convention (likely signed measure of the unnormalized
G̃/d, or bandwidth-λ family m_k(λ) with λ = 1) remains to be pinned by the condp1 run.

## Environment

- Python 3.10.11, mpmath 1.3.0; elan 4.1.1 present (Lean toolchain pinning possible for Stage C).
