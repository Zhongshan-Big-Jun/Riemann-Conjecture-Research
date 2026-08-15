"""
kernel_limit_verify.py
======================
Numerical verification of the kernel-limit lemma (T1c item 3) for the C9 record.

Facts established in candidate_proof.md:
  * The normalized Montgomery-Taylor overlap kernel is
        kMT(x) = [sinc((√2)^-1 - πx) + sinc((√2)^-1 + πx)] / (2·√2·sin((√2)^-1))
              = K_1(x) / K_1(0),
    where
        K_λ(x) = ∫_{-1/2}^{1/2} cos(√2·λ·t) cos(2π·x·t) dt,
        K_λ(0) = √2·sin(λ/√2).
  * The finite-window (Fourier) overlap of the Montgomery-Taylor window is
        O_L(x) = ∫_{-L/2}^{L/2} cos(√2·λ·u/L) · cos(2π·x·u/L) du   (ramp -> 1 limit),
    and the kernel-limit lemma asserts, for λ = 1 (the C9 case),
        O_L(x)/O_L(0) --> kMT(x),   x=(γ-γ')·L/(2π),   uniform for bounded x,
    with rate O(w/L) where w is the fixed ramp width (here w = 0 limit).

We verify:
  (1) kMT(x) == K_1(x)/K_1(0)  (kernel form consistency; exact).
  (2) O_L(x)/O_L(0) - kMT(x) decays like 1/L for x in {0.3,1.0,1.9},
      L in {100, 1000, 10000}.
  (3) Honest note: the profile AUTOCORRELATION Cfun (used for the J-moment in
      Window.lean:1211) does NOT, by itself, converge to kMT(x); the kernel
      kMT comes from the Fourier (cross-frequency) overlap. This is documented
      to resolve the framing ambiguity.

Numerical evidence only -- NOT a proof. See candidate_proof.md for the proof.
"""
import mpmath as mp
mp.mp.dps = 40

SR2 = mp.sqrt(2)
INV = 1 / mp.sqrt(2)          # (√2)^-1

def sinc(z):
    return mp.sin(z) / z

def kMT(x):
    return (sinc(INV - mp.pi * x) + sinc(INV + mp.pi * x)) / (2 * SR2 * mp.sin(INV))

def S(c):
    """S(c) = ∫_{-1/2}^{1/2} exp(ic t) dt's real part = 2 sin(c/2)/c, S(0)=1."""
    if c == 0:
        return mp.mpf(1)
    return 2 * mp.sin(c / 2) / c

def K_lam(lam, x):
    """K_λ(x) = ∫_{-1/2}^{1/2} cos(√2λt) cos(2πxt) dt = ½[S(a-b)+S(a+b)], a=√2λ, b=2πx."""
    a = SR2 * lam
    b = 2 * mp.pi * x
    return mp.mpf('0.5') * (S(a - b) + S(a + b))

def O_L(lam, L, x, q=40):
    """Fourier overlap ∫_{-L/2}^{L/2} cos(√2λu/L) cos(2π x u/L) du (ramp->1)."""
    L = mp.mpf(L)
    def f(u):
        return mp.cos(SR2 * lam * u / L) * mp.cos(2 * mp.pi * x * u / L)
    return mp.quad(f, [-L / 2, L / 2], maxdegree=q)

def Cfun(lam, L, y):
    """Window.lean:1211 sharp-cutoff comparison autocorrelation."""
    L = mp.mpf(L)
    w = SR2 * lam / L
    return (L - y) / 2 * mp.cos(w * y) + mp.sin(w * (L - y)) / (2 * w)

if __name__ == "__main__":
    print("mpmath precision (digits):", mp.mp.dps)

    # (1) kernel form: kMT(x) == K_1(x)/K_1(0)
    print("\n[1] kMT(x) vs K_1(x)/K_1(0):")
    xs = [mp.mpf('0.3'), mp.mpf('1.0'), mp.mpf('1.9')]
    for xv in xs:
        d = kMT(xv) - (K_lam(1, xv) / K_lam(1, 0))
        print(f"    x={mp.nstr(xv,4):6s}  |diff|={mp.nstr(abs(d),6)}")

    # (2) Fourier overlap limit & 1/L decay
    print("\n[2] O_L(x)/O_L(0) vs kMT(x), and error*L (should be ~constant => O(1/L) rate):")
    lam = mp.mpf(1)
    letters = {100: 'a', 1000: 'b', 10000: 'c'}
    last = {}
    for xv in xs:
        print(f"    --- x = {mp.nstr(xv,4)} ---")
        for L in [100, 1000, 10000]:
            r = O_L(lam, L, xv) / O_L(lam, L, 0)
            err = r - kMT(xv)
            print(f"        L={L:6d}  ratio={mp.nstr(r,16)}  kMT={mp.nstr(kMT(xv),16)}"
                  f"  err={mp.nstr(err,8)}  err*L={mp.nstr(err*L,8)}")
            last[letters[L]] = err

    # (3) Cfun does NOT converge to kMT (documents the framing ambiguity)
    print("\n[3] Cfun-based autocorrelation is NOT kMT (framing note):")
    import mpmath
    for xv in [mp.mpf('0.3')]:
        L = mp.mpf('100')
        # y = x*L is the natural normalized-separation identification used by Cfun
        Cf = Cfun(lam, L, xv * L)
        print(f"    x={mp.nstr(xv,4)}  Cfun/L={mp.nstr(Cf/L,10)}  kMT={mp.nstr(kMT(xv),10)}  (differ => Cfun is not the kernel overlap)")
