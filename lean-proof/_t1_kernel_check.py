"""T1 repair re-audit: independent numeric check of the Lean kMT formula vs the
certificate integral K(x)/K(0). Uses mpmath. Independent of the formalizer."""
import mpmath as mp

mp.mp.dps = 50

SQ2 = mp.sqrt(2)
INV_SQ2 = 1 / SQ2          # (sqrt2)^-1 == sqrt2/2
PI = mp.pi

def sinc(z):
    # guarded sinc: sin z / z, sinc(0)=1
    if z == 0:
        return mp.mpf(1)
    return mp.sin(z) / z

def K_integral(x):
    """K(x) = integral_{-1/2}^{1/2} cos(sqrt2 t) cos(2pi x t) dt"""
    f = lambda t: mp.cos(SQ2 * t) * mp.cos(2 * PI * x * t)
    return mp.quad(f, [-mp.mpf('0.5'), mp.mpf('0.5')])

def K_zero():
    return K_integral(0)

def lean_kMT(x):
    # Guarded sinc == arblib .sinc() for x != 0; our x-grid avoids the removable poles,
    # so no guard needed for the comparisons we record (all sample x give nonzero args).
    a = INV_SQ2 - PI * x
    b = INV_SQ2 + PI * x
    denom = SQ2 * mp.sin(INV_SQ2)
    return (sinc(a) + sinc(b)) / 2 / denom

zs = list(map(mp.mpf, [0, 0.3, 0.9, 1.0, 1.5, 2.0]))
k0 = K_zero()
print(f"k_zero (integral K(0)) = {mp.nstr(k0, 20)}")
print(f"cert k_zero sqrt2*sin(1/sqrt2) = {mp.nstr(SQ2*mp.sin(INV_SQ2), 20)}")
print(f"ratio = {mp.nstr(k0/(SQ2*mp.sin(INV_SQ2)), 20)}")

print("\n  x      integral K(x)/K(0)      Lean-kMT formula         agreement(digits)")
hdr = True
worst = mp.mpf('1e99')
for x in zs:
    kint = K_integral(x) / k0
    klyn = lean_kMT(x)
    diff = abs(kint - klyn)
    if kint != 0:
        digits = -mp.log10(diff / abs(kint)) if diff > 0 else mp.inf
    else:
        digits = mp.inf
    if digits < worst:
        worst = digits
    print(f"{mp.nstr(x,4):>6}   {mp.nstr(kint,18):>14}   {mp.nstr(klyn,18):>14}   {mp.nstr(digits,6)}")

print(f"\nWORST agreement (digits): {mp.nstr(worst,6)}")
assert worst > 12, "FAIL: less than 12-digit agreement"

# wMT(0) = kMT(0)^2 == 1
w0 = lean_kMT(0)**2
print(f"\nwMT(0) = kMT(0)^2 = {mp.nstr(w0, 20)}")
assert abs(w0 - 1) < mp.mpf('1e-30'), "wMT(0) != 1"

# Also check the integral equals the sinc closed form symbolically-consistently at x=0:
# K(0) = int cos(sqrt2 t) dt over [-1/2,1/2] = 2 sin(sqrt2/2)/sqrt2 = (sqrt2) sin(1/sqrt2)
K0_analytic = SQ2 * mp.sin(INV_SQ2)
print(f"K(0) integral = {mp.nstr(k0,20)}, analytic sqrt2 sin(1/sqrt2) = {mp.nstr(K0_analytic,20)} diff={mp.nstr(abs(k0-K0_analytic),20)}")
assert abs(k0 - K0_analytic) < mp.mpf('1e-30')

print("\nALL NUMERIC CHECKS PASSED")
