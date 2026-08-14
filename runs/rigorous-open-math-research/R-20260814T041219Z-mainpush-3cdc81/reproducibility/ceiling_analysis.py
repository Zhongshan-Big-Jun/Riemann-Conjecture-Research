"""Analyze the true ceiling of the trace-defect class (O3/O4).

Key quantities for the Montgomery-Taylor normalized kernel k(x):
  w(x) = k(x)^2
  W := integral_0^infty w(x) dx   (full second moment, pair-correlation weight)

For a large normalized interval of length ~N (mean spacing 1, N zeros),
the total pair weight  sum_{pairs} w(x_i-x_j) ~ N * W  (2 * W per zero because
each zero pairs with ~N others, giving W per zero on average... actually
sum_{i<j} w ~ (1/2) * int 1_{|x|<L} int density^2 w dx du ~ (N^2/L)*W ~ N*W/1 ... we
normalize density so total pairs ~ N W).  We then place the per-zero defect budget.

We compute W numerically to estimate how much defect (tr Psi(M)) is available at all.
Also compute the Fourier transform |k_hat| and its support to compare with bandwidth-one.
"""
import mpmath as mp
mp.mp.dps = 50

sq2 = mp.sqrt(2)
# kernel on normalized variable x (paper's k(x) = K(x)/K(0))
def k(x):
    a = mp.pi*x - 1/sq2
    b = mp.pi*x + 1/sq2
    if mp.almosteq(x, 0):
        K = 0
        # K(0) = sqrt2 sin(1/sqrt2); K(x)->K(0) as x->0
    a0 = 1/sq2
    K0 = sq2*mp.sin(1/sq2)
    if abs(x) < mp.mpf('1e-9'):
        return K0/K0  # k(0)=1 by normalization? Actually k(0)=K(0)/K(0)=1
        # but wait, sinc(0)... need limit. K(0)=sqrt2 sin(1/sqrt2). and formula
    Ka = mp.sin(a)/a
    Kb = mp.sin(b)/b
    K = (Ka+Kb)/2
    return K/K0

# verify k(0)
a0=1/sq2; K0=sq2*mp.sin(1/sq2)
print("K(0) =", mp.nstr(K0, 30))
print("k(0) limit (sinc sin(a)/a with a=... )")

# compute W = integral_0^infty k(x)^2 dx via mpmath quad, truncating
def w(x):
    return k(x)**2

# Integrate with split at around where oscillatory tail begins
parts = []
# sample values to understand decay
for x in [0,0.5,1,1.5,2,2.5,3,4,5,6,8,10,15,20,30]:
    try:
        print(f"x={x}: w={mp.nstr(w(x),12)}")
    except Exception as e:
        print(x, "err", e)

# Numerical integration using mpmath quad on intervals
W = mp.quad(w, [0, mp.inf])
print("\nW = integral_0^inf k(x)^2 dx =", mp.nstr(W, 30))

# Also compute via its Fourier: by Plancherel W_full = integral x ... ; here on [0,inf)
# (for even k, integral_-inf^inf k^2 = 2W)
Wfull = mp.quad(w, [-mp.inf, mp.inf])
print("int_-inf^inf k^2 =", mp.nstr(Wfull, 30))

# Bandwidth: k_hat support. k is the (2/?)-bandlimited? K = overlap kernel of cos(sqrt2 .)
# Its Fourier transform k_hat(u) is supported where? K(x)=conv of cos window => supp k_hat subset [-sqrt2/(2pi)*??]
# Actually phi_hat of cos window has support [-sqrt2/(2pi), sqrt2/(2pi)] in frequency => bandwidth_one,
# i.e. support in [-1,1] after normalization by mean spacing. Confirm numerically below via sampling.
