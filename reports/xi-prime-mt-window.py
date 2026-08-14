import mpmath as mp

mp.mp.dps = 50

# ---- D1 series (Lean XiPrime/Defs.lean): D1(s) = s - 4s^2 + sum_{k>=0} D1coeff(k) s^{2k+3}
# D1coeff k = 2 * 4^(k+1) * k! / (2k+2)!
def D1(s):
    total = s - 4 * s**2
    k = 0
    while True:
        c = 2 * mp.mpf(4) ** (k + 1) * mp.factorial(k) / mp.factorial(2 * k + 2)
        term = c * s ** (2 * k + 3)
        if abs(term) < mp.mpf(10) ** (-45):
            break
        total += term
        k += 1
    return total

# ---- vConv(v, r) = int_{-1/2}^{1/2-r} v(s) v(s+r) ds
def vConv_num(v, r):
    if r < 0 or r > 1:
        return mp.mpf(0)
    return mp.quad(lambda s: v(s) * v(s + r), [-mp.mpf(1) / 2, mp.mpf(1) / 2 - r])

# ---- jWin(D, lam, v) = 2 * int_0^1 D(lam*r) * vConv(v, r) dr
def jWin(v, lam):
    return 2 * mp.quad(lambda r: D1(lam * r) * vConv_num(v, r), [0, 1])

# ---- cWin = lam * (int v)^2 / (int v^2 + lam * jWin); kappa = 1/cWin
def kappaXi(v, lam):
    Iv = mp.quad(lambda s: v(s), [-mp.mpf(1) / 2, mp.mpf(1) / 2])
    Iv2 = mp.quad(lambda s: v(s) ** 2, [-mp.mpf(1) / 2, mp.mpf(1) / 2])
    jw = jWin(v, lam)
    c = lam * Iv**2 / (Iv2 + lam * jw)
    return 1 / c

# ---- profiles
vFlat = lambda s: mp.mpf(1)
vQuartic = lambda s: 1 - mp.mpf(7) / 100 * (2 * s) ** 2 - mp.mpf(51) / 200 * (2 * s) ** 4
vMT = lambda s: mp.cos(mp.sqrt(2) * s)

for name, v in [("flat", vFlat), ("quartic", vQuartic), ("MT cos(sqrt2 s)", vMT)]:
    k1 = kappaXi(v, mp.mpf(1))
    print(f"{name}: kappa1 = {mp.nstr(k1, 20)}   2 - kappa1 = {mp.nstr(2 - k1, 20)}")

# reference: flat -> 2-kappa >= 0.85838371 (kappa ~ 1.1416163); quartic -> 0.86864017 (kappa ~ 1.1313598)
