"""General-k derivation of the pressure-method constant C_k.

Reproduces k=3 (triangle mechanism) and k=7 (block-pressure mechanism), and
exposes C_k(m) / C_k_infinity as a function of the certified k-point pressure
value f_k and the block parameter m.

Block-pressure mechanism (k >= 3): k consecutive zeros, k-1 nonneg gaps.
  F_{k-1}(g) = 1/(500(k-1)) * sum_i g_i
             + sum_{s=1}^{k-1} (2/(k-s)) * sum_{i=1}^{k-s} w(g_i+...+g_{i+s-1})
  Certified: F_{k-1} >= f_k  (f_7 = 19/5000).
  Block-energy (m ordered points): E_m + (1/500)(y_m-y_1) >= f_k*(m-k+1).
  A0 = f_k*(m-k+1) < 1 required (Lemma 4.3 min{1,.} device).
  Max rigorous m_k = (k-1) + n_max, n_max = largest int with f_k*n < 1.
  Defect: D(M^o) >= (A0/m_k) S - (m_k-1)/(500*m_k) N - o(N).
  Constant: C_k = (H_MT - (m_k-1)/(500*m_k)) / (1 - A0/m_k).
  Formal class limit (m->inf, needs uncontrolled large-block monotonicity):
  C_inf = (H_MT - 1/500) / (1 - f_k).

Triangle mechanism (k=3): eps_4 = min{ w(u)+w(v)+w(u+v) : u,v>=0,u+v<=4 }.
  Bound = (H_MT - eps_4/4)/(1 - eps_4/2).
"""
import mpmath as mp
mp.mp.dps = 60

H_MT = mp.mpf('1.5') - (1/mp.sqrt(2))*mp.cot(1/mp.sqrt(2))

def max_m(k, fk):
    """Largest m with fk*(m-k+1) < 1 (A0 < 1 device)."""
    # need integer n = m-k+1 >= 1 with fk*n < 1; largest is ceil(1/fk)-1
    n = mp.ceil(mp.mpf(1)/fk) - 1
    # verify
    assert fk*n < 1 and fk*(n+1) >= 1, (fk, n)
    return (k-1) + int(n)

def C_k_at(m, k, fk):
    A0 = fk*(m - k + 1)
    num = H_MT - mp.mpf(m-1)/(mp.mpf(500)*m)
    den = 1 - A0/m
    return num/den

def C_inf(fk):
    return (H_MT - mp.mpf(1)/mp.mpf(500))/(1 - fk)

print("H_MT =", mp.nstr(H_MT, 20))
print()

# ---- k=7 verification -----------------------------------------------------
f7 = mp.mpf(19)/mp.mpf(5000)
k7, m7 = 7, 269
A0_7 = f7*(m7 - k7 + 1)
print("k=7: f_7 =", mp.nstr(f7, 10), " A0 =", mp.nstr(A0_7, 20), " (<1:", A0_7<1, ")")
print("     max rigorous m_7 =", max_m(7, f7), " (expected 269)")
print("     C_7(m=269) =", mp.nstr(C_k_at(269, 7, f7), 22), " (expected 0.6730085279277797613)")
print("     C_7 class limit =", mp.nstr(C_inf(f7), 22), " (expected ~0.673058...)")
print("     ratio check (m-1)/(500m) =", mp.nstr(mp.mpf(268)/mp.mpf(134500), 12))
print()

# ---- k=3 verification (triangle mechanism) --------------------------------
eps4 = mp.mpf(221)/mp.mpf(1000000)
C3 = (H_MT - eps4/4)/(1 - eps4/2)
print("k=3: triangle bound =", mp.nstr(C3, 22), " (expected 0.6725197671136777071)")
print()

# ---- class limit threshold: what f_k is needed ---------------------------
# The k=7 certificate value 0.6730085279277797613.
target = mp.mpf('0.6730085279277797613')
# When does the CLASS LIMIT C_inf(f) exceed target?
import itertools
def f_needed_for_limit(C):
    # (H-0.002)/(1-f) > C  =>  1 - f < (H-0.002)/C  =>  f > 1 - (H-0.002)/C
    return 1 - (H_MT - mp.mpf(1)/mp.mpf(500))/C
print("for class-limit to exceed 0.673008528 need f_k >", mp.nstr(f_needed_for_limit(target),12))
print("   (f_7 = 19/5000 =", mp.nstr(f7,8),")")
print()

# ---- probe C_k for a range of hypothetical f_k ---------------------------
print("Hypothetical probe (k=9):  max m and C_9(m) vs f_9")
for f in [mp.mpf('0.0037'), mp.mpf('0.0038'), mp.mpf('0.0040'),
          mp.mpf('0.0042'), mp.mpf('0.0045'), mp.mpf('0.0050')]:
    m = max_m(9, f)
    c = C_k_at(m, 9, f)
    print(f"   f_9={mp.nstr(f,7)}  m_9={m}  A0={mp.nstr(f*(m-8),8)}  C_9={mp.nstr(c,18)} "
          f" limit={mp.nstr(C_inf(f),12)}  beats7={c>target}")
