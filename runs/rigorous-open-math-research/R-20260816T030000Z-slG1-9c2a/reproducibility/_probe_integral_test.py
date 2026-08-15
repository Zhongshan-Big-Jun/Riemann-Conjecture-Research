"""Probe: gauge reachable precision for direct mpmath integration of the
translation-invariant shape integrals (exact infinite-volume sinc), before committing
to the full m_5 shape sum. Validates the {(12),(3)} shape of m_3 = c2-c4 = 1/3 and
c4=int sinc^4 = 2/3 at high precision. Also checks the exact box-spline numbers.
"""
import mpmath as mp

mp.mp.dps = 60

def sinc(t):
    t = mp.mpf(t)
    if mp.fabs(t) < mp.mpf("1e-14"):
        return mp.mpf(1)
    return mp.sin(mp.pi*t)/(mp.pi*t)

# c_4 = ∫ sinc^4 = 2/3 ; c2=1 ; test one 2-D shape: ∫ K^2 - K^4  (pattern {12}{3} of m3)
c4 = mp.quad(lambda t: sinc(t)**4, [-mp.inf, mp.inf])
print("c4 =", mp.nstr(c4, 40), " expect 2/3 ", mp.nstr(mp.mpf(2)/3, 40))
c2 = mp.quad(lambda t: sinc(t)**2, [-mp.inf, mp.inf])
print("c2 =", mp.nstr(c2, 40), " expect 1")
# higher c's
for n,val in [(8,"151/315"),(10,"15619/36288")]:
    v = mp.quad(lambda t: sinc(t)**n, [-mp.inf, mp.inf])
    print(f"c{n} =", mp.nstr(v, 40), f" expect {val}", mp.nstr(mp.mpf(val),40))

# Now the 2-D shape scalar: integral over (x,y) of [1-K(x-y)^2]*K(x-y)^2 = c2 - c4
# In translation-invariant form with x1=0: ∫_R K(t)^2(1-K(t)^2) dt  -- that's just c2-c4, single integral.
print("\npattern {12}{3} scalar =", mp.nstr(c2-c4,40), " expect 1/3")
