# -*- coding: utf-8 -*-
"""
audit_kappa.py — INDEPENDENT cross-check (EVIDENCE, not the certificate) of
κ₁(1, vMT) and H = 2 − κ₁, computed by a SEPARATE code path (mpmath native, no flint/arb,
no sympy), and checked against:
  (a) the canonical dps=120 value H_xip_MT = 0.8678888651990519355503147104203403132225704976166306446…
      (reports/xi-prime-mt-window.py, analytic vConv closed form),
  (b) the ADM sandbox ARB enclosure produced by atone_xip_mt.py:
         κ₉ ∈ [kappa9_lo, kappa9_hi],  κ₁(1,vMT) ∈ [kappa9_lo, kappa9_hi + eps9].
The goal is to confirm the derived sandwich actually CONTAINS the canonical value (it does),
lending confidence the certified rational bounds are on the correct side.

EVIDENCE ONLY — this file uses mpmath quadrature for the integral, which is numerical
evidence, not a rigorous bound.  The rigorous certificate is atone_xip_mt.py (Arb intervals).
"""
import json, math
import mpmath as mp

mp.mp.dps = 120
STATUS = "FINITE_COMPUTATIONAL_RESULT"

# ---- the canonical constants (read from the reported authoritative run)
CANON_H = mp.mpf('0.8678888651990519355503147104203403132225704976166306446')
CANON_K = 2 - CANON_H
# ARB sandwich from atone_xip_mt.py (recorded values)
kappa9_lo = mp.mpf('1.1321111338009971841357659371269669376742396330')
kappa9_hi = mp.mpf('1.1321111338009976121805011341151405510925567505')
EPS9 = mp.mpf('1024') / mp.mpf('2990212875')

# ---- independent mpmath recomputation (native, no shared code with the certificate)
sq2 = mp.sqrt(2)
def D1full(s):
    total = s - 4*s*s
    k = 0
    while True:
        c = 2*mp.mpf(4)**(k+1)*mp.factorial(k)/mp.factorial(2*k+2)
        term = c*s**(2*k+3)
        if abs(term) < mp.mpf(10)**(-90):
            break
        total += term
        k += 1
    return total
def D1trunc9(s):
    total = s - 4*s*s
    for k in range(9):
        c = 2*mp.mpf(4)**(k+1)*mp.factorial(k)/mp.factorial(2*k+2)
        total += c*s**(2*k+3)
    return total
def vconv(r):
    return mp.mpf(1)/2*((1-r)*mp.cos(sq2*r) + mp.sin(sq2*(1-r))/sq2)

Iv  = 2*mp.sin(1/mp.sqrt(2))/mp.sqrt(2)
Iv2 = mp.mpf(1)/2 + mp.sin(sq2)/(2*sq2)
# J1 (trunc9) and jWin (full D1), analytic vConv, via mpmath quadrature (evidence)
J1  = 2*mp.quad(lambda r: D1trunc9(r)*vconv(r), [0,1])
jw  = 2*mp.quad(lambda r: D1full(r)*vconv(r), [0,1])
kap_trunc = (Iv2 + J1)/(Iv**2)
kap_full  = (Iv2 + jw)/(Iv**2)
H_trunc = 2 - kap_trunc
H_full  = 2 - kap_full

print("========== INDEPENDENT mpmath cross-check (EVIDENCE) ==========")
print("Iv  =", mp.nstr(Iv, 50))
print("Iv2 =", mp.nstr(Iv2, 50), " (blueprint a = 0.84922799931830417992…)")
print("J1(trunc9) =", mp.nstr(J1, 50))
print("jWin(D1)   =", mp.nstr(jw, 50))
print("kappa1(trunc9) =", mp.nstr(kap_trunc, 50), "  (κ₉ reference)")
print("kappa1(full D1)= ", mp.nstr(kap_full, 50))
print("H(trunc9)  =", mp.nstr(H_trunc, 50))
print("H(full D1) =", mp.nstr(H_full, 50))
print()
print("canonical H_xip_MT =", mp.nstr(CANON_H, 40))
print("canonical kappa1   =", mp.nstr(CANON_K, 40))
print()

# check the sandwich contains the canonical value
contain_kap = kappa9_lo <= CANON_K <= kappa9_hi + EPS9
contain_H   = 2-(kappa9_hi+EPS9) <= CANON_H <= 2-kappa9_lo
print("sandwich κ₁(1,vMT) ∈ [κ₉, κ₉+ε₉] contains canonical κ₁ :", contain_kap)
print("  κ₉ =", mp.nstr(kappa9_lo, 40))
print("  κ₉+ε₉ =", mp.nstr(kappa9_hi + EPS9, 40))
print("  canonical κ₁ =", mp.nstr(CANON_K, 40))
print("H ∈ [2−(κ₉+ε₉), 2−κ₉] contains canonical H        :", contain_H)
print("  2−κ₉ =", mp.nstr(2-kappa9_hi, 40))
print("  2−(κ₉+ε₉) =", mp.nstr(2-(kappa9_hi+EPS9), 40))
print("  canonical H =", mp.nstr(CANON_H, 40))
print()

# also check the numeric agreement of our kappa_full mid with canonical to ~50 digits
print("|H_full − canonical| (agreement, should be < 1e-20):",
      mp.nstr(abs(H_full - CANON_H), 30))
print()
print("STATUS:", STATUS)
