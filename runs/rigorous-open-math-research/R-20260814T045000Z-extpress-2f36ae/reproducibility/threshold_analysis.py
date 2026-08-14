"""Find the exact threshold f* at which C_9(max rigorous m) exceeds the k=7 record.

C_9(f) = (H_MT - (m-1)/(500m)) / (1 - f*(m-8)/m),  m = 8 + (ceil(1/f)-1).
We solve for the smallest f > 0 with C_9(f) > 0.6730085279277797613.
"""
import mpmath as mp
mp.mp.dps = 60
H_MT = mp.mpf('1.5') - (1/mp.sqrt(2))*mp.cot(1/mp.sqrt(2))
TARGET = mp.mpf('0.6730085279277797613')

def max_m(k, fk):
    n = mp.ceil(mp.mpf(1)/fk) - 1
    return (k-1) + int(n)

def C9(f):
    m = max_m(9, f)
    A0 = f*(m-8)
    num = H_MT - mp.mpf(m-1)/(mp.mpf(500)*m)
    den = 1 - A0/m
    return num/den

# scan threshold
lo, hi = mp.mpf('0.0037'), mp.mpf('0.0040')
# find where C9 crosses TARGET via bisection on the smooth C_inf first (upper), then check actual
# actual C9 is piecewise constant between jumps of max_m. Just sample.
prev = None
for i in range(0, 501):
    f = lo + (hi-lo)*mp.mpf(i)/500
    c = C9(f)
    if prev is None:
        pass
    if prev is not None and prev < TARGET and c >= TARGET:
        print(f"crossing in [{mp.nstr(f, 10)}]: C9={mp.nstr(c,16)}")
    prev = c

# precise: the max_m jumps. Find candidate f values just below/above each jump.
print("\nm / f thresholds (where max_m changes):")
for n in range(250, 264):
    # n=ceil(1/f)-1 ranges; f in (1/(n+1), 1/n]
    pass

# Print C9 across n (=m-8) from 250 to 270
print("\n  n(=m-8)  m      f=~1/n        C9")
for n in range(245, 272):
    f_upper = mp.mpf(1)/n           # max f that yields this n (=ceil(1/f)-1 = n)
    # largest f with ceil(1/f)-1 = n  is f in (1/(n+1), 1/n]  -> max f ~ 1/n
    f = mp.mpf(1)/mp.mpf(n)
    m = 8+n
    A0 = f*n
    num = H_MT - mp.mpf(m-1)/(mp.mpf(500)*m)
    den = 1 - A0/m
    c = num/den
    print(f"  {n:>4} {m:>4}  {mp.nstr(f,8)}   {mp.nstr(c,16)}  {'>7' if c>TARGET else ''}")
