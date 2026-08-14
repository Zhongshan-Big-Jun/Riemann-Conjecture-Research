# Linked zeta/ξ′ record ladder (2026-08-14)

One k=9 pressure certificate serves BOTH families (the kernel is window-determined only):
the ζ record and the ξ′ candidate (reports/xi-prime-pressure-method.md) move together.

| Certified f₉ | ζ: C₉ (N₀ˢ/N) | ξ′: C₉^{ξ′} (N₀ˢ_{ξ′}/N_{ξ′}) |
|---|---|---|
| 0.00390 (certified) | 0.67305364595258992520 | 0.86918353505282747704 |
| 0.00392 (in certification, pwsh-4 grid-2000 — RELEASE TARGET) | 0.67306647267593966585 | 0.86920009109661916184 |
| ~~0.00395 (withdrawn)~~ | ~~0.67308556213350404907~~ | ~~0.86922472623415578068~~ |
| 0.00398 (stretch) | 0.67310463444279257595 | 0.86924933896212678271 |

**2026-08-15 correction**: the 0.00395 row is WITHDRAWN — the F₈ ≥ 0.00395 certificate failed
(both grid-2000 and grid-4000 runs): the true minimum of F₈ is ≈ 0.00395005 (configuration
[1.0465,1.996,1.9995,1.9995,1.9865,1.04525,1.97575,1.04525]; value 0.003950049001339790,
exact-kernel verified), so the margin ≈ 5e-8 is below the verifier's bound loss ≈ 1e-5 —
infeasible (details: f9-ladder.md CORRECTION). The release target is now f₉ = 0.00392
(n = 255, m = 263, A₀ = 2499/2500 < 1; margins ≈ 1.1e-5 above the critical leaf bound,
≈ 3.0e-5 above the presumed true min).

Exact rational forms (manager, mpmath 70 digits, 2026-08-15; pure-integer-coefficient
evaluations — float64 division pitfalls avoided):
- C₉(f; H) = (H − (m−1)/(500m)) / (1 − f·n/m), n = ⌈1/f⌉−1, m = 8+n.
- f=0.00392 (n=255, m=263): C₉ = (657,500·H − 1,310)/655,001
  → ζ: 0.673066472675939665848379945149956391669879116706338817644865705…
  → ξ′: 0.869200091096619161839954323888625751630669422158034337098576708…
- f=0.00395 (n=253, m=261): C₉ = (26,100,000·H − 52,000)/26,000,065
  → ζ: 0.67308556213350404907323549152534827979421663165632441534520277175… (withdrawn)
  → ξ′: 0.869224726234155780682210369165264862803577221356718139913624558108218… (withdrawn)
- f=0.00398 (n=251, m=259): C₉ = (25,900,000·H − 51,600)/25,800,102
  → ζ: 0.673104634442792575956499574373982916213631188024769810765723008758…
  → ξ′: 0.8692493389621267827062525179120150033695438835191711139556918072623011…
- f=0.00390 (n=256, m=264): C₉ = (2,640,000·H − 5,260)/2,630,016
  = (6875·H − 1315/96)/6849 (closed form; identity verified to 1e-71).
  → ζ: 0.673053645952589925209110000745508505608552950085983191119032970318…

ξ′ comparanda: flat 0.85838, quartic 0.86864 (unconditional); 0.8825 (RH-conditional,
CGdL20). At f₉ = 0.0039 the ξ′ candidate already exceeds quartic by 5.4e-4; at 0.00392 it
would exceed by 5.6e-4.

Notes: m₉ and A₀ are f₉-determined and identical for both families (pressure chain is
structural); the ξ′ baseline H_{ξ′}^{MT} = 0.8678888651990519355503… is fixed (A2-verified).
Optimality check (2026-08-14): C₉(n) is strictly increasing in n (f=0.0039: n=200 →
0.6730342, n=256 → 0.6730536), so n = ⌈1/f⌉−1 (the largest n with A₀ = f·n < 1) is the
optimal block parameter; both ladders use it.
**Optimality re-verified 2026-08-15 (mpmath 40d): strict increase confirmed on n ∈
{1,50,100,150,200,220,240,255,256,257} (n=257 has A₀ = 1.0023 ≥ 1, excluded); n=200 →
0.673034197303917, n=256 → 0.67305364595259 — matches the quoted values.**
Pending audits: A1 (block structure write-up), A3 (kernel-limit transfer), plus the f₉
certificate itself.
