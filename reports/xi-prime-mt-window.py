import mpmath as mp

mp.mp.dps = 120  # 2026-08-15: raised to 120; published values are digit-exact to this
# precision (reports/xi-prime-record-theorem.md, release-checklist.md exact forms).
# NOTE 1: keep ALL arithmetic in mpmath — int/float division (e.g. (m-1)/(500*m))
# contaminates results at 1e-16.
# NOTE 2: use the ANALYTIC vConv closed form (A2) instead of nested quadrature —
# nested mp.quad inside the jWin integrand produced ~1e-50 noise at dps=80 (observed
# divergence at digit ~56 between two runs).

# ---- D1 series (Lean XiPrime/Defs.lean): D1(s) = s - 4s^2 + sum_{k>=0} D1coeff(k) s^{2k+3}
# D1coeff k = 2 * 4^(k+1) * k! / (2k+2)!
def D1(s):
    total = s - 4 * s**2
    k = 0
    while True:
        c = 2 * mp.mpf(4) ** (k + 1) * mp.factorial(k) / mp.factorial(2 * k + 2)
        term = c * s ** (2 * k + 3)
        if abs(term) < mp.mpf(10) ** (-100):
            break
        total += term
        k += 1
    return total

# ---- vConv(v, r) = int_{-1/2}^{1/2-r} v(s) v(s+r) ds
# For v_MT(s) = cos(sqrt(2) s) this has the exact closed form (A2-verified):
#   vConv(r) = 1/2 * [(1-r) cos(sqrt(2) r) + sin(sqrt(2)(1-r))/sqrt(2)]
def vConvMT(r):
    if r < 0 or r > 1:
        return mp.mpf(0)
    sq2 = mp.sqrt(2)
    return mp.mpf(1) / 2 * ((1 - r) * mp.cos(sq2 * r) + mp.sin(sq2 * (1 - r)) / sq2)

# ---- jWin(D, v) = 2 * int_0^1 D1(r) * vConv(v, r) dr  (lam = 1)
def jWinMT():
    return 2 * mp.quad(lambda r: D1(r) * vConvMT(r), [0, 1])

# ---- kappa1 = 1/cWin for v_MT at lam = 1
def kappaXiMT():
    sq2 = mp.sqrt(2)
    Iv = mp.quad(lambda s: mp.cos(sq2 * s), [-mp.mpf(1) / 2, mp.mpf(1) / 2])
    Iv2 = mp.quad(lambda s: mp.cos(sq2 * s) ** 2, [-mp.mpf(1) / 2, mp.mpf(1) / 2])
    jw = jWinMT()
    return 1 / (Iv**2 / (Iv2 + jw))

# ---- cross-checks: flat / quartic reproduce the Lean-certified constants
# (20-digit sanity only -> run at dps=40 for speed; nested quadrature is fine here)
vFlat = lambda s: mp.mpf(1)
vQuartic = lambda s: 1 - mp.mpf(7) / 100 * (2 * s) ** 2 - mp.mpf(51) / 200 * (2 * s) ** 4
def kappaXi_num(v, dps=40):
    saved = mp.mp.dps
    mp.mp.dps = dps
    try:
        Iv = mp.quad(lambda s: v(s), [-mp.mpf(1) / 2, mp.mpf(1) / 2])
        Iv2 = mp.quad(lambda s: v(s) ** 2, [-mp.mpf(1) / 2, mp.mpf(1) / 2])
        jw = 2 * mp.quad(lambda r: D1(r) * mp.quad(lambda s: v(s) * v(s + r),
                         [-mp.mpf(1) / 2, mp.mpf(1) / 2 - r]), [0, 1])
        return 1 / (Iv**2 / (Iv2 + jw))
    finally:
        mp.mp.dps = saved
for name, v in [("flat", vFlat), ("quartic", vQuartic)]:
    k1 = kappaXi_num(v)
    print(f"{name}: 2 - kappa1 = {mp.nstr(2 - k1, 20)}   (Lean: >= 0.85838371 / >= 0.86864017)")

# ---- authoritative values (dps=120, 2026-08-15)
k1mt = kappaXiMT()
Hmt = 2 - k1mt
print()
print("AUTHORITATIVE (dps=120, analytic vConv):")
print("kappa1(1, v_MT) =", mp.nstr(k1mt, 100))
print("H_xip_MT        =", mp.nstr(Hmt, 100))
print("C9xip(0.0039)   =", mp.nstr((2640000 * Hmt - 5260) / mp.mpf(2630016), 90))
print("C9xip(0.00395)  =", mp.nstr((26100000 * Hmt - 52000) / mp.mpf(26000065), 90))
print("C9xip(0.00398)  =", mp.nstr((25900000 * Hmt - 51600) / mp.mpf(25800102), 90))

# reference: flat -> 2-kappa >= 0.85838371 (kappa ~ 1.1416163); quartic -> 0.86864017 (kappa ~ 1.1313598)
