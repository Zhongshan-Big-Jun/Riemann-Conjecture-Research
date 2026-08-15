"""Verify the exact moment decomposition reproduces m_2=4/3, m_3=2, m_4=13/4 from the shape
algebra (probe report section 2), establishing the exact framework we extend to m_5/m_6.
Then print the required integral classes for m_5 (B-spline constants and star integrals).

The decomposition (probe): with c_{2n}=∫sinc^{2n}, S_3=star, D_k=all-distinct:
  m_2 = 1 + (c_2 - c_4)
  m_3 = 1 + 3(c_2 - c_4) + D_3
  m_4 = 1 + 4(c_2 - c_4) + 2(c_2 - c_4) + (c_4 - c_6) + 2 S_3 + D_4
with c_2=1, c_4=2/3, c_6=11/20, S_3=1/15.
(EVIDENCE that D_3=D_4=0 makes the exact list; the shape coefficients are audit-level.)
"""
from fractions import Fraction as F

c2 = F(1); c4 = F(2,3); c6 = F(11,20); S3 = F(1,15)

m2 = 1 + (c2 - c4)
m3 = 1 + 3*(c2-c4) + F(0)          # D_3 = 0
m4 = 1 + 4*(c2-c4) + 2*(c2-c4) + (c4-c6) + 2*S3 + F(0)   # D_4 = 0
print("m_2 =", m2, "=", float(m2), "(expect 4/3,", m2==F(4,3), ")")
print("m_3 =", m3, "=", float(m3), "(expect 2,", m3==F(2), ")")
print("m_4 =", m4, "=", float(m4), "(expect 13/4,", m4==F(13,4), ")")

print("\nB-spline constants needed for m_5 (order up to c_10) and star terms:")
# c_8, c_10 computed numerically via box-spline (B_{2n}(0)) using mpmath high precision:
import mpmath as mp
mp.mp.dps = 40
def s(t):  # normalized sinc: sin(pi t)/(pi t)
    return mp.sin(mp.pi*t)/(mp.pi*t)
for n in [1,2,3,4,5]:
    v = mp.quad(lambda t: s(t)**(2*n), [-mp.inf, mp.inf])
    print(f"  c_{2*n} = {mp.nstr(v, 25)}")
print("  (c_2=1, c_4=2/3, c_6=11/20 exact per probe; c_8, c_10 are the next B-spline values.)")
