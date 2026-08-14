import mpmath as mp

mp.mp.dps = 120

# 1. H_MT = 3/2 - (1/sqrt(2)) * cot(1/sqrt(2))
x = 1 / mp.sqrt(2)
H_MT = mp.mpf(3) / 2 - x * mp.cot(x)
print("H_MT            =", H_MT)
print("H_MT 50dp       =", mp.nstr(H_MT, 50))

# c1 such that 2 - 1/c1 = H_MT
c1 = 1 / (2 - H_MT)
print("c1              =", mp.nstr(c1, 50))
print("2 - 1/c1 - H_MT =", mp.nstr(2 - 1 / c1 - H_MT, 30), "(should be 0)")

# 2. Draft constant: (1,345,000*H_MT - 2,680)/1,340,003
C7 = (mp.mpf(1345000) * H_MT - 2680) / mp.mpf(1340003)
print("C7 (draft)      =", mp.nstr(C7, 50))
print("C7 - 0.6730085279277797613 =", mp.nstr(C7 - mp.mpf("0.6730085279277797613"), 30))

# 3. General-k ceiling formula c(m) = (H_MT - (m-1)/(500m)) / (1 - 19(m-6)/(5000m)); m=269
m = 269
c269 = (H_MT - (m - 1) / (500 * m)) / (1 - mp.mpf(19) * (m - 6) / (5000 * m))
print("c(269)          =", mp.nstr(c269, 50))
print("c(269) - C7     =", mp.nstr(c269 - C7, 30), "(should be ~0)")
# consistency of the numerator/denominator rearrangement
print("268/134500      =", mp.nstr(mp.mpf(268) / 134500, 30), "  (m-1)/(500m) at m=269 =", mp.nstr((m-1)/(500*m), 30))
print("4997/1345000    =", mp.nstr(mp.mpf(4997) / 1345000, 30), "  19(m-6)/(5000m) at m=269 =", mp.nstr(mp.mpf(19)*(m-6)/(5000*m), 30))
# A0 <= 1 condition: 19(m-6)/5000 <= 1 -> m <= 5000/19 + 6
print("m_max(A0<=1)    =", mp.nstr(mp.mpf(5000)/19 + 6, 30), "-> m <= 269")

# 4. Formal limit (H_MT - 1/500)/(1 - 19/5000)
lim = (H_MT - mp.mpf(1) / 500) / (1 - mp.mpf(19) / 5000)
print("class limit     =", mp.nstr(lim, 50))
print("limit - 0.6730583 =", mp.nstr(lim - mp.mpf("0.6730583"), 30))

# 5. 3-point constant (H_MT - eps/4)/(1 - eps/2), eps = 221/10^6
eps = mp.mpf(221) / 10**6
C3 = (H_MT - eps / 4) / (1 - eps / 2)
print("C3 (3-point)    =", mp.nstr(C3, 50))
print("C3 - 0.6725197671136777071 =", mp.nstr(C3 - mp.mpf("0.6725197671136777071"), 30))

# 6. Moment-sequence sanity: m0=1, m1=1, m2=3/4, m3=2, m4=13/4
# A positive measure with mass 1 and mean 1 must have m2 >= m1^2 = 1. Here m2 = 3/4 < 1.
# Hankel determinants:
M2 = mp.matrix([[1, 1], [1, mp.mpf(3)/4]])
M3 = mp.matrix([[1, 1, mp.mpf(3)/4], [1, mp.mpf(3)/4, 2], [mp.mpf(3)/4, 2, mp.mpf(13)/4]])
print("det M2          =", mp.nstr(mp.det(M2), 30), "(negative -> NOT a positive-measure moment sequence)")
print("det M3          =", mp.nstr(mp.det(M3), 30))
# variance m2 - m1^2
print("m2 - m1^2       =", mp.nstr(mp.mpf(3)/4 - 1, 30), "(negative -> impossible for a probability measure)")
