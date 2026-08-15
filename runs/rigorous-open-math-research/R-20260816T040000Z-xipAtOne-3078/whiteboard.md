# Whiteboard — M3-open-A AtOne certificate for κ₁(1,vMT)

Key numbers (all rounded; exact enclosures in `atone_xip_mt.py` and `audit_kappa.py`):

```
vMT(s) = cos(√2·s) on [−1/2, 1/2]

Iv  = ∫vMT   = √2·sin(1/√2)          = 0.91872536986556843778423152512466175181017247999457…
aMT = ∫vMT²  = ½ + sin(√2)/(2√2)     = 0.84922799931830417992129835162854794836529182414764…  (blueprint a)
bMT = ∫vMT⁴  = 3/8 + sin√2/(2√2) + sin(2√2)/(16√2) = 0.73784297545060818785290713144314417506871198524289…  (blueprint b)

vConv vMT r  = ½(1−r)cos(√2r) + sin(√2(1−r))/(2√2)   (r ∈ [0,1]), ≥ 0
2∫₀¹vConv vMT = (∫vMT)² = 0.8440563052346255265453520210914103583756…
  (= 2 sin²(1/√2) = 1 − cos(√2), consistent with the ‖(v²)′‖₁ blueprint row)

J1 = 2∫₀¹ D1trunc 9 r·vConv vMT r dr = 0.10633754139274846 ± 2·10⁻¹⁶
κ₉ = (aMT + J1)/(IvMT)² = 1.132111133800997 ± 2·10⁻¹⁶

ε₉ = 1024/2990212875 = 3.424505…×10⁻⁷   (D₁ tail; formally verified)

CERTIFIED:  κ₉ ≤ κ₁(1,vMT) ≤ κ₉ + ε₉         (κ₁ = 1/cWin(D₁,1,vMT))
  κ₁ ∈ [1.13211113380…, 1.13211147625…]
  canonical κ₁ = 1.132111134800948064449685289579659686777429502383…  ∈ sandwich ✓

H_xip = 2 − κ₁(1,vMT) ∈ [2 − (κ₉+ε₉), 2 − κ₉] = [0.8678885237…, 0.8678888662…]  ∋ canonical H
  canonical H = 0.8678888651990519355503147104203403132225704976166306446…
```

Flow of the sandwich (AtOne device):
`D1trunc9 ≤ D₁ ≤ D1trunc9 + ε₉` on [0,1]  ⟹ (multiply by vConv≥0, integrate ×2, use 2∫vConv=(∫v)²)
`J1 ≤ jWin(D₁,1,vMT) ≤ J1 + ε₉·(∫vMT)²`  ⟹
`κ₉ = (aMT+J1)/(∫v)² ≤ κ₁(1,vMT) = (aMT+jWin)/(∫v)² ≤ (aMT+J1)/(∫v)² + ε₉ = κ₉ + ε₉`.

Remark: for v_MT, ∫vMT, aMT and vConv are NOT rational (they contain sin/cos of √2), so κ₉ is a
real number enclosed to ~10⁻¹⁶ (≪ ε₉), not an exact rational as in the flat/quartic case.  The
Lean module therefore declares `kappaXiOne_MT := (aMT+J1MT)/(IvMT)²` as a real and proves the
interval membership `kappaXi 1 vMT ∈ Icc kappaXiOne_MT (kappaXiOne_MT + eps9)` conditional on
the closed-form/Fubini facts (honest bridge).
