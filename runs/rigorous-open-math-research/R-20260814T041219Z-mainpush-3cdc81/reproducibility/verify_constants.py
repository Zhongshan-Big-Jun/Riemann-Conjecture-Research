"""Independent verification of the OpenAI draft's claimed constants (O2).

Computes, with high-precision (mpmath, >= 200 dp):
  * H_MT = 3/2 - (1/sqrt(2)) * cot(1/sqrt(2))
  * c_1 such that 2 - 1/c_1 = H_MT
  * three-point bound (H_MT - eps/4)/(1 - eps/2) with eps = 221/1e6
  * seven-point bound (1345000 H_MT - 2680)/1340003
Outputs both the claimed decimals from the paper and independently computed values.
Also verifies the algebraic identity min_{n>=0}[(p-n)^2 + 4n] = 2p-1+Psi(p).
"""
import mpmath as mp

mp.mp.dps = 250

sq2 = mp.sqrt(2)
H_MT = mp.mpf(3)/2 - (mp.mpf(1)/sq2) * mp.cot(mp.mpf(1)/sq2)
print("H_MT          =", mp.nstr(H_MT, 40))
print("claimed H_MT  = 0.6725007036794116...")

inv_c1 = mp.mpf(2) - H_MT
c1 = 1/inv_c1
print("c1            =", mp.nstr(c1, 40))
print("1/c1          =", mp.nstr(inv_c1, 40))
print("2 - 1/c1      =", mp.nstr(mp.mpf(2) - inv_c1, 40))


def three_point(eps):
    return (H_MT - eps/4)/(1 - eps/2)

eps3 = mp.mpf(221)/mp.mpf(10**6)
b3 = three_point(eps3)
print("three_point   =", mp.nstr(b3, 40), "(claimed 0.672519767)")
# percentage
print("  as %%        =", mp.nstr(b3*100, 30))

b7 = (mp.mpf(1345000)*H_MT - mp.mpf(2680))/mp.mpf(1340003)
print("seven_point   =", mp.nstr(b7, 40), "(claimed 0.6730085279277...)")
print("  as %%        =", mp.nstr(b7*100, 30))

# Verify identity min_{n>=0}[(p-n)^2+4n] = 2p-1+Psi(p)
print("\nChecking Psi identity at several p:")
for pr in ["0.0","0.5","1.0","1.5","1.99","2.0","2.5","4.0","10.0"]:
    p = mp.mpf(pr)
    if 0<=p<=2:
        Psi = (p-1)**2
        expected = p**2
    else:
        Psi = 2*p-3
        expected = 4*p-4
    rhs = 2*p-1+Psi
    # numerical min
    # derivative of (p-n)^2+4n w.r.t n is -2(p-n)+4 = 2n -2p +4, zero at n=p-2
    n_opt = max(mp.mpf(0), p-2)
    lhs = (p-n_opt)**2 + 4*n_opt
    assert abs(lhs-expected) < mp.mpf("1e-200")
    assert abs(lhs-rhs) < mp.mpf("1e-200")
    print(f"  p={p}: min={(mp.nstr(lhs,20))}  2p-1+Psi={mp.nstr(rhs,20)}  OK")

# Verify the X<=... <= chain: s_1 + 2 s_2 + 2 p <= N(I')
# (structural: checked in paper; nothing numeric here)

# Verify 4997/5000 < 1 and 0.6730085... constants
A0 = mp.mpf(4997)/mp.mpf(5000)
m = 269
print("\nA0 =", mp.nstr(A0, 30))
print("(m-6)*19/5000 =", mp.nstr(mp.mpf(19)*mp.mpf(m-6)/mp.mpf(5000), 30))
print("A0/m =", mp.nstr(A0/m, 30))
print("(m-1)/(500*m) =", mp.nstr(mp.mpf(m-1)/(mp.mpf(500)*m), 30))
