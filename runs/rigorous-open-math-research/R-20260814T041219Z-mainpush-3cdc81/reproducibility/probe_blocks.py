"""O3 probe: effect of block length m on the stability-refinement constant.

Derivation reproduced independently (see ledger):
If for an m-point block we have the local inequality
   E_m + (1/500)(y_m - y_1) >= (19/5000)(m-6)   [this holds for ALL m>=7 by the
   block-energy lemma summing F6 >= 19/5000 over (m-6) seven-point windows]
then the block-averaging defect argument gives
   D(M^o) >= (A0/m) S - (m-1)/(500m) N - o(N),   A0 = (19/5000)(m-6)
and hence  liminf S/N >= [H_MT - (m-1)/(500m)] / [1 - 19(m-6)/(5000m)].

Compute c(m) for m = 7..large, find the max, and check whether it exceeds
the OpenAI 269-block value 0.6730085 and where the ceiling is.
"""
import mpmath as mp
mp.mp.dps = 60

H_MT = mp.mpf('1.5') - (1/mp.sqrt(2))*mp.cot(1/mp.sqrt(2))

def c_of_m(m):
    A0 = mp.mpf(19)*mp.mpf(m-6)/mp.mpf(5000)
    num = H_MT - mp.mpf(m-1)/(mp.mpf(500)*mp.mpf(m))
    denom = 1 - A0/m
    return num/denom

prev = None
best = (0, None)
print(f"{'m':>6} {'c(m)':>20} {'delta':>12}")
for m in range(7, 3001):
    cm = c_of_m(m)
    delta = '' if prev is None else mp.nstr(cm-prev, 6)
    if delta and abs(cm-prev) < 1e-9 and prev>0:
        pass
    if cm > best[0]:
        best = (cm, m)
    if m <= 20 or m in (30,50,100,200,269,400,500,700,1000,1500,2000,2690,3000):
        print(f"{m:>6} {mp.nstr(cm,18):>20} {delta}")
    prev = cm

print("\nbest c(m) value      =", mp.nstr(best[0], 18), "at m=", best[1])
print("OpenAI m=269 value   =", mp.nstr(c_of_m(269), 18))
print("bandwidth-one ceiling= 0.6818287...")
print("exceeds 0.6818287 ?  ", best[0] > mp.mpf('0.6818287'))

# What is the asymptotic ceiling as m -> infinity?
# A0/m -> (19/5000), (m-1)/(500m) -> 1/500
c_inf = (H_MT - mp.mpf(1)/mp.mpf(500)) / (1 - mp.mpf(19)/mp.mpf(5000))
print("asymptotic ceiling m->inf =", mp.nstr(c_inf, 18))
