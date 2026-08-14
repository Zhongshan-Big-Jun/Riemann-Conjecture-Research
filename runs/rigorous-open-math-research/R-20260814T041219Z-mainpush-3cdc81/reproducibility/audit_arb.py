"""Correct Arb audit: H_MT and c1* from their closed forms, exact-ish.
"""
from flint import arb, ctx
ctx.prec = 250

sq2 = arb(2).sqrt()
inv_sq2 = (1/sq2)

# H_MT = 3/2 - (1/sqrt2) * cot(1/sqrt2) = 3/2 - (1/sqrt2)*cos(1/sqrt2)/sin(1/sqrt2)
x = inv_sq2
cot_x = (1/x).tan()   # WRONG: (1/x) is 1/sqrt2; .tan() gives tan(1/sqrt2). cot=1/tan.
# do correctly:
cotx = 1 / x.tan()
H_MT = arb("1.5") - (1/sq2) * cotx
print("H_MT Arb    :", H_MT)
print("mpmath value: 0.6725007036794116457343797908032951885934030")

# c1* satisfies 1/c1* = 1/2 + (1/sqrt2)*cot(1/sqrt2)  (Claude 7.4 / [Mon75, CG93])
inv_c1 = arb("0.5") + (1/sq2)*cotx
print("1/c1* Arb   :", inv_c1)
c1 = 1/inv_c1
print("c1* Arb     :", c1, " (claimed 0.7532960...)")
print("2-1/c1*     :", arb(2)-inv_c1)
print("H_MT overlap with 2-1/c1*:", bool(H_MT.overlaps(arb(2)-inv_c1)))
print("2-1/c1* contains claim 0.6725007036794116:", bool((arb(2)-inv_c1).contains(arb("0.672500703679411645734379790803295188593403"))))
