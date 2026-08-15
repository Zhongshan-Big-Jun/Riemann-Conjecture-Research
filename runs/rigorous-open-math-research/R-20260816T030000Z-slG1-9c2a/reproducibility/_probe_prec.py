"""Probe precision of numerical integration methods for exact rational recognition of
sinc-power integrals. Goal: reach ~1e-12 relative so we can trust rational recognition.
Compare mpmath tanh-sinh on [-R,R] with large R (smooth away from origin, even).
"""
import mpmath as mp
mp.mp.dps=50

def sinc(t):
    t=mp.mpf(t)
    if abs(t)<mp.mpf('1e-16'): return mp.mpf(1)
    return mp.sin(mp.pi*t)/(mp.pi*t)

for n,exact in [(4,mp.mpf(2)/3),(6,mp.mpf(11)/20),(2,mp.mpf(1))]:
    print(f"=== c_{n} expect {mp.nstr(exact,20)} ===")
    for R in [40,80,160]:
        v=mp.quad(lambda t: sinc(t)**n, [-R,R])
        print(f"  R={R}: {mp.nstr(v,25)}  err={mp.nstr(abs(v-exact),5)}")
