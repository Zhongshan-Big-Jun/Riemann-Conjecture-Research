"""O6: enumerate on-line zeros via mpmath.zetazero(n) (imaginary parts), count those with
height <= T, form N0(0,T)/N(T). N(T) by Riemann-von Mangoldt main term. NUMERICAL EVIDENCE only."""
import mpmath as mp
mp.mp.dps = 12

def N_T(T):
    return float(T/(2*mp.pi)*mp.log(T/(2*mp.pi)) - T/(2*mp.pi) + 7.0/8)

heights = {}
for k in range(1, 600):
    h = abs(mp.zetazero(k))
    heights[k] = h

# For each T, N0(0,T) = largest k with height <= T
def N0(T):
    cnt = 0
    for k, h in heights.items():
        if h <= T:
            cnt = k
    return cnt

for T in [50, 100, 200, 300, 500, 700]:
    # need heights up to T; if not enumerated, extend
    maxh = max(heights.values())
    if T > maxh:
        k = max(heights.keys())+1
        h = abs(mp.zetazero(k))
        while h <= T:
            heights[k] = h
            k += 1
            h = abs(mp.zetazero(k))
    n0 = N0(T)
    nm = N_T(T)
    print(f"T={T}: N0(0,T)={n0}, N(T)~{nm:.0f}, ratio={n0/nm:.6f}")
