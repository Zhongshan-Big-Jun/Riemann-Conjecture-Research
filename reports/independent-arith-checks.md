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

## Records-family re-verification (manager, 2026-08-15, mpmath 70 digits)

Every constant in the FRONTIER records table now has an exact rational form and was
re-verified with pure-integer-coefficient mpmath evaluation (float64-division pitfalls
avoided):

| Constant | Exact form | Value (60 dp) |
|---|---|---|
| C₇ | (1,345,000·H_MT − 2,680)/1,340,003 | 0.673008527927779761323475259854218258211457044127760… |
| C₃ | (H_MT − 221/4,000,000)/(1 − 221/2,000,000) | 0.67251976711367770712101666314457266387276096871331… |
| C₉(0.0039) | (2,640,000·H_MT − 5,260)/2,630,016 = (6875·H_MT − 1315/96)/6849 | 0.673053645952589925209110000745508505608552950085983… |
| C₉(0.00395) | (26,100,000·H_MT − 52,000)/26,000,065 | 0.673085562133504049073235491525348279794216631656324… |
| C₉(0.00398) | (25,900,000·H_MT − 51,600)/25,800,102 | 0.673104634442792575956499574373982916213631188024770… |
| C₉^{ξ′}(0.0039) | (2,640,000·H_{ξ′} − 5,260)/2,630,016 | 0.869183535052827477039238862238746238390867247961215… |
| C₉^{ξ′}(0.00395) | (26,100,000·H_{ξ′} − 52,000)/26,000,065 | 0.869224726234155780682210369165264862803577221356718… |
| Nd/N | (3 − 1/c1)/2 | 0.83625035183964… (c1 = 0.753296067856…) |
| class limits | (H_MT − 1/500)/(1 − f) | k=7@19/5000: 0.67305832531561…; k=9@0.0039: 0.67312589466862…; k=9@0.00395: 0.67315968443292…; k=9@true-min: 0.67318118876984… |

All values match the previously synced records (differences at 1e-19 in intermediate checks
were traced to float64 division in the checking code, not the records).
